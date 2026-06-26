import { logDebug, logWarn } from '../lib/log.js'
import { releasePump, retainPump } from './drainRunLoop.js'
import { requireComputerUseSwift } from './swiftLoader.js'

let registered = false

export function registerEscHotkey(onEscape: () => void): boolean {
  if (registered) return true
  const cu = requireComputerUseSwift()
  if (!cu.hotkey?.registerEscape?.(onEscape)) {
    logWarn('escape hotkey registration failed')
    return false
  }
  retainPump()
  registered = true
  logDebug('escape hotkey registered')
  return true
}

export function unregisterEscHotkey(): void {
  if (!registered) return
  try {
    requireComputerUseSwift().hotkey.unregister()
  } finally {
    releasePump()
    registered = false
    logDebug('escape hotkey unregistered')
  }
}

export function notifyExpectedEscape(): void {
  if (!registered) return
  requireComputerUseSwift().hotkey.notifyExpectedEscape()
}
