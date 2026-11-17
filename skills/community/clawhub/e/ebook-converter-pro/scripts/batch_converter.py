#!/usr/bin/env python3
"""
batch_converter.py — 批量轉換引擎
自動偵測格式、支援混合輸入、並行處理進度條、轉換報告
"""

import sys
import os
import re
import json
import time
import concurrent.futures
import argparse
import threading
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Literal

# ── Dataclass ─────────────────────────────────────────────────────────────────

@dataclass
class Job:
    input_path:  Path
    output_path: Path
    source_type: Literal["epub","pdf","mobi","azw3","fb2"] = "epub"
    target_fmt:  str = "txt"
    status: Literal["pending","running","done","failed","skipped"] = "pending"
    error:  str = ""
    size_kb: float = 0.0
    duration_ms: int = 0

    def to_dict(self):
        d = asdict(self)
        d["input_path"]  = str(self.input_path)
        d["output_path"] = str(self.output_path)
        return d


# ── Format Detection ──────────────────────────────────────────────────────────

SUPPORTED = {
    "epub":  "epub_converter",
    "pdf":   "pdf_converter",
    "mobi":  "mobi_converter",
    "azw3":  "mobi_converter",
    "fb2":   "fb2_converter",
    "txt":   "txt_converter",
}

FMT_EXT   = {"txt": ".txt", "md": ".md", "html": ".html", "json": ".json"}


def detect_format(p: Path) -> str:
    ext = p.suffix.lower().lstrip(".")
    return ext if ext in SUPPORTED else "unknown"


def build_output(input_p: Path, target_fmt: str, out_dir: Path = None) -> Path:
    out_dir = out_dir or input_p.parent
    ext = FMT_EXT.get(target_fmt, f".{target_fmt}")
    return out_dir / (input_p.stem + ext)


# ── Workers ───────────────────────────────────────────────────────────────────

def _import_converter(name: str):
    if name == "epub_converter":
        import ebook_converter.scripts.epub_converter as m
        return m
    elif name == "pdf_converter":
        import ebook_converter.scripts.pdf_converter as m
        return m
    return None


def _ensure_module():
    """Add scripts dir to path so imports work"""
    skill_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(skill_dir))


def convert_job(job: Job, _lock=threading.Lock()) -> Job:
    """Run one conversion. Mutates & returns job."""
    job.status = "running"
    t0 = time.time()
    job.size_kb = job.input_path.stat().st_size / 1024

    try:
        _ensure_module()
        if job.source_type == "epub":
            from epub_converter import to_txt, to_markdown, to_html_single, to_json
            conv = {"txt": to_txt, "md": to_markdown,
                    "html": to_html_single, "json": to_json}
        elif job.source_type == "pdf":
            from pdf_converter import pdf_to_txt, pdf_to_markdown, pdf_to_images
            conv = {"txt": pdf_to_txt, "md": pdf_to_markdown}
        else:
            job.status = "skipped"
            job.error = f"不支援格式：{job.source_type}"
            return job

        fn = conv.get(job.target_fmt)
        if not fn:
            job.status = "failed"
            job.error = f"目標格式不支援：{job.target_fmt}"
            return job

        fn(job.input_path, job.output_path)
        job.status = "done"

    except Exception as e:
        job.status = "failed"
        job.error  = str(e)[:120]

    job.duration_ms = int((time.time() - t0) * 1000)
    return job


# ── Progress Bar ──────────────────────────────────────────────────────────────

def _bar(done: int, total: int, width: int = 32) -> str:
    filled = int(width * done / total) if total else 0
    pct    = f"{100*done/total:.0f}%" if total else "???"
    return f"\r  [{'█'*filled}{'░'*(width-filled)}] {pct}  {done}/{total}"


# ── Job List Builder ─────────────────────────────────────────────────────────

def scan_inputs(paths: list[Path], recursive: bool,
                source_types: list[str] | None) -> list[Job]:
    jobs: list[Job] = []
    for p in paths:
        if p.is_file():
            fmt = detect_format(p)
            if fmt in SUPPORTED and (not source_types or fmt in source_types):
                jobs.append(Job(input_path=p, output_path=build_output(p, "txt")))
        elif p.is_dir():
            pattern = "**/*" if recursive else "*"
            for child in p.glob(pattern):
                if child.is_file():
                    fmt = detect_format(child)
                    if fmt in SUPPORTED and (not source_types or fmt in source_types):
                        jobs.append(Job(input_path=child,
                                        output_path=build_output(child, "txt")))
    return sorted(jobs, key=lambda j: j.input_path.name)


# ── Report ────────────────────────────────────────────────────────────────────

def generate_report(jobs: list[Job], out_path: Path) -> Path:
    done   = [j for j in jobs if j.status == "done"]
    failed = [j for j in jobs if j.status == "failed"]
    skip   = [j for j in jobs if j.status == "skipped"]

    total_size = sum(j.size_kb for j in done)
    total_time = sum(j.duration_ms for j in done)
    avg_speed  = (total_size / (total_time/1000)) if total_time else 0

    lines = [
        "# 批量轉換報告",
        f"\n**時間：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"\n**統計：**",
        f"- 總任務：{len(jobs)}",
        f"- 成功：{len(done)} ✅",
        f"- 失敗：{len(failed)} ❌",
        f"- 跳過：{len(skip)} ⏭",
        f"- 總大小：{total_size/1024:.1f} MB",
        f"- 平均速度：{avg_speed:.1f} KB/s",
        "\n---\n",
    ]

    if done:
        lines.append("\n## ✅ 成功\n")
        for j in done:
            lines.append(f"- `{j.input_path.name}` → `{j.output_path.name}` "
                         f"({j.size_kb:.0f} KB, {j.duration_ms/1000:.1f}s)")

    if failed:
        lines.append("\n## ❌ 失敗\n")
        for j in failed:
            lines.append(f"- `{j.input_path.name}`：{j.error}")

    if skip:
        lines.append("\n## ⏭ 跳過\n")
        for j in skip:
            lines.append(f"- `{j.input_path.name}`：{j.error}")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="批量轉換工具")
    parser.add_argument("inputs", nargs="+", type=Path, help="檔案或目錄")
    parser.add_argument("-f", "--format", choices=["txt","md","html","json"],
                        default="txt", help="目標格式（預設：txt）")
    parser.add_argument("-o", "--output-dir", type=Path,
                        help="輸出目錄（預設：與來源相同目錄）")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="遞迴掃描子目錄")
    parser.add_argument("-t", "--source-types", nargs="+",
                        choices=list(SUPPORTED.keys()),
                        help="限定來源格式，如 epub pdf")
    parser.add_argument("-j", "--jobs", type=int,
                        default=min(os.cpu_count() or 4, 4),
                        help=f"並行任務數（預設：CPU 核心數）")
    parser.add_argument("--report", action="store_true",
                        help="同時生成 Markdown 轉換報告")
    parser.add_argument("-q", "--quiet", action="store_true")

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    def log(msg):
        if not args.quiet:
            print(msg)

    # Scan
    jobs = scan_inputs(args.inputs, args.recursive, args.source_types)
    if not jobs:
        log("❌ 找不到可轉換的檔案")
        sys.exit(1)

    # Set global output dir
    for j in jobs:
        j.output_path = build_output(j.input_path, args.format, args.output_dir)
        j.target_fmt  = args.format

    log(f"\n📦 發現 {len(jobs)} 個任務（格式：{args.format}）")
    print(_bar(0, len(jobs)), end="", flush=True)

    # Run
    done_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futures = {ex.submit(convert_job, j): j for j in jobs}
        for fut in concurrent.futures.as_completed(futures):
            j = futures[fut]
            try:
                j = fut.result()
            except Exception as e:
                j.status = "failed"
                j.error  = str(e)[:120]
            done_count += 1
            print(_bar(done_count, len(jobs)), end="", flush=True)

    print()  # newline
    done   = [j for j in jobs if j.status == "done"]
    failed = [j for j in jobs if j.status == "failed"]

    log(f"\n✅ 成功：{len(done)}   ❌ 失敗：{len(failed)}")

    if failed and not args.quiet:
        log("\n失敗列表：")
        for j in failed:
            log(f"  • {j.input_path.name}：{j.error}")

    if args.report:
        report_path = (args.output_dir or jobs[0].input_path.parent) / "conversion_report.md"
        generate_report(jobs, report_path)
        log(f"📋 報告已生成：{report_path}")


if __name__ == "__main__":
    main()
