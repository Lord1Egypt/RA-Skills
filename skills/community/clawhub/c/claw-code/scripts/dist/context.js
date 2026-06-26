// Context – workspace context mirrored from Python src/context.ts
// Note: Path resolution uses string-based paths since Node.js path module
// is used instead of Python's pathlib.
export function buildPortContext(_base) {
    // In the TypeScript port, we keep paths as logical strings.
    // The actual path resolution would use Node.js `path` module in a real implementation.
    return {
        source_root: '<src_root>',
        tests_root: '<tests_root>',
        assets_root: '<assets_root>',
        archive_root: '<archive_root>',
        python_file_count: 0,
        test_file_count: 0,
        asset_file_count: 0,
        archive_available: false,
    };
}
export function renderContext(context) {
    const lines = [
        `Source root: ${context.source_root}`,
        `Test root: ${context.tests_root}`,
        `Assets root: ${context.assets_root}`,
        `Archive root: ${context.archive_root}`,
        `Python files: ${context.python_file_count}`,
        `Test files: ${context.test_file_count}`,
        `Assets: ${context.asset_file_count}`,
        `Archive available: ${context.archive_available}`,
    ];
    return lines.join('\n');
}
