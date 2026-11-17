"""Tests for cite-check. The extraction tests are offline and deterministic;
the network tests are marked and skipped unless CITE_CHECK_NET=1 is set.
"""
import os
import subprocess
import sys
from pathlib import Path

import cite_check as cc

HERE = Path(__file__).parent
NET = os.environ.get("CITE_CHECK_NET") == "1"


# --- extraction (offline) ------------------------------------------------

def test_finds_plain_urls():
    urls, ids = cc.find_citations("see https://a.com/x and http://b.org.")
    assert "https://a.com/x" in urls
    assert "http://b.org" in urls  # trailing full stop trimmed


def test_trailing_punctuation_trimmed():
    urls, _ = cc.find_citations("(link: https://x.com/page).")
    assert urls == ["https://x.com/page"]


def test_arxiv_shapes_all_normalise_to_id():
    text = ("arXiv:2404.10774, https://arxiv.org/abs/2404.10774v2, "
            "and bare 2404.10774 again")
    _, ids = cc.find_citations(text)
    assert ids == ["2404.10774"]  # de-duped to one canonical id


def test_arxiv_url_not_double_counted_as_url():
    urls, ids = cc.find_citations("https://arxiv.org/abs/2404.10774")
    assert urls == []          # handled as an arXiv id, not a plain URL
    assert ids == ["2404.10774"]


def test_dedup_preserves_order():
    urls, _ = cc.find_citations("https://b.com then https://a.com then https://b.com")
    assert urls == ["https://b.com", "https://a.com"]


def test_no_citations_is_empty():
    urls, ids = cc.find_citations("no links here, just prose.")
    assert urls == [] and ids == []


# --- CLI behaviour (offline) ---------------------------------------------

def test_cli_no_citations_exit_zero():
    r = subprocess.run([sys.executable, str(HERE / "cite_check.py")],
                       input="plain prose, nothing to check",
                       capture_output=True, text=True)
    assert r.returncode == 0


def test_cli_strict_no_citations_exit_one():
    r = subprocess.run([sys.executable, str(HERE / "cite_check.py"), "--strict"],
                       input="plain prose", capture_output=True, text=True)
    assert r.returncode == 1


# --- network (opt-in) ----------------------------------------------------

def test_real_vs_fake_arxiv():
    if not NET:
        return  # skipped without CITE_CHECK_NET=1
    with cc.httpx.Client(headers={"User-Agent": cc.UA}) as c:
        assert cc.check_arxiv(c, "2404.10774").ok is True    # MiniCheck, real
        assert cc.check_arxiv(c, "2606.99999").ok is False   # fabricated


def test_dead_url_fails():
    if not NET:
        return
    with cc.httpx.Client(headers={"User-Agent": cc.UA}) as c:
        assert cc.check_url(c, "https://workloft.ai").ok is True
        assert cc.check_url(
            c, "https://workloft.ai/nope-xyz-404").ok is False


if __name__ == "__main__":
    # tiny runner so it works without pytest installed
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            fn()
            passed += 1
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            print(f"FAIL {fn.__name__}: {e}")
    print(f"\n{passed}/{len(fns)} passed"
          + ("" if NET else "  (network tests skipped; set CITE_CHECK_NET=1)"))
    raise SystemExit(0 if passed == len(fns) else 1)
