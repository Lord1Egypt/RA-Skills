#!/usr/bin/env python3
"""可插拔 OCR 后端。

不同平台/不同 agent 环境能用的 OCR 能力差别很大，所以做成后端可切换：

| 后端 | 平台 | 依赖 | 说明 |
| --- | --- | --- | --- |
| `winrt` | Windows | `winrt-*` 包（pip 可装，有 wheel） | 用系统内置 `Windows.Media.Ocr`，离线、快、中文效果好 |
| `tesseract` | 全平台 | `tesseract` 可执行文件 + `chi_sim` 语言包 | 跨平台兜底；有 `pytesseract` 就用，没有就直接调 CLI |
| `none` | 全平台 | 无 | 不识别，只产出裁好的字幕图 + 清单，**交给具备视觉能力的 agent 直接读图** |

`auto` 的选择顺序：winrt → tesseract → none。

对 Claude Code / Codex 这类有视觉能力的 agent，`none` 其实是完全可行的路线：
图片已经裁好并按时间戳命名，agent 直接读图即可，省掉一切 OCR 依赖。
"""
from __future__ import annotations

import os
import shutil
import subprocess
from typing import Dict, Iterable, List, Tuple

BACKENDS = ("auto", "winrt", "tesseract", "none")


def _winrt_available() -> bool:
    if os.name != "nt":
        return False
    try:
        import winrt.windows.media.ocr  # noqa: F401
        return True
    except Exception:
        return False


def _tesseract_available() -> bool:
    return shutil.which("tesseract") is not None


def resolve_backend(name: str) -> Tuple[str, str]:
    """把 auto 解析成具体后端。返回 (backend, 说明)。"""
    name = (name or "auto").strip().lower()
    if name != "auto":
        return name, "用户指定"
    if _winrt_available():
        return "winrt", "自动选择：检测到 Windows 内置 OCR"
    if _tesseract_available():
        return "tesseract", "自动选择：检测到 tesseract"
    return "none", "自动选择：无可用 OCR 引擎，改为输出图片交给 agent 读图"


def _ocr_winrt(paths: List[str]) -> Dict[str, str]:
    """Windows 内置 OCR。"""
    import asyncio

    from winrt.windows.globalization import Language
    from winrt.windows.graphics.imaging import (BitmapAlphaMode, BitmapDecoder,
                                                BitmapPixelFormat)
    from winrt.windows.media.ocr import OcrEngine
    from winrt.windows.storage import FileAccessMode, StorageFile

    engine = OcrEngine.try_create_from_language(Language("zh-Hans-CN"))
    if not engine:
        engine = OcrEngine.try_create_from_user_profile_languages()
    if not engine:
        raise RuntimeError(
            "系统未安装中文 OCR 语言包。Windows 设置 → 时间和语言 → 语言 → "
            "中文(简体) → 语言选项 → 光学字符识别")

    async def one(path: str) -> str:
        sf = await StorageFile.get_file_from_path_async(os.path.abspath(path))
        stream = await sf.open_async(FileAccessMode.READ)
        try:
            decoder = await BitmapDecoder.create_async(stream)
            # OCR 只接受 Bgra8。注意 winrt-py 的重载参数个数与文档不一致：
            # get_software_bitmap_async() 必须 0 参；
            # get_software_bitmap_converted_async(fmt, alpha) 必须 2 参。
            bmp = await decoder.get_software_bitmap_converted_async(
                BitmapPixelFormat.BGRA8, BitmapAlphaMode.PREMULTIPLIED)
            res = await engine.recognize_async(bmp)
            return res.text or ""
        finally:
            stream.close()

    async def all_of() -> Dict[str, str]:
        out: Dict[str, str] = {}
        for p in paths:
            try:
                out[os.path.basename(p)] = await one(p)
            except Exception as e:
                out[os.path.basename(p)] = f"OCR_ERROR: {e}"
        return out

    return asyncio.run(all_of())


def _ocr_tesseract(paths: List[str], lang: str = "chi_sim+eng") -> Dict[str, str]:
    """跨平台 OCR。优先 pytesseract，否则直接调 CLI。"""
    out: Dict[str, str] = {}
    try:
        import pytesseract  # type: ignore
        from PIL import Image
        for p in paths:
            try:
                out[os.path.basename(p)] = pytesseract.image_to_string(
                    Image.open(p), lang=lang)
            except Exception as e:
                out[os.path.basename(p)] = f"OCR_ERROR: {e}"
        return out
    except ImportError:
        pass

    for p in paths:
        try:
            proc = subprocess.run(
                ["tesseract", p, "stdout", "-l", lang],
                capture_output=True, timeout=120)
            text = proc.stdout.decode("utf-8", "replace") if proc.stdout else ""
            if proc.returncode != 0 and not text:
                text = f"OCR_ERROR: {proc.stderr.decode('utf-8', 'replace')[:200]}"
            out[os.path.basename(p)] = text
        except Exception as e:
            out[os.path.basename(p)] = f"OCR_ERROR: {e}"
    return out


def ocr_images(paths: Iterable[str], backend: str = "auto",
               tess_lang: str = "chi_sim+eng") -> Tuple[Dict[str, str], str]:
    """对一批图片做 OCR。返回 (文件名 -> 文本, 实际使用的后端)。"""
    paths = list(paths)
    resolved, _why = resolve_backend(backend)
    # 所有 jpg 都跑；主流程只关心 *_n / *_i 两种变体
    if resolved == "winrt":
        return _ocr_winrt(paths), "winrt"
    if resolved == "tesseract":
        return _ocr_tesseract(paths, tess_lang), "tesseract"
    if resolved == "none":
        return {os.path.basename(p): "" for p in paths}, "none"
    raise ValueError(f"未知 OCR 后端: {backend}（可选 {', '.join(BACKENDS)}）")
