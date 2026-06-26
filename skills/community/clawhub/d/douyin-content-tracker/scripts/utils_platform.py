import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


def platform_defaults() -> str:
    if sys.platform.startswith("win"):
        return "D:/MediaCrawler"
    # macOS / Linux 默认放到 home 下
    return str(Path.home() / "MediaCrawler")
