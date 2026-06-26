/**
 * Direct Modes Module
 * Supports: direct-connect / deep-link modes
 */
export function asText(report) {
    return `mode=${report.mode}\ntarget=${report.target}\nactive=${report.active}`;
}
export function runDirectConnect(target) {
    return Object.freeze({
        mode: 'direct-connect',
        target,
        active: true,
    });
}
export function runDeepLink(target) {
    return Object.freeze({
        mode: 'deep-link',
        target,
        active: true,
    });
}
