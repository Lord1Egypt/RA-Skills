from __future__ import annotations

import argparse
import logging
import sys

from .ark_client import configure_response_logging
from .composition_service import BestSegmentCompositionService
from .config import ConfigError, Settings


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    log_path = configure_response_logging()
    logging.getLogger(__name__).info("Ark API logs are written to %s", log_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dpp-compose-best",
        description="Generate one best-segment product composition task from storyboard and placement analysis.",
    )
    parser.add_argument("--storyboard", required=True, help="Path to an existing storyboard.json file.")
    parser.add_argument(
        "--placement-analysis",
        required=True,
        help="Path to an existing placement_analysis.json file.",
    )
    parser.add_argument(
        "--material-config",
        default="configs/placement_material.json",
        help="Path to a single-material JSON config file. Default: configs/placement_material.json.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Directory where composition_result.json is written. Defaults to the placement-analysis directory.",
    )
    parser.add_argument(
        "--prompt-model",
        default=None,
        help="Optional Doubao-Seed prompt-planning model override. Defaults to DOUBAO_SEED_ENDPOINT_ID.",
    )
    parser.add_argument(
        "--generation-model",
        default=None,
        help="Optional video-generation model override. Defaults to DPP_VIDEO_GENERATION_MODEL.",
    )
    parser.add_argument(
        "--reference-video-url",
        default=None,
        help="Optional public or asset:// URL for the extracted reference clip. Defaults to DPP_REFERENCE_VIDEO_URL.",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=None,
        help=(
            "Optional generated clip duration override in seconds. Use -1 to let the model decide. "
            "Otherwise the value must be between 2 and 12. "
            "If omitted, compose-best uses the extracted reference clip duration (must be within 2-12s)."
        ),
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=1,
        help="Format-repair retries after validation failure. Default: 1.",
    )
    parser.add_argument(
        "--generate-audio",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Request generated audio for the edited clip (default: enabled, use --no-generate-audio to disable).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    logger = logging.getLogger(__name__)

    try:
        settings = Settings.from_env()
        service = BestSegmentCompositionService(settings)
        logger.info("Starting best-segment composition.")
        output_path = service.run(
            storyboard_path=args.storyboard,
            placement_analysis_path=args.placement_analysis,
            material_config_path=args.material_config,
            output_dir=args.output,
            prompt_model=args.prompt_model,
            generation_model=args.generation_model,
            reference_video_url=args.reference_video_url,
            duration=args.duration,
            retry=args.retry,
            generate_audio=args.generate_audio,
        )
    except (ConfigError, FileNotFoundError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"error: {exc}\n")
    except Exception as exc:  # pragma: no cover
        parser.exit(1, f"unexpected error: {exc}\n")

    logger.info("Best-segment composition completed.")
    print(output_path)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
