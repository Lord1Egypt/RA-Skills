/**
 * Parity Audit – compare TypeScript port against the archived snapshot.
 * Mirrored from Python src/parity_audit.py
 *
 * Strict mode: enabled (tsconfig.json strict:true)
 */
/**
 * Render the parity audit result as a Markdown string.
 */
export function parityAuditAsMarkdown(result) {
    const lines = ['# Parity Audit'];
    if (!result.archive_present) {
        lines.push('Local archive unavailable; parity audit cannot compare against the original snapshot.');
        return lines.join('\n');
    }
    lines.push('');
    lines.push(`Root file coverage: **${result.root_file_coverage[0]}/${result.root_file_coverage[1]}**`);
    lines.push(`Directory coverage: **${result.directory_coverage[0]}/${result.directory_coverage[1]}**`);
    lines.push(`Total Python files vs archived TS-like files: **${result.total_file_ratio[0]}/${result.total_file_ratio[1]}**`);
    lines.push(`Command entry coverage: **${result.command_entry_ratio[0]}/${result.command_entry_ratio[1]}**`);
    lines.push(`Tool entry coverage: **${result.tool_entry_ratio[0]}/${result.tool_entry_ratio[1]}**`);
    lines.push('');
    lines.push('Missing root targets:');
    if (result.missing_root_targets.length > 0) {
        for (const item of result.missing_root_targets) {
            lines.push(`- ${item}`);
        }
    }
    else {
        lines.push('- none');
    }
    lines.push('');
    lines.push('Missing directory targets:');
    if (result.missing_directory_targets.length > 0) {
        for (const item of result.missing_directory_targets) {
            lines.push(`- ${item}`);
        }
    }
    else {
        lines.push('- none');
    }
    return lines.join('\n');
}
/**
 * Stub parity audit – returns a placeholder result.
 * A full implementation would read the archive snapshot and compare file coverage.
 */
export function runParityAudit() {
    return {
        archive_present: false,
        root_file_coverage: [0, 0],
        directory_coverage: [0, 0],
        total_file_ratio: [0, 0],
        command_entry_ratio: [0, 0],
        tool_entry_ratio: [0, 0],
        missing_root_targets: [],
        missing_directory_targets: [],
    };
}
