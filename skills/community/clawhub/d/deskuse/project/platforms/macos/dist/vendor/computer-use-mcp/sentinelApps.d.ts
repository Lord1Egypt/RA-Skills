/**
 * Bundle IDs that are escalations-in-disguise. The approval UI shows a warning
 * badge for these; they are NOT blocked. Power users may legitimately want the
 * model controlling a terminal.
 *
 * Imported by the renderer via the `./sentinelApps` subpath (package.json
 * `exports`), which keeps Next.js from reaching index.ts → mcpServer.ts →
 * @modelcontextprotocol/sdk (devDep, would fail module resolution). Keep
 * this file import-free so the subpath stays clean.
 */
export declare const SENTINEL_BUNDLE_IDS: ReadonlySet<string>;
export type SentinelCategory = "shell" | "filesystem" | "system_settings";
export declare function getSentinelCategory(bundleId: string): SentinelCategory | null;
