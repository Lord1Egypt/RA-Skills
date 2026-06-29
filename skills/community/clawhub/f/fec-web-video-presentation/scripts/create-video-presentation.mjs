#!/usr/bin/env node
import l from"node:fs";import i from"node:path";import{fileURLToPath as g}from"node:url";const u=i.resolve(i.dirname(g(import.meta.url)),".."),h=i.join(u,"data","starter-themes.json"),p=JSON.parse(l.readFileSync(h,"utf8")),f=process.argv.slice(2),o=v(f);if(o.help&&(w(),process.exit(0)),o.listThemes){for(const e of p)console.log(`${e.id}	${e.name}	${e.bestFor}`);process.exit(0)}const n=i.resolve(process.cwd(),o.target??"presentation"),r=p.find(e=>e.id===o.theme);r||c(`Unknown theme "${o.theme}". Run with --list-themes to see available themes.`);const m=y(r);if(o.dryRun){console.log(`Would create ${m.length} files in ${n}`),console.log(`Theme: ${r.id} (${r.name})`);for(const e of m)console.log(`- ${e.name}`);process.exit(0)}l.existsSync(n)&&l.readdirSync(n).length>0&&c(`Target directory is not empty: ${n}`);for(const e of m){const t=i.join(n,e.name);l.mkdirSync(i.dirname(t),{recursive:!0}),l.writeFileSync(t,e.body,"utf8")}console.log(`Created web video presentation at ${n}`),console.log(`Theme: ${r.id} (${r.name})`),console.log("Next:"),console.log("  cd "+i.relative(process.cwd(),n)),console.log("  npm install"),console.log("  npm run dev");function v(e){const t={dryRun:!1,help:!1,listThemes:!1,target:void 0,theme:p[0]?.id??"editorial-slate"};for(let a=0;a<e.length;a+=1){const s=e[a];if(s==="--help"||s==="-h")t.help=!0;else if(s==="--dry-run")t.dryRun=!0;else if(s==="--list-themes")t.listThemes=!0;else if(s.startsWith("--theme="))t.theme=s.slice(8);else if(s==="--theme"){const d=e[a+1];(!d||d.startsWith("--"))&&c("Missing value for --theme."),t.theme=d,a+=1}else s.startsWith("--")?c(`Unknown option: ${s}`):t.target?c(`Unexpected argument: ${s}`):t.target=s}return t}function y(e){const t=b(e.tokens);return[{name:"package.json",body:JSON.stringify({scripts:{dev:"vite",build:"tsc --noEmit && vite build",preview:"vite preview"},dependencies:{react:"latest","react-dom":"latest"},devDependencies:{"@types/react":"latest","@types/react-dom":"latest","@vitejs/plugin-react":"latest",typescript:"latest",vite:"latest"}},null,2)+`
`},{name:"index.html",body:`<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Web Video Presentation</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"><\/script>
  </body>
</html>
`},{name:"tsconfig.json",body:JSON.stringify({compilerOptions:{target:"ES2022",useDefineForClassFields:!0,lib:["DOM","DOM.Iterable","ES2022"],allowJs:!1,skipLibCheck:!0,esModuleInterop:!0,allowSyntheticDefaultImports:!0,strict:!0,forceConsistentCasingInFileNames:!0,module:"ESNext",moduleResolution:"Node",resolveJsonModule:!0,isolatedModules:!0,noEmit:!0,jsx:"react-jsx"},include:["src"]},null,2)+`
`},{name:"vite.config.ts",body:`import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});
`},{name:"src/main.tsx",body:`import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

type Scene = {
  eyebrow: string;
  title: string;
  body: string;
  detail: string;
};

const scenes: Scene[] = [
  {
    eyebrow: '01 / Hook',
    title: 'Replace this with the first spoken beat',
    body: 'One step equals one idea. Keep it readable in a 1080p recording.',
    detail: 'Use source facts, product states, diagrams, or real assets to make the screen specific.',
  },
  {
    eyebrow: '02 / Proof',
    title: 'Show the evidence, not a generic slide',
    body: 'Turn a claim into a visual: timeline, interface state, metric, map, comparison, or system diagram.',
    detail: 'Advance with Space, ArrowRight, PageDown, or click. Go back with ArrowLeft or PageUp.',
  },
  {
    eyebrow: '03 / Close',
    title: 'End on the idea the viewer should remember',
    body: 'Swap this starter content for your script and outline.',
    detail: 'Controls stay quiet so the stage is clean for recording.',
  },
];

const storageKey = 'fec-web-video-presentation-step-v1';

function App() {
  const [step, setStep] = useState(() => Number(localStorage.getItem(storageKey) ?? 0));
  const current = scenes[Math.min(Math.max(step, 0), scenes.length - 1)];
  const progress = useMemo(() => ((step + 1) / scenes.length) * 100, [step]);

  useEffect(() => {
    localStorage.setItem(storageKey, String(step));
  }, [step]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'ArrowRight' || event.key === 'PageDown' || event.key === ' ') {
        event.preventDefault();
        setStep((value) => Math.min(value + 1, scenes.length - 1));
      }
      if (event.key === 'ArrowLeft' || event.key === 'PageUp') {
        event.preventDefault();
        setStep((value) => Math.max(value - 1, 0));
      }
      if (event.key.toLowerCase() === 'r') {
        setStep(0);
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, []);

  return (
    <main className="viewport" onClick={() => setStep((value) => Math.min(value + 1, scenes.length - 1))}>
      <section className="stage" aria-live="polite">
        <div className="scene-grid">
          <div className="copy">
            <p className="eyebrow">{current.eyebrow}</p>
            <h1>{current.title}</h1>
            <p className="body">{current.body}</p>
          </div>
          <div className="visual" aria-label="Visual evidence placeholder">
            <span>{String(step + 1).padStart(2, '0')}</span>
            <p>{current.detail}</p>
          </div>
        </div>
        <div className="progress" aria-hidden="true">
          <span style={{ width: \`\${progress}%\` }} />
        </div>
      </section>
    </main>
  );
}

createRoot(document.getElementById('root')!).render(<App />);
`},{name:"src/styles.css",body:`${t}

* {
  box-sizing: border-box;
}

html,
body,
#root {
  margin: 0;
  min-height: 100%;
}

body {
  background: #111;
  color: var(--stage-fg);
  font-family: var(--font-body);
}

.viewport {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
}

.stage {
  width: min(100vw - 48px, calc((100vh - 48px) * 16 / 9));
  aspect-ratio: 16 / 9;
  position: relative;
  overflow: hidden;
  background: var(--stage-bg);
  color: var(--stage-fg);
  box-shadow: var(--shadow);
}

.scene-grid {
  height: 100%;
  display: grid;
  grid-template-columns: 1.12fr 0.88fr;
  gap: 72px;
  align-items: center;
  padding: 96px;
}

.eyebrow {
  color: var(--accent);
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 26px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

h1 {
  font-family: var(--font-display);
  font-size: clamp(48px, 6vw, 104px);
  line-height: 0.96;
  letter-spacing: 0;
  margin: 0;
  text-wrap: balance;
}

.body {
  color: var(--muted-fg);
  font-size: 32px;
  line-height: 1.35;
  margin: 36px 0 0;
  max-width: 820px;
  text-wrap: pretty;
}

.visual {
  min-height: 560px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--panel);
  display: grid;
  align-content: space-between;
  padding: 42px;
}

.visual span {
  color: var(--accent-2);
  font-family: var(--font-display);
  font-size: 132px;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.visual p {
  margin: 0;
  color: var(--muted-fg);
  font-size: 26px;
  line-height: 1.4;
}

.progress {
  position: absolute;
  left: 32px;
  right: 32px;
  bottom: 28px;
  height: 3px;
  background: color-mix(in srgb, var(--line) 70%, transparent);
  opacity: 0;
  transition: opacity 160ms ease;
}

.stage:hover .progress,
.stage:focus-within .progress {
  opacity: 1;
}

.progress span {
  display: block;
  height: 100%;
  background: var(--accent);
  transition: width var(--step-duration) ease;
}

@media (prefers-reduced-motion: reduce) {
  .progress,
  .progress span {
    transition: none;
  }
}
`},{name:"README.md",body:`# Web Video Presentation

Generated with Frontend Craft.

- 16:9 browser recording stage
- Step-driven scenes
- Keyboard and click navigation
- Theme tokens in \`src/styles.css\`

Replace the starter scenes in \`src/main.tsx\` with your script and outline.
`}]}function b(e){return`:root {
  --stage-bg: ${e.stageBg};
  --stage-fg: ${e.stageFg};
  --muted-fg: ${e.mutedFg};
  --accent: ${e.accent};
  --accent-2: ${e.accent2};
  --panel: ${e.panel};
  --line: ${e.line};
  --shadow: ${e.shadow};
  --font-display: ${e.fontDisplay};
  --font-body: ${e.fontBody};
  --radius: ${e.radius};
  --step-duration: ${e.stepDuration};
}`}function w(){console.log(`Usage:
  node skills/fec-web-video-presentation/scripts/create-video-presentation.mjs [target] [--theme=<id>] [--dry-run]
  node skills/fec-web-video-presentation/scripts/create-video-presentation.mjs --list-themes
`)}function c(e){console.error(`[create-video-presentation] ${e}`),process.exit(1)}
