"""
tests/conftest.py — pytest fixtures
"""
import sys, os, tempfile
from pathlib import Path

# 确保 amber_hunter 模块可导入
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


@pytest.fixture
def temp_home(monkeypatch, tmp_path):
    """将 HOME 指向临时目录，隔离测试数据"""
    test_home = tmp_path / ".amber-hunter"
    test_home.mkdir()
    monkeypatch.setenv("HOME", str(tmp_path))
    yield test_home


@pytest.fixture
def test_db(temp_home):
    """初始化测试数据库，返回 DB_PATH"""
    import core.db as db_module
    old_path = db_module.DB_PATH
    db_module.DB_PATH = temp_home / "test_hunter.db"
    db_module.init_db()
    yield db_module.DB_PATH
    db_module.DB_PATH = old_path


@pytest.fixture
def test_client(test_db, monkeypatch):
    """FastAPI TestClient with隔离的数据库"""
    import core.db as db_module

    # 让 core.db 使用测试数据库
    monkeypatch.setattr(db_module, "DB_PATH", test_db)

    # 重新初始化（确保表结构就绪）
    db_module.init_db()

    from amber_hunter import app
    from fastapi.testclient import TestClient
    return TestClient(app)
