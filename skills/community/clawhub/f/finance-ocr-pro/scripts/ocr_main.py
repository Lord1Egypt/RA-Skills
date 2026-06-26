"""
OCR Pipeline — end-to-end document extraction.

Converts a source document into page images, extracts content via VLM,
and produces Markdown, HTML comparison, DOCX, and Excel outputs.
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPT_DIR.parent
DEFAULT_OUTPUT_DIR = Path.cwd() / "ocr_output"

if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from ocr_runtime import NullProgressReporter, ProgressReporter

_preflight_done = False
_IMAGE_EXTS = {".jpeg", ".jpg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


def _preflight() -> None:
    """Validate local dependencies and .env before the pipeline runs.

    Skips silently on subsequent calls within the same process.
    """
    global _preflight_done
    if _preflight_done:
        return

    from ocr_setup import check_packages, check_env, bootstrap_env, python_install_command

    missing_pkgs = check_packages()
    if missing_pkgs:
        sys.exit(
            f"[preflight] Missing packages: {', '.join(missing_pkgs)}\n"
            "[preflight] Automatic installation is disabled for security.\n"
            f"  Run manually: {python_install_command()}"
        )

    missing_env = check_env()
    env_path = _SKILL_ROOT / ".env"
    if missing_env and not env_path.exists():
        bootstrap_env()
        missing_env = check_env()
    if missing_env:
        sys.exit(
            f"[preflight] Missing required config: {', '.join(missing_env)}\n"
            f"  Please edit {env_path} with your VLM credentials.\n"
            f"  Run: python scripts/ocr_setup.py   (for interactive guided setup)"
        )

    _preflight_done = True


def ocr_main(
    source_file: str | Path,
    threads: int = 1,
    reporter: ProgressReporter | None = None,
    project_dir: str | Path | None = None,
    resume: bool = False,
) -> Path:
    """
    Run the full OCR pipeline on *source_file*.

    Args:
        source_file:       Path to the document to process.
        threads:           Number of concurrent OCR threads (default: 1).

    Returns the project directory containing all outputs.
    """
    reporter = reporter or NullProgressReporter()

    reporter.step_started("preflight", "Preflight checks")
    _preflight()
    reporter.step_completed("preflight")

    from docs_to_image import document_to_images
    from image_to_md import image_folder_to_md
    from md_to_html import markdown_to_html
    from md_to_docx import markdown_to_docx
    from md_to_excel import markdown_folder_to_excel

    file_path = Path(source_file).resolve()
    if not file_path.is_file():
        raise FileNotFoundError(f"Source file not found: {file_path}")

    file_name = file_path.stem
    if project_dir is not None:
        project_dir = Path(project_dir).resolve()
    else:
        project_dir = DEFAULT_OUTPUT_DIR / f"OCR_{file_name}"
    image_dir = project_dir / "images"
    markdown_dir = project_dir / "markdowns"
    results_dir = project_dir / "results"
    combined_md_path = results_dir / f"{file_name}_combined.md"
    html_path = results_dir / f"{file_name}.html"
    docx_path = results_dir / f"{file_name}.docx"
    excel_path = results_dir / f"{file_name}.xlsx"

    for folder in (project_dir, image_dir, markdown_dir, results_dir):
        folder.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  OCR Pipeline — {file_path.name}")
    print(f"  Project folder: {project_dir}")
    print(f"{'='*60}\n")

    reporter.check_cancelled()
    reporter.step_started("render_pages", "Converting document to images")
    print("[Step 1/5] Converting document to images …")
    existing_images = sorted(
        p for p in image_dir.iterdir()
        if p.is_file() and p.suffix.lower() in _IMAGE_EXTS
    )
    if resume and existing_images:
        print(f"[Resume] Reusing {len(existing_images)} existing page image(s).")
        reporter.log(f"Reusing {len(existing_images)} existing page image(s).")
    else:
        document_to_images(file_path, output_dir=image_dir, reporter=reporter)
        existing_images = sorted(
            p for p in image_dir.iterdir()
            if p.is_file() and p.suffix.lower() in _IMAGE_EXTS
        )
    if not existing_images:
        raise RuntimeError(
            "No page images were generated from the source document. "
            "Check the input file and any required system converters."
        )
    reporter.pages_discovered(len(existing_images))
    reporter.step_completed("render_pages")

    reporter.check_cancelled()
    reporter.step_started("ocr_pages", "Extracting page content via VLM")
    print("\n[Step 2/5] Extracting page content via VLM …")
    succeeded_pages, failed_pages = image_folder_to_md(
        image_dir,
        markdown_dir,
        combined_md_path,
        threads=threads,
        reporter=reporter,
        resume=resume,
    )
    if failed_pages:
        raise RuntimeError(
            f"OCR failed for {failed_pages} of {succeeded_pages + failed_pages} page image(s). "
            "Partial outputs were retained so the job can be resumed."
        )
    reporter.artifact_ready("combined_md", combined_md_path)
    reporter.step_completed("ocr_pages")

    reporter.check_cancelled()
    reporter.step_started("build_html", "Generating HTML comparison report")
    print("\n[Step 3/5] Generating HTML comparison report …")
    markdown_to_html(image_dir, markdown_dir, html_path)
    reporter.artifact_ready("html", html_path)
    reporter.step_completed("build_html")

    reporter.check_cancelled()
    reporter.step_started("build_docx", "Generating DOCX document")
    print("\n[Step 4/5] Generating DOCX document …")
    markdown_to_docx(combined_md_path, docx_path)
    reporter.artifact_ready("docx", docx_path)
    reporter.step_completed("build_docx")

    reporter.check_cancelled()
    reporter.step_started("build_excel", "Generating Excel workbook")
    print("\n[Step 5/5] Generating Excel workbook …")
    markdown_folder_to_excel(markdown_dir, excel_path)
    reporter.artifact_ready("excel", excel_path)
    reporter.step_completed("build_excel")

    reporter.check_cancelled()
    reporter.step_started("finalize", "Finalizing outputs")
    print("\n[Cleanup] Removing intermediate files …")
    freed = 0
    for d in (image_dir, markdown_dir):
        if d.is_dir():
            for f in d.rglob("*"):
                if f.is_file():
                    freed += f.stat().st_size
            shutil.rmtree(d)
    print(f"  Freed {freed / (1024 * 1024):.1f} MB")

    reporter.step_completed("finalize")
    print(f"\nAll done.  Outputs in: {results_dir}")
    return project_dir


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="OCR pipeline: document → images → Markdown → HTML + DOCX + XLSX",
    )
    parser.add_argument("file", help="Path to the source document.")
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=1,
        help="Number of concurrent OCR threads (default: 1; raise only if the API plan supports parallel OCR requests).",
    )
    args = parser.parse_args()

    ocr_main(
        args.file,
        threads=args.threads,
    )
