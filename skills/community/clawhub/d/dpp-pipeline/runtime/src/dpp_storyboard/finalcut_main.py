from __future__ import annotations

import argparse
import logging
import sys

from .ark_client import configure_response_logging
from .config import ConfigError
from .finalcut_service import FinalCutService


def configure_logging() -> None:
    """配置日志输出格式和 Ark 响应日志。"""

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    log_path = configure_response_logging()
    logging.getLogger(__name__).info("Ark API logs are written to %s", log_path)


def build_parser() -> argparse.ArgumentParser:
    """构建 CLI 参数解析器。"""

    parser = argparse.ArgumentParser(
        prog="dpp-final-cut",
        description="Replace the best segment in the original video with the generated video clip.",
    )
    parser.add_argument(
        "--composition-result",
        required=True,
        help="Path to an existing composition_result.json file.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Directory where final_cut.mp4 and finalcut_result.json are written. "
        "Defaults to a 'finalCut' subdirectory next to the composition result.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI 入口函数。"""

    configure_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    logger = logging.getLogger(__name__)

    try:
        service = FinalCutService()
        logger.info("Starting final cut assembly.")
        output_path = service.run(
            composition_result_path=args.composition_result,
            output_dir=args.output,
        )
    except (ConfigError, FileNotFoundError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"error: {exc}\n")
    except Exception as exc:  # pragma: no cover
        parser.exit(1, f"unexpected error: {exc}\n")

    logger.info("Final cut assembly completed.")
    print(output_path)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
