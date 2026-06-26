// Prefetch – side-effect prefetch results (stub)
// Mirrored from Python src/prefetch.py
export function startMdmRawRead() {
    return { name: 'mdm_raw_read', detail: 'stub prefetch – no-op' };
}
export function startKeychainPrefetch() {
    return { name: 'keychain_prefetch', detail: 'stub prefetch – no-op' };
}
export function startProjectScan(_root) {
    return { name: 'project_scan', detail: `stub prefetch for root=${_root}` };
}
