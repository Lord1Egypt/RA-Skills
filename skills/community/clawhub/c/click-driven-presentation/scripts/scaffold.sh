#!/usr/bin/env bash
#
# Scaffold a click-driven presentation (Vite + React + TS engine + one theme).
#
# Usage:
#   bash scaffold.sh [target-dir] [--theme=<id>] [--no-install] [--force]
#
#   target-dir    where to create the project (default: ./presentation)
#   --theme=<id>  theme to copy from the skill's themes/ dir (default: neutral-ink)
#   --no-install  skip `npm install`
#   --force       write into a non-empty target directory
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

TARGET="./presentation"
THEME="neutral-ink"
DO_INSTALL=1
FORCE=0

for arg in "$@"; do
  case "$arg" in
    --theme=*) THEME="${arg#*=}" ;;
    --no-install) DO_INSTALL=0 ;;
    --force) FORCE=1 ;;
    --list-themes) ls "$SKILL_DIR/themes" 2>/dev/null; exit 0 ;;
    --*) echo "Unknown option: $arg" >&2; exit 1 ;;
    *) TARGET="$arg" ;;
  esac
done

THEME_TOKENS="$SKILL_DIR/themes/$THEME/tokens.css"
if [ ! -f "$THEME_TOKENS" ]; then
  echo "Theme not found: $THEME (looked for $THEME_TOKENS)" >&2
  echo "Available themes:" >&2
  ls "$SKILL_DIR/themes" 2>/dev/null >&2 || true
  exit 1
fi

if [ -e "$TARGET" ] && [ -n "$(ls -A "$TARGET" 2>/dev/null)" ] && [ "$FORCE" -ne 1 ]; then
  echo "Target '$TARGET' exists and is not empty. Use --force to write into it." >&2
  exit 1
fi

mkdir -p "$TARGET/src/stage" "$TARGET/src/stepper" "$TARGET/src/registry" \
         "$TARGET/src/theme" "$TARGET/src/scenes/01-example"

# ---------------------------------------------------------------------------
# package.json
# ---------------------------------------------------------------------------
cat > "$TARGET/package.json" <<'FILE'
{
  "name": "presentation",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.3.4",
    "typescript": "^5.6.3",
    "vite": "^6.0.5"
  }
}
FILE

# ---------------------------------------------------------------------------
# vite.config.ts
# ---------------------------------------------------------------------------
cat > "$TARGET/vite.config.ts" <<'FILE'
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});
FILE

# ---------------------------------------------------------------------------
# tsconfig.json
# ---------------------------------------------------------------------------
cat > "$TARGET/tsconfig.json" <<'FILE'
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src", "vite.config.ts"]
}
FILE

# ---------------------------------------------------------------------------
# index.html
# ---------------------------------------------------------------------------
cat > "$TARGET/index.html" <<'FILE'
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Presentation</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
FILE

# ---------------------------------------------------------------------------
# src/main.tsx
# ---------------------------------------------------------------------------
cat > "$TARGET/src/main.tsx" <<'FILE'
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { Stage } from './stage/Stage';
import './theme/tokens.css';
import './deck.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Stage />
  </StrictMode>,
);
FILE

# ---------------------------------------------------------------------------
# src/deck.css  (engine layout only — personality lives in theme/tokens.css)
# ---------------------------------------------------------------------------
cat > "$TARGET/src/deck.css" <<'FILE'
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, #root { height: 100%; }

body {
  background: #000;
  color: var(--text);
  font-family: var(--font-body);
  -webkit-font-smoothing: antialiased;
}

/* full-viewport black shell; the stage is centered and letterboxed */
.deck-shell {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  overflow: hidden;
}

/* fixed 16:9 design canvas; scaled to fit via inline transform */
.deck-stage {
  position: relative;
  flex: none;
  overflow: hidden;
  transform-origin: center center;
}

/* hover-only progress bar — invisible on the recording unless cursor is at the bottom edge */
.deck-hotzone {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 56px;
  display: flex;
  align-items: flex-end;
}
.deck-progress {
  height: 3px;
  background: var(--accent);
  opacity: 0;
  transition: opacity 0.25s ease;
}
.deck-hotzone:hover .deck-progress { opacity: 1; }
FILE

# ---------------------------------------------------------------------------
# src/registry/types.ts
# ---------------------------------------------------------------------------
cat > "$TARGET/src/registry/types.ts" <<'FILE'
import type { ComponentType } from 'react';

/** One beat: what the speaker says + a short note on what the screen does. */
export type StepSpec = { say: string; show: string };

/** A scene = its steps (single source of truth) + a component that is a pure function of the local step. */
export type Scene = {
  id: string;
  steps: StepSpec[];
  Component: ComponentType<{ step: number }>;
};
FILE

# ---------------------------------------------------------------------------
# src/registry/scenes.ts
# ---------------------------------------------------------------------------
cat > "$TARGET/src/registry/scenes.ts" <<'FILE'
import type { Scene } from './types';
import { Example } from '../scenes/01-example/Example';
import { steps as exampleSteps } from '../scenes/01-example/steps';

// Scenes in deck order. Add one entry per scene folder.
// Delete the example entry (and its folder) before building real scenes.
export const scenes: Scene[] = [
  { id: 'example', steps: exampleSteps, Component: Example },
];
FILE

# ---------------------------------------------------------------------------
# src/stepper/useStepper.ts
# ---------------------------------------------------------------------------
cat > "$TARGET/src/stepper/useStepper.ts" <<'FILE'
import { useCallback, useEffect, useState } from 'react';

/**
 * Global step counter for the whole deck.
 * Advances on ArrowRight / Space, retreats on ArrowLeft. No timers — the
 * speaker controls the rhythm. Stage also advances on click.
 */
export function useStepper(total: number) {
  const [index, setIndex] = useState(0);

  const next = useCallback(
    () => setIndex((i) => Math.min(i + 1, Math.max(total - 1, 0))),
    [total],
  );
  const prev = useCallback(() => setIndex((i) => Math.max(i - 1, 0)), []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault();
        next();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        prev();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [next, prev]);

  return { index, total, next, prev };
}
FILE

# ---------------------------------------------------------------------------
# src/stage/Stage.tsx
# ---------------------------------------------------------------------------
cat > "$TARGET/src/stage/Stage.tsx" <<'FILE'
import { useEffect, useMemo, useState } from 'react';
import type { MouseEvent } from 'react';
import { scenes } from '../registry/scenes';
import { useStepper } from '../stepper/useStepper';

const STAGE_W = 1920;
const STAGE_H = 1080;

/** Map a global step index to which scene is active and the local step within it. */
function resolve(index: number) {
  let acc = 0;
  for (let s = 0; s < scenes.length; s++) {
    const len = scenes[s].steps.length;
    if (index < acc + len) return { sceneIndex: s, local: index - acc };
    acc += len;
  }
  const last = Math.max(scenes.length - 1, 0);
  return { sceneIndex: last, local: Math.max((scenes[last]?.steps.length ?? 1) - 1, 0) };
}

export function Stage() {
  const total = useMemo(() => scenes.reduce((n, s) => n + s.steps.length, 0), []);
  const { index, next } = useStepper(total);
  const [scale, setScale] = useState(1);

  useEffect(() => {
    const fit = () =>
      setScale(Math.min(window.innerWidth / STAGE_W, window.innerHeight / STAGE_H));
    fit();
    window.addEventListener('resize', fit);
    return () => window.removeEventListener('resize', fit);
  }, []);

  const onClick = (e: MouseEvent<HTMLDivElement>) => {
    // interactive elements inside a scene opt out with data-no-advance
    if ((e.target as HTMLElement).closest('[data-no-advance]')) return;
    next();
  };

  const { sceneIndex, local } = resolve(index);
  const scene = scenes[sceneIndex];
  const Scene = scene?.Component;
  const progress = total > 1 ? (index / (total - 1)) * 100 : 100;

  return (
    <div className="deck-shell" onClick={onClick}>
      <div
        className="deck-stage stage-frame"
        style={{ width: STAGE_W, height: STAGE_H, transform: `scale(${scale})` }}
      >
        {Scene ? <Scene step={local} /> : null}
      </div>
      <div className="deck-hotzone">
        <div className="deck-progress" style={{ width: `${progress}%` }} />
      </div>
    </div>
  );
}
FILE

# ---------------------------------------------------------------------------
# src/scenes/01-example/steps.ts
# ---------------------------------------------------------------------------
cat > "$TARGET/src/scenes/01-example/steps.ts" <<'FILE'
import type { StepSpec } from '../../registry/types';

// steps.length must equal the largest step the component uses, plus one.
export const steps: StepSpec[] = [
  { say: 'This is the first beat — the hook.', show: 'hero line' },
  { say: 'Click again and a bar grows in.', show: 'demonstration: bar grows' },
  { say: 'One more click reveals the closing point.', show: 'reveal closing point' },
];
FILE

# ---------------------------------------------------------------------------
# src/scenes/01-example/Example.tsx
# ---------------------------------------------------------------------------
cat > "$TARGET/src/scenes/01-example/Example.tsx" <<'FILE'
import './Example.css';

// Demo scene. Delete this folder and its entry in registry/scenes.ts before
// building real scenes. CSS prefix: .ex-
export function Example({ step }: { step: number }) {
  return (
    <div className="ex-root">
      <h1 className="ex-hero">Click-driven demo</h1>
      <p className="ex-line">Click anywhere — or press → / Space — to advance one beat.</p>

      {step >= 1 && (
        <div className="ex-bar-track">
          <div className="ex-bar-fill" />
        </div>
      )}

      {step >= 2 && (
        <p className="ex-point hero-num">3 beats. Now make your own.</p>
      )}

      <p className="ex-hint">
        Delete <code>src/scenes/01-example</code> and remove its entry in{' '}
        <code>src/registry/scenes.ts</code> before building real scenes.
      </p>
    </div>
  );
}
FILE

# ---------------------------------------------------------------------------
# src/scenes/01-example/Example.css
# ---------------------------------------------------------------------------
cat > "$TARGET/src/scenes/01-example/Example.css" <<'FILE'
.ex-root {
  width: 100%;
  height: 100%;
  padding: 120px 140px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  justify-content: center;
}
.ex-hero {
  font-family: var(--font-display);
  font-size: 120px;
  line-height: 1;
  letter-spacing: -0.02em;
  color: var(--text);
}
.ex-line {
  font-size: 36px;
  color: var(--text-2);
}
.ex-bar-track {
  width: 60%;
  height: 28px;
  background: var(--surface-2);
  border-radius: 2px;
  overflow: hidden;
}
.ex-bar-fill {
  height: 100%;
  width: 0;
  background: var(--accent);
  animation: ex-grow 700ms cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}
@keyframes ex-grow {
  to { width: 72%; }
}
.ex-point {
  font-size: 64px;
}
.ex-hint {
  margin-top: auto;
  font-size: 22px;
  color: var(--text-mute);
  font-family: var(--font-mono);
}
.ex-hint code {
  color: var(--text-2);
}
FILE

# ---------------------------------------------------------------------------
# theme tokens (copied from the skill's themes/ dir)
# ---------------------------------------------------------------------------
cp "$THEME_TOKENS" "$TARGET/src/theme/tokens.css"

# ---------------------------------------------------------------------------
# .gitignore
# ---------------------------------------------------------------------------
cat > "$TARGET/.gitignore" <<'FILE'
node_modules
dist
*.local
FILE

if [ "$DO_INSTALL" -eq 1 ]; then
  echo "Installing dependencies in $TARGET ..."
  (cd "$TARGET" && npm install)
fi

cat <<DONE

Scaffolded a click-driven presentation in: $TARGET
  theme: $THEME

Next:
  cd "$TARGET"
  npm run dev            # open the printed localhost URL, click / press -> to advance
  npm run typecheck      # run before reporting a scene "done"

Before building real scenes, delete the demo:
  rm -rf "$TARGET/src/scenes/01-example"
  # then remove the Example import + entry from src/registry/scenes.ts

Build one scene per folder (NN-id), each with its own steps.ts and CSS prefix.
See the skill's references/SCENE-CRAFT.md and references/STEPS-SPEC.md.
DONE
