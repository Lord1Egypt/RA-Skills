"""Allow running geminipdfocr as a module: python -m geminipdfocr."""

import sys
from pathlib import Path

# Ensure geminipdfocr directory is on path so flat imports (gemini_client, service, etc.) resolve
_skill_dir = Path(__file__).resolve().parent
if str(_skill_dir) not in sys.path:
    sys.path.insert(0, str(_skill_dir))

from main import main

if __name__ == "__main__":
    sys.exit(main())
