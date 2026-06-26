from __future__ import annotations

import argparse
import logging
import sys

from .ark_client import configure_response_logging
from .config import ConfigError, Settings
from .placement_service import PlacementAnalysisService


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    log_path = configure_response_logging()
    logging.getLogger(__name__).info("Responses API logs are written to %s", log_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dpp-placement",
        description="Analyze which storyboard segments are suitable for compositing a product material.",
    )
    parser.add_argument("--storyboard", required=True, help="Path to an existing storyboard.json file.")
    parser.add_argument(
        "--material-config",
        default="configs/placement_material.json",
        help="Path to a single-material JSON config file. Default: configs/placement_material.json.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Directory where placement_analysis.json is written. Defaults to the storyboard directory.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Optional model or endpoint override. Defaults to DOUBAO_SEED_ENDPOINT_ID.",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=1,
        help="Format-repair retries after validation failure. Default: 1.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    logger = logging.getLogger(__name__)

    try:
        settings = Settings.from_env()
        service = PlacementAnalysisService(settings)
        logger.info("Starting placement analysis.")
        output_path = service.run(
            storyboard_path=args.storyboard,
            material_config_path=args.material_config,
            output_dir=args.output,
            model=args.model,
            retry=args.retry,
        )
    except (ConfigError, FileNotFoundError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"error: {exc}\n")
    except Exception as exc:  # pragma: no cover
        parser.exit(1, f"unexpected error: {exc}\n")

    logger.info("Placement analysis completed.")
    print(output_path)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
