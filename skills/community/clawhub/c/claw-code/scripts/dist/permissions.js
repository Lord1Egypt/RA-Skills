/**
 * Permission context for blocking tool access.
 * TypeScript port of permissions.py with strict mode.
 */
/**
 * Encapsulates deny-lists for tool names and name prefixes.
 * Use ToolPermissionContext.fromIterables() to construct from optional arrays.
 *
 * Mirrors the Python @dataclass(frozen=True) ToolPermissionContext.
 */
export class ToolPermissionContext {
    constructor(args) {
        this.denyNames = args?.denyNames ?? new Set();
        this.denyPrefixes = args?.denyPrefixes ?? [];
    }
    /**
     * Factory: build a ToolPermissionContext from optional arrays of
     * deny-names and deny-prefixes. All values are lower-cased.
     *
     * Mirrors the Python classmethod `from_iterables`.
     */
    static fromIterables(denyNames, denyPrefixes) {
        const names = denyNames ?? [];
        const prefixes = denyPrefixes ?? [];
        return new ToolPermissionContext({
            denyNames: new Set(names.map((n) => n.toLowerCase())),
            denyPrefixes: prefixes.map((p) => p.toLowerCase()),
        });
    }
    /**
     * Returns true when the given tool name is blocked by either the exact-name
     * deny-list or any of the prefix deny-list entries.
     *
     * Mirrors the Python method `blocks`.
     */
    blocks(toolName) {
        const lowered = toolName.toLowerCase();
        if (this.denyNames.has(lowered)) {
            return true;
        }
        return this.denyPrefixes.some((prefix) => lowered.startsWith(prefix));
    }
}
