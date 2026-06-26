from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .ark_client import configure_response_logging
from .config import ConfigError, Settings
from .material_generate_service import MaterialGenerationService


def configure_logging() -> None:
    """Configure CLI logging for visible progress output."""
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    log_path = configure_response_logging()
    logging.getLogger(__name__).info("Responses API logs are written to %s", log_path)


def _find_single_product_image(assets_dir: Path) -> Path:
    """Find a single product image file under assets/ for convenience defaults."""
    if not assets_dir.exists():
        raise FileNotFoundError(f"assets directory not found: {assets_dir}")
    if not assets_dir.is_dir():
        raise ValueError(f"assets path is not a directory: {assets_dir}")

    exts = {".png", ".jpg", ".jpeg", ".webp"}
    candidates = sorted([p for p in assets_dir.iterdir() if p.is_file() and p.suffix.lower() in exts])
    if not candidates:
        raise FileNotFoundError(
            f"No product image found under {assets_dir}. Put one image there or pass --image explicitly."
        )
    if len(candidates) > 1:
        names = ", ".join(p.name for p in candidates[:10])
        raise ValueError(
            f"Multiple product images found under {assets_dir}: {names}. "
            "Keep only one image there or pass --image explicitly."
        )
    return candidates[0]


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        prog="dpp-generate-material",
        description="Generate a single-product material config JSON from a local product image.",
    )
    parser.add_argument(
        "--image",
        default=None,
        help="Optional path to the product image. If omitted, auto-detects a single image under assets/.",
    )
    parser.add_argument(
        "--output",
        default="configs/placement_material.json",
        help="Output JSON path. Default: configs/placement_material.json (overwrites).",
    )
    parser.add_argument("--model", default=None, help="Optional model or endpoint override.")
    parser.add_argument("--brand", default=None, help="Optional brand hint (LLM may infer if omitted).")
    parser.add_argument(
        "--product-name",
        default=None,
        help="Optional product name hint (LLM may infer if omitted).",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=1,
        help="Format-repair retries after validation failure. Default: 1.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """解析命令行参数并生成 material config JSON。"""
    configure_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    logger = logging.getLogger(__name__)

    try:
        settings = Settings.from_env()
        service = MaterialGenerationService(settings)

        repo_root = Path.cwd().expanduser().resolve()
        image_path = (
            Path(args.image).expanduser()
            if args.image
            else _find_single_product_image(repo_root / "assets")
        )

        # When writing to configs/, store a stable relative reference to assets/.
        output_path = Path(args.output).expanduser()
        output_abs = (repo_root / output_path).resolve() if not output_path.is_absolute() else output_path.resolve()
        image_abs = (repo_root / image_path).resolve() if not image_path.is_absolute() else image_path.resolve()
        try:
            image_path_for_config = image_abs.relative_to(output_abs.parent).as_posix()
        except ValueError:
            image_path_for_config = str(image_abs)

        logger.info("Using product image: %s", image_abs)
        logger.info("Writing material config to: %s", output_abs)

        written = service.run(
            product_image_path=image_abs,
            image_path_for_config=image_path_for_config,
            output_path=output_abs,
            model=args.model,
            brand=args.brand,
            product_name=args.product_name,
            retry=args.retry,
        )
        print(written)
        return 0
    except (ConfigError, FileNotFoundError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"error: {exc}\n")
    except Exception as exc:  # pragma: no cover
        parser.exit(1, f"unexpected error: {exc}\n")


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

