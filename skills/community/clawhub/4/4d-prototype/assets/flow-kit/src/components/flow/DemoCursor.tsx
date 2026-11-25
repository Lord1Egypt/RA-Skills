import { useEffect, useRef } from 'react';
import { ACTORS } from '@/flow/actors';
import { useClockFrozen, useSpeed } from '@/flow/clock';
import { cursorStore, cursorTarget } from '@/flow/cursor';
import { useFlow } from '@/flow/director';
import { USERS } from '@/state/session';
import { useStore } from '@/lib/store';

const NAME: Partial<Record<string, string>> = Object.fromEntries(Object.values(USERS).map((u) => [u.role, u.name]));

/**
 * Demo cursor: smoothly follows the target element (also while the page scrolls) and plays a ripple and press animation on click
 * (keyframes in flow-kit.css).
 * Lives in the browser top layer (popover) so it stays visible above <dialog>; re-raised after dialogs open or close; never intercepts mouse events.
 * Stops in place while the clock is frozen (paused); the label flips near the right / bottom edge so it is not clipped.
 */
export function DemoCursor() {
  const c = useStore(cursorStore, (s) => s);
  const active = useFlow((s) => s.active);
  const speed = useSpeed();
  const rootRef = useRef<HTMLDivElement>(null);
  const bodyRef = useRef<HTMLDivElement>(null);
  const labelRef = useRef<HTMLSpanElement>(null);
  const speedRef = useRef(speed);
  speedRef.current = speed;
  const frozen = useClockFrozen();
  const frozenRef = useRef(frozen);
  frozenRef.current = frozen;
  const pos = useRef({ x: 0, y: 0, init: false });

  useEffect(() => {
    try {
      rootRef.current?.showPopover?.();
    } catch {
      /* no popover support: fall back to a plain fixed layer */
    }
  }, []);

  useEffect(() => {
    if (!active) return;
    let raf = 0;
    let last = performance.now();
    let dialogs = -1;
    const frame = (t: number) => {
      const dt = Math.min(64, t - last);
      last = t;
      const node = bodyRef.current;
      const root = rootRef.current;
      const el = cursorTarget();
      if (node) {
        if (!pos.current.init) pos.current = { x: window.innerWidth * 0.55, y: window.innerHeight * 0.7, init: true };
        if (el && el.isConnected) {
          const r = el.getBoundingClientRect();
          const gx = r.left + Math.min(r.width / 2, 96);
          const gy = r.top + Math.min(r.height / 2, 18);
          const k = frozenRef.current ? 0 : 1 - Math.exp(-dt * 0.0105 * speedRef.current);
          pos.current.x += (gx - pos.current.x) * k;
          pos.current.y += (gy - pos.current.y) * k;
        }
        node.style.transform = `translate(${pos.current.x}px, ${pos.current.y}px)`;
        const lab = labelRef.current;
        if (lab) {
          const flipX = pos.current.x > window.innerWidth - 180;
          const flipY = pos.current.y > window.innerHeight - 48;
          lab.style.left = flipX ? 'auto' : '20px';
          lab.style.right = flipX ? '6px' : 'auto';
          lab.style.top = flipY ? '-22px' : '20px';
        }
      }
      const n = document.querySelectorAll('dialog[open]').length;
      if (n !== dialogs && root?.showPopover && root.hidePopover) {
        dialogs = n;
        try {
          root.hidePopover();
          root.showPopover();
        } catch {
          /* ignore */
        }
      }
      raf = requestAnimationFrame(frame);
    };
    raf = requestAnimationFrame(frame);
    return () => cancelAnimationFrame(raf);
  }, [active]);

  const a = ACTORS[c.actor];
  const shown = active && c.visible;
  return (
    <div
      ref={rootRef}
      popover="manual"
      aria-hidden="true"
      style={{ position: 'fixed', inset: 'auto', left: 0, top: 0, width: 0, height: 0, margin: 0, padding: 0, border: 0, background: 'transparent', overflow: 'visible', pointerEvents: 'none', zIndex: 9999 }}
    >
      <div ref={bodyRef} style={{ position: 'absolute', left: 0, top: 0, opacity: shown ? 1 : 0, transition: 'opacity 220ms ease-out', willChange: 'transform' }}>
        {c.clicks ? (
          <span
            key={c.clicks}
            style={{ position: 'absolute', left: -20, top: -20, width: 40, height: 40, borderRadius: 999, background: `color-mix(in srgb, ${a.color} 38%, transparent)`, animation: `cursor-click ${Math.round(650 / speed)}ms ease-out both` }}
          />
        ) : null}
        <svg
          key={`p-${c.clicks}`}
          width="26"
          height="26"
          viewBox="0 0 24 24"
          style={{ position: 'relative', filter: 'drop-shadow(0 2px 3px rgb(0 0 0 / 0.3))', animation: c.clicks ? `cursor-press ${Math.round(260 / speed)}ms ease-out both` : undefined, transformOrigin: '4px 3px' }}
        >
          <path d="M4 3l15 7-6.5 2L10 19z" fill={a.color} stroke="#fff" strokeWidth="1.7" strokeLinejoin="round" />
        </svg>
        <span
          ref={labelRef}
          style={{ position: 'absolute', left: 20, top: 20, whiteSpace: 'nowrap', borderRadius: 999, padding: '2px 8px', fontSize: 12, fontWeight: 500, color: '#fff', background: a.color, boxShadow: '0 2px 6px rgb(0 0 0 / 0.18)' }}
        >
          {a.short}
          {NAME[c.actor] ? ` · ${NAME[c.actor]}` : ''}
        </span>
      </div>
    </div>
  );
}
