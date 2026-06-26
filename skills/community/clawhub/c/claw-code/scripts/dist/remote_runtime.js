/**
 * Remote Runtime Module
 * Supports: remote / ssh / teleport modes
 */
export function asText(report) {
    return `mode=${report.mode}\nconnected=${report.connected}\ndetail=${report.detail}`;
}
export function runRemoteMode(target) {
    return Object.freeze({
        mode: 'remote',
        connected: true,
        detail: `Remote control placeholder prepared for ${target}`,
    });
}
export function runSshMode(target) {
    return Object.freeze({
        mode: 'ssh',
        connected: true,
        detail: `SSH proxy placeholder prepared for ${target}`,
    });
}
export function runTeleportMode(target) {
    return Object.freeze({
        mode: 'teleport',
        connected: true,
        detail: `Teleport resume/create placeholder prepared for ${target}`,
    });
}
