from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Modules inside business_blueprint use flat imports (e.g. ``from model import ...``)
# because cli.py adds the package directory to sys.path at runtime. To match that
# behaviour during tests, expose the inner directory too.
PACKAGE_DIR = ROOT / "business_blueprint"
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))
