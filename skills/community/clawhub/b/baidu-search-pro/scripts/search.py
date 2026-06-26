import runpy
from pathlib import Path


CANONICAL_SCRIPT = (
    Path(__file__).resolve().parents[3]
    / "custom-skills"
    / "realtime-web-search"
    / "scripts"
    / "search.py"
)


if __name__ == "__main__":
    runpy.run_path(str(CANONICAL_SCRIPT), run_name="__main__")
