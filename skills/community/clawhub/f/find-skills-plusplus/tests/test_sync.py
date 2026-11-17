"""Phase 3：在线目录同步与离线缓存（TTL）。"""
import json

import findskills


def _fake_results():
    return [{
        "name": "cached-skill", "slug": "cached-skill",
        "description": "示例技能", "source": "skillhub",
        "official_source": False, "score": 0.6, "downloads": 10,
        "reputation": 0.6,
    }]


def test_load_cache_fresh(tmp_path, monkeypatch):
    cache = tmp_path / "cache.json"
    payload = {"fetched_at": "2099-01-01T00:00:00+00:00", "count": 1, "skills": _fake_results()}
    cache.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(findskills, "SKILLHUB_CACHE", cache)
    assert len(findskills.load_cache()) == 1


def test_load_cache_expired(tmp_path, monkeypatch):
    cache = tmp_path / "cache.json"
    payload = {"fetched_at": "2000-01-01T00:00:00+00:00", "count": 1, "skills": _fake_results()}
    cache.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(findskills, "SKILLHUB_CACHE", cache)
    assert findskills.load_cache() == []


def test_sync_writes_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(findskills, "query_skillhub", lambda q, lim: _fake_results())
    cache = tmp_path / "cache.json"
    monkeypatch.setattr(findskills, "SKILLHUB_CACHE", cache)
    stats = findskills.sync_skillhub(5)
    assert stats["fetched"] == 1
    data = json.loads(cache.read_text(encoding="utf-8"))
    assert data["count"] == 1
    assert data["skills"][0]["slug"] == "cached-skill"


def test_sync_empty_returns_zero(tmp_path, monkeypatch):
    monkeypatch.setattr(findskills, "query_skillhub", lambda q, lim: [])
    cache = tmp_path / "cache.json"
    monkeypatch.setattr(findskills, "SKILLHUB_CACHE", cache)
    stats = findskills.sync_skillhub(5)
    assert stats["fetched"] == 0
