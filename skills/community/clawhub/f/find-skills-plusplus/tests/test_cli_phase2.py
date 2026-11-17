import io
import sys
from pathlib import Path

import findskills


def _capture(func, argv):
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        rc = func(argv)
    finally:
        sys.stdout = old
    return rc, buf.getvalue()


ROOT = Path(__file__).resolve().parent.parent


def test_cli_quality_self():
    rc, out = _capture(findskills.main, ["quality", "--path", str(ROOT)])
    assert rc == 0
    assert "质量评级" in out


def test_cli_redundancy_no_crash():
    rc, _ = _capture(findskills.main, ["redundancy"])
    assert rc == 0


def test_cli_prune_no_crash():
    rc, _ = _capture(findskills.main, ["prune"])
    assert rc == 0


def test_cli_search_semantic_no_crash():
    rc, out = _capture(findskills.main, ["search", "股票", "--offline", "--limit", "5"])
    assert rc == 0
    assert "找到" in out or "Top" in out
