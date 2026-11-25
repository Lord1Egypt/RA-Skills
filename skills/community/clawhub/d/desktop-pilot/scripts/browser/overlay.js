/* Informational in-page status UI only. A webpage can alter/remove this UI.
 * NEVER use page state as cancellation/authorization. Use the trusted host's
 * cancellation control (or Desktop Pilot's native Windows Stop) instead.
 * API: window.__dpOverlay.show(text), .text(text), .hide(), .visible().
 * This intentionally has no Stop/clear/stopped API or input blocking.
 */
(() => {
  if (window.__dpOverlay) return;
  let host = null, label = null, timer = null, idleMs = 120000;

  const css = `
    :host { all: initial; }
    .glow { position: fixed; inset: 0; pointer-events: none; z-index: 2147483646; }
    .edge { position: absolute; pointer-events: none; animation: hue 6s linear infinite; }
    .top { left: 0; right: 0; top: 0; height: 110px; background: linear-gradient(to bottom, var(--c), transparent); }
    .bottom { left: 0; right: 0; bottom: 0; height: 110px; background: linear-gradient(to top, var(--c), transparent); animation-delay: -3s; }
    .left { top: 0; bottom: 0; left: 0; width: 110px; background: linear-gradient(to right, var(--c), transparent); animation-delay: -4.5s; }
    .right { top: 0; bottom: 0; right: 0; width: 110px; background: linear-gradient(to left, var(--c), transparent); animation-delay: -1.5s; }
    .line { position: absolute; inset: 0; border: 3px solid var(--c); box-shadow: 0 0 40px var(--c), inset 0 0 40px var(--c); pointer-events: none; animation: hue 6s linear infinite; }
    .glow { animation: pulse 1.6s ease-in-out infinite alternate; }
    @property --c { syntax: '<color>'; inherits: true; initial-value: #00e5ff; }
    @keyframes hue { 0%, 100% { --c: rgba(0,229,255,.62); } 33% { --c: rgba(45,123,255,.62); } 66% { --c: rgba(139,92,246,.62); } }
    @keyframes pulse { from { opacity: .6; } to { opacity: 1; } }
    .pill { position: fixed; left: 50%; bottom: 28px; transform: translateX(-50%); z-index: 2147483647; pointer-events: auto;
      display: flex; align-items: center; gap: 12px; padding: 8px 8px 8px 16px; border-radius: 24px;
      background: rgba(12,38,42,.94); border: 1px solid rgba(0,229,255,.45); box-shadow: 0 6px 24px rgba(0,0,0,.45);
      font: 14px/1.2 system-ui, 'Segoe UI', sans-serif; color: #fff; max-width: min(90vw, 640px); }
    .dot { width: 10px; height: 10px; border-radius: 50%; background: #00e5ff; animation: blink .9s ease-in-out infinite alternate; flex: none; }
    @keyframes blink { from { opacity: .25; } to { opacity: 1; } }
    .txt { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  `;

  function arm() { clearTimeout(timer); timer = setTimeout(api.hide, idleMs); }
  const api = {
    show(text, opts) {
      if (opts && opts.idleMs) idleMs = opts.idleMs;
      if (!host) {
        host = document.createElement('div');
        host.setAttribute('data-desktop-pilot-overlay', '');
        const root = host.attachShadow({ mode: 'open' });
        root.innerHTML = `<style>${css}</style>
          <div class="glow"><div class="edge top"></div><div class="edge bottom"></div><div class="edge left"></div><div class="edge right"></div><div class="line"></div></div>
          <div class="pill"><span class="dot"></span><span class="txt"></span></div>`;
        label = root.querySelector('.txt');
        (document.documentElement || document.body).appendChild(host);
      }
      label.textContent = text || 'Agent is working...';
      arm();
    },
    text(t) { if (!host) return api.show(t); label.textContent = t; arm(); },
    hide() { clearTimeout(timer); if (host) { host.remove(); host = null; label = null; } },
    visible() { return !!host; },
  };
  Object.defineProperty(window, '__dpOverlay', { value: Object.freeze(api), configurable: false, writable: false });
})();
