#!/usr/bin/env bash
# openclaw-agent-runner-site: create a minimal static site skeleton.
#
# Generates a mobile-first static site (index.html + style.css) that matches the
# skill's Option A: a single-page UI with API Key / Base URL / Model inputs and a
# "Run Agent" button stub. No backend is created and no API calls are made.
#
# Usage:
#   ./scaffold_site.sh [output_dir]      # default: ./agent-runner-site
set -euo pipefail

OUT="${1:-agent-runner-site}"
mkdir -p "$OUT"

cat > "$OUT/index.html" <<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
  <title>OpenClaw Agent Runner</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <main class="card">
    <h1>Agent Runner</h1>
    <label>API Key
      <input id="apiKey" type="password" autocomplete="off" placeholder="never logged, stays in browser" />
    </label>
    <label>Base URL
      <input id="baseUrl" type="text" placeholder="https://your-gateway.example.com" />
    </label>
    <label>Model
      <input id="model" type="text" list="modelList" placeholder="e.g. gpt-4o-mini" />
      <datalist id="modelList">
        <option value="gpt-4o-mini"></option>
        <option value="claude-3-5-sonnet"></option>
        <option value="local/llama3"></option>
      </datalist>
    </label>
    <label>Prompt
      <textarea id="prompt" rows="3" placeholder="What should the agent do?"></textarea>
    </label>
    <button id="runBtn" type="button">Run Agent</button>
    <pre id="output" aria-live="polite"></pre>
  </main>
  <script src="app.js"></script>
</body>
</html>
HTML

cat > "$OUT/style.css" <<'CSS'
:root { --bg:#0f1115; --fg:#e6e6e6; --accent:#5b8cff; --card:#1a1d24; }
* { box-sizing: border-box; }
body {
  margin: 0; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
  background: var(--bg); color: var(--fg);
  display: flex; min-height: 100vh; justify-content: center; align-items: flex-start;
  padding: 1rem;
}
.card { background: var(--card); width: 100%; max-width: 420px; border-radius: 14px; padding: 1.25rem; }
h1 { font-size: 1.25rem; margin: 0 0 1rem; }
label { display: block; font-size: .8rem; margin: .6rem 0 .25rem; }
input, textarea {
  width: 100%; padding: .6rem; border-radius: 8px; border: 1px solid #2c3038;
  background: #0f1115; color: var(--fg); font-size: .95rem;
}
button {
  margin-top: 1rem; width: 100%; padding: .7rem; border: 0; border-radius: 8px;
  background: var(--accent); color: #fff; font-weight: 600; cursor: pointer;
}
pre { margin-top: 1rem; background: #0b0d11; padding: .75rem; border-radius: 8px; max-height: 40vh; overflow: auto; white-space: pre-wrap; }
CSS

# Minimal app.js stub: wires button but does not execute anything on its own.
cat > "$OUT/app.js" <<'JS'
// Stub only. Verify the Gateway API shape (POST /sessions + WS stream) before
// filling this in. The API key is read from the field and never logged.
document.getElementById('runBtn').addEventListener('click', () => {
  const cfg = {
    baseUrl: document.getElementById('baseUrl').value,
    model: document.getElementById('model').value,
    prompt: document.getElementById('prompt').value,
  };
  const out = document.getElementById('output');
  if (!cfg.baseUrl || !cfg.model) { out.textContent = 'Base URL and Model are required.'; return; }
  out.textContent = 'Config captured (dry run). Implement POST /sessions + WS stream per Gateway docs.';
});
JS

echo "[scaffold_site] created: $OUT/index.html, $OUT/style.css, $OUT/app.js"
echo "[scaffold_site] open index.html in a browser to preview (no backend needed)."
