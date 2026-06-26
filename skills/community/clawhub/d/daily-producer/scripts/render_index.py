#!/usr/bin/env python3
"""
生成日报导航首页 output/index.html。

扫描 output/daily/ 下所有已生成的 JSON 日报文件，
按日期倒序列出，输出一个简单的导航页面。
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any


def resolve_root_dir() -> Path:
    env_root = os.environ.get("DAILY_ROOT") or os.environ.get("AI_DAILY_ROOT")
    candidates: list[Path] = []
    if env_root:
        candidates.append(Path(env_root).expanduser())

    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    script_dir = Path(__file__).resolve().parent
    candidates.extend([script_dir, *script_dir.parents])

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (
            (candidate / "SKILL.md").exists()
            and (candidate / "reference" / "daily_example.html").exists()
            and (candidate / "scripts" / "render_index.py").exists()
        ):
            return candidate

    return script_dir.parent


ROOT_DIR = resolve_root_dir()
DAILY_DIR = ROOT_DIR / "output" / "daily"
INDEX_PATH = ROOT_DIR / "output" / "index.html"

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def h(value: Any) -> str:
    return escape("" if value is None else str(value), quote=True)


def scan_dailies() -> list[dict[str, Any]]:
    """扫描 output/daily/*.json，提取日期和基本信息。"""
    results = []
    for json_path in sorted(DAILY_DIR.glob("*.json"), reverse=True):
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            continue
        meta = payload.get("meta", {})
        date_str = meta.get("date", json_path.stem)
        articles = payload.get("articles", [])
        html_path = json_path.with_suffix(".html")
        results.append(
            {
                "date": date_str,
                "date_label": meta.get("date_label", ""),
                "role": meta.get("role", ""),
                "article_count": len(articles),
                "has_html": html_path.exists(),
                "html_name": f"daily/{html_path.name}",
            }
        )
    return results


def format_date_label(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{dt.year}年{dt.month}月{dt.day}日 · {WEEKDAYS[dt.weekday()]}"
    except ValueError:
        return date_str


def render_index(dailies: list[dict[str, Any]]) -> str:
    rows = []
    for d in dailies:
        label = d["date_label"] or format_date_label(d["date"])
        count = d["article_count"]
        role = d["role"]
        if d["has_html"]:
            link = f'<a href="{h(d["html_name"])}" class="text-accent hover:underline font-medium">{h(label)}</a>'
        else:
            link = f'<span class="text-gray-400">{h(label)}（未渲染）</span>'
        role_badge = (
            f'<span class="bg-[#F3F0FF] text-accent text-xs px-2 py-0.5 rounded-full">{h(role)}</span>'
            if role
            else ""
        )
        rows.append(
            f"""      <tr class="border-b border-gray-50 hover:bg-gray-50/50">
        <td class="py-3 px-4">{link}</td>
        <td class="py-3 px-4 text-center text-sm text-gray-500">{count} 条</td>
        <td class="py-3 px-4 text-center">{role_badge}</td>
      </tr>"""
        )

    table_body = "\n".join(rows) if rows else (
        '      <tr><td colspan="3" class="py-8 text-center text-gray-400">暂无日报，运行 /ai-daily 生成第一份</td></tr>'
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>日报 · 导航</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            primary: '#1A1A2E',
            accent: '#6C5CE7',
          }}
        }}
      }}
    }}
  </script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif; }}
  </style>
</head>
<body class="bg-[#FAFBFC] text-primary min-h-screen">
  <div class="max-w-3xl mx-auto py-12 px-6">
    <h1 class="text-2xl font-bold mb-1">
      <i class="fa-solid fa-newspaper text-accent mr-2"></i>日报
    </h1>
    <p class="text-gray-400 text-sm mb-8">共 {len(dailies)} 期</p>

    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-100 text-gray-400 text-xs uppercase">
            <th class="py-3 px-4 text-left font-medium">日期</th>
            <th class="py-3 px-4 text-center font-medium">资讯</th>
            <th class="py-3 px-4 text-center font-medium">角色</th>
          </tr>
        </thead>
        <tbody>
{table_body}
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
"""


def main() -> None:
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    dailies = scan_dailies()
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(render_index(dailies), encoding="utf-8")
    print(f"Rendered {INDEX_PATH} ({len(dailies)} entries)")


if __name__ == "__main__":
    main()
