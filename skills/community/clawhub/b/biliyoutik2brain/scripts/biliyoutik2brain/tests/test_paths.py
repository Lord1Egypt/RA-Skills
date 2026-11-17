"""
BiliYouTik2Brain — 存储路径管理测试
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.paths import (
    TRANSCRIPTS_DIR, NOTES_DIR, CARDS_DIR, ERRORS_DIR,
    KNOWLEDGE_DIR, COMMENTS_DIR, storage_path,
)


class TestStoragePaths:
    """存储路径管理测试"""

    def test_directories_exist(self):
        assert os.path.exists(TRANSCRIPTS_DIR)
        assert os.path.exists(NOTES_DIR)
        assert os.path.exists(CARDS_DIR)
        assert os.path.exists(ERRORS_DIR)
        assert os.path.exists(KNOWLEDGE_DIR)
        assert os.path.exists(COMMENTS_DIR)

    def test_directories_absolute(self):
        assert os.path.isabs(TRANSCRIPTS_DIR)
        assert os.path.isabs(NOTES_DIR)

    def test_storage_path_creates_subdirs(self):
        p = storage_path("transcripts", "test_UP主_VID.md")
        assert p.endswith("test_UP主_VID.md")
        parent = os.path.dirname(p)
        assert os.path.exists(parent)

    def test_env_override(self):
        """BILI_STORAGE_HOME 环境变量覆盖"""
        original = os.environ.get("BILI_STORAGE_HOME")
        try:
            os.environ["BILI_STORAGE_HOME"] = "/tmp/test_bili_storage"
            import importlib
            from core import paths
            importlib.reload(paths)
            assert paths.TRANSCRIPTS_DIR.startswith("/tmp/test_bili_storage")
        finally:
            if original:
                os.environ["BILI_STORAGE_HOME"] = original
            else:
                os.environ.pop("BILI_STORAGE_HOME", None)
            importlib.reload(paths)
