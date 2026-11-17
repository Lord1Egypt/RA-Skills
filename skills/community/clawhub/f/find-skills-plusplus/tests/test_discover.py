"""Phase 3：discover 榜单与跨源版本仲裁。"""
import io
import contextlib
import json
import datetime
import tempfile
from pathlib import Path

import findskills


def test_parse_version():
    assert findskills.parse_version("v1.2.3") == (1, 2, 3)
    assert findskills.parse_version("1.10") > findskills.parse_version("1.9")
    assert findskills.parse_version("") == (0,)
    assert findskills.parse_version("2.0-beta") == (2, 0, 0)


def test_merge_records_source_versions():
    lists = [
        ("registry", [{"name": "demo", "slug": "demo", "version": "1.0"}]),
        ("cache", [{"name": "demo", "slug": "demo", "version": "2.0"}]),
    ]
    merged = findskills.merge_candidates(lists)
    key = findskills.normalize_key("demo")
    assert key in merged
    assert merged[key]["_source_versions"] == {"registry": "1.0", "cache": "2.0"}


def test_discover_version_arbitration(tmp_path, monkeypatch):
    reg = {"skills": [{
        "slug": "demo", "name": "demo", "description": "d",
        "category": "t", "source": "workbuddy-builtin",
        "official_source": False, "reputation": 0.9,
        "version": "1.0", "updated": 1700000000000,
    }]}
    reg_path = tmp_path / "registry.json"
    reg_path.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(findskills, "REGISTRY_PATH", reg_path)

    cache = {
        "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "count": 1,
        "skills": [{
            "slug": "demo", "name": "demo", "description": "d",
            "source": "skillhub", "official_source": False,
            "score": 0.7, "downloads": 9000, "reputation": 0.6,
            "version": "2.0", "updatedAt": 1780000000000,
        }],
    }
    cache_path = tmp_path / "cache.json"
    cache_path.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(findskills, "SKILLHUB_CACHE", cache_path)
    # 避免 discover 混入真实本地技能造成干扰
    monkeypatch.setattr(findskills, "discover_local", lambda: [])

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = findskills.main(["discover"])
    out = buf.getvalue()
    assert rc == 0
    assert "跨源版本仲裁" in out
    assert "落后源: registry" in out


def test_ts_normalizes_mixed_date_formats():
    """回归：registry 用 '2026-03-05' 字符串、缓存用毫秒整数，都要能比较。"""
    assert findskills._ts(None) == 0.0
    assert findskills._ts("2026-03-05") > findskills._ts("2025-01-01")
    assert findskills._ts(1780000000000) > findskills._ts(1700000000000)
    assert findskills._ts("not-a-date") == 0.0
    # 毫秒整数与日期字符串可混合比较（同一量级：秒）
    assert findskills._ts(1780000000000) > findskills._ts("2026-03-05")


def test_discover_new_with_string_dates_does_not_crash(tmp_path, monkeypatch):
    """回归：discover --new 曾因对日期字符串取负而 TypeError 崩溃。"""
    reg = {"skills": [
        {"slug": "a", "name": "a", "description": "d", "category": "t",
         "source": "workbuddy-builtin", "official_source": False,
         "reputation": 0.9, "version": "1.0", "updated": "2026-03-05"},
        {"slug": "b", "name": "b", "description": "d", "category": "t",
         "source": "workbuddy-builtin", "official_source": False,
         "reputation": 0.9, "version": "1.0", "updated": "2025-01-01"},
    ]}
    reg_path = tmp_path / "registry.json"
    reg_path.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(findskills, "REGISTRY_PATH", reg_path)
    monkeypatch.setattr(findskills, "SKILLHUB_CACHE", tmp_path / "nope.json")
    monkeypatch.setattr(findskills, "discover_local", lambda: [])

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = findskills.main(["discover", "--new"])
    out = buf.getvalue()
    assert rc == 0, f"discover --new 崩溃，输出：{out}"
    assert "新上架" in out
    # 日期新的应排在前面
    assert out.index("a") < out.index("b")
