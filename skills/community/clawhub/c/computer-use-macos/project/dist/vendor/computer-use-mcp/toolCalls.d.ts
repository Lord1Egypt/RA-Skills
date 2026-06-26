/**
 * Tool dispatch. Every security decision from plan §2 is enforced HERE,
 * before any executor method is called.
 *
 * Enforcement order, every call:
 *   1. Kill switch (`adapter.isDisabled()`).
 *   2. TCC gate (`adapter.ensureOsPermissions()`). `request_access` is
 *      exempted — it threads the ungranted state to the renderer so the
 *      user can grant TCC perms from inside the approval dialog.
 *   3. Tool-specific gates (see dispatch table) — ANY exception in a gate
 *      returns a tool error, executor never called.
 *   4. Executor call.
 *
 * For input actions (click/type/key/scroll/drag/move_mouse) the tool-specific
 * gates are, in order:
 *   a. `prepareForAction` — hide every non-allowlisted app, then defocus us
 *      (battle-tested pre-action sequence from the Vercept acquisition).
 *      Sub-gated via `hideBeforeAction`. After this runs the screenshot is
 *      TRUE (what the
 *      model sees IS what's at each pixel) and we are not keyboard-focused.
 *   b. Frontmost gate — branched by actionKind:
 *        mouse:    frontmost ∈ allowlist ∪ {hostBundleId, Finder} → pass.
 *                  hostBundleId passes because the executor's
 *                  `withClickThrough` bracket makes us click-through.
 *        keyboard: frontmost ∈ allowlist ∪ {Finder} → pass.
 *                  hostBundleId → ERROR (safety net — defocus should have
 *                  moved us off; if it didn't, typing would go into our
 *                  own chat box).
 *      After step (a) this gate fires RARELY — only when something popped
 *      up between prepare and action, or the 5-try hide loop gave up.
 *      Checked FRESH on every call, not cached across calls.
 *
 * For click variants only, AFTER the above gates but BEFORE the executor call:
 *   c. Pixel-validation staleness check (sub-gated).
 */
import type { CallToolResult } from "@modelcontextprotocol/sdk/types.js";
import type { DisplayGeometry, InstalledApp, ScreenshotResult } from "./executor.js";
import type { AppGrant, ComputerUseHostAdapter, ComputerUseOverrides, CoordinateMode, CuAppPermTier, Logger, ResolvedAppRequest } from "./types.js";
/**
 * Categorical error classes for the cu_tool_call telemetry event. Never
 * free text — error messages may contain file paths / app content (PII).
 */
export type CuErrorKind = "allowlist_empty" | "tcc_not_granted" | "cu_lock_held" | "teach_mode_conflict" | "teach_mode_not_active" | "executor_threw" | "capture_failed" | "app_denied" | "bad_args" | "app_not_granted" | "tier_insufficient" | "feature_unavailable" | "state_conflict" | "grant_flag_required" | "display_error" | "other";
/**
 * Telemetry payload piggybacked on the result — populated by handlers,
 * consumed and stripped by the host wrapper (serverDef.ts) before the
 * result goes to the SDK. Same pattern as `screenshot`.
 */
export interface CuCallTelemetry {
    /** request_access / request_teach_access: apps NEWLY granted in THIS call
     *  (does NOT include idempotent re-grants of already-allowed apps). */
    granted_count?: number;
    /** request_access / request_teach_access: apps denied in THIS call */
    denied_count?: number;
    /** request_access / request_teach_access: apps safety-denied (browser) this call */
    denied_browser_count?: number;
    /** request_access / request_teach_access: apps safety-denied (terminal) this call */
    denied_terminal_count?: number;
    /** Categorical error class (only set when isError) */
    error_kind?: CuErrorKind;
}
/**
 * `CallToolResult` augmented with the screenshot payload. `bindSessionContext`
 * reads `result.screenshot` after a `screenshot` tool call and stashes it in a
 * closure cell for the next pixel-validation. MCP clients never see this
 * field — the host wrapper strips it before returning to the SDK.
 */
export type CuCallToolResult = CallToolResult & {
    screenshot?: ScreenshotResult;
    /** Piggybacked telemetry — stripped by the host wrapper before SDK return. */
    telemetry?: CuCallTelemetry;
};
/**
 * Extract (x, y) from `coordinate: [x, y]` tuple.
 * array of length 2, both non-negative numbers.
 */
declare function extractCoordinate(args: Record<string, unknown>, paramName?: string): [number, number] | Error;
/**
 * Convert model-space coordinates to the logical points that enigo expects.
 *
 *   - `normalized_0_100`: (x / 100) * display.width. `display` is fetched
 *     fresh per tool call — never cached across calls —
 *     so a mid-session display-settings change doesn't leave us stale.
 *   - `pixels`: the model sent image-space pixel coords (it read them off the
 *     last screenshot). With the 1568-px long-edge downsample, the
 *     screenshot-px → logical-pt ratio is `displayWidth / screenshotWidth`,
 *     NOT `1/scaleFactor`. Uses the display geometry stashed at CAPTURE time
 *     (`lastScreenshot.displayWidth`), not fresh — so the transform matches
 *     what the model actually saw even if the user changed display settings
 *     since. (Chrome's ScreenshotContext pattern — CDPService.ts:1486-1493.)
 */
declare function scaleCoord(rawX: number, rawY: number, mode: CoordinateMode, display: DisplayGeometry, lastScreenshot: ScreenshotResult | undefined, logger: Logger): {
    x: number;
    y: number;
};
/**
 * Convert model-space coordinates to the 0–100 percentage that
 * pixelCompare.ts works in. The staleness check operates in screenshot-image
 * space; comparing by percentage lets us crop both last and fresh screenshots
 * at the same relative location without caring about their absolute dims.
 *
 * With the 1568-px downsample, `screenshot.width != display.width * sf`, so
 * the old `rawX / (display.width * sf)` formula is wrong. The correct
 * denominator is just `lastScreenshot.width` — the model's raw pixel coord is
 * already in that image's coordinate space. `DisplayGeometry` is no longer
 * consumed at all.
 */
declare function coordToPercentageForPixelCompare(rawX: number, rawY: number, mode: CoordinateMode, lastScreenshot: ScreenshotResult | undefined): {
    xPct: number;
    yPct: number;
};
/**
 * Tier needed to perform a given action class. `undefined` → `"full"`.
 *
 *   - `"mouse_position"` — mouse_move only. Passes at any tier including
 *     `"read"`. Pure cursor positioning, no app interaction. Still runs
 *     prepareForAction (hide non-allowed apps).
 *   - `"mouse"` — plain left click, double/triple, scroll, drag-from.
 *     Requires tier `"click"` or `"full"`.
 *   - `"mouse_full"` — right/middle click, any click with modifiers,
 *     drag-drop (the `to` endpoint of left_click_drag). Requires tier
 *     `"full"`. Right-click → context menu Paste, modifier chords →
 *     keystrokes before click, drag-drop → text insertion at the drop
 *     point. All escalate a click-tier grant to keyboard-equivalent input.
 *     Blunt: also rejects same-app drags (scrollbar, panel resize) onto
 *     click-tier apps; `scroll` is the tier-"click" way to scroll.
 *   - `"keyboard"` — type, key, hold_key. Requires tier `"full"`.
 */
type CuActionKind = "mouse_position" | "mouse" | "mouse_full" | "keyboard";
declare function tierSatisfies(grantTier: CuAppPermTier | undefined, actionKind: CuActionKind): boolean;
declare function decodedByteLength(base64: string): number;
declare function segmentGraphemes(text: string): string[];
/**
 * Split a chord string like "ctrl+shift" into individual key names.
 * Same parsing as `key` tool / executor.key / keyBlocklist.normalizeKeySequence.
 */
declare function parseKeyChord(text: string): string[];
/** Clears the cross-call drag flags. Called from Gate-3 on lock-acquire and
 *  from `bindSessionContext` in mcpServer.ts — a fresh lock holder must not
 *  inherit a prior session's mid-drag state. */
export declare function resetMouseButtonHeld(): void;
/**
 * Tools that check the lock but don't acquire it. `request_access` and
 * `list_granted_applications` hit the CHECK (so a blocked session doesn't
 * show an approval dialog for access it can't use) but defer ACQUIRE — the
 * enter-CU notification/overlay only fires on the first action tool.
 *
 * `request_teach_access` is NOT here: approving teach mode hides the main
 * window, and the lock must be held before that. See Gate-3 block in
 * `handleToolCall` for the full explanation.
 *
 * Exported for `bindSessionContext` in mcpServer.ts so the async lock gate
 * uses the same set as the sync one.
 */
export declare function defersLockAcquire(toolName: string): boolean;
declare function looksLikeBundleId(s: string): boolean;
declare function resolveRequestedApps(requestedNames: string[], installed: InstalledApp[], alreadyGrantedBundleIds: ReadonlySet<string>): ResolvedAppRequest[];
/**
 * Shared app-resolution + partition + hide-preview pipeline. Extracted from
 * `handleRequestAccess` so `handleRequestTeachAccess` can call the same path.
 *
 * Does the full app-name→InstalledApp resolution, assigns each a tier
 * (browser→"read", terminal/IDE→"click", else "full" — see deniedApps.ts),
 * splits into already-granted (skip the dialog, preserve grantedAt+tier) vs
 * need-dialog, and computes the willHide preview. Unlike the previous
 * hard-deny model, ALL apps proceed to the dialog; the tier just constrains
 * what actions are allowed once granted.
 */
/** An app assigned a restricted tier (not `"full"`). Used to build the
 *  guidance message telling the model what it can/can't do. */
interface TieredApp {
    bundleId: string;
    displayName: string;
    /** Never `"full"` — only restricted tiers are collected. */
    tier: "read" | "click";
}
interface AccessRequestParts {
    needDialog: ResolvedAppRequest[];
    skipDialogGrants: AppGrant[];
    willHide: Array<{
        bundleId: string;
        displayName: string;
    }>;
    /** Resolved apps with `proposedTier !== "full"` — for the guidance text.
     *  Unresolved apps are omitted (they go to `denied` with `not_installed`).  */
    tieredApps: TieredApp[];
    /** Apps stripped by the user's Settings auto-deny list. Surfaced in the
     *  response with guidance; never reach the dialog. */
    userDenied: Array<{
        requestedName: string;
        displayName: string;
    }>;
    /** Apps stripped by the baked-in policy blocklist (streaming/music/ebooks,
     *  etc. — `deniedApps.isPolicyDenied`). Precedence over userDenied. */
    policyDenied: Array<{
        requestedName: string;
        displayName: string;
    }>;
}
declare function buildAccessRequest(adapter: ComputerUseHostAdapter, apps: string[], allowedApps: AppGrant[], userDeniedBundleIds: ReadonlySet<string>, selectedDisplayId?: number): Promise<AccessRequestParts>;
/**
 * Build guidance text for apps granted at a restricted tier. Returned
 * inline in the okJson response so the model knows upfront what it can
 * do with each app, instead of learning by hitting the tier gate.
 */
declare function buildTierGuidanceMessage(tiered: TieredApp[]): string;
/**
 * Build guidance text for apps stripped by the user's Settings auto-deny
 * list. Returned inline in the okJson response so the agent knows (a) the
 * app is auto-denied by request_access and (b) the escape hatch
 * is to ask the human to edit Settings, not to retry or reword the request.
 */
declare function buildUserDeniedGuidance(userDenied: Array<{
    requestedName: string;
    displayName: string;
}>): string;
/**
 * Assign a human-readable label to each display. Falls back to `display N`
 * when NSScreen.localizedName is undefined; disambiguates identical labels
 * (matched-pair external monitors) with a `(2)` suffix. Used by both
 * buildMonitorNote and handleSwitchDisplay so the name the model sees in a
 * screenshot note is the same name it can pass back to switch_display.
 */
declare function uniqueDisplayLabels(displays: readonly DisplayGeometry[]): Map<number, string>;
/**
 * Build the monitor-context text that accompanies a screenshot. Tells the
 * model which monitor it's looking at (by human name), lists other attached
 * monitors, and flags when the monitor changed vs. the previous screenshot.
 *
 * Only emitted when there are 2+ displays AND (first screenshot OR the
 * display changed). Single-monitor setups and steady-state same-monitor
 * screenshots get no text — avoids noise.
 */
declare function buildMonitorNote(adapter: ComputerUseHostAdapter, shotDisplayId: number, lastDisplayId: number | undefined, canSwitchDisplay: boolean): Promise<string | undefined>;
declare function handleSwitchDisplay(adapter: ComputerUseHostAdapter, args: Record<string, unknown>, overrides: ComputerUseOverrides): Promise<CuCallToolResult>;
export declare function handleToolCall(adapter: ComputerUseHostAdapter, name: string, args: unknown, rawOverrides: ComputerUseOverrides): Promise<CuCallToolResult>;
export declare const _test: {
    scaleCoord: typeof scaleCoord;
    coordToPercentageForPixelCompare: typeof coordToPercentageForPixelCompare;
    segmentGraphemes: typeof segmentGraphemes;
    decodedByteLength: typeof decodedByteLength;
    resolveRequestedApps: typeof resolveRequestedApps;
    buildAccessRequest: typeof buildAccessRequest;
    buildTierGuidanceMessage: typeof buildTierGuidanceMessage;
    buildUserDeniedGuidance: typeof buildUserDeniedGuidance;
    tierSatisfies: typeof tierSatisfies;
    looksLikeBundleId: typeof looksLikeBundleId;
    extractCoordinate: typeof extractCoordinate;
    parseKeyChord: typeof parseKeyChord;
    buildMonitorNote: typeof buildMonitorNote;
    handleSwitchDisplay: typeof handleSwitchDisplay;
    uniqueDisplayLabels: typeof uniqueDisplayLabels;
};
export {};
