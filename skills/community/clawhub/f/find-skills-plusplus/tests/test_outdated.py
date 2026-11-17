"""测试过期巡检 `outdated`：复用注册表/缓存版本，比对已装技能是否落后。"""

from __future__ import annotations

import pytest

import findskills as fk


def test_outdated_flags_newer_available(monkeypatch, capsys):
    monkeypatch.setattr(fk, "discover_local", lambda include_self=False: [
        {"name": "Demo Skill", "slug": "demo-skill", "version": "1.0.0", "path": "/x"},
    ])
    monkeypatch.setattr(fk, "load_registry", lambda: [
        {"name": "Demo Skill", "slug": "demo-skill", "version": "2.0.0"},
    ])
    monkeypatch.setattr(fk, "load_cache", lambda: [])
    rc = fk.main(["outdated"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Demo Skill" in out
    assert "1.0.0" in out and "2.0.0" in out


def test_outdated_up_to_date(monkeypatch, capsys):
    monkeypatch.setattr(fk, "discover_local", lambda include_self=False: [
        {"name": "Demo Skill", "slug": "demo-skill", "version": "2.0.0", "path": "/x"},
    ])
    monkeypatch.setattr(fk, "load_registry", lambda: [
        {"name": "Demo Skill", "slug": "demo-skill", "version": "1.0.0"},
    ])
    monkeypatch.setattr(fk, "load_cache", lambda: [])
    rc = fk.main(["outdated"])
    assert rc == 0
    assert "全部已装技能均为最新" in capsys.readouterr().out


def test_outdated_no_local(monkeypatch, capsys):
    monkeypatch.setattr(fk, "discover_local", lambda include_self=False: [])
    rc = fk.main(["outdated"])
    assert rc == 0
    assert "未发现本地已装技能" in capsys.readouterr().out


def test_outdated_uses_cache_when_registry_empty(monkeypatch, capsys):
    monkeypatch.setattr(fk, "discover_local", lambda include_self=False: [
        {"name": "Cache Only", "slug": "cache-only", "version": "0.9.0", "path": "/y"},
    ])
    monkeypatch.setattr(fk, "load_registry", lambda: [])
    monkeypatch.setattr(fk, "load_cache", lambda: [
        {"name": "Cache Only", "slug": "cache-only", "version": "1.1.0"},
    ])
    rc = fk.main(["outdated"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Cache Only" in out and "1.1.0" in out



def test_outdated_reports_no_data_honestly(monkeypatch, capsys):
    """注册表/缓存无 version 字段时，应如实提示「无版本数据」，而非谎报「全部最新」。"""
    monkeypatch.setattr(fk, "discover_local", lambda include_self=False: [
        {"name": "Demo Skill", "slug": "demo-skill", "version": "1.0.0", "path": "/x"},
    ])
    monkeypatch.setattr(fk, "load_registry", lambda: [
        {"name": "Demo Skill", "slug": "demo-skill"},  # 无 version 字段
    ])
    monkeypatch.setattr(fk, "load_cache", lambda: [])
    rc = fk.main(["outdated"])
    assert rc == 0
    out = capsys.readouterr().out
    assert ("无版本数据" in out) or ("version 字段" in out)
    assert "全部已装技能均为最新" not in out
