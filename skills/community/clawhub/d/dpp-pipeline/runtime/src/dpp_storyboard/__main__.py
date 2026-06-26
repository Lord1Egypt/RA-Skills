from __future__ import annotations

import argparse
import logging
import sys

from .ark_client import configure_response_logging
from .config import ConfigError, Settings
from .service import StoryboardService


def configure_logging() -> None:
    """Configure CLI logging for visible progress output."""
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    log_path = configure_response_logging()
    logging.getLogger(__name__).info("Responses API logs are written to %s", log_path)


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        prog="dpp-storyboard",
        description="Generate storyboard.json from a local video with Doubao-Seed.",
    )
    parser.add_argument(
        "--video",
        default=None,
        help="Optional path to a local .mp4 or .mov file. Defaults to DPP_DEFAULT_VIDEO_PATH.",
    )
    parser.add_argument("--output", required=True, help="Directory where storyboard output is written.")
    parser.add_argument(
        "--model",
        default=None,
        help="Optional model or endpoint override. Defaults to DOUBAO_SEED_ENDPOINT_ID.",
    )
    parser.add_argument(
        "--file-id",
        default=None,
        help="Optional Ark file id. Defaults to ARK_FILE_ID. When provided, skips file upload.",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=1,
        help="Format-repair retries after validation failure. Default: 1.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """解析命令行参数并执行分镜生成流程。"""
    configure_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    logger = logging.getLogger(__name__)

    try:
        settings = Settings.from_env()
        logger.info("Loaded runtime settings.")
        service = StoryboardService(settings)
        logger.info("Starting storyboard generation.")
        output_path = service.run(
            video_path=args.video or settings.default_video_path,
            output_dir=args.output,
            model=args.model,
            file_id=args.file_id or settings.default_file_id,
            retry=args.retry,
        )
    except (ConfigError, FileNotFoundError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"error: {exc}\n")
    except Exception as exc:  # pragma: no cover - CLI catch-all
        parser.exit(1, f"unexpected error: {exc}\n")

    logger.info("Storyboard generation completed.")
    print(output_path)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
