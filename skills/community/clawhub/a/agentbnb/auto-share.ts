/**
 * AgentBnB Auto-Share adapter for OpenClaw skill integration.
 * Delegates to IdleMonitor from src/autonomy/.
 * This is a thin re-export wrapper — no business logic lives here.
 */
import { IdleMonitor } from '../../src/autonomy/idle-monitor.js';
import type { IdleMonitorOptions } from '../../src/autonomy/idle-monitor.js';

export { IdleMonitor };
export type { IdleMonitorOptions };
