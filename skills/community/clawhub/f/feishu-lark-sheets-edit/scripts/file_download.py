#!/usr/bin/env python3
"""Download a Lark/Feishu file by file link using the OpenClaw Feishu app credentials.

- Reads appId/appSecret from ~/.openclaw/openclaw.json (OpenClaw config)
- Fetches tenant_access_token
- Calls Feishu/Lark Drive OpenAPI to download the file content
- For PDF files, automatically extracts text to a .txt file for easy reading

Usage examples:
  python3 file_download.py --url "https://.../file/YOUR_FILE_TOKEN" --out /tmp/report.pdf
  python3 file_download.py --file-token YOUR_FILE_TOKEN --out /tmp/report.pdf
  python3 file_download.py --file-token YOUR_FILE_TOKEN --out /tmp/doc.bin --extract-text

Notes:
- This script targets the Drive File Download API endpoint:
  GET /open-apis/drive/v1/files/:file_token/download
- The caller must ensure the app/bot has permission to access the file (shared to the app).
- Text extraction uses pdfplumber → pypdf → poppler fallback chain (auto pip-installed).
- If text is garbled/unreadable, pages are rendered to images for visual reading.
- Image extraction uses pypdf → poppler fallback.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

OPENCLAW_CONFIG = os.environ.get(
    "OPENCLAW_CONFIG",
    os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json"),
)


def _read_openclaw_feishu_config(path: str = OPENCLAW_CONFIG) -> tuple[str, str, str]:
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    feishu = (cfg.get("channels") or {}).get("feishu") or {}
    app_id = feishu.get("appId")
    app_secret = feishu.get("appSecret")
    domain = feishu.get("domain") or "feishu"  # "lark" or "feishu"

    if not app_id or not app_secret:
        raise RuntimeError(
            f"Missing channels.feishu.appId/appSecret in {path}. "
            "Run `openclaw configure` or set OPENCLAW_CONFIG."
        )

    return app_id, app_secret, domain


def _base_url(domain: str) -> str:
    domain = (domain or "").lower().strip()
    if domain == "lark":
        return "https://open.larksuite.com"
    return "https://open.feishu.cn"


def _http_json(method: str, url: str, headers: dict[str, str] | None = None, body: dict | None = None, timeout: int = 30):
    import json as _json

    data = None
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)

    if body is not None:
        data = _json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method.upper())
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    try:
        return _json.loads(raw)
    except _json.JSONDecodeError:
        raise RuntimeError(f"Non-JSON response from {url}: {raw[:2000]}")


def _get_tenant_access_token(app_id: str, app_secret: str, base: str) -> str:
    url = base + "/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": app_id, "app_secret": app_secret}
    j = _http_json("POST", url, body=payload)

    if j.get("code") != 0:
        raise RuntimeError(f"Failed to get tenant_access_token: code={j.get('code')} msg={j.get('msg')}")

    token = (j.get("tenant_access_token") or "").strip()
    if not token:
        raise RuntimeError("tenant_access_token missing in response")
    return token


def _extract_file_token(url: str) -> str | None:
    """Extract file token from a Lark/Feishu file URL.

    Example:
      https://xxx.larksuite.com/file/YOUR_FILE_TOKEN
      -> file_token = YOUR_FILE_TOKEN
    """

    m = re.search(r"/file/([A-Za-z0-9]+)", url)
    return m.group(1) if m else None


def _download_file(file_token: str, access_token: str, base: str, out_path: str, timeout: int = 300):
    """Download file content via Feishu Drive API and save to out_path.

    API: GET /open-apis/drive/v1/files/:file_token/download
    The response is binary file content (not JSON).
    """

    endpoint = f"{base}/open-apis/drive/v1/files/{file_token}/download"
    headers = {"Authorization": f"Bearer {access_token}"}

    req = urllib.request.Request(endpoint, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()

    with open(out_path, "wb") as f:
        f.write(data)


def _pip_install(*packages: str):
    """Install packages via pip if not already present."""
    subprocess.run(
        [sys.executable, "-m", "pip", "install", *packages],
        check=True,
        capture_output=True,
    )


def _ensure_import(module_name: str, pip_name: str | None = None):
    """Import a module, auto-installing via pip if missing."""
    import importlib
    try:
        return importlib.import_module(module_name)
    except ImportError:
        pip_pkg = pip_name or module_name
        print(f"{pip_pkg} not found, installing via pip...", file=sys.stderr)
        _pip_install(pip_pkg)
        return importlib.import_module(module_name)


def _is_readable_text(text: str, threshold: float = 0.3) -> bool:
    """Check if extracted text is readable (not garbled).

    Returns True if the ratio of common readable characters (letters, digits,
    common CJK, punctuation, whitespace) to total characters exceeds threshold.
    """
    if not text or len(text.strip()) < 20:
        return False
    readable = 0
    for ch in text:
        cp = ord(ch)
        if (
            ch.isalnum() or ch.isspace()
            or cp in range(0x4E00, 0x9FFF + 1)   # CJK Unified
            or cp in range(0x3000, 0x303F + 1)   # CJK punctuation
            or cp in range(0xFF00, 0xFFEF + 1)   # Fullwidth forms
            or ch in '.,;:!?\'"-()[]{}/@#$%^&*+=<>~`_|\\'
        ):
            readable += 1
    return (readable / len(text)) > threshold


def _extract_text_from_pdf(pdf_path: str, txt_path: str) -> tuple[str, bool]:
    """Extract text from a PDF file and save to txt_path.

    Priority: pdfplumber → pypdf → pdftotext (poppler).
    Returns (txt_path, is_readable) — is_readable indicates if text is usable.
    """

    content = ""

    # 1. Try pdfplumber (best for complex fonts/encodings)
    try:
        pdfplumber = _ensure_import("pdfplumber")
        pages_text = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                if text.strip():
                    pages_text.append(f"--- Page {i + 1} ---\n{text}")
        content = "\n\n".join(pages_text)
        if _is_readable_text(content):
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(content)
            return txt_path, True
        print("pdfplumber: extracted text appears garbled, trying next...", file=sys.stderr)
    except Exception as e:
        print(f"pdfplumber failed: {e}", file=sys.stderr)

    # 2. Try pypdf
    try:
        pypdf = _ensure_import("pypdf")
        reader = pypdf.PdfReader(pdf_path)
        pages_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages_text.append(f"--- Page {i + 1} ---\n{text}")
        content = "\n\n".join(pages_text)
        if _is_readable_text(content):
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(content)
            return txt_path, True
        print("pypdf: extracted text appears garbled, trying next...", file=sys.stderr)
    except Exception as e:
        print(f"pypdf failed: {e}", file=sys.stderr)

    # 3. Try pdftotext (poppler)
    if shutil.which("pdftotext"):
        subprocess.run(
            ["pdftotext", "-layout", pdf_path, txt_path],
            check=True,
            capture_output=True,
        )
        with open(txt_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        if _is_readable_text(content):
            return txt_path, True
        print("pdftotext: extracted text appears garbled", file=sys.stderr)

    # Write whatever we got (even if garbled) as best-effort
    if content:
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(content)

    return txt_path, False


def _render_pdf_pages_to_images(pdf_path: str, out_dir: str) -> list[str]:
    """Render each PDF page as a PNG image for visual reading.

    Priority: pymupdf (fitz) → pdf2image (poppler-based).
    Returns list of image paths.
    """

    os.makedirs(out_dir, exist_ok=True)
    images: list[str] = []

    # 1. Try pymupdf (fitz) — no system deps, pip-installable
    try:
        fitz = _ensure_import("fitz", "pymupdf")
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150)
            img_path = os.path.join(out_dir, f"page-{i + 1:03d}.png")
            pix.save(img_path)
            images.append(img_path)
        doc.close()
        return images
    except Exception as e:
        print(f"pymupdf page rendering failed: {e}", file=sys.stderr)

    # 2. Fallback to pdf2image (needs poppler system package)
    try:
        pdf2image = _ensure_import("pdf2image")
        pil_images = pdf2image.convert_from_path(pdf_path, dpi=150)
        for i, pil_img in enumerate(pil_images):
            img_path = os.path.join(out_dir, f"page-{i + 1:03d}.png")
            pil_img.save(img_path, "PNG")
            images.append(img_path)
        return images
    except Exception as e:
        print(f"pdf2image page rendering failed: {e}", file=sys.stderr)

    return images


def _extract_images_from_pdf(pdf_path: str, out_dir: str) -> list[str]:
    """Extract embedded images from a PDF.

    Priority: pypdf → pdfimages (poppler).
    Saves images as PNG/JPEG files in out_dir. Returns list of extracted image paths.
    """

    os.makedirs(out_dir, exist_ok=True)
    images: list[str] = []

    # 1. Try pypdf
    try:
        pypdf = _ensure_import("pypdf")
        reader = pypdf.PdfReader(pdf_path)
        idx = 0
        for page in reader.pages:
            for image_obj in page.images:
                ext = os.path.splitext(image_obj.name)[1] or ".png"
                img_path = os.path.join(out_dir, f"img-{idx:03d}{ext}")
                with open(img_path, "wb") as f:
                    f.write(image_obj.data)
                images.append(img_path)
                idx += 1
        if images:
            return images
    except Exception as e:
        print(f"pypdf image extraction failed: {e}", file=sys.stderr)

    # 2. Fallback to pdfimages (poppler)
    if shutil.which("pdfimages"):
        prefix = os.path.join(out_dir, "img")
        subprocess.run(
            ["pdfimages", "-png", pdf_path, prefix],
            check=True,
            capture_output=True,
        )
        images = sorted(
            os.path.join(out_dir, f)
            for f in os.listdir(out_dir)
            if f.startswith("img") and f.endswith(".png")
        )

    return images


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", help="Lark/Feishu file URL")
    ap.add_argument("--file-token", help="File token (the part after /file/)")
    ap.add_argument("--out", required=True, help="Output path for downloaded file")
    ap.add_argument(
        "--extract-text",
        action="store_true",
        help="For PDF files, also extract text to a .txt file for easy reading",
    )
    args = ap.parse_args()

    file_token = args.file_token
    if not file_token and args.url:
        file_token = _extract_file_token(args.url)

    if not file_token:
        raise SystemExit("Missing file token. Provide --file-token or --url containing /file/<token>.")

    app_id, app_secret, domain = _read_openclaw_feishu_config()
    base = _base_url(domain)
    access_token = _get_tenant_access_token(app_id, app_secret, base)

    _download_file(file_token, access_token, base, args.out)
    print(f"OK: downloaded file_token={file_token} to {args.out}")

    # Auto-detect PDF or honor --extract-text
    is_pdf = args.out.lower().endswith(".pdf")
    if args.extract_text or is_pdf:
        base_name = os.path.splitext(args.out)[0]
        txt_path = base_name + ".txt"
        text_readable = False

        # Step 1: Extract text
        try:
            _, text_readable = _extract_text_from_pdf(args.out, txt_path)
            if text_readable:
                print(f"OK: extracted text to {txt_path}")
            else:
                print(f"WARNING: extracted text appears garbled in {txt_path}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: text extraction failed: {e}", file=sys.stderr)

        # Step 2: Extract embedded images
        img_dir = base_name + "_images"
        try:
            images = _extract_images_from_pdf(args.out, img_dir)
            if images:
                print(f"OK: extracted {len(images)} embedded image(s) to {img_dir}/")
                for img in images:
                    print(f"  - {img}")
            else:
                if os.path.isdir(img_dir) and not os.listdir(img_dir):
                    os.rmdir(img_dir)
        except Exception as e:
            print(f"Warning: image extraction failed: {e}", file=sys.stderr)

        # Step 3: If text is garbled, render pages to images for visual reading
        if not text_readable:
            pages_dir = base_name + "_pages"
            print("Text is not readable. Rendering PDF pages to images...", file=sys.stderr)
            try:
                page_images = _render_pdf_pages_to_images(args.out, pages_dir)
                if page_images:
                    print(f"OK: rendered {len(page_images)} page(s) to {pages_dir}/")
                    print(f"    Use the Read tool to view these images for content analysis.")
                    for img in page_images:
                        print(f"  - {img}")
                else:
                    print("Warning: page rendering produced no images", file=sys.stderr)
            except Exception as e:
                print(f"Warning: page rendering failed: {e}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
