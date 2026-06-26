/**
 * Parity Audit – compare TypeScript port against the archived snapshot.
 * Mirrored from Python src/parity_audit.py
 *
 * Strict mode: enabled (tsconfig.json strict:true)
 */
export interface ParityAuditResult {
    readonly archive_present: boolean;
    readonly root_file_coverage: readonly [number, number];
    readonly directory_coverage: readonly [number, number];
    readonly total_file_ratio: readonly [number, number];
    readonly command_entry_ratio: readonly [number, number];
    readonly tool_entry_ratio: readonly [number, number];
    readonly missing_root_targets: readonly string[];
    readonly missing_directory_targets: readonly string[];
}
/**
 * Render the parity audit result as a Markdown string.
 */
export declare function parityAuditAsMarkdown(result: ParityAuditResult): string;
/**
 * Stub parity audit – returns a placeholder result.
 * A full implementation would read the archive snapshot and compare file coverage.
 */
export declare function runParityAudit(): ParityAuditResult;
