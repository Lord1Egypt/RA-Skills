// Port Manifest – workspace manifest mirrored from Python src/port_manifest.py
export function buildPortManifest(_srcRoot) {
    // Stub: returns an empty manifest. Real implementation would scan the filesystem.
    return {
        src_root: _srcRoot ?? '<port_root>',
        total_python_files: 0,
        top_level_modules: [],
    };
}
