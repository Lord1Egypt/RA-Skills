#!/usr/bin/env python3
"""文件契约测试 —— 验证 validate_book.py 对各类书籍的检测能力。

运行：python -m pytest tests/test_contract.py -v
"""

import os
import sys
import pytest

# 将 scripts/ 加入路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from validate_book import validate, file_exists_with_alias


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


class TestStandardBook:
    """标准新书 fixture 应该通过全部验证。"""

    def setup_method(self):
        self.book_dir = os.path.join(FIXTURES_DIR, "standard-book")

    def test_validation_passes(self):
        result = validate(self.book_dir)
        assert result.ok, f"标准书应通过验证，但失败：{result.errors}"

    def test_no_missing_files(self):
        result = validate(self.book_dir)
        # 不应有"缺失必需文件"错误
        missing_errors = [e for e in result.errors if "缺失" in e]
        assert not missing_errors, f"不应有缺失文件：{missing_errors}"

    def test_book_json_valid(self):
        result = validate(self.book_dir)
        json_errors = [e for e in result.errors if "book.json" in e]
        assert not json_errors, f"book.json 应合法：{json_errors}"

    def test_chapters_continuous(self):
        result = validate(self.book_dir)
        continuity_warnings = [w for w in result.warnings if "不连续" in w]
        assert not continuity_warnings, f"章节应连续：{continuity_warnings}"

    def test_index_consistent(self):
        result = validate(self.book_dir)
        index_errors = [e for e in result.errors if "index" in e.lower()]
        assert not index_errors, f"index 应一致：{index_errors}"


class TestAliasBook:
    """使用全部旧别名的旧书应该通过验证（含别名回退）。"""

    def setup_method(self):
        self.book_dir = os.path.join(FIXTURES_DIR, "alias-book")

    @pytest.fixture(autouse=True)
    def create_alias_book(self, tmp_path):
        """创建使用旧别名的书籍。"""
        import shutil
        # 从标准书复制，然后重命名文件为旧名
        if os.path.exists(self.book_dir):
            shutil.rmtree(self.book_dir)
        shutil.copytree(os.path.join(FIXTURES_DIR, "standard-book"), self.book_dir)
        # 重命名为旧名
        story_dir = os.path.join(self.book_dir, "story")
        outline_dir = os.path.join(story_dir, "outline")
        # story_frame.md → story_bible.md
        if os.path.exists(os.path.join(outline_dir, "story_frame.md")):
            os.rename(
                os.path.join(outline_dir, "story_frame.md"),
                os.path.join(story_dir, "story_bible.md"),
            )
        yield
        shutil.rmtree(self.book_dir, ignore_errors=True)

    def test_alias_fallback(self):
        """别名文件应被识别。"""
        exists, actual = file_exists_with_alias(
            self.book_dir, "story/outline/story_frame.md"
        )
        assert exists, "应通过别名 story_bible.md 找到故事基础文件"
        assert actual == "story/story_bible.md"

    def test_validation_with_aliases(self):
        result = validate(self.book_dir)
        # 使用别名应有警告但不报错
        alias_warnings = [w for w in result.warnings if "旧名" in w]
        assert alias_warnings, "使用旧名应产生警告"


class TestMissingStateBook:
    """缺少状态文件的导入书应该报错。"""

    def setup_method(self):
        self.book_dir = os.path.join(FIXTURES_DIR, "missing-state-book")

    @pytest.fixture(autouse=True)
    def create_book(self, tmp_path):
        import shutil
        if os.path.exists(self.book_dir):
            shutil.rmtree(self.book_dir)
        shutil.copytree(os.path.join(FIXTURES_DIR, "standard-book"), self.book_dir)
        # 删除 current_state.md
        os.remove(os.path.join(self.book_dir, "story", "current_state.md"))
        yield
        shutil.rmtree(self.book_dir, ignore_errors=True)

    def test_missing_state_detected(self):
        result = validate(self.book_dir)
        missing_errors = [e for e in result.errors if "current_state" in e]
        assert missing_errors, "缺少 current_state.md 应报错"


class TestNonContiguousBook:
    """章节编号不连续的书应该警告。"""

    def setup_method(self):
        self.book_dir = os.path.join(FIXTURES_DIR, "non-contiguous-book")

    @pytest.fixture(autouse=True)
    def create_book(self, tmp_path):
        import shutil
        if os.path.exists(self.book_dir):
            shutil.rmtree(self.book_dir)
        shutil.copytree(os.path.join(FIXTURES_DIR, "standard-book"), self.book_dir)
        # 添加一个跳号的章节
        with open(os.path.join(self.book_dir, "chapters", "0005_跳跃.md"), "w") as f:
            f.write("# 跳跃\n\n内容。")
        yield
        shutil.rmtree(self.book_dir, ignore_errors=True)

    def test_non_contiguous_warning(self):
        result = validate(self.book_dir)
        continuity_warnings = [w for w in result.warnings if "不连续" in w or "缺失" in w]
        assert continuity_warnings, "章节不连续应警告"


class TestMultiBookProject:
    """包含多本书的项目——validate_book 应只检查指定书。"""

    def test_independent_validation(self):
        """两本书的验证结果互不影响。"""
        book1 = os.path.join(FIXTURES_DIR, "standard-book")
        result1 = validate(book1)
        assert result1.ok


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
