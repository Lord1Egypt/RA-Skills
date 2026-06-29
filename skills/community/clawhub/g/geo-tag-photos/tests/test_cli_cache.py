"""Tests for the `cache` subcommand."""
from __future__ import annotations

import json
from pathlib import Path

from scripts.photo_geolocator import main


def test_cache_show_prints_entries(tmp_path, capsys):
    cache = tmp_path / "cache.json"
    cache.write_text(json.dumps({"a|b|c": [1.0, 2.0]}), encoding="utf-8")
    code = main(["cache", "--show", "--cache", str(cache)])
    assert code == 0
    out = capsys.readouterr().out
    assert '"a|b|c"' in out


def test_cache_show_with_missing_file_prints_empty(tmp_path, capsys):
    code = main(["cache", "--show", "--cache", str(tmp_path / "nope.json")])
    assert code == 0
    out = capsys.readouterr().out
    assert "{}" in out


def test_cache_clear_removes_file(tmp_path):
    cache = tmp_path / "cache.json"
    cache.write_text("{}", encoding="utf-8")
    code = main(["cache", "--clear", "--cache", str(cache)])
    assert code == 0
    assert not cache.exists()


def test_cache_clear_missing_file_is_ok(tmp_path):
    code = main(["cache", "--clear", "--cache", str(tmp_path / "nope.json")])
    assert code == 0
