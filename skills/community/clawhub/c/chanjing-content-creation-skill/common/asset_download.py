"""将蝉镜结果 URL 下载到本地 output 子目录。"""
from __future__ import annotations

import os
import urllib.parse
import urllib.request
from pathlib import Path


def infer_download_filename(url: str, default_basename: str) -> str:
    parsed = urllib.parse.urlparse(url)
    name = Path(parsed.path).name or default_basename
    if "." not in name:
        name += ".bin"
    return name


def download_chanjing_result_url(
    url: str,
    *,
    outputs_subdir: str,
    user_agent: str,
    default_basename: str,
    output_path: Path | None = None,
    timeout: int = 120,
) -> Path:
    """
    下载到 output_path；若未指定则写入
    skills/chanjing-content-creation-skill/output/<outputs_subdir>/<推断文件名>。
    失败时抛出 RuntimeError（与原有脚本语义一致，便于 CLI 捕获）。
    """
    skill_root = Path(__file__).resolve().parents[1]
    default_dir = skill_root / "output" / outputs_subdir
    dest = output_path if output_path is not None else default_dir / infer_download_filename(url, default_basename)
    dest.parent.mkdir(parents=True, exist_ok=True)

    req = urllib.request.Request(url, headers={"User-Agent": user_agent}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp, open(dest, "wb") as handle:
            handle.write(resp.read())
    except Exception as exc:
        raise RuntimeError(f"下载失败: {exc}") from exc

    if not dest.exists() or dest.stat().st_size == 0:
        raise RuntimeError("下载失败: 输出文件为空")

    return dest


def print_downloaded_path(path: Path) -> None:
    print(os.fspath(path))
