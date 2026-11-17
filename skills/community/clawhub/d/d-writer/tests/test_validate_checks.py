#!/usr/bin/env python3
"""账本一致性新检查测试 —— validate_book.py 的 T1.2 / T2.2 / T3.2 / T4.2 / T5.2 / T7 / T14.3。

运行：python -m pytest tests/test_validate_checks.py -v
"""

import json
import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from validate_book import validate  # noqa: E402


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
STD_BOOK = os.path.join(FIXTURES_DIR, "standard-book")


def copy_std(tmp_path, name="book"):
    """从 standard-book 复制一份可变书籍。"""
    target = os.path.join(tmp_path, name)
    shutil.copytree(STD_BOOK, target)
    return target


def messages(result, level, keyword):
    return [m for m in getattr(result, level) if keyword in m]


class TestAliasConflict:
    """T1.2：规范名与别名并存 → error。"""

    def test_both_exist_is_error(self, tmp_path):
        book = copy_std(tmp_path)
        # 制造规范名与别名并存（audit-drift.md 已存在，再加别名 audit_drift.md）
        with open(os.path.join(book, "story", "audit_drift.md"), "w", encoding="utf-8") as f:
            f.write("# Audit Drift\n")
        result = validate(book)
        errs = messages(result, "errors", "别名并存")
        assert errs, f"应报'规范名与别名并存'错误，但无：{result.errors}"

    def test_canonical_only_is_fine(self, tmp_path):
        book = copy_std(tmp_path)
        result = validate(book)
        assert not messages(result, "errors", "别名并存")


class TestRoleNameConflict:
    """T2.2：major/minor 同名双卡 → error。"""

    def test_duplicate_role_is_error(self, tmp_path):
        book = copy_std(tmp_path)
        # 把 minor 卡复制进 major，制造同名双卡
        shutil.copyfile(
            os.path.join(book, "story", "roles", "minor", "林逸.md"),
            os.path.join(book, "story", "roles", "major", "林逸.md"),
        )
        result = validate(book)
        errs = messages(result, "errors", "同名双卡")
        assert errs, f"应报'角色同名双卡'错误，但无：{result.errors}"

    def test_no_duplicate_is_fine(self, tmp_path):
        book = copy_std(tmp_path)
        result = validate(book)
        assert not messages(result, "errors", "同名双卡")


class TestWordCountConsistency:
    """T3.2：index wordCount 与正文重算值核对。"""

    def test_mismatch_is_error(self, tmp_path):
        book = copy_std(tmp_path)
        index_path = os.path.join(book, "chapters", "index.json")
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)
        index["chapters"][0]["wordCount"] = 99999  # 明显错误
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        result = validate(book)
        errs = messages(result, "errors", "wordCount 与正文不符")
        assert errs, f"应报 wordCount 不符错误，但无：{result.errors}"

    def test_matching_is_fine(self, tmp_path):
        book = copy_std(tmp_path)
        result = validate(book)
        assert not messages(result, "errors", "wordCount 与正文不符")


class TestFactEvidence:
    """T4.2：事实表 evidence 引文必须在来源章命中。"""

    def _add_evidence(self, book, rows):
        """把 facts 表替换为含 evidence 列的版本。rows = [(fact_id, evidence), ...]

        按行定位修改（header / fact- 行），不依赖分隔行内容，兼容不同对齐。
        """
        state_path = os.path.join(book, "story", "current_state.md")
        with open(state_path, "r", encoding="utf-8") as f:
            lines = f.read().split("\n")
        hdr_idx = next(i for i, l in enumerate(lines) if l.startswith("| fact_id"))
        # 表头在 confidence 与 notes 之间插入 evidence
        cells = lines[hdr_idx].split("|")
        cells.insert(len(cells) - 2, " evidence ")
        lines[hdr_idx] = "|".join(cells)
        ev_map = dict(rows)
        for i in range(hdr_idx + 2, len(lines)):
            if not lines[i].startswith("| fact-"):
                continue
            fid = lines[i].split("|")[1].strip()
            if fid not in ev_map:
                continue
            cells = lines[i].split("|")
            cells.insert(len(cells) - 2, f" {ev_map[fid]} ")
            lines[i] = "|".join(cells)
        with open(state_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def test_fabricated_evidence_is_error(self, tmp_path):
        book = copy_std(tmp_path)
        self._add_evidence(book, [("fact-001", "陆恒一夜之间想通了全部"), ("fact-002", "林逸")])
        result = validate(book)
        errs = messages(result, "errors", "证据引文在章节 1 正文未命中")
        assert errs, f"应报引文未命中错误，但无：{result.errors}"

    def test_real_evidence_is_fine(self, tmp_path):
        book = copy_std(tmp_path)
        # 0001_入门.md 正文实际包含的片段
        self._add_evidence(book, [("fact-001", "陆恒站在甲字七号舍前"), ("fact-002", "林逸住甲字八号")])
        result = validate(book)
        assert not messages(result, "errors", "证据引文在章节 1 正文未命中")

    def test_missing_column_is_warning(self, tmp_path):
        book = copy_std(tmp_path)  # 原 fixture 无 evidence 列
        result = validate(book)
        warns = messages(result, "warnings", "缺少 evidence 列")
        assert warns, "旧表缺少 evidence 列应提示升级"


class TestPropOriginDrift:
    """T5.2：道具 origin 在快照间变化 → warning。"""

    def _set_prop_origin(self, book, origin):
        """给道具账本设置 prop-001 的 origin 值（幂等：已存在 origin 列则更新值）。"""
        state_path = os.path.join(book, "story", "current_state.md")
        with open(state_path, "r", encoding="utf-8") as f:
            lines = f.read().split("\n")
        hdr_idx = next(i for i, l in enumerate(lines) if l.startswith("| prop_id"))
        cells = lines[hdr_idx].split("|")
        if not any("origin" in c for c in cells):
            evt_idx = next(i for i, c in enumerate(cells) if "event_id" in c)
            cells.insert(evt_idx, " origin ")
            lines[hdr_idx] = "|".join(cells)
        for i in range(hdr_idx + 2, len(lines)):
            if not lines[i].startswith("| prop-"):
                continue
            row = lines[i].split("|")
            # origin 列 = header 中 origin 所在位置
            hdr = lines[hdr_idx].split("|")
            origin_idx = next(j for j, c in enumerate(hdr) if "origin" in c)
            if len(row) <= origin_idx:
                continue
            row[origin_idx] = f" {origin} " if row[1].strip() == "prop-001" else " — "
            lines[i] = "|".join(row)
        with open(state_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def test_origin_changed_between_snapshots_warns(self, tmp_path):
        book = copy_std(tmp_path)
        self._set_prop_origin(book, "旧来历")
        # 建最新快照，其中 origin 为"旧来历"
        snap = os.path.join(book, "story", "snapshots", "0001", "story")
        os.makedirs(snap, exist_ok=True)
        with open(os.path.join(book, "story", "current_state.md"), "r", encoding="utf-8") as f:
            shutil.copyfile(
                os.path.join(book, "story", "current_state.md"),
                os.path.join(snap, "current_state.md"),
            )
        # 当前 state 的 origin 改为"新来历"
        self._set_prop_origin(book, "新来历")
        result = validate(book)
        warns = messages(result, "warnings", "origin 在快照间变化")
        assert warns, f"应报 origin 漂移警告，但无：{result.warnings}"


class TestGenderAddress:
    """T7：性别称谓 lint（仅 warning）。"""

    def test_female_named_as_male_warns(self, tmp_path):
        book = copy_std(tmp_path)
        # 加一个女性角色卡（含性别字段）
        role_dir = os.path.join(book, "story", "roles", "major")
        with open(os.path.join(role_dir, "苏小小.md"), "w", encoding="utf-8") as f:
            f.write("# 苏小小\n\n## 基本信息\n- 性别：女\n")
        # 覆盖第一章正文：苏小小被称"一个男的"
        with open(os.path.join(book, "chapters", "0001_入门.md"), "w", encoding="utf-8") as f:
            f.write("# 入门\n\n苏小小你一个男的，这怎么行。\n")
        result = validate(book)
        warns = messages(result, "warnings", "被男性称谓")
        assert warns, f"应报性别称谓警告，但无：{result.warnings}"

    def test_no_gender_field_is_silent(self, tmp_path):
        book = copy_std(tmp_path)
        result = validate(book)
        assert not messages(result, "warnings", "被男性称谓")

    def test_template_file_is_skipped(self, tmp_path):
        """骨架角色卡模板（_前缀/含'模板'）不参与性别称谓 lint。"""
        book = copy_std(tmp_path)
        role_dir = os.path.join(book, "story", "roles", "major")
        with open(os.path.join(role_dir, "_角色卡模板.md"), "w", encoding="utf-8") as f:
            f.write("# <角色名>\n\n## 基本信息\n- 性别：女\n")
        with open(os.path.join(book, "chapters", "0001_入门.md"), "w", encoding="utf-8") as f:
            f.write("# 入门\n\n角色卡模板你一个男的。\n")
        result = validate(book)
        assert not messages(result, "warnings", "被男性称谓")


class TestNumberAnchorSelfConflict:
    """T6.4：角色卡 canon 数字锚点表内自相矛盾 → warning。"""

    def _write_role_card(self, book, content):
        role_dir = os.path.join(book, "story", "roles", "major")
        with open(os.path.join(role_dir, "测试.md"), "w", encoding="utf-8") as f:
            f.write(content)

    def test_conflicting_anchors_warn(self, tmp_path):
        book = copy_std(tmp_path)
        self._write_role_card(book, (
            "# 测试\n\n"
            "## canon 数字锚点 Number Anchors\n\n"
            "| anchor_id | 事项 | 值 | 生效章 | 依据 |\n"
            "| --- | --- | --- | ---: | --- |\n"
            "| anchor-001 | 当前年龄 | 20 | 1 | 正文 |\n"
            "| anchor-002 | 当前年龄 | 19 | 1 | 正文 |\n"
        ))
        result = validate(book)
        warns = messages(result, "warnings", "canon 数字锚点")
        assert warns, f"应报锚点自冲突警告，但无：{result.warnings}"

    def test_monotonic_change_chain_is_fine(self, tmp_path):
        book = copy_std(tmp_path)
        self._write_role_card(book, (
            "# 测试\n\n"
            "## canon 数字锚点 Number Anchors\n\n"
            "| anchor_id | 事项 | 值 | 生效章 | 依据 |\n"
            "| --- | --- | --- | ---: | --- |\n"
            "| anchor-001 | 身高 | 5尺2寸 | 1 | 基线 |\n"
            "| anchor-002 | 身高 | 5尺4寸 | 24 | 突破 |\n"
        ))
        result = validate(book)
        assert not messages(result, "warnings", "canon 数字锚点")


class TestBookJsonStale:
    """T14.3：book.json 生命周期字段陈旧提示。"""

    def test_status_outlining_with_completed_chapters_warns(self, tmp_path):
        book = copy_std(tmp_path)
        book_path = os.path.join(book, "book.json")
        with open(book_path, "r", encoding="utf-8") as f:
            bj = json.load(f)
        bj["status"] = "outlining"
        with open(book_path, "w", encoding="utf-8") as f:
            json.dump(bj, f, ensure_ascii=False, indent=2)
        # 标记一章 completed
        index_path = os.path.join(book, "chapters", "index.json")
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)
        index["chapters"][0]["status"] = "completed"
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        result = validate(book)
        warns = messages(result, "warnings", "book.json.status 仍为 outlining")
        assert warns, f"应报 status 陈旧警告，但无：{result.warnings}"


class TestSkeletonClean:
    """书骨架（assets/book-skeleton）本身必须 validate 全绿（0 error + 0 warning）。"""

    def test_skeleton_validation_clean(self):
        skeleton = os.path.join(
            os.path.dirname(__file__), "..", "assets", "book-skeleton"
        )
        if not os.path.isdir(skeleton):
            pytest.skip("骨架目录不存在")
        result = validate(skeleton)
        assert result.ok, f"骨架不应有 error：{result.errors}"
        assert not result.warnings, f"骨架不应有 warning：{result.warnings}"


class TestDimensionColumns:
    """角色卡时间线列必须与 book_rules 维度声明一致（未声明列 -> warning）。"""

    def _write_rules(self, book, content):
        with open(os.path.join(book, "story", "book_rules.md"), "w", encoding="utf-8") as f:
            f.write(content)

    def _write_card(self, book, name, content):
        # 清掉 fixture 的角色卡，避免其未声明列干扰本用例
        for root, _, files in os.walk(os.path.join(book, "story", "roles")):
            for f in files:
                if f.endswith(".md"):
                    os.remove(os.path.join(root, f))
        role_dir = os.path.join(book, "story", "roles", "major")
        with open(os.path.join(role_dir, name), "w", encoding="utf-8") as f:
            f.write(content)

    def test_undeclared_physical_column_warns(self, tmp_path):
        book = copy_std(tmp_path)
        self._write_rules(book, (
            "# Book Rules\n\n"
            "## 物理数据维度 Physical Data Dimensions\n\n"
            "| dim_id | 维度名 | 单位/取值口径 | 说明 |\n"
            "| --- | --- | --- | --- |\n"
            "| phy-001 | 身高 | 尺/寸 | 身高 |\n"
            "| phy-002 | 体重 | 斤 | 体重 |\n"
        ))
        self._write_card(book, "测试.md", (
            "# 测试\n\n"
            "## 物理数据时间线 Physical Data Timeline\n\n"
            "| 章 | 身高 | 体重 | 三围（胸/腰/臀） | 变化事件 |\n"
            "| ---: | ---: | ---: | --- | --- |\n"
            "| 1 | 5尺 | 100斤 | 32/24/34 | 出场基线 |\n"
        ))
        result = validate(book)
        warns = messages(result, "warnings", "未声明的列")
        assert warns, f"应报未声明列警告，但无：{result.warnings}"

    def test_declared_columns_are_fine(self, tmp_path):
        book = copy_std(tmp_path)
        self._write_rules(book, (
            "# Book Rules\n\n"
            "## 物理数据维度 Physical Data Dimensions\n\n"
            "| dim_id | 维度名 | 单位/取值口径 | 说明 |\n"
            "| --- | --- | --- | --- |\n"
            "| phy-001 | 身高 | 尺/寸 | 身高 |\n"
        ))
        self._write_card(book, "测试.md", (
            "# 测试\n\n"
            "## 物理数据时间线 Physical Data Timeline\n\n"
            "| 章 | 身高 | 变化事件 |\n"
            "| ---: | ---: | --- |\n"
            "| 1 | 5尺 | 出场基线 |\n"
        ))
        result = validate(book)
        assert not messages(result, "warnings", "未声明的列")


class TestRebuildIndex:
    """rebuild_index 的章节标题解析。"""

    def test_parse_title_strips_extension(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
        import rebuild_index
        num, title = rebuild_index.parse_chapter_file("0001_入门.md")
        assert num == 1
        assert title == "入门"
        assert not title.endswith(".md")


class TestCountCharacters:
    """_contract.count_characters 与 count_words 语义区分。"""

    def test_count_characters_counts_non_whitespace(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
        from _contract import count_characters, count_words
        text = "青云山下，陆恒入门。\n\n这是第一天。"
        # 字符数（去空白）> 段数（非标点连续段）
        assert count_characters(text) > count_words(text)
        assert count_characters("甲字七号舍") == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
