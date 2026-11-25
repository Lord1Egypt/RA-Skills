import { useEffect, type ReactNode } from 'react';
import { SPEEDS, useSpeed, type Speed } from '@/flow/clock';
import { flowPrefs, nextStep, prevStep, restartFlow, setFlowMode, setFlowSpeed, stopFlow, togglePlay, useFlow, type FlowMode, type FlowState } from '@/flow/director';
import { STEPS } from '@/flow/workflow';

/**
 * Playback controls live in exactly one place — a centered floating capsule (role=toolbar, so scripts can read its state).
 * Styling uses neutral Tailwind utilities; swap in the project's own buttons / segmented controls when integrating.
 */
export const SPEED_LABEL: Record<Speed, string> = { 0.25: '0.25×', 0.5: '0.5×', 1: '1×', 2: '2×' };

const ICON: Record<'prev' | 'play' | 'pause' | 'next' | 'stop' | 'replay', ReactNode> = {
  prev: <path d="M7 5v14M19 5l-9 7 9 7z" />,
  play: <path d="M8 5l11 7-11 7z" />,
  pause: <path d="M8 5v14M16 5v14" />,
  next: <path d="M17 5v14M5 5l9 7-9 7z" />,
  stop: <rect x="6" y="6" width="12" height="12" rx="1.5" />,
  replay: <path d="M4 12a8 8 0 1 0 2.3-5.6M4 4v4h4" />,
};

function RoundBtn({ icon, label, onClick, disabled, primary }: { icon: keyof typeof ICON; label: string; onClick: () => void; disabled?: boolean; primary?: boolean }) {
  const size = primary ? 44 : 36;
  return (
    <button
      type="button"
      aria-label={label}
      title={label}
      onClick={onClick}
      disabled={disabled}
      className={`flex shrink-0 items-center justify-center rounded-full transition-[background-color,transform] duration-150 active:scale-95 disabled:cursor-not-allowed disabled:opacity-35 ${primary ? 'bg-primary-500 text-white hover:brightness-[1.06]' : 'bg-ink-950/[0.06] text-ink-800 hover:bg-ink-950/[0.1]'}`}
      style={{ width: size, height: size }}
    >
      <svg width={primary ? 20 : 16} height={primary ? 20 : 16} viewBox="0 0 24 24" fill={icon === 'play' || icon === 'prev' || icon === 'next' ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
        {ICON[icon]}
      </svg>
    </button>
  );
}

function Segmented<T extends string>({ value, items, onChange }: { value: T; items: { value: T; label: string }[]; onChange: (v: T) => void }) {
  return (
    <div className="inline-flex rounded-full bg-ink-950/[0.06] p-0.5" role="radiogroup">
      {items.map((it) => (
        <button
          key={it.value}
          type="button"
          role="radio"
          aria-checked={it.value === value}
          onClick={() => onChange(it.value)}
          className={`rounded-full px-2.5 py-1 text-xs font-medium ${it.value === value ? 'bg-surface text-ink-900 shadow-sm' : 'text-ink-600'}`}
        >
          {it.label}
        </button>
      ))}
    </div>
  );
}

/** Playback speed: adjustable at any time, applies immediately to the director, page scripts, animations and the cursor */
export function SpeedControl() {
  const speed = useSpeed() as Speed;
  return <Segmented<string> value={String(speed)} onChange={(v) => setFlowSpeed(Number(v) as Speed)} items={SPEEDS.map((x) => ({ value: String(x), label: SPEED_LABEL[x] }))} />;
}

export function ModeControl({ f }: { f: FlowState }) {
  return (
    <Segmented<FlowMode>
      value={f.mode}
      onChange={setFlowMode}
      items={[
        { value: 'auto', label: '自动连播' },
        { value: 'step', label: '逐步' },
      ]}
    />
  );
}

/** Big playback controls: previous / pause·resume / next / stop; after finishing: run again / stop */
export function BigControls({ f }: { f: FlowState }) {
  if (f.status === 'finished')
    return (
      <div className="flex items-center gap-2">
        <RoundBtn icon="replay" label="重新运行" onClick={restartFlow} primary />
        <RoundBtn icon="stop" label="结束演示" onClick={stopFlow} />
      </div>
    );
  const waitingNext = f.status === 'step-done' && f.mode === 'step' && !f.paused;
  const playing = !f.paused && !waitingNext;
  return (
    <div className="flex items-center gap-2">
      <RoundBtn icon="prev" label="上一环节" onClick={prevStep} disabled={f.trail.length < 2} />
      <RoundBtn icon={playing ? 'pause' : 'play'} label={f.paused ? '继续（空格）' : waitingNext ? '下一环节（空格）' : '暂停（空格）'} onClick={togglePlay} primary />
      <RoundBtn icon="next" label="下一环节" onClick={nextStep} />
      <RoundBtn icon="stop" label="结束演示" onClick={stopFlow} />
    </div>
  );
}

/** Centered floating playback capsule (nothing on either side); sits above the "Flow · Data" dock's top edge, or at the bottom center of the main area when the dock is collapsed */
export function PlaybackCapsule() {
  const f = useFlow((s) => s);
  if (!f.active) return null;
  const step = STEPS[f.idx];
  const status = f.status === 'finished' ? `已完成 ${f.completed.length + f.assumed.length}/${STEPS.length}` : f.paused ? '已暂停' : f.status === 'step-done' ? '本环节完成' : '运行中';
  return (
    <div role="toolbar" aria-label="演示播放控制" className="pointer-events-auto flex w-max items-center gap-4 rounded-full bg-surface/90 px-4 py-2 shadow-[0_8px_30px_-8px_rgb(0_0_0/0.35)] backdrop-blur">
      <span className="max-w-[16rem] truncate text-sm font-medium text-ink-900">
        {STEP_NO(f.idx)} {step?.short}
      </span>
      <BigControls f={f} />
      <SpeedControl />
      <ModeControl f={f} />
      <span className="text-xs text-ink-600">{status}</span>
    </div>
  );
}

const STEP_NO = (i: number) => String.fromCodePoint(0x2460 + i);

/** Global hotkeys: Space pauses / resumes (during a demo), [ ] change playback speed; never intercepted inside inputs */
export function usePlaybackHotkeys(active: boolean) {
  useEffect(() => {
    const typing = (t: EventTarget | null) => {
      const el = t as HTMLElement | null;
      return !!el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));
    };
    const onDown = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey || typing(e.target)) return;
      if (e.key === '[' || e.key === ']') {
        const cur = SPEEDS.indexOf(flowPrefs.get().speed ?? 1);
        const i = Math.max(0, Math.min(SPEEDS.length - 1, cur + (e.key === ']' ? 1 : -1)));
        setFlowSpeed(SPEEDS[i]);
        e.preventDefault();
        return;
      }
      if (active && (e.code === 'Space' || e.key === ' ')) {
        // Handle in the capture phase and prevent the default: a focused button won't fire a second click
        e.preventDefault();
        e.stopPropagation();
        if (!e.repeat) togglePlay();
      }
    };
    const onUp = (e: KeyboardEvent) => {
      if (active && (e.code === 'Space' || e.key === ' ') && !typing(e.target)) {
        e.preventDefault();
        e.stopPropagation();
      }
    };
    window.addEventListener('keydown', onDown, true);
    window.addEventListener('keyup', onUp, true);
    return () => {
      window.removeEventListener('keydown', onDown, true);
      window.removeEventListener('keyup', onUp, true);
    };
  }, [active]);
}
