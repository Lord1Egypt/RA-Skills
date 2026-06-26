/**
 * MCP tool schemas for the computer-use server. Mirrors
 * claude-for-chrome-mcp/src/browserTools.ts in shape (plain `Tool`-shaped
 * object literals, no zod).
 *
 * Coordinate descriptions are baked in at tool-list build time from the
 * `chicago_coordinate_mode` gate. The model sees exactly ONE coordinate
 * convention in the param descriptions and never learns the other exists.
 * The host (`serverDef.ts`) reads the same frozen gate value for
 * `scaleCoord` — both must agree or clicks land in the wrong space.
 */
import type { Tool } from "@modelcontextprotocol/sdk/types.js";
import type { CoordinateMode } from "./types.js";
/**
 * Build the tool list. Parameterized by capabilities and coordinate mode so
 * descriptions are honest and unambiguous (plan §1 — "Unfiltered + honest").
 *
 * `coordinateMode` MUST match what the host passes to `scaleCoord` at tool-
 * -call time. Both should read the same frozen-at-load gate constant.
 *
 * `installedAppNames` — optional pre-sanitized list of app display names to
 * enumerate in the `request_access` description. The caller is responsible
 * for sanitization (length cap, character allowlist, sort, count cap) —
 * this function just splices the list into the description verbatim. Omit
 * to fall back to the generic "display names or bundle IDs" wording.
 */
export declare function buildComputerUseTools(caps: {
    screenshotFiltering: "native" | "none";
    platform: "darwin" | "win32";
    /** Include request_teach_access + teach_step. Read once at server construction. */
    teachMode?: boolean;
}, coordinateMode: CoordinateMode, installedAppNames?: string[]): Tool[];
