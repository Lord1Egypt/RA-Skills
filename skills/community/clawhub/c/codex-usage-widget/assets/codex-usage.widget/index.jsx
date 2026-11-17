// Codex usage monitor — lightweight Übersicht widget.
// Reads local Codex sqlite + rollout files only; no network, no model call.

export const refreshFrequency = 10000;

export const command =
  "/usr/bin/python3 "/Library/Application Support/Übersicht/widgets/codex-usage.widget/codex-usage.py"";

export const className = `
  top: 40px;
  left: 40px;
  z-index: 2;
`;

const C = {
  bg1: "rgba(252,252,255,0.88)",
  bg2: "rgba(244,247,250,0.90)",
  text: "#1D1B20",
  sub: "#5D5965",
  faint: "#8A8494",
  line: "rgba(73,69,79,0.13)",
  green: "#2D8F5F",
  blue: "#2866B8",
  purple: "#6750A4",
  warn: "#B26A00",
};

function fmtTok(n) {
  n = Math.max(0, Math.round(Number(n || 0)));
  if (n < 1000) return `${n}`;
  if (n < 10000) return `${(n / 1000).toFixed(1)}K`;
  if (n < 1000000) {
    const k = Math.round(n / 1000);
    return k >= 1000 ? `${(n / 1000000).toFixed(1)}M` : `${k}K`;
  }
  if (n < 10000000) return `${(n / 1000000).toFixed(1)}M`;
  if (n < 1000000000) {
    const m = Math.round(n / 1000000);
    return m >= 1000 ? `${(n / 1000000000).toFixed(1)}B` : `${m}M`;
  }
  return `${(n / 1000000000).toFixed(1)}B`;
}

function fmtBytes(n) {
  n = Math.max(0, Math.round(Number(n || 0)));
  if (n < 1024) return `${n}B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)}KB`;
  if (n < 1024 * 1024 * 1024) return `${(n / 1024 / 1024).toFixed(1)}MB`;
  return `${(n / 1024 / 1024 / 1024).toFixed(1)}GB`;
}

function ago(sec) {
  sec = Math.max(0, Math.round(Number(sec || 0)));
  if (sec < 60) return `${sec}s`;
  const m = Math.round(sec / 60);
  if (m < 60) return `${m}m`;
  const h = Math.round(m / 60);
  if (h < 48) return `${h}h`;
  return `${Math.round(h / 24)}d`;
}

let pos = (() => {
  try {
    return JSON.parse(localStorage.getItem("codexUsagePos")) ||
      JSON.parse(localStorage.getItem("ccpos")) ||
      { x: 0, y: 310 };
  }
  catch (e) { return { x: 0, y: 310 }; }
})();

const xf = (p) => `translate(${p.x}px, ${p.y}px)`;

function startDrag(e) {
  if (e.button !== 0) return;
  e.preventDefault();
  const sx = e.clientX, sy = e.clientY, ox = pos.x, oy = pos.y;
  const card = document.getElementById("cu-card");
  const move = (ev) => {
    pos = { x: ox + ev.clientX - sx, y: oy + ev.clientY - sy };
    if (card) card.style.transform = xf(pos);
  };
  const up = () => {
    window.removeEventListener("mousemove", move);
    window.removeEventListener("mouseup", up);
    try { localStorage.setItem("codexUsagePos", JSON.stringify(pos)); } catch (e) {}
  };
  window.addEventListener("mousemove", move);
  window.addEventListener("mouseup", up);
}

const STYLE = `
  .cu-card,.cu-card *{box-sizing:border-box;font-family:-apple-system,"SF Pro Display","PingFang SC",sans-serif;-webkit-font-smoothing:antialiased;}
  .cu-card{width:264px;color:${C.text};background:linear-gradient(157deg,${C.bg1},${C.bg2});
    backdrop-filter:blur(24px) saturate(140%);-webkit-backdrop-filter:blur(24px) saturate(140%);
    border:1px solid rgba(40,102,184,0.16);border-radius:14px;padding:10px 11px 9px;
    box-shadow:0 20px 50px rgba(55,68,94,0.16),inset 0 1px 0 rgba(255,255,255,0.72);}
  .cu-head{display:flex;align-items:center;gap:7px;margin-bottom:8px;}
  .cu-dot{width:7px;height:7px;border-radius:50%;background:${C.green};box-shadow:0 0 7px rgba(45,143,95,.5);}
  .cu-dot.hot{background:${C.blue};animation:cupulse 1.1s ease-in-out infinite;}
  @keyframes cupulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.45;transform:scale(.75)}}
  .cu-head{cursor:grab;user-select:none;-webkit-user-select:none;}
  .cu-head:active{cursor:grabbing;}
  .cu-title{font-size:12px;font-weight:720;letter-spacing:0;}
  .cu-time{margin-left:auto;color:${C.faint};font-size:9px;font-variant-numeric:tabular-nums;}
  .cu-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin-bottom:7px;}
  .cu-stat{background:rgba(40,102,184,.08);border:1px solid rgba(40,102,184,.08);border-radius:8px;padding:5px 3px;text-align:center;min-width:0;overflow:hidden;}
  .cu-label{font-size:8px;color:${C.sub};letter-spacing:0;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  .cu-val{font-size:11px;font-weight:760;letter-spacing:0;font-variant-numeric:tabular-nums;white-space:nowrap;line-height:1.15;}
  .cu-row{display:flex;align-items:center;gap:6px;border-top:1px solid ${C.line};padding:5px 0;}
  .cu-row:first-of-type{border-top:0;}
  .cu-name{flex:1;min-width:0;font-size:10px;color:${C.text};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  .cu-meta{font-size:9px;color:${C.faint};white-space:nowrap;font-variant-numeric:tabular-nums;}
  .cu-meta.warn{color:${C.warn};}
  .cu-meta.danger{color:#B3261E;}
  .cu-pill{font-size:8px;color:#fff;background:${C.purple};border-radius:5px;padding:1px 5px;max-width:50px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
  .cu-bars{display:flex;align-items:flex-end;gap:4px;height:21px;margin-top:6px;border-top:1px solid ${C.line};padding-top:5px;}
  .cu-barbox{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;}
  .cu-bar{width:100%;min-height:2px;border-radius:3px 3px 0 0;background:linear-gradient(180deg,${C.blue},${C.purple});opacity:.88;}
  .cu-day{font-size:8px;color:${C.faint};line-height:1;}
  .cu-foot{display:flex;align-items:center;margin-top:6px;color:${C.faint};font-size:9px;}
  .cu-warn{color:${C.warn};}
`;

export const render = ({ output }) => {
  let data = {};
  try { data = JSON.parse((output || "").trim()); } catch (e) {
    data = { ok: false, error: "json parse failed" };
  }
  if (!data.ok) {
    return <div><style>{STYLE}</style><div id="cu-card" className="cu-card" style={{transform: xf(pos)}}>
      <div className="cu-head" onMouseDown={startDrag}><span className="cu-dot"></span><span className="cu-title">Codex Usage</span></div>
      <div className="cu-foot cu-warn">{data.error || "Read failed"}</div>
    </div></div>;
  }

  const recentRows = 6;
  const recentAll = data.recent || [];
  const recent = recentAll.slice(0, recentRows);
  const hiddenRecent = Math.max(0, Number(data.thread_count || recentAll.length) - recent.length);
  const bars = data.days || [];
  const maxDay = Math.max(1, ...bars.map(d => Number(d.tokens || 0)));
  const hot = Number(data.active_threads || 0) > 0;

  return <div><style>{STYLE}</style><div id="cu-card" className="cu-card" style={{transform: xf(pos)}}>
    <div className="cu-head" onMouseDown={startDrag}>
      <span className={`cu-dot ${hot ? "hot" : ""}`}></span>
      <span className="cu-title">Codex Usage</span>
      <span className="cu-time">{data.now}</span>
    </div>

    <div className="cu-grid">
      <div className="cu-stat"><div className="cu-label">Today</div><div className="cu-val">{fmtTok(data.today_tokens)}</div></div>
      <div className="cu-stat"><div className="cu-label">Total</div><div className="cu-val">{fmtTok(data.total_tokens)}</div></div>
      <div className="cu-stat"><div className="cu-label">Sessions</div><div className="cu-val">{data.today_threads}</div></div>
      <div className="cu-stat"><div className="cu-label">10 min</div><div className="cu-val">{data.active_threads}</div></div>
    </div>

    {recent.map((r, i) =>
      <div className="cu-row" key={i}>
        <span className="cu-pill">{r.source || "codex"}</span>
        <span className="cu-name">{r.title || "Untitled"}</span>
        <span className={`cu-meta ${Number(r.ctx_pct || 0) >= 85 ? "danger" : Number(r.ctx_pct || 0) >= 60 ? "warn" : ""}`}>
          {Math.round(Number(r.ctx_pct || 0))}% · {ago(r.age_sec)}
        </span>
      </div>
    )}

    <div className="cu-bars">
      {bars.map((d, i) =>
        <div className="cu-barbox" key={i}>
          <div className="cu-bar" style={{height: `${Math.max(2, Math.round((Number(d.tokens || 0) / maxDay) * 12))}px`}}></div>
          <div className="cu-day">{d.label}</div>
        </div>
      )}
    </div>

    <div className="cu-foot">
      {data.thread_count} threads · logs {fmtBytes(data.log_bytes)}
      {hiddenRecent ? <span style={{marginLeft:"6px"}}>+{hiddenRecent}</span> : null}
      <span style={{marginLeft:"auto"}}>local only</span>
    </div>
  </div></div>;
};
