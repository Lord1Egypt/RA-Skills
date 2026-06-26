"""Entry point for the `dazzle` console script. Defers to proxy.main()."""

from __future__ import annotations

import argparse
import sys

from dazzle_photo_intelligence import __version__, proxy


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="dazzle",
        description=(
            "Stdio MCP server that bridges an MCP-capable agent to Dazzle. "
            "Auto-runs the OAuth2 device flow on first use; subsequent invocations are silent."
        ),
    )
    parser.add_argument("--version", action="version", version=f"dazzle {__version__}")
    parser.parse_args(argv)
    proxy.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
