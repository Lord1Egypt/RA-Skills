/**
 * App category lookup for tiered CU permissions. Three categories land at a
 * restricted tier instead of `"full"`:
 *
 *   - **browser** → `"read"` tier — visible in screenshots, NO interaction.
 *     The model can read an already-open page but must use the Claude-in-Chrome
 *     MCP for navigation/clicking/typing.
 *   - **terminal** → `"click"` tier — visible + clickable, NO typing. The
 *     model can click a Run button or scroll test output in an IDE, but can't
 *     type into the integrated terminal. Use the Bash tool for shell work.
 *   - **trading** → `"read"` tier — same restrictions as browsers, but no
 *     CiC-MCP alternative exists. For platforms where a stray click can
 *     execute a trade or send a message to a counterparty.
 *
 * Uncategorized apps default to `"full"`. See `getDefaultTierForApp`.
 *
 * Identification is two-layered:
 *   1. Bundle ID match (macOS-only; `InstalledApp.bundleId` is a
 *      CFBundleIdentifier and meaningless on Windows). Fast, exact, the
 *      primary mechanism while CU is darwin-gated.
 *   2. Display-name substring match (cross-platform fallback). Catches
 *      unresolved requests ("Chrome" when Chrome isn't installed) AND will
 *      be the primary mechanism on Windows/Linux where there's no bundle ID.
 *      Windows-relevant names (PowerShell, cmd, Windows Terminal) are
 *      included now so they activate the moment the darwin gate lifts.
 *
 * Keep this file **import-free** (like sentinelApps.ts) — the renderer may
 * import it via a package.json subpath export, and pulling in
 * `@modelcontextprotocol/sdk` (a devDep) through the index → mcpServer chain
 * would fail module resolution in Next.js. The `CuAppPermTier` type is
 * duplicated as a string literal below rather than imported.
 */
export type DeniedCategory = "browser" | "terminal" | "trading";
/**
 * Map a category to its hardcoded tier. Return-type is the string-literal
 * union inline (this file is import-free; see header comment). The
 * authoritative type is `CuAppPermTier` in types.ts — keep in sync.
 *
 * Not bijective — both `"browser"` and `"trading"` map to `"read"`. Copy
 * that differs by category (the "use CiC" hint is browser-only) must check
 * the category, not just the tier.
 */
export declare function categoryToTier(category: DeniedCategory | null): "read" | "click" | "full";
/**
 * Policy-level auto-deny. Unlike `userDeniedBundleIds` (per-user Settings
 * page), this is baked into the build. `buildAccessRequest` strips these
 * before the approval dialog with "blocked by policy" guidance; the agent
 * is told to not retry.
 */
export declare function isPolicyDenied(bundleId: string | undefined, displayName: string): boolean;
export declare function getDeniedCategory(bundleId: string): DeniedCategory | null;
/**
 * Display-name substring match. Called when bundle-ID resolution returned
 * nothing (`resolved === undefined`) or when no bundle-ID deny-list entry
 * matched. Returns the category for the first matching substring, or null.
 *
 * Case-insensitive, substring — so `"Google Chrome"`, `"chrome"`, and
 * `"Chrome Canary"` all match the `"chrome"` entry.
 */
export declare function getDeniedCategoryByDisplayName(name: string): DeniedCategory | null;
/**
 * Combined check — bundle ID first (exact, fast), then display-name
 * fallback. This is the function tool-call handlers should use.
 *
 * `bundleId` may be undefined (unresolved request — model asked for an app
 * that isn't installed or Spotlight didn't find). In that case only the
 * display-name check runs.
 */
export declare function getDeniedCategoryForApp(bundleId: string | undefined, displayName: string): DeniedCategory | null;
/**
 * Default tier for an app at grant time. Wraps `getDeniedCategoryForApp` +
 * `categoryToTier`. Browsers → `"read"`, terminals/IDEs → `"click"`,
 * everything else → `"full"`.
 *
 * Called by `buildAccessRequest` to populate `ResolvedAppRequest.proposedTier`
 * before the approval dialog shows.
 */
export declare function getDefaultTierForApp(bundleId: string | undefined, displayName: string): "read" | "click" | "full";
export declare const _test: {
    BROWSER_BUNDLE_IDS: ReadonlySet<string>;
    TERMINAL_BUNDLE_IDS: ReadonlySet<string>;
    TRADING_BUNDLE_IDS: ReadonlySet<string>;
    POLICY_DENIED_BUNDLE_IDS: ReadonlySet<string>;
    BROWSER_NAME_SUBSTRINGS: readonly string[];
    TERMINAL_NAME_SUBSTRINGS: readonly string[];
    TRADING_NAME_SUBSTRINGS: readonly string[];
    POLICY_DENIED_NAME_SUBSTRINGS: readonly string[];
};
