#!/usr/bin/env python3
"""Extract ISBN from a book photo using barcode-first then OCR fallback."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_config import get_env_bool, get_env_int, get_env_str
from common_isbn import extract_isbn_candidates_from_text, to_unique_isbn13
from common_json import fail_and_print, make_result, print_json

STAGE = "extract_isbn"


def _decode_with_zbarimg(image_path: str, binary: str, timeout_sec: int) -> Tuple[List[str], List[str]]:
    """Decode barcode values using zbarimg CLI."""
    warnings: List[str] = []
    values: List[str] = []
    try:
        run = subprocess.run(
            [binary, "--quiet", image_path],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
    except FileNotFoundError:
        return [], [f"zbarimg binary not found: {binary}"]
    except subprocess.TimeoutExpired:
        return [], [f"zbarimg timed out after {timeout_sec}s"]
    except Exception as exc:  # defensive
        return [], [f"zbarimg execution error: {exc}"]

    output = (run.stdout or "") + "\n" + (run.stderr or "")
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            _, value = line.split(":", 1)
            value = value.strip()
        else:
            value = line
        if value:
            values.append(value)

    if run.returncode not in (0, 4) and not values:
        warnings.append(f"zbarimg returned code {run.returncode}")

    return values, warnings


def _decode_with_pyzbar(image_path: str) -> Tuple[List[str], List[str]]:
    """Decode barcode values using pyzbar as an additional barcode pass."""
    try:
        from PIL import Image
    except Exception as exc:
        return [], [f"Pillow unavailable for pyzbar decode: {exc}"]

    try:
        from pyzbar.pyzbar import decode
    except Exception as exc:
        return [], [f"pyzbar unavailable: {exc}"]

    try:
        image = Image.open(image_path)
        decoded = decode(image)
    except Exception as exc:
        return [], [f"pyzbar decode failed: {exc}"]

    values: List[str] = []
    for item in decoded:
        try:
            raw = item.data.decode("utf-8", errors="ignore").strip()
        except Exception:
            continue
        if raw:
            values.append(raw)

    # Sort to keep deterministic output regardless of decode iteration details.
    return sorted(values), []


def _dedupe_texts(texts: List[str]) -> List[str]:
    unique_texts: List[str] = []
    seen = set()
    for text in texts:
        normalized = text.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_texts.append(normalized)
    return unique_texts


def _get_pytesseract_module() -> Optional[Any]:
    try:
        import pytesseract
    except Exception:
        return None
    return pytesseract


def _run_ocr_cli(
    image_path: str,
    lang: str,
    tesseract_cmd: str,
    timeout_sec: int,
) -> Tuple[List[str], List[str]]:
    """Invoke tesseract without a shell when the Python wrapper is unavailable."""
    binary = tesseract_cmd or "tesseract"
    configurations = [[], ["--oem", "3", "--psm", "6"], ["--oem", "3", "--psm", "11"]]
    texts: List[str] = []
    warnings: List[str] = []

    for config in configurations:
        try:
            run = subprocess.run(
                [binary, image_path, "stdout", "-l", lang, *config],
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
            )
        except FileNotFoundError:
            return [], ["tesseract binary not found"]
        except subprocess.TimeoutExpired:
            warnings.append(f"tesseract timed out after {timeout_sec}s")
            continue
        except Exception:
            warnings.append("tesseract execution failed")
            continue

        if run.returncode != 0:
            warnings.append(f"tesseract returned code {run.returncode}")
            continue
        if run.stdout and run.stdout.strip():
            texts.append(run.stdout)

    return _dedupe_texts(texts), sorted(set(warnings))


def _run_ocr(
    image_path: str,
    lang: str,
    tesseract_cmd: str,
    timeout_sec: int = 20,
) -> Tuple[List[str], List[str]]:
    """Run OCR through pytesseract or its direct CLI fallback."""
    pytesseract = _get_pytesseract_module()
    if pytesseract is None:
        texts, warnings = _run_ocr_cli(
            image_path=image_path,
            lang=lang,
            tesseract_cmd=tesseract_cmd,
            timeout_sec=timeout_sec,
        )
        return texts, ["pytesseract unavailable; tesseract CLI fallback attempted", *warnings]

    try:
        from PIL import Image, ImageOps
    except Exception:
        texts, warnings = _run_ocr_cli(
            image_path=image_path,
            lang=lang,
            tesseract_cmd=tesseract_cmd,
            timeout_sec=timeout_sec,
        )
        return texts, ["Pillow unavailable; tesseract CLI fallback attempted", *warnings]

    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    try:
        image = Image.open(image_path)
    except Exception:
        return [], ["could not open image for OCR"]

    variants = [
        image,
        ImageOps.autocontrast(ImageOps.grayscale(image)),
    ]
    configs = ["", "--oem 3 --psm 6", "--oem 3 --psm 11"]

    texts: List[str] = []
    warnings: List[str] = []
    for img in variants:
        for cfg in configs:
            try:
                text = pytesseract.image_to_string(
                    img,
                    lang=lang,
                    config=cfg,
                    timeout=timeout_sec,
                )
            except Exception:
                warnings.append(f"OCR call failed ({cfg or 'default'})")
                continue
            if text and text.strip():
                texts.append(text)

    return _dedupe_texts(texts), warnings


def extract_isbn_from_image(image_path: str) -> dict:
    """Main extraction flow: barcode-first, OCR fallback."""
    warnings: List[str] = []

    if not image_path:
        return make_result(STAGE, ok=False, error="image_path is required", source_image=image_path)

    if not os.path.isfile(image_path):
        return make_result(STAGE, ok=False, error=f"image file not found: {image_path}", source_image=image_path)

    barcode_values: List[str] = []
    enable_zbarimg = get_env_bool("BOOK_CAPTURE_ENABLE_ZBARIMG", True)
    enable_pyzbar = get_env_bool("BOOK_CAPTURE_ENABLE_PYZBAR", True)
    enable_ocr = get_env_bool("BOOK_CAPTURE_ENABLE_OCR", True)

    if enable_zbarimg:
        zbar_bin = get_env_str("BOOK_CAPTURE_ZBARIMG_BIN", "zbarimg")
        timeout_sec = get_env_int("BOOK_CAPTURE_ZBARIMG_TIMEOUT_SECONDS", 8, minimum=1)
        values, warn = _decode_with_zbarimg(image_path=image_path, binary=zbar_bin, timeout_sec=timeout_sec)
        barcode_values.extend(values)
        warnings.extend(warn)

    if enable_pyzbar:
        values, warn = _decode_with_pyzbar(image_path=image_path)
        barcode_values.extend(values)
        warnings.extend(warn)

    barcode_candidates = to_unique_isbn13(barcode_values)
    if barcode_candidates:
        best = barcode_candidates[0]
        return make_result(
            STAGE,
            ok=True,
            error=None,
            source_image=image_path,
            method="barcode",
            isbn13=best,
            isbn_candidates=barcode_candidates,
            warnings=sorted(set(warnings)),
        )

    ocr_candidates: List[str] = []
    if enable_ocr:
        ocr_lang = get_env_str("BOOK_CAPTURE_OCR_LANG", "eng")
        tesseract_cmd = get_env_str("BOOK_CAPTURE_TESSERACT_CMD", "")
        tesseract_timeout_sec = get_env_int(
            "BOOK_CAPTURE_TESSERACT_TIMEOUT_SECONDS", 20, minimum=1
        )
        texts, warn = _run_ocr(
            image_path=image_path,
            lang=ocr_lang,
            tesseract_cmd=tesseract_cmd,
            timeout_sec=tesseract_timeout_sec,
        )
        warnings.extend(warn)
        for text in texts:
            ocr_candidates.extend(extract_isbn_candidates_from_text(text))
        ocr_candidates = to_unique_isbn13(ocr_candidates)

    if ocr_candidates:
        best = ocr_candidates[0]
        return make_result(
            STAGE,
            ok=True,
            error=None,
            source_image=image_path,
            method="ocr",
            isbn13=best,
            isbn_candidates=ocr_candidates,
            warnings=sorted(set(warnings)),
        )

    return make_result(
        STAGE,
        ok=False,
        error="no valid ISBN found via barcode or OCR",
        source_image=image_path,
        method="none",
        isbn13=None,
        isbn_candidates=[],
        warnings=sorted(set(warnings)),
    )


def diagnose_dependencies() -> Dict[str, object]:
    """Report optional dependency availability for portability checks."""
    zbar_bin = get_env_str("BOOK_CAPTURE_ZBARIMG_BIN", "zbarimg")
    tesseract_cmd = get_env_str("BOOK_CAPTURE_TESSERACT_CMD", "")

    try:
        import PIL  # noqa: F401
        pillow_ok = True
        pillow_err = None
    except Exception as exc:
        pillow_ok = False
        pillow_err = str(exc)

    try:
        from pyzbar.pyzbar import decode  # noqa: F401
        pyzbar_ok = True
        pyzbar_err = None
    except Exception as exc:
        pyzbar_ok = False
        pyzbar_err = str(exc)

    try:
        import pytesseract  # noqa: F401
        pytesseract_ok = True
        pytesseract_err = None
    except Exception as exc:
        pytesseract_ok = False
        pytesseract_err = str(exc)

    tesseract_bin = tesseract_cmd or "tesseract"
    return {
        "zbarimg_bin": zbar_bin,
        "zbarimg_available": bool(shutil.which(zbar_bin)),
        "pillow_available": pillow_ok,
        "pillow_error": pillow_err,
        "pyzbar_available": pyzbar_ok,
        "pyzbar_error": pyzbar_err,
        "pytesseract_available": pytesseract_ok,
        "pytesseract_error": pytesseract_err,
        "tesseract_bin": tesseract_bin,
        "tesseract_available": bool(shutil.which(tesseract_bin)),
    }


def _self_check() -> dict:
    """Fast internal checks that do not require external binaries."""
    sample_text = "Example line ISBN 978-1-4919-1889-0 and garbage 12345"
    candidates = extract_isbn_candidates_from_text(sample_text)
    ok = candidates == ["9781491918890"]
    return make_result(
        STAGE,
        ok=ok,
        error=None if ok else "isbn text extraction self-check failed",
        checks={
            "text_candidate_parse": candidates,
        },
    )


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", help="Path to image file")
    parser.add_argument("--self-check", action="store_true", help="Run internal quick checks")
    parser.add_argument("--diagnose-deps", action="store_true", help="Print optional dependency availability")
    args = parser.parse_args(argv)

    if args.self_check:
        result = _self_check()
        print_json(result)
        return 0 if result.get("ok") else 1

    if args.diagnose_deps:
        result = make_result(STAGE, ok=True, error=None, dependencies=diagnose_dependencies())
        print_json(result)
        return 0

    if not args.image:
        return fail_and_print(STAGE, "--image is required", source_image=None)

    result = extract_isbn_from_image(args.image)
    print_json(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
