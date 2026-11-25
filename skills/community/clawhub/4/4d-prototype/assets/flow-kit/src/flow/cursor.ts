/**
 * The demo "mouse": moves to the element to operate, plays a click animation, then runs the action.
 * Cursor color and label show who is operating (human role · name); machine sub-steps (backend batch, agent, RPA) hide the cursor.
 * Clickable targets carry data-demo="…"; the main scroll region is <main id="main"> by convention.
 * Timing uses the demo virtual clock and scales with playback speed.
 */
import { createStore } from '@/lib/store';
import { HUMAN, type ActorKey } from './actors';
import { vSetTimeout } from './clock';

export interface CursorState {
  visible: boolean;
  actor: ActorKey;
  /** Click count (a change plays the click ripple) */
  clicks: number;
}

export const cursorStore = createStore<CursorState>('cursor', () => ({ visible: false, actor: HUMAN[0], clicks: 0 }), { persist: false });

export { HUMAN };

/** Virtual duration of the move, and when the press and the action happen (ms, scaled by playback speed) */
export const CURSOR_MOVE = 700;
const ACT_DELAY = 180;

let target: Element | null = null;
let pending = 0;
let hideAfter = false;

export function cursorTarget() {
  return target;
}

type Target = string | Element;

/** Find the element: right after a state change it may not be rendered yet, so retry for about 2 s */
function resolve(t: Target, cb: (el: Element | null) => void) {
  if (typeof t !== 'string') {
    cb(t);
    return;
  }
  let n = 0;
  const find = () => {
    const el = document.querySelector(t);
    if (el || n++ >= 20) cb(el);
    else window.setTimeout(find, 100);
  };
  find();
}

function bringIntoView(el: Element) {
  const r = el.getBoundingClientRect();
  // Elements in the main area use the main scroll region (the "Flow · Data" dock may sit at the bottom); elements in drawers / dialogs use the window
  const main = document.getElementById('main');
  const dock = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--flow-dock-h')) || 0;
  const box = main && main.contains(el) ? main.getBoundingClientRect() : { top: 0, bottom: window.innerHeight - dock };
  if (r.top < box.top + 64 || r.bottom > box.bottom - 24) el.scrollIntoView({ block: 'center', behavior: 'smooth' });
}

/** Move the cursor over an element (hover, no click) */
export function cursorHover(t: Target, actor: ActorKey, then?: () => void) {
  resolve(t, (el) => {
    if (!el) {
      then?.();
      return;
    }
    target = el;
    bringIntoView(el);
    hideAfter = false;
    cursorStore.set({ visible: true, actor });
    if (then) vSetTimeout(then, CURSOR_MOVE);
  });
}

/** Move the cursor to the element → click animation → run the action; if the element is not found, run the action directly */
export function cursorClick(t: Target, actor: ActorKey, fn?: () => void, guard: () => boolean = () => true) {
  pending++;
  hideAfter = false;
  const finish = () => {
    pending = Math.max(0, pending - 1);
    if (!pending && hideAfter) {
      hideAfter = false;
      cursorStore.set({ visible: false });
    }
  };
  resolve(t, (el) => {
    if (!guard()) {
      finish();
      return;
    }
    if (!el) {
      fn?.();
      finish();
      return;
    }
    target = el;
    bringIntoView(el);
    cursorStore.set({ visible: true, actor });
    vSetTimeout(() => {
      if (guard()) cursorStore.set((s) => ({ clicks: s.clicks + 1 }));
    }, CURSOR_MOVE);
    vSetTimeout(() => {
      if (guard()) fn?.();
      finish();
    }, CURSOR_MOVE + ACT_DELAY);
  });
}

/** Hide the cursor (if a click is still in progress, hide it when the click ends) */
export function hideCursor(force = false) {
  if (pending && !force) {
    hideAfter = true;
    return;
  }
  pending = 0;
  hideAfter = false;
  cursorStore.set({ visible: false });
}
