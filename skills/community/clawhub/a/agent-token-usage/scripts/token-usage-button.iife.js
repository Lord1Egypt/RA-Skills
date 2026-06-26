// agent-token-usage-ui v1 — local stop-gap UI
// Adds a small "📊" button next to the Control UI header search,
// shows per-agent LLM token consumption for today in a modal.
//
// Data source: ./data/agent-token-usage.json (same-origin, refreshed by a
// background scheduler installed alongside this skill).
// Anchor: .topbar-search button inside <header>. Fail-quiet if not found.
//
// localStorage:
//   milly.tokenUsageBtn = 'off'  → disable the button
(() => {
  if (typeof window === "undefined" || typeof document === "undefined") return;
  if (window.__milly_token_usage_btn_v1__) return;
  window.__milly_token_usage_btn_v1__ = true;

  const LS = (() => { try { return window.localStorage; } catch (_) { return null; } })();
  const get = (k) => { try { return LS && LS.getItem(k); } catch (_) { return null; } };
  if (get("milly.tokenUsageBtn") === "off") return;

  const DATA_URL = "./data/agent-token-usage.json";

  // ---------- styles (once) ----------
  const styleId = "milly-token-usage-style";
  if (!document.getElementById(styleId)) {
    const s = document.createElement("style");
    s.id = styleId;
    s.textContent = `
      .milly-tk-btn {
        display: inline-flex; align-items: center; justify-content: center;
        width: 32px; height: 32px; margin-left: 6px;
        border-radius: 8px; cursor: pointer;
        background: transparent; border: 1px solid transparent;
        color: var(--text-2, #888); font-size: 16px; line-height: 1;
        transition: background .15s, color .15s, border-color .15s;
      }
      .milly-tk-btn:hover { background: var(--surface-2, rgba(255,255,255,.06)); color: var(--text-1, #ccc); }
      .milly-tk-overlay {
        position: fixed; inset: 0; background: rgba(0,0,0,.55);
        display: flex; align-items: center; justify-content: center;
        z-index: 99999; backdrop-filter: blur(4px);
      }
      .milly-tk-modal {
        background: var(--surface-1, #1a1a1d); color: var(--text-1, #e5e5e5);
        border: 1px solid var(--border-1, #2a2a2e); border-radius: 12px;
        padding: 20px 24px; min-width: 720px; max-width: 90vw; max-height: 80vh;
        overflow: auto; font: 13px/1.4 -apple-system,BlinkMacSystemFont,'SF Pro',system-ui,sans-serif;
        box-shadow: 0 20px 60px rgba(0,0,0,.6);
      }
      .milly-tk-modal h2 {
        margin: 0 0 4px; font-size: 16px; font-weight: 600;
        display: flex; align-items: center; gap: 8px;
      }
      .milly-tk-modal .milly-tk-meta { font-size: 11px; color: var(--text-2, #888); margin-bottom: 14px; }
      .milly-tk-modal table { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
      .milly-tk-modal th, .milly-tk-modal td {
        text-align: right; padding: 6px 10px;
        border-bottom: 1px solid var(--border-1, #2a2a2e);
      }
      .milly-tk-modal th:first-child, .milly-tk-modal td:first-child { text-align: left; }
      .milly-tk-modal th { font-weight: 500; font-size: 11px; color: var(--text-2, #888); text-transform: uppercase; letter-spacing: .04em; }
      .milly-tk-modal tr.total td { font-weight: 600; border-top: 2px solid var(--border-1, #2a2a2e); border-bottom: none; }
      .milly-tk-modal .milly-tk-close {
        position: absolute; top: 18px; right: 24px;
        background: transparent; border: none; color: var(--text-2, #888);
        font-size: 18px; cursor: pointer;
      }
      .milly-tk-modal .milly-tk-close:hover { color: var(--text-1, #ccc); }
      .milly-tk-bar { display: inline-block; height: 6px; background: linear-gradient(90deg, #60a5fa, #a78bfa); border-radius: 3px; vertical-align: middle; margin-left: 6px; }
      .milly-tk-empty { padding: 24px; text-align: center; color: var(--text-2, #888); }
      .milly-tk-modal pre.err { font-family: monospace; font-size: 11px; background: #2a1212; color: #f99; padding: 10px; border-radius: 6px; white-space: pre-wrap; }
    `;
    document.head.appendChild(s);
  }

  // ---------- helpers ----------
  const fmt = (n) => {
    if (!n && n !== 0) return "—";
    if (n >= 1e6) return (n / 1e6).toFixed(2) + "M";
    if (n >= 1e3) return (n / 1e3).toFixed(1) + "k";
    return String(Math.round(n));
  };

  const render = (data) => {
    const agents = (data && data.agents) || [];
    const date = (data && data.date) || "—";
    const updated = data && data.generatedAt ? new Date(data.generatedAt).toLocaleString() : "—";
    const max = Math.max(1, ...agents.map((a) => a.total || 0));

    const rows = agents.map((a) => {
      const pct = Math.round(((a.total || 0) / max) * 100);
      const bar = `<span class="milly-tk-bar" style="width:${Math.max(2, pct * 0.6)}px"></span>`;
      return `
        <tr>
          <td>${a.agent}${bar}</td>
          <td>${a.calls || 0}</td>
          <td>${fmt(a.input)}</td>
          <td>${fmt(a.output)}</td>
          <td>${fmt(a.cacheRead)}</td>
          <td>${fmt(a.cacheWrite)}</td>
          <td><b>${fmt(a.total)}</b></td>
          <td>${fmt(a.billable)}</td>
        </tr>`;
    }).join("");

    const grand = agents.reduce((acc, a) => {
      acc.input += a.input || 0; acc.output += a.output || 0;
      acc.cacheRead += a.cacheRead || 0; acc.cacheWrite += a.cacheWrite || 0;
      acc.total += a.total || 0; acc.billable += a.billable || 0;
      acc.calls += a.calls || 0; return acc;
    }, { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, total: 0, billable: 0, calls: 0 });

    return `
      <h2>📊 Agent Token Usage <span style="font-weight:400;font-size:12px;color:var(--text-2,#888)">— ${date}</span></h2>
      <div class="milly-tk-meta">Last updated: ${updated} · ${agents.length} agents · ~bill weights: cacheRead ×0.1, cacheWrite ×1.25</div>
      ${agents.length === 0
        ? `<div class="milly-tk-empty">No usage records found for ${date}.<br>Run the scheduler or check <code>~/.openclaw/agents/*/sessions/*.trajectory.jsonl</code></div>`
        : `<table>
            <thead><tr>
              <th>Agent</th><th>Calls</th><th>Input</th><th>Output</th>
              <th>CacheR</th><th>CacheW</th><th>Total</th><th>~Bill</th>
            </tr></thead>
            <tbody>${rows}</tbody>
            <tfoot><tr class="total">
              <td>TOTAL</td><td>${grand.calls}</td>
              <td>${fmt(grand.input)}</td><td>${fmt(grand.output)}</td>
              <td>${fmt(grand.cacheRead)}</td><td>${fmt(grand.cacheWrite)}</td>
              <td>${fmt(grand.total)}</td><td>${fmt(grand.billable)}</td>
            </tr></tfoot>
          </table>`
      }
    `;
  };

  const showModal = async () => {
    if (document.querySelector(".milly-tk-overlay")) return;
    const overlay = document.createElement("div");
    overlay.className = "milly-tk-overlay";
    const modal = document.createElement("div");
    modal.className = "milly-tk-modal";
    modal.style.position = "relative";
    modal.innerHTML = `<button class="milly-tk-close" aria-label="Close">✕</button><div class="milly-tk-body">Loading…</div>`;
    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    const close = () => overlay.remove();
    overlay.addEventListener("click", (e) => { if (e.target === overlay) close(); });
    modal.querySelector(".milly-tk-close").addEventListener("click", close);
    const onKey = (e) => { if (e.key === "Escape") { close(); document.removeEventListener("keydown", onKey); } };
    document.addEventListener("keydown", onKey);

    const body = modal.querySelector(".milly-tk-body");
    try {
      const resp = await fetch(DATA_URL + "?t=" + Date.now(), { cache: "no-cache" });
      if (!resp.ok) throw new Error("HTTP " + resp.status + " — " + DATA_URL);
      const data = await resp.json();
      body.innerHTML = render(data);
    } catch (err) {
      body.innerHTML = `
        <h2>📊 Agent Token Usage</h2>
        <div class="milly-tk-meta">Failed to load data.</div>
        <pre class="err">${(err && err.message) || err}

The scheduler may not be running yet.
Re-apply the skill or run the script once:

  python ~/.openclaw/workspace/skills/agent-token-usage/scripts/agent_token_usage.py --format json > &lt;openclaw-control-ui&gt;/data/agent-token-usage.json
        </pre>`;
    }
  };

  // ---------- mount button next to .topbar-search ----------
  const mountBtn = () => {
    const search = document.querySelector(".topbar-search");
    if (!search) return false;
    if (search.parentElement && search.parentElement.querySelector(".milly-tk-btn")) return true;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "milly-tk-btn";
    btn.title = "Agent Token Usage (today)";
    btn.setAttribute("aria-label", "Agent Token Usage");
    btn.textContent = "📊";
    btn.addEventListener("click", (e) => { e.preventDefault(); e.stopPropagation(); showModal(); });
    search.insertAdjacentElement("afterend", btn);
    return true;
  };

  // Re-mount across SPA re-renders.
  if (!mountBtn()) {
    const obs = new MutationObserver(() => { mountBtn(); });
    obs.observe(document.body, { childList: true, subtree: true });
  } else {
    // Still observe in case header re-renders
    const obs = new MutationObserver(() => { mountBtn(); });
    obs.observe(document.body, { childList: true, subtree: true });
  }
})();
