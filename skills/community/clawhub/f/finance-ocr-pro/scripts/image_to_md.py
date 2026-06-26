"""Batch OCR: extract Markdown from a folder of page images via VLM."""

from __future__ import annotations

import argparse
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from ai_service_vlm import ai_request  # noqa: E402
from ocr_prompt import ocr_to_markdown  # noqa: E402
from ocr_runtime import CancellationRequested, NullProgressReporter, ProgressReporter  # noqa: E402

logger = logging.getLogger(__name__)

IMAGE_EXTS: set[str] = {".jpeg", ".jpg", ".png", ".webp", ".bmp", ".tiff", ".tif"}

DEFAULT_MAX_ATTEMPTS = 2
DEFAULT_RETRY_DELAY = 2.0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _collect_images(folder: Path) -> list[Path]:
    """Return supported image files in *folder*, sorted by name."""
    return sorted(
        (p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS),
        key=lambda p: p.name,
    )


def _ocr_single_image(
    image_path: Path,
    *,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    retry_delay: float = DEFAULT_RETRY_DELAY,
) -> str:
    """Send one image to the VLM, retrying on transient failures."""
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return ai_request(prompt=ocr_to_markdown, image_url=str(image_path))
        except Exception as exc:
            last_exc = exc
            if attempt < max_attempts:
                wait = retry_delay * attempt
                logger.warning(
                    "Attempt %d/%d failed for %s (%s); retrying in %.1fs …",
                    attempt, max_attempts, image_path.name, exc, wait,
                )
                time.sleep(wait)
    raise RuntimeError(
        f"All {max_attempts} attempts failed for {image_path.name}"
    ) from last_exc


def _build_combined_markdown(
    pages: list[tuple[int, str]],
    *,
    page_marker: bool = True,
) -> str:
    """Assemble per-page markdown texts into one document.

    Each page is separated by a blank line.  When *page_marker* is True a
    ``Page_Order_N`` sentinel line is inserted before each page (consumed
    downstream by md_to_docx for page-break insertion).
    """
    sections: list[str] = []
    for order, text in pages:
        text = text.strip()
        if not text:
            continue
        if page_marker:
            sections.append(f"Page_Order_{order}\n\n{text}")
        else:
            sections.append(text)
    return "\n\n".join(sections) + "\n"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def _process_one(
    order: int,
    image_path: Path,
    page_folder: Path,
    total: int,
    reporter: ProgressReporter,
) -> tuple[int, str]:
    """OCR a single image and write its page ``.md`` file.

    Returns ``(order, md_text)`` on success; propagates exceptions so the
    caller can record the failure without aborting other workers.
    """
    reporter.check_cancelled()
    print(f"[{order}/{total}] OCR scanning: {image_path.name}")
    md_text = _ocr_single_image(image_path)
    reporter.check_cancelled()
    page_file = page_folder / f"{image_path.stem}.md"
    page_file.write_text(md_text, encoding="utf-8")
    print(f"  [OK]   {image_path.name} → {page_file.name}")
    reporter.page_done(order, total)
    return order, md_text


def image_folder_to_md(
    source_folder: Path,
    page_folder: Path,
    combined_file: Path,
    page_marker: bool = True,
    threads: int = 1,
    reporter: ProgressReporter | None = None,
    resume: bool = False,
) -> tuple[int, int]:
    """OCR every image in *source_folder*, write individual ``.md`` files
    into *page_folder*, and merge them into *combined_file*.

    When *threads* > 1 images are processed concurrently.  Each image is
    independent: a failure in one thread does not affect the others.
    """
    reporter = reporter or NullProgressReporter()
    images = _collect_images(source_folder)
    if not images:
        logger.warning("No supported images found in %s", source_folder)
        print(f"[WARN] No supported images in {source_folder}")
        return 0, 0

    page_folder.mkdir(parents=True, exist_ok=True)
    combined_file.parent.mkdir(parents=True, exist_ok=True)

    total = len(images)
    pages: list[tuple[int, str]] = []
    failed: list[str] = []
    pending: list[tuple[int, Path]] = []

    for order, img in enumerate(images, start=1):
        reporter.check_cancelled()
        page_file = page_folder / f"{img.stem}.md"
        if resume and page_file.exists():
            try:
                pages.append((order, page_file.read_text(encoding="utf-8")))
                print(f"[{order}/{total}] Reusing existing OCR: {page_file.name}")
                reporter.page_done(order, total, skipped=True)
                continue
            except Exception as exc:
                logger.warning("Could not reuse %s (%s); OCR will run again.", page_file.name, exc)
        pending.append((order, img))

    with ThreadPoolExecutor(max_workers=max(1, threads)) as executor:
        future_to_img = {
            executor.submit(_process_one, order, img, page_folder, total, reporter): img
            for order, img in pending
        }
        for future in as_completed(future_to_img):
            img = future_to_img[future]
            try:
                pages.append(future.result())
            except CancellationRequested:
                raise
            except Exception as exc:
                logger.error("Failed: %s — %s", img.name, exc)
                print(f"  [FAIL] {img.name}: {exc}")
                failed.append(img.name)
                try:
                    order = next(order for order, pending_img in pending if pending_img == img)
                except StopIteration:
                    order = 0
                if order:
                    reporter.page_failed(order, total, str(exc))

    pages.sort(key=lambda t: t[0])
    reporter.check_cancelled()

    combined_file.write_text(
        _build_combined_markdown(pages, page_marker=page_marker),
        encoding="utf-8",
    )

    succeeded = total - len(failed)
    summary = f"Done — {succeeded} succeeded, {len(failed)} failed out of {total} images."
    print(f"\n{summary}")
    if failed:
        print("Failed images:")
        for name in failed:
            print(f"  - {name}")

    return succeeded, len(failed)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    parser = argparse.ArgumentParser(description="Batch OCR images to Markdown via VLM.")
    parser.add_argument("source_folder", type=Path, help="Folder containing source images.")
    parser.add_argument("page_folder", type=Path, help="Output folder for individual page .md files.")
    parser.add_argument("combined_file", type=Path, help="Path for the combined Markdown file.")
    parser.add_argument("--no-page-marker", action="store_true", help="Omit page markers in the combined file.")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of concurrent OCR threads (default: 1).")
    args = parser.parse_args()

    image_folder_to_md(
        source_folder=args.source_folder,
        page_folder=args.page_folder,
        combined_file=args.combined_file,
        page_marker=not args.no_page_marker,
        threads=args.threads,
    )


if __name__ == "__main__":
    main()
