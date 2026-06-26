/**
 * init.ts — cc-soul 初始化（从 handler.ts 拆出）
 *
 * 单一职责：初始化系统状态。
 * soul-process.ts 和 plugin-entry.ts 都调这里。
 * handler.ts re-export 以保持向后兼容。
 */

let _initialized = false
export function getInitialized(): boolean { return _initialized }
export function setInitialized(v: boolean): void { _initialized = v }

export function initializeSoul(): void {
  if (_initialized) return
  _initialized = true

  // Lightweight init only — no memory loading
  try { require('./persistence.ts').ensureDataDir() } catch {}
  try { require('./cli.ts').loadAIConfig() } catch {}
  try { require('./body.ts').loadBodyState() } catch {}
  try { require('./memory.ts').ensureSQLiteReady() } catch (e: any) { console.error('[cc-soul] SQLite init failed:', e.message) }
  try { require('./features.ts').loadFeatures() } catch {}
  try { require('./handler-state.ts').loadStats() } catch {}
  try { require('./user-profiles.ts').loadProfiles() } catch {}
  try { require('./distill.ts').loadDistillState() } catch {}
  try { require('./absence-detection.ts').loadAbsenceState() } catch {}

  console.log(`[cc-soul] initializeSoul done (from init.ts)`)
}
