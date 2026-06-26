import { format } from 'node:util';
import { logDebug, logWarn } from '../lib/log.js';
import { COMPUTER_USE_MCP_SERVER_NAME } from './common.js';
import { createCliExecutor } from './executor.js';
import { getChicagoEnabled, getChicagoSubGates } from './gates.js';
import { callPythonHelper } from './pythonBridge.js';
class DebugLogger {
    silly(message, ...args) { logDebug(format(message, ...args)); }
    debug(message, ...args) { logDebug(format(message, ...args)); }
    info(message, ...args) { logDebug(format(message, ...args)); }
    warn(message, ...args) { logWarn(format(message, ...args)); }
    error(message, ...args) { logWarn(format(message, ...args)); }
}
let cached;
export function getComputerUseHostAdapter() {
    if (cached)
        return cached;
    cached = {
        serverName: COMPUTER_USE_MCP_SERVER_NAME,
        logger: new DebugLogger(),
        executor: createCliExecutor({
            getMouseAnimationEnabled: () => getChicagoSubGates().mouseAnimation,
            getHideBeforeActionEnabled: () => getChicagoSubGates().hideBeforeAction,
        }),
        ensureOsPermissions: async () => {
            const perms = await callPythonHelper('check_permissions', {});
            return perms.accessibility && perms.screenRecording
                ? { granted: true }
                : { granted: false, accessibility: perms.accessibility, screenRecording: perms.screenRecording };
        },
        isDisabled: () => !getChicagoEnabled(),
        getSubGates: getChicagoSubGates,
        getAutoUnhideEnabled: () => true,
        cropRawPatch: () => null,
    };
    return cached;
}
//# sourceMappingURL=hostAdapter.js.map