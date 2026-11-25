/**
 * Sub-step "spotlight": when the demo reaches a sub-step —
 * - the sub-step has an anchor: scroll to the matching data-flow-anchor region and highlight it (.flow-spotlight, see flow-kit.css);
 * - the sub-step is performed by a machine (backend, scheduler, external system, RPA, agent): hide the human cursor;
 * - a walk step (advanced by the director, no page script moves the cursor) viewed by a human: hover the cursor over the region;
 * - the demo ends: hide the cursor.
 * Call it once in the shell (the worked examples call it inside the floating navigator).
 */
import { useEffect } from 'react';
import { HUMAN, cursorHover, hideCursor } from './cursor';
import { flowStore, useFlow } from './director';
import { STEPS } from './workflow';

export function useFlowSpotlight() {
  const key = useFlow((s) => (s.active ? `${s.nonce}:${s.sub}` : ''));
  useEffect(() => {
    if (!key) {
      hideCursor(true);
      return;
    }
    const s = flowStore.get();
    const step = STEPS[s.idx];
    const sub = step?.subs[s.sub];
    if (sub && !HUMAN.includes(sub.actor)) hideCursor();
    const anchor = sub?.anchor;
    if (!step || !sub || !anchor) return;
    let tries = 0;
    let el: HTMLElement | null = null;
    let t = 0;
    const find = () => {
      el = document.querySelector<HTMLElement>(`[data-flow-anchor="${anchor}"]`);
      if (el) {
        const tall = el.getBoundingClientRect().height > window.innerHeight * 0.6;
        el.scrollIntoView({ behavior: 'smooth', block: tall ? 'start' : 'center' });
        el.classList.add('flow-spotlight');
        if (step.drive === 'walk' && HUMAN.includes(sub.actor)) cursorHover(el, sub.actor);
      } else if (tries++ < 16) t = window.setTimeout(find, 250);
    };
    t = window.setTimeout(find, 120);
    return () => {
      window.clearTimeout(t);
      el?.classList.remove('flow-spotlight');
    };
  }, [key]);
}
