#!/usr/bin/env python3
"""
Generate a local HTML dashboard (light/white background) to preview resume artifacts.
No external Python dependencies. The HTML pulls Tailwind + Marked + DOMPurify from CDNs.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


ROOT_REL = Path("career/ai-pm-campus")


@dataclass
class Inputs:
    onepage_md: str
    master_points_md: str
    points_by_label: Dict[str, int]
    gaps: List[str]
    generated_at: str


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _collect_points_by_label(master_points_md: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for m in re.finditer(r"(?m)^\-\s*项目标签：\s*(.+?)\s*$", master_points_md):
        label = m.group(1).strip()
        if not label:
            continue
        counts[label] = counts.get(label, 0) + 1
    return counts


def _collect_gaps(onepage_md: str, master_points_md: str) -> List[str]:
    gaps: List[str] = []
    gap_re = re.compile(r"\[待补(?:数据)?[：:]\s*(.+?)\]", re.IGNORECASE)
    
    for text in [onepage_md, master_points_md]:
        for m in gap_re.finditer(text):
            gap = m.group(1).strip()
            if gap and gap not in gaps:
                gaps.append(gap)
    
    return gaps


def _load_inputs() -> Inputs:
    workspace = Path(os.getcwd())
    root = workspace / ROOT_REL
    
    onepage_md = _read_text(root / "outputs" / "resume-onepage.md")
    master_points_md = _read_text(root / "inputs" / "points-pool" / "master-points.md")
    
    points_by_label = _collect_points_by_label(master_points_md)
    gaps = _collect_gaps(onepage_md, master_points_md)
    
    return Inputs(
        onepage_md=onepage_md,
        master_points_md=master_points_md,
        points_by_label=points_by_label,
        gaps=gaps,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


def _render_html(inputs: Inputs) -> str:
    payload = {
        "onepage_md": inputs.onepage_md,
        "points_by_label": inputs.points_by_label,
        "gaps": inputs.gaps,
        "generated_at": inputs.generated_at,
    }
    payload_json = json.dumps(payload, ensure_ascii=False)
    
    return f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>AI PM Resume Hub — Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {{
        theme: {{
          extend: {{
            boxShadow: {{
              card: "0 10px 40px rgba(0,0,0,.08), 0 2px 8px rgba(0,0,0,.04)",
            }},
            colors: {{
              primary: '#0071e3',
              secondary: '#34c759',
              neutral: '#86868b',
              danger: '#ff3b30',
            }}
          }},
        }},
      }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dompurify@3.0.8/dist/purify.min.js"></script>
    <style>
      /* Light mode typography */
      .md h1, .md h2, .md h3 {{ color: #1d1d1f; font-weight: 650; letter-spacing: -0.02em; }}
      .md p, .md li {{ color: #424245; line-height: 1.6; }}
      .md code {{ color: #1d1d1f; background: #f5f5f7; padding: .12rem .35rem; border-radius: .5rem; }}
      .md a {{ color: #0071e3; text-decoration: none; }}
      .md a:hover {{ text-decoration: underline; }}
      .md ul {{ list-style: disc; padding-left: 1.25rem; }}
    </style>
  </head>
  <body class="min-h-screen bg-white text-gray-900 font-sans tracking-tight">
    <main class="relative mx-auto max-w-6xl px-5 py-10 md:px-10">
      <header class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <div class="inline-flex items-center gap-2 rounded-full border border-gray-200 bg-gray-50 px-3 py-1 text-xs text-gray-600">
            <span class="h-1.5 w-1.5 rounded-full bg-primary shadow-[0_0_8px_rgba(0,113,227,.4)]"></span>
            <span>AI PM Resume Hub</span>
          </div>
          <h1 class="mt-3 text-3xl md:text-4xl font-semibold text-gray-900">简历可视化仪表盘</h1>
          <p class="mt-2 text-sm md:text-base text-gray-600">一页简历、要点池统计与 Gap 清单集中预览。</p>
        </div>
        <div class="flex items-center gap-3">
          <button id="toggleRaw" class="rounded-2xl border border-gray-200 bg-white px-4 py-2 text-sm text-gray-700 shadow-card transition-all duration-300 ease-out hover:bg-gray-50 hover:scale-[1.01]">
            切换 Raw/渲染
          </button>
          <div class="rounded-2xl border border-gray-200 bg-white px-4 py-2 text-sm text-gray-600 shadow-card">
            生成时间：<span id="genAt" class="text-gray-900"></span>
          </div>
        </div>
      </header>

      <section class="mt-8 grid grid-cols-1 gap-5 md:grid-cols-12">
        <!-- One-page -->
        <div class="group md:col-span-7 rounded-3xl border border-gray-200 bg-white shadow-card transition-all duration-300 ease-out hover:shadow-lg">
          <div class="flex items-center justify-between px-6 pt-6">
            <div>
              <h2 class="text-lg font-semibold text-gray-900">一页简历</h2>
              <p class="mt-1 text-sm text-gray-600">来自 resume-onepage.md</p>
            </div>
            <span class="rounded-full border border-primary/20 bg-primary/5 px-3 py-1 text-xs text-primary">Primary</span>
          </div>
          <div class="px-6 pb-6 pt-4">
            <div id="onepage" class="md prose max-w-none prose-headings:tracking-tight"></div>
            <pre id="onepageRaw" class="hidden whitespace-pre-wrap rounded-2xl border border-gray-200 bg-gray-50 p-4 text-xs text-gray-700"></pre>
            <div id="onepageEmpty" class="hidden rounded-2xl border border-dashed border-gray-200 bg-gray-50 p-6 text-gray-600">
              没有检测到一页简历文件内容。请先生成 <code>resume-onepage.md</code>。
            </div>
          </div>
        </div>

        <!-- Right column -->
        <div class="md:col-span-5 grid grid-cols-1 gap-5">
          <!-- Gaps -->
          <div class="rounded-3xl border border-gray-200 bg-white shadow-card transition-all duration-300 ease-out hover:shadow-lg">
            <div class="px-6 pt-6">
              <h2 class="text-lg font-semibold text-gray-900">Gap 清单</h2>
              <p class="mt-1 text-sm text-gray-600">聚合所有 <code>[待补数据：...]</code></p>
            </div>
            <div class="px-6 pb-6 pt-4">
              <ul id="gaps" class="space-y-2"></ul>
              <div id="gapsEmpty" class="hidden rounded-2xl border border-dashed border-gray-200 bg-gray-50 p-6 text-gray-600">
                暂无待补数据标签。
              </div>
            </div>
          </div>

          <!-- Points by label -->
          <div class="rounded-3xl border border-gray-200 bg-white shadow-card transition-all duration-300 ease-out hover:shadow-lg">
            <div class="px-6 pt-6">
              <h2 class="text-lg font-semibold text-gray-900">要点池统计</h2>
              <p class="mt-1 text-sm text-gray-600">按项目标签聚合（master-points.md）</p>
            </div>
            <div class="px-6 pb-6 pt-4">
              <div id="pointsBars" class="space-y-2"></div>
              <div id="pointsEmpty" class="hidden rounded-2xl border border-dashed border-gray-200 bg-gray-50 p-6 text-gray-600">
                暂无要点统计。请先运行 extract 生成 master-points.md。
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer class="mt-8 text-xs text-gray-500">
        提示：这是本地预览页，不会上传任何内容。你可以反复运行 visualize 覆盖生成。
      </footer>
    </main>

    <script id="resumeData" type="application/json">{payload_json}</script>
    <script>
      const data = JSON.parse(document.getElementById('resumeData').textContent);
      document.getElementById('genAt').textContent = data.generated_at || '-';

      const mdToHtml = (md) => {{
        if (!md) return '';
        const raw = marked.parse(md, {{ gfm: true, breaks: false }});
        return DOMPurify.sanitize(raw);
      }};

      const setMdPane = (id, rawId, emptyId, md) => {{
        const pane = document.getElementById(id);
        const rawPane = document.getElementById(rawId);
        const empty = document.getElementById(emptyId);
        if (!md || !md.trim()) {{
          pane.classList.add('hidden');
          rawPane.classList.add('hidden');
          empty.classList.remove('hidden');
          return;
        }}
        empty.classList.add('hidden');
        pane.innerHTML = mdToHtml(md);
        rawPane.textContent = md;
      }};

      // Render gaps
      const renderGaps = () => {{
        const gaps = data.gaps || [];
        const container = document.getElementById('gaps');
        const empty = document.getElementById('gapsEmpty');
        if (!gaps.length) {{
          container.classList.add('hidden');
          empty.classList.remove('hidden');
          return;
        }}
        empty.classList.add('hidden');
        container.innerHTML = gaps.map(gap => `
          <li class="flex items-start gap-2 text-sm">
            <span class="mt-0.5 h-4 w-4 flex-shrink-0 rounded-full bg-danger/20 flex items-center justify-center">
              <span class="h-1.5 w-1.5 rounded-full bg-danger"></span>
            </span>
            <span class="text-gray-700">${{gap}}</span>
          </li>
        `).join('');
      }};

      // Render points bars
      const renderPointsBars = () => {{
        const points = data.points_by_label || {{}};
        const container = document.getElementById('pointsBars');
        const empty = document.getElementById('pointsEmpty');
        const entries = Object.entries(points).sort((a, b) => b[1] - a[1]);
        if (!entries.length) {{
          container.classList.add('hidden');
          empty.classList.remove('hidden');
          return;
        }}
        empty.classList.add('hidden');
        const max = Math.max(...entries.map(([k, v]) => v));
        container.innerHTML = entries.map(([label, count]) => {{
          const pct = Math.round((count / max) * 100);
          return `
            <div class="space-y-1">
              <div class="flex items-center justify-between text-xs">
                <span class="text-gray-700 font-medium">${{label}}</span>
                <span class="text-gray-500">${{count}} 条</span>
              </div>
              <div class="h-2 rounded-full bg-gray-100 overflow-hidden">
                <div class="h-full rounded-full bg-gradient-to-r from-primary to-secondary" style="width: ${{pct}}%"></div>
              </div>
            </div>
          `;
        }}).join('');
      }};

      // Toggle raw/rendered
      let rawMode = false;
      document.getElementById('toggleRaw').addEventListener('click', () => {{
        rawMode = !rawMode;
        const onepage = document.getElementById('onepage');
        const onepageRaw = document.getElementById('onepageRaw');
        if (rawMode) {{
          onepage.classList.add('hidden');
          onepageRaw.classList.remove('hidden');
          document.getElementById('toggleRaw').textContent = '切换到渲染模式';
        }} else {{
          onepage.classList.remove('hidden');
          onepageRaw.classList.add('hidden');
          document.getElementById('toggleRaw').textContent = '切换 Raw/渲染';
        }}
      }});

      // Initial render
      setMdPane('onepage', 'onepageRaw', 'onepageEmpty', data.onepage_md);
      renderGaps();
      renderPointsBars();
    </script>
  </body>
</html>
"""


def main():
    inputs = _load_inputs()
    html = _render_html(inputs)
    out_path = Path(os.getcwd()) / ROOT_REL / "outputs" / "resume-dashboard.html"
    _ensure_parent(out_path)
    out_path.write_text(html, encoding="utf-8")
    print(out_path.resolve())
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
