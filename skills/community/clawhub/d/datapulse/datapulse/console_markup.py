"""HTML surface bundle for the DataPulse command chamber."""

from __future__ import annotations

import json
from typing import Any


def _json_blob(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False)


def render_console_html(title: str) -> str:
    initial_state = _json_blob(
        {
            "title": title,
            "sections": ["overview", "missions", "cockpit", "alerts", "routes", "status", "triage", "stories"],
        }
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="icon" type="image/png" href="/brand/icon">
  <link rel="apple-touch-icon" href="/brand/square">
  <style>
    :root {{
      --paper: #08111c;
      --mist: #112033;
      --panel: rgba(10, 18, 31, 0.76);
      --panel-strong: rgba(9, 15, 28, 0.9);
      --ink: #eaf4ff;
      --muted: #9fb3ca;
      --accent: #ff6a82;
      --accent-2: #7fe4ff;
      --line: rgba(146, 175, 210, 0.18);
      --warn: #ff6a82;
      --shadow: 0 28px 90px rgba(3, 8, 18, 0.5);
      --headline: "Eurostile Extended", "Avenir Next Condensed", "Arial Narrow", sans-serif;
      --body: "IBM Plex Sans", "Avenir Next", "Segoe UI", sans-serif;
      --mono: "SF Mono", "IBM Plex Mono", "Menlo", monospace;
      --headline-zh: "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", "Microsoft YaHei", sans-serif;
      --body-zh: "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", "Microsoft YaHei", sans-serif;
      --mono-zh: "SF Mono", "IBM Plex Mono", "PingFang SC", "Microsoft YaHei", monospace;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      background:
        radial-gradient(circle at 50% 24%, rgba(255, 106, 130, 0.16), transparent 18%),
        radial-gradient(circle at 50% 26%, rgba(127, 228, 255, 0.14), transparent 24%),
        radial-gradient(circle at 10% 10%, rgba(255, 106, 130, 0.14), transparent 26%),
        radial-gradient(circle at 90% 8%, rgba(127, 228, 255, 0.12), transparent 22%),
        linear-gradient(180deg, #101a2c 0%, #0a111c 52%, var(--paper) 100%);
      font-family: var(--body);
    }}
    body[data-lang="zh"] {{
      font-family: var(--body-zh);
      line-break: strict;
      word-break: keep-all;
    }}
    body[data-lang="zh"] .eyebrow,
    body[data-lang="zh"] .mono,
    body[data-lang="zh"] .metric-label,
    body[data-lang="zh"] .preview-label,
    body[data-lang="zh"] .palette-kicker,
    body[data-lang="zh"] .chip,
    body[data-lang="zh"] .chip-btn,
    body[data-lang="zh"] button,
    body[data-lang="zh"] label {{
      font-family: var(--body-zh);
      letter-spacing: 0.01em;
      text-transform: none;
    }}
    body[data-lang="zh"] .panel-title,
    body[data-lang="zh"] .topbar-copy strong,
    body[data-lang="zh"] .brand-copy strong,
    body[data-lang="zh"] .stage-hud-title {{
      font-family: var(--headline-zh);
      letter-spacing: 0;
      text-transform: none;
    }}
    body::before {{
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background-image:
        linear-gradient(rgba(148, 176, 209, 0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(148, 176, 209, 0.07) 1px, transparent 1px);
      background-size: 28px 28px;
      mask-image: linear-gradient(180deg, rgba(0,0,0,0.55), transparent 92%);
    }}
    body::after {{
      content: "";
      position: fixed;
      right: 44px;
      bottom: 34px;
      width: 32px;
      height: 32px;
      transform: rotate(45deg);
      border: 1px solid rgba(234, 244, 255, 0.32);
      box-shadow:
        0 0 22px rgba(255, 106, 130, 0.14),
        0 0 32px rgba(127, 228, 255, 0.12);
      pointer-events: none;
    }}
    .shell {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px;
      display: grid;
      gap: 18px;
    }}
    .topbar {{
      position: sticky;
      top: 14px;
      z-index: 35;
      display: grid;
      grid-template-columns: auto 1fr auto;
      gap: 16px;
      align-items: center;
      padding: 14px 18px;
      border: 1px solid rgba(147, 181, 215, 0.16);
      border-radius: 22px;
      background: rgba(8, 14, 24, 0.78);
      backdrop-filter: blur(14px);
      box-shadow: 0 18px 44px rgba(3, 8, 18, 0.28);
    }}
    .topbar-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }}
    .topbar-copy {{
      display: grid;
      gap: 3px;
      min-width: 0;
    }}
    .topbar-copy strong {{
      font-family: var(--headline);
      font-size: 1rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .topbar-copy span {{
      color: var(--muted);
      font-size: 0.86rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .topbar-nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      justify-content: center;
    }}
    .nav-pill {{
      padding: 10px 12px;
      border: 1px solid rgba(147, 181, 215, 0.16);
      background: rgba(127, 228, 255, 0.05);
      color: var(--muted);
      font-size: 0.76rem;
    }}
    .nav-pill:hover,
    .nav-pill:focus-visible {{
      color: var(--ink);
      border-color: rgba(127, 228, 255, 0.3);
      background: rgba(127, 228, 255, 0.1);
    }}
    .topbar-tools {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .palette-trigger {{
      padding: 10px 12px;
      font-size: 0.76rem;
    }}
    .lang-switch {{
      display: inline-flex;
      align-items: center;
      padding: 4px;
      gap: 4px;
      border-radius: 999px;
      border: 1px solid rgba(147, 181, 215, 0.16);
      background: rgba(16, 27, 43, 0.7);
    }}
    .lang-btn {{
      min-width: 68px;
      padding: 9px 12px;
      background: transparent;
      color: var(--muted);
      font-size: 0.76rem;
    }}
    .lang-btn.active {{
      background: linear-gradient(135deg, rgba(127, 228, 255, 0.22), rgba(255, 106, 130, 0.18));
      color: var(--ink);
      box-shadow: inset 0 0 0 1px rgba(127, 228, 255, 0.12);
    }}
    .hero {{
      display: grid;
      grid-template-columns: 1.4fr 0.8fr;
      gap: 18px;
      align-items: stretch;
      animation: rise .55s ease-out both;
    }}
    .hero-main, .hero-side, .panel {{
      border: 1px solid var(--line);
      border-radius: 26px;
      background: var(--panel);
      backdrop-filter: blur(10px);
      box-shadow: var(--shadow);
    }}
    .hero-main {{
      overflow: hidden;
      position: relative;
      padding: 28px;
      background:
        linear-gradient(160deg, rgba(20, 34, 53, 0.94), rgba(8, 14, 24, 0.92)),
        var(--panel);
    }}
    .hero-main::before {{
      content: "";
      position: absolute;
      inset: -12% 22% 26% 22%;
      border-radius: 999px;
      background:
        radial-gradient(circle, rgba(127, 228, 255, 0.16), transparent 46%),
        radial-gradient(circle, rgba(255, 106, 130, 0.12), transparent 58%);
      filter: blur(6px);
      pointer-events: none;
    }}
    .hero-main::after {{
      content: "";
      position: absolute;
      inset: 54px 54px auto auto;
      width: 240px;
      height: 240px;
      border-radius: 999px;
      border: 1px solid rgba(255, 136, 154, 0.28);
      box-shadow:
        inset 0 0 0 16px rgba(255, 106, 130, 0.06),
        0 0 48px rgba(255, 106, 130, 0.18);
      opacity: 0.7;
      pointer-events: none;
    }}
    .hero-side {{
      padding: 24px;
      display: grid;
      gap: 12px;
      align-content: start;
      background:
        linear-gradient(180deg, rgba(18, 28, 45, 0.92), rgba(9, 14, 24, 0.9)),
        var(--panel);
    }}
    .brand-tile {{
      display: grid;
      grid-template-columns: 88px 1fr;
      gap: 14px;
      align-items: center;
      padding: 12px;
      border-radius: 20px;
      border: 1px solid rgba(147, 181, 215, 0.18);
      background: linear-gradient(180deg, rgba(14, 24, 39, 0.9), rgba(9, 14, 24, 0.94));
      box-shadow: inset 0 0 0 1px rgba(127, 228, 255, 0.05);
    }}
    .brand-image {{
      width: 88px;
      height: 88px;
      border-radius: 20px;
      object-fit: cover;
      border: 1px solid rgba(147, 181, 215, 0.24);
      box-shadow:
        0 0 24px rgba(127, 228, 255, 0.08),
        0 0 18px rgba(255, 106, 130, 0.1);
    }}
    .brand-copy {{
      display: grid;
      gap: 4px;
    }}
    .brand-copy strong {{
      font-family: var(--headline);
      font-size: 1.08rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .brand-copy span {{
      color: var(--muted);
      font-size: 0.92rem;
      line-height: 1.35;
    }}
    .eyebrow {{
      display: inline-flex;
      gap: 8px;
      align-items: center;
      font: 700 12px/1 var(--mono);
      text-transform: uppercase;
      letter-spacing: 0.16em;
      color: var(--accent-2);
    }}
    .dot {{
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: linear-gradient(180deg, #ffa1b0, var(--accent));
      box-shadow:
        0 0 0 5px rgba(255, 106, 130, 0.12),
        0 0 18px rgba(255, 106, 130, 0.45);
    }}
    h1 {{
      margin: 12px 0 8px;
      font-family: var(--headline);
      font-size: clamp(2.8rem, 6vw, 5.8rem);
      line-height: 0.95;
      letter-spacing: -0.04em;
      text-transform: uppercase;
      max-width: 9ch;
    }}
    body[data-lang="zh"] h1 {{
      font-family: var(--headline-zh);
      font-size: clamp(2.3rem, 7vw, 4.6rem);
      line-height: 1.08;
      letter-spacing: -0.02em;
      text-transform: none;
      max-width: 12em;
    }}
    .hero-copy {{
      max-width: 60ch;
      color: var(--muted);
      font-size: 1.05rem;
      line-height: 1.65;
    }}
    .toolbar {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
    }}
    .guide-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 20px;
    }}
    .guide-card {{
      display: grid;
      gap: 8px;
      padding: 14px;
      border-radius: 18px;
      border: 1px solid rgba(147, 181, 215, 0.16);
      background: rgba(12, 20, 34, 0.68);
      box-shadow: inset 0 0 0 1px rgba(127, 228, 255, 0.04);
    }}
    .guide-step {{
      width: 34px;
      height: 34px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 999px;
      font: 700 12px/1 var(--mono);
      color: var(--ink);
      border: 1px solid rgba(127, 228, 255, 0.26);
      background: linear-gradient(180deg, rgba(127, 228, 255, 0.12), rgba(255, 106, 130, 0.12));
    }}
    button {{
      border: 0;
      cursor: pointer;
      border-radius: 999px;
      padding: 12px 16px;
      font: 700 0.88rem/1 var(--mono);
      letter-spacing: 0.02em;
      transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
    }}
    button:hover {{ transform: translateY(-1px); }}
    button:disabled {{
      opacity: 0.62;
      cursor: wait;
      transform: none;
    }}
    .btn-primary {{
      background: linear-gradient(135deg, #ff8c9f, var(--accent));
      color: #fff7fb;
      box-shadow: 0 10px 28px rgba(255, 106, 130, 0.3);
    }}
    .btn-secondary {{
      background: rgba(127, 228, 255, 0.08);
      color: var(--ink);
    }}
    .btn-danger {{
      background: rgba(255, 106, 130, 0.14);
      color: #ffd7de;
      box-shadow: inset 0 0 0 1px rgba(255, 106, 130, 0.14);
    }}
    .hero-metrics {{
      display: grid;
      gap: 10px;
    }}
    .signal-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 12px;
      margin-top: 22px;
    }}
    .hero-stage {{
      position: relative;
      height: 220px;
      margin: 18px 0 10px;
      border-radius: 24px;
      border: 1px solid rgba(147, 181, 215, 0.16);
      background:
        radial-gradient(circle at 50% 42%, rgba(127, 228, 255, 0.12), transparent 18%),
        radial-gradient(circle at 50% 46%, rgba(255, 106, 130, 0.14), transparent 24%),
        linear-gradient(180deg, rgba(15, 24, 39, 0.82), rgba(7, 11, 18, 0.94));
      overflow: hidden;
      transform-style: preserve-3d;
      transition: transform .28s ease, box-shadow .28s ease;
      will-change: transform;
    }}
    .hero-stage::after {{
      content: "";
      position: absolute;
      inset: 0;
      background:
        linear-gradient(180deg, rgba(8, 14, 24, 0.08), rgba(8, 14, 24, 0.44)),
        radial-gradient(circle at 50% 42%, rgba(127, 228, 255, 0.1), transparent 30%);
      pointer-events: none;
    }}
    .hero-stage::before {{
      content: "";
      position: absolute;
      inset: auto 0 0 0;
      height: 68px;
      background:
        linear-gradient(rgba(147, 181, 215, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(147, 181, 215, 0.08) 1px, transparent 1px);
      background-size: 30px 30px;
      opacity: 0.85;
    }}
    .hero-visual {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
      opacity: 0.92;
      filter: saturate(1.02) contrast(1.03);
      transition: transform .28s ease, filter .28s ease;
      will-change: transform;
    }}
    .stage-ring {{
      position: absolute;
      top: 22px;
      bottom: 34px;
      width: 186px;
      border: 2px solid rgba(255, 125, 145, 0.44);
      border-radius: 999px;
      background: linear-gradient(180deg, rgba(255, 124, 144, 0.1), rgba(255, 124, 144, 0.04));
      box-shadow:
        inset 0 0 0 10px rgba(255, 106, 130, 0.06),
        0 0 36px rgba(255, 106, 130, 0.18);
      transition: transform .28s ease;
      will-change: transform;
    }}
    .stage-ring-left {{ left: -24px; }}
    .stage-ring-right {{ right: -24px; }}
    .stage-ring::after {{
      content: "";
      position: absolute;
      left: 12px;
      right: 12px;
      top: 18px;
      bottom: 18px;
      border-radius: 999px;
      border: 1px solid rgba(255, 175, 186, 0.28);
    }}
    .stage-globe {{
      position: absolute;
      left: 50%;
      top: 44px;
      width: 168px;
      height: 168px;
      transform: translateX(-50%);
      border-radius: 999px;
      border: 2px solid rgba(167, 238, 255, 0.48);
      background:
        radial-gradient(circle at 50% 46%, rgba(127, 228, 255, 0.14), transparent 58%),
        radial-gradient(circle at 42% 40%, rgba(255, 122, 143, 0.18), transparent 48%);
      box-shadow:
        inset 0 0 42px rgba(127, 228, 255, 0.12),
        0 0 42px rgba(127, 228, 255, 0.12);
      transition: transform .28s ease, box-shadow .28s ease;
      will-change: transform;
    }}
    .stage-globe::before,
    .stage-globe::after {{
      content: "";
      position: absolute;
      border-radius: 999px;
      inset: 18px;
      border: 1px solid rgba(167, 238, 255, 0.22);
    }}
    .stage-globe::after {{
      inset: 48% 8px auto 8px;
      height: 1px;
      border: 0;
      background: rgba(167, 238, 255, 0.28);
    }}
    .stage-console {{
      position: absolute;
      bottom: 34px;
      width: 126px;
      height: 58px;
      border-radius: 16px;
      border: 1px solid rgba(147, 181, 215, 0.24);
      background:
        linear-gradient(180deg, rgba(16, 26, 41, 0.94), rgba(9, 14, 24, 0.98));
      box-shadow: inset 0 0 0 1px rgba(127, 228, 255, 0.06);
      transition: transform .28s ease;
      will-change: transform;
    }}
    .stage-console-left {{ left: 22%; }}
    .stage-console-right {{ right: 22%; }}
    .stage-console::before {{
      content: "";
      position: absolute;
      left: 16px;
      right: 16px;
      top: 16px;
      height: 4px;
      background:
        linear-gradient(90deg, rgba(127, 228, 255, 0.54), rgba(255, 106, 130, 0.72));
      border-radius: 999px;
    }}
    .stage-hud {{
      position: absolute;
      left: 16px;
      right: 16px;
      top: 16px;
      display: grid;
      gap: 8px;
      padding: 12px 14px;
      border-radius: 18px;
      border: 1px solid rgba(147, 181, 215, 0.22);
      background: linear-gradient(180deg, rgba(8, 14, 24, 0.76), rgba(8, 14, 24, 0.28));
      backdrop-filter: blur(10px);
      box-shadow: inset 0 0 0 1px rgba(127, 228, 255, 0.05);
      z-index: 2;
      pointer-events: none;
    }}
    .stage-hud-title {{
      font-family: var(--headline);
      font-size: 1.1rem;
      letter-spacing: 0.02em;
      text-transform: uppercase;
    }}
    .stage-hud-summary {{
      color: var(--muted);
      font-size: 0.9rem;
      line-height: 1.4;
      max-width: 58ch;
    }}
    .stage-hud-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .metric {{
      padding: 16px;
      border-radius: 18px;
      border: 1px solid var(--line);
      background: rgba(17, 28, 45, 0.72);
    }}
    .metric-label {{
      font: 700 11px/1 var(--mono);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--muted);
    }}
    .metric-value {{
      margin-top: 8px;
      font-family: var(--headline);
      font-size: clamp(1.8rem, 3vw, 2.8rem);
      line-height: 1;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1.05fr 1.05fr 0.9fr;
      gap: 18px;
      animation: rise .7s ease-out both;
      animation-delay: .08s;
    }}
    .dual-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
      animation: rise .76s ease-out both;
      animation-delay: .12s;
    }}
    .panel {{
      padding: 22px;
      display: grid;
      gap: 14px;
      align-content: start;
    }}
    .panel-head {{
      display: flex;
      align-items: start;
      justify-content: space-between;
      gap: 12px;
    }}
    .panel-title {{
      margin: 0;
      font-family: var(--headline);
      font-size: 1.55rem;
      letter-spacing: -0.02em;
      text-transform: uppercase;
    }}
    .panel-sub {{
      color: var(--muted);
      font-size: 0.95rem;
      line-height: 1.6;
    }}
    .stack {{
      display: grid;
      gap: 12px;
    }}
    .card {{
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 14px 16px;
      background: rgba(16, 27, 43, 0.76);
    }}
    .card-top {{
      display: flex;
      align-items: start;
      justify-content: space-between;
      gap: 12px;
    }}
    .card-title {{
      margin: 0;
      font-size: 1.08rem;
      line-height: 1.2;
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border-radius: 999px;
      padding: 5px 9px;
      font: 700 11px/1 var(--mono);
      text-transform: uppercase;
      background: rgba(127, 228, 255, 0.08);
      color: var(--muted);
    }}
    .chip.hot {{ background: rgba(255, 106, 130, 0.14); color: var(--accent); }}
    .chip.ok {{ background: rgba(127, 228, 255, 0.14); color: var(--accent-2); }}
    .chip-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 8px;
    }}
    .chip-btn {{
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 6px 10px;
      background: rgba(127, 228, 255, 0.05);
      color: var(--muted);
      font: 700 11px/1 var(--mono);
      text-transform: uppercase;
      cursor: pointer;
      transition: background 140ms ease, border-color 140ms ease, color 140ms ease;
    }}
    .chip-btn:hover {{
      border-color: rgba(127, 228, 255, 0.32);
      color: var(--text);
    }}
    .chip-btn.active {{
      background: rgba(127, 228, 255, 0.16);
      border-color: rgba(127, 228, 255, 0.36);
      color: var(--accent-2);
    }}
    .meta {{
      margin-top: 10px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px 12px;
      font: 700 12px/1.35 var(--mono);
      color: var(--muted);
    }}
    .actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }}
    .actions button {{
      padding: 9px 12px;
      font-size: 0.76rem;
    }}
    .actions a {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 999px;
      padding: 9px 12px;
      font: 700 0.76rem/1 var(--mono);
      letter-spacing: 0.02em;
      background: rgba(127, 228, 255, 0.08);
      color: var(--ink);
      text-decoration: none;
      transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
    }}
    .actions a:hover {{
      transform: translateY(-1px);
    }}
    form {{
      display: grid;
      gap: 12px;
    }}
    .control-cluster {{
      display: grid;
      gap: 10px;
      padding: 14px;
      border-radius: 18px;
      border: 1px solid rgba(147, 181, 215, 0.14);
      background: rgba(10, 18, 31, 0.44);
    }}
    .deck-mode-strip {{
      display: grid;
      gap: 12px;
      padding: 14px;
      border-radius: 18px;
      border: 1px solid rgba(147, 181, 215, 0.14);
      background:
        linear-gradient(180deg, rgba(13, 22, 37, 0.84), rgba(10, 18, 31, 0.58));
      box-shadow: inset 0 0 0 1px rgba(127, 228, 255, 0.04);
    }}
    .deck-mode-head {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: start;
      justify-content: space-between;
    }}
    .advanced-toggle {{
      white-space: nowrap;
    }}
    .advanced-summary {{
      min-height: 36px;
    }}
    .advanced-summary .chip {{
      background: rgba(255, 255, 255, 0.04);
    }}
    .compact-stack {{
      gap: 8px;
    }}
    .deck-advanced-panel {{
      display: grid;
      gap: 12px;
      overflow: hidden;
      max-height: 1200px;
      opacity: 1;
      transform: translateY(0);
      transition: max-height .24s ease, opacity .2s ease, transform .2s ease, margin .2s ease;
    }}
    .deck-advanced-panel.collapsed {{
      max-height: 0;
      opacity: 0;
      transform: translateY(-8px);
      pointer-events: none;
      margin-top: -8px;
    }}
    .deck-section {{
      display: grid;
      gap: 12px;
      padding: 14px;
      border-radius: 18px;
      border: 1px solid rgba(147, 181, 215, 0.14);
      background: rgba(10, 18, 31, 0.5);
    }}
    .deck-section-head {{
      display: flex;
      gap: 12px;
      align-items: start;
    }}
    .step-index {{
      width: 34px;
      height: 34px;
      flex: 0 0 auto;
      border-radius: 12px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font: 700 12px/1 var(--mono);
      color: var(--ink);
      border: 1px solid rgba(147, 181, 215, 0.16);
      background: rgba(127, 228, 255, 0.08);
    }}
    .field-hint {{
      display: block;
      margin-top: 2px;
      font: 500 12px/1.45 var(--body);
      letter-spacing: 0;
      text-transform: none;
      color: var(--muted);
    }}
    .section-jumps {{
      margin-top: 2px;
    }}
    .field-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}
    .section-toolbox {{
      display: grid;
      gap: 12px;
      padding: 14px;
      border-radius: 18px;
      border: 1px solid rgba(147, 181, 215, 0.14);
      background:
        linear-gradient(180deg, rgba(11, 19, 31, 0.78), rgba(9, 15, 25, 0.54));
      box-shadow: inset 0 0 0 1px rgba(127, 228, 255, 0.04);
    }}
    .section-toolbox-head {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: start;
      justify-content: space-between;
    }}
    .section-toolbox-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .search-shell {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
      align-items: center;
    }}
    .batch-toolbar {{
      display: grid;
      gap: 12px;
    }}
    .batch-toolbar-card {{
      position: sticky;
      top: 92px;
      z-index: 12;
      backdrop-filter: blur(12px);
      background: rgba(9, 15, 26, 0.86);
    }}
    .batch-toolbar-card.selection-live {{
      border-color: rgba(127, 228, 255, 0.24);
      box-shadow:
        var(--shadow),
        inset 0 0 0 1px rgba(127, 228, 255, 0.08);
    }}
    .batch-toolbar-head {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      justify-content: space-between;
      align-items: start;
    }}
    .checkbox-inline {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font: 700 12px/1 var(--mono);
      color: var(--muted);
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }}
    .checkbox-inline input {{
      width: 18px;
      height: 18px;
      margin: 0;
      accent-color: var(--accent-2);
      cursor: pointer;
    }}
    .triage-card-head {{
      display: grid;
      gap: 10px;
      min-width: 0;
    }}
    label {{
      display: grid;
      gap: 6px;
      font: 700 12px/1 var(--mono);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
    }}
    input, select, textarea {{
      width: 100%;
      border: 1px solid rgba(147, 181, 215, 0.16);
      border-radius: 14px;
      background: rgba(11, 18, 30, 0.86);
      color: var(--ink);
      padding: 13px 14px;
      font: 500 0.96rem/1.2 var(--body);
    }}
    textarea {{
      resize: vertical;
      min-height: 84px;
    }}
    input:focus, select:focus, textarea:focus {{
      outline: none;
      border-color: rgba(127, 228, 255, 0.48);
      box-shadow:
        0 0 0 1px rgba(127, 228, 255, 0.24),
        0 0 0 5px rgba(127, 228, 255, 0.08);
    }}
    .mission-preview.ready {{
      border-color: rgba(127, 228, 255, 0.28);
      box-shadow: inset 0 0 0 1px rgba(127, 228, 255, 0.08);
    }}
    .preview-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}
    .preview-line {{
      border-radius: 14px;
      border: 1px solid var(--line);
      padding: 12px;
      background: rgba(16, 27, 43, 0.64);
    }}
    .preview-label {{
      font: 700 11px/1 var(--mono);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
    }}
    .preview-value {{
      margin-top: 8px;
      font-size: 0.98rem;
      line-height: 1.35;
    }}
    .preview-meter {{
      position: relative;
      height: 10px;
      border-radius: 999px;
      overflow: hidden;
      background: rgba(127, 228, 255, 0.08);
      border: 1px solid rgba(147, 181, 215, 0.16);
    }}
    .preview-meter-fill {{
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, rgba(127, 228, 255, 0.72), rgba(255, 106, 130, 0.82));
      transition: width .24s ease;
    }}
    .shortcut-strip {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .shortcut-strip .chip {{
      background: rgba(255, 255, 255, 0.04);
    }}
    .toast-rack {{
      position: fixed;
      right: 20px;
      bottom: 22px;
      z-index: 50;
      display: grid;
      gap: 10px;
      width: min(360px, calc(100vw - 32px));
      pointer-events: none;
    }}
    .toast {{
      padding: 14px 16px;
      border-radius: 18px;
      border: 1px solid rgba(147, 181, 215, 0.24);
      background: rgba(9, 15, 28, 0.94);
      color: var(--ink);
      box-shadow: var(--shadow);
      animation: rise .22s ease-out both;
    }}
    .toast.success {{
      border-color: rgba(127, 228, 255, 0.3);
      box-shadow:
        var(--shadow),
        0 0 0 1px rgba(127, 228, 255, 0.08);
    }}
    .toast.error {{
      border-color: rgba(255, 106, 130, 0.3);
      box-shadow:
        var(--shadow),
        0 0 0 1px rgba(255, 106, 130, 0.08);
    }}
    .action-log {{
      display: grid;
      gap: 10px;
    }}
    .action-log-item {{
      display: grid;
      gap: 8px;
      border-radius: 16px;
      border: 1px solid var(--line);
      padding: 12px;
      background: rgba(16, 27, 43, 0.72);
    }}
    .palette-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(4, 8, 16, 0.72);
      backdrop-filter: blur(10px);
      z-index: 60;
      display: none;
      align-items: start;
      justify-content: center;
      padding: 8vh 16px 16px;
    }}
    .palette-backdrop.open {{
      display: flex;
    }}
    .palette-shell {{
      width: min(760px, 100%);
      border-radius: 24px;
      border: 1px solid rgba(147, 181, 215, 0.24);
      background: rgba(7, 12, 22, 0.96);
      box-shadow: var(--shadow);
      overflow: hidden;
    }}
    .palette-head {{
      padding: 14px;
      border-bottom: 1px solid var(--line);
    }}
    .palette-input {{
      width: 100%;
      border-radius: 16px;
      border: 1px solid rgba(147, 181, 215, 0.18);
      background: rgba(11, 18, 30, 0.92);
      color: var(--ink);
      padding: 14px 16px;
      font: 500 1rem/1.2 var(--body);
    }}
    .palette-list {{
      display: grid;
      gap: 0;
      max-height: 56vh;
      overflow: auto;
    }}
    .palette-item {{
      display: grid;
      gap: 6px;
      padding: 14px 16px;
      border-bottom: 1px solid rgba(147, 181, 215, 0.1);
      cursor: pointer;
      transition: background .14s ease;
    }}
    .palette-item.active {{
      background: rgba(127, 228, 255, 0.12);
    }}
    .palette-item:hover {{
      background: rgba(127, 228, 255, 0.08);
    }}
    .palette-kicker {{
      font: 700 11px/1 var(--mono);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
    }}
    .suggestion-grid {{
      display: grid;
      gap: 12px;
    }}
    .suggestion-list {{
      display: grid;
      gap: 8px;
    }}
    .skeleton {{
      position: relative;
      overflow: hidden;
    }}
    .skeleton::after {{
      content: "";
      position: absolute;
      inset: 0;
      transform: translateX(-100%);
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
      animation: shimmer 1.2s infinite;
    }}
    .skeleton-block {{
      height: 14px;
      border-radius: 999px;
      background: rgba(147, 181, 215, 0.12);
    }}
    .skeleton-block.short {{ width: 34%; }}
    .skeleton-block.medium {{ width: 58%; }}
    .skeleton-block.long {{ width: 84%; }}
    .status-shell {{
      display: grid;
      gap: 10px;
    }}
    .state-banner {{
      border-radius: 18px;
      padding: 16px;
      background: linear-gradient(135deg, rgba(127, 228, 255, 0.12), rgba(10, 18, 31, 0.74));
      border: 1px solid rgba(127, 228, 255, 0.16);
    }}
    .state-banner.error {{
      background: linear-gradient(135deg, rgba(255, 106, 130, 0.16), rgba(10, 18, 31, 0.72));
      border-color: rgba(255, 106, 130, 0.18);
    }}
    .mono {{
      font-family: var(--mono);
      color: var(--muted);
      font-size: 12px;
    }}
    .empty {{
      padding: 24px;
      border-radius: 16px;
      border: 1px dashed rgba(147, 181, 215, 0.24);
      color: var(--muted);
      text-align: center;
    }}
    .story-grid {{
      display: grid;
      grid-template-columns: 0.96fr 1.14fr;
      gap: 16px;
      align-items: start;
    }}
    .story-list {{
      display: grid;
      gap: 12px;
      max-height: 760px;
      overflow: auto;
      padding-right: 4px;
    }}
    .card.selected {{
      border-color: rgba(127, 228, 255, 0.3);
      box-shadow: inset 0 0 0 1px rgba(127, 228, 255, 0.16);
      background: rgba(15, 26, 41, 0.9);
    }}
    .card.selectable {{
      cursor: pointer;
      transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
    }}
    .card.selectable:hover {{
      transform: translateY(-1px);
      border-color: rgba(127, 228, 255, 0.24);
    }}
    .entity-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }}
    .story-detail {{
      display: grid;
      gap: 12px;
    }}
    .story-columns {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}
    .timeline-strip {{
      display: grid;
      grid-auto-flow: column;
      grid-auto-columns: minmax(180px, 220px);
      gap: 10px;
      overflow-x: auto;
      padding-bottom: 6px;
    }}
    .timeline-event {{
      border-radius: 16px;
      border: 1px solid var(--line);
      padding: 12px;
      background: rgba(16, 27, 43, 0.78);
      display: grid;
      gap: 8px;
    }}
    .timeline-event.ok {{
      border-color: rgba(127, 228, 255, 0.28);
    }}
    .timeline-event.hot {{
      border-color: rgba(255, 106, 130, 0.28);
    }}
    .graph-shell {{
      display: grid;
      gap: 12px;
    }}
    .graph-canvas {{
      border-radius: 18px;
      border: 1px solid var(--line);
      background:
        radial-gradient(circle at 50% 45%, rgba(127, 228, 255, 0.12), transparent 42%),
        linear-gradient(180deg, rgba(17, 27, 43, 0.92), rgba(9, 14, 24, 0.94));
      overflow: hidden;
    }}
    .graph-canvas svg {{
      width: 100%;
      height: auto;
      display: block;
    }}
    .graph-meta {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}
    .mini-list {{
      display: grid;
      gap: 8px;
    }}
    .mini-item {{
      border-radius: 14px;
      border: 1px solid var(--line);
      padding: 10px 12px;
      background: rgba(16, 27, 43, 0.72);
      font: 700 12px/1.4 var(--mono);
      color: var(--muted);
    }}
    .text-block {{
      margin: 0;
      padding: 14px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: rgba(16, 27, 43, 0.74);
      white-space: pre-wrap;
      overflow: auto;
      font: 500 12px/1.55 var(--mono);
      color: var(--ink);
    }}
    .footer-note {{
      padding: 18px 0 8px;
      color: var(--muted);
      font-size: 0.92rem;
      text-align: center;
    }}
    @keyframes rise {{
      from {{ opacity: 0; transform: translateY(12px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes shimmer {{
      to {{ transform: translateX(100%); }}
    }}
    @media (max-width: 1100px) {{
      .topbar {{ grid-template-columns: 1fr; }}
      .topbar-nav {{
        justify-content: start;
        flex-wrap: nowrap;
        overflow-x: auto;
        padding-bottom: 2px;
        scrollbar-width: none;
      }}
      .topbar-nav::-webkit-scrollbar {{ display: none; }}
      .hero, .grid, .dual-grid {{ grid-template-columns: 1fr; }}
      .hero-side {{ order: -1; }}
      .story-grid, .story-columns {{ grid-template-columns: 1fr; }}
      .preview-grid, .guide-grid {{ grid-template-columns: 1fr; }}
      .batch-toolbar-card {{ top: 152px; }}
    }}
    @media (max-width: 760px) {{
      .shell {{ padding: 16px; }}
      .topbar {{
        top: 10px;
        padding: 12px 14px;
      }}
      .topbar-copy span {{ white-space: normal; }}
      .signal-strip, .field-grid {{ grid-template-columns: 1fr 1fr; }}
      .topbar-tools {{ flex-wrap: wrap; justify-content: start; }}
      .hero-main, .hero-side, .panel {{ border-radius: 22px; }}
      .hero-main, .hero-side, .panel {{ padding: 18px; }}
      h1 {{
        max-width: none;
        font-size: clamp(2.2rem, 11vw, 3.3rem);
        line-height: 1.02;
      }}
      body[data-lang="zh"] h1 {{
        font-size: clamp(2rem, 10vw, 3.1rem);
        line-height: 1.14;
      }}
      .hero-copy {{ font-size: 0.98rem; }}
      .hero-stage {{ height: 150px; }}
      .stage-ring {{ top: 24px; bottom: 20px; width: 124px; }}
      .stage-globe {{ width: 112px; height: 112px; top: 22px; }}
      .stage-console {{ width: 88px; height: 42px; bottom: 18px; }}
      .guide-grid {{ gap: 10px; }}
      .guide-card, .deck-section, .control-cluster {{ padding: 12px; }}
      .deck-mode-strip {{ padding: 12px; }}
      .batch-toolbar-card {{ top: 132px; }}
    }}
    @media (max-width: 560px) {{
      .signal-strip, .field-grid {{ grid-template-columns: 1fr; }}
      .toolbar {{ flex-direction: column; }}
      .search-shell {{ grid-template-columns: 1fr; }}
      .toolbar > button,
      .toolbar > a,
      .actions > button,
      .actions > a {{
        width: 100%;
      }}
      .topbar-tools {{ width: 100%; }}
      .palette-trigger {{ flex: 1 1 auto; }}
      .lang-switch {{ margin-left: auto; }}
      .hero-stage {{ display: none; }}
      .nav-pill {{ white-space: nowrap; }}
      .batch-toolbar-card {{ top: 122px; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <header class="topbar">
      <div class="topbar-brand">
        <span class="dot"></span>
        <div class="topbar-copy">
          <strong id="topbar-title">DataPulse Operations Console</strong>
          <span id="topbar-subtitle">Mission -> Triage -> Story -> Delivery</span>
        </div>
      </div>
      <nav class="topbar-nav" aria-label="Section Navigation">
        <button class="nav-pill" id="nav-intake" type="button" data-jump-target="section-intake">Quick Start</button>
        <button class="nav-pill" id="nav-board" type="button" data-jump-target="section-board">Mission Board</button>
        <button class="nav-pill" id="nav-cockpit" type="button" data-jump-target="section-cockpit">Cockpit</button>
        <button class="nav-pill" id="nav-triage" type="button" data-jump-target="section-triage">Triage</button>
        <button class="nav-pill" id="nav-story" type="button" data-jump-target="section-story">Stories</button>
        <button class="nav-pill" id="nav-ops" type="button" data-jump-target="section-ops">Ops</button>
      </nav>
      <div class="topbar-tools">
        <button class="btn-secondary palette-trigger" id="palette-open" type="button">Command Palette</button>
        <div class="lang-switch" id="language-switch" aria-label="Language Switch">
          <button class="lang-btn active" id="lang-en" type="button" data-lang="en">EN</button>
          <button class="lang-btn" id="lang-zh" type="button" data-lang="zh">简中</button>
        </div>
      </div>
    </header>

    <section class="hero" id="section-intake">
      <div class="hero-main" id="hero-main">
        <div class="eyebrow" id="hero-eyebrow"><span class="dot"></span> Guided Analyst Workflow</div>
        <h1 id="hero-title">Run Missions, Review Signal, Publish Stories</h1>
        <p class="hero-copy" id="hero-copy">This console follows the real operating path: draft a watch, run it, triage the evidence, then promote verified signal into stories and delivery.</p>
        <div class="toolbar">
          <button class="btn-primary" id="refresh-all">Refresh Console</button>
          <button class="btn-secondary" id="run-due">Run Due Missions</button>
          <button class="btn-secondary" id="jump-watch-board" type="button" data-jump-target="section-board">Open Mission Board</button>
        </div>
        <div class="guide-grid">
          <div class="guide-card">
            <div class="guide-step">01</div>
            <div class="mono" id="guide-step-1-title">Start With A Draft</div>
            <div class="panel-sub" id="guide-step-1-copy">Use a preset, clone an existing watch, or enter just Name + Query to get moving.</div>
          </div>
          <div class="guide-card">
            <div class="guide-step">02</div>
            <div class="mono" id="guide-step-2-title">Add Scope Only If Needed</div>
            <div class="panel-sub" id="guide-step-2-copy">Schedule, platform, and domain narrow the watch. Leave them open if you need broad discovery first.</div>
          </div>
          <div class="guide-card">
            <div class="guide-step">03</div>
            <div class="mono" id="guide-step-3-title">Arm Alerts Last</div>
            <div class="panel-sub" id="guide-step-3-copy">Route, keyword, score, and confidence are optional. Add them only when you want automated delivery.</div>
          </div>
        </div>
        <div class="hero-stage" aria-hidden="true">
          <img class="hero-visual" src="/brand/hero" alt="DataPulse command chamber brand visual">
          <div class="stage-ring stage-ring-left"></div>
          <div class="stage-ring stage-ring-right"></div>
          <div class="stage-globe"></div>
          <div class="stage-console stage-console-left"></div>
          <div class="stage-console stage-console-right"></div>
          <div class="stage-hud" id="stage-hud"></div>
        </div>
        <div class="signal-strip" id="overview-metrics"></div>
      </div>
      <aside class="hero-side">
        <div class="guide-card">
          <div class="card-top">
            <div>
              <div class="mono" id="guide-kicker">Operator Guidance</div>
              <h2 class="panel-title" id="guide-panel-title">Mission Intake</h2>
            </div>
            <span class="chip ok" id="guide-chip">Start here</span>
          </div>
          <div class="panel-sub" id="guide-panel-copy">Required fields come first. Alert gating is optional, and the mission preview updates as you type.</div>
          <div class="shortcut-strip">
            <span class="chip" id="shortcut-focus">/ focus draft</span>
            <span class="chip" id="shortcut-preset">1-4 load preset</span>
            <span class="chip" id="shortcut-submit">Cmd/Ctrl+Enter deploy</span>
          </div>
          <div class="chip-row section-jumps">
            <button class="chip-btn" id="jump-cockpit" type="button" data-jump-target="section-cockpit">Cockpit</button>
            <button class="chip-btn" id="jump-triage" type="button" data-jump-target="section-triage">Triage</button>
            <button class="chip-btn" id="jump-story" type="button" data-jump-target="section-story">Stories</button>
            <button class="chip-btn" id="jump-ops" type="button" data-jump-target="section-ops">Ops</button>
          </div>
        </div>
        <div class="panel-head">
          <div>
            <div class="panel-title" id="deploy-title">Deploy Mission</div>
            <div class="panel-sub" id="deploy-copy">Create one watch, add optional scope, then decide whether alert routing is needed.</div>
          </div>
        </div>
        <div class="control-cluster" id="create-watch-preset-panel">
          <div class="mono" id="preset-title">Mission Modes</div>
          <div class="panel-sub" id="preset-copy">Start from an archetype when the workflow is familiar, then only adjust the fields that matter.</div>
          <div class="chip-row" id="create-watch-presets"></div>
        </div>
        <form id="create-watch-form">
          <div class="deck-section">
            <div class="deck-section-head">
              <span class="step-index">01</span>
              <div>
                <div class="mono" id="deck-step-1-title">Required Mission Input</div>
                <div class="panel-sub" id="deck-step-1-copy">Name and query define the watch. Everything else can be layered on later.</div>
              </div>
            </div>
            <div class="field-grid">
              <label><span id="label-name">Name</span><input id="input-name" name="name" list="mission-name-options-list" placeholder="Launch Ops" required><span class="field-hint" id="hint-name">Use a short operator-facing label.</span></label>
              <label><span id="label-query">Query</span><input id="input-query" name="query" list="query-options-list" placeholder="OpenAI launch" required><span class="field-hint" id="hint-query">Describe the signal you want tracked.</span></label>
            </div>
          </div>
          <div class="deck-mode-strip">
            <div class="deck-mode-head">
              <div>
                <div class="mono" id="deck-advanced-title">Keep It Simple First</div>
                <div class="panel-sub" id="deck-advanced-copy">Most missions only need Name and Query. Open advanced settings only when you need scope or alert delivery.</div>
              </div>
              <button class="btn-secondary advanced-toggle" id="create-watch-advanced-toggle" type="button">Show Advanced</button>
            </div>
            <div class="chip-row advanced-summary" id="create-watch-advanced-summary"></div>
          </div>
          <div class="deck-advanced-panel" id="create-watch-advanced-panel">
          <div class="deck-section">
            <div class="deck-section-head">
              <span class="step-index">02</span>
              <div>
                <div class="mono" id="deck-step-2-title">Scope And Cadence</div>
                <div class="panel-sub" id="deck-step-2-copy">Use schedule and platform to narrow the mission only when you already know the operating lane.</div>
              </div>
            </div>
            <div class="field-grid">
              <label><span id="label-schedule">Schedule</span><input id="input-schedule" name="schedule" list="schedule-options-list" placeholder="@hourly / interval:15m"><span class="field-hint" id="hint-schedule">Manual is fine for first exploration.</span></label>
              <label><span id="label-platform">Platform</span><input id="input-platform" name="platform" list="platform-options-list" placeholder="twitter"><span class="field-hint" id="hint-platform">Leave empty for broader discovery.</span></label>
            </div>
            <label><span id="label-domain">Alert Domain</span><input id="input-domain" name="domain" list="domain-options-list" placeholder="openai.com"><span class="field-hint" id="hint-domain">Optional domain guard for tighter recall.</span></label>
            <div class="stack compact-stack">
              <div class="mono" id="schedule-lanes-title">Schedule Lanes</div>
              <div class="chip-row" id="create-watch-schedule-picks"></div>
            </div>
            <div class="stack compact-stack">
              <div class="mono" id="platform-lanes-title">Platform Lanes</div>
              <div class="chip-row" id="create-watch-platform-picks"></div>
            </div>
          </div>
          <div class="deck-section">
            <div class="deck-section-head">
              <span class="step-index">03</span>
              <div>
                <div class="mono" id="deck-step-3-title">Optional Alert Gate</div>
                <div class="panel-sub" id="deck-step-3-copy">Attach delivery only when the mission is ready to trigger downstream action.</div>
              </div>
            </div>
            <div class="field-grid">
              <label><span id="label-route">Alert Route</span><input id="input-route" name="route" list="route-options-list" placeholder="ops-webhook"><span class="field-hint" id="hint-route">Choose a named route when the watch should notify someone.</span></label>
              <label><span id="label-keyword">Alert Keyword</span><input id="input-keyword" name="keyword" list="keyword-options-list" placeholder="launch"><span class="field-hint" id="hint-keyword">Use a high-signal term to reduce noise.</span></label>
            </div>
            <div class="stack compact-stack">
              <div class="mono" id="route-snap-title">Route Snap</div>
              <div class="chip-row" id="create-watch-route-picks"></div>
            </div>
            <div class="field-grid">
              <label><span id="label-score">Min Score</span><input id="input-score" name="min_score" list="score-options-list" placeholder="70" inputmode="numeric"><span class="field-hint" id="hint-score">Use when you only want stronger ranked hits.</span></label>
              <label><span id="label-confidence">Min Confidence</span><input id="input-confidence" name="min_confidence" list="confidence-options-list" placeholder="0.8" inputmode="decimal"><span class="field-hint" id="hint-confidence">Use when analyst quality matters more than coverage.</span></label>
            </div>
          </div>
          </div>
          <div class="toolbar">
            <button class="btn-primary" id="create-watch-submit" type="submit">Create Watch</button>
            <button class="btn-secondary" id="create-watch-clear" type="button">Reset Draft</button>
          </div>
          <div class="panel-sub" id="create-watch-feedback">Required fields: `Name` and `Query`. Use `/` to focus the mission deck.</div>
        </form>
        <datalist id="mission-name-options-list"></datalist>
        <datalist id="query-options-list"></datalist>
        <datalist id="schedule-options-list"></datalist>
        <datalist id="platform-options-list"></datalist>
        <datalist id="domain-options-list"></datalist>
        <datalist id="route-options-list"></datalist>
        <datalist id="keyword-options-list"></datalist>
        <datalist id="score-options-list"></datalist>
        <datalist id="confidence-options-list"></datalist>
        <div class="card mission-preview" id="create-watch-preview"></div>
        <div class="card" id="create-watch-suggestions"></div>
        <div class="control-cluster" id="create-watch-clone-panel">
          <div class="mono" id="clone-title">Clone Existing Mission</div>
          <div class="panel-sub" id="clone-copy">Fork an existing watch when the current mission is only a variation in route, threshold, or query wording.</div>
          <div class="chip-row" id="create-watch-clones"></div>
        </div>
        <div class="control-cluster">
          <div class="mono" id="actions-title">Recent Actions</div>
          <div class="panel-sub" id="actions-copy">Every reversible mutation stays here briefly so you can undo false starts without losing flow.</div>
          <div class="action-log" id="console-action-history"></div>
        </div>
      </aside>
    </section>

    <section class="grid">
      <article class="panel" id="section-board">
        <div class="panel-head">
          <div>
            <h2 class="panel-title" id="board-title">Mission Board</h2>
            <div class="panel-sub" id="board-copy">Run, inspect, pause, or remove watch missions from one board.</div>
          </div>
        </div>
        <div class="stack" id="watch-list"></div>
      </article>

      <article class="panel">
        <div class="panel-head">
          <div>
            <h2 class="panel-title" id="alert-stream-title">Alert Stream</h2>
            <div class="panel-sub" id="alert-stream-copy">Read recent alert events without confusing them with editable route configuration.</div>
          </div>
          <span class="chip" id="alert-stream-mode">Events read-only</span>
        </div>
        <div class="stack" id="alert-list"></div>
        <div class="control-cluster" id="route-manager-shell">
          <div class="deck-mode-head">
            <div>
              <div class="mono" id="route-manager-title">Route Manager</div>
              <div class="panel-sub" id="route-manager-copy">Create named delivery sinks once, then reuse them across missions without retyping webhook or chat details.</div>
            </div>
            <span class="chip ok" id="route-manager-mode">Editable</span>
          </div>
          <div class="card" id="route-deck"></div>
          <div class="stack" id="route-list"></div>
        </div>
      </article>

      <article class="panel" id="section-ops">
        <div class="panel-head">
          <div>
            <h2 class="panel-title" id="ops-title">Ops Snapshot</h2>
            <div class="panel-sub" id="ops-copy">Watch daemon health, collector risk, route delivery, and recent failures in one slice.</div>
          </div>
        </div>
        <div class="status-shell" id="status-card"></div>
      </article>
    </section>

    <section class="dual-grid">
      <article class="panel" id="section-cockpit">
        <div class="panel-head">
          <div>
            <h2 class="panel-title" id="cockpit-title">Mission Cockpit</h2>
            <div class="panel-sub" id="cockpit-copy">Open one mission to inspect runs, filters, retry guidance, and alert rules.</div>
          </div>
        </div>
        <div class="stack" id="watch-detail"></div>
      </article>

      <article class="panel">
        <div class="panel-head">
          <div>
            <h2 class="panel-title" id="distribution-title">Distribution Health</h2>
            <div class="panel-sub" id="distribution-copy">See whether named delivery routes are healthy before they become silent failures.</div>
          </div>
          <span class="chip" id="distribution-mode">Read-only</span>
        </div>
        <div class="stack" id="route-health"></div>
      </article>
    </section>

    <section class="panel" id="section-triage">
      <div class="panel-head">
        <div>
          <h2 class="panel-title" id="triage-title">Triage Queue</h2>
          <div class="panel-sub" id="triage-copy">Review open items, mark duplicates, and capture analyst reasoning without leaving the queue.</div>
        </div>
      </div>
      <div class="meta" id="triage-stats-inline"></div>
      <div class="stack" id="triage-list"></div>
    </section>

    <section class="panel" id="section-story">
      <div class="panel-head">
        <div>
          <h2 class="panel-title" id="story-title">Story Workspace</h2>
          <div class="panel-sub" id="story-copy">Inspect clustered stories, evidence stacks, contradictions, and exportable summaries.</div>
        </div>
      </div>
      <div class="meta" id="story-stats-inline"></div>
      <div class="control-cluster" id="story-intake-shell">
        <div class="deck-mode-head">
          <div>
            <div class="mono" id="story-intake-title">Story Intake</div>
            <div class="panel-sub" id="story-intake-copy">Capture a manual brief when a story should exist before clustering catches up, then refine it inside the workspace.</div>
          </div>
          <span class="chip ok" id="story-intake-mode">Editable</span>
        </div>
        <div class="card" id="story-intake-deck"></div>
      </div>
      <div class="story-grid">
        <div class="story-list" id="story-list"></div>
        <div class="story-detail" id="story-detail"></div>
      </div>
    </section>

    <div class="footer-note" id="footer-note">The browser is the operating surface. CLI and MCP remain first-class control planes.</div>
  </div>
  <div class="toast-rack" id="toast-rack" aria-live="polite" aria-atomic="false"></div>
  <div class="palette-backdrop" id="command-palette">
    <div class="palette-shell">
      <div class="palette-head">
        <input class="palette-input" id="command-palette-input" type="text" placeholder="Search actions, missions, stories, or routes">
      </div>
      <div class="palette-list" id="command-palette-list"></div>
    </div>
  </div>

    <script>
    const initial = {initial_state};
    const state = {{
      watches: [],
      watchDetails: {{}},
      watchResultFilters: {{}},
      selectedWatchId: "",
      watchSearch: "",
      alerts: [],
      routes: [],
      routeSearch: "",
      routeDraft: null,
      routeEditingId: "",
      routeAdvancedOpen: null,
      routeHealth: [],
      status: null,
      ops: null,
      overview: null,
      triage: [],
      triageStats: null,
      triageFilter: "open",
      triageSearch: "",
      triagePinnedIds: [],
      selectedTriageId: "",
      selectedTriageIds: [],
      triageBulkBusy: false,
      triageExplain: {{}},
      triageNoteDrafts: {{}},
      stories: [],
      storyDraft: null,
      storySearch: "",
      storyFilter: "all",
      storySort: "attention",
      selectedStoryIds: [],
      storyBulkBusy: false,
      storyDetails: {{}},
      storyGraph: {{}},
      storyMarkdown: {{}},
      selectedStoryId: "",
      createWatchDraft: null,
      createWatchEditingId: "",
      createWatchAdvancedOpen: null,
      createWatchPresetId: "",
      createWatchSuggestions: null,
      createWatchSuggestionTimer: 0,
      actionLog: [],
      language: "en",
      loading: {{
        board: false,
        watchDetail: false,
        storyDetail: false,
        suggestions: false,
      }},
      commandPalette: {{
        open: false,
        query: "",
        selectedIndex: 0,
      }},
    }};

    const $ = (id) => document.getElementById(id);
    const jsonHeaders = {{ "Content-Type": "application/json" }};

    async function api(path, options = {{}}) {{
      const response = await fetch(path, options);
      if (!response.ok) {{
        const detail = await response.text();
        throw new Error(detail || `Request failed: ${{response.status}}`);
      }}
      return response.json();
    }}

    async function apiText(path, options = {{}}) {{
      const response = await fetch(path, options);
      if (!response.ok) {{
        const detail = await response.text();
        throw new Error(detail || `Request failed: ${{response.status}}`);
      }}
      return response.text();
    }}

    function escapeHtml(value) {{
      return String(value ?? "").replace(/[&<>"']/g, (char) => {{
        return {{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }}[char];
      }});
    }}

    const languageStorageKey = "datapulse.console.language.v1";
    const createWatchStorageKey = "datapulse.console.create-watch-draft.v2";
    const storyFilterStorageKey = "datapulse.console.story-filter.v1";
    const storySortStorageKey = "datapulse.console.story-sort.v1";
    const createWatchFormFields = ["name", "schedule", "query", "platform", "domain", "route", "keyword", "min_score", "min_confidence"];
    const routeFormFields = [
      "name",
      "channel",
      "description",
      "webhook_url",
      "authorization",
      "headers_json",
      "feishu_webhook",
      "telegram_bot_token",
      "telegram_chat_id",
      "timeout_seconds",
    ];

    function copy(enText, zhText) {{
      return state.language === "zh" ? zhText : enText;
    }}

    function phrase(enText, zhText, values = {{}}) {{
      const template = copy(enText, zhText);
      return String(template).replace(/\\{{(\\w+)\\}}/g, (_, key) => String(values[key] ?? ""));
    }}

    function localizeWord(value) {{
      const raw = String(value || "").trim();
      const key = raw.toLowerCase();
      const map = {{
        active: ["active", "活跃"],
        aligned: ["aligned", "一致"],
        all: ["all", "全部"],
        closed: ["closed", "关闭"],
        degraded: ["degraded", "降级"],
        disabled: ["disabled", "已停用"],
        done: ["done", "完成"],
        draft: ["draft", "草稿"],
        due: ["due", "待执行"],
        editable: ["editable", "可编辑"],
        duplicate: ["duplicate", "重复"],
        escalated: ["escalated", "已升级"],
        error: ["error", "错误"],
        events: ["events", "事件"],
        feishu: ["feishu", "飞书"],
        healthy: ["healthy", "健康"],
        idle: ["idle", "空闲"],
        ignored: ["ignored", "已忽略"],
        keep: ["keep", "保留"],
        manual: ["manual", "手动"],
        merge: ["merge", "合并"],
        missing: ["missing", "缺失"],
        mixed: ["mixed", "混合"],
        monitoring: ["monitoring", "监控中"],
        new: ["new", "新建"],
        ok: ["ok", "正常"],
        open: ["open", "开放"],
        pending: ["pending", "处理中"],
        ready: ["ready", "就绪"],
        resolved: ["resolved", "已解决"],
        running: ["running", "运行中"],
        same: ["same", "相同"],
        success: ["success", "成功"],
        synced: ["synced", "已同步"],
        telegram: ["telegram", "telegram"],
        triaged: ["triaged", "已分诊"],
        unknown: ["unknown", "未知"],
        verified: ["verified", "已核验"],
        waiting: ["waiting", "等待"],
        warn: ["warn", "警告"],
        webhook: ["webhook", "webhook"],
        markdown: ["markdown", "markdown"],
      }};
      const pair = map[key];
      return pair ? copy(pair[0], pair[1]) : raw;
    }}

    function localizeBoolean(value) {{
      return value ? copy("yes", "是") : copy("no", "否");
    }}
    const createWatchPresets = [
      {{
        id: "launch",
        label: "Launch Pulse",
        zhLabel: "发布脉冲",
        description: "Tight interval for product or company launches.",
        zhDescription: "适合产品或公司发布场景的高频任务。",
        values: {{
          name: "Launch Pulse",
          schedule: "interval:15m",
          query: "OpenAI launch",
          platform: "twitter",
          domain: "",
          route: "",
          keyword: "launch",
          min_score: "70",
          min_confidence: "0.75",
        }},
      }},
      {{
        id: "risk",
        label: "Risk Sweep",
        zhLabel: "风险巡检",
        description: "Higher confidence gate for operational risk review.",
        zhDescription: "适合运维风险巡检的高置信度门槛。",
        values: {{
          name: "Risk Sweep",
          schedule: "@hourly",
          query: "service outage rumor",
          platform: "web",
          domain: "",
          route: "",
          keyword: "outage",
          min_score: "80",
          min_confidence: "0.88",
        }},
      }},
      {{
        id: "market",
        label: "Market Shift",
        zhLabel: "市场异动",
        description: "Cross-signal watch for moves around listed names.",
        zhDescription: "适合上市主体异动监测的跨信号任务。",
        values: {{
          name: "Market Shift",
          schedule: "@hourly",
          query: "Xiaomi earnings",
          platform: "news",
          domain: "",
          route: "",
          keyword: "earnings",
          min_score: "68",
          min_confidence: "0.8",
        }},
      }},
      {{
        id: "creator",
        label: "Creator Surge",
        zhLabel: "创作者热度",
        description: "Faster scan for creator and social breakout chatter.",
        zhDescription: "适合创作者与社媒爆发信号的快速扫描。",
        values: {{
          name: "Creator Surge",
          schedule: "interval:30m",
          query: "viral creator trend",
          platform: "reddit",
          domain: "",
          route: "",
          keyword: "viral",
          min_score: "55",
          min_confidence: "0.65",
        }},
      }},
    ];
    const scheduleLaneOptions = [
      {{ label: "manual", value: "manual" }},
      {{ label: "15m", value: "interval:15m" }},
      {{ label: "30m", value: "interval:30m" }},
      {{ label: "hourly", value: "@hourly" }},
    ];
    const platformLaneOptions = [
      {{ label: "twitter", value: "twitter" }},
      {{ label: "reddit", value: "reddit" }},
      {{ label: "news", value: "news" }},
      {{ label: "web", value: "web" }},
    ];
    const routeChannelOptions = [
      {{ label: "Webhook", zhLabel: "Webhook", value: "webhook" }},
      {{ label: "Telegram", zhLabel: "Telegram", value: "telegram" }},
      {{ label: "Feishu", zhLabel: "飞书", value: "feishu" }},
      {{ label: "Markdown", zhLabel: "Markdown", value: "markdown" }},
    ];
    const storyStatusOptions = ["active", "monitoring", "resolved", "archived"];
    const storySortOptions = ["attention", "recent", "evidence", "conflict", "score"];
    const storyViewPresetOptions = ["desk", "fresh", "conflicts", "archive"];
    const scoreSuggestionOptions = ["40", "55", "68", "70", "80", "90"];
    const confidenceSuggestionOptions = ["0.6", "0.65", "0.75", "0.8", "0.88", "0.95"];

    function uniqueValues(values) {{
      return Array.from(new Set((Array.isArray(values) ? values : [values])
        .flatMap((value) => Array.isArray(value) ? value : [value])
        .map((value) => String(value ?? "").trim())
        .filter(Boolean)));
    }}

    function normalizeStorySort(value) {{
      const normalized = String(value || "").trim().toLowerCase() || "attention";
      return storySortOptions.includes(normalized) ? normalized : "attention";
    }}

    function normalizeStoryFilter(value) {{
      const normalized = String(value || "").trim().toLowerCase() || "all";
      if (normalized === "all" || normalized === "conflicted") {{
        return normalized;
      }}
      return storyStatusOptions.includes(normalized) ? normalized : "all";
    }}

    function storyViewPresetLabel(viewKey) {{
      const labels = {{
        desk: copy("Ops Desk", "运营台"),
        fresh: copy("Fresh Radar", "新近雷达"),
        conflicts: copy("Conflict Queue", "冲突队列"),
        archive: copy("Archive Review", "归档回看"),
        custom: copy("Custom", "自定义"),
      }};
      return labels[String(viewKey || "").trim().toLowerCase()] || labels.custom;
    }}

    function storyViewPresetDescription(viewKey) {{
      const descriptions = {{
        desk: copy(
          "Default operating lane for active story review.",
          "默认的日常运营视角，先看当前应处理的故事。"
        ),
        fresh: copy(
          "Pull the latest story updates to the top.",
          "把最新更新的故事优先提到最前。"
        ),
        conflicts: copy(
          "Narrow to contradiction-heavy stories first.",
          "直接聚焦冲突较多的故事。"
        ),
        archive: copy(
          "Review recently archived stories without reopening the whole queue.",
          "查看最近归档的故事，而不用重新打开整个队列。"
        ),
        custom: copy(
          "You are using a manual filter or sort combination.",
          "当前使用的是手动组合的筛选与排序。"
        ),
      }};
      return descriptions[String(viewKey || "").trim().toLowerCase()] || descriptions.custom;
    }}

    function getStoryViewPreset(viewKey) {{
      const normalized = String(viewKey || "").trim().toLowerCase();
      const presets = {{
        desk: {{ key: "desk", filter: "all", sort: "attention" }},
        fresh: {{ key: "fresh", filter: "all", sort: "recent" }},
        conflicts: {{ key: "conflicts", filter: "conflicted", sort: "conflict" }},
        archive: {{ key: "archive", filter: "archived", sort: "recent" }},
      }};
      return presets[normalized] || null;
    }}

    function detectStoryViewPreset({{ filter = "all", sort = "attention", search = "" }} = {{}}) {{
      if (String(search || "").trim()) {{
        return "custom";
      }}
      const normalizedFilter = normalizeStoryFilter(filter);
      const normalizedSort = normalizeStorySort(sort);
      const matchedPreset = storyViewPresetOptions.find((viewKey) => {{
        const preset = getStoryViewPreset(viewKey);
        return preset && preset.filter === normalizedFilter && preset.sort === normalizedSort;
      }});
      return matchedPreset || "custom";
    }}

    function storySortLabel(sortKey) {{
      const normalized = normalizeStorySort(sortKey);
      const labels = {{
        attention: copy("Attention Order", "优先级排序"),
        recent: copy("Most Recent", "最近更新"),
        evidence: copy("Most Evidence", "证据最多"),
        conflict: copy("Conflict Load", "冲突强度"),
        score: copy("Highest Score", "最高分数"),
      }};
      return labels[normalized] || labels.attention;
    }}

    function storySortSummary(sortKey) {{
      const normalized = normalizeStorySort(sortKey);
      const summaries = {{
        attention: copy(
          "Default lane: unresolved conflicts, fresh updates, and active stories float to the top first.",
          "默认把未解决冲突、最近更新且仍在活跃队列里的故事放在最前面。"
        ),
        recent: copy(
          "Use when recency matters more than story depth.",
          "当时效比故事深度更重要时，用这个排序。"
        ),
        evidence: copy(
          "Use when you want the densest evidence packs first.",
          "当你想先看证据最密集的故事时，用这个排序。"
        ),
        conflict: copy(
          "Use when contradiction triage is the current priority.",
          "当处理冲突信号是当前优先级时，用这个排序。"
        ),
        score: copy(
          "Use when ranked signal quality should lead the queue.",
          "当你想按综合分数先看高质量信号时，用这个排序。"
        ),
      }};
      return summaries[normalized] || summaries.attention;
    }}

    function parseDateValue(value) {{
      const stamp = Date.parse(String(value || "").trim());
      return Number.isFinite(stamp) ? stamp : 0;
    }}

    function formatCompactDateTime(value) {{
      const stamp = parseDateValue(value);
      if (!stamp) {{
        return "-";
      }}
      const formatter = new Intl.DateTimeFormat(state.language === "zh" ? "zh-CN" : "en-US", {{
        month: "short",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      }});
      return formatter.format(new Date(stamp));
    }}

    function getStoryUpdatedAt(story) {{
      return parseDateValue((story && (story.updated_at || story.generated_at)) || "");
    }}

    function getStoryContradictionCount(story) {{
      return Array.isArray(story?.contradictions) ? story.contradictions.length : 0;
    }}

    function getStoryAttentionScore(story) {{
      const status = String(story?.status || "active").trim().toLowerCase() || "active";
      const contradictionCount = getStoryContradictionCount(story);
      const itemCount = Math.max(0, Number(story?.item_count || 0));
      const sourceCount = Math.max(0, Number(story?.source_count || 0));
      const score = Number(story?.score || 0);
      const confidence = Number(story?.confidence || 0);
      const updatedAt = getStoryUpdatedAt(story);
      const ageHours = updatedAt ? Math.max(0, (Date.now() - updatedAt) / 3600000) : 999;
      const freshness = Math.max(0, 48 - Math.min(48, ageHours));
      const statusWeights = {{
        active: 40,
        monitoring: 26,
        resolved: 10,
        archived: -24,
      }};
      return (
        contradictionCount * 70 +
        itemCount * 8 +
        sourceCount * 4 +
        score * 0.4 +
        confidence * 18 +
        freshness +
        (statusWeights[status] ?? 16)
      );
    }}

    function compareNumberDesc(leftValue, rightValue) {{
      if (leftValue === rightValue) {{
        return 0;
      }}
      return leftValue < rightValue ? 1 : -1;
    }}

    function compareStoriesByWorkspaceOrder(left, right, sortKey) {{
      const normalized = normalizeStorySort(sortKey);
      const leftUpdated = getStoryUpdatedAt(left);
      const rightUpdated = getStoryUpdatedAt(right);
      const leftAttention = getStoryAttentionScore(left);
      const rightAttention = getStoryAttentionScore(right);
      const leftConflicts = getStoryContradictionCount(left);
      const rightConflicts = getStoryContradictionCount(right);
      const leftItems = Math.max(0, Number(left?.item_count || 0));
      const rightItems = Math.max(0, Number(right?.item_count || 0));
      const leftSources = Math.max(0, Number(left?.source_count || 0));
      const rightSources = Math.max(0, Number(right?.source_count || 0));
      const leftScore = Number(left?.score || 0);
      const rightScore = Number(right?.score || 0);
      const leftConfidence = Number(left?.confidence || 0);
      const rightConfidence = Number(right?.confidence || 0);
      const chain = normalized === "recent"
        ? [
            compareNumberDesc(leftUpdated, rightUpdated),
            compareNumberDesc(leftAttention, rightAttention),
            compareNumberDesc(leftItems, rightItems),
          ]
        : normalized === "evidence"
          ? [
              compareNumberDesc(leftItems, rightItems),
              compareNumberDesc(leftSources, rightSources),
              compareNumberDesc(leftAttention, rightAttention),
              compareNumberDesc(leftUpdated, rightUpdated),
            ]
          : normalized === "conflict"
            ? [
                compareNumberDesc(leftConflicts, rightConflicts),
                compareNumberDesc(leftAttention, rightAttention),
                compareNumberDesc(leftUpdated, rightUpdated),
              ]
            : normalized === "score"
              ? [
                  compareNumberDesc(leftScore, rightScore),
                  compareNumberDesc(leftConfidence, rightConfidence),
                  compareNumberDesc(leftAttention, rightAttention),
                  compareNumberDesc(leftUpdated, rightUpdated),
                ]
              : [
                  compareNumberDesc(leftAttention, rightAttention),
                  compareNumberDesc(leftConflicts, rightConflicts),
                  compareNumberDesc(leftUpdated, rightUpdated),
                  compareNumberDesc(leftItems, rightItems),
                ];
      for (const result of chain) {{
        if (result) {{
          return result;
        }}
      }}
      return String(left?.title || left?.id || "").localeCompare(String(right?.title || right?.id || ""));
    }}

    function describeStoryPriority(story) {{
      const contradictionCount = getStoryContradictionCount(story);
      const itemCount = Math.max(0, Number(story?.item_count || 0));
      const status = String(story?.status || "active").trim().toLowerCase() || "active";
      const updatedAt = getStoryUpdatedAt(story);
      const ageHours = updatedAt ? Math.max(0, (Date.now() - updatedAt) / 3600000) : 999;
      if (status === "archived") {{
        return {{ tone: "", label: copy("cold lane", "冷队列") }};
      }}
      if (contradictionCount > 0) {{
        return {{
          tone: "hot",
          label: phrase("conflict x{{count}}", "冲突 x{{count}}", {{ count: contradictionCount }}),
        }};
      }}
      if (ageHours <= 12) {{
        return {{ tone: "ok", label: copy("fresh update", "新近更新") }};
      }}
      if (itemCount >= 4) {{
        return {{ tone: "ok", label: copy("deep evidence", "证据较多") }};
      }}
      if (status === "monitoring") {{
        return {{ tone: "", label: copy("watching", "持续监控") }};
      }}
      if (status === "resolved") {{
        return {{ tone: "", label: copy("resolved lane", "已解决") }};
      }}
      return {{ tone: "ok", label: copy("active lane", "活跃队列") }};
    }}

    function renderDatalist(identifier, values) {{
      const root = $(identifier);
      if (!root) {{
        return;
      }}
      root.innerHTML = uniqueValues(values).slice(0, 32).map((value) => `<option value="${{escapeHtml(value)}}"></option>`).join("");
    }}

    function collectWatchValues(fieldName) {{
      return [
        ...state.watches.map((watch) => watch ? watch[fieldName] : ""),
        ...Object.values(state.watchDetails || {{}}).map((watch) => watch ? watch[fieldName] : ""),
      ];
    }}

    function collectWatchArrayValues(fieldName) {{
      return [
        ...state.watches.flatMap((watch) => Array.isArray(watch?.[fieldName]) ? watch[fieldName] : []),
        ...Object.values(state.watchDetails || {{}}).flatMap((watch) => Array.isArray(watch?.[fieldName]) ? watch[fieldName] : []),
      ];
    }}

    function collectAlertRuleValues(fieldName) {{
      return Object.values(state.watchDetails || {{}}).flatMap((watch) => {{
        return (Array.isArray(watch?.alert_rules) ? watch.alert_rules : []).flatMap((rule) => {{
          const raw = rule ? rule[fieldName] : "";
          return Array.isArray(raw) ? raw : [raw];
        }});
      }});
    }}

    function collectRouteNames() {{
      return state.routes.map((route) => route && (route.name || route.route_name || route.id || ""));
    }}

    function renderFormSuggestionLists() {{
      const suggestionPatch = state.createWatchSuggestions?.autofill_patch || {{}};
      renderDatalist("mission-name-options-list", [
        state.createWatchDraft?.name,
        ...createWatchPresets.map((preset) => preset.values.name),
        ...collectWatchValues("name"),
      ]);
      renderDatalist("query-options-list", [
        state.createWatchDraft?.query,
        ...createWatchPresets.map((preset) => preset.values.query),
        ...collectWatchValues("query"),
      ]);
      renderDatalist("schedule-options-list", [
        state.createWatchDraft?.schedule,
        suggestionPatch.schedule,
        state.createWatchSuggestions?.recommended_schedule,
        ...scheduleLaneOptions.map((option) => option.value),
        ...collectWatchValues("schedule"),
      ]);
      renderDatalist("platform-options-list", [
        state.createWatchDraft?.platform,
        suggestionPatch.platform,
        state.createWatchSuggestions?.recommended_platform,
        ...platformLaneOptions.map((option) => option.value),
        ...collectWatchArrayValues("platforms"),
      ]);
      renderDatalist("domain-options-list", [
        state.createWatchDraft?.domain,
        suggestionPatch.domain,
        state.createWatchSuggestions?.recommended_domain,
        ...collectWatchArrayValues("sites"),
        ...collectAlertRuleValues("domains"),
      ]);
      renderDatalist("route-options-list", [
        state.createWatchDraft?.route,
        suggestionPatch.route,
        state.createWatchSuggestions?.recommended_route,
        ...collectRouteNames(),
        ...collectAlertRuleValues("routes"),
      ]);
      renderDatalist("keyword-options-list", [
        state.createWatchDraft?.keyword,
        suggestionPatch.keyword,
        state.createWatchSuggestions?.recommended_keyword,
        ...createWatchPresets.map((preset) => preset.values.keyword),
        ...collectAlertRuleValues("keyword_any"),
      ]);
      renderDatalist("score-options-list", [
        state.createWatchDraft?.min_score,
        suggestionPatch.min_score,
        ...scoreSuggestionOptions,
        ...collectAlertRuleValues("min_score").filter((value) => Number(value || 0) > 0),
      ]);
      renderDatalist("confidence-options-list", [
        state.createWatchDraft?.min_confidence,
        suggestionPatch.min_confidence,
        ...confidenceSuggestionOptions,
        ...collectAlertRuleValues("min_confidence").filter((value) => Number(value || 0) > 0),
      ]);
    }}

    function defaultCreateWatchDraft() {{
      return {{
        name: "",
        schedule: "",
        query: "",
        platform: "",
        domain: "",
        route: "",
        keyword: "",
        min_score: "",
        min_confidence: "",
      }};
    }}

    function draftHasAdvancedSignal(payload = {{}}) {{
      const draft = normalizeCreateWatchDraft(payload || defaultCreateWatchDraft());
      return Boolean(
        draft.schedule.trim() ||
        draft.platform.trim() ||
        draft.domain.trim() ||
        draft.route.trim() ||
        draft.keyword.trim() ||
        draft.min_score.trim() ||
        draft.min_confidence.trim()
      );
    }}

    function normalizeCreateWatchDraft(payload = {{}}) {{
      const draft = defaultCreateWatchDraft();
      createWatchFormFields.forEach((field) => {{
        draft[field] = String(payload[field] ?? "");
      }});
      return draft;
    }}

    function isCreateWatchAdvancedOpen(draftInput) {{
      const draft = normalizeCreateWatchDraft(draftInput || defaultCreateWatchDraft());
      if (typeof state.createWatchAdvancedOpen === "boolean") {{
        return state.createWatchAdvancedOpen;
      }}
      return Boolean(String(state.createWatchEditingId || "").trim() || draftHasAdvancedSignal(draft));
    }}

    function summarizeCreateWatchAdvanced(draftInput) {{
      const draft = normalizeCreateWatchDraft(draftInput || defaultCreateWatchDraft());
      const chips = [];
      if (draft.schedule.trim()) {{
        chips.push(scheduleModeLabel(draft.schedule));
      }}
      if (draft.platform.trim()) {{
        chips.push(phrase("platform: {{value}}", "平台：{{value}}", {{ value: draft.platform.trim() }}));
      }}
      if (draft.domain.trim()) {{
        chips.push(phrase("domain: {{value}}", "域名：{{value}}", {{ value: draft.domain.trim() }}));
      }}
      if (draft.route.trim()) {{
        chips.push(phrase("route: {{value}}", "路由：{{value}}", {{ value: draft.route.trim() }}));
      }}
      if (draft.keyword.trim()) {{
        chips.push(phrase("keyword: {{value}}", "关键词：{{value}}", {{ value: draft.keyword.trim() }}));
      }}
      if (draft.min_score.trim()) {{
        chips.push(phrase("score >= {{value}}", "分数 >= {{value}}", {{ value: draft.min_score.trim() }}));
      }}
      if (draft.min_confidence.trim()) {{
        chips.push(phrase("confidence >= {{value}}", "置信度 >= {{value}}", {{ value: draft.min_confidence.trim() }}));
      }}
      if (!chips.length) {{
        chips.push(copy("No scope or alert gate yet", "当前还没有范围或告警门槛"));
      }}
      return chips.slice(0, 6);
    }}

    function defaultRouteDraft() {{
      return {{
        name: "",
        channel: "webhook",
        description: "",
        webhook_url: "",
        authorization: "",
        headers_json: "",
        feishu_webhook: "",
        telegram_bot_token: "",
        telegram_chat_id: "",
        timeout_seconds: "",
      }};
    }}

    function normalizeRouteDraft(payload = {{}}) {{
      const draft = defaultRouteDraft();
      routeFormFields.forEach((field) => {{
        if (field === "channel") {{
          return;
        }}
        draft[field] = String(payload[field] ?? draft[field] ?? "");
      }});
      const channel = String(payload.channel ?? draft.channel ?? "webhook").trim().toLowerCase();
      draft.channel = routeChannelOptions.some((option) => option.value === channel) ? channel : "webhook";
      return draft;
    }}

    function routeChannelLabel(channel) {{
      const normalized = String(channel || "").trim().toLowerCase();
      const option = routeChannelOptions.find((candidate) => candidate.value === normalized);
      if (!option) {{
        return normalized || copy("unknown", "未知");
      }}
      return copy(option.label, option.zhLabel || option.label);
    }}

    function routeDraftHasAdvancedSignal(payload = {{}}) {{
      const draft = normalizeRouteDraft(payload || defaultRouteDraft());
      return Boolean(
        draft.description.trim() ||
        draft.authorization.trim() ||
        draft.headers_json.trim() ||
        draft.timeout_seconds.trim()
      );
    }}

    function isRouteAdvancedOpen(draftInput) {{
      const draft = normalizeRouteDraft(draftInput || defaultRouteDraft());
      if (typeof state.routeAdvancedOpen === "boolean") {{
        return state.routeAdvancedOpen;
      }}
      return Boolean(String(state.routeEditingId || "").trim() || routeDraftHasAdvancedSignal(draft));
    }}

    function normalizeRouteName(value) {{
      return String(value || "").trim().toLowerCase();
    }}

    function normalizeRouteRuleNames(rule) {{
      if (!rule) {{
        return [];
      }}
      const raw = Array.isArray(rule.routes) ? rule.routes : [rule.route];
      return uniqueValues(raw).map((value) => normalizeRouteName(value)).filter(Boolean);
    }}

    function watchUsesRoute(watch, routeName) {{
      const normalized = normalizeRouteName(routeName);
      if (!normalized) {{
        return false;
      }}
      return (Array.isArray(watch?.alert_rules) ? watch.alert_rules : []).some((rule) => {{
        return normalizeRouteRuleNames(rule).includes(normalized);
      }});
    }}

    function getRouteUsageRows(routeName) {{
      const rows = [
        ...state.watches,
        ...Object.values(state.watchDetails || {{}}),
      ];
      const seen = new Set();
      return rows.filter((watch) => {{
        const identifier = String(watch?.id || "").trim();
        if (!identifier || seen.has(identifier)) {{
          return false;
        }}
        seen.add(identifier);
        return watchUsesRoute(watch, routeName);
      }});
    }}

    function getRouteUsageCount(routeName) {{
      return getRouteUsageRows(routeName).length;
    }}

    function getRouteUsageNames(routeName) {{
      return getRouteUsageRows(routeName).map((watch) => String(watch.name || watch.id || "").trim()).filter(Boolean);
    }}

    function getRouteHealthRow(routeName) {{
      const normalized = normalizeRouteName(routeName);
      if (!normalized) {{
        return null;
      }}
      return state.routeHealth.find((route) => normalizeRouteName(route?.name) === normalized) || null;
    }}

    function summarizeUrlHost(rawUrl) {{
      const value = String(rawUrl || "").trim();
      if (!value) {{
        return "";
      }}
      try {{
        const parsed = new URL(value);
        const path = parsed.pathname && parsed.pathname !== "/" ? parsed.pathname.slice(0, 18) : "";
        return `${{parsed.host}}${{path}}`;
      }} catch {{
        return value;
      }}
    }}

    function summarizeRouteDestination(route) {{
      const channel = normalizeRouteName(route?.channel);
      if (channel === "webhook") {{
        return route?.webhook_url
          ? summarizeUrlHost(route.webhook_url)
          : copy("Webhook URL missing", "Webhook URL 未配置");
      }}
      if (channel === "feishu") {{
        return route?.feishu_webhook
          ? summarizeUrlHost(route.feishu_webhook)
          : copy("Feishu webhook missing", "飞书 webhook 未配置");
      }}
      if (channel === "telegram") {{
        return route?.telegram_chat_id
          ? phrase("chat {{value}}", "会话 {{value}}", {{ value: route.telegram_chat_id }})
          : copy("Telegram chat missing", "Telegram 会话未配置");
      }}
      if (channel === "markdown") {{
        return copy("Append to alert markdown log", "追加到告警 Markdown 日志");
      }}
      return copy("Route target not configured", "路由目标未配置");
    }}

    function createRouteDraftFromRoute(route) {{
      const rawHeaders = route && typeof route.headers === "object" && !Array.isArray(route.headers)
        ? {{ ...route.headers }}
        : {{}};
      let authorization = "";
      if (typeof route?.authorization === "string" && route.authorization !== "***") {{
        authorization = route.authorization;
      }}
      if (!authorization && typeof rawHeaders.Authorization === "string" && rawHeaders.Authorization !== "***") {{
        authorization = rawHeaders.Authorization;
      }}
      delete rawHeaders.Authorization;
      return normalizeRouteDraft({{
        name: String(route?.name || ""),
        channel: String(route?.channel || "webhook"),
        description: String(route?.description || ""),
        webhook_url: String(route?.webhook_url || ""),
        authorization,
        headers_json: Object.keys(rawHeaders).length ? JSON.stringify(rawHeaders, null, 2) : "",
        feishu_webhook: String(route?.feishu_webhook || ""),
        telegram_bot_token: "",
        telegram_chat_id: String(route?.telegram_chat_id || ""),
        timeout_seconds: route?.timeout_seconds != null ? String(route.timeout_seconds) : "",
      }});
    }}

    function collectRouteDraft(form) {{
      if (!form) {{
        return normalizeRouteDraft(state.routeDraft || defaultRouteDraft());
      }}
      const next = defaultRouteDraft();
      routeFormFields.forEach((fieldName) => {{
        const field = form.elements.namedItem(fieldName);
        next[fieldName] = field ? String(field.value ?? "") : "";
      }});
      return normalizeRouteDraft(next);
    }}

    function setRouteDraft(nextDraft, editingId = state.routeEditingId) {{
      state.routeDraft = normalizeRouteDraft(nextDraft || defaultRouteDraft());
      state.routeEditingId = String(editingId || "").trim();
      renderRouteDeck();
    }}

    function focusRouteDeck(fieldName = "name") {{
      $("route-manager-shell")?.scrollIntoView({{ block: "start", behavior: "smooth" }});
      window.setTimeout(() => {{
        const form = $("route-form");
        const field = form?.elements?.namedItem(fieldName);
        if (field && typeof field.focus === "function") {{
          field.focus();
        }}
      }}, 140);
    }}

    async function editRouteInDeck(identifier) {{
      const normalized = normalizeRouteName(identifier);
      if (!normalized) {{
        return;
      }}
      const route = state.routes.find((item) => normalizeRouteName(item?.name) === normalized);
      if (!route) {{
        throw new Error(copy("Alert route not found in current board state.", "当前看板中没有找到该告警路由。"));
      }}
      state.routeAdvancedOpen = true;
      setRouteDraft(createRouteDraftFromRoute(route), normalized);
      focusRouteDeck(route.channel === "markdown" ? "description" : "name");
    }}

    async function applyRouteToMissionDraft(identifier) {{
      const normalized = normalizeRouteName(identifier);
      if (!normalized) {{
        return;
      }}
      state.createWatchAdvancedOpen = true;
      updateCreateWatchDraft({{ route: normalized }});
      focusCreateWatchDeck("route");
      showToast(
        state.language === "zh"
          ? `已把路由载入任务草稿：${{normalized}}`
          : `Route loaded into mission deck: ${{normalized}}`,
        "success",
      );
    }}

    function parseRouteHeaders(rawValue) {{
      const text = String(rawValue || "").trim();
      if (!text) {{
        return null;
      }}
      let parsed;
      try {{
        parsed = JSON.parse(text);
      }} catch (error) {{
        throw new Error(copy("Custom headers must be valid JSON.", "自定义请求头必须是合法 JSON。"));
      }}
      if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {{
        throw new Error(copy("Custom headers must be a JSON object.", "自定义请求头必须是 JSON 对象。"));
      }}
      return Object.fromEntries(
        Object.entries(parsed)
          .map(([key, value]) => [String(key || "").trim(), String(value ?? "").trim()])
          .filter(([key]) => Boolean(key)),
      );
    }}

    function defaultStoryDraft() {{
      return {{
        title: "",
        summary: "",
        status: "active",
      }};
    }}

    function normalizeStoryDraft(payload = {{}}) {{
      return {{
        title: String(payload.title ?? "").trimStart(),
        summary: String(payload.summary ?? ""),
        status: storyStatusOptions.includes(String(payload.status || "").trim().toLowerCase())
          ? String(payload.status || "").trim().toLowerCase()
          : "active",
      }};
    }}

    function collectStoryDraft(form) {{
      if (!form) {{
        return normalizeStoryDraft(state.storyDraft || defaultStoryDraft());
      }}
      return normalizeStoryDraft({{
        title: String(form.elements.namedItem("title")?.value || ""),
        summary: String(form.elements.namedItem("summary")?.value || ""),
        status: String(form.elements.namedItem("status")?.value || "active"),
      }});
    }}

    function setStoryDraft(nextDraft) {{
      state.storyDraft = normalizeStoryDraft(nextDraft || defaultStoryDraft());
      renderStoryCreateDeck();
    }}

    function focusStoryDeck(fieldName = "title") {{
      $("story-intake-shell")?.scrollIntoView({{ block: "start", behavior: "smooth" }});
      window.setTimeout(() => {{
        const form = $("story-create-form");
        const field = form?.elements?.namedItem(fieldName);
        if (field && typeof field.focus === "function") {{
          field.focus();
        }}
      }}, 140);
    }}

    function getStoryRecord(identifier) {{
      const normalized = String(identifier || "").trim();
      if (!normalized) {{
        return null;
      }}
      return state.storyDetails[normalized] || state.stories.find((story) => story.id === normalized) || null;
    }}

    function removeStoryFromState(identifier) {{
      const normalized = String(identifier || "").trim();
      if (!normalized) {{
        return;
      }}
      state.stories = state.stories.filter((story) => story.id !== normalized);
      delete state.storyDetails[normalized];
      delete state.storyGraph[normalized];
      delete state.storyMarkdown[normalized];
      if (state.selectedStoryId === normalized) {{
        state.selectedStoryId = state.stories[0] ? state.stories[0].id : "";
      }}
    }}

    async function submitStoryDeck(form) {{
      const draft = collectStoryDraft(form);
      state.storyDraft = draft;
      if (!draft.title.trim()) {{
        showToast(copy("Provide a story title before creating a brief.", "创建故事前请先填写标题。"), "error");
        focusStoryDeck("title");
        return;
      }}
      const submitButton = form?.querySelector("button[type='submit']");
      if (submitButton) {{
        submitButton.disabled = true;
      }}
      try {{
        const created = await api("/api/stories", {{
          method: "POST",
          headers: jsonHeaders,
          body: JSON.stringify(draft),
        }});
        setStoryDraft(defaultStoryDraft());
        pushActionEntry({{
          kind: copy("story create", "故事创建"),
          label: state.language === "zh" ? `已创建故事：${{created.title}}` : `Created story: ${{created.title}}`,
          detail: copy("The story is now part of the workspace and can be archived or refined in place.", "该故事已进入工作台，后续可以继续编辑或归档。"),
          undoLabel: copy("Delete story", "删除故事"),
          undo: async () => {{
            await api(`/api/stories/${{created.id}}`, {{ method: "DELETE" }});
            await refreshBoard();
            showToast(
              state.language === "zh" ? `已删除故事：${{created.title}}` : `Story deleted: ${{created.title}}`,
              "success",
            );
          }},
        }});
        await refreshBoard();
        state.selectedStoryId = created.id;
        state.storyDetails[created.id] = created;
        renderStories();
        showToast(
          state.language === "zh" ? `故事已创建：${{created.title}}` : `Story created: ${{created.title}}`,
          "success",
        );
      }} catch (error) {{
        reportError(error, copy("Create story", "创建故事"));
      }} finally {{
        if (submitButton) {{
          submitButton.disabled = false;
        }}
      }}
    }}

    async function setStoryStatusQuick(identifier, nextStatus) {{
      const story = getStoryRecord(identifier);
      if (!story) {{
        throw new Error(copy("Story not found in the current workspace.", "当前工作区中没有找到该故事。"));
      }}
      const targetStatus = String(nextStatus || "").trim().toLowerCase();
      if (!targetStatus || targetStatus === String(story.status || "active").trim().toLowerCase()) {{
        return;
      }}
      const previousStory = {{
        title: story.title || "",
        summary: story.summary || "",
        status: story.status || "active",
      }};
      try {{
        await api(`/api/stories/${{story.id}}`, {{
          method: "PUT",
          headers: jsonHeaders,
          body: JSON.stringify({{ status: targetStatus }}),
        }});
        pushActionEntry({{
          kind: copy("story state", "故事状态"),
          label: state.language === "zh"
            ? `已将故事切换为 ${{localizeWord(targetStatus)}}：${{story.title}}`
            : `Story moved to ${{targetStatus}}: ${{story.title}}`,
          detail: copy("Use undo to restore the previous workspace state.", "如需回退，可在最近操作里恢复。"),
          undoLabel: copy("Restore story", "恢复故事"),
          undo: async () => {{
            await api(`/api/stories/${{story.id}}`, {{
              method: "PUT",
              headers: jsonHeaders,
              body: JSON.stringify(previousStory),
            }});
            await refreshBoard();
            showToast(
              state.language === "zh" ? `已恢复故事：${{previousStory.title}}` : `Story restored: ${{previousStory.title}}`,
              "success",
            );
          }},
        }});
        await refreshBoard();
        showToast(
          state.language === "zh"
            ? `故事状态已更新：${{story.title}}`
            : `Story status updated: ${{story.title}}`,
          "success",
        );
      }} catch (error) {{
        reportError(error, copy("Update story state", "更新故事状态"));
      }}
    }}

    async function deleteStoryFromWorkspace(identifier) {{
      const story = getStoryRecord(identifier);
      if (!story) {{
        throw new Error(copy("Story not found in the current workspace.", "当前工作区中没有找到该故事。"));
      }}
      const confirmed = window.confirm(
        state.language === "zh"
          ? `确认删除故事 ${{story.title}}？这会把它从当前工作台移除。`
          : `Delete story ${{story.title}} from the workspace?`,
      );
      if (!confirmed) {{
        return;
      }}
      const snapshot = JSON.parse(JSON.stringify(story));
      try {{
        await api(`/api/stories/${{story.id}}`, {{ method: "DELETE" }});
        removeStoryFromState(story.id);
        pushActionEntry({{
          kind: copy("story delete", "故事删除"),
          label: state.language === "zh" ? `已删除故事：${{story.title}}` : `Deleted story: ${{story.title}}`,
          detail: copy("The full story payload is kept in recent actions so you can restore it once.", "完整故事快照会暂存在最近操作中，方便你单次恢复。"),
          undoLabel: copy("Restore story", "恢复故事"),
          undo: async () => {{
            await api("/api/stories", {{
              method: "POST",
              headers: jsonHeaders,
              body: JSON.stringify(snapshot),
            }});
            await refreshBoard();
            showToast(
              state.language === "zh" ? `已恢复故事：${{snapshot.title}}` : `Story restored: ${{snapshot.title}}`,
              "success",
            );
          }},
        }});
        await refreshBoard();
        showToast(
          state.language === "zh" ? `故事已删除：${{story.title}}` : `Story deleted: ${{story.title}}`,
          "success",
        );
      }} catch (error) {{
        reportError(error, copy("Delete story", "删除故事"));
      }}
    }}

    function isStorySelected(storyId) {{
      return state.selectedStoryIds.includes(storyId);
    }}

    function toggleStorySelection(storyId, checked = null) {{
      if (!storyId) {{
        return;
      }}
      const next = new Set(state.selectedStoryIds);
      const shouldSelect = checked === null ? !next.has(storyId) : Boolean(checked);
      if (shouldSelect) {{
        next.add(storyId);
        state.selectedStoryId = storyId;
      }} else {{
        next.delete(storyId);
      }}
      state.selectedStoryIds = Array.from(next);
    }}

    function selectVisibleStories(filteredStories) {{
      const visibleIds = (Array.isArray(filteredStories) ? filteredStories : []).map((story) => story.id);
      state.selectedStoryIds = visibleIds;
      if (visibleIds.length && !visibleIds.includes(state.selectedStoryId)) {{
        state.selectedStoryId = visibleIds[0];
      }}
    }}

    function clearStorySelection() {{
      state.selectedStoryIds = [];
    }}

    async function runStoryBatchStatusUpdate(storyIds, nextStatus) {{
      const normalizedIds = uniqueValues(storyIds).filter((storyId) => state.stories.some((story) => story.id === storyId));
      if (!normalizedIds.length || !nextStatus || state.storyBulkBusy) {{
        return;
      }}
      state.storyBulkBusy = true;
      const previousStates = {{}};
      normalizedIds.forEach((storyId) => {{
        const currentStory = getStoryRecord(storyId);
        previousStates[storyId] = currentStory ? String(currentStory.status || "active") : "active";
        if (currentStory && state.storyDetails[storyId]) {{
          state.storyDetails[storyId] = {{
            ...state.storyDetails[storyId],
            status: nextStatus,
          }};
        }}
      }});
      renderStories();
      try {{
        for (const storyId of normalizedIds) {{
          await api(`/api/stories/${{storyId}}`, {{
            method: "PUT",
            headers: jsonHeaders,
            body: JSON.stringify({{ status: nextStatus }}),
          }});
        }}
        state.selectedStoryIds = [];
        pushActionEntry({{
          kind: copy("story batch", "故事批处理"),
          label: state.language === "zh"
            ? `已批量将 ${{normalizedIds.length}} 条故事切换为 ${{localizeWord(nextStatus)}}`
            : `Moved ${{normalizedIds.length}} stories to ${{nextStatus}}`,
          detail: state.language === "zh"
            ? `涉及故事：${{normalizedIds.join(", ")}}`
            : `Stories: ${{normalizedIds.join(", ")}}`,
          undoLabel: copy("Restore stories", "恢复故事"),
          undo: async () => {{
            for (const storyId of normalizedIds) {{
              await api(`/api/stories/${{storyId}}`, {{
                method: "PUT",
                headers: jsonHeaders,
                body: JSON.stringify({{ status: previousStates[storyId] || "active" }}),
              }});
            }}
            await refreshBoard();
            showToast(
              state.language === "zh"
                ? `已恢复 ${{normalizedIds.length}} 条故事`
                : `Restored ${{normalizedIds.length}} stories`,
              "success",
            );
          }},
        }});
        await refreshBoard();
        showToast(
          state.language === "zh"
            ? `已批量更新 ${{normalizedIds.length}} 条故事`
            : `Updated ${{normalizedIds.length}} stories`,
          "success",
        );
      }} catch (error) {{
        normalizedIds.forEach((storyId) => {{
          if (state.storyDetails[storyId]) {{
            state.storyDetails[storyId] = {{
              ...state.storyDetails[storyId],
              status: previousStates[storyId] || "active",
            }};
          }}
        }});
        renderStories();
        throw error;
      }} finally {{
        state.storyBulkBusy = false;
        renderStories();
      }}
    }}

    function safeLocalStorageGet(key) {{
      try {{
        return window.localStorage.getItem(key);
      }} catch (error) {{
        return null;
      }}
    }}

    function safeLocalStorageSet(key, value) {{
      try {{
        window.localStorage.setItem(key, value);
      }} catch (error) {{
        console.warn("localStorage write skipped", error);
      }}
    }}

    function safeLocalStorageRemove(key) {{
      try {{
        window.localStorage.removeItem(key);
      }} catch (error) {{
        console.warn("localStorage remove skipped", error);
      }}
    }}

    function loadCreateWatchDraft() {{
      const raw = safeLocalStorageGet(createWatchStorageKey);
      if (!raw) {{
        return defaultCreateWatchDraft();
      }}
      try {{
        return normalizeCreateWatchDraft(JSON.parse(raw));
      }} catch (error) {{
        safeLocalStorageRemove(createWatchStorageKey);
        return defaultCreateWatchDraft();
      }}
    }}

    function persistCreateWatchDraft() {{
      const draft = normalizeCreateWatchDraft(state.createWatchDraft || defaultCreateWatchDraft());
      const hasSignal = createWatchFormFields.some((field) => String(draft[field] || "").trim());
      if (!hasSignal) {{
        safeLocalStorageRemove(createWatchStorageKey);
        return;
      }}
      safeLocalStorageSet(createWatchStorageKey, JSON.stringify(draft));
    }}

    function persistStoryWorkspacePrefs() {{
      safeLocalStorageSet(storyFilterStorageKey, normalizeStoryFilter(state.storyFilter));
      safeLocalStorageSet(storySortStorageKey, normalizeStorySort(state.storySort));
    }}

    function applyStoryViewPreset(viewKey) {{
      const preset = getStoryViewPreset(viewKey);
      if (!preset) {{
        return;
      }}
      state.storySearch = "";
      state.storyFilter = preset.filter;
      state.storySort = preset.sort;
      persistStoryWorkspacePrefs();
      renderStories();
    }}

    state.storyFilter = normalizeStoryFilter(safeLocalStorageGet(storyFilterStorageKey) || state.storyFilter);
    state.storySort = normalizeStorySort(safeLocalStorageGet(storySortStorageKey) || state.storySort);

    function detectInitialLanguage() {{
      const stored = String(safeLocalStorageGet(languageStorageKey) || "").trim().toLowerCase();
      if (stored === "zh" || stored === "en") {{
        return stored;
      }}
      const browserLanguage = String(window.navigator.language || "").trim().toLowerCase();
      return browserLanguage.startsWith("zh") ? "zh" : "en";
    }}

    function setText(id, value) {{
      const node = $(id);
      if (node) {{
        node.textContent = value;
      }}
    }}

    function setHTML(id, value) {{
      const node = $(id);
      if (node) {{
        node.innerHTML = value;
      }}
    }}

    function setPlaceholder(id, value) {{
      const node = $(id);
      if (node) {{
        node.placeholder = value;
      }}
    }}

    function applyLanguageChrome() {{
      document.documentElement.lang = state.language === "zh" ? "zh-CN" : "en";
      document.body.dataset.lang = state.language;
      document.title = state.language === "zh" ? "DataPulse 情报控制台" : initial.title;
      setText("topbar-title", copy("DataPulse Operations Console", "DataPulse 情报控制台"));
      setText("topbar-subtitle", copy("Mission -> Triage -> Story -> Delivery", "任务 -> 分诊 -> 故事 -> 交付"));
      setText("nav-intake", copy("New Mission", "新建任务"));
      setText("nav-board", copy("Mission Board", "任务列表"));
      setText("nav-cockpit", copy("Cockpit", "任务详情"));
      setText("nav-triage", copy("Triage", "分诊"));
      setText("nav-story", copy("Stories", "故事"));
      setText("nav-ops", copy("Ops", "运行状态"));
      setText("palette-open", copy("Command Palette", "快速命令"));
      setText("hero-eyebrow", copy("Guided Analyst Workflow", "引导式工作流"));
      setHTML("hero-title", state.language === "zh" ? "运行任务<br>审阅信号<br>沉淀故事" : "Run Missions, Review Signal, Publish Stories");
      setText("hero-copy", copy(
        "This console follows the real operating path: draft a watch, run it, triage the evidence, then promote verified signal into stories and delivery.",
        "页面按真实工作节奏组织：先创建监测任务，再执行、分诊，最后把验证后的信号沉淀成故事并进入交付。"
      ));
      setText("refresh-all", copy("Refresh Console", "刷新控制台"));
      setText("run-due", copy("Run Due Missions", "运行待执行任务"));
      setText("jump-watch-board", copy("Open Mission Board", "查看任务列表"));
      setText("guide-step-1-title", copy("Start With A Draft", "先创建任务"));
      setText("guide-step-1-copy", copy("Use a preset, clone an existing watch, or enter just Name + Query to get moving.", "可以使用预设、复制已有任务，或者只填名称和查询词直接开始。"));
      setText("guide-step-2-title", copy("Add Scope Only If Needed", "按需收窄范围"));
      setText("guide-step-2-copy", copy("Schedule, platform, and domain narrow the watch. Leave them open if you need broad discovery first.", "频率、平台和站点用于收窄监测范围；如果先做广泛发现，可以先留空。"));
      setText("guide-step-3-title", copy("Arm Alerts Last", "最后添加告警"));
      setText("guide-step-3-copy", copy("Route, keyword, score, and confidence are optional. Add them only when you want automated delivery.", "路由、关键词、分数和置信度都属于可选项，只在需要自动通知时再添加。"));
      setText("guide-kicker", copy("Operator Guidance", "操作提示"));
      setText("guide-panel-title", copy("Mission Intake", "任务创建"));
      setText("guide-chip", copy("Start here", "从这里开始"));
      setText("guide-panel-copy", copy("Required fields come first. Alert gating is optional, and the mission preview updates as you type.", "先填必填字段；告警条件是可选项，任务预览会随输入实时更新。"));
      setText("shortcut-focus", copy("/ focus draft", "/ 聚焦任务草稿"));
      setText("shortcut-preset", copy("1-4 load preset", "1-4 套用预设"));
      setText("shortcut-submit", copy("Cmd/Ctrl+Enter deploy", "Cmd/Ctrl+Enter 提交"));
      setText("jump-cockpit", copy("Cockpit", "任务详情"));
      setText("jump-triage", copy("Triage", "分诊"));
      setText("jump-story", copy("Stories", "故事"));
      setText("jump-ops", copy("Ops", "运行状态"));
      setText("deploy-title", copy("Deploy Mission", "创建监测任务"));
      setText("deploy-copy", copy("Create one watch, add optional scope, then decide whether alert routing is needed.", "先定义监测任务，再按需补充范围和通知条件。"));
      setText("preset-title", copy("Mission Modes", "任务预设"));
      setText("preset-copy", copy("Start from an archetype when the workflow is familiar, then only adjust the fields that matter.", "如果任务模式比较固定，可以直接套用预设，再修改关键字段。"));
      setText("deck-step-1-title", copy("Required Mission Input", "基础信息"));
      setText("deck-step-1-copy", copy("Name and query define the watch. Everything else can be layered on later.", "名称和查询词决定这个任务监测什么，其余设置都可以后补。"));
      setText("label-name", copy("Name", "名称"));
      setText("label-query", copy("Query", "查询词"));
      setText("hint-name", copy("Use a short operator-facing label.", "建议填写一个便于识别的简短名称。"));
      setText("hint-query", copy("Describe the signal you want tracked.", "描述你希望持续跟踪的主题、事件或对象。"));
      setText("deck-step-2-title", copy("Scope And Cadence", "范围与频率"));
      setText("deck-step-2-copy", copy("Use schedule and platform to narrow the mission only when you already know the operating lane.", "只有当你已经知道主要监测通道时，再补充频率、平台或站点。"));
      setText("label-schedule", copy("Schedule", "调度频率"));
      setText("label-platform", copy("Platform", "平台"));
      setText("label-domain", copy("Alert Domain", "站点/域名"));
      setText("hint-schedule", copy("Manual is fine for first exploration.", "初次探索时，用手动执行就够了。"));
      setText("hint-platform", copy("Leave empty for broader discovery.", "如果还不确定监测来源，可以先留空。"));
      setText("hint-domain", copy("Optional domain guard for tighter recall.", "可选的站点约束，用来提升结果收敛度。"));
      setText("schedule-lanes-title", copy("Schedule Lanes", "常用频率"));
      setText("platform-lanes-title", copy("Platform Lanes", "常用平台"));
      setText("deck-step-3-title", copy("Optional Alert Gate", "通知条件（可选）"));
      setText("deck-step-3-copy", copy("Attach delivery only when the mission is ready to trigger downstream action.", "只有当这个任务需要自动通知外部时，再补充告警条件。"));
      setText("label-route", copy("Alert Route", "告警路由"));
      setText("label-keyword", copy("Alert Keyword", "告警关键词"));
      setText("label-score", copy("Min Score", "最低分数"));
      setText("label-confidence", copy("Min Confidence", "最低置信度"));
      setText("hint-route", copy("Choose a named route when the watch should notify someone.", "如果需要自动通知，就选择一个命名路由。"));
      setText("hint-keyword", copy("Use a high-signal term to reduce noise.", "用高信号关键词减少无关结果。"));
      setText("hint-score", copy("Use when you only want stronger ranked hits.", "只想保留高分结果时再设置。"));
      setText("hint-confidence", copy("Use when analyst quality matters more than coverage.", "当质量比覆盖更重要时再设置。"));
      setText("route-snap-title", copy("Route Snap", "常用路由"));
      setText("create-watch-submit", copy("Create Watch", "创建任务"));
      setText("create-watch-clear", copy("Reset Draft", "清空草稿"));
      setText("clone-title", copy("Clone Existing Mission", "从已有任务复制"));
      setText("clone-copy", copy("Fork an existing watch when the current mission is only a variation in route, threshold, or query wording.", "如果当前任务只是查询词、阈值或路由的小改动，直接复制已有任务会更快。"));
      setText("actions-title", copy("Recent Actions", "最近变更"));
      setText("actions-copy", copy("Every reversible mutation stays here briefly so you can undo false starts without losing flow.", "最近的可撤销操作会暂时保留在这里，方便你快速回退。"));
      setText("board-title", copy("Mission Board", "任务看板"));
      setText("board-copy", copy("Run, inspect, pause, or remove watch missions from one board.", "在一个列表中完成运行、查看、停用和删除任务。"));
      setText("alert-stream-title", copy("Alert Stream", "告警动态"));
      setText("alert-stream-copy", copy("Read recent alert events without mixing them up with editable route configuration.", "这里专门查看最近告警事件，不再和可编辑路由配置混在一起。"));
      setText("alert-stream-mode", copy("Events read-only", "事件只读"));
      setText("route-manager-title", copy("Route Manager", "路由管理"));
      setText("route-manager-copy", copy("Create named delivery sinks once, then reuse them across missions without retyping webhook or chat details.", "把命名交付路由配置一次，后续在任务里直接复用，不必重复填写 webhook 或会话信息。"));
      setText("route-manager-mode", copy("Editable", "可编辑"));
      setText("ops-title", copy("Ops Snapshot", "运行状态"));
      setText("ops-copy", copy("Watch daemon health, collector risk, route delivery, and recent failures in one slice.", "把守护进程健康、采集器风险、路由投递和近期失败集中到一个视图。"));
      setText("cockpit-title", copy("Mission Cockpit", "任务详情"));
      setText("cockpit-copy", copy("Open one mission to inspect runs, filters, retry guidance, and alert rules.", "打开单个任务后，可查看执行记录、筛选条件、重试建议和告警规则。"));
      setText("distribution-title", copy("Distribution Health", "分发健康"));
      setText("distribution-copy", copy("See whether named delivery routes are healthy before they become silent failures.", "提前发现命名路由是否异常，避免进入静默失败。"));
      setText("distribution-mode", copy("Read-only", "只读"));
      setText("triage-title", copy("Triage Queue", "分诊队列"));
      setText("triage-copy", copy("Review open items, mark duplicates, and capture analyst reasoning without leaving the queue.", "在不离开队列的前提下完成审阅、去重和备注记录。"));
      setText("story-title", copy("Story Workspace", "故事工作台"));
      setText("story-copy", copy("Inspect clustered stories, evidence stacks, contradictions, and exportable summaries.", "查看聚类后的故事、证据堆栈、冲突点，以及可导出的摘要。"));
      setText("story-intake-title", copy("Story Intake", "故事录入"));
      setText("story-intake-copy", copy("Capture a manual brief when a story should exist before clustering catches up, then refine it inside the workspace.", "当某个故事需要先落下来、而聚类还没跟上时，可以先手工补录，再在工作台里继续完善。"));
      setText("story-intake-mode", copy("Editable", "可编辑"));
      setText("footer-note", copy("The browser is the operating surface. CLI and MCP remain first-class control planes.", "浏览器是主要操作界面；CLI 和 MCP 仍保持一等能力。"));
      setPlaceholder("command-palette-input", copy("Search actions, missions, stories, or routes", "搜索操作、任务、故事或路由"));
      setPlaceholder("input-name", copy("Launch Ops", "新品发布监测"));
      setPlaceholder("input-query", copy("OpenAI launch", "OpenAI 发布"));
      setPlaceholder("input-schedule", copy("@hourly / interval:15m", "@hourly / interval:15m"));
      setPlaceholder("input-platform", copy("twitter", "twitter"));
      setPlaceholder("input-domain", copy("openai.com", "openai.com"));
      setPlaceholder("input-route", copy("ops-webhook", "ops-webhook"));
      setPlaceholder("input-keyword", copy("launch", "发布"));
      setPlaceholder("input-score", copy("70", "70"));
      setPlaceholder("input-confidence", copy("0.8", "0.8"));
      document.querySelectorAll("[data-lang]").forEach((button) => {{
        button.classList.toggle("active", String(button.dataset.lang || "") === state.language);
      }});
    }}

    state.language = detectInitialLanguage();

    function showToast(message, tone = "info") {{
      const rack = $("toast-rack");
      if (!rack) {{
        return;
      }}
      const toast = document.createElement("div");
      toast.className = `toast ${{tone}}`;
      toast.innerHTML = `
        <div class="mono">${{copy("mission signal", "任务信号")}} / ${{localizeWord(tone)}}</div>
        <div style="margin-top:6px;">${{escapeHtml(message)}}</div>
      `;
      rack.appendChild(toast);
      window.setTimeout(() => {{
        toast.style.opacity = "0";
        toast.style.transform = "translateY(8px)";
        toast.style.transition = "opacity .18s ease, transform .18s ease";
        window.setTimeout(() => toast.remove(), 220);
      }}, 2800);
    }}

    window.alert = (message) => showToast(String(message || ""), "error");

    function reportError(error, prefix = "") {{
      console.error(error);
      const message = error && error.message ? error.message : String(error || "Unknown error");
      showToast(prefix ? `${{prefix}}: ${{message}}` : message, "error");
    }}

    function focusCreateWatchDeck(fieldName = "query") {{
      const form = $("create-watch-form");
      if (!form) {{
        return;
      }}
      form.scrollIntoView({{ block: "nearest", behavior: "smooth" }});
      const field = form.elements.namedItem(fieldName);
      if (field && typeof field.focus === "function") {{
        field.focus();
        if (typeof field.select === "function") {{
          field.select();
        }}
      }}
    }}

    function scheduleModeLabel(value) {{
      const schedule = String(value || "").trim();
      if (!schedule || schedule === "manual") {{
        return copy("manual dispatch", "手动执行");
      }}
      if (schedule.startsWith("interval:")) {{
        return state.language === "zh"
          ? `频率 ${{schedule.replace("interval:", "")}}`
          : `cadence ${{schedule.replace("interval:", "")}}`;
      }}
      if (schedule.startsWith("@")) {{
        return state.language === "zh" ? `Cron 别名 ${{schedule}}` : `cron alias ${{schedule}}`;
      }}
      return schedule;
    }}

    function buildCreateWatchPreview(draftInput) {{
      const draft = normalizeCreateWatchDraft(draftInput || defaultCreateWatchDraft());
      const requiredReady = Boolean(draft.name.trim() && draft.query.trim());
      const alertArmed = Boolean(
        draft.route.trim() ||
        draft.keyword.trim() ||
        draft.domain.trim() ||
        Number(draft.min_score || 0) > 0 ||
        Number(draft.min_confidence || 0) > 0,
      );
      const readiness = Math.min(
        100,
        (draft.name.trim() ? 34 : 0) +
        (draft.query.trim() ? 34 : 0) +
        (draft.schedule.trim() ? 8 : 0) +
        (draft.platform.trim() ? 8 : 0) +
        ((draft.route.trim() || draft.keyword.trim() || draft.domain.trim()) ? 8 : 0) +
        ((draft.min_score.trim() || draft.min_confidence.trim()) ? 8 : 0),
      );
      const filters = [draft.platform.trim(), draft.domain.trim(), draft.keyword.trim()].filter(Boolean);
      return {{
        draft,
        requiredReady,
        alertArmed,
        readiness,
        summary: draft.query.trim()
          ? phrase(
              "Track {{query}} with {{schedule}} across {{platform}} surfaces.",
              "围绕 {{query}} 以 {{schedule}} 跟踪 {{platform}} 信号。",
              {{
                query: draft.query.trim(),
                schedule: scheduleModeLabel(draft.schedule),
                platform: draft.platform.trim() || copy("cross-platform", "跨平台"),
              }},
            )
          : copy("Add a query to project the mission into the live preview lane.", "填入查询词后，任务会立即投射到实时预览区。"),
        scoreLabel: draft.min_score.trim() ? copy(`score >= ${{draft.min_score.trim()}}`, `分数 >= ${{draft.min_score.trim()}}`) : copy("score gate unset", "未设置分数门槛"),
        confidenceLabel: draft.min_confidence.trim() ? copy(`confidence >= ${{draft.min_confidence.trim()}}`, `置信度 >= ${{draft.min_confidence.trim()}}`) : copy("confidence gate unset", "未设置置信度门槛"),
        filtersLabel: filters.length ? filters.join(" / ") : copy("no scope filter", "未设置范围过滤"),
        routeLabel: draft.route.trim() || copy("route not attached", "未绑定路由"),
        scheduleLabel: scheduleModeLabel(draft.schedule),
      }};
    }}

    function syncCreateWatchForm() {{
      const form = $("create-watch-form");
      const draft = normalizeCreateWatchDraft(state.createWatchDraft || defaultCreateWatchDraft());
      if (!form) {{
        return;
      }}
      createWatchFormFields.forEach((fieldName) => {{
        const field = form.elements.namedItem(fieldName);
        if (!field || field.value === draft[fieldName]) {{
          return;
        }}
        field.value = draft[fieldName];
      }});
    }}

    function collectCreateWatchDraft(form) {{
      if (!form) {{
        return defaultCreateWatchDraft();
      }}
      const next = defaultCreateWatchDraft();
      createWatchFormFields.forEach((fieldName) => {{
        const field = form.elements.namedItem(fieldName);
        next[fieldName] = field ? String(field.value ?? "") : "";
      }});
      return normalizeCreateWatchDraft(next);
    }}

    function setCreateWatchDraft(nextDraft, presetId = "", editingId = state.createWatchEditingId) {{
      state.createWatchDraft = normalizeCreateWatchDraft(nextDraft || defaultCreateWatchDraft());
      state.createWatchPresetId = presetId;
      state.createWatchEditingId = String(editingId || "").trim();
      syncCreateWatchForm();
      persistCreateWatchDraft();
      renderCreateWatchDeck();
      queueCreateWatchSuggestions();
    }}

    function updateCreateWatchDraft(patch = {{}}, presetId = "") {{
      setCreateWatchDraft({{
        ...normalizeCreateWatchDraft(state.createWatchDraft || defaultCreateWatchDraft()),
        ...patch,
      }}, presetId);
    }}

    async function refreshCreateWatchSuggestions(force = false) {{
      const draft = normalizeCreateWatchDraft(state.createWatchDraft || defaultCreateWatchDraft());
      if (!force && !(draft.name.trim() || draft.query.trim() || draft.keyword.trim())) {{
        state.createWatchSuggestions = null;
        renderCreateWatchDeck();
        return;
      }}
      state.loading.suggestions = true;
      renderCreateWatchDeck();
      try {{
        state.createWatchSuggestions = await api("/api/console/deck/suggestions", {{
          method: "POST",
          headers: jsonHeaders,
          body: JSON.stringify(draft),
        }});
      }} catch (error) {{
        state.createWatchSuggestions = null;
        reportError(error, "Load mission suggestions");
      }} finally {{
        state.loading.suggestions = false;
        renderCreateWatchDeck();
      }}
    }}

    function queueCreateWatchSuggestions(force = false) {{
      if (state.createWatchSuggestionTimer) {{
        window.clearTimeout(state.createWatchSuggestionTimer);
      }}
      state.createWatchSuggestionTimer = window.setTimeout(() => {{
        refreshCreateWatchSuggestions(force).catch((error) => reportError(error, "Load mission suggestions"));
      }}, force ? 20 : 220);
    }}

    function renderCreateWatchDeck() {{
      const draft = normalizeCreateWatchDraft(state.createWatchDraft || defaultCreateWatchDraft());
      const editingId = String(state.createWatchEditingId || "").trim();
      const editing = Boolean(editingId);
      const advancedOpen = isCreateWatchAdvancedOpen(draft);
      const preview = buildCreateWatchPreview(draft);
      renderFormSuggestionLists();
      const presetPanel = $("create-watch-preset-panel");
      const presetRoot = $("create-watch-presets");
      const scheduleRoot = $("create-watch-schedule-picks");
      const platformRoot = $("create-watch-platform-picks");
      const routeRoot = $("create-watch-route-picks");
      const advancedTitle = $("deck-advanced-title");
      const advancedCopy = $("deck-advanced-copy");
      const advancedToggle = $("create-watch-advanced-toggle");
      const advancedSummary = $("create-watch-advanced-summary");
      const advancedPanel = $("create-watch-advanced-panel");
      const clonePanel = $("create-watch-clone-panel");
      const cloneRoot = $("create-watch-clones");
      const previewRoot = $("create-watch-preview");
      const suggestionRoot = $("create-watch-suggestions");
      const feedbackRoot = $("create-watch-feedback");
      const stageHudRoot = $("stage-hud");
      const submitButton = $("create-watch-submit");
      const clearButton = $("create-watch-clear");
      const deployTitle = $("deploy-title");
      const deployCopy = $("deploy-copy");

      if (deployTitle) {{
        deployTitle.textContent = editing ? copy("Edit Mission", "编辑监测任务") : copy("Deploy Mission", "创建监测任务");
      }}
      if (deployCopy) {{
        deployCopy.textContent = editing
          ? copy("Update one existing watch in place using the same mission deck.", "沿用同一套任务草稿面板，直接原位修改已有任务。")
          : copy("Create one watch, add optional scope, then decide whether alert routing is needed.", "先定义监测任务，再按需补充范围和通知条件。");
      }}
      if (advancedTitle) {{
        advancedTitle.textContent = editing ? copy("Refine Scope Carefully", "精细调整范围") : copy("Keep It Simple First", "先从简单输入开始");
      }}
      if (advancedCopy) {{
        advancedCopy.textContent = advancedOpen
          ? copy("Only fill the extra controls you actually need. Empty fields keep the mission broad and easier to operate.", "只填写真正需要的额外条件；留空代表任务保持更宽、更易操作。")
          : copy("Most missions only need Name and Query. Open advanced settings only when you need scope or alert delivery.", "大多数任务只需要名称和查询词；只有在要限定范围或接入告警时，再展开高级设置。");
      }}
      if (advancedToggle) {{
        advancedToggle.textContent = advancedOpen ? copy("Hide Advanced", "收起高级设置") : copy("Show Advanced", "展开高级设置");
        advancedToggle.setAttribute("aria-expanded", String(advancedOpen));
      }}
      if (advancedSummary) {{
        advancedSummary.innerHTML = summarizeCreateWatchAdvanced(draft).map((item) => `<span class="chip">${{escapeHtml(item)}}</span>`).join("");
      }}
      if (advancedPanel) {{
        advancedPanel.classList.toggle("collapsed", !advancedOpen);
        advancedPanel.setAttribute("aria-hidden", String(!advancedOpen));
      }}
      if (presetPanel) {{
        presetPanel.hidden = editing;
      }}
      if (clonePanel) {{
        clonePanel.hidden = editing;
      }}

      if (submitButton) {{
        submitButton.textContent = editing ? copy("Save Changes", "保存修改") : copy("Create Watch", "创建任务");
      }}
      if (clearButton) {{
        clearButton.textContent = editing ? copy("Cancel Edit", "取消编辑") : copy("Reset Draft", "清空草稿");
      }}

      if (presetRoot) {{
        presetRoot.innerHTML = createWatchPresets.map((preset, index) => `
          <button
            class="chip-btn ${{state.createWatchPresetId === preset.id ? "active" : ""}}"
            type="button"
            data-create-watch-preset="${{preset.id}}"
            title="${{escapeHtml(copy(preset.description, preset.zhDescription || preset.description))}}"
          >${{index + 1}}. ${{escapeHtml(copy(preset.label, preset.zhLabel || preset.label))}}</button>
        `).join("");
      }}

      if (scheduleRoot) {{
        scheduleRoot.innerHTML = scheduleLaneOptions.map((option) => `
          <button
            class="chip-btn ${{draft.schedule.trim() === option.value ? "active" : ""}}"
            type="button"
            data-create-watch-schedule="${{option.value}}"
          >${{escapeHtml(option.value === "manual" ? copy("manual", "手动") : option.label)}}</button>
        `).join("");
      }}

      if (platformRoot) {{
        platformRoot.innerHTML = platformLaneOptions.map((option) => `
          <button
            class="chip-btn ${{draft.platform.trim() === option.value ? "active" : ""}}"
            type="button"
            data-create-watch-platform="${{option.value}}"
          >${{escapeHtml(option.label)}}</button>
        `).join("");
      }}

      if (routeRoot) {{
        const routeButtons = state.routes.length
          ? state.routes.slice(0, 6).map((route) => `
              <button
                class="chip-btn ${{draft.route.trim() === String(route.name || "").trim() ? "active" : ""}}"
                type="button"
                data-create-watch-route="${{escapeHtml(route.name || "")}}"
              >${{escapeHtml(route.name || "unnamed-route")}}</button>
            `).join("")
          : `<span class="chip">${{copy("No named routes", "暂无命名路由")}}</span>`;
        routeRoot.innerHTML = routeButtons;
      }}

      if (cloneRoot) {{
        const cloneButtons = state.watches.length
          ? state.watches.slice(0, 6).map((watch) => `
              <button class="chip-btn" type="button" data-create-watch-clone="${{escapeHtml(watch.id)}}">${{escapeHtml(watch.name || watch.id)}}</button>
            `).join("")
          : `<span class="chip">${{copy("No mission to clone", "暂无可克隆任务")}}</span>`;
        cloneRoot.innerHTML = cloneButtons;
      }}

      if (previewRoot) {{
        previewRoot.className = `card mission-preview ${{preview.requiredReady ? "ready" : ""}}`;
        previewRoot.innerHTML = `
          <div class="card-top">
            <div>
              <div class="mono">${{copy("mission brief", "任务概览")}}</div>
              <h3 class="card-title" style="margin-top:10px;">${{escapeHtml(draft.name.trim() || copy("Unnamed Mission", "未命名任务"))}}</h3>
            </div>
            <span class="chip ${{preview.requiredReady ? "ok" : "hot"}}">${{preview.requiredReady ? copy("ready", "就绪") : copy("needs query/name", "缺少名称或查询词")}}</span>
          </div>
          <div class="panel-sub">${{escapeHtml(preview.summary)}}</div>
          <div class="preview-meter">
            <div class="preview-meter-fill" style="width:${{preview.readiness}}%;"></div>
          </div>
          <div class="meta">
            <span>${{copy("mode", "模式")}}=${{editing ? copy("edit existing", "编辑已有任务") : copy("create new", "新建任务")}}</span>
            <span>${{copy("readiness", "就绪度")}}=${{preview.readiness}}%</span>
            <span>${{copy("alert", "告警")}}=${{preview.alertArmed ? copy("armed", "已启用") : copy("passive", "未启用")}}</span>
            <span>${{copy("schedule", "频率")}}=${{escapeHtml(preview.scheduleLabel)}}</span>
          </div>
          <div class="preview-grid">
            <div class="preview-line">
              <div class="preview-label">${{copy("Scope", "范围")}}</div>
              <div class="preview-value">${{escapeHtml(preview.filtersLabel)}}</div>
            </div>
            <div class="preview-line">
              <div class="preview-label">${{copy("Route", "路由")}}</div>
              <div class="preview-value">${{escapeHtml(preview.routeLabel)}}</div>
            </div>
            <div class="preview-line">
              <div class="preview-label">${{copy("Score Gate", "分数门槛")}}</div>
              <div class="preview-value">${{escapeHtml(preview.scoreLabel)}}</div>
            </div>
            <div class="preview-line">
              <div class="preview-label">${{copy("Confidence Gate", "置信度门槛")}}</div>
              <div class="preview-value">${{escapeHtml(preview.confidenceLabel)}}</div>
            </div>
          </div>
        `;
      }}

      if (suggestionRoot) {{
        if (state.loading.suggestions) {{
          suggestionRoot.innerHTML = `
            <div class="mono">${{copy("mission suggestions", "任务建议")}}</div>
            <div class="panel-sub">${{copy("Deriving route, cadence, and duplicate signals from the current repository state.", "正在基于当前仓库状态推导路由、频率和重复信号。")}}</div>
            <div class="stack" style="margin-top:12px;">${{skeletonCard(4)}}</div>
          `;
        }} else if (!state.createWatchSuggestions) {{
          suggestionRoot.innerHTML = `
            <div class="mono">${{copy("mission suggestions", "任务建议")}}</div>
            <div class="panel-sub">${{copy("Start typing a mission draft and the deck will derive cadence, route, and duplicate pressure from current watches and stories.", "开始输入任务草稿后，系统会根据现有任务和故事自动推导频率、路由与重复风险。")}}</div>
          `;
        }} else {{
          const suggestions = state.createWatchSuggestions;
          const warningBlock = Array.isArray(suggestions.warnings) && suggestions.warnings.length
            ? `<div class="suggestion-list">${{suggestions.warnings.map((item) => `<div class="mini-item">${{escapeHtml(item)}}</div>`).join("")}}</div>`
            : `<div class="panel-sub">${{copy("No active conflict or delivery warning for this draft.", "当前草稿没有冲突或交付告警。")}}</div>`;
          const similarWatches = Array.isArray(suggestions.similar_watches) ? suggestions.similar_watches : [];
          const relatedStories = Array.isArray(suggestions.related_stories) ? suggestions.related_stories : [];
          suggestionRoot.innerHTML = `
            <div class="card-top">
              <div>
                <div class="mono">${{copy("mission suggestions", "任务建议")}}</div>
                <div class="panel-sub" style="margin-top:8px;">${{escapeHtml(suggestions.summary || "")}}</div>
              </div>
              <button class="btn-secondary" id="apply-all-suggestions" type="button">${{copy("Apply All", "全部应用")}}</button>
            </div>
            <div class="suggestion-grid">
              <div class="preview-grid">
                <div class="preview-line">
                  <div class="preview-label">${{copy("Cadence", "频率")}}</div>
                  <div class="preview-value">${{escapeHtml(suggestions.recommended_schedule || "-")}}</div>
                  <div class="panel-sub">${{escapeHtml(suggestions.schedule_reason || "")}}</div>
                </div>
                <div class="preview-line">
                  <div class="preview-label">${{copy("Platform", "平台")}}</div>
                  <div class="preview-value">${{escapeHtml(suggestions.recommended_platform || "-")}}</div>
                  <div class="panel-sub">${{escapeHtml(suggestions.platform_reason || "")}}</div>
                </div>
                <div class="preview-line">
                  <div class="preview-label">${{copy("Route", "路由")}}</div>
                  <div class="preview-value">${{escapeHtml(suggestions.recommended_route || "-")}}</div>
                  <div class="panel-sub">${{escapeHtml(suggestions.route_reason || "")}}</div>
                </div>
                <div class="preview-line">
                  <div class="preview-label">${{copy("Scope Hints", "范围提示")}}</div>
                  <div class="preview-value">${{escapeHtml(suggestions.recommended_keyword || "-")}} / ${{escapeHtml(suggestions.recommended_domain || "-")}}</div>
                  <div class="panel-sub">${{escapeHtml(suggestions.keyword_reason || suggestions.domain_reason || "")}}</div>
                </div>
              </div>
              <div class="chip-row">
                <button class="chip-btn" type="button" data-suggestion-apply="schedule">${{escapeHtml(suggestions.recommended_schedule || "schedule")}}</button>
                <button class="chip-btn" type="button" data-suggestion-apply="platform">${{escapeHtml(suggestions.recommended_platform || "platform")}}</button>
                <button class="chip-btn" type="button" data-suggestion-apply="route">${{escapeHtml(suggestions.recommended_route || "route")}}</button>
                <button class="chip-btn" type="button" data-suggestion-apply="keyword">${{escapeHtml(suggestions.recommended_keyword || "keyword")}}</button>
                <button class="chip-btn" type="button" data-suggestion-apply="thresholds">${{copy("score/confidence", "分数/置信度")}}</button>
              </div>
              <div class="stack">
                <div class="mono">${{copy("Warnings", "提醒")}}</div>
                ${{warningBlock}}
              </div>
              <div class="preview-grid">
                <div class="stack">
                  <div class="mono">${{copy("Similar Missions", "相似任务")}}</div>
                  ${{similarWatches.length ? similarWatches.map((item) => `<div class="mini-item">${{escapeHtml(item.name)}} | ${{copy("similarity", "相似度")}}=${{Number(item.similarity || 0).toFixed(2)}} | ${{escapeHtml(item.schedule || copy("manual", "手动"))}}</div>`).join("") : `<div class="panel-sub">${{copy("No mission conflict found.", "未发现任务冲突。")}}</div>`}}
                </div>
                <div class="stack">
                  <div class="mono">${{copy("Related Stories", "相关故事")}}</div>
                  ${{relatedStories.length ? relatedStories.map((item) => `<div class="mini-item">${{escapeHtml(item.title)}} | ${{copy("similarity", "相似度")}}=${{Number(item.similarity || 0).toFixed(2)}} | ${{copy("items", "条目")}}=${{item.item_count || 0}}</div>`).join("") : `<div class="panel-sub">${{copy("No story cluster overlap found.", "未发现故事簇重叠。")}}</div>`}}
                </div>
              </div>
            </div>
          `;
          suggestionRoot.querySelector("#apply-all-suggestions")?.addEventListener("click", () => {{
            const patch = suggestions.autofill_patch || {{}};
            state.createWatchAdvancedOpen = true;
            updateCreateWatchDraft(patch);
            showToast(copy("Applied suggested mission defaults", "已应用建议的任务默认值"), "success");
          }});
          suggestionRoot.querySelectorAll("[data-suggestion-apply]").forEach((button) => {{
            button.addEventListener("click", () => {{
              const patch = suggestions.autofill_patch || {{}};
              const field = String(button.dataset.suggestionApply || "").trim();
              if (field === "thresholds") {{
                state.createWatchAdvancedOpen = true;
                updateCreateWatchDraft({{
                  min_score: String(patch.min_score || ""),
                  min_confidence: String(patch.min_confidence || ""),
                }});
                return;
              }}
              if (!field || !(field in patch)) {{
                return;
              }}
              if (["schedule", "platform", "route", "keyword", "domain", "min_score", "min_confidence"].includes(field)) {{
                state.createWatchAdvancedOpen = true;
              }}
              updateCreateWatchDraft({{ [field]: String(patch[field] || "") }});
            }});
          }});
        }}
      }}

      if (feedbackRoot) {{
        if (editing) {{
          feedbackRoot.textContent = preview.requiredReady
            ? copy(
                `Editing ${{editingId}}. Use Cmd/Ctrl+Enter to save${{preview.alertArmed ? " with alert gating." : "."}}`,
                `正在编辑 ${{editingId}}。使用 Cmd/Ctrl+Enter 保存${{preview.alertArmed ? "，并带上告警门槛。" : "。"}}`,
              )
            : copy(
                `Editing ${{editingId}}. Name and Query are still required before saving.`,
                `正在编辑 ${{editingId}}。保存前仍需填写名称和查询词。`,
              );
        }} else {{
          feedbackRoot.textContent = preview.requiredReady
            ? copy(
                `Deck armed. Use Cmd/Ctrl+Enter to dispatch${{preview.alertArmed ? " with alert gating." : "."}}`,
                `草稿已就绪。使用 Cmd/Ctrl+Enter 提交${{preview.alertArmed ? "，并带上告警门槛。" : "。"}}`,
              )
            : copy("Required fields: Name and Query. Use / to focus the mission deck.", "必填字段：名称和查询词。按 / 可快速聚焦任务草稿。");
        }}
      }}

      if (stageHudRoot) {{
        stageHudRoot.innerHTML = `
          <div class="card-top">
            <div>
              <div class="mono">${{copy("Live Mission Projection", "实时任务投影")}}</div>
              <div class="stage-hud-title">${{escapeHtml(draft.name.trim() || draft.query.trim() || copy("Awaiting Mission Draft", "等待任务草稿"))}}</div>
            </div>
            <span class="chip ${{preview.requiredReady ? "ok" : ""}}">${{preview.requiredReady ? copy("synced", "已同步") : copy("draft", "草稿")}}</span>
          </div>
          <div class="stage-hud-summary">${{escapeHtml(preview.summary)}}</div>
          <div class="stage-hud-meta">
            <span class="chip">${{escapeHtml(preview.scheduleLabel)}}</span>
            <span class="chip">${{escapeHtml(preview.filtersLabel)}}</span>
            <span class="chip ${{preview.alertArmed ? "hot" : ""}}">${{preview.alertArmed ? copy("alert armed", "告警已启用") : copy("passive watch", "仅监测")}}</span>
          </div>
        `;
      }}
      renderActionHistory();
    }}

    function createWatchDraftFromMissionDetail(detail, {{ copyName = false }} = {{}}) {{
      const firstRule = Array.isArray(detail.alert_rules) && detail.alert_rules.length ? detail.alert_rules[0] : {{}};
      return {{
        name: copyName && detail.name ? `${{detail.name}} copy` : (detail.name || ""),
        schedule: detail.schedule || "",
        query: detail.query || "",
        platform: Array.isArray(detail.platforms) && detail.platforms.length ? detail.platforms[0] : "",
        domain: Array.isArray(firstRule.domains) && firstRule.domains.length ? firstRule.domains[0] : "",
        route: Array.isArray(firstRule.routes) && firstRule.routes.length ? firstRule.routes[0] : "",
        keyword: Array.isArray(firstRule.keyword_any) && firstRule.keyword_any.length ? firstRule.keyword_any[0] : "",
        min_score: firstRule.min_score ? String(firstRule.min_score) : "",
        min_confidence: firstRule.min_confidence ? String(firstRule.min_confidence) : "",
      }};
    }}

    async function editMissionInCreateWatch(identifier) {{
      if (!identifier) {{
        return;
      }}
      const detail = state.watchDetails[identifier] || await api(`/api/watches/${{identifier}}`);
      state.watchDetails[identifier] = detail;
      state.createWatchAdvancedOpen = true;
      setCreateWatchDraft(createWatchDraftFromMissionDetail(detail), "", detail.id || identifier);
      showToast(
        state.language === "zh"
          ? `已载入任务编辑：${{detail.name || identifier}}`
          : `Editing mission: ${{detail.name || identifier}}`,
        "success",
      );
      focusCreateWatchDeck("name");
    }}

    async function cloneMissionIntoCreateWatch(identifier) {{
      if (!identifier) {{
        return;
      }}
      const detail = state.watchDetails[identifier] || await api(`/api/watches/${{identifier}}`);
      state.watchDetails[identifier] = detail;
      state.createWatchAdvancedOpen = true;
      setCreateWatchDraft(createWatchDraftFromMissionDetail(detail, {{ copyName: true }}), "", "");
      showToast(
        state.language === "zh"
          ? `已从 ${{detail.name || identifier}} 克隆任务草稿`
          : `Mission deck cloned from ${{detail.name || identifier}}`,
        "success",
      );
      focusCreateWatchDeck("name");
    }}

    function bindCreateWatchDeck() {{
      const form = $("create-watch-form");
      const presetRoot = $("create-watch-presets");
      const scheduleRoot = $("create-watch-schedule-picks");
      const platformRoot = $("create-watch-platform-picks");
      const routeRoot = $("create-watch-route-picks");
      const cloneRoot = $("create-watch-clones");
      const clearButton = $("create-watch-clear");
      const advancedToggle = $("create-watch-advanced-toggle");
      if (!form) {{
        return;
      }}

      syncCreateWatchForm();
      renderCreateWatchDeck();
      queueCreateWatchSuggestions(true);

      form.addEventListener("input", () => {{
        state.createWatchPresetId = "";
        state.createWatchDraft = collectCreateWatchDraft(form);
        persistCreateWatchDraft();
        renderCreateWatchDeck();
        queueCreateWatchSuggestions();
      }});

      form.addEventListener("keydown", (event) => {{
        if ((event.metaKey || event.ctrlKey) && String(event.key || "").toLowerCase() === "enter") {{
          event.preventDefault();
          form.requestSubmit();
        }}
      }});

      advancedToggle?.addEventListener("click", () => {{
        state.createWatchAdvancedOpen = !isCreateWatchAdvancedOpen(state.createWatchDraft || defaultCreateWatchDraft());
        renderCreateWatchDeck();
      }});

      presetRoot?.addEventListener("click", (event) => {{
        const button = event.target.closest("[data-create-watch-preset]");
        if (!button) {{
          return;
        }}
        const preset = createWatchPresets.find((candidate) => candidate.id === button.dataset.createWatchPreset);
        if (!preset) {{
          return;
        }}
        state.createWatchAdvancedOpen = draftHasAdvancedSignal(preset.values);
        setCreateWatchDraft(preset.values, preset.id, "");
        showToast(
          state.language === "zh"
            ? `${{preset.zhLabel || preset.label}} 已载入任务草稿`
            : `${{preset.label}} loaded into the mission deck`,
          "success",
        );
        focusCreateWatchDeck("query");
      }});

      scheduleRoot?.addEventListener("click", (event) => {{
        const button = event.target.closest("[data-create-watch-schedule]");
        if (!button) {{
          return;
        }}
        state.createWatchAdvancedOpen = true;
        updateCreateWatchDraft({{ schedule: String(button.dataset.createWatchSchedule || "") }});
      }});

      platformRoot?.addEventListener("click", (event) => {{
        const button = event.target.closest("[data-create-watch-platform]");
        if (!button) {{
          return;
        }}
        state.createWatchAdvancedOpen = true;
        updateCreateWatchDraft({{ platform: String(button.dataset.createWatchPlatform || "") }});
      }});

      routeRoot?.addEventListener("click", (event) => {{
        const button = event.target.closest("[data-create-watch-route]");
        if (!button) {{
          return;
        }}
        state.createWatchAdvancedOpen = true;
        updateCreateWatchDraft({{ route: String(button.dataset.createWatchRoute || "") }});
      }});

      cloneRoot?.addEventListener("click", async (event) => {{
        const button = event.target.closest("[data-create-watch-clone]");
        if (!button) {{
          return;
        }}
        button.disabled = true;
        try {{
          await cloneMissionIntoCreateWatch(String(button.dataset.createWatchClone || ""));
        }} catch (error) {{
          reportError(error, copy("Clone mission", "克隆任务"));
        }} finally {{
          button.disabled = false;
        }}
      }});

      clearButton?.addEventListener("click", () => {{
        const wasEditing = Boolean(String(state.createWatchEditingId || "").trim());
        state.createWatchAdvancedOpen = null;
        setCreateWatchDraft(defaultCreateWatchDraft(), "", "");
        showToast(
          wasEditing
            ? copy("Mission edit cancelled", "已取消任务编辑")
            : copy("Mission deck draft cleared", "已清空任务草稿"),
          "success",
        );
        focusCreateWatchDeck("name");
      }});
    }}

    function bindRouteDeck() {{
      if (!state.routeDraft) {{
        state.routeDraft = defaultRouteDraft();
      }}
      renderRouteDeck();
    }}

    function bindStoryDeck() {{
      if (!state.storyDraft) {{
        state.storyDraft = defaultStoryDraft();
      }}
      renderStoryCreateDeck();
    }}

    function bindHeroStageMotion() {{
      const hero = $("hero-main");
      const stage = hero?.querySelector(".hero-stage");
      const visual = hero?.querySelector(".hero-visual");
      const globe = hero?.querySelector(".stage-globe");
      const leftRing = hero?.querySelector(".stage-ring-left");
      const rightRing = hero?.querySelector(".stage-ring-right");
      const leftConsole = hero?.querySelector(".stage-console-left");
      const rightConsole = hero?.querySelector(".stage-console-right");
      if (!hero || !stage || !visual || !globe || !leftRing || !rightRing || !leftConsole || !rightConsole) {{
        return;
      }}

      const reset = () => {{
        stage.style.transform = "";
        visual.style.transform = "";
        globe.style.transform = "translateX(-50%)";
        leftRing.style.transform = "";
        rightRing.style.transform = "";
        leftConsole.style.transform = "";
        rightConsole.style.transform = "";
      }};

      hero.addEventListener("pointermove", (event) => {{
        const rect = hero.getBoundingClientRect();
        const x = ((event.clientX - rect.left) / rect.width) - 0.5;
        const y = ((event.clientY - rect.top) / rect.height) - 0.5;
        stage.style.transform = `perspective(1200px) rotateX(${{-y * 6}}deg) rotateY(${{x * 7}}deg)`;
        visual.style.transform = `scale(1.05) translate(${{x * -16}}px, ${{y * -12}}px)`;
        globe.style.transform = `translate(calc(-50% + ${{x * 20}}px), ${{y * 12}}px)`;
        leftRing.style.transform = `translateX(${{x * -10}}px)`;
        rightRing.style.transform = `translateX(${{x * 10}}px)`;
        leftConsole.style.transform = `translate(${{x * -8}}px, ${{y * 6}}px)`;
        rightConsole.style.transform = `translate(${{x * 8}}px, ${{y * 6}}px)`;
      }});

      hero.addEventListener("pointerleave", reset);
      reset();
    }}

    function rerenderLanguageSensitiveViews() {{
      applyLanguageChrome();
      renderOverview();
      renderWatches();
      renderWatchDetail();
      renderAlerts();
      renderRoutes();
      renderRouteHealth();
      renderStatus();
      renderTriage();
      renderStories();
      renderCreateWatchDeck();
      renderCommandPalette();
    }}

    function setLanguage(nextLanguage) {{
      const normalized = String(nextLanguage || "").trim().toLowerCase() === "zh" ? "zh" : "en";
      state.language = normalized;
      safeLocalStorageSet(languageStorageKey, normalized);
      rerenderLanguageSensitiveViews();
    }}

    function bindLanguageSwitch() {{
      document.querySelectorAll("[data-lang]").forEach((button) => {{
        button.addEventListener("click", () => {{
          const nextLanguage = String(button.dataset.lang || "").trim();
          if (!nextLanguage || nextLanguage === state.language) {{
            return;
          }}
          setLanguage(nextLanguage);
        }});
      }});
    }}

    function bindSectionJumps() {{
      document.querySelectorAll("[data-jump-target]").forEach((button) => {{
        button.addEventListener("click", () => {{
          const targetId = String(button.dataset.jumpTarget || "").trim();
          const target = targetId ? document.getElementById(targetId) : null;
          target?.scrollIntoView({{ block: "start", behavior: "smooth" }});
        }});
      }});
    }}

    function buildCommandPaletteEntries() {{
      const entries = [
        {{
          id: "refresh",
          group: copy("system", "系统"),
          title: copy("Refresh Console", "刷新控制台"),
          subtitle: copy("Reload overview, missions, triage, stories, and ops.", "重新加载总览、任务、分诊、故事和运维视图。"),
          run: async () => {{
            await refreshBoard();
            showToast(copy("Console refreshed", "控制台已刷新"), "success");
          }},
        }},
        {{
          id: "run-due",
          group: copy("system", "系统"),
          title: copy("Run Due Missions", "执行到点任务"),
          subtitle: copy("Dispatch every mission currently due.", "立即执行当前所有到点任务。"),
          run: async () => {{
            await api("/api/watches/run-due", {{ method: "POST", headers: jsonHeaders, body: JSON.stringify({{ limit: 0 }}) }});
            await refreshBoard();
            showToast(copy("Due missions dispatched", "到点任务已触发执行"), "success");
          }},
        }},
        {{
          id: "focus-deck",
          group: copy("deck", "草稿"),
          title: copy("Focus Mission Deck", "聚焦任务草稿"),
          subtitle: copy("Jump to the draft deck and focus the main field.", "跳转到任务草稿区并聚焦主输入框。"),
          run: async () => {{
            focusCreateWatchDeck((state.createWatchDraft && state.createWatchDraft.name.trim()) ? "query" : "name");
          }},
        }},
        {{
          id: "clear-deck",
          group: copy("deck", "草稿"),
          title: copy("Reset Mission Deck", "清空任务草稿"),
          subtitle: copy("Clear the current draft and its stored local state.", "清空当前草稿及其本地缓存。"),
          run: async () => {{
            const wasEditing = Boolean(String(state.createWatchEditingId || "").trim());
            state.createWatchAdvancedOpen = null;
            setCreateWatchDraft(defaultCreateWatchDraft(), "", "");
            showToast(
              wasEditing
                ? copy("Mission edit cancelled", "已取消任务编辑")
                : copy("Mission deck draft cleared", "已清空任务草稿"),
              "success",
            );
          }},
        }},
        {{
          id: "focus-route-deck",
          group: copy("routes", "路由"),
          title: copy("Focus Route Deck", "聚焦路由草稿"),
          subtitle: copy("Jump to the route manager and focus the route name field.", "跳转到路由管理区并聚焦路由名称。"),
          run: async () => {{
            focusRouteDeck((state.routeDraft && state.routeDraft.name.trim()) ? "description" : "name");
          }},
        }},
        {{
          id: "clear-route-deck",
          group: copy("routes", "路由"),
          title: copy("Reset Route Deck", "清空路由草稿"),
          subtitle: copy("Clear the current route draft or exit edit mode.", "清空当前路由草稿或退出编辑模式。"),
          run: async () => {{
            const wasEditing = Boolean(normalizeRouteName(state.routeEditingId));
            state.routeAdvancedOpen = null;
            setRouteDraft(defaultRouteDraft(), "");
            showToast(
              wasEditing
                ? copy("Route edit cancelled", "已取消路由编辑")
                : copy("Route deck draft cleared", "已清空路由草稿"),
              "success",
            );
          }},
        }},
        {{
          id: "focus-story-deck",
          group: copy("stories", "故事"),
          title: copy("Focus Story Intake", "聚焦故事录入"),
          subtitle: copy("Jump to the manual story deck and start a new brief.", "跳转到手工故事草稿区，直接开始新建简报。"),
          run: async () => {{
            focusStoryDeck((state.storyDraft && state.storyDraft.title.trim()) ? "summary" : "title");
          }},
        }},
      ];
      if (state.actionLog.length && state.actionLog[0].undo) {{
        const latestAction = state.actionLog[0];
        entries.unshift({{
          id: `undo-${{latestAction.id}}`,
          group: copy("actions", "操作"),
          title: state.language === "zh" ? `撤销：${{latestAction.label}}` : `Undo: ${{latestAction.label}}`,
          subtitle: latestAction.detail || copy("Reverse the latest reversible action.", "撤销最近一次可回退操作。"),
          run: async () => {{
            await latestAction.undo();
            state.actionLog = state.actionLog.filter((entry) => entry.id !== latestAction.id);
            renderActionHistory();
          }},
        }});
      }}
      state.watches.slice(0, 6).forEach((watch) => {{
        entries.push({{
          id: `watch-open-${{watch.id}}`,
          group: copy("missions", "任务"),
          title: state.language === "zh" ? `打开任务：${{watch.name}}` : `Open Mission: ${{watch.name}}`,
          subtitle: `${{watch.query || "-"}} | ${{watch.enabled ? copy("enabled", "已启用") : copy("disabled", "已停用")}}`,
          run: async () => {{
            await loadWatch(watch.id);
          }},
        }});
        entries.push({{
          id: `watch-edit-${{watch.id}}`,
          group: copy("missions", "任务"),
          title: state.language === "zh" ? `编辑任务：${{watch.name}}` : `Edit Mission: ${{watch.name}}`,
          subtitle: copy("Load this mission into the deck for in-place editing.", "把该任务载入草稿区，直接原位编辑。"),
          run: async () => {{
            await editMissionInCreateWatch(watch.id);
          }},
        }});
        entries.push({{
          id: `watch-clone-${{watch.id}}`,
          group: copy("missions", "任务"),
          title: state.language === "zh" ? `克隆任务：${{watch.name}}` : `Clone Mission: ${{watch.name}}`,
          subtitle: copy("Pull this mission into the deck as a draft fork.", "把这个任务拉进草稿区，作为分支任务继续编辑。"),
          run: async () => {{
            await cloneMissionIntoCreateWatch(watch.id);
          }},
        }});
      }});
      state.routes.slice(0, 6).forEach((route) => {{
        entries.push({{
          id: `route-edit-${{route.name}}`,
          group: copy("routes", "路由"),
          title: state.language === "zh" ? `编辑路由：${{route.name}}` : `Edit Route: ${{route.name}}`,
          subtitle: `${{routeChannelLabel(route.channel)}} | ${{summarizeRouteDestination(route)}}`,
          run: async () => {{
            await editRouteInDeck(route.name);
          }},
        }});
        entries.push({{
          id: `route-apply-${{route.name}}`,
          group: copy("routes", "路由"),
          title: state.language === "zh" ? `把路由用于任务：${{route.name}}` : `Use Route In Mission: ${{route.name}}`,
          subtitle: copy("Attach this named route to the mission intake deck.", "把这个命名路由直接带入任务草稿。"),
          run: async () => {{
            await applyRouteToMissionDraft(route.name);
          }},
        }});
      }});
      const visibleTriage = getVisibleTriageItems();
      const focusedTriageId = state.selectedTriageId || (visibleTriage[0] ? visibleTriage[0].id : "");
      const focusedTriage = focusedTriageId
        ? visibleTriage.find((item) => item.id === focusedTriageId) || state.triage.find((item) => item.id === focusedTriageId)
        : null;
      if (focusedTriage) {{
        entries.push({{
          id: `triage-story-${{focusedTriage.id}}`,
          group: copy("triage", "分诊"),
          title: state.language === "zh" ? `从分诊生成故事：${{focusedTriage.title}}` : `Create Story From Triage: ${{focusedTriage.title}}`,
          subtitle: copy("Promote the focused triage item into a story draft and jump to Story Workspace.", "把当前焦点分诊条目提升为故事草稿，并跳转到故事工作台。"),
          run: async () => {{
            await createStoryFromTriageItems([focusedTriage.id]);
          }},
        }});
        entries.push({{
          id: `triage-note-${{focusedTriage.id}}`,
          group: copy("triage", "分诊"),
          title: state.language === "zh" ? `聚焦备注：${{focusedTriage.title}}` : `Focus Note: ${{focusedTriage.title}}`,
          subtitle: copy("Jump back to the queue and place the cursor in the note composer.", "跳回分诊队列，并把光标放进备注输入框。"),
          run: async () => {{
            focusTriageNoteComposer(focusedTriage.id);
          }},
        }});
      }}
      state.stories.slice(0, 5).forEach((story) => {{
        entries.push({{
          id: `story-open-${{story.id}}`,
          group: copy("stories", "故事"),
          title: state.language === "zh" ? `打开故事：${{story.title}}` : `Open Story: ${{story.title}}`,
          subtitle: `${{localizeWord(story.status || "active")}} | ${{copy("items", "条目")}}=${{story.item_count || 0}}`,
          run: async () => {{
            await loadStory(story.id);
          }},
        }});
      }});
      return entries;
    }}

    function renderCommandPalette() {{
      const backdrop = $("command-palette");
      const input = $("command-palette-input");
      const list = $("command-palette-list");
      if (!backdrop || !input || !list) {{
        return;
      }}
      backdrop.classList.toggle("open", state.commandPalette.open);
      if (!state.commandPalette.open) {{
        return;
      }}
      const query = String(state.commandPalette.query || "").trim().toLowerCase();
      const entries = buildCommandPaletteEntries().filter((entry) => {{
        if (!query) {{
          return true;
        }}
        return [entry.group, entry.title, entry.subtitle].some((value) => String(value || "").toLowerCase().includes(query));
      }});
      if (state.commandPalette.selectedIndex >= entries.length) {{
        state.commandPalette.selectedIndex = Math.max(entries.length - 1, 0);
      }}
      list.innerHTML = entries.length
        ? entries.map((entry, index) => `
            <div class="palette-item ${{index === state.commandPalette.selectedIndex ? "active" : ""}}" data-palette-id="${{entry.id}}" data-palette-index="${{index}}">
              <div class="palette-kicker">${{escapeHtml(entry.group)}}</div>
              <div>${{escapeHtml(entry.title)}}</div>
              <div class="panel-sub">${{escapeHtml(entry.subtitle || "")}}</div>
            </div>
          `).join("")
        : `<div class="empty">${{copy("No command matched the current search.", "当前搜索没有匹配到命令。")}}</div>`;
      list.querySelectorAll("[data-palette-id]").forEach((item) => {{
        item.addEventListener("mouseenter", () => {{
          state.commandPalette.selectedIndex = Number(item.dataset.paletteIndex || 0);
          renderCommandPalette();
        }});
        item.addEventListener("click", async () => {{
          const entry = entries.find((candidate) => candidate.id === item.dataset.paletteId);
          if (!entry) {{
            return;
          }}
          closeCommandPalette();
          try {{
            await entry.run();
          }} catch (error) {{
            reportError(error, "Palette action");
          }}
        }});
      }});
      input.value = state.commandPalette.query;
    }}

    function openCommandPalette() {{
      state.commandPalette.open = true;
      state.commandPalette.selectedIndex = 0;
      renderCommandPalette();
      window.setTimeout(() => $("command-palette-input")?.focus(), 10);
    }}

    function closeCommandPalette() {{
      state.commandPalette.open = false;
      state.commandPalette.query = "";
      state.commandPalette.selectedIndex = 0;
      renderCommandPalette();
    }}

    function bindCommandPalette() {{
      const backdrop = $("command-palette");
      const input = $("command-palette-input");
      if (!backdrop || !input) {{
        return;
      }}
      backdrop.addEventListener("click", (event) => {{
        if (event.target === backdrop) {{
          closeCommandPalette();
        }}
      }});
      input.addEventListener("input", () => {{
        state.commandPalette.query = input.value;
        state.commandPalette.selectedIndex = 0;
        renderCommandPalette();
      }});
      input.addEventListener("keydown", async (event) => {{
        const list = buildCommandPaletteEntries().filter((entry) => {{
          const query = String(state.commandPalette.query || "").trim().toLowerCase();
          if (!query) {{
            return true;
          }}
          return [entry.group, entry.title, entry.subtitle].some((value) => String(value || "").toLowerCase().includes(query));
        }});
        if (event.key === "ArrowDown") {{
          event.preventDefault();
          state.commandPalette.selectedIndex = Math.min(state.commandPalette.selectedIndex + 1, Math.max(list.length - 1, 0));
          renderCommandPalette();
        }} else if (event.key === "ArrowUp") {{
          event.preventDefault();
          state.commandPalette.selectedIndex = Math.max(state.commandPalette.selectedIndex - 1, 0);
          renderCommandPalette();
        }} else if (event.key === "Enter") {{
          event.preventDefault();
          const entry = list[state.commandPalette.selectedIndex];
          if (!entry) {{
            return;
          }}
          closeCommandPalette();
          try {{
            await entry.run();
          }} catch (error) {{
            reportError(error, "Palette action");
          }}
        }} else if (event.key === "Escape") {{
          event.preventDefault();
          closeCommandPalette();
        }}
      }});
    }}

    state.createWatchDraft = loadCreateWatchDraft();

    function metricCard(label, value, tone = "") {{
      return `<div class="metric"><div class="metric-label">${{label}}</div><div class="metric-value ${{tone}}">${{value}}</div></div>`;
    }}

    function formatRate(value) {{
      if (value === null || value === undefined || Number.isNaN(Number(value))) {{
        return "-";
      }}
      return `${{Math.round(Number(value) * 100)}}%`;
    }}

    function skeletonCard(lines = 3) {{
      return `
        <div class="card skeleton">
          <div class="stack">
            ${{Array.from({{ length: lines }}).map((_, index) => `
              <div class="skeleton-block ${{index === 0 ? "short" : index === lines - 1 ? "long" : "medium"}}"></div>
            `).join("")}}
          </div>
        </div>
      `;
    }}

    function renderActionHistory() {{
      const root = $("console-action-history");
      if (!root) {{
        return;
      }}
      if (!state.actionLog.length) {{
        root.innerHTML = `<div class="empty">${{copy("No reversible action yet. Create, tune, or triage something and it will show up here.", "当前还没有可回退的操作。创建、调整或分诊后，会在这里显示。")}}</div>`;
        return;
      }}
      root.innerHTML = state.actionLog.slice(0, 6).map((entry) => `
        <div class="action-log-item">
          <div class="card-top">
            <div>
              <div class="mono">${{escapeHtml(entry.kind || "action")}}</div>
              <div>${{escapeHtml(entry.label || "")}}</div>
            </div>
            <span class="chip ${{entry.status === "error" ? "hot" : entry.status === "ready" ? "ok" : ""}}">${{escapeHtml(localizeWord(entry.status || "done"))}}</span>
          </div>
          <div class="panel-sub">${{escapeHtml(entry.detail || "")}}</div>
          <div class="actions">
            ${{
              entry.undo
                ? `<button class="btn-secondary" type="button" data-action-undo="${{entry.id}}">${{escapeHtml(entry.undoLabel || copy("Undo", "撤销"))}}</button>`
                : ""
            }}
          </div>
        </div>
      `).join("");
      root.querySelectorAll("[data-action-undo]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          const item = state.actionLog.find((entry) => entry.id === button.dataset.actionUndo);
          if (!item || !item.undo) {{
            return;
          }}
          button.disabled = true;
          try {{
            await item.undo();
            state.actionLog = state.actionLog.filter((entry) => entry.id !== item.id);
            renderActionHistory();
          }} catch (error) {{
            reportError(error, "Undo action");
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});
    }}

    function pushActionEntry(entry) {{
      state.actionLog = [{{
        id: `action-${{Date.now()}}-${{Math.random().toString(16).slice(2, 8)}}`,
        timestamp: new Date().toISOString(),
        status: "ready",
        ...entry,
      }}, ...state.actionLog].slice(0, 8);
      renderActionHistory();
    }}

    function buildAlertRules({{ route = "", keyword = "", domain = "", minScore = 0, minConfidence = 0 }}) {{
      const cleanedRoute = String(route || "").trim();
      const cleanedKeyword = String(keyword || "").trim();
      const cleanedDomain = String(domain || "").trim();
      const scoreValue = Math.max(0, Number(minScore || 0));
      const confidenceValue = Math.max(0, Number(minConfidence || 0));
      if (!(cleanedRoute || cleanedKeyword || cleanedDomain || scoreValue > 0 || confidenceValue > 0)) {{
        return [];
      }}
      const alertRule = {{
        name: "console-threshold",
        min_score: scoreValue,
        min_confidence: confidenceValue,
        channels: ["json"],
      }};
      if (cleanedRoute) alertRule.routes = [cleanedRoute];
      if (cleanedKeyword) alertRule.keyword_any = [cleanedKeyword];
      if (cleanedDomain) alertRule.domains = [cleanedDomain];
      return [alertRule];
    }}

    function renderOverview() {{
      const metrics = state.overview || {{}};
      if (state.loading.board && !state.overview) {{
        $("overview-metrics").innerHTML = [metricCard(copy("Loading", "加载中"), "..."), metricCard(copy("Loading", "加载中"), "..."), metricCard(copy("Loading", "加载中"), "...")].join("");
        return;
      }}
      $("overview-metrics").innerHTML = [
        metricCard(copy("Enabled Missions", "已启用任务"), metrics.enabled_watches ?? 0),
        metricCard(copy("Due Now", "当前到点"), metrics.due_watches ?? 0, "hot"),
        metricCard(copy("Stories", "故事"), metrics.story_count ?? 0),
        metricCard(copy("Alert Routes", "告警路由"), metrics.route_count ?? 0),
        metricCard(copy("Open Queue", "待分诊队列"), metrics.triage_open_count ?? 0),
        metricCard(copy("Daemon State", "守护进程状态"), localizeWord(String(metrics.daemon_state || "idle")).toUpperCase()),
      ].join("");
    }}

    function renderWatches() {{
      const root = $("watch-list");
      if (state.loading.board && !state.watches.length) {{
        root.innerHTML = [skeletonCard(4), skeletonCard(4), skeletonCard(4)].join("");
        return;
      }}
      if (!state.watches.length) {{
        root.innerHTML = `<div class="empty">${{copy("No watch mission configured yet.", "当前还没有配置监测任务。")}}</div>`;
        return;
      }}
      const searchValue = String(state.watchSearch || "");
      const searchQuery = searchValue.trim().toLowerCase();
      const filteredWatches = state.watches.filter((watch) => {{
        if (!searchQuery) {{
          return true;
        }}
        const haystack = [
          watch.id,
          watch.name,
          watch.query,
          ...(Array.isArray(watch.platforms) ? watch.platforms : []),
          ...(Array.isArray(watch.sites) ? watch.sites : []),
          watch.schedule,
          watch.schedule_label,
        ].join(" ").toLowerCase();
        return haystack.includes(searchQuery);
      }});
      const searchToolbar = `
        <div class="card section-toolbox">
          <div class="section-toolbox-head">
            <div>
              <div class="mono">${{copy("mission search", "任务搜索")}}</div>
              <div class="panel-sub">${{copy("Search by name, query, id, platform, or site to narrow the board before acting.", "可按名称、查询词、任务 ID、平台或站点快速缩小任务列表。")}}</div>
            </div>
            <div class="section-toolbox-meta">
              <span class="chip">${{copy("shown", "显示")}}=${{filteredWatches.length}}</span>
              <span class="chip">${{copy("total", "总数")}}=${{state.watches.length}}</span>
            </div>
          </div>
          <div class="search-shell">
            <input type="search" value="${{escapeHtml(searchValue)}}" data-watch-search placeholder="${{copy("Search missions", "搜索任务")}}">
            <button class="btn-secondary" type="button" data-watch-search-clear ${{searchValue.trim() ? "" : "disabled"}}>${{copy("Clear", "清空")}}</button>
          </div>
        </div>
      `;
      if (!filteredWatches.length) {{
        root.innerHTML = `${{searchToolbar}}<div class="empty">${{copy("No mission matched the current search.", "没有任务匹配当前搜索。")}}</div>`;
        root.querySelector("[data-watch-search]")?.addEventListener("input", (event) => {{
          state.watchSearch = event.target.value;
          renderWatches();
        }});
        root.querySelector("[data-watch-search-clear]")?.addEventListener("click", () => {{
          state.watchSearch = "";
          renderWatches();
        }});
        return;
      }}
      root.innerHTML = `${{searchToolbar}}${{filteredWatches.map((watch) => {{
        const platforms = (watch.platforms || []).join(", ") || copy("any", "任意");
        const sites = (watch.sites || []).join(", ") || "-";
        const stateChip = watch.enabled ? "ok" : "";
        const dueChip = watch.is_due ? "hot" : "";
        const selected = watch.id === state.selectedWatchId ? "selected" : "";
        return `
          <div class="card selectable ${{selected}}">
            <div class="card-top">
              <div>
                <h3 class="card-title">${{watch.name}}</h3>
                <div class="meta">
                  <span>${{watch.id}}</span>
                  <span>${{copy("schedule", "频率")}}=${{watch.schedule_label || watch.schedule || copy("manual", "手动")}}</span>
                  <span>${{copy("platforms", "平台")}}=${{platforms}}</span>
                  <span>${{copy("sites", "站点")}}=${{sites}}</span>
                </div>
              </div>
              <div style="display:grid; gap:6px; justify-items:end;">
                <span class="chip ${{stateChip}}">${{watch.enabled ? copy("enabled", "已启用") : copy("disabled", "已停用")}}</span>
                <span class="chip ${{dueChip}}">${{watch.is_due ? copy("due", "待执行") : copy("waiting", "等待")}}</span>
              </div>
            </div>
            <div class="meta">
              <span>${{copy("alert_rules", "告警规则")}}=${{watch.alert_rule_count || 0}}</span>
              <span>${{copy("last_run", "上次执行")}}=${{watch.last_run_at || "-"}}</span>
              <span>${{copy("status", "状态")}}=${{localizeWord(watch.last_run_status || "-")}}</span>
              <span>${{copy("next", "下次")}}=${{watch.next_run_at || "-"}}</span>
            </div>
            <div class="actions">
              <button class="btn-secondary" data-watch-open="${{watch.id}}">${{copy("Open Cockpit", "打开驾驶舱")}}</button>
              <button class="btn-secondary" data-edit-watch="${{watch.id}}">${{copy("Edit", "编辑")}}</button>
              <button class="btn-secondary" data-run-watch="${{watch.id}}">${{copy("Run Mission", "执行任务")}}</button>
              <button class="btn-secondary" data-watch-toggle="${{watch.id}}" data-watch-enabled="${{watch.enabled ? "1" : "0"}}">${{watch.enabled ? copy("Disable", "停用") : copy("Enable", "启用")}}</button>
              <button class="btn-danger" data-delete-watch="${{watch.id}}">${{copy("Delete", "删除")}}</button>
            </div>
          </div>`;
      }}).join("")}}`;

      root.querySelector("[data-watch-search]")?.addEventListener("input", (event) => {{
        state.watchSearch = event.target.value;
        renderWatches();
      }});
      root.querySelector("[data-watch-search-clear]")?.addEventListener("click", () => {{
        state.watchSearch = "";
        renderWatches();
      }});

      root.querySelectorAll("[data-watch-open]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await loadWatch(button.dataset.watchOpen);
          }} catch (error) {{
            reportError(error, copy("Open mission", "打开任务"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      root.querySelectorAll("[data-edit-watch]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await editMissionInCreateWatch(button.dataset.editWatch);
          }} catch (error) {{
            reportError(error, copy("Edit mission", "编辑任务"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      root.querySelectorAll("[data-run-watch]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await api(`/api/watches/${{button.dataset.runWatch}}/run`, {{ method: "POST" }});
            await refreshBoard();
          }} catch (error) {{
            reportError(error, copy("Run mission", "执行任务"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      root.querySelectorAll("[data-watch-toggle]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          const identifier = String(button.dataset.watchToggle || "").trim();
          const isEnabled = String(button.dataset.watchEnabled || "1") === "1";
          const previousWatch = state.watches.find((watch) => watch.id === identifier);
          const previousDetail = state.watchDetails[identifier] ? {{ ...state.watchDetails[identifier] }} : null;
          button.disabled = true;
          if (previousWatch) {{
            previousWatch.enabled = !isEnabled;
          }}
          if (state.watchDetails[identifier]) {{
            state.watchDetails[identifier].enabled = !isEnabled;
          }}
          renderWatches();
          renderWatchDetail();
          try {{
            await api(`/api/watches/${{identifier}}/${{isEnabled ? "disable" : "enable"}}`, {{ method: "POST" }});
            pushActionEntry({{
              kind: "mission state",
              label: `${{isEnabled ? "Disabled" : "Enabled"}} ${{previousWatch && previousWatch.name ? previousWatch.name : identifier}}`,
              detail: `${{identifier}} switched to ${{isEnabled ? "disabled" : "enabled"}}.`,
              undoLabel: isEnabled ? "Re-enable" : "Disable again",
              undo: async () => {{
                await api(`/api/watches/${{identifier}}/${{isEnabled ? "enable" : "disable"}}`, {{ method: "POST" }});
                await refreshBoard();
                showToast(`Mission ${{isEnabled ? "re-enabled" : "disabled"}}: ${{identifier}}`, "success");
              }},
            }});
            await refreshBoard();
          }} catch (error) {{
            if (previousWatch) {{
              previousWatch.enabled = isEnabled;
            }}
            if (previousDetail) {{
              state.watchDetails[identifier] = previousDetail;
            }}
            renderWatches();
            renderWatchDetail();
            reportError(error, `${{isEnabled ? "Disable" : "Enable"}} mission`);
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      root.querySelectorAll("[data-delete-watch]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          const identifier = String(button.dataset.deleteWatch || "").trim();
          const removedWatch = state.watches.find((watch) => watch.id === identifier);
          const removedDetail = state.watchDetails[identifier] ? {{ ...state.watchDetails[identifier] }} : null;
          button.disabled = true;
          state.watches = state.watches.filter((watch) => watch.id !== identifier);
          delete state.watchDetails[identifier];
          if (state.selectedWatchId === identifier) {{
            state.selectedWatchId = state.watches[0] ? state.watches[0].id : "";
          }}
          renderWatches();
          renderWatchDetail();
          try {{
            await api(`/api/watches/${{identifier}}`, {{ method: "DELETE" }});
            pushActionEntry({{
              kind: "mission delete",
              label: `Deleted ${{removedWatch && removedWatch.name ? removedWatch.name : identifier}}`,
              detail: "Deletion is reversible from the recent action log.",
              undoLabel: "Restore",
              undo: async () => {{
                if (!removedWatch) {{
                  return;
                }}
                const payload = {{
                  name: String(removedWatch.name || identifier),
                  query: String(removedWatch.query || ""),
                  schedule: String(removedWatch.schedule || removedWatch.schedule_label || "manual"),
                  platforms: Array.isArray(removedWatch.platforms) ? removedWatch.platforms : [],
                  alert_rules: removedDetail && Array.isArray(removedDetail.alert_rules) ? removedDetail.alert_rules : [],
                }};
                await api("/api/watches", {{ method: "POST", headers: jsonHeaders, body: JSON.stringify(payload) }});
                await refreshBoard();
                showToast(`Mission restored: ${{payload.name}}`, "success");
              }},
            }});
            await refreshBoard();
          }} catch (error) {{
            if (removedWatch) {{
              state.watches = [removedWatch, ...state.watches];
            }}
            if (removedDetail) {{
              state.watchDetails[identifier] = removedDetail;
            }}
            reportError(error, "Delete mission");
            await refreshBoard();
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});
    }}

    async function loadWatch(identifier) {{
      state.selectedWatchId = identifier;
      state.loading.watchDetail = true;
      renderWatches();
      renderWatchDetail();
      try {{
        state.watchDetails[identifier] = await api(`/api/watches/${{identifier}}`);
      }} finally {{
        state.loading.watchDetail = false;
      }}
      renderWatches();
      renderWatchDetail();
    }}

    function renderWatchDetail() {{
      const root = $("watch-detail");
      renderFormSuggestionLists();
      const selected = state.selectedWatchId;
      if (state.loading.watchDetail && selected) {{
        root.innerHTML = [skeletonCard(4), skeletonCard(4), skeletonCard(4)].join("");
        return;
      }}
      const watch = state.watchDetails[selected] || state.watches.find((candidate) => candidate.id === selected);
      if (!watch) {{
        root.innerHTML = `<div class="empty">${{copy("Select one mission from the board to inspect schedule, run history, and alert output.", "从看板中选择一个任务，以查看调度、执行历史和告警输出。")}}</div>`;
        return;
      }}
      const recentRuns = Array.isArray(watch.runs) ? watch.runs : [];
      const recentResults = Array.isArray(watch.recent_results) ? watch.recent_results : [];
      const recentAlerts = Array.isArray(watch.recent_alerts) ? watch.recent_alerts : [];
      const lastFailure = watch.last_failure || null;
      const retryAdvice = watch.retry_advice || null;
      const runStats = watch.run_stats || {{}};
      const resultStats = watch.result_stats || {{}};
      const deliveryStats = watch.delivery_stats || {{}};
      const resultFilters = watch.result_filters || {{}};
      const timelineEvents = Array.isArray(watch.timeline_strip) ? watch.timeline_strip : [];
      const stateOptions = Array.isArray(resultFilters.states) ? resultFilters.states : [];
      const sourceOptions = Array.isArray(resultFilters.sources) ? resultFilters.sources : [];
      const domainOptions = Array.isArray(resultFilters.domains) ? resultFilters.domains : [];
      const savedFilters = state.watchResultFilters[watch.id] || {{}};
      const normalizeFilterValue = (key, options) => {{
        const raw = String(savedFilters[key] || "all");
        return raw === "all" || options.some((option) => option.key === raw) ? raw : "all";
      }};
      const activeFilters = {{
        state: normalizeFilterValue("state", stateOptions),
        source: normalizeFilterValue("source", sourceOptions),
        domain: normalizeFilterValue("domain", domainOptions),
      }};
      state.watchResultFilters[watch.id] = activeFilters;
      const runsBlock = recentRuns.length
        ? recentRuns.map((run) => `
            <div class="card">
              <div class="card-top">
                <div>
                  <h3 class="card-title">${{run.status || "success"}}</h3>
                  <div class="meta">
                    <span>${{run.id || "-"}}</span>
                    <span>${{copy("trigger", "触发方式")}}=${{localizeWord(run.trigger || "manual")}}</span>
                    <span>${{copy("items", "条目")}}=${{run.item_count || 0}}</span>
                  </div>
                </div>
                <span class="chip ${{run.status === "success" ? "ok" : "hot"}}">${{localizeWord(run.status || "unknown")}}</span>
              </div>
              <div class="meta">
                <span>${{copy("started", "开始")}}=${{run.started_at || "-"}}</span>
                <span>${{copy("finished", "结束")}}=${{run.finished_at || "-"}}</span>
              </div>
              <div class="panel-sub">${{run.error || copy("No recorded error.", "没有记录到错误。")}}</div>
            </div>
          `).join("")
        : `<div class="empty">${{copy("No mission run recorded yet.", "当前还没有任务执行记录。")}}</div>`;
      const alertsBlock = recentAlerts.length
        ? recentAlerts.map((alert) => `
            <div class="card">
              <div class="card-top">
                <div>
                  <h3 class="card-title">${{alert.rule_name}}</h3>
                  <div class="meta">
                    <span>${{alert.created_at || "-"}}</span>
                    <span>${{copy("items", "条目")}}=${{(alert.item_ids || []).length}}</span>
                  </div>
                </div>
                <span class="chip ${{alert.extra && alert.extra.delivery_errors ? "hot" : "ok"}}">${{(alert.delivered_channels || ["json"]).join(",")}}</span>
              </div>
              <div class="panel-sub">${{alert.summary || copy("No alert summary captured.", "没有记录到告警摘要。")}}</div>
            </div>
          `).join("")
        : `<div class="empty">${{copy("No recent alert event for this mission.", "这个任务近期没有告警事件。")}}</div>`;
      const filteredResults = recentResults.filter((item) => {{
        const filters = item.watch_filters || {{}};
        if (activeFilters.state !== "all" && (filters.state || "new") !== activeFilters.state) {{
          return false;
        }}
        if (activeFilters.source !== "all" && (filters.source || "unknown") !== activeFilters.source) {{
          return false;
        }}
        if (activeFilters.domain !== "all" && (filters.domain || "unknown") !== activeFilters.domain) {{
          return false;
        }}
        return true;
      }});
      const filterGroups = [
        {{ key: "state", label: copy("state", "状态"), options: stateOptions }},
        {{ key: "source", label: copy("source", "来源"), options: sourceOptions }},
        {{ key: "domain", label: copy("domain", "域名"), options: domainOptions }},
      ];
      const filterWindowCount = Number(resultFilters.window_count || recentResults.length || 0);
      const filterBlock = filterGroups.map((group) => `
          <div class="stack">
            <div class="panel-sub">${{group.label}}</div>
            <div class="chip-row">
              <button class="chip-btn ${{activeFilters[group.key] === "all" ? "active" : ""}}" type="button" data-filter-group="${{group.key}}" data-filter-value="all">${{copy("all", "全部")}} (${{filterWindowCount}})</button>
              ${{group.options.map((option) => `
                <button class="chip-btn ${{activeFilters[group.key] === option.key ? "active" : ""}}" type="button" data-filter-group="${{group.key}}" data-filter-value="${{escapeHtml(option.key)}}">${{escapeHtml(localizeWord(option.label))}} (${{option.count || 0}})</button>
              `).join("")}}
            </div>
          </div>
        `).join("");
      const resultsBlock = filteredResults.length
        ? filteredResults.map((item) => `
            <div class="card">
              <div class="card-top">
                <div>
                  <h3 class="card-title">${{item.title}}</h3>
                  <div class="meta">
                    <span>${{item.id}}</span>
                    <span>${{copy("score", "分数")}}=${{item.score || 0}}</span>
                    <span>${{copy("confidence", "置信度")}}=${{Number(item.confidence || 0).toFixed(2)}}</span>
                    <span>${{item.source_name || item.source_type || "-"}}</span>
                  </div>
                </div>
                <span class="chip">${{localizeWord(item.review_state || "new")}}</span>
              </div>
              <div class="panel-sub">${{item.url || "-"}}</div>
            </div>
          `).join("")
        : `<div class="empty">${{copy("No persisted result matched the active filter chips in the current mission window.", "当前任务窗口内没有结果匹配所选筛选条件。")}}</div>`;
      const timelineBlock = timelineEvents.length
        ? `<div class="timeline-strip">${{timelineEvents.map((event) => `
            <div class="timeline-event ${{event.tone || ""}}">
              <div class="card-top">
                <span class="chip ${{event.tone || ""}}">${{event.kind || "event"}}</span>
                <span class="panel-sub">${{event.time || "-"}}</span>
              </div>
              <div class="mono">${{event.label || "-"}}</div>
              <div class="panel-sub">${{event.detail || "-"}}</div>
            </div>
          `).join("")}}</div>`
        : `<div class="empty">${{copy("No mission timeline event captured yet.", "当前还没有记录到任务时间线事件。")}}</div>`;
      const retryCollectors = retryAdvice && Array.isArray(retryAdvice.suspected_collectors)
        ? retryAdvice.suspected_collectors
        : [];
      const retryNotes = retryAdvice && Array.isArray(retryAdvice.notes) ? retryAdvice.notes : [];
      const failureBlock = lastFailure
        ? `
            <div class="card">
              <div class="card-top">
                <div>
                  <h3 class="card-title">${{copy("latest failure", "最近失败")}}</h3>
                  <div class="meta">
                    <span>${{lastFailure.id || "-"}}</span>
                    <span>${{copy("status", "状态")}}=${{localizeWord(lastFailure.status || "error")}}</span>
                    <span>${{copy("trigger", "触发方式")}}=${{localizeWord(lastFailure.trigger || "manual")}}</span>
                    <span>${{copy("finished", "结束")}}=${{lastFailure.finished_at || "-"}}</span>
                  </div>
                </div>
                <span class="chip hot">${{retryAdvice && retryAdvice.failure_class ? retryAdvice.failure_class : localizeWord("error")}}</span>
              </div>
              <div class="panel-sub">${{lastFailure.error || copy("No failure message captured.", "没有记录到失败信息。")}}</div>
            </div>
          `
        : "";
      const retryAdviceBlock = retryAdvice
        ? `
            <div class="card">
              <div class="mono">${{copy("retry advice", "重试建议")}}</div>
              <div class="meta">
                <span>${{copy("retry", "重试")}}=${{retryAdvice.retry_command || "-"}}</span>
                <span>${{copy("daemon", "守护进程")}}=${{retryAdvice.daemon_retry_command || "-"}}</span>
              </div>
              <div class="panel-sub">${{retryAdvice.summary || copy("No retry guidance recorded.", "没有记录到重试建议。")}}</div>
              ${{
                retryCollectors.length
                  ? `<div class="stack" style="margin-top:12px;">${{retryCollectors.map((collector) => `
                      <div class="mini-item">${{collector.name}} | ${{collector.tier || "-"}} | ${{collector.status || "-"}} | available=${{collector.available}} | ${{collector.setup_hint || collector.message || "-"}}</div>
                    `).join("")}}</div>`
                  : ""
              }}
              ${{
                retryNotes.length
                  ? `<div class="stack" style="margin-top:12px;">${{retryNotes.map((note) => `<div class="mini-item">${{note}}</div>`).join("")}}</div>`
                  : ""
              }}
            </div>
          `
        : "";

      root.innerHTML = `
        <div class="card">
          <div class="card-top">
            <div>
                <h3 class="card-title">${{watch.name}}</h3>
                <div class="meta">
                  <span>${{watch.id}}</span>
                  <span>${{copy("schedule", "频率")}}=${{watch.schedule_label || watch.schedule || copy("manual", "手动")}}</span>
                  <span>${{copy("next", "下次")}}=${{watch.next_run_at || "-"}}</span>
                  <span>${{copy("query", "查询")}}=${{watch.query || "-"}}</span>
                </div>
              </div>
            <span class="chip ${{watch.enabled ? "ok" : "hot"}}">${{watch.enabled ? copy("enabled", "已启用") : copy("disabled", "已停用")}}</span>
          </div>
          <div class="meta">
            <span>${{copy("due", "到点")}}=${{localizeBoolean(watch.is_due)}}</span>
            <span>${{copy("alert_rules", "告警规则")}}=${{watch.alert_rule_count || 0}}</span>
            <span>${{copy("runs", "执行")}}=${{runStats.total || 0}}</span>
            <span>${{copy("success", "成功")}}=${{runStats.success || 0}}</span>
            <span>${{copy("errors", "错误")}}=${{runStats.error || 0}}</span>
            <span>${{copy("results", "结果")}}=${{resultStats.stored_result_count || 0}}</span>
            <span>${{copy("alerts", "告警")}}=${{deliveryStats.recent_alert_count || 0}}</span>
          </div>
          <div class="actions" style="margin-top:12px;">
            <button class="btn-secondary" type="button" data-watch-edit="${{watch.id}}">${{copy("Edit Mission", "编辑任务")}}</button>
          </div>
          <div class="panel-sub">${{watch.last_run_error || copy("Mission history and recent delivery outcomes are visible below.", "下方可查看任务历史和最近交付结果。")}}</div>
        </div>
        ${{failureBlock}}
        ${{retryAdviceBlock}}
        <div class="card">
          <div class="mono">${{copy("timeline strip", "时间线")}}</div>
          <div class="panel-sub">${{copy("Recent run, result, and alert events are merged into one server-backed mission timeline.", "最近的运行、结果和告警事件会合并成一条服务端驱动的任务时间线。")}}</div>
          <div style="margin-top:12px;">
            ${{timelineBlock}}
          </div>
        </div>
        <div class="story-columns">
          <div class="stack">
            <div class="mono">${{copy("recent runs", "最近执行")}}</div>
            ${{runsBlock}}
          </div>
          <div class="stack">
            <div class="mono">${{copy("recent alerts", "最近告警")}}</div>
            ${{alertsBlock}}
          </div>
        </div>
        <div class="stack">
          <div class="mono">${{copy("result stream", "结果流")}}</div>
          <div class="card">
            <div class="mono">${{copy("filter chips", "筛选标签")}}</div>
            <div class="panel-sub">${{copy("Filter the current persisted result window by review state, source, or domain without leaving the cockpit.", "在不离开驾驶舱的情况下，按审核状态、来源或域名筛选当前结果窗口。")}}</div>
            <div class="stack" style="margin-top:12px;">
              ${{filterBlock}}
            </div>
          </div>
          ${{resultsBlock}}
        </div>
        <div class="card">
          <div class="card-top">
            <div>
              <div class="mono">${{copy("alert rule editor", "告警规则编辑器")}}</div>
              <div class="panel-sub">${{copy("Edit multiple console threshold rules for this mission, then replace the saved rule set in one write.", "可以在这里为任务编辑多条阈值规则，并一次性替换已保存的规则集。")}}</div>
            </div>
            <span class="chip">${{(watch.alert_rules || []).length}} ${{copy("rule(s)", "条规则")}}</span>
          </div>
          <form id="watch-alert-form" data-watch-id="${{watch.id}}">
            <div class="stack" id="watch-alert-rules">
              ${{
                ((watch.alert_rules || []).length ? watch.alert_rules : [{{}}]).map((rule, index) => `
                  <div class="card" data-alert-rule-card="${{index}}">
                    <div class="card-top">
                      <div>
                        <div class="mono">${{copy("rule", "规则")}} ${{index + 1}}</div>
                        <div class="panel-sub">${{copy("Current name", "当前名称")}}: ${{rule.name || "console-threshold"}}</div>
                      </div>
                      <button class="btn-secondary" type="button" data-remove-alert-rule="${{index}}">${{copy("Remove", "移除")}}</button>
                    </div>
                    <div class="field-grid">
                      <label>${{copy("Alert Route", "告警路由")}}<input name="route" list="route-options-list" placeholder="ops-webhook" value="${{(rule.routes || [])[0] || ""}}"></label>
                      <label>${{copy("Alert Keyword", "告警关键词")}}<input name="keyword" list="keyword-options-list" placeholder="launch" value="${{(rule.keyword_any || [])[0] || ""}}"></label>
                    </div>
                    <div class="field-grid">
                      <label>${{copy("Alert Domain", "告警域名")}}<input name="domain" list="domain-options-list" placeholder="openai.com" value="${{(rule.domains || [])[0] || ""}}"></label>
                      <label>${{copy("Min Score", "最低分数")}}<input name="min_score" list="score-options-list" placeholder="70" inputmode="numeric" value="${{(rule.min_score || 0) || ""}}"></label>
                    </div>
                    <div class="field-grid">
                      <label>${{copy("Min Confidence", "最低置信度")}}<input name="min_confidence" list="confidence-options-list" placeholder="0.8" inputmode="decimal" value="${{(rule.min_confidence || 0) || ""}}"></label>
                      <div class="stack">
                        <div class="panel-sub">${{copy("Channels are still pinned to json; named route delivery is configured via Alert Route.", "通道仍固定为 json；命名路由交付通过“告警路由”配置。")}}</div>
                      </div>
                    </div>
                  </div>
                `).join("")
              }}
            </div>
            <div class="toolbar">
              <button class="btn-secondary" id="watch-alert-add" type="button">${{copy("Add Alert Rule", "新增告警规则")}}</button>
              <button class="btn-primary" type="submit">${{copy("Save Alert Rules", "保存告警规则")}}</button>
              <button class="btn-secondary" id="watch-alert-clear" type="button">${{copy("Clear Alert Rules", "清空告警规则")}}</button>
            </div>
          </form>
        </div>
      `;

      root.querySelectorAll("[data-filter-group]").forEach((button) => {{
        button.addEventListener("click", () => {{
          const filterGroup = String(button.dataset.filterGroup || "").trim();
          if (!filterGroup) {{
            return;
          }}
          const current = state.watchResultFilters[watch.id] || {{ state: "all", source: "all", domain: "all" }};
          current[filterGroup] = String(button.dataset.filterValue || "all");
          state.watchResultFilters[watch.id] = current;
          renderWatchDetail();
        }});
      }});

      const alertForm = document.getElementById("watch-alert-form");
      const addRuleButton = document.getElementById("watch-alert-add");
      if (addRuleButton) {{
        addRuleButton.addEventListener("click", () => {{
          const rulesRoot = document.getElementById("watch-alert-rules");
          if (!rulesRoot) {{
            return;
          }}
          const nextIndex = rulesRoot.querySelectorAll("[data-alert-rule-card]").length;
          rulesRoot.insertAdjacentHTML("beforeend", `
            <div class="card" data-alert-rule-card="${{nextIndex}}">
              <div class="card-top">
                <div>
                  <div class="mono">${{copy("rule", "规则")}} ${{nextIndex + 1}}</div>
                  <div class="panel-sub">${{copy("New console threshold rule.", "新的控制台阈值规则。")}}</div>
                </div>
                <button class="btn-secondary" type="button" data-remove-alert-rule="${{nextIndex}}">${{copy("Remove", "移除")}}</button>
              </div>
              <div class="field-grid">
                <label>${{copy("Alert Route", "告警路由")}}<input name="route" list="route-options-list" placeholder="ops-webhook"></label>
                <label>${{copy("Alert Keyword", "告警关键词")}}<input name="keyword" list="keyword-options-list" placeholder="launch"></label>
              </div>
              <div class="field-grid">
                <label>${{copy("Alert Domain", "告警域名")}}<input name="domain" list="domain-options-list" placeholder="openai.com"></label>
                <label>${{copy("Min Score", "最低分数")}}<input name="min_score" list="score-options-list" placeholder="70" inputmode="numeric"></label>
              </div>
              <div class="field-grid">
                <label>${{copy("Min Confidence", "最低置信度")}}<input name="min_confidence" list="confidence-options-list" placeholder="0.8" inputmode="decimal"></label>
                <div class="stack">
                  <div class="panel-sub">${{copy("Channels stay pinned to json; named route delivery is configured via Alert Route.", "通道仍固定为 json；命名路由交付通过“告警路由”配置。")}}</div>
                </div>
              </div>
            </div>
          `);
          rulesRoot.querySelectorAll("[data-remove-alert-rule]").forEach((button) => {{
            button.onclick = () => {{
              button.closest("[data-alert-rule-card]")?.remove();
            }};
          }});
        }});
      }}
      root.querySelectorAll("[data-remove-alert-rule]").forEach((button) => {{
        button.onclick = () => {{
          button.closest("[data-alert-rule-card]")?.remove();
        }};
      }});
      if (alertForm) {{
        alertForm.addEventListener("submit", async (event) => {{
          event.preventDefault();
          const cards = Array.from(document.querySelectorAll("[data-alert-rule-card]"));
          const alertRules = cards.flatMap((card) => {{
            return buildAlertRules({{
              route: String(card.querySelector('[name=\"route\"]')?.value || "").trim(),
              keyword: String(card.querySelector('[name=\"keyword\"]')?.value || "").trim(),
              domain: String(card.querySelector('[name=\"domain\"]')?.value || "").trim(),
              minScore: Number(card.querySelector('[name=\"min_score\"]')?.value || 0),
              minConfidence: Number(card.querySelector('[name=\"min_confidence\"]')?.value || 0),
            }});
          }});
          const payload = {{
            alert_rules: alertRules,
          }};
          if (!payload.alert_rules.length) {{
            showToast(copy("Provide at least one route, keyword, domain, or threshold across the rule set.", "请至少提供一个路由、关键词、域名或阈值。"), "error");
            return;
          }}
          try {{
            await api(`/api/watches/${{watch.id}}/alert-rules`, {{
              method: "PUT",
              headers: jsonHeaders,
              body: JSON.stringify(payload),
            }});
            await refreshBoard();
          }} catch (error) {{
            reportError(error, copy("Update alert rules", "更新告警规则"));
          }}
        }});
      }}

      const clearButton = document.getElementById("watch-alert-clear");
      if (clearButton) {{
        clearButton.addEventListener("click", async () => {{
          try {{
            await api(`/api/watches/${{watch.id}}/alert-rules`, {{
              method: "PUT",
              headers: jsonHeaders,
              body: JSON.stringify({{ alert_rules: [] }}),
            }});
            await refreshBoard();
          }} catch (error) {{
            reportError(error, copy("Clear alert rules", "清空告警规则"));
          }}
        }});
      }}

      root.querySelectorAll("[data-watch-edit]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await editMissionInCreateWatch(String(button.dataset.watchEdit || "").trim());
          }} catch (error) {{
            reportError(error, copy("Edit mission", "编辑任务"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});
    }}

    function renderAlerts() {{
      const root = $("alert-list");
      if (state.loading.board && !state.alerts.length) {{
        root.innerHTML = [skeletonCard(3), skeletonCard(3)].join("");
        return;
      }}
      if (!state.alerts.length) {{
        root.innerHTML = `<div class="empty">${{copy("No alert event stored.", "当前没有告警事件。")}}</div>`;
        return;
      }}
      root.innerHTML = state.alerts.map((alert) => `
        <div class="card">
          <div class="card-top">
            <div>
              <h3 class="card-title">${{alert.mission_name}}</h3>
              <div class="meta">
                <span>${{alert.rule_name}}</span>
                <span>${{alert.created_at || "-"}}</span>
              </div>
            </div>
            <span class="chip hot">${{(alert.delivered_channels || ["json"]).join(",")}}</span>
          </div>
          <div class="panel-sub">${{alert.summary || ""}}</div>
        </div>
      `).join("");
    }}

    async function submitRouteDeck(form) {{
      const draft = collectRouteDraft(form);
      state.routeDraft = draft;
      const editingId = normalizeRouteName(state.routeEditingId);
      let headers = null;
      try {{
        headers = parseRouteHeaders(draft.headers_json);
      }} catch (error) {{
        showToast(error.message, "error");
        focusRouteDeck("headers_json");
        return;
      }}
      if (!draft.name.trim()) {{
        showToast(copy("Provide a route name before saving.", "保存前请先填写路由名称。"), "error");
        focusRouteDeck("name");
        return;
      }}
      if (draft.channel === "webhook" && !draft.webhook_url.trim()) {{
        showToast(copy("Webhook routes need a webhook URL.", "Webhook 路由需要填写 webhook URL。"), "error");
        focusRouteDeck("webhook_url");
        return;
      }}
      if (draft.channel === "feishu" && !draft.feishu_webhook.trim()) {{
        showToast(copy("Feishu routes need a webhook URL.", "飞书路由需要填写 webhook URL。"), "error");
        focusRouteDeck("feishu_webhook");
        return;
      }}
      if (draft.channel === "telegram" && !draft.telegram_chat_id.trim()) {{
        showToast(copy("Telegram routes need a chat ID.", "Telegram 路由需要填写 chat ID。"), "error");
        focusRouteDeck("telegram_chat_id");
        return;
      }}
      if (draft.channel === "telegram" && !editingId && !draft.telegram_bot_token.trim()) {{
        showToast(copy("Telegram routes need a bot token when created.", "创建 Telegram 路由时必须填写 bot token。"), "error");
        focusRouteDeck("telegram_bot_token");
        return;
      }}
      let timeoutSeconds = null;
      if (draft.timeout_seconds.trim()) {{
        timeoutSeconds = Number(draft.timeout_seconds);
        if (!(timeoutSeconds > 0)) {{
          showToast(copy("Timeout must be greater than 0.", "超时时间必须大于 0。"), "error");
          focusRouteDeck("timeout_seconds");
          return;
        }}
      }}

      const payload = {{
        channel: draft.channel,
      }};
      if (draft.description.trim()) {{
        payload.description = draft.description.trim();
      }}
      if (timeoutSeconds !== null) {{
        payload.timeout_seconds = timeoutSeconds;
      }}
      if (draft.channel === "webhook") {{
        payload.webhook_url = draft.webhook_url.trim();
        if (draft.authorization.trim()) {{
          payload.authorization = draft.authorization.trim();
        }}
        if (headers && Object.keys(headers).length) {{
          payload.headers = headers;
        }}
      }}
      if (draft.channel === "feishu") {{
        payload.feishu_webhook = draft.feishu_webhook.trim();
      }}
      if (draft.channel === "telegram") {{
        payload.telegram_chat_id = draft.telegram_chat_id.trim();
        if (draft.telegram_bot_token.trim()) {{
          payload.telegram_bot_token = draft.telegram_bot_token.trim();
        }}
      }}

      const submitButton = form?.querySelector("button[type='submit']");
      if (submitButton) {{
        submitButton.disabled = true;
      }}
      try {{
        if (editingId) {{
          const updated = await api(`/api/alert-routes/${{editingId}}`, {{
            method: "PUT",
            headers: jsonHeaders,
            body: JSON.stringify(payload),
          }});
          state.routeAdvancedOpen = null;
          setRouteDraft(defaultRouteDraft(), "");
          pushActionEntry({{
            kind: copy("route update", "路由修改"),
            label: state.language === "zh" ? `已更新路由：${{updated.name}}` : `Updated route: ${{updated.name}}`,
            detail: state.language === "zh"
              ? `通道：${{routeChannelLabel(updated.channel)}}`
              : `Channel: ${{routeChannelLabel(updated.channel)}}`,
          }});
          await refreshBoard();
          showToast(
            state.language === "zh" ? `路由已更新：${{updated.name}}` : `Route updated: ${{updated.name}}`,
            "success",
          );
          return;
        }}
        const created = await api("/api/alert-routes", {{
          method: "POST",
          headers: jsonHeaders,
          body: JSON.stringify({{ name: draft.name.trim(), ...payload }}),
        }});
        const nextChannel = draft.channel;
        state.routeAdvancedOpen = null;
        setRouteDraft({{ ...defaultRouteDraft(), channel: nextChannel }}, "");
        pushActionEntry({{
          kind: copy("route create", "路由创建"),
          label: state.language === "zh" ? `已创建路由：${{created.name}}` : `Created route: ${{created.name}}`,
          detail: copy("The route is now available in mission alert rules and route quick-picks.", "该路由现在已可用于任务告警规则和快捷选择。"),
          undoLabel: copy("Delete route", "删除路由"),
          undo: async () => {{
            await api(`/api/alert-routes/${{created.name}}`, {{ method: "DELETE" }});
            await refreshBoard();
            showToast(
              state.language === "zh" ? `已删除路由：${{created.name}}` : `Route deleted: ${{created.name}}`,
              "success",
            );
          }},
        }});
        await refreshBoard();
        showToast(
          state.language === "zh" ? `路由已创建：${{created.name}}` : `Route created: ${{created.name}}`,
          "success",
        );
      }} catch (error) {{
        reportError(error, copy("Save route", "保存路由"));
      }} finally {{
        if (submitButton) {{
          submitButton.disabled = false;
        }}
      }}
    }}

    async function deleteRouteFromBoard(identifier) {{
      const normalized = normalizeRouteName(identifier);
      if (!normalized) {{
        return;
      }}
      const usageNames = getRouteUsageNames(normalized);
      const confirmation = usageNames.length
        ? copy(
            `Delete route ${{normalized}}? It is referenced by ${{usageNames.length}} mission(s): ${{usageNames.slice(0, 3).join(", ")}}.`,
            `确认删除路由 ${{normalized}}？它仍被 ${{usageNames.length}} 个任务引用：${{usageNames.slice(0, 3).join("、")}}。`,
          )
        : copy(
            `Delete route ${{normalized}}?`,
            `确认删除路由 ${{normalized}}？`,
          );
      if (!window.confirm(confirmation)) {{
        return;
      }}
      try {{
        const deleted = await api(`/api/alert-routes/${{normalized}}`, {{ method: "DELETE" }});
        if (normalizeRouteName(state.routeEditingId) === normalized) {{
          state.routeAdvancedOpen = null;
          setRouteDraft(defaultRouteDraft(), "");
        }}
        const createDraftRoute = normalizeRouteName(state.createWatchDraft?.route);
        if (createDraftRoute === normalized) {{
          updateCreateWatchDraft({{ route: "" }});
        }}
        pushActionEntry({{
          kind: copy("route delete", "路由删除"),
          label: state.language === "zh" ? `已删除路由：${{deleted.name}}` : `Deleted route: ${{deleted.name}}`,
          detail: usageNames.length
            ? copy("This route was still referenced by one or more missions. Review mission alert rules before the next run.", "该路由此前仍被任务引用，请在下一次执行前检查相关任务的告警规则。")
            : copy("Unused route removed from the delivery surface.", "未使用路由已从交付面移除。"),
        }});
        await refreshBoard();
        showToast(
          state.language === "zh" ? `路由已删除：${{deleted.name}}` : `Route deleted: ${{deleted.name}}`,
          "success",
        );
      }} catch (error) {{
        reportError(error, copy("Delete route", "删除路由"));
      }}
    }}

    function renderRouteDeck() {{
      const root = $("route-deck");
      if (!root) {{
        return;
      }}
      const draft = normalizeRouteDraft(state.routeDraft || defaultRouteDraft());
      const editingId = normalizeRouteName(state.routeEditingId);
      const editing = Boolean(editingId);
      const advancedOpen = isRouteAdvancedOpen(draft);
      const routeName = normalizeRouteName(editing ? editingId : draft.name);
      const usageCount = routeName ? getRouteUsageCount(routeName) : 0;
      const health = routeName ? getRouteHealthRow(routeName) : null;
      const advancedChips = [];
      if (draft.description.trim()) {{
        advancedChips.push(copy("description added", "已补充说明"));
      }}
      if (draft.authorization.trim()) {{
        advancedChips.push(copy("auth attached", "已附带认证"));
      }}
      if (draft.headers_json.trim()) {{
        advancedChips.push(copy("custom headers", "自定义请求头"));
      }}
      if (draft.timeout_seconds.trim()) {{
        advancedChips.push(phrase("timeout {{value}}s", "超时 {{value}} 秒", {{ value: draft.timeout_seconds.trim() }}));
      }}
      if (!advancedChips.length) {{
        advancedChips.push(copy("No advanced control yet", "当前没有高级设置"));
      }}

      root.innerHTML = `
        <form id="route-form">
          <div class="card-top">
            <div>
              <div class="mono">${{editing ? copy("route edit", "路由编辑") : copy("route create", "路由创建")}}</div>
              <h3 class="card-title" style="margin-top:10px;">${{editing ? escapeHtml(draft.name) : copy("Create Named Route", "创建命名路由")}}</h3>
            </div>
            <div style="display:grid; gap:6px; justify-items:end;">
              <span class="chip ${{health && health.status === "healthy" ? "ok" : health && health.status && health.status !== "idle" ? "hot" : ""}}">${{health ? localizeWord(health.status || "idle") : localizeWord(editing ? "editable" : "new")}}</span>
              <span class="chip">${{copy("used", "已引用")}}=${{usageCount}}</span>
            </div>
          </div>
          <div class="panel-sub">${{
            editing
              ? copy("Update the sink in place. Route name stays fixed so existing mission rules do not drift.", "原位更新交付路由。路由名称保持不变，避免已有任务规则漂移。")
              : copy("Add a reusable sink once, then pick it from mission alert rules and quick route chips.", "先把可复用的交付路由配置好，后续在任务告警规则和快捷路由里直接选择。")
          }}</div>
          <div class="chip-row" style="margin-top:4px;">
            ${{
              routeChannelOptions.map((option) => `
                <button
                  class="chip-btn ${{draft.channel === option.value ? "active" : ""}}"
                  type="button"
                  data-route-channel="${{option.value}}"
                >${{escapeHtml(copy(option.label, option.zhLabel || option.label))}}</button>
              `).join("")
            }}
          </div>
          <div class="field-grid" style="margin-top:2px;">
            <label>${{copy("Route Name", "路由名称")}}<input name="name" placeholder="ops-webhook" value="${{escapeHtml(draft.name)}}" ${{editing ? "readonly" : ""}}><span class="field-hint">${{editing ? copy("Name is fixed during edit so existing mission rules keep resolving.", "编辑时名称固定，避免已有任务规则失效。") : copy("Use a short reusable id, such as ops-webhook or exec-telegram.", "建议使用可复用的简短 ID，例如 ops-webhook 或 exec-telegram。")}}</span></label>
            <label>${{copy("Channel", "通道")}}<input name="channel" value="${{escapeHtml(routeChannelLabel(draft.channel))}}" readonly><span class="field-hint">${{copy("Change channel with the route type chips above.", "通过上方的路由类型按钮切换通道。")}}</span></label>
          </div>
          <div class="field-grid">
            ${{
              draft.channel === "webhook"
                ? `
                    <label>${{copy("Webhook URL", "Webhook URL")}}<input name="webhook_url" placeholder="https://hooks.example.com/ops" value="${{escapeHtml(draft.webhook_url)}}"><span class="field-hint">${{copy("Paste the receiver endpoint once, then reuse the route everywhere else.", "把接收端地址配置一次，后续在其他地方直接复用。")}}</span></label>
                    <label>${{copy("Destination Preview", "目标预览")}}<input value="${{escapeHtml(draft.webhook_url.trim() ? summarizeUrlHost(draft.webhook_url) : copy("Waiting for URL", "等待输入 URL"))}}" readonly><span class="field-hint">${{copy("Only the host preview is shown here to keep scanning fast.", "这里只显示主机预览，方便快速扫描。")}}</span></label>
                  `
                : draft.channel === "feishu"
                  ? `
                    <label>${{copy("Feishu Webhook", "飞书 Webhook")}}<input name="feishu_webhook" placeholder="https://open.feishu.cn/..." value="${{escapeHtml(draft.feishu_webhook)}}"><span class="field-hint">${{copy("Use the bot webhook issued by the target Feishu group.", "填写目标飞书群机器人提供的 webhook。")}}</span></label>
                    <label>${{copy("Destination Preview", "目标预览")}}<input value="${{escapeHtml(draft.feishu_webhook.trim() ? summarizeUrlHost(draft.feishu_webhook) : copy("Waiting for URL", "等待输入 URL"))}}" readonly><span class="field-hint">${{copy("Preview keeps the card readable without exposing the full URL at a glance.", "保留预览而不是完整地址，列表浏览时更轻量。")}}</span></label>
                  `
                  : draft.channel === "telegram"
                    ? `
                      <label>${{copy("Telegram Chat ID", "Telegram Chat ID")}}<input name="telegram_chat_id" placeholder="-1001234567890" value="${{escapeHtml(draft.telegram_chat_id)}}"><span class="field-hint">${{copy("The chat id remains visible so you can confirm the destination quickly.", "保留 chat id 可见，便于快速确认目标会话。")}}</span></label>
                      <label>${{copy("Bot Token", "Bot Token")}}<input name="telegram_bot_token" type="password" placeholder="${{editing ? copy("Leave blank to keep the current token", "留空则保留当前 token") : "123456:ABCDEF"}}" value="${{escapeHtml(draft.telegram_bot_token)}}"><span class="field-hint">${{editing ? copy("Leave blank to keep the existing bot token.", "留空会保留当前 bot token。") : copy("Required when the route is created.", "创建路由时必须填写。")}}</span></label>
                    `
                    : `
                      <label>${{copy("Markdown Delivery", "Markdown 交付")}}<input value="${{copy("Append alert summaries to the local markdown log.", "把告警摘要追加到本地 Markdown 日志。")}}" readonly><span class="field-hint">${{copy("Use this when operators want a file-backed trail with zero external dependency.", "当你需要零外部依赖的文件留痕时，用这个通道。")}}</span></label>
                      <label>${{copy("Destination Preview", "目标预览")}}<input value="${{copy("alerts.md append target", "alerts.md 追加目标")}}" readonly><span class="field-hint">${{copy("Markdown routes need no extra endpoint fields.", "Markdown 路由不需要额外的目标配置字段。")}}</span></label>
                    `
            }}
          </div>
          <div class="deck-mode-strip">
            <div class="deck-mode-head">
              <div>
                <div class="mono">${{copy("advanced controls", "高级设置")}}</div>
                <div class="panel-sub">${{copy("Keep advanced fields closed until you need auth headers, timeout control, or delivery notes.", "只有在需要认证、超时控制或交付备注时，再展开高级设置。")}}</div>
              </div>
              <button class="btn-secondary advanced-toggle" id="route-advanced-toggle" type="button" aria-expanded="${{String(advancedOpen)}}">${{advancedOpen ? copy("Hide Advanced", "收起高级设置") : copy("Show Advanced", "展开高级设置")}}</button>
            </div>
            <div class="chip-row advanced-summary">${{advancedChips.map((chip) => `<span class="chip">${{escapeHtml(chip)}}</span>`).join("")}}</div>
            <div class="deck-advanced-panel ${{advancedOpen ? "" : "collapsed"}}" aria-hidden="${{String(!advancedOpen)}}">
              <div class="field-grid">
                <label>${{copy("Description", "说明")}}<input name="description" placeholder="${{copy("Primary route for on-call ops", "值班运维主路由")}}" value="${{escapeHtml(draft.description)}}"><span class="field-hint">${{copy("Use one short note so operators know why this sink exists.", "补一句简短说明，让操作者知道这个路由的用途。")}}</span></label>
                <label>${{copy("Timeout Seconds", "超时秒数")}}<input name="timeout_seconds" inputmode="decimal" placeholder="10" value="${{escapeHtml(draft.timeout_seconds)}}"><span class="field-hint">${{copy("Optional override for slower receivers.", "当接收端偏慢时，可以单独覆盖超时时间。")}}</span></label>
              </div>
              ${{
                draft.channel === "webhook"
                  ? `
                      <div class="field-grid">
                        <label>${{copy("Authorization Header", "Authorization 请求头")}}<input name="authorization" type="password" placeholder="${{editing ? copy("Leave blank to keep current auth", "留空则保留当前认证") : "Bearer ..."}}" value="${{escapeHtml(draft.authorization)}}"><span class="field-hint">${{editing ? copy("Leave blank to keep the current secret.", "留空会保留当前密钥。") : copy("Optional bearer token or pre-shared auth header.", "可选的 bearer token 或预共享认证头。")}}</span></label>
                        <label>${{copy("Custom Headers JSON", "自定义请求头 JSON")}}<textarea name="headers_json" rows="4" placeholder='{{"X-Env":"prod"}}'>${{escapeHtml(draft.headers_json)}}</textarea><span class="field-hint">${{copy("Only include extra headers that are not already captured above.", "这里只填写上方未覆盖的额外请求头。")}}</span></label>
                      </div>
                    `
                  : ""
              }}
            </div>
          </div>
          <div class="toolbar">
            <button class="btn-primary" id="route-submit" type="submit">${{editing ? copy("Save Route", "保存路由") : copy("Create Route", "创建路由")}}</button>
            <button class="btn-secondary" id="route-clear" type="button">${{editing ? copy("Cancel Edit", "取消编辑") : copy("Reset Draft", "清空草稿")}}</button>
            ${{
              editing
                ? `<button class="btn-secondary" id="route-apply" type="button">${{copy("Use In Mission", "用于任务草稿")}}</button>`
                : ""
            }}
          </div>
        </form>
      `;

      const form = $("route-form");
      form?.addEventListener("input", () => {{
        state.routeDraft = collectRouteDraft(form);
      }});
      form?.addEventListener("submit", async (event) => {{
        event.preventDefault();
        await submitRouteDeck(form);
      }});
      $("route-advanced-toggle")?.addEventListener("click", () => {{
        state.routeDraft = collectRouteDraft(form);
        state.routeAdvancedOpen = !isRouteAdvancedOpen(state.routeDraft || defaultRouteDraft());
        renderRouteDeck();
      }});
      root.querySelectorAll("[data-route-channel]").forEach((button) => {{
        button.addEventListener("click", () => {{
          const nextChannel = String(button.dataset.routeChannel || "webhook").trim().toLowerCase();
          state.routeDraft = {{
            ...collectRouteDraft(form),
            channel: nextChannel,
          }};
          if (nextChannel !== "markdown") {{
            state.routeAdvancedOpen = true;
          }}
          renderRouteDeck();
        }});
      }});
      $("route-clear")?.addEventListener("click", () => {{
        const wasEditing = Boolean(normalizeRouteName(state.routeEditingId));
        state.routeAdvancedOpen = null;
        setRouteDraft(defaultRouteDraft(), "");
        showToast(
          wasEditing
            ? copy("Route edit cancelled", "已取消路由编辑")
            : copy("Route draft cleared", "已清空路由草稿"),
          "success",
        );
      }});
      $("route-apply")?.addEventListener("click", async () => {{
        await applyRouteToMissionDraft(draft.name);
      }});
    }}

    function renderRouteHealth() {{
      const root = $("route-health");
      if (state.loading.board && !state.routeHealth.length) {{
        root.innerHTML = [skeletonCard(4), skeletonCard(4)].join("");
        return;
      }}
      if (!state.routeHealth.length) {{
        root.innerHTML = `<div class="empty">${{copy("No route health signal yet. Trigger named-route alerts to populate delivery quality.", "当前还没有路由健康信号。触发命名路由告警后会出现交付质量数据。")}}</div>`;
        return;
      }}
      root.innerHTML = state.routeHealth.map((route) => `
        <div class="card">
          <div class="card-top">
            <div>
              <h3 class="card-title">${{route.name}}</h3>
              <div class="meta">
                <span>${{copy("channel", "通道")}}=${{routeChannelLabel(route.channel || "unknown")}}</span>
                <span>${{copy("status", "状态")}}=${{localizeWord(route.status || "idle")}}</span>
                <span>${{copy("rate", "成功率")}}=${{formatRate(route.success_rate)}}</span>
              </div>
            </div>
            <span class="chip ${{route.status === "healthy" ? "ok" : route.status === "idle" ? "" : "hot"}}">${{localizeWord(route.status || "idle")}}</span>
          </div>
          <div class="meta">
            <span>${{copy("events", "事件")}}=${{route.event_count || 0}}</span>
            <span>${{copy("delivered", "送达")}}=${{route.delivered_count || 0}}</span>
            <span>${{copy("failed", "失败")}}=${{route.failure_count || 0}}</span>
            <span>${{copy("last", "最近")}}=${{route.last_event_at || "-"}}</span>
          </div>
          <div class="panel-sub">${{route.last_error || route.last_summary || copy("No recent route delivery attempt recorded.", "近期没有记录到路由投递尝试。")}}</div>
        </div>
      `).join("");
    }}

    function renderRoutes() {{
      const root = $("route-list");
      renderRouteDeck();
      if (state.loading.board && !state.routes.length) {{
        root.innerHTML = skeletonCard(3);
        return;
      }}
      const searchValue = String(state.routeSearch || "");
      const searchQuery = searchValue.trim().toLowerCase();
      const filteredRoutes = state.routes.filter((route) => {{
        if (!searchQuery) {{
          return true;
        }}
        const health = getRouteHealthRow(route.name);
        const haystack = [
          route.name,
          route.channel,
          route.description,
          route.webhook_url,
          route.feishu_webhook,
          route.telegram_chat_id,
          summarizeRouteDestination(route),
          health?.status,
          health?.last_error,
          ...getRouteUsageNames(route.name),
        ].join(" ").toLowerCase();
        return haystack.includes(searchQuery);
      }});
      const toolbox = `
        <div class="card section-toolbox">
          <div class="section-toolbox-head">
            <div>
              <div class="mono">${{copy("route search", "路由搜索")}}</div>
              <div class="panel-sub">${{copy("Search by name, channel, destination, or attached mission before you edit or delete a route.", "可按名称、通道、目标地址或引用任务快速定位路由。")}}</div>
            </div>
            <div class="section-toolbox-meta">
              <span class="chip">${{copy("shown", "显示")}}=${{filteredRoutes.length}}</span>
              <span class="chip">${{copy("total", "总数")}}=${{state.routes.length}}</span>
            </div>
          </div>
          <div class="search-shell">
            <input type="search" value="${{escapeHtml(searchValue)}}" data-route-search placeholder="${{copy("Search routes", "搜索路由")}}">
            <button class="btn-secondary" type="button" data-route-search-clear ${{searchValue.trim() ? "" : "disabled"}}>${{copy("Clear", "清空")}}</button>
          </div>
        </div>
      `;
      if (!filteredRoutes.length) {{
        root.innerHTML = `${{toolbox}}<div class="empty">${{state.routes.length ? copy("No route matched the current search.", "没有路由匹配当前搜索。") : copy("No named alert route configured yet. Start with one route so mission alerts can attach to a reusable sink.", "当前还没有配置命名告警路由。先创建一个路由，任务告警才能直接复用。")}}</div>`;
        root.querySelector("[data-route-search]")?.addEventListener("input", (event) => {{
          state.routeSearch = event.target.value;
          renderRoutes();
        }});
        root.querySelector("[data-route-search-clear]")?.addEventListener("click", () => {{
          state.routeSearch = "";
          renderRoutes();
        }});
        return;
      }}
      root.innerHTML = `${{toolbox}}${{filteredRoutes.map((route) => {{
        const health = getRouteHealthRow(route.name);
        const usageNames = getRouteUsageNames(route.name);
        const usageCount = usageNames.length;
        const healthTone = health?.status === "healthy" ? "ok" : health?.status && health.status !== "idle" ? "hot" : "";
        const destination = summarizeRouteDestination(route);
        return `
          <div class="card">
            <div class="card-top">
              <div>
                <h3 class="card-title">${{escapeHtml(route.name || "unnamed-route")}}</h3>
                <div class="meta">
                  <span>${{copy("channel", "通道")}}=${{escapeHtml(routeChannelLabel(route.channel))}}</span>
                  <span>${{copy("used", "已引用")}}=${{usageCount}}</span>
                  <span>${{copy("status", "状态")}}=${{escapeHtml(localizeWord(health?.status || "idle"))}}</span>
                </div>
              </div>
              <div style="display:grid; gap:6px; justify-items:end;">
                <span class="chip ${{healthTone}}">${{escapeHtml(localizeWord(health?.status || "idle"))}}</span>
                <span class="chip">${{escapeHtml(routeChannelLabel(route.channel))}}</span>
              </div>
            </div>
            <div class="panel-sub">${{escapeHtml(route.description || destination)}}</div>
            <div class="meta">
              <span>${{copy("destination", "目标")}}=${{escapeHtml(destination)}}</span>
              <span>${{copy("rate", "成功率")}}=${{formatRate(health?.success_rate)}}</span>
              <span>${{copy("last", "最近")}}=${{escapeHtml(health?.last_event_at || "-")}}</span>
            </div>
            ${{
              usageCount
                ? `<div class="panel-sub">${{copy("Used by", "正在被这些任务引用")}}: ${{escapeHtml(usageNames.slice(0, 3).join(", "))}}${{usageCount > 3 ? " ..." : ""}}</div>`
                : ""
            }}
            <div class="actions">
              <button class="btn-secondary" type="button" data-route-edit="${{escapeHtml(route.name)}}">${{copy("Edit", "编辑")}}</button>
              <button class="btn-secondary" type="button" data-route-attach="${{escapeHtml(route.name)}}">${{copy("Use In Mission", "用于任务草稿")}}</button>
              <button class="btn-danger" type="button" data-route-delete="${{escapeHtml(route.name)}}">${{copy("Delete", "删除")}}</button>
            </div>
          </div>
        `;
      }}).join("")}}`;
      root.querySelector("[data-route-search]")?.addEventListener("input", (event) => {{
        state.routeSearch = event.target.value;
        renderRoutes();
      }});
      root.querySelector("[data-route-search-clear]")?.addEventListener("click", () => {{
        state.routeSearch = "";
        renderRoutes();
      }});
      root.querySelectorAll("[data-route-edit]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await editRouteInDeck(String(button.dataset.routeEdit || ""));
          }} catch (error) {{
            reportError(error, copy("Edit route", "编辑路由"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});
      root.querySelectorAll("[data-route-attach]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await applyRouteToMissionDraft(String(button.dataset.routeAttach || ""));
          }} catch (error) {{
            reportError(error, copy("Apply route", "应用路由"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});
      root.querySelectorAll("[data-route-delete]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await deleteRouteFromBoard(String(button.dataset.routeDelete || ""));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});
    }}

    function renderStatus() {{
      const root = $("status-card");
      if (state.loading.board && !state.status && !state.ops) {{
        root.innerHTML = [skeletonCard(4), skeletonCard(4), skeletonCard(4)].join("");
        return;
      }}
      const ops = state.ops || {{}};
      const status = ops.daemon || state.status || {{}};
      const metrics = status.metrics || {{}};
      const collectorSummary = ops.collector_summary || {{}};
      const collectorTiers = ops.collector_tiers || {{}};
      const collectorDrilldown = Array.isArray(ops.collector_drilldown) ? ops.collector_drilldown : [];
      const watchMetrics = ops.watch_metrics || {{}};
      const watchSummary = ops.watch_summary || {{}};
      const watchHealth = Array.isArray(ops.watch_health) ? ops.watch_health : [];
      const routeSummary = ops.route_summary || {{}};
      const routeDrilldown = Array.isArray(ops.route_drilldown) ? ops.route_drilldown : [];
      const routeTimeline = Array.isArray(ops.route_timeline) ? ops.route_timeline : [];
      const degradedCollectors = ops.degraded_collectors || [];
      const recentFailures = ops.recent_failures || [];
      const isError = status.state === "error";
      const tierBlock = Object.entries(collectorTiers).length
        ? Object.entries(collectorTiers).map(([tierName, tier]) => `
            <div class="mini-item">${{tierName}} | total=${{tier.total || 0}} | ok=${{tier.ok || 0}} | warn=${{tier.warn || 0}} | error=${{tier.error || 0}}</div>
          `).join("")
        : `<div class="empty">${{copy("No collector tier breakdown available.", "没有采集器层级拆分数据。")}}</div>`;
      const watchBlock = watchHealth.length
        ? watchHealth.slice(0, 5).map((mission) => `
            <div class="mini-item">${{mission.id}} | ${{mission.status || "idle"}} | due=${{mission.is_due ? "yes" : "no"}} | rate=${{formatRate(mission.success_rate)}}</div>
          `).join("")
        : `<div class="empty">${{copy("No watch mission health record yet.", "当前没有任务健康记录。")}}</div>`;
      const collectorBlock = degradedCollectors.length
        ? degradedCollectors.slice(0, 4).map((collector) => `
            <div class="mini-item">${{collector.name}} | ${{collector.tier}} | ${{collector.status}} | available=${{collector.available}}</div>
          `).join("")
        : `<div class="empty">${{copy("No degraded collector currently reported.", "当前没有降级采集器。")}}</div>`;
      const collectorDrilldownBlock = collectorDrilldown.length
        ? collectorDrilldown.slice(0, 8).map((collector) => `
            <div class="mini-item">${{collector.name}} | ${{collector.tier || "-"}} | ${{collector.status || "ok"}} | available=${{collector.available}}</div>
            <div class="panel-sub">${{collector.setup_hint || collector.message || copy("No remediation note.", "没有修复说明。")}}</div>
          `).join("")
        : `<div class="empty">${{copy("No collector drill-down entry available.", "没有采集器下钻条目。")}}</div>`;
      const routeDrilldownBlock = routeDrilldown.length
        ? routeDrilldown.slice(0, 8).map((route) => `
            <div class="mini-item">${{route.name}} | channel=${{route.channel || "unknown"}} | status=${{route.status || "idle"}} | rate=${{formatRate(route.success_rate)}}</div>
            <div class="panel-sub">missions=${{route.mission_count || 0}} | rules=${{route.rule_count || 0}} | events=${{route.event_count || 0}} | failed=${{route.failure_count || 0}}</div>
            <div class="panel-sub">${{route.last_error || route.last_summary || copy("No recent route detail.", "没有最近路由详情。")}}</div>
          `).join("")
        : `<div class="empty">${{copy("No route drill-down entry available.", "没有路由下钻条目。")}}</div>`;
      const routeTimelineBlock = routeTimeline.length
        ? routeTimeline.slice(0, 8).map((event) => `
            <div class="mini-item">${{event.created_at || "-"}} | ${{event.route || "-"}} | ${{event.status || "pending"}} | ${{event.mission_name || event.mission_id || "-"}}</div>
            <div class="panel-sub">${{event.error || event.summary || copy("No route event detail.", "没有路由事件详情。")}}</div>
          `).join("")
        : `<div class="empty">${{copy("No route delivery timeline event available.", "没有路由投递时间线事件。")}}</div>`;
      const failureBlock = recentFailures.length
        ? recentFailures.slice(0, 4).map((failure) => `
            <div class="mini-item">${{failure.kind}} | ${{failure.mission_name || failure.name || "-"}} | ${{localizeWord(failure.status || "error")}} | ${{failure.error || "-"}}</div>
          `).join("")
        : `<div class="empty">${{copy("No recent failure captured.", "近期没有失败记录。")}}</div>`;
      root.innerHTML = `
        <div class="state-banner ${{isError ? "error" : ""}}">
          <div class="eyebrow"><span class="dot"></span> ${{copy("daemon", "守护进程")}} / ${{localizeWord(status.state || "idle")}}</div>
          <h3 class="card-title" style="margin-top:12px;">${{copy("Heartbeat", "心跳")}}: ${{status.heartbeat_at || "-"}}</h3>
          <div class="meta">
            <span>${{copy("cycles", "轮次")}}=${{metrics.cycles_total || 0}}</span>
            <span>${{copy("runs", "执行")}}=${{metrics.runs_total || 0}}</span>
            <span>${{copy("alerts", "告警")}}=${{metrics.alerts_total || 0}}</span>
            <span>${{copy("errors", "错误")}}=${{metrics.error_total || 0}}</span>
            <span>${{copy("success", "成功")}}=${{metrics.success_total || 0}}</span>
          </div>
        </div>
        <div class="card">
          <div class="mono">${{copy("collector health", "采集器健康")}}</div>
          <div class="meta">
            <span>total=${{collectorSummary.total || 0}}</span>
            <span>ok=${{collectorSummary.ok || 0}}</span>
            <span>warn=${{collectorSummary.warn || 0}}</span>
            <span>error=${{collectorSummary.error || 0}}</span>
            <span>unavailable=${{collectorSummary.unavailable || 0}}</span>
          </div>
        </div>
        <div class="card">
          <div class="mono">${{copy("route health", "路由健康")}}</div>
          <div class="meta">
            <span>healthy=${{routeSummary.healthy || 0}}</span>
            <span>degraded=${{routeSummary.degraded || 0}}</span>
            <span>missing=${{routeSummary.missing || 0}}</span>
            <span>idle=${{routeSummary.idle || 0}}</span>
          </div>
        </div>
        <div class="card">
          <div class="mono">${{copy("watch health", "任务健康")}}</div>
          <div class="meta">
            <span>total=${{watchSummary.total || 0}}</span>
            <span>enabled=${{watchSummary.enabled || 0}}</span>
            <span>healthy=${{watchSummary.healthy || 0}}</span>
            <span>degraded=${{watchSummary.degraded || 0}}</span>
            <span>idle=${{watchSummary.idle || 0}}</span>
            <span>disabled=${{watchSummary.disabled || 0}}</span>
            <span>due=${{watchSummary.due || 0}}</span>
            <span>rate=${{formatRate(watchMetrics.success_rate)}}</span>
          </div>
        </div>
        <div class="card">
          <div class="mono">${{copy("last_error", "最近错误")}}</div>
          <div>${{status.last_error || "-"}}</div>
        </div>
        <div class="graph-meta">
          <div class="mini-list">
            <div class="mono">${{copy("collector tiers", "采集器层级")}}</div>
            ${{tierBlock}}
          </div>
          <div class="mini-list">
            <div class="mono">${{copy("watch board", "任务面板")}}</div>
            ${{watchBlock}}
          </div>
        </div>
        <div class="graph-meta">
          <div class="mini-list">
            <div class="mono">${{copy("degraded collectors", "降级采集器")}}</div>
            ${{collectorBlock}}
          </div>
          <div class="mini-list">
            <div class="mono">${{copy("collector drill-down", "采集器下钻")}}</div>
            ${{collectorDrilldownBlock}}
          </div>
        </div>
        <div class="graph-meta">
          <div class="mini-list">
            <div class="mono">${{copy("route drill-down", "路由下钻")}}</div>
            ${{routeDrilldownBlock}}
          </div>
          <div class="mini-list">
            <div class="mono">${{copy("recent failures", "最近失败")}}</div>
            ${{failureBlock}}
          </div>
        </div>
        <div class="graph-meta">
          <div class="mini-list">
            <div class="mono">${{copy("route timeline", "路由时间线")}}</div>
            ${{routeTimelineBlock}}
          </div>
          <div class="mini-list">
            <div class="mono">${{copy("degraded collectors", "降级采集器")}}</div>
            ${{collectorBlock}}
          </div>
        </div>`;
    }}

    function renderDuplicateExplain(payload) {{
      if (!payload) {{
        return "";
      }}
      const candidates = payload.candidates || [];
      const header = `
        <div class="meta">
          <span>${{copy("suggested_primary", "建议主项")}}=${{payload.suggested_primary_id || "-"}}</span>
          <span>${{copy("matches", "匹配数")}}=${{payload.candidate_count || 0}}</span>
          <span>${{copy("shown", "显示数")}}=${{payload.returned_count || 0}}</span>
        </div>
      `;
      if (!candidates.length) {{
        return `<div class="card" style="margin-top:12px;">${{header}}<div class="panel-sub">${{copy("No close duplicate candidate found.", "没有找到接近的重复候选项。")}}</div></div>`;
      }}
      return `
        <div class="card" style="margin-top:12px;">
          ${{header}}
          <div class="stack" style="margin-top:12px;">
            ${{candidates.map((candidate) => `
              <div class="card">
                <div class="card-top">
                  <div>
                    <h3 class="card-title">${{candidate.title}}</h3>
                    <div class="meta">
                      <span>${{candidate.id}}</span>
                      <span>${{copy("similarity", "相似度")}}=${{Number(candidate.similarity || 0).toFixed(2)}}</span>
                      <span>${{copy("state", "状态")}}=${{localizeWord(candidate.review_state || "new")}}</span>
                    </div>
                  </div>
                  <span class="chip ${{candidate.suggested_primary_id === candidate.id ? "ok" : ""}}">${{candidate.suggested_primary_id === candidate.id ? copy("keep", "保留") : copy("merge", "合并")}}</span>
                </div>
                <div class="meta">
                  <span>${{copy("signals", "信号")}}=${{(candidate.signals || []).join(", ") || "-"}}</span>
                  <span>${{copy("domain", "域名")}}=${{candidate.same_domain ? copy("same", "相同") : copy("mixed", "混合")}}</span>
                </div>
              </div>
            `).join("")}}
          </div>
        </div>
      `;
    }}

    function renderReviewNotes(notes) {{
      const entries = Array.isArray(notes) ? notes : [];
      if (!entries.length) {{
        return `<div class="panel-sub">${{copy("No review note recorded yet.", "当前还没有审核备注。")}}</div>`;
      }}
      return `
        <div class="stack" style="margin-top:12px;">
          ${{entries.slice(-3).map((entry) => `
            <div class="mini-item">${{escapeHtml(entry.author || "console")}} | ${{escapeHtml(entry.created_at || "-")}}</div>
            <div class="panel-sub">${{escapeHtml(entry.note || "")}}</div>
          `).join("")}}
        </div>
      `;
    }}

    function getVisibleTriageItems() {{
      const activeFilter = state.triageFilter || "open";
      const searchQuery = String(state.triageSearch || "").trim().toLowerCase();
      const pinnedIds = new Set(uniqueValues(state.triagePinnedIds));
      return state.triage.filter((item) => {{
        if (pinnedIds.size && !pinnedIds.has(String(item.id || "").trim())) {{
          return false;
        }}
        const reviewState = String(item.review_state || "new").trim().toLowerCase() || "new";
        if (activeFilter === "all") {{
          // pass
        }} else if (activeFilter === "open") {{
          if (["verified", "duplicate", "ignored"].includes(reviewState)) {{
            return false;
          }}
        }} else if (reviewState !== activeFilter) {{
          return false;
        }}
        if (!searchQuery) {{
          return true;
        }}
        const noteText = Array.isArray(item.review_notes)
          ? item.review_notes.map((note) => String(note.note || "")).join(" ")
          : "";
        const haystack = [
          item.id,
          item.title,
          item.url,
          noteText,
        ].join(" ").toLowerCase();
        return haystack.includes(searchQuery);
      }});
    }}

    function isTriageItemSelected(itemId) {{
      return state.selectedTriageIds.includes(itemId);
    }}

    function toggleTriageSelection(itemId, checked = null) {{
      if (!itemId) {{
        return;
      }}
      const next = new Set(state.selectedTriageIds);
      const shouldSelect = checked === null ? !next.has(itemId) : Boolean(checked);
      if (shouldSelect) {{
        next.add(itemId);
        state.selectedTriageId = itemId;
      }} else {{
        next.delete(itemId);
      }}
      state.selectedTriageIds = Array.from(next);
    }}

    function selectVisibleTriageItems() {{
      const visibleIds = getVisibleTriageItems().map((item) => item.id);
      state.selectedTriageIds = visibleIds;
      if (visibleIds.length && !visibleIds.includes(state.selectedTriageId)) {{
        state.selectedTriageId = visibleIds[0];
      }}
    }}

    function clearTriageSelection() {{
      state.selectedTriageIds = [];
    }}

    function clearTriageEvidenceFocus() {{
      state.triagePinnedIds = [];
      renderTriage();
      showToast(copy("Returned to the full triage queue.", "已返回完整分诊队列。"), "success");
    }}

    function focusTriageEvidence(itemIds, {{ itemId = "", jump = true }} = {{}}) {{
      const normalizedIds = uniqueValues(itemIds).filter((candidate) => state.triage.some((item) => item.id === candidate));
      if (!normalizedIds.length) {{
        showToast(copy("No matching triage evidence is available for this story.", "当前没有可回查的分诊证据。"), "error");
        return;
      }}
      state.triagePinnedIds = normalizedIds;
      state.triageFilter = "all";
      state.triageSearch = "";
      state.selectedTriageId = itemId && normalizedIds.includes(itemId) ? itemId : normalizedIds[0];
      state.selectedTriageIds = [];
      renderTriage();
      if (jump) {{
        $("section-triage")?.scrollIntoView({{ block: "start", behavior: "smooth" }});
      }}
      showToast(
        state.language === "zh"
          ? `已聚焦 ${{normalizedIds.length}} 条相关分诊证据`
          : `Focused ${{normalizedIds.length}} related triage item(s)`,
        "success",
      );
    }}

    async function postTriageState(itemId, nextState) {{
      return api(`/api/triage/${{itemId}}/state`, {{
        method: "POST",
        headers: jsonHeaders,
        body: JSON.stringify({{ state: nextState, actor: "console" }}),
      }});
    }}

    async function deleteTriageItem(itemId) {{
      return api(`/api/triage/${{itemId}}`, {{
        method: "DELETE",
      }});
    }}

    async function runTriageExplain(itemId) {{
      if (!itemId) {{
        return;
      }}
      state.selectedTriageId = itemId;
      state.triageExplain[itemId] = await api(`/api/triage/${{itemId}}/explain?limit=4`);
      renderTriage();
    }}

    async function runTriageStateUpdate(itemId, nextState) {{
      if (!itemId || !nextState) {{
        return;
      }}
      state.selectedTriageId = itemId;
      const currentItem = state.triage.find((item) => item.id === itemId);
      const previousState = currentItem ? String(currentItem.review_state || "new") : "new";
      if (currentItem) {{
        currentItem.review_state = nextState;
      }}
      renderTriage();
      try {{
        await postTriageState(itemId, nextState);
        pushActionEntry({{
          kind: copy("triage state", "分诊状态"),
          label: state.language === "zh" ? `已将 ${{itemId}} 标记为 ${{localizeWord(nextState)}}` : `Marked ${{itemId}} as ${{nextState}}`,
          detail: state.language === "zh" ? `之前状态为 ${{localizeWord(previousState)}}。` : `Previous state was ${{previousState}}.`,
          undoLabel: state.language === "zh" ? `恢复为 ${{localizeWord(previousState)}}` : `Restore ${{previousState}}`,
          undo: async () => {{
            await postTriageState(itemId, previousState);
            await refreshBoard();
            showToast(
              state.language === "zh"
                ? `已恢复分诊状态：${{itemId}} -> ${{localizeWord(previousState)}}`
                : `Triage state restored: ${{itemId}} -> ${{previousState}}`,
              "success",
            );
          }},
        }});
        await refreshBoard();
      }} catch (error) {{
        if (currentItem) {{
          currentItem.review_state = previousState;
        }}
        renderTriage();
        throw error;
      }}
    }}

    async function runTriageDelete(itemId) {{
      if (!itemId) {{
        return;
      }}
      const currentItem = state.triage.find((item) => item.id === itemId);
      const itemLabel = currentItem && currentItem.title ? currentItem.title : itemId;
      const confirmed = window.confirm(
        state.language === "zh"
          ? `确认删除分诊条目：${{itemLabel}}？该操作会把条目从当前收件箱中移除。`
          : `Delete triage item "${{itemLabel}}" from the inbox?`,
      );
      if (!confirmed) {{
        return;
      }}
      await deleteTriageItem(itemId);
      state.selectedTriageIds = state.selectedTriageIds.filter((selectedId) => selectedId !== itemId);
      delete state.triageExplain[itemId];
      delete state.triageNoteDrafts[itemId];
      pushActionEntry({{
        kind: copy("triage delete", "分诊删除"),
        label: state.language === "zh" ? `已删除：${{itemLabel}}` : `Deleted ${{itemLabel}}`,
        detail: state.language === "zh" ? `条目 ID：${{itemId}}` : `Item id: ${{itemId}}`,
      }});
      await refreshBoard();
      showToast(
        state.language === "zh" ? `已删除分诊条目：${{itemLabel}}` : `Deleted triage item: ${{itemLabel}}`,
        "success",
      );
    }}

    async function createStoryFromTriageItems(itemIds) {{
      const normalizedIds = uniqueValues(itemIds).filter((itemId) => state.triage.some((item) => item.id === itemId));
      if (!normalizedIds.length) {{
        return;
      }}
      const selectedItems = normalizedIds
        .map((itemId) => state.triage.find((item) => item.id === itemId))
        .filter(Boolean);
      const created = await api("/api/stories/from-triage", {{
        method: "POST",
        headers: jsonHeaders,
        body: JSON.stringify({{
          item_ids: normalizedIds,
          status: "monitoring",
        }}),
      }});
      state.storySearch = "";
      state.storyFilter = "all";
      state.storySort = "attention";
      persistStoryWorkspacePrefs();
      state.selectedStoryId = created.id;
      state.storyDetails[created.id] = created;
      state.selectedTriageIds = state.selectedTriageIds.filter((itemId) => !normalizedIds.includes(itemId));
      pushActionEntry({{
        kind: copy("story seed", "故事生成"),
        label: state.language === "zh"
          ? `已从分诊生成故事：${{created.title}}`
          : `Created story from triage: ${{created.title}}`,
        detail: state.language === "zh"
          ? `来源条目：${{selectedItems.map((item) => item.title || item.id).slice(0, 3).join("、")}}`
          : `Source items: ${{selectedItems.map((item) => item.title || item.id).slice(0, 3).join(", ")}}`,
        undoLabel: copy("Delete story", "删除故事"),
        undo: async () => {{
          await api(`/api/stories/${{created.id}}`, {{ method: "DELETE" }});
          await refreshBoard();
          showToast(
            state.language === "zh" ? `已删除故事：${{created.title}}` : `Story deleted: ${{created.title}}`,
            "success",
          );
        }},
      }});
      await refreshBoard();
      state.selectedStoryId = created.id;
      renderStories();
      $("section-story")?.scrollIntoView({{ block: "start", behavior: "smooth" }});
      showToast(
        state.language === "zh"
          ? `已从 ${{normalizedIds.length}} 条分诊记录生成故事`
          : `Created story from ${{normalizedIds.length}} triage item(s)`,
        "success",
      );
    }}

    async function runTriageBatchStateUpdate(nextState) {{
      const itemIds = uniqueValues(state.selectedTriageIds).filter((itemId) => state.triage.some((item) => item.id === itemId));
      if (!itemIds.length || !nextState || state.triageBulkBusy) {{
        return;
      }}
      state.triageBulkBusy = true;
      if (!itemIds.includes(state.selectedTriageId)) {{
        state.selectedTriageId = itemIds[0];
      }}
      const previousStates = {{}};
      itemIds.forEach((itemId) => {{
        const currentItem = state.triage.find((item) => item.id === itemId);
        previousStates[itemId] = currentItem ? String(currentItem.review_state || "new") : "new";
        if (currentItem) {{
          currentItem.review_state = nextState;
        }}
      }});
      renderTriage();
      const appliedIds = [];
      try {{
        for (const itemId of itemIds) {{
          await postTriageState(itemId, nextState);
          appliedIds.push(itemId);
        }}
        state.selectedTriageIds = [];
        pushActionEntry({{
          kind: copy("triage batch", "分诊批处理"),
          label: state.language === "zh"
            ? `已批量将 ${{itemIds.length}} 条记录标记为 ${{localizeWord(nextState)}}`
            : `Marked ${{itemIds.length}} triage items as ${{nextState}}`,
          detail: state.language === "zh"
            ? `涉及条目：${{itemIds.join(", ")}}`
            : `Items: ${{itemIds.join(", ")}}`,
          undoLabel: state.language === "zh"
            ? `恢复这 ${{itemIds.length}} 条记录`
            : `Restore ${{itemIds.length}} items`,
          undo: async () => {{
            for (const itemId of itemIds) {{
              await postTriageState(itemId, previousStates[itemId] || "new");
            }}
            await refreshBoard();
            showToast(
              state.language === "zh"
                ? `已恢复 ${{itemIds.length}} 条分诊记录`
                : `Restored ${{itemIds.length}} triage items`,
              "success",
            );
          }},
        }});
        await refreshBoard();
        showToast(
          state.language === "zh"
            ? `已批量处理 ${{itemIds.length}} 条分诊记录`
            : `Processed ${{itemIds.length}} triage items`,
          "success",
        );
      }} catch (error) {{
        itemIds.forEach((itemId) => {{
          const currentItem = state.triage.find((item) => item.id === itemId);
          if (currentItem) {{
            currentItem.review_state = previousStates[itemId] || "new";
          }}
        }});
        renderTriage();
        for (const itemId of appliedIds.reverse()) {{
          try {{
            await postTriageState(itemId, previousStates[itemId] || "new");
          }} catch (rollbackError) {{
            console.error("triage batch rollback failed", rollbackError);
          }}
        }}
        await refreshBoard();
        throw error;
      }} finally {{
        state.triageBulkBusy = false;
        renderTriage();
      }}
    }}

    async function runTriageBatchDelete() {{
      const itemIds = uniqueValues(state.selectedTriageIds).filter((itemId) => state.triage.some((item) => item.id === itemId));
      if (!itemIds.length || state.triageBulkBusy) {{
        return;
      }}
      const confirmed = window.confirm(
        state.language === "zh"
          ? `确认删除已选的 ${{itemIds.length}} 条分诊记录？该操作会把它们从当前收件箱中移除。`
          : `Delete ${{itemIds.length}} selected triage items from the inbox?`,
      );
      if (!confirmed) {{
        return;
      }}
      state.triageBulkBusy = true;
      renderTriage();
      let deletedCount = 0;
      try {{
        for (const itemId of itemIds) {{
          await deleteTriageItem(itemId);
          deletedCount += 1;
          delete state.triageExplain[itemId];
          delete state.triageNoteDrafts[itemId];
        }}
        state.selectedTriageIds = [];
        pushActionEntry({{
          kind: copy("triage batch delete", "分诊批量删除"),
          label: state.language === "zh"
            ? `已批量删除 ${{itemIds.length}} 条分诊记录`
            : `Deleted ${{itemIds.length}} triage items`,
          detail: state.language === "zh"
            ? `涉及条目：${{itemIds.join(", ")}}`
            : `Items: ${{itemIds.join(", ")}}`,
        }});
        await refreshBoard();
        showToast(
          state.language === "zh"
            ? `已批量删除 ${{itemIds.length}} 条分诊记录`
            : `Deleted ${{itemIds.length}} triage items`,
          "success",
        );
      }} catch (error) {{
        await refreshBoard();
        const message = error && error.message ? error.message : String(error || "Unknown error");
        if (deletedCount > 0) {{
          throw new Error(
            state.language === "zh"
              ? `已删除 ${{deletedCount}}/${{itemIds.length}} 条记录后失败：${{message}}`
              : `Deleted ${{deletedCount}}/${{itemIds.length}} items before failure: ${{message}}`,
          );
        }}
        throw error;
      }} finally {{
        state.triageBulkBusy = false;
        renderTriage();
      }}
    }}

    function focusTriageNoteComposer(itemId) {{
      if (!itemId) {{
        return;
      }}
      state.selectedTriageId = itemId;
      renderTriage();
      const field = document.querySelector(`[data-triage-note-input="${{itemId}}"]`);
      if (field) {{
        field.focus();
        field.setSelectionRange(field.value.length, field.value.length);
      }}
    }}

    function moveTriageSelection(delta) {{
      const visibleItems = getVisibleTriageItems();
      if (!visibleItems.length) {{
        return;
      }}
      const currentIndex = Math.max(
        0,
        visibleItems.findIndex((item) => item.id === state.selectedTriageId),
      );
      const nextIndex = Math.min(
        visibleItems.length - 1,
        Math.max(0, currentIndex + delta),
      );
      state.selectedTriageId = visibleItems[nextIndex].id;
      renderTriage();
      const selectedCard = document.querySelector(`[data-triage-card="${{state.selectedTriageId}}"]`);
      selectedCard?.scrollIntoView({{ block: "nearest", behavior: "smooth" }});
    }}

    function renderTriage() {{
      const root = $("triage-list");
      const inlineStats = $("triage-stats-inline");
      if (state.loading.board && !state.triage.length) {{
        inlineStats.innerHTML = `<span>${{copy("loading", "加载中")}}=triage</span>`;
        root.innerHTML = [skeletonCard(4), skeletonCard(4), skeletonCard(4)].join("");
        return;
      }}
      const stats = state.triageStats || {{}};
      const triageStates = stats.states || {{}};
      const triageSearchValue = String(state.triageSearch || "");
      const filterOptions = [
        {{ key: "open", label: copy("open", "开放"), count: stats.open_count || 0 }},
        {{ key: "all", label: copy("all", "全部"), count: stats.total || state.triage.length }},
        ...Object.entries(triageStates).map(([key, count]) => ({{ key, label: localizeWord(key), count: count || 0 }})),
      ];
      const activeFilter = state.triageFilter || "open";
      const filteredItems = getVisibleTriageItems();
      const evidenceFocusCount = uniqueValues(state.triagePinnedIds).filter((itemId) => state.triage.some((item) => item.id === itemId)).length;
      const visibleIds = new Set(filteredItems.map((item) => item.id));
      state.selectedTriageIds = uniqueValues(state.selectedTriageIds).filter((itemId) => visibleIds.has(itemId));
      if (filteredItems.length && !filteredItems.some((item) => item.id === state.selectedTriageId)) {{
        state.selectedTriageId = filteredItems[0].id;
      }}
      if (!filteredItems.length) {{
        state.selectedTriageId = "";
      }}
      const selectedCount = state.selectedTriageIds.length;
      const batchBusy = Boolean(state.triageBulkBusy);
      const triageSearchCard = `
        <div class="card section-toolbox">
          <div class="section-toolbox-head">
            <div>
              <div class="mono">${{copy("queue search", "队列搜索")}}</div>
              <div class="panel-sub">${{copy("Search the visible queue by title, url, id, or recent review notes.", "按标题、链接、条目 ID 或最近备注搜索当前可见队列。")}}</div>
            </div>
            <div class="section-toolbox-meta">
              <span class="chip">${{copy("shown", "显示")}}=${{filteredItems.length}}</span>
              <span class="chip">${{copy("selected", "已选")}}=${{selectedCount}}</span>
              <span class="chip ${{evidenceFocusCount ? "hot" : ""}}">${{copy("evidence", "证据")}}=${{evidenceFocusCount || 0}}</span>
            </div>
          </div>
          <div class="search-shell">
            <input type="search" value="${{escapeHtml(triageSearchValue)}}" data-triage-search placeholder="${{copy("Search visible queue", "搜索当前队列")}}">
            <button class="btn-secondary" type="button" data-triage-search-clear ${{triageSearchValue.trim() ? "" : "disabled"}}>${{copy("Clear", "清空")}}</button>
          </div>
          ${{
            evidenceFocusCount
              ? `
                <div class="actions" style="margin-top:12px;">
                  <span class="chip hot">${{copy("evidence focus active", "证据聚焦中")}}</span>
                  <span class="panel-sub">${{copy(`Showing ${{evidenceFocusCount}} triage evidence item(s) linked to the current story.`, `当前只显示与故事关联的 ${{evidenceFocusCount}} 条分诊证据。`)}}</span>
                  <button class="btn-secondary" type="button" data-triage-pin-clear>${{copy("Show Full Queue", "显示完整队列")}}</button>
                </div>
              `
              : ""
          }}
        </div>
      `;
      const batchCopy = selectedCount
        ? copy(
            `Selected ${{selectedCount}} items. Apply one queue action or clear the selection.`,
            `已选 ${{selectedCount}} 条。直接执行一个批量动作，或先清空选择。`,
          )
        : copy(
            "Select visible items, then apply one review action across the queue without leaving the page.",
            "先选择当前列表中的条目，再在当前页面内一次性执行统一审核动作。",
          );
      const filterBlock = filterOptions.map((option) => `
        <button class="chip-btn ${{activeFilter === option.key ? "active" : ""}}" type="button" data-triage-filter="${{escapeHtml(option.key)}}">${{escapeHtml(option.label)}} (${{option.count || 0}})</button>
      `).join("");
      const batchToolbar = `
        <div class="card batch-toolbar-card ${{selectedCount ? "selection-live" : ""}}">
          <div class="batch-toolbar">
            <div class="batch-toolbar-head">
              <div>
                <div class="mono">${{copy("batch actions", "批量操作")}}</div>
                <div class="panel-sub">${{batchCopy}}</div>
              </div>
              <span class="chip ${{selectedCount ? "ok" : ""}}">${{copy("selected", "已选")}}=${{selectedCount}}</span>
            </div>
            <div class="actions">
              <button class="btn-secondary" type="button" data-triage-select-visible ${{(!filteredItems.length || batchBusy) ? "disabled" : ""}}>${{copy("Select Visible", "选择当前列表")}}</button>
              <button class="btn-secondary" type="button" data-triage-selection-clear ${{(!selectedCount || batchBusy) ? "disabled" : ""}}>${{copy("Clear Selection", "清空选择")}}</button>
              <button class="btn-secondary" type="button" data-triage-batch-state="triaged" ${{(!selectedCount || batchBusy) ? "disabled" : ""}}>${{copy("Batch Triage", "批量分诊")}}</button>
              <button class="btn-secondary" type="button" data-triage-batch-state="verified" ${{(!selectedCount || batchBusy) ? "disabled" : ""}}>${{copy("Batch Verify", "批量核验")}}</button>
              <button class="btn-secondary" type="button" data-triage-batch-state="escalated" ${{(!selectedCount || batchBusy) ? "disabled" : ""}}>${{copy("Batch Escalate", "批量升级")}}</button>
              <button class="btn-secondary" type="button" data-triage-batch-state="ignored" ${{(!selectedCount || batchBusy) ? "disabled" : ""}}>${{copy("Batch Ignore", "批量忽略")}}</button>
              <button class="btn-secondary" type="button" data-triage-batch-story ${{(!selectedCount || batchBusy) ? "disabled" : ""}}>${{copy("Batch Story", "批量生成故事")}}</button>
              <button class="btn-danger" type="button" data-triage-batch-delete ${{(!selectedCount || batchBusy) ? "disabled" : ""}}>${{copy("Batch Delete", "批量删除")}}</button>
            </div>
          </div>
        </div>
      `;
      inlineStats.innerHTML = `
        <span>${{copy("open", "开放")}}=${{stats.open_count || 0}}</span>
        <span>${{copy("closed", "关闭")}}=${{stats.closed_count || 0}}</span>
        <span>${{copy("notes", "备注")}}=${{stats.note_count || 0}}</span>
        <span>${{copy("verified", "已核验")}}=${{(stats.states || {{}}).verified || 0}}</span>
        <span>${{copy("filter", "筛选")}}=${{localizeWord(activeFilter)}}</span>
        <span>${{copy("selected", "选中")}}=${{selectedCount}}</span>
        <span>${{copy("evidence", "证据")}}=${{evidenceFocusCount}}</span>
        <span>${{copy("focus", "焦点")}}=${{state.selectedTriageId || "-"}}</span>
      `;
      if (!state.triage.length) {{
        root.innerHTML = `
          ${{triageSearchCard}}
          <div class="card">
            <div class="mono">${{copy("triage filters", "分诊筛选")}}</div>
            <div class="panel-sub">${{copy("Slice the queue by current review state before applying notes or state transitions.", "在写备注或修改状态前，先按审核状态切分队列。")}}</div>
            <div class="stack" style="margin-top:12px;">${{filterBlock}}</div>
          </div>
          <div class="card">
            <div class="mono">${{copy("triage shortcuts", "分诊快捷键")}}</div>
            <div class="panel-sub">${{copy("Use J/K to move, V to verify, T to triage, E to escalate, I to ignore, S to create a story, D to explain duplicates, and N to focus the note composer.", "使用 J/K 上下移动，V 核验，T 分诊，E 升级，I 忽略，S 生成故事，D 查看重复解释，N 聚焦备注输入。")}}</div>
          </div>
          ${{batchToolbar}}
          <div class="empty">${{copy("No triage item stored right now.", "当前没有分诊条目。")}}</div>`;
        return;
      }}
      root.innerHTML = `
        ${{triageSearchCard}}
        <div class="card">
          <div class="mono">${{copy("triage filters", "分诊筛选")}}</div>
          <div class="panel-sub">${{copy("Slice the queue by current review state before applying notes or state transitions.", "在写备注或修改状态前，先按审核状态切分队列。")}}</div>
          <div class="stack" style="margin-top:12px;">${{filterBlock}}</div>
        </div>
        <div class="card">
          <div class="mono">${{copy("triage shortcuts", "分诊快捷键")}}</div>
          <div class="panel-sub">${{copy("Use J/K to move, V to verify, T to triage, E to escalate, I to ignore, S to create a story, D to explain duplicates, and N to focus the note composer.", "使用 J/K 上下移动，V 核验，T 分诊，E 升级，I 忽略，S 生成故事，D 查看重复解释，N 聚焦备注输入。")}}</div>
        </div>
        ${{batchToolbar}}
        ${{
          filteredItems.length
            ? filteredItems.map((item) => `
        <div class="card selectable ${{item.id === state.selectedTriageId ? "selected" : ""}}" data-triage-card="${{item.id}}">
          <div class="card-top">
            <div class="triage-card-head">
              <label class="checkbox-inline">
                <input type="checkbox" data-triage-select="${{item.id}}" ${{isTriageItemSelected(item.id) ? "checked" : ""}}>
                <span>${{copy("select", "选择")}}</span>
              </label>
              <div>
                <h3 class="card-title">${{item.title}}</h3>
                <div class="meta">
                  <span>${{item.id}}</span>
                  <span>${{copy("state", "状态")}}=${{localizeWord(item.review_state || "new")}}</span>
                  <span>${{copy("score", "分数")}}=${{item.score || 0}}</span>
                  <span>${{copy("confidence", "置信度")}}=${{Number(item.confidence || 0).toFixed(2)}}</span>
                </div>
              </div>
            </div>
            <span class="chip ${{item.review_state === "escalated" ? "hot" : ""}}">${{localizeWord(item.review_state || "new")}}</span>
          </div>
          <div class="panel-sub">${{item.url}}</div>
          <div class="actions">
            <button class="btn-secondary" data-triage-explain="${{item.id}}">${{copy("Explain Dup", "查看重复解释")}}</button>
            <button class="btn-secondary" data-triage-state="triaged" data-triage-id="${{item.id}}">${{copy("Triaged", "分诊")}}</button>
            <button class="btn-secondary" data-triage-state="verified" data-triage-id="${{item.id}}">${{copy("Verify", "核验")}}</button>
            <button class="btn-secondary" data-triage-state="escalated" data-triage-id="${{item.id}}">${{copy("Escalate", "升级")}}</button>
            <button class="btn-secondary" data-triage-state="ignored" data-triage-id="${{item.id}}">${{copy("Ignore", "忽略")}}</button>
            <button class="btn-secondary" data-triage-story="${{item.id}}">${{copy("Create Story", "生成故事")}}</button>
            <button class="btn-danger" data-triage-delete="${{item.id}}">${{copy("Delete", "删除")}}</button>
          </div>
          <div class="card" style="margin-top:12px;">
            <div class="mono">${{copy("review notes", "审核备注")}}</div>
            <div class="panel-sub">${{copy("Capture reviewer rationale, routing hints, and merge context without leaving the queue.", "在不离开队列的前提下，记录审核理由、路由提示和合并上下文。")}}</div>
            ${{renderReviewNotes(item.review_notes)}}
            <form data-triage-note-form="${{item.id}}" style="margin-top:12px;">
              <label>${{copy("note composer", "备注编辑")}}<textarea name="note" rows="3" data-triage-note-input="${{item.id}}" placeholder="${{copy("Capture reviewer rationale, routing hint, or merge context.", "记录审核理由、路由提示或合并上下文。")}}">${{escapeHtml(state.triageNoteDrafts[item.id] || "")}}</textarea></label>
              <div class="toolbar">
                <button class="btn-primary" type="submit">${{copy("Save Note", "保存备注")}}</button>
              </div>
            </form>
          </div>
          ${{renderDuplicateExplain(state.triageExplain[item.id])}}
        </div>
      `).join("")
            : `<div class="empty">${{copy("No triage item matched the active queue filter.", "没有条目匹配当前分诊筛选。")}}</div>`
        }}
      `;

      root.querySelectorAll("[data-triage-filter]").forEach((button) => {{
        button.addEventListener("click", () => {{
          state.triageFilter = String(button.dataset.triageFilter || "open").trim() || "open";
          renderTriage();
        }});
      }});

      root.querySelector("[data-triage-search]")?.addEventListener("input", (event) => {{
        state.triageSearch = event.target.value;
        renderTriage();
      }});

      root.querySelector("[data-triage-search-clear]")?.addEventListener("click", () => {{
        state.triageSearch = "";
        renderTriage();
      }});

      root.querySelector("[data-triage-pin-clear]")?.addEventListener("click", () => {{
        clearTriageEvidenceFocus();
      }});

      root.querySelector("[data-triage-select-visible]")?.addEventListener("click", () => {{
        selectVisibleTriageItems();
        renderTriage();
      }});

      root.querySelector("[data-triage-selection-clear]")?.addEventListener("click", () => {{
        clearTriageSelection();
        renderTriage();
      }});

      root.querySelectorAll("[data-triage-batch-state]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await runTriageBatchStateUpdate(String(button.dataset.triageBatchState || "").trim());
          }} catch (error) {{
            reportError(error, copy("Batch triage", "批量分诊"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      root.querySelector("[data-triage-batch-story]")?.addEventListener("click", async (event) => {{
        const button = event.currentTarget;
        button.disabled = true;
        try {{
          await createStoryFromTriageItems(state.selectedTriageIds);
        }} catch (error) {{
          reportError(error, copy("Create story from triage", "从分诊生成故事"));
        }} finally {{
          button.disabled = false;
        }}
      }});

      root.querySelector("[data-triage-batch-delete]")?.addEventListener("click", async (event) => {{
        const button = event.currentTarget;
        button.disabled = true;
        try {{
          await runTriageBatchDelete();
        }} catch (error) {{
          reportError(error, copy("Batch delete", "批量删除"));
        }} finally {{
          button.disabled = false;
        }}
      }});

      root.querySelectorAll("[data-triage-card]").forEach((card) => {{
        card.addEventListener("click", (event) => {{
          if (event.target.closest("button, textarea, input, select, a, form, label")) {{
            return;
          }}
          state.selectedTriageId = String(card.dataset.triageCard || "").trim();
          renderTriage();
        }});
      }});

      root.querySelectorAll("[data-triage-select]").forEach((input) => {{
        input.addEventListener("change", () => {{
          toggleTriageSelection(String(input.dataset.triageSelect || "").trim(), input.checked);
          renderTriage();
        }});
      }});

      root.querySelectorAll("[data-triage-explain]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await runTriageExplain(String(button.dataset.triageExplain || "").trim());
          }} catch (error) {{
            reportError(error, copy("Explain duplicates", "查看重复解释"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      root.querySelectorAll("[data-triage-state]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await runTriageStateUpdate(
              String(button.dataset.triageId || "").trim(),
              String(button.dataset.triageState || "").trim(),
            );
          }} catch (error) {{
            reportError(error, copy("Update triage state", "更新分诊状态"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      root.querySelectorAll("[data-triage-story]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await createStoryFromTriageItems([String(button.dataset.triageStory || "").trim()]);
          }} catch (error) {{
            reportError(error, copy("Create story from triage", "从分诊生成故事"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      root.querySelectorAll("[data-triage-delete]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await runTriageDelete(String(button.dataset.triageDelete || "").trim());
          }} catch (error) {{
            reportError(error, copy("Delete triage item", "删除分诊条目"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      root.querySelectorAll("[data-triage-note-input]").forEach((field) => {{
        field.addEventListener("input", () => {{
          state.triageNoteDrafts[field.dataset.triageNoteInput] = field.value;
        }});
      }});

      root.querySelectorAll("[data-triage-note-form]").forEach((form) => {{
        form.addEventListener("submit", async (event) => {{
          event.preventDefault();
          const itemId = String(form.dataset.triageNoteForm || "").trim();
          const note = String(new FormData(form).get("note") || "").trim();
          if (!note) {{
            showToast(copy("Provide a note before saving.", "保存前请先填写备注。"), "error");
            return;
          }}
          const submitButton = form.querySelector("button[type='submit']");
          if (submitButton) {{
            submitButton.disabled = true;
          }}
          try {{
            await api(`/api/triage/${{itemId}}/note`, {{
              method: "POST",
              headers: jsonHeaders,
              body: JSON.stringify({{ note, author: "console" }}),
            }});
            state.triageNoteDrafts[itemId] = "";
            await refreshBoard();
          }} catch (error) {{
            reportError(error, copy("Save triage note", "保存分诊备注"));
          }} finally {{
            if (submitButton) {{
              submitButton.disabled = false;
            }}
          }}
        }});
      }});
    }}

    async function loadStory(identifier) {{
      state.selectedStoryId = identifier;
      state.loading.storyDetail = true;
      renderStories();
      try {{
        const [detail, graph] = await Promise.all([
          api(`/api/stories/${{identifier}}`),
          api(`/api/stories/${{identifier}}/graph`),
        ]);
        state.storyDetails[identifier] = detail;
        state.storyGraph[identifier] = graph;
      }} finally {{
        state.loading.storyDetail = false;
      }}
      renderStories();
    }}

    async function previewStoryMarkdown(identifier) {{
      state.selectedStoryId = identifier;
      if (!state.storyDetails[identifier]) {{
        state.storyDetails[identifier] = await api(`/api/stories/${{identifier}}`);
      }}
      state.storyMarkdown[identifier] = await apiText(`/api/stories/${{identifier}}/export?format=markdown`);
      renderStories();
    }}

    function renderStoryGraph(payload) {{
      if (!payload || !Array.isArray(payload.nodes) || !payload.nodes.length) {{
        return `<div class="empty">${{copy("No entity graph available for this story.", "这个故事当前没有实体图谱。")}}</div>`;
      }}
      const storyNode = payload.nodes.find((node) => node.kind === "story") || payload.nodes[0];
      const entityNodes = payload.nodes.filter((node) => node.kind === "entity");
      const positions = {{}};
      positions[storyNode.id] = {{ x: 360, y: 160 }};
      const radius = Math.min(145, 88 + (entityNodes.length * 5));
      entityNodes.forEach((node, index) => {{
        const angle = ((Math.PI * 2) * index) / Math.max(entityNodes.length, 1) - (Math.PI / 2);
        positions[node.id] = {{
          x: 360 + (Math.cos(angle) * radius),
          y: 160 + (Math.sin(angle) * radius),
        }};
      }});

      const lines = (payload.edges || []).map((edge) => {{
        const source = positions[edge.source];
        const target = positions[edge.target];
        if (!source || !target) {{
          return "";
        }}
        const stroke = edge.kind === "entity_relation" ? "rgba(255, 106, 130, 0.78)" : "rgba(127, 228, 255, 0.42)";
        const dash = edge.kind === "entity_relation" ? "0" : "6 6";
        return `<line x1="${{source.x}}" y1="${{source.y}}" x2="${{target.x}}" y2="${{target.y}}" stroke="${{stroke}}" stroke-width="2.5" stroke-dasharray="${{dash}}" />`;
      }}).join("");

      const labels = [storyNode, ...entityNodes].map((node) => {{
        const pos = positions[node.id];
        if (!pos) {{
          return "";
        }}
        const isStory = node.kind === "story";
        const radiusValue = isStory ? 34 : 22 + Math.min(10, (Number(node.in_story_source_count || 0) * 2));
        const fill = isStory ? "#07111d" : "#102031";
        const stroke = isStory ? "rgba(234, 244, 255, 0.76)" : "rgba(127, 228, 255, 0.32)";
        const textFill = "#eaf4ff";
        const label = escapeHtml(node.label || node.id);
        const subtitle = isStory
          ? `${{node.item_count || 0}} items`
          : `${{node.entity_type || "UNKNOWN"}} / ${{node.in_story_source_count || 0}} src`;
        const subtitleY = isStory ? 8 : 6;
        return `
          <g>
            <circle cx="${{pos.x}}" cy="${{pos.y}}" r="${{radiusValue}}" fill="${{fill}}" stroke="${{stroke}}" stroke-width="2.5"></circle>
            <text x="${{pos.x}}" y="${{pos.y - 4}}" text-anchor="middle" font-family="Avenir Next Condensed, Arial Narrow, sans-serif" font-size="${{isStory ? 16 : 13}}" fill="${{textFill}}">
              ${{label.slice(0, isStory ? 22 : 14)}}
            </text>
            <text x="${{pos.x}}" y="${{pos.y + subtitleY}}" text-anchor="middle" font-family="SF Mono, IBM Plex Mono, monospace" font-size="10" fill="${{textFill}}">
              ${{escapeHtml(subtitle)}}
            </text>
          </g>
        `;
      }}).join("");

      const entityList = entityNodes.length
        ? entityNodes.map((node) => `
            <div class="mini-item">${{escapeHtml(node.label)}} | ${{copy("type", "类型")}}=${{escapeHtml(node.entity_type || "UNKNOWN")}} | ${{copy("in_story", "故事内来源")}}=${{node.in_story_source_count || 0}}</div>
          `).join("")
        : `<div class="empty">${{copy("No entity node captured.", "没有捕获到实体节点。")}}</div>`;

      const relationList = (payload.edges || []).filter((edge) => edge.kind === "entity_relation").length
        ? (payload.edges || []).filter((edge) => edge.kind === "entity_relation").map((edge) => `
            <div class="mini-item">${{escapeHtml(edge.source)}} -> ${{escapeHtml(edge.target)}} | ${{escapeHtml(edge.relation_type || "RELATED")}}</div>
          `).join("")
        : `<div class="empty">${{copy("No direct entity relation captured. Story-level mention edges are still shown above.", "没有直接实体关系；上方仍会展示故事级提及关系。")}}</div>`;

      return `
        <div class="graph-shell">
          <div class="graph-canvas">
            <svg viewBox="0 0 720 320" role="img" aria-label="Story entity graph">
              <rect x="0" y="0" width="720" height="320" fill="transparent"></rect>
              ${{lines}}
              ${{labels}}
            </svg>
          </div>
          <div class="meta">
            <span>${{copy("nodes", "节点")}}=${{payload.nodes.length}}</span>
            <span>${{copy("edges", "边")}}=${{payload.edge_count || 0}}</span>
            <span>${{copy("relations", "关系")}}=${{payload.relation_count || 0}}</span>
            <span>${{copy("entities", "实体")}}=${{payload.entity_count || 0}}</span>
          </div>
          <div class="graph-meta">
            <div class="mini-list">${{entityList}}</div>
            <div class="mini-list">${{relationList}}</div>
          </div>
        </div>
      `;
    }}

    function renderStoryCreateDeck() {{
      const root = $("story-intake-deck");
      if (!root) {{
        return;
      }}
      const draft = normalizeStoryDraft(state.storyDraft || defaultStoryDraft());
      const selectedStory = getStoryRecord(state.selectedStoryId);
      root.innerHTML = `
        <form id="story-create-form">
          <div class="card-top">
            <div>
              <div class="mono">${{copy("manual story", "手工故事")}}</div>
              <h3 class="card-title" style="margin-top:10px;">${{copy("Capture A Brief Before It Gets Lost", "在信号散掉前先补一条故事")}}</h3>
            </div>
            <span class="chip ok">${{copy("lightweight", "轻量录入")}}</span>
          </div>
          <div class="panel-sub">${{copy("Use this for operator-authored briefs, incident notes, or tracking stubs that should be visible before automated clustering catches up.", "适合录入人工简报、事故备注，或那些需要先被看见、再等待自动聚类补齐的追踪占位。")}}</div>
          <div class="chip-row">
            ${{
              storyStatusOptions.map((status) => `
                <button class="chip-btn ${{draft.status === status ? "active" : ""}}" type="button" data-story-draft-status="${{status}}">${{escapeHtml(localizeWord(status))}}</button>
              `).join("")
            }}
          </div>
          <div class="field-grid">
            <label>${{copy("Story Title", "故事标题")}}<input name="title" value="${{escapeHtml(draft.title)}}" placeholder="${{copy("OpenAI launch brief", "OpenAI 发布简报")}}"><span class="field-hint">${{copy("Keep it short and legible in the story list.", "标题尽量短，方便在故事列表里快速扫读。")}}</span></label>
            <label>${{copy("Story Status", "故事状态")}}
              <select name="status">
                ${{storyStatusOptions.map((value) => `<option value="${{value}}" ${{draft.status === value ? "selected" : ""}}>${{localizeWord(value)}}</option>`).join("")}}
              </select>
              <span class="field-hint">${{copy("Status decides which lane this manual story enters first.", "状态决定这条手工故事先落在哪个工作阶段。")}}</span>
            </label>
          </div>
          <label>${{copy("Story Summary", "故事摘要")}}<textarea name="summary" rows="4" placeholder="${{copy("Capture what happened, why it matters, and what still needs confirmation.", "记录发生了什么、为什么重要，以及哪些部分仍待确认。")}}">${{escapeHtml(draft.summary)}}</textarea><span class="field-hint">${{copy("A compact summary is enough. Evidence and timeline can remain empty for manual stories.", "摘要写到够用即可；手工故事不需要一开始就补齐证据和时间线。")}}</span></label>
          <div class="toolbar">
            <button class="btn-primary" type="submit">${{copy("Create Story", "创建故事")}}</button>
            <button class="btn-secondary" type="button" id="story-draft-clear">${{copy("Clear Draft", "清空草稿")}}</button>
            <button class="btn-secondary" type="button" id="story-draft-template" ${{selectedStory ? "" : "disabled"}}>${{copy("Use Selected As Template", "以当前故事为模板")}}</button>
          </div>
        </form>
      `;
      const form = $("story-create-form");
      form?.addEventListener("input", () => {{
        state.storyDraft = collectStoryDraft(form);
      }});
      form?.addEventListener("submit", async (event) => {{
        event.preventDefault();
        await submitStoryDeck(form);
      }});
      root.querySelectorAll("[data-story-draft-status]").forEach((button) => {{
        button.addEventListener("click", () => {{
          state.storyDraft = {{
            ...collectStoryDraft(form),
            status: String(button.dataset.storyDraftStatus || "active").trim().toLowerCase() || "active",
          }};
          renderStoryCreateDeck();
        }});
      }});
      $("story-draft-clear")?.addEventListener("click", () => {{
        setStoryDraft(defaultStoryDraft());
        showToast(copy("Story draft cleared", "已清空故事草稿"), "success");
      }});
      $("story-draft-template")?.addEventListener("click", () => {{
        if (!selectedStory) {{
          return;
        }}
        setStoryDraft({{
          title: `${{selectedStory.title || copy("Story", "故事")}} ${{copy("Follow-up", "跟进")}}`,
          summary: String(selectedStory.summary || ""),
          status: String(selectedStory.status || "active"),
        }});
        focusStoryDeck("title");
        showToast(
          state.language === "zh"
            ? `已从 ${{selectedStory.title}} 生成故事草稿`
            : `Story draft cloned from ${{selectedStory.title}}`,
          "success",
        );
      }});
    }}

    function renderStoryDetail() {{
      const root = $("story-detail");
      const selected = state.selectedStoryId;
      if (state.loading.storyDetail && selected) {{
        root.innerHTML = [skeletonCard(4), skeletonCard(4), skeletonCard(4)].join("");
        return;
      }}
      const story = state.storyDetails[selected] || state.stories.find((candidate) => candidate.id === selected);
      if (!story) {{
        root.innerHTML = `<div class="empty">${{
          state.stories.length
            ? copy("No story is selected in the current filtered workspace.", "当前筛选后的工作区里没有选中的故事。")
            : copy("No persisted story snapshot yet. Create a manual brief above or build stories from CLI/MCP.", "当前还没有持久化故事快照。可以先在上方手工补一条，或通过 CLI/MCP 构建故事。")
        }}</div>`;
        return;
      }}
      const storyEvidenceIds = uniqueValues([
        story.primary_item_id,
        ...(Array.isArray(story.primary_evidence) ? story.primary_evidence.map((row) => row.item_id) : []),
        ...(Array.isArray(story.secondary_evidence) ? story.secondary_evidence.map((row) => row.item_id) : []),
      ]);
      const evidenceBlock = (rows, emptyLabel) => rows.length
        ? rows.map((row) => `
            <div class="card">
              <div class="card-top">
                <div>
                    <h3 class="card-title">${{row.title}}</h3>
                    <div class="meta">
                      <span>${{row.item_id}}</span>
                      <span>${{row.source_name || row.source_type || "-"}}</span>
                      <span>${{copy("score", "分数")}}=${{row.score || 0}}</span>
                      <span>${{copy("confidence", "置信度")}}=${{Number(row.confidence || 0).toFixed(2)}}</span>
                    </div>
                  </div>
                <span class="chip ${{row.role === "primary" ? "ok" : ""}}">${{copy(row.role || "secondary", row.role === "primary" ? "主证据" : "次证据")}}</span>
              </div>
              <div class="panel-sub">${{row.url || "-"}}</div>
              <div class="actions">
                <button class="btn-secondary" type="button" data-story-evidence-triage="${{row.item_id}}">${{copy("Open In Triage", "回到分诊")}}</button>
              </div>
            </div>
          `).join("")
        : `<div class="empty">${{emptyLabel}}</div>`;
      const contradictionBlock = (story.contradictions || []).length
        ? story.contradictions.map((conflict) => `
            <div class="card">
              <div class="card-top">
                <div>
                    <h3 class="card-title">${{conflict.topic}}</h3>
                    <div class="meta">
                    <span>${{copy("positive", "正向")}}=${{conflict.positive || 0}}</span>
                    <span>${{copy("negative", "负向")}}=${{conflict.negative || 0}}</span>
                    <span>${{copy("neutral", "中性")}}=${{conflict.neutral || 0}}</span>
                    </div>
                  </div>
                <span class="chip hot">${{copy("conflict", "冲突")}}</span>
              </div>
              <div class="panel-sub">${{conflict.note || copy("Cross-source stance divergence detected.", "检测到跨来源立场分歧。")}}</div>
            </div>
          `).join("")
        : `<div class="empty">${{copy("No contradiction marker in this story.", "这个故事没有冲突标记。")}}</div>`;
      const timelineBlock = (story.timeline || []).length
        ? story.timeline.map((event) => `
            <div class="card">
              <div class="card-top">
                <div>
                    <h3 class="card-title">${{event.title}}</h3>
                    <div class="meta">
                      <span>${{event.time || "-"}}</span>
                      <span>${{event.source_name || "-"}}</span>
                      <span>${{copy("role", "角色")}}=${{copy(event.role || "secondary", event.role === "primary" ? "主证据" : "次证据")}}</span>
                      <span>${{copy("score", "分数")}}=${{event.score || 0}}</span>
                    </div>
                  </div>
                </div>
              <div class="panel-sub">${{event.url || "-"}}</div>
            </div>
          `).join("")
        : `<div class="empty">${{copy("No timeline event captured.", "当前没有时间线事件。")}}</div>`;
      const markdownPreview = state.storyMarkdown[selected]
        ? `
            <div class="card">
              <div class="mono">${{copy("markdown evidence pack", "Markdown 证据包")}}</div>
              <pre class="text-block">${{escapeHtml(state.storyMarkdown[selected])}}</pre>
            </div>
          `
        : "";
      const graphPreview = renderStoryGraph(state.storyGraph[selected]);
      root.innerHTML = `
        <div class="card">
          <div class="card-top">
            <div>
              <h3 class="card-title">${{story.title}}</h3>
              <div class="meta">
                <span>${{story.id}}</span>
                <span>${{copy("status", "状态")}}=${{localizeWord(story.status || "active")}}</span>
                <span>${{copy("items", "条目")}}=${{story.item_count || 0}}</span>
                <span>${{copy("sources", "来源")}}=${{story.source_count || 0}}</span>
                <span>${{copy("score", "分数")}}=${{Number(story.score || 0).toFixed(1)}}</span>
                <span>${{copy("confidence", "置信度")}}=${{Number(story.confidence || 0).toFixed(2)}}</span>
              </div>
            </div>
            <span class="chip ${{(story.contradictions || []).length ? "hot" : "ok"}}">${{(story.contradictions || []).length ? copy("mixed signals", "信号冲突") : copy("aligned", "一致")}}</span>
          </div>
          <div class="panel-sub">${{story.summary || copy("No summary captured.", "没有记录到摘要。")}}</div>
          <div class="entity-row">
            ${{(story.entities || []).slice(0, 8).map((entity) => `<span class="chip">${{entity}}</span>`).join("") || `<span class="chip">${{copy("no entities", "无实体")}}</span>`}}
          </div>
          <div class="actions">
            <button class="btn-secondary" data-story-markdown="${{story.id}}">${{copy("Preview Markdown", "预览 Markdown")}}</button>
            <button class="btn-secondary" type="button" data-story-focus-triage="${{story.id}}" ${{storyEvidenceIds.length ? "" : "disabled"}}>${{copy("Focus Evidence In Triage", "回查分诊证据")}}</button>
            <a href="/api/stories/${{story.id}}" target="_blank" rel="noreferrer">${{copy("Open JSON", "打开 JSON")}}</a>
            <a href="/api/stories/${{story.id}}/export?format=markdown" target="_blank" rel="noreferrer">${{copy("Export MD", "导出 MD")}}</a>
          </div>
        </div>
        <div class="card">
          <div class="mono">${{copy("story editor", "故事编辑器")}}</div>
          <div class="meta" style="margin-top:8px;">
            <span class="chip ok">${{copy("editable", "可编辑")}}</span>
            <span>${{copy("Only title, summary, and status change here.", "这里只修改标题、摘要和状态。")}}</span>
          </div>
          <div class="panel-sub">${{copy("Tune the persisted title, summary, and story status without rebuilding the whole workspace snapshot.", "无需重建整个工作区快照，也能直接调整已持久化的标题、摘要和故事状态。")}}</div>
          <form id="story-editor-form" data-story-id="${{story.id}}" style="margin-top:12px;">
            <div class="field-grid">
              <label>${{copy("Story Title", "故事标题")}}<input name="title" value="${{escapeHtml(story.title || "")}}" placeholder="${{copy("OpenAI Launch Story", "OpenAI 发布故事")}}"></label>
              <label>${{copy("Story Status", "故事状态")}}
                <select name="status">
                  ${{storyStatusOptions.map((value) => `<option value="${{value}}" ${{(story.status || "active") === value ? "selected" : ""}}>${{localizeWord(value)}}</option>`).join("")}}
                </select>
              </label>
            </div>
            <label>${{copy("Story Summary", "故事摘要")}}<textarea name="summary" rows="4" placeholder="${{copy("Condense why this story matters right now.", "简要说明这个故事此刻为什么重要。")}}">${{escapeHtml(story.summary || "")}}</textarea></label>
            <div class="toolbar">
              <button class="btn-primary" type="submit">${{copy("Save Story", "保存故事")}}</button>
              <button class="btn-secondary" type="button" data-story-detail-status="${{story.status === "archived" ? "active" : "archived"}}">${{story.status === "archived" ? copy("Restore Story", "恢复故事") : copy("Archive Story", "归档故事")}}</button>
              <button class="btn-danger" type="button" data-story-delete="${{story.id}}">${{copy("Delete Story", "删除故事")}}</button>
            </div>
          </form>
        </div>
        <div class="story-columns">
          <div class="stack">
            <div class="meta"><span class="mono">${{copy("primary evidence", "主证据")}}</span><span class="chip">${{copy("read-only snapshot", "只读快照")}}</span></div>
            ${{evidenceBlock(story.primary_evidence || [], copy("No primary evidence captured.", "没有主证据。"))}}
          </div>
          <div class="stack">
            <div class="meta"><span class="mono">${{copy("secondary evidence", "次证据")}}</span><span class="chip">${{copy("read-only snapshot", "只读快照")}}</span></div>
            ${{evidenceBlock(story.secondary_evidence || [], copy("No secondary evidence captured.", "没有次证据。"))}}
          </div>
        </div>
        <div class="stack">
          <div class="meta"><span class="mono">${{copy("contradiction markers", "冲突标记")}}</span><span class="chip">${{copy("read-only analysis", "只读分析")}}</span></div>
          ${{contradictionBlock}}
        </div>
        <div class="stack">
          <div class="meta"><span class="mono">${{copy("timeline", "时间线")}}</span><span class="chip">${{copy("read-only analysis", "只读分析")}}</span></div>
          ${{timelineBlock}}
        </div>
        <div class="stack">
          <div class="meta"><span class="mono">${{copy("entity graph", "实体图谱")}}</span><span class="chip">${{copy("read-only analysis", "只读分析")}}</span></div>
          ${{graphPreview}}
        </div>
        ${{markdownPreview}}
      `;

      root.querySelectorAll("[data-story-markdown]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await previewStoryMarkdown(button.dataset.storyMarkdown);
          }} catch (error) {{
            reportError(error, copy("Preview story markdown", "预览故事 Markdown"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});
      root.querySelector("[data-story-focus-triage]")?.addEventListener("click", () => {{
        focusTriageEvidence(storyEvidenceIds, {{ itemId: story.primary_item_id || storyEvidenceIds[0] || "" }});
      }});
      root.querySelectorAll("[data-story-evidence-triage]").forEach((button) => {{
        button.addEventListener("click", () => {{
          const itemId = String(button.dataset.storyEvidenceTriage || "").trim();
          if (!itemId) {{
            return;
          }}
          focusTriageEvidence(storyEvidenceIds, {{ itemId }});
        }});
      }});

      const storyEditorForm = document.getElementById("story-editor-form");
      if (storyEditorForm) {{
        storyEditorForm.addEventListener("submit", async (event) => {{
          event.preventDefault();
          const form = new FormData(storyEditorForm);
          const payload = {{
            title: String(form.get("title") || "").trim(),
            summary: String(form.get("summary") || "").trim(),
            status: String(form.get("status") || "").trim(),
          }};
          if (!payload.title) {{
            showToast(copy("Provide a story title before saving.", "保存前请先填写故事标题。"), "error");
            return;
          }}
          const submitButton = storyEditorForm.querySelector("button[type='submit']");
          if (submitButton) {{
            submitButton.disabled = true;
          }}
          const previousStory = {{
            title: story.title || "",
            summary: story.summary || "",
            status: story.status || "active",
          }};
          if (state.storyDetails[story.id]) {{
            state.storyDetails[story.id] = {{
              ...state.storyDetails[story.id],
              ...payload,
            }};
          }}
          renderStories();
          try {{
            await api(`/api/stories/${{story.id}}`, {{
              method: "PUT",
              headers: jsonHeaders,
              body: JSON.stringify(payload),
            }});
            state.storyMarkdown[story.id] = "";
            pushActionEntry({{
              kind: copy("story update", "故事更新"),
              label: state.language === "zh" ? `已更新故事：${{payload.title}}` : `Updated story ${{payload.title}}`,
              detail: state.language === "zh" ? `当前故事状态为 ${{localizeWord(payload.status || "active")}}。` : `Story status is now ${{payload.status || "active"}}.`,
              undoLabel: copy("Restore story", "恢复故事"),
              undo: async () => {{
                await api(`/api/stories/${{story.id}}`, {{
                  method: "PUT",
                  headers: jsonHeaders,
                  body: JSON.stringify(previousStory),
                }});
                await refreshBoard();
                showToast(
                  state.language === "zh" ? `已恢复故事：${{previousStory.title}}` : `Story restored: ${{previousStory.title}}`,
                  "success",
                );
              }},
            }});
            await refreshBoard();
            showToast(
              state.language === "zh" ? `故事已更新：${{payload.title}}` : `Story updated: ${{payload.title}}`,
              "success",
            );
          }} catch (error) {{
            if (state.storyDetails[story.id]) {{
              state.storyDetails[story.id] = {{
                ...state.storyDetails[story.id],
                ...previousStory,
              }};
            }}
            renderStories();
            reportError(error, copy("Update story", "更新故事"));
          }} finally {{
            if (submitButton) {{
              submitButton.disabled = false;
            }}
          }}
        }});
      }}
      root.querySelector("[data-story-detail-status]")?.addEventListener("click", async (event) => {{
        const button = event.currentTarget;
        button.disabled = true;
        try {{
          await setStoryStatusQuick(story.id, String(button.dataset.storyDetailStatus || ""));
        }} catch (error) {{
          reportError(error, copy("Update story state", "更新故事状态"));
        }} finally {{
          button.disabled = false;
        }}
      }});
      root.querySelector("[data-story-delete]")?.addEventListener("click", async (event) => {{
        const button = event.currentTarget;
        button.disabled = true;
        try {{
          await deleteStoryFromWorkspace(String(button.dataset.storyDelete || story.id));
        }} catch (error) {{
          reportError(error, copy("Delete story", "删除故事"));
        }} finally {{
          button.disabled = false;
        }}
      }});
    }}

    function renderStories() {{
      const root = $("story-list");
      const inlineStats = $("story-stats-inline");
      renderStoryCreateDeck();
      if (state.loading.board && !state.stories.length) {{
        inlineStats.innerHTML = `<span>${{copy("loading", "加载中")}}=stories</span>`;
        root.innerHTML = [skeletonCard(4), skeletonCard(4)].join("");
        $("story-detail").innerHTML = skeletonCard(5);
        return;
      }}
      const contradictions = state.stories.reduce((count, story) => count + ((story.contradictions || []).length ? 1 : 0), 0);
      const totalEvidence = state.stories.reduce((count, story) => count + (story.item_count || 0), 0);
      const storySearchValue = String(state.storySearch || "");
      const storySearchQuery = storySearchValue.trim().toLowerCase();
      const storyFilter = normalizeStoryFilter(state.storyFilter);
      const storySort = normalizeStorySort(state.storySort);
      const activeStoryView = detectStoryViewPreset({{ filter: storyFilter, sort: storySort, search: storySearchValue }});
      const matchedStories = state.stories.filter((story) => {{
        const storyStatus = String(story.status || "active").trim().toLowerCase() || "active";
        if (storyFilter === "conflicted" && !(Array.isArray(story.contradictions) && story.contradictions.length)) {{
          return false;
        }}
        if (storyFilter !== "all" && storyFilter !== "conflicted" && storyStatus !== storyFilter) {{
          return false;
        }}
        if (!storySearchQuery) {{
          return true;
        }}
        const primaryTitles = Array.isArray(story.primary_evidence)
          ? story.primary_evidence.map((row) => String(row.title || "")).join(" ")
          : "";
        const haystack = [
          story.id,
          story.title,
          story.summary,
          ...(Array.isArray(story.entities) ? story.entities : []),
          primaryTitles,
        ].join(" ").toLowerCase();
        return haystack.includes(storySearchQuery);
      }});
      const filteredStories = [...matchedStories].sort((left, right) => compareStoriesByWorkspaceOrder(left, right, storySort));
      const visibleStoryIds = new Set(filteredStories.map((story) => story.id));
      state.selectedStoryIds = uniqueValues(state.selectedStoryIds).filter((storyId) => visibleStoryIds.has(storyId));
      const storyFilterOptions = [
        {{ key: "all", label: copy("all", "全部"), count: state.stories.length }},
        {{ key: "conflicted", label: copy("conflicted", "冲突"), count: contradictions }},
        ...["active", "monitoring", "resolved", "archived"].map((key) => ({{
          key,
          label: localizeWord(key),
          count: state.stories.filter((story) => (String(story.status || "active").trim().toLowerCase() || "active") === key).length,
        }})),
      ];
      inlineStats.innerHTML = `
        <span>${{copy("stories", "故事")}}=${{state.stories.length}}</span>
        <span>${{copy("evidence", "证据")}}=${{totalEvidence}}</span>
        <span>${{copy("contradicted", "冲突故事")}}=${{contradictions}}</span>
        <span>${{copy("shown", "显示")}}=${{filteredStories.length}}</span>
        <span>${{copy("view", "视图")}}=${{storyViewPresetLabel(activeStoryView)}}</span>
        <span>${{copy("sort", "排序")}}=${{storySortLabel(storySort)}}</span>
        <span>${{copy("selected", "已选")}}=${{state.selectedStoryIds.length}}</span>
        <span>${{copy("selected", "选中")}}=${{state.selectedStoryId || "-"}}</span>
      `;
      const storyBatchCount = state.selectedStoryIds.length;
      const storyBatchBusy = Boolean(state.storyBulkBusy);
      const storySearchCard = `
        <div class="card section-toolbox">
          <div class="section-toolbox-head">
            <div>
              <div class="mono">${{copy("story search", "故事搜索")}}</div>
              <div class="panel-sub">${{copy("Search by story title, summary, entity, id, or primary evidence title before opening the workspace.", "可按故事标题、摘要、实体、故事 ID 或主证据标题快速定位。")}}</div>
            </div>
            <div class="section-toolbox-meta">
              <button class="btn-secondary" type="button" data-story-deck-focus>${{copy("New Story", "新建故事")}}</button>
              <span class="chip ${{activeStoryView === "custom" ? "hot" : "ok"}}">${{storyViewPresetLabel(activeStoryView)}}</span>
              <span class="chip ok">${{storySortLabel(storySort)}}</span>
              <span class="chip">${{copy("shown", "显示")}}=${{filteredStories.length}}</span>
              <span class="chip">${{copy("total", "总数")}}=${{state.stories.length}}</span>
            </div>
          </div>
          <div class="search-shell">
            <input type="search" value="${{escapeHtml(storySearchValue)}}" data-story-search placeholder="${{copy("Search stories", "搜索故事")}}">
            <button class="btn-secondary" type="button" data-story-search-clear ${{storySearchValue.trim() ? "" : "disabled"}}>${{copy("Clear", "清空")}}</button>
          </div>
          <div class="field-grid" style="margin-top:12px;">
            <label>${{copy("Story Sort", "故事排序")}}
              <select data-story-sort>
                ${{storySortOptions.map((option) => `<option value="${{option}}" ${{storySort === option ? "selected" : ""}}>${{storySortLabel(option)}}</option>`).join("")}}
              </select>
            </label>
            <div>
              <div class="mono">${{copy("view hint", "视图提示")}}</div>
              <div class="panel-sub">${{activeStoryView === "custom" ? storySortSummary(storySort) : storyViewPresetDescription(activeStoryView)}}</div>
            </div>
          </div>
          <div class="chip-row">
            ${{storyViewPresetOptions.map((option) => `
              <button class="chip-btn ${{activeStoryView === option ? "active" : ""}}" type="button" data-story-view="${{escapeHtml(option)}}">${{escapeHtml(storyViewPresetLabel(option))}}</button>
            `).join("")}}
            ${{activeStoryView === "custom" ? `<span class="chip hot">${{storyViewPresetLabel("custom")}}</span>` : ""}}
          </div>
          <div class="chip-row">
            ${{storyFilterOptions.map((option) => `
              <button class="chip-btn ${{storyFilter === option.key ? "active" : ""}}" type="button" data-story-filter="${{escapeHtml(option.key)}}">${{escapeHtml(option.label)}} (${{option.count || 0}})</button>
            `).join("")}}
          </div>
        </div>
      `;
      const storyBatchToolbar = `
        <div class="card batch-toolbar-card ${{storyBatchCount ? "selection-live" : ""}}">
          <div class="batch-toolbar">
            <div class="batch-toolbar-head">
              <div>
                <div class="mono">${{copy("story batch", "故事批量操作")}}</div>
                <div class="panel-sub">${{
                  storyBatchCount
                    ? copy(`Selected ${{storyBatchCount}} stories. Move them together to reduce workspace churn.`, `已选 ${{storyBatchCount}} 条故事，可以一起切换状态。`)
                    : copy("Select visible stories when you need to archive, monitor, or resolve a whole lane together.", "当你需要整体归档、恢复监控或批量解决时，可以先选择当前可见故事。")
                }}</div>
              </div>
              <span class="chip ${{storyBatchCount ? "ok" : ""}}">${{copy("selected", "已选")}}=${{storyBatchCount}}</span>
            </div>
            <div class="actions">
              <button class="btn-secondary" type="button" data-story-select-visible ${{(!filteredStories.length || storyBatchBusy) ? "disabled" : ""}}>${{copy("Select Visible", "选择当前列表")}}</button>
              <button class="btn-secondary" type="button" data-story-selection-clear ${{(!storyBatchCount || storyBatchBusy) ? "disabled" : ""}}>${{copy("Clear Selection", "清空选择")}}</button>
              <button class="btn-secondary" type="button" data-story-batch-status="monitoring" ${{(!storyBatchCount || storyBatchBusy) ? "disabled" : ""}}>${{copy("Batch Monitor", "批量监控")}}</button>
              <button class="btn-secondary" type="button" data-story-batch-status="resolved" ${{(!storyBatchCount || storyBatchBusy) ? "disabled" : ""}}>${{copy("Batch Resolve", "批量解决")}}</button>
              <button class="btn-secondary" type="button" data-story-batch-status="archived" ${{(!storyBatchCount || storyBatchBusy) ? "disabled" : ""}}>${{copy("Batch Archive", "批量归档")}}</button>
            </div>
          </div>
        </div>
      `;
      if (!state.stories.length) {{
        root.innerHTML = `${{storySearchCard}}${{storyBatchToolbar}}<div class="empty">${{copy("No story snapshot yet. Create a manual brief above or run datapulse --story-build / MCP story tools first.", "当前还没有故事快照。可以先在上方手工补一条，或执行 datapulse --story-build / MCP 故事工具。")}}</div>`;
        root.querySelector("[data-story-deck-focus]")?.addEventListener("click", () => {{
          focusStoryDeck("title");
        }});
        root.querySelector("[data-story-search]")?.addEventListener("input", (event) => {{
          state.storySearch = event.target.value;
          renderStories();
        }});
        root.querySelector("[data-story-search-clear]")?.addEventListener("click", () => {{
          state.storySearch = "";
          renderStories();
        }});
        root.querySelector("[data-story-sort]")?.addEventListener("change", (event) => {{
          state.storySort = normalizeStorySort(event.target.value);
          persistStoryWorkspacePrefs();
          renderStories();
        }});
        root.querySelectorAll("[data-story-view]").forEach((button) => {{
          button.addEventListener("click", () => {{
            applyStoryViewPreset(String(button.dataset.storyView || "").trim());
          }});
        }});
        root.querySelectorAll("[data-story-filter]").forEach((button) => {{
          button.addEventListener("click", () => {{
            state.storyFilter = normalizeStoryFilter(button.dataset.storyFilter);
            persistStoryWorkspacePrefs();
            renderStories();
          }});
        }});
        renderStoryDetail();
        return;
      }}
      if (filteredStories.length && !filteredStories.some((story) => story.id === state.selectedStoryId)) {{
        state.selectedStoryId = filteredStories[0].id;
      }}
      if (!filteredStories.length) {{
        state.selectedStoryId = "";
        root.innerHTML = `${{storySearchCard}}${{storyBatchToolbar}}<div class="empty">${{copy("No story matched the current search or filter.", "没有故事匹配当前搜索或筛选。")}}</div>`;
        renderStoryDetail();
        root.querySelector("[data-story-deck-focus]")?.addEventListener("click", () => {{
          focusStoryDeck("title");
        }});
        root.querySelector("[data-story-search]")?.addEventListener("input", (event) => {{
          state.storySearch = event.target.value;
          renderStories();
        }});
        root.querySelector("[data-story-search-clear]")?.addEventListener("click", () => {{
          state.storySearch = "";
          renderStories();
        }});
        root.querySelector("[data-story-sort]")?.addEventListener("change", (event) => {{
          state.storySort = normalizeStorySort(event.target.value);
          persistStoryWorkspacePrefs();
          renderStories();
        }});
        root.querySelectorAll("[data-story-view]").forEach((button) => {{
          button.addEventListener("click", () => {{
            applyStoryViewPreset(String(button.dataset.storyView || "").trim());
          }});
        }});
        root.querySelectorAll("[data-story-filter]").forEach((button) => {{
          button.addEventListener("click", () => {{
            state.storyFilter = normalizeStoryFilter(button.dataset.storyFilter);
            persistStoryWorkspacePrefs();
            renderStories();
          }});
        }});
        return;
      }}
      root.innerHTML = `${{storySearchCard}}${{storyBatchToolbar}}${{filteredStories.map((story) => {{
        const selected = story.id === state.selectedStoryId ? "selected" : "";
        const primary = (story.primary_evidence || [])[0];
        const updatedLabel = formatCompactDateTime(story.updated_at || story.generated_at || "");
        const priority = describeStoryPriority(story);
        return `
          <div class="card selectable ${{selected}}" data-story-card="${{story.id}}">
            <div class="card-top">
              <div>
                <label class="checkbox-inline" style="margin-bottom:8px;">
                  <input type="checkbox" data-story-select="${{story.id}}" ${{isStorySelected(story.id) ? "checked" : ""}}>
                  <span>${{copy("select", "选择")}}</span>
                </label>
                <h3 class="card-title">${{story.title}}</h3>
                <div class="meta">
                  <span>${{story.id}}</span>
                  <span>${{copy("status", "状态")}}=${{localizeWord(story.status || "active")}}</span>
                  <span>${{copy("updated", "更新")}}=${{updatedLabel}}</span>
                </div>
                <div class="meta">
                  <span>${{copy("items", "条目")}}=${{story.item_count || 0}}</span>
                  <span>${{copy("sources", "来源")}}=${{story.source_count || 0}}</span>
                  <span>${{copy("score", "分数")}}=${{Number(story.score || 0).toFixed(1)}}</span>
                  <span>${{copy("confidence", "置信度")}}=${{Number(story.confidence || 0).toFixed(2)}}</span>
                </div>
              </div>
              <span class="chip ${{(story.contradictions || []).length ? "hot" : "ok"}}">${{(story.contradictions || []).length ? copy("mixed", "冲突") : copy("aligned", "一致")}}</span>
            </div>
            <div class="panel-sub">${{story.summary || copy("No summary captured.", "没有记录到摘要。")}}</div>
            <div class="entity-row">
              <span class="chip ${{priority.tone}}">${{priority.label}}</span>
              ${{(story.entities || []).slice(0, 4).map((entity) => `<span class="chip">${{entity}}</span>`).join("") || `<span class="chip">${{copy("no entities", "无实体")}}</span>`}}
            </div>
            <div class="meta">
              <span>${{copy("primary", "主证据")}}=${{primary ? primary.title : "-"}}</span>
              <span>${{copy("timeline", "时间线")}}=${{(story.timeline || []).length}}</span>
              <span>${{copy("conflicts", "冲突")}}=${{(story.contradictions || []).length}}</span>
            </div>
            <div class="actions">
              <button class="btn-secondary" data-story-open="${{story.id}}">${{copy("Open Story", "打开故事")}}</button>
              <button class="btn-secondary" data-story-preview="${{story.id}}">${{copy("Preview MD", "预览 MD")}}</button>
              <button class="btn-secondary" data-story-quick-status="${{story.id}}" data-story-next-status="${{story.status === "archived" ? "active" : "archived"}}">${{story.status === "archived" ? copy("Restore", "恢复") : copy("Archive", "归档")}}</button>
            </div>
          </div>
        `;
      }}).join("")}}`;

      root.querySelector("[data-story-deck-focus]")?.addEventListener("click", () => {{
        focusStoryDeck("title");
      }});

      root.querySelector("[data-story-search]")?.addEventListener("input", (event) => {{
        state.storySearch = event.target.value;
        renderStories();
      }});

      root.querySelector("[data-story-search-clear]")?.addEventListener("click", () => {{
        state.storySearch = "";
        renderStories();
      }});

      root.querySelector("[data-story-sort]")?.addEventListener("change", (event) => {{
        state.storySort = normalizeStorySort(event.target.value);
        persistStoryWorkspacePrefs();
        renderStories();
      }});

      root.querySelectorAll("[data-story-view]").forEach((button) => {{
        button.addEventListener("click", () => {{
          applyStoryViewPreset(String(button.dataset.storyView || "").trim());
        }});
      }});

      root.querySelector("[data-story-select-visible]")?.addEventListener("click", () => {{
        selectVisibleStories(filteredStories);
        renderStories();
      }});

      root.querySelector("[data-story-selection-clear]")?.addEventListener("click", () => {{
        clearStorySelection();
        renderStories();
      }});

      root.querySelectorAll("[data-story-filter]").forEach((button) => {{
        button.addEventListener("click", () => {{
          state.storyFilter = normalizeStoryFilter(button.dataset.storyFilter);
          persistStoryWorkspacePrefs();
          renderStories();
        }});
      }});

      root.querySelectorAll("[data-story-batch-status]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await runStoryBatchStatusUpdate(state.selectedStoryIds, String(button.dataset.storyBatchStatus || "").trim());
          }} catch (error) {{
            reportError(error, copy("Batch update stories", "批量更新故事"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      root.querySelectorAll("[data-story-card]").forEach((card) => {{
        card.addEventListener("click", (event) => {{
          if (event.target.closest("button, textarea, input, select, a, form, label")) {{
            return;
          }}
          state.selectedStoryId = String(card.dataset.storyCard || "").trim();
          renderStories();
        }});
      }});

      root.querySelectorAll("[data-story-select]").forEach((input) => {{
        input.addEventListener("change", () => {{
          toggleStorySelection(String(input.dataset.storySelect || "").trim(), input.checked);
          renderStories();
        }});
      }});

      root.querySelectorAll("[data-story-open]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await loadStory(button.dataset.storyOpen);
          }} catch (error) {{
            reportError(error, copy("Open story", "打开故事"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      root.querySelectorAll("[data-story-preview]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await previewStoryMarkdown(button.dataset.storyPreview);
          }} catch (error) {{
            reportError(error, copy("Preview story markdown", "预览故事 Markdown"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      root.querySelectorAll("[data-story-quick-status]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          button.disabled = true;
          try {{
            await setStoryStatusQuick(
              String(button.dataset.storyQuickStatus || ""),
              String(button.dataset.storyNextStatus || ""),
            );
          }} catch (error) {{
            reportError(error, copy("Update story state", "更新故事状态"));
          }} finally {{
            button.disabled = false;
          }}
        }});
      }});

      renderStoryDetail();
    }}

    async function refreshBoard() {{
      state.loading.board = true;
      renderOverview();
      renderWatches();
      renderWatchDetail();
      renderAlerts();
      renderRoutes();
      renderRouteHealth();
      renderStatus();
      renderTriage();
      renderStories();
      try {{
        const [overview, watches, alerts, routes, routeHealth, status, ops, triage, triageStats, stories] = await Promise.all([
          api("/api/overview"),
          api("/api/watches?include_disabled=true"),
          api("/api/alerts?limit=8"),
          api("/api/alert-routes"),
          api("/api/alert-routes/health?limit=60"),
          api("/api/watch-status"),
          api("/api/ops"),
          api("/api/triage?limit=12&include_closed=true"),
          api("/api/triage/stats"),
          api("/api/stories?limit=6&min_items=0"),
        ]);
        state.overview = overview;
        state.watches = watches;
        state.alerts = alerts;
        state.routes = routes;
        state.routeHealth = routeHealth;
        state.status = status;
        state.ops = ops;
        state.triage = triage;
        state.triageStats = triageStats;
        state.stories = stories;
        if (state.watches.length) {{
          const selectedWatch = state.watches.some((watch) => watch.id === state.selectedWatchId)
            ? state.selectedWatchId
            : state.watches[0].id;
          state.selectedWatchId = selectedWatch;
          state.watchDetails[selectedWatch] = await api(`/api/watches/${{selectedWatch}}`);
        }} else {{
          state.selectedWatchId = "";
        }}
        if (state.stories.length) {{
          const selected = state.stories.some((story) => story.id === state.selectedStoryId)
            ? state.selectedStoryId
            : state.stories[0].id;
          state.selectedStoryId = selected;
          if (!state.storyDetails[selected]) {{
            const seeded = state.stories.find((story) => story.id === selected);
            if (seeded) {{
              state.storyDetails[selected] = seeded;
            }}
          }}
          if (!state.storyGraph[selected]) {{
            state.storyGraph[selected] = await api(`/api/stories/${{selected}}/graph`);
          }}
        }} else {{
          state.selectedStoryId = "";
        }}
      }} finally {{
        state.loading.board = false;
      }}
      renderOverview();
      renderWatches();
      renderWatchDetail();
      renderAlerts();
      renderRoutes();
      renderRouteHealth();
      renderStatus();
      renderTriage();
      renderStories();
      renderCreateWatchDeck();
    }}

    bindCreateWatchDeck();
    bindRouteDeck();
    bindStoryDeck();
    bindHeroStageMotion();
    bindSectionJumps();
    bindLanguageSwitch();
    bindCommandPalette();
    applyLanguageChrome();
    renderActionHistory();
    renderCommandPalette();
    $("palette-open")?.addEventListener("click", () => {{
      if (state.commandPalette.open) {{
        closeCommandPalette();
      }} else {{
        openCommandPalette();
      }}
    }});

    $("refresh-all").addEventListener("click", async () => {{
      const button = $("refresh-all");
      button.disabled = true;
      try {{
        await refreshBoard();
        showToast(copy("Console refreshed", "控制台已刷新"), "success");
      }} catch (error) {{
        reportError(error, copy("Refresh console", "刷新控制台"));
      }} finally {{
        button.disabled = false;
      }}
    }});
    $("run-due").addEventListener("click", async () => {{
      const button = $("run-due");
      button.disabled = true;
      try {{
        await api("/api/watches/run-due", {{ method: "POST", headers: jsonHeaders, body: JSON.stringify({{ limit: 0 }}) }});
        await refreshBoard();
        showToast(copy("Due missions dispatched", "到点任务已触发执行"), "success");
      }} catch (error) {{
        reportError(error, copy("Run due missions", "执行到点任务"));
      }} finally {{
        button.disabled = false;
      }}
    }});

    $("create-watch-form").addEventListener("submit", async (event) => {{
      event.preventDefault();
      const formElement = event.target;
      const submitButton = formElement.querySelector("button[type='submit']");
      const draft = collectCreateWatchDraft(formElement);
      state.createWatchDraft = draft;
      persistCreateWatchDraft();
      renderCreateWatchDeck();
      if (!(draft.name.trim() && draft.query.trim())) {{
        showToast(
          String(state.createWatchEditingId || "").trim()
            ? copy("Provide both Name and Query before saving changes.", "保存修改前请同时填写名称和查询词。")
            : copy("Provide both Name and Query before creating a watch.", "创建任务前请同时填写名称和查询词。"),
          "error",
        );
        focusCreateWatchDeck(draft.name.trim() ? "query" : "name");
        return;
      }}
      const alertRules = buildAlertRules({{
        route: draft.route.trim(),
        keyword: draft.keyword.trim(),
        domain: draft.domain.trim(),
        minScore: Number(draft.min_score || 0),
        minConfidence: Number(draft.min_confidence || 0),
      }});
      const payload = {{
        name: draft.name.trim(),
        query: draft.query.trim(),
        schedule: draft.schedule.trim() || "manual",
        platforms: draft.platform.trim() ? [draft.platform.trim()] : null,
        alert_rules: alertRules.length ? alertRules : null,
      }};
      const editingId = String(state.createWatchEditingId || "").trim();
      if (submitButton) {{
        submitButton.disabled = true;
      }}
      if (editingId) {{
        try {{
          const updated = await api(`/api/watches/${{editingId}}`, {{
            method: "PUT",
            headers: jsonHeaders,
            body: JSON.stringify(payload),
          }});
          state.selectedWatchId = updated.id || editingId;
          state.watchDetails[state.selectedWatchId] = updated;
          state.createWatchAdvancedOpen = null;
          setCreateWatchDraft(defaultCreateWatchDraft(), "", "");
          formElement.reset();
          pushActionEntry({{
            kind: copy("mission update", "任务修改"),
            label: state.language === "zh" ? `已更新任务：${{payload.name}}` : `Updated ${{payload.name}}`,
            detail: state.language === "zh" ? `任务 ID：${{editingId}}` : `Mission id: ${{editingId}}`,
          }});
          await refreshBoard();
          showToast(
            state.language === "zh" ? `任务已更新：${{payload.name}}` : `Mission updated: ${{payload.name}}`,
            "success",
          );
        }} catch (error) {{
          reportError(error, copy("Update watch", "更新任务"));
        }} finally {{
          if (submitButton) {{
            submitButton.disabled = false;
          }}
        }}
        return;
      }}
      const optimisticId = `draft-${{Date.now()}}`;
      const optimisticWatch = {{
        id: optimisticId,
        name: payload.name,
        query: payload.query,
        enabled: true,
        platforms: payload.platforms || [],
        sites: draft.domain.trim() ? [draft.domain.trim()] : [],
        schedule: payload.schedule,
        schedule_label: payload.schedule,
        is_due: false,
        next_run_at: "",
        alert_rule_count: Array.isArray(payload.alert_rules) ? payload.alert_rules.length : 0,
        alert_rules: payload.alert_rules || [],
        last_run_at: "",
        last_run_status: "pending",
      }};
      state.watches = [optimisticWatch, ...state.watches];
      state.selectedWatchId = optimisticId;
      state.watchDetails[optimisticId] = optimisticWatch;
      renderWatches();
      renderWatchDetail();
      try {{
        const created = await api("/api/watches", {{ method: "POST", headers: jsonHeaders, body: JSON.stringify(payload) }});
        state.createWatchAdvancedOpen = null;
        setCreateWatchDraft(defaultCreateWatchDraft(), "", "");
        formElement.reset();
        pushActionEntry({{
          kind: copy("mission create", "任务创建"),
          label: state.language === "zh" ? `已创建任务：${{payload.name}}` : `Created ${{payload.name}}`,
          detail: copy("The new mission can be removed from the recent action log if this was a false start.", "如果这是误创建，可以在最近操作中直接删除。"),
          undoLabel: copy("Delete mission", "删除任务"),
          undo: async () => {{
            await api(`/api/watches/${{created.id}}`, {{ method: "DELETE" }});
            await refreshBoard();
            showToast(
              state.language === "zh" ? `已删除任务：${{created.name || created.id}}` : `Mission deleted: ${{created.name || created.id}}`,
              "success",
            );
          }},
        }});
        await refreshBoard();
        showToast(
          state.language === "zh" ? `任务已创建：${{payload.name}}` : `Watch created: ${{payload.name}}`,
          "success",
        );
      }} catch (error) {{
        state.watches = state.watches.filter((watch) => watch.id !== optimisticId);
        delete state.watchDetails[optimisticId];
        if (state.selectedWatchId === optimisticId) {{
          state.selectedWatchId = state.watches[0] ? state.watches[0].id : "";
        }}
        renderWatches();
        renderWatchDetail();
        reportError(error, copy("Create watch", "创建任务"));
      }} finally {{
        if (submitButton) {{
          submitButton.disabled = false;
        }}
      }}
    }});

    refreshBoard().catch((error) => {{
      reportError(error, copy("Console boot failed", "控制台启动失败"));
    }});

    document.addEventListener("keydown", (event) => {{
      const target = event.target;
      const tagName = target && target.tagName ? String(target.tagName).toLowerCase() : "";
      const key = String(event.key || "").toLowerCase();
      if ((event.metaKey || event.ctrlKey) && key === "k") {{
        event.preventDefault();
        if (state.commandPalette.open) {{
          closeCommandPalette();
        }} else {{
          openCommandPalette();
        }}
        return;
      }}
      if (key === "escape" && state.commandPalette.open) {{
        event.preventDefault();
        closeCommandPalette();
        return;
      }}
      if (state.commandPalette.open) {{
        return;
      }}
      if (event.metaKey || event.ctrlKey || event.altKey) {{
        return;
      }}
      if (["input", "textarea", "select", "button"].includes(tagName)) {{
        return;
      }}
      if (key === "/") {{
        event.preventDefault();
        focusCreateWatchDeck((state.createWatchDraft && state.createWatchDraft.name.trim()) ? "query" : "name");
        return;
      }}
      if (["1", "2", "3", "4"].includes(key)) {{
        const preset = createWatchPresets[Number(key) - 1];
        if (preset) {{
          event.preventDefault();
          state.createWatchAdvancedOpen = draftHasAdvancedSignal(preset.values);
          setCreateWatchDraft(preset.values, preset.id, "");
          showToast(
            state.language === "zh"
              ? `${{preset.zhLabel || preset.label}} 已载入任务草稿`
              : `${{preset.label}} loaded into the mission deck`,
            "success",
          );
        }}
        return;
      }}
      const visibleItems = getVisibleTriageItems();
      if (!visibleItems.length) {{
        return;
      }}
      const selectedId = state.selectedTriageId || visibleItems[0].id;
      const hasBatchSelection = state.selectedTriageIds.length > 0;
      if (key === "j") {{
        event.preventDefault();
        moveTriageSelection(1);
      }} else if (key === "k") {{
        event.preventDefault();
        moveTriageSelection(-1);
      }} else if (key === "v") {{
        event.preventDefault();
        (hasBatchSelection ? runTriageBatchStateUpdate("verified") : runTriageStateUpdate(selectedId, "verified")).catch((error) => reportError(error, copy("Verify triage item", "核验分诊条目")));
      }} else if (key === "t") {{
        event.preventDefault();
        (hasBatchSelection ? runTriageBatchStateUpdate("triaged") : runTriageStateUpdate(selectedId, "triaged")).catch((error) => reportError(error, copy("Triage item", "分诊条目")));
      }} else if (key === "e") {{
        event.preventDefault();
        (hasBatchSelection ? runTriageBatchStateUpdate("escalated") : runTriageStateUpdate(selectedId, "escalated")).catch((error) => reportError(error, copy("Escalate triage item", "升级分诊条目")));
      }} else if (key === "i") {{
        event.preventDefault();
        (hasBatchSelection ? runTriageBatchStateUpdate("ignored") : runTriageStateUpdate(selectedId, "ignored")).catch((error) => reportError(error, copy("Ignore triage item", "忽略分诊条目")));
      }} else if (key === "s") {{
        event.preventDefault();
        (hasBatchSelection ? createStoryFromTriageItems(state.selectedTriageIds) : createStoryFromTriageItems([selectedId])).catch((error) => reportError(error, copy("Create story from triage", "从分诊生成故事")));
      }} else if (key === "d") {{
        event.preventDefault();
        runTriageExplain(selectedId).catch((error) => reportError(error, copy("Explain duplicates", "查看重复解释")));
      }} else if (key === "n") {{
        event.preventDefault();
        focusTriageNoteComposer(selectedId);
      }}
    }});
  </script>
</body>
</html>"""
