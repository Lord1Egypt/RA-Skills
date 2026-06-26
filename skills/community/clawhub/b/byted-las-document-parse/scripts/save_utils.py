"""
save_utils.py — 解析结果多格式保存、图片本地化、TOS 归档

放置路径: scripts/save_utils.py
被 skill.py 的 check-and-notify 命令调用

Output directory structure (task_id as folder):
  /tmp/las_parse_{task_id}/
  ├── result.md              (images replaced with local paths)
  ├── result.full.json       (complete API response)
  ├── images/
  │   ├── p1_000.png
  │   └── ...
  └── images.json            (image manifest)
"""

from __future__ import annotations

import json
import os
import re
import time
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# 智能 Preview
# ---------------------------------------------------------------------------

def extract_smart_preview(md: str, max_chars: int = 500) -> str:
    """从 markdown 中提取有意义的预览文本，跳过 HTML table 标签。

    策略:
    1. 提取文档标题和纯文本段落（跳过 HTML 和图片语法）
    2. 从 <th> 中提取表格字段名
    3. 从 <td> 中提取首行数据
    4. 统计图片数量
    5. 提取末尾备注文本
    """
    lines = md.split("\n")
    parts: list[str] = []

    # 1) 标题 + 纯文本行
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("<") or s.startswith("!["):
            continue
        parts.append(s)
        if len("\n".join(parts)) > 150:
            break

    # 2) 表头字段
    th_matches = re.findall(r"<th[^>]*>(.*?)</th>", md, re.DOTALL)
    if th_matches:
        headers: list[str] = []
        for h in th_matches:
            h = re.sub(r"<[^>]+>", "", h).strip()
            if h and h not in headers:
                headers.append(h)
        if headers:
            parts.append(f"[表格字段: {', '.join(headers[:10])}]")

    # 3) 首行数据
    td_matches = re.findall(r"<td[^>]*>(.*?)</td>", md, re.DOTALL)
    if td_matches:
        cells = [re.sub(r"<[^>]+>", "", t).strip() for t in td_matches[:13]]
        cells = [c for c in cells if c]
        if cells:
            parts.append(f"[首行数据: {', '.join(cells[:8])}...]")

    # 4) 图片统计
    img_count = len(re.findall(r"!\[.*?\]\(.*?\)", md))
    if img_count:
        parts.append(f"[含 {img_count} 张图片]")

    # 5) 末尾备注
    for line in reversed(lines):
        s = line.strip()
        if s and not s.startswith("<") and not s.startswith("!["):
            if s not in "\n".join(parts):
                parts.append(s)
            break

    preview = "\n".join(parts)
    return preview[:max_chars] + "..." if len(preview) > max_chars else preview


# ---------------------------------------------------------------------------
# 图片清单提取
# ---------------------------------------------------------------------------

def _extract_image_info(res: Dict[str, Any]) -> List[Dict[str, Any]]:
    """从完整 API 响应中提取所有图片的 URL + 位置信息。"""
    images: list[dict] = []
    for page in res.get("data", {}).get("detail", []):
        page_id = page.get("page_id", 0)
        for block in page.get("text_blocks", []):
            if block.get("label") == "image" and block.get("url"):
                images.append({
                    "page": page_id,
                    "url": block["url"],
                    "box": block.get("box"),
                })
    return images


def _get_image_expiry_hours(images: List[Dict]) -> Optional[int]:
    """从图片 URL 的 TOS 签名参数中提取过期时间（小时）。"""
    if not images:
        return None
    m = re.search(r"X-Tos-Expires=(\d+)", images[0].get("url", ""))
    return int(m.group(1)) // 3600 if m else None


# ---------------------------------------------------------------------------
# 图片下载
# ---------------------------------------------------------------------------

def _download_image(url: str, dest: Path, max_retries: int = 2) -> bool:
    """下载单张图片到本地，支持重试。成功返回 True。"""
    import requests

    for attempt in range(max_retries + 1):
        try:
            r = requests.get(url, timeout=30, stream=True)
            r.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            if attempt < max_retries:
                time.sleep(1 * (attempt + 1))
                continue
            print(f"✗ 下载图片失败: {url} -> {e}", file=__import__("sys").stderr)
            return False


def _download_all_images(
    images: List[Dict[str, Any]],
    images_dir: Path,
) -> List[Dict[str, Any]]:
    """批量下载所有图片到 images_dir，返回更新后的 images 列表。

    每个 image dict 新增字段:
      - local_path: 绝对路径
      - local_relative: 相对于 task_dir 的路径 (e.g. images/p1_000.png)
      - downloaded: bool
    """
    images_dir.mkdir(parents=True, exist_ok=True)

    for i, img in enumerate(images):
        page = img.get("page", 0)
        # 从 URL 推断扩展名
        parsed = urlparse(img["url"])
        ext = Path(parsed.path).suffix.lower()
        if ext not in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"):
            ext = ".png"

        filename = f"p{page}_{i:03d}{ext}"
        dest = images_dir / filename

        ok = _download_image(img["url"], dest)
        img["local_path"] = str(dest)
        img["local_relative"] = f"images/{filename}"
        img["downloaded"] = ok

    return images


# ---------------------------------------------------------------------------
# Markdown 图片链接替换
# ---------------------------------------------------------------------------

def _replace_image_urls_in_markdown(
    md: str,
    images: List[Dict[str, Any]],
) -> str:
    """将 Markdown 中的远程图片 URL 替换为本地相对路径。

    仅替换已成功下载的图片。
    """
    for img in images:
        if not img.get("downloaded"):
            continue
        remote_url = img["url"]
        local_rel = img["local_relative"]
        # 替换 markdown 图片语法中的 URL
        md = md.replace(remote_url, local_rel)
    return md


# ---------------------------------------------------------------------------
# TOS 归档上传
# ---------------------------------------------------------------------------

def _create_zip_archive(task_dir: Path, task_id: str) -> Path:
    """将 task_dir 下的所有结果文件打包成 zip。

    压缩包内部目录结构:
      {task_id}/
      ├── result.md
      ├── result.full.json
      ├── images.json
      └── images/
          ├── p1_000.png
          └── ...

    Returns: zip 文件的路径
    """
    zip_path = task_dir / f"{task_id}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(task_dir.rglob("*")):
            if file_path.is_file() and file_path != zip_path:
                arcname = f"{task_id}/{file_path.relative_to(task_dir)}"
                zf.write(file_path, arcname)

    _log = lambda msg: __import__("builtins").print(msg, file=__import__("sys").stderr)
    zip_size_mb = zip_path.stat().st_size / 1024 / 1024
    _log(f"压缩包已创建: {zip_path} ({zip_size_mb:.2f} MB)")
    return zip_path


def _upload_results_to_tos(
    task_dir: Path,
    task_id: str,
    tos_bucket: str,
    tos_prefix: str = "las_pdf_parse",
    region: Optional[str] = None,
    presign_expires: int = 86400,
) -> Dict[str, Any]:
    """将解析结果打包上传到 TOS 并生成预签名下载 URL。

    流程:
      1. 将 task_dir 打包为 {task_id}.zip
      2. 上传 zip 到 TOS: {prefix}/{task_id}/{task_id}.zip
      3. 生成预签名下载 URL（默认 24 小时有效）

    Returns:
        {
            "tos_internal_path": "tos://bucket/key"  (内部追溯，不可直接下载),
            "tos_key": "prefix/task_id/result/task_id.zip",
            "archive_size_mb": 0.15,
            "download_url": "https://...signed_url..."  (可能为 None),
            "download_url_expires_hours": 24,
            "presign_error": "..."  (仅当预签名失败时),
        }
    """
    import sys as _sys
    from tos_utils import upload_to_tos, get_tos_bucket, generate_presigned_download_url

    actual_bucket = get_tos_bucket(tos_bucket)
    zip_key = f"{tos_prefix.rstrip('/')}/{task_id}/result/{task_id}.zip"

    # 1. 打包
    zip_path = _create_zip_archive(task_dir, task_id)

    # 2. 上传
    upload_to_tos(str(zip_path), actual_bucket, zip_key, region=region)
    tos_internal = f"tos://{actual_bucket}/{zip_key}"

    result: Dict[str, Any] = {
        "tos_internal_path": tos_internal,  # 内部路径(tos://...)，不可直接下载，仅供内部追溯
        "tos_key": zip_key,
        "archive_size_mb": round(zip_path.stat().st_size / (1024 * 1024), 2),
    }

    # 3. 生成预签名下载 URL（独立 try/except，不影响上传结果）
    try:
        download_url = generate_presigned_download_url(
            actual_bucket, zip_key, expires=presign_expires, region=region,
        )
        result["download_url"] = download_url
        result["download_url_expires_hours"] = presign_expires // 3600
    except Exception as presign_err:
        result["download_url"] = None
        result["presign_error"] = str(presign_err)
        print(f"\u2717 预签名 URL 生成失败: {presign_err}", file=_sys.stderr)

    # 清理本地 zip
    try:
        zip_path.unlink()
    except OSError:
        pass

    return result


# ---------------------------------------------------------------------------
# 主入口：多格式保存
# ---------------------------------------------------------------------------

def save_parse_result(
    res: Dict[str, Any],
    output_dir: str,
    task_id: Optional[str] = None,
    tos_bucket: Optional[str] = None,
    tos_prefix: str = "las_results",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """多格式保存解析结果，支持图片本地化和 TOS 归档。

    Args:
        res: 完整 API 响应 dict
        output_dir: 输出目录路径（如 /tmp/las_parse_{task_id}）
        task_id: 任务 ID（用于 TOS 归档路径）
        tos_bucket: TOS bucket 名称（提供则归档到 TOS）
        tos_prefix: TOS 归档路径前缀
        region: TOS/LAS region

    Output directory:
      {output_dir}/
      ├── result.md              (images replaced with local paths)
      ├── result.full.json       (complete API response)
      ├── images/
      │   ├── p1_000.png
      │   └── ...
      └── images.json            (image manifest)

    Returns: 结构化摘要 dict，用于 check-and-notify 的 stdout JSON
    """
    task_dir = Path(output_dir)
    task_dir.mkdir(parents=True, exist_ok=True)

    data = res.get("data", {})
    md = data.get("markdown", "")
    saved_files: list[str] = []

    # --- 提取图片信息 ---
    images = _extract_image_info(res)

    # --- 下载图片到本地 ---
    downloaded_count = 0
    if images:
        images_dir = task_dir / "images"
        images = _download_all_images(images, images_dir)
        downloaded_count = sum(1 for img in images if img.get("downloaded"))

        # 替换 Markdown 中的图片 URL 为本地路径
        if downloaded_count > 0:
            md = _replace_image_urls_in_markdown(md, images)

    # --- 保存 result.md (with local image paths) ---
    md_path = task_dir / "result.md"
    md_path.write_text(md, encoding="utf-8")
    saved_files.append(str(md_path))

    # --- 保存 result.full.json ---
    json_path = task_dir / "result.full.json"
    json_path.write_text(
        json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    saved_files.append(str(json_path))

    # --- 保存 images.json (image manifest) ---
    if images:
        img_manifest_path = task_dir / "images.json"
        img_manifest_path.write_text(
            json.dumps(images, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        saved_files.append(str(img_manifest_path))

    # --- 统计 ---
    page_count = len(data.get("detail", []))
    table_count = md.count("<table")
    image_count = len(images)
    expiry_hours = _get_image_expiry_hours(images)

    result: Dict[str, Any] = {
        "status": "COMPLETED",
        "output_dir": str(task_dir),
        "output_file": str(md_path),  # 向后兼容
        "saved_files": saved_files,
        "markdown_size": len(md.encode("utf-8")),
        "page_count": page_count,
        "table_count": table_count,
        "image_count": image_count,
        "image_downloaded": downloaded_count,
        "preview": extract_smart_preview(md),
    }

    if expiry_hours is not None:
        result["image_expiry_hours"] = expiry_hours
        if downloaded_count < image_count:
            result["image_expiry_warning"] = (
                f"图片URL将在{expiry_hours}小时后过期，"
                f"{image_count - downloaded_count}张图片未能下载"
            )

    # --- TOS 归档（打包 zip + 预签名下载 URL）---
    if tos_bucket:
        try:
            tos_result = _upload_results_to_tos(
                task_dir, task_id or "unknown", tos_bucket,
                tos_prefix=tos_prefix, region=region,
            )
            result.update(tos_result)
        except Exception as e:
            result["tos_error"] = str(e)
            print(f"✗ TOS 归档失败: {e}", file=__import__("sys").stderr)


    # --- 安全兜底检查 ---
    if tos_bucket and "download_url" not in result and "tos_error" not in result:
        result["tos_error"] = "TOS 归档未执行（未知原因）"
    if result.get("download_url") is None and "tos_error" not in result and "presign_error" not in result:
        if tos_bucket:
            result["download_url_missing_reason"] = "预签名 URL 生成失败，请检查 TOS 凭证配置"

    return result
