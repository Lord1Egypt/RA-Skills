import io
import sys

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


def test_cli_registry_validate():
    rc, out = _capture(findskills.main, ["registry", "validate"])
    assert rc == 0
    assert "合法" in out


def test_cli_registry_show():
    rc, out = _capture(findskills.main, ["registry", "show"])
    assert rc == 0
    assert "条" in out


def test_cli_search_offline_no_crash():
    # 离线搜索不应崩溃，且返回 0
    rc, out = _capture(findskills.main, ["search", "pdf", "--offline", "--limit", "5"])
    assert rc == 0
    assert "找到" in out or "Top" in out


def test_cli_search_empty_offline():
    rc, out = _capture(findskills.main, ["search", "", "--offline", "--limit", "3"])
    assert rc == 0
