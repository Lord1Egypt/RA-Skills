from __future__ import annotations

from pathlib import Path

from support import load_skill_script

validate_agent_doc = load_skill_script("validate_agent_doc.py")


def write_doc(path: Path, body: str) -> None:
    path.write_text(
        """---
summary: Test document.
aliases: []
search_terms: []
use_when: []
skip_when: []
---

# Test

## 摘要

- Keep source expression.

## Insight

- Keep unique takeaway.

## Details

Original wording with light Markdown cleanup.
"""
        + body,
        encoding="utf-8",
    )


def test_validate_accepts_article_level_archived_source_map(tmp_path: Path) -> None:
    doc = tmp_path / "ok.md"
    write_doc(
        doc,
        """

## Source Map

- [[Archived/source.md]]
""",
    )

    assert validate_agent_doc.validate(doc) == []


def test_validate_rejects_legacy_block_level_source_map(tmp_path: Path) -> None:
    doc = tmp_path / "bad.md"
    write_doc(
        doc,
        """

## Source Map

| Ref | Output Block | Source Block | Source Location | Transformation |
| --- | --- | --- | --- | --- |
| S1 | `Details` | `Intro` | source.md#Intro | rewritten |
""",
    )

    assert validate_agent_doc.validate(doc) == [(
        "Source Map should be a bullet list of article-level archived Obsidian wikilinks, "
        "e.g. '- [[Archived/path/source.md]]'. / 来源映射应使用文章级归档 Obsidian wikilink 的项目列表。"
    )]


def test_validate_rejects_table_source_map_with_wikilink_alias(tmp_path: Path) -> None:
    doc = tmp_path / "table.md"
    write_doc(
        doc,
        """

## Source Map

| Source | Archived Link |
| --- | --- |
| source.md | [[Archived/source.md|source.md]] |
""",
    )

    assert validate_agent_doc.validate(doc) == [(
        "Source Map should be a bullet list of article-level archived Obsidian wikilinks, "
        "e.g. '- [[Archived/path/source.md]]'. / 来源映射应使用文章级归档 Obsidian wikilink 的项目列表。"
    )]


def test_validate_accepts_code_repo_source_map(tmp_path: Path) -> None:
    doc = tmp_path / "repo.md"
    doc.write_text(
        """---
summary: Code repo.
search_terms: []
use_when: []
skip_when: []
version: "code-repo-v1"
---

## 摘要

Code repo summary.

## Insight

- Project-level code asset.

## Details

### Repository Metadata

- Asset type: `code_project`

## Source Map

- Source repository: `repo`
- Semantic entry: `repo/repo.agent.md`
""",
        encoding="utf-8",
    )

    assert validate_agent_doc.validate(doc) == []


def test_validate_rejects_duplicate_frontmatter_title_h1(tmp_path: Path) -> None:
    doc = tmp_path / "duplicate-title.md"
    doc.write_text(
        """---
title: Duplicate Title
summary: Test document.
aliases: []
search_terms: []
use_when: []
skip_when: []
---

# Duplicate Title

## 摘要

- Keep title in frontmatter only.

## Insight

- Keep unique takeaway.

## Details

Original wording.
""",
        encoding="utf-8",
    )

    assert validate_agent_doc.validate(doc) == [
        "Do not repeat the frontmatter title as a body H1; start with ## Summary / 摘要. / 不要在正文 H1 重复 frontmatter 标题；正文应从 ## Summary / 摘要 开始。"
    ]


def test_validate_rejects_legacy_conclusion_heading(tmp_path: Path) -> None:
    doc = tmp_path / "legacy-heading.md"
    doc.write_text(
        """---
summary: Test document.
aliases: []
search_terms: []
use_when: []
skip_when: []
---

## 先给结论

- Legacy heading should no longer validate.

## Details

Body.
""",
        encoding="utf-8",
    )

    assert validate_agent_doc.validate(doc) == [
        "Missing section: ## Summary / 摘要 / 缺少章节：## Summary / 摘要",
        "Missing section: ## Insight / 洞察 / 缺少章节：## Insight / 洞察",
    ]


def test_validate_rejects_duplicate_merged_boilerplate_heading(tmp_path: Path) -> None:
    doc = tmp_path / "duplicate-boilerplate.md"
    write_doc(
        doc,
        """

### 欢迎交流与合作

Contact text.

### 来源：second.md

Body.

### 欢迎交流与合作

Contact text.
""",
    )

    assert validate_agent_doc.validate(doc) == [
        "Duplicate boilerplate section in merged output: ### 欢迎交流与合作 appears 2 times; keep at most one. "
        "/ 合并输出中样板章节重复：### 欢迎交流与合作 出现 2 次；最多保留一次。"
    ]


def test_validate_rejects_empty_related_brackets(tmp_path: Path) -> None:
    doc = tmp_path / "bad-related.md"
    doc.write_text(
        """---
summary: Test document.
aliases: []
search_terms: []
use_when: []
skip_when: []
related:
[]
---

## 摘要

- Keep empty related omitted.

## Insight

- Keep unique takeaway.

## Details

Body.
""",
        encoding="utf-8",
    )

    assert validate_agent_doc.validate(doc) == [
        "Omit empty related frontmatter instead of writing related: [] or an empty related field. "
        "/ 省略空的 related frontmatter，不要写 related: [] 或空 related 字段。"
    ]


def test_validate_rejects_empty_related_field(tmp_path: Path) -> None:
    doc = tmp_path / "empty-related.md"
    doc.write_text(
        """---
summary: Test document.
aliases: []
search_terms: []
use_when: []
skip_when: []
related:
version: 0.6.5
---

## 摘要

- Keep empty related omitted.

## Insight

- Keep unique takeaway.

## Details

Body.
""",
        encoding="utf-8",
    )

    assert validate_agent_doc.validate(doc) == [
        "Omit empty related frontmatter instead of writing related: [] or an empty related field. "
        "/ 省略空的 related frontmatter，不要写 related: [] 或空 related 字段。"
    ]


def test_validate_rejects_unsized_images(tmp_path: Path) -> None:
    doc = tmp_path / "unsized-image.md"
    write_doc(
        doc,
        """

![[diagram.png]]

![formula](https://example.com/formula.png)
""",
    )

    assert validate_agent_doc.validate(doc) == [
        "Images should include an Obsidian width hint, e.g. ![[image.png|560]] or ![alt|560](url). "
        "/ 图片应包含 Obsidian 宽度提示。"
    ]


def test_validate_rejects_duplicate_conclusion_summary_section(tmp_path: Path) -> None:
    doc = tmp_path / "duplicate-summary.md"
    doc.write_text(
        """---
summary: Test document.
aliases: []
search_terms: []
use_when: []
skip_when: []
---

## 摘要

- 第一条核心结论已经提升到结论区。
- 第二条核心结论也已经提升到结论区。

## Insight

- Keep unique takeaway.

## Details

### 摘要总结

- 第一条核心结论已经提升到结论区。
- 第二条核心结论也已经提升到结论区。

### 全文

正文内容。
""",
        encoding="utf-8",
    )

    assert validate_agent_doc.validate(doc) == [
        (
            "Do not duplicate conclusion content in Details summary sections; "
            "remove repeated legacy summary content after it is promoted to ## Summary / 摘要. / 不要在详情的摘要小节重复结论；内容提升到 ## Summary / 摘要 后应删除重复项。"
        )
    ]


def test_validate_accepts_non_duplicate_summary_section(tmp_path: Path) -> None:
    doc = tmp_path / "non-duplicate-summary.md"
    doc.write_text(
        """---
summary: Test document.
aliases: []
search_terms: []
use_when: []
skip_when: []
---

## 摘要

- 第一条核心结论已经提升到结论区。

## Insight

- Keep unique takeaway.

## Details

### 摘要总结

- 这里保留的是不同的来源备注，不重复结论区的表达。

### 全文

正文内容。
""",
        encoding="utf-8",
    )

    assert validate_agent_doc.validate(doc) == []


def test_validate_rejects_source_h2_inside_details(tmp_path: Path) -> None:
    doc = tmp_path / "source-h2.md"
    doc.write_text(
        """---
summary: Test document.
aliases: []
search_terms: []
use_when: []
skip_when: []
---

## 摘要

- Keep source headings below Details.

## Insight

- Keep unique takeaway.

## Details

## Source Title

Body.
""",
        encoding="utf-8",
    )

    assert validate_agent_doc.validate(doc) == [
        "Source headings inside ## Details / 详情 should be H3 or deeper. "
        "/ ## Details / 详情 内的来源标题应使用 H3 或更深层级。"
    ]


def test_validate_allows_h2_inside_fenced_prompt_block(tmp_path: Path) -> None:
    doc = tmp_path / "prompt-h2.md"
    doc.write_text(
        """---
summary: Test document.
aliases: []
search_terms: []
use_when: []
skip_when: []
---

## 摘要

- Preserve prompt wording.

## Insight

- Keep unique takeaway.

## Details

```text
## 执行流程

- 保留 prompt 内部的 Markdown 标题。
```
""",
        encoding="utf-8",
    )

    assert validate_agent_doc.validate(doc) == []


def test_validate_rejects_empty_summary_section(tmp_path: Path) -> None:
    doc = tmp_path / "empty-summary.md"
    doc.write_text(
        """---
summary: Test document.
aliases: []
search_terms: []
use_when: []
skip_when: []
---

## 摘要

- Useful conclusion.

## Insight

- Keep unique takeaway.

## Details

### 摘要总结

### 全文

Body.
""",
        encoding="utf-8",
    )

    assert validate_agent_doc.validate(doc) == [
        "Omit empty summary sections inside Details. / 省略 Details 内的空摘要小节。"
    ]


def test_validate_rejects_cover_metadata_conclusion_when_summary_exists(tmp_path: Path) -> None:
    doc = tmp_path / "cover-conclusion.md"
    doc.write_text(
        """---
summary: Test document.
aliases: []
search_terms: []
use_when: []
skip_when: []
---

## 摘要

- 标题：未知标题
- 链接：https://example.com
- 发布日期：未知日期

## Insight

- Keep unique takeaway.

## Details

### 摘要总结

- 这是来源中真正有信息量的摘要。

### 全文

Body.
""",
        encoding="utf-8",
    )

    assert validate_agent_doc.validate(doc) == [
        "Do not use cover metadata as ## Summary / 摘要 when a source summary exists. / 原文存在摘要时，不要用封面 metadata 充当 ## Summary / 摘要。"
    ]
