import { reqStore, ruleStore } from './requests';
import { sessionStore } from './session';

/**
 * Clear data produced during demos and restore the initial state (used by the reset button on the assumptions page
 * and by "reset first" when starting a demo).
 * It pulls in large modules such as config stores and retained results: use it only through dynamic import, outside the first load.
 * Add per project: reset() of every config store / business data / case library store.
 */
export function resetDemo() {
  ruleStore.reset();
  reqStore.reset();
  sessionStore.reset();
}
