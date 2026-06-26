"""
VLM OCR 处理器
读取 vlm_queue.jsonl → pdftoppm转图片 → spawn sub-agent分析 → 保存结果JSON

用法:
  python3 vlm_ocr.py                  # 全量处理队列
  python3 vlm_ocr.py --limit 5       # 限制数量（测试）
  python3 vlm_ocr.py --dry-run        # 只显示队列，不处理
"""
import json
import subprocess
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime

RAW_DIR = Path(__file__).parent.parent.parent / "cfc_raw_data"
VLM_QUEUE = RAW_DIR / "vlm_queue.jsonl"
VLM_OUT_DIR = RAW_DIR / "vlm_results"


def pdf_to_images(pdf_path: Path, out_dir: Path, max_pages: int = 5) -> list[Path]:
    """用 pdftoppm 将 PDF 转为 PNG 图片列表。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ['pdftoppm', '-r', '150', '-l', str(max_pages),
             '-png', '-f', '1', str(pdf_path), str(out_dir / 'page')],
            capture_output=True, timeout=120
        )
        return sorted(out_dir.glob('page-*.png'))
    except Exception:
        return []


def parse_vlm_response(text: str) -> list[dict]:
    """从 VLM 输出文本中解析出公司名+电话列表。"""
    # VLM 应返回纯 JSON 数组
    start = text.find('[')
    end = text.rfind(']') + 1
    if start == -1 or end == 0:
        return []
    try:
        data = json.loads(text[start:end])
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict) and d.get('name')]
    except Exception:
        pass
    return []


def build_prompt(dtype: str) -> str:
    """根据披露类型构建分析提示词。"""
    base = (
        "这是一张消费金融公司合作机构公示的截图。\n"
        "请仔细识别图中所有条目，提取每个公司的【名称】和【联系电话】。\n"
        "返回格式：纯JSON数组，不要其他文字：\n"
        "[{\"name\":\"公司全称\",\"phone\":\"电话\"},...]\n"
        "如果某个条目没有电话，phone填空字符串。\n"
        "只返回JSON数组。"
    )
    return base


def process_queue(limit: int = None, dry_run: bool = False) -> dict:
    """
    读取队列，启动 sub-agent 进行 VLM OCR。
    支持 pdf_path（PDF转图片）和 image_path（直接图片）两种队列条目。
    返回处理统计。
    """
    if not VLM_QUEUE.exists():
        print(f"VLM queue empty: {VLM_QUEUE}")
        return {}

    VLM_OUT_DIR.mkdir(parents=True, exist_ok=True)
    stats = {"total": 0, "ok": 0, "fail": 0, "skipped": 0}
    entries = []

    with open(VLM_QUEUE) as f:
        lines = [l.strip() for l in f if l.strip()]

    if limit:
        lines = lines[:limit]

    print(f"VLM OCR: {len(lines)} items in queue")

    for i, line in enumerate(lines):
        item = json.loads(line)
        dtype = item['dtype']
        date = item['date']

        # 判断是 PDF 还是图片
        pdf_path_str = item.get('pdf_path')
        img_path_str = item.get('image_path')

        if img_path_str:
            # 图片条目：直接分析
            img_path = Path(img_path_str)
            print(f"\n[{i+1}/{len(lines)}] [image] {img_path.name}")
            if not img_path.exists():
                print(f"  SKIP: image not found")
                stats["skipped"] += 1
                continue
            if dry_run:
                stats["skipped"] += 1
                continue
            img_paths = [img_path]
            img_dir = VLM_OUT_DIR / img_path.stem
            img_dir.mkdir(parents=True, exist_ok=True)
        elif pdf_path_str:
            # PDF条目：转图片后分析
            pdf_path = Path(pdf_path_str)
            print(f"\n[{i+1}/{len(lines)}] [pdf] {pdf_path.name}")
            if not pdf_path.exists():
                print(f"  SKIP: PDF not found")
                stats["skipped"] += 1
                continue
            size_kb = pdf_path.stat().st_size // 1024
            print(f"  PDF size: {size_kb}KB, type: {dtype}, date: {date}")
            img_dir = VLM_OUT_DIR / pdf_path.stem
            img_paths = pdf_to_images(pdf_path, img_dir, max_pages=3)
            if not img_paths:
                print(f"  FAIL: pdftoppm failed")
                stats["fail"] += 1
                stats["total"] += 1
                continue
            print(f"  Images: {[p.name for p in img_paths]}")
            if dry_run:
                stats["skipped"] += 1
                continue
        else:
            print(f"  SKIP: unknown entry type")
            stats["skipped"] += 1
            continue

        # 调用 VLM 分析
        prompt = build_prompt(dtype)
        try:
            from tools.image import image as img_tool
            result = img_tool({
                "images": [str(p) for p in img_paths],
                "prompt": prompt
            })
            print(f"  VLM result (first 300 chars): {str(result)[:300]}")
            entities = parse_vlm_response(str(result))
            if entities:
                out_file = img_dir / "result.json"
                with open(out_file, 'w') as f:
                    json.dump(entities, f, ensure_ascii=False, indent=2)
                print(f"  OK: {len(entities)} entities saved to {out_file.name}")
                stats["ok"] += 1
            else:
                print(f"  FAIL: no entities parsed from VLM response")
                stats["fail"] += 1
        except Exception as e:
            print(f"  FAIL: {e}")
            stats["fail"] += 1

        stats["total"] += 1

    print(f"\nVLM OCR done: {stats}")
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=None)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    process_queue(limit=args.limit, dry_run=args.dry_run)
