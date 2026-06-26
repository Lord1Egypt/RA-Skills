import type { ComputerUseHostAdapter, Logger } from '../vendor/computer-use-mcp/types.js'
import { format } from 'node:util'
import { logDebug, logWarn } from '../lib/log.js'
import { COMPUTER_USE_MCP_SERVER_NAME } from './common.js'
import { createCliExecutor } from './executor.js'
import { getChicagoEnabled, getChicagoSubGates } from './gates.js'
import { callPythonHelper } from './pythonBridge.js'

class DebugLogger implements Logger {
  silly(message: string, ...args: unknown[]): void { logDebug(format(message, ...args)) }
  debug(message: string, ...args: unknown[]): void { logDebug(format(message, ...args)) }
  info(message: string, ...args: unknown[]): void { logDebug(format(message, ...args)) }
  warn(message: string, ...args: unknown[]): void { logWarn(format(message, ...args)) }
  error(message: string, ...args: unknown[]): void { logWarn(format(message, ...args)) }
}

let cached: ComputerUseHostAdapter | undefined

export function getComputerUseHostAdapter(): ComputerUseHostAdapter {
  if (cached) return cached
  cached = {
    serverName: COMPUTER_USE_MCP_SERVER_NAME,
    logger: new DebugLogger(),
    executor: createCliExecutor({
      getMouseAnimationEnabled: () => getChicagoSubGates().mouseAnimation,
      getHideBeforeActionEnabled: () => getChicagoSubGates().hideBeforeAction,
    }),
    ensureOsPermissions: async () => {
      const perms = await callPythonHelper<{ accessibility: boolean; screenRecording: boolean }>('check_permissions', {})
      return perms.accessibility && perms.screenRecording
        ? { granted: true as const }
        : { granted: false as const, accessibility: perms.accessibility, screenRecording: perms.screenRecording }
    },
    isDisabled: () => !getChicagoEnabled(),
    getSubGates: getChicagoSubGates,
    getAutoUnhideEnabled: () => true,
    cropRawPatch: () => null,
  }
  return cached
}
