/**
 * AgentBnB Auto-Request adapter for OpenClaw skill integration.
 * Delegates to AutoRequestor from src/autonomy/.
 * This is a thin re-export wrapper — no business logic lives here.
 */
import { AutoRequestor } from '../../src/autonomy/auto-request.js';
import type {
  AutoRequestOptions,
  CapabilityNeed,
  AutoRequestResult,
} from '../../src/autonomy/auto-request.js';

export { AutoRequestor };
export type { AutoRequestOptions, CapabilityNeed, AutoRequestResult };
