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
export declare class ToolPermissionContext {
    readonly denyNames: ReadonlySet<string>;
    readonly denyPrefixes: readonly string[];
    constructor(args?: {
        denyNames?: ReadonlySet<string>;
        denyPrefixes?: readonly string[];
    });
    /**
     * Factory: build a ToolPermissionContext from optional arrays of
     * deny-names and deny-prefixes. All values are lower-cased.
     *
     * Mirrors the Python classmethod `from_iterables`.
     */
    static fromIterables(denyNames?: readonly string[] | null, denyPrefixes?: readonly string[] | null): ToolPermissionContext;
    /**
     * Returns true when the given tool name is blocked by either the exact-name
     * deny-list or any of the prefix deny-list entries.
     *
     * Mirrors the Python method `blocks`.
     */
    blocks(toolName: string): boolean;
}
