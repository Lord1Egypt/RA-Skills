"""Tests for task_suite_generator — the core module of skill-forge."""

import pytest
import sys
from pathlib import Path

# Add skill root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.task_suite_generator import (
    parse_frontmatter,
    generate_task_suite,
    generate_trigger_tasks,
    generate_when_to_use_tasks,
    generate_example_tasks,
    generate_anti_example_tasks,
    generate_output_format_tasks,
    extract_keywords,
    deduplicate_tasks,
    GeneratedTask,
)


class TestParseFrontmatter:
    def test_valid_frontmatter(self):
        content = "---\nname: test\ndescription: a test\n---\n\n# Body"
        fm, body = parse_frontmatter(content)
        assert fm["name"] == "test"
        assert fm["description"] == "a test"
        assert "Body" in body

    def test_no_frontmatter(self):
        fm, body = parse_frontmatter("# Just body")
        assert fm == {}
        assert "Just body" in body

    def test_empty_frontmatter(self):
        content = "---\n---\n\n# Body"
        fm, body = parse_frontmatter(content)
        assert fm == {}
        assert "Body" in body

    def test_frontmatter_with_list(self):
        content = "---\nname: test\ntriggers:\n  - foo\n  - bar\n---\n\nbody"
        fm, body = parse_frontmatter(content)
        assert fm["triggers"] == ["foo", "bar"]

    def test_content_without_triple_dashes(self):
        content = "Just some content without frontmatter"
        fm, body = parse_frontmatter(content)
        assert fm == {}
        assert body == content


class TestGenerateTriggerTasks:
    def test_generates_from_description(self):
        fm = {"name": "test-skill", "description": "Analyze code for bugs"}
        tasks = generate_trigger_tasks(fm)
        assert len(tasks) == 1
        assert tasks[0].id == "test-skill-core-capability"
        assert tasks[0].judge["type"] == "llm-rubric"
        assert "Analyze code for bugs" in tasks[0].judge["rubric"]

    def test_empty_description(self):
        tasks = generate_trigger_tasks({"name": "test", "description": ""})
        assert len(tasks) == 0

    def test_missing_description(self):
        tasks = generate_trigger_tasks({"name": "test"})
        assert len(tasks) == 0

    def test_missing_name_uses_unknown(self):
        tasks = generate_trigger_tasks({"description": "Do stuff"})
        assert len(tasks) == 1
        assert tasks[0].id == "unknown-core-capability"


class TestGenerateWhenToUseTasks:
    def test_extracts_bullet_points(self):
        body = "\n## When to Use\n- When running tests\n- When validating output\n- When checking format\n"
        tasks = generate_when_to_use_tasks(body, {"name": "test"})
        assert len(tasks) == 3
        assert tasks[0].id == "test-use-case-01"
        assert tasks[1].id == "test-use-case-02"
        assert tasks[2].id == "test-use-case-03"

    def test_max_three_bullets(self):
        body = "\n## When to Use\n- A\n- B\n- C\n- D\n- E\n"
        tasks = generate_when_to_use_tasks(body, {"name": "test"})
        assert len(tasks) == 3

    def test_no_when_section(self):
        body = "\n## Other Section\n- stuff\n"
        tasks = generate_when_to_use_tasks(body, {"name": "test"})
        assert len(tasks) == 0

    def test_chinese_header(self):
        body = "\n## 使用场景\n- 当需要运行测试时\n"
        tasks = generate_when_to_use_tasks(body, {"name": "test"})
        assert len(tasks) == 1

    def test_asterisk_bullets(self):
        body = "\n## When to Use\n* First scenario\n* Second scenario\n"
        tasks = generate_when_to_use_tasks(body, {"name": "test"})
        assert len(tasks) == 2

    def test_section_boundary(self):
        body = "\n## When to Use\n- Valid task\n\n## When NOT to Use\n- Invalid task\n"
        tasks = generate_when_to_use_tasks(body, {"name": "test"})
        assert len(tasks) == 1
        assert "Valid task" in tasks[0].prompt


class TestGenerateExampleTasks:
    def test_extracts_from_example_tags(self):
        body = """
## Usage
<example>
Correct: run `generate_notes --platform ios`
produces structured markdown with commit refs
</example>
"""
        tasks = generate_example_tasks(body, {"name": "test"})
        assert len(tasks) >= 1
        assert tasks[0].source == "example_tag"
        assert tasks[0].judge["type"] == "contains"

    def test_multiple_examples(self):
        body = """
<example>
First example with "keyword1"
</example>
<example>
Second example with "keyword2"
</example>
<example>
Third example with "keyword3"
</example>
"""
        tasks = generate_example_tasks(body, {"name": "test"})
        # Max 2 from examples
        assert len(tasks) <= 2

    def test_empty_example(self):
        body = "<example>\n\n</example>"
        tasks = generate_example_tasks(body, {"name": "test"})
        assert len(tasks) == 0

    def test_example_with_only_headers(self):
        body = "<example>\n# Just a header\n</example>"
        tasks = generate_example_tasks(body, {"name": "test"})
        # Headers are filtered out, so no lines remain
        assert len(tasks) == 0


class TestGenerateAntiExampleTasks:
    def test_extracts_from_anti_example_tags(self):
        body = """
<anti-example>
Wrong: using orchestrator just to check scores
should use improvement-learner instead
</anti-example>
"""
        tasks = generate_anti_example_tasks(body, {"name": "test"})
        assert len(tasks) == 1
        assert "anti-pattern" in tasks[0].id
        assert tasks[0].judge["type"] == "llm-rubric"

    def test_max_two_anti_examples(self):
        body = """
<anti-example>Anti 1</anti-example>
<anti-example>Anti 2</anti-example>
<anti-example>Anti 3</anti-example>
"""
        tasks = generate_anti_example_tasks(body, {"name": "test"})
        assert len(tasks) == 2


class TestGenerateOutputFormatTasks:
    def test_extracts_from_output_table(self):
        body = (
            "\n## Output Artifacts\n"
            "| Request | Deliverable |\n"
            "|---------|------------|\n"
            "| Test run | JSON report with pass/fail counts |\n"
        )
        tasks = generate_output_format_tasks(body, {"name": "test"})
        assert len(tasks) == 1
        assert tasks[0].source == "output_artifacts"

    def test_skips_header_row(self):
        body = """
## Output Artifacts
| Request | Deliverable |
|---------|------------|
"""
        tasks = generate_output_format_tasks(body, {"name": "test"})
        assert len(tasks) == 0

    def test_no_output_section(self):
        body = "## Other Section\nstuff"
        tasks = generate_output_format_tasks(body, {"name": "test"})
        assert len(tasks) == 0


class TestExtractKeywords:
    def test_extracts_quoted_strings(self):
        kw = extract_keywords('Use "ContainsJudge" for "keyword matching"')
        assert "ContainsJudge" in kw
        assert "keyword matching" in kw

    def test_extracts_camelcase(self):
        kw = extract_keywords("Use TaskRunner and PytestJudge")
        assert "TaskRunner" in kw
        assert "PytestJudge" in kw

    def test_filters_short_quoted(self):
        kw = extract_keywords('"a" and "be" and "long enough"')
        assert "a" not in kw
        assert "be" not in kw
        assert "long enough" in kw

    def test_deduplicates(self):
        kw = extract_keywords("TaskRunner TaskRunner TaskRunner")
        assert kw.count("TaskRunner") == 1

    def test_max_four_keywords(self):
        kw = extract_keywords('"a1234" "b1234" "c1234" "d1234" "e1234"')
        assert len(kw) <= 4

    def test_code_blocks_removed(self):
        kw = extract_keywords("```python\ncode_here\n```\nSomeClass outside")
        assert "SomeClass" in kw


class TestDeduplication:
    def test_removes_duplicate_ids(self):
        t1 = GeneratedTask(id="a", description="x", prompt="p", judge={})
        t2 = GeneratedTask(id="a", description="y", prompt="q", judge={})
        t3 = GeneratedTask(id="b", description="z", prompt="r", judge={})
        result = deduplicate_tasks([t1, t2, t3])
        assert len(result) == 2
        # First occurrence wins
        assert result[0].description == "x"

    def test_preserves_order(self):
        tasks = [
            GeneratedTask(id="c", description="3", prompt="p", judge={}),
            GeneratedTask(id="a", description="1", prompt="p", judge={}),
            GeneratedTask(id="b", description="2", prompt="p", judge={}),
        ]
        result = deduplicate_tasks(tasks)
        assert [t.id for t in result] == ["c", "a", "b"]

    def test_empty_list(self):
        assert deduplicate_tasks([]) == []


class TestFullGeneration:
    def test_generates_from_real_skill(self, tmp_path):
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            """---
name: test-skill
description: Test skill for unit testing
triggers:
  - test
---

# Test Skill

## When to Use
- When you need to run tests
- When validating output format

<example>
Run: python3 -m pytest tests/ -v
All tests pass
</example>

<anti-example>
Wrong: skipping tests before commit
</anti-example>

## Output Artifacts
| Request | Deliverable |
|---------|------------|
| Test run | JSON report with pass/fail counts |
"""
        )
        suite = generate_task_suite(skill_dir)
        assert suite["skill_id"] == "test-skill"
        assert suite["version"] == "1.0"
        assert suite["generated_by"] == "skill-forge"
        assert len(suite["tasks"]) >= 3  # trigger + use-cases + example/anti
        # Verify task structure
        for task in suite["tasks"]:
            assert "id" in task
            assert "prompt" in task
            assert "judge" in task
            assert "description" in task

    def test_max_ten_tasks(self, tmp_path):
        """Even with many sections, output is capped at 10 tasks."""
        skill_dir = tmp_path / "big-skill"
        skill_dir.mkdir()
        bullets = "\n".join(f"- Use case {i}" for i in range(20))
        examples = "\n".join(
            f'<example>\nExample {i} with "keyword{i}"\n</example>'
            for i in range(10)
        )
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: big\ndescription: Big skill\n---\n\n"
            f"## When to Use\n{bullets}\n\n{examples}\n"
        )
        suite = generate_task_suite(skill_dir)
        assert len(suite["tasks"]) <= 10

    def test_missing_skill_md(self, tmp_path):
        skill_dir = tmp_path / "empty-skill"
        skill_dir.mkdir()
        with pytest.raises(FileNotFoundError):
            generate_task_suite(skill_dir)

    def test_minimal_skill(self, tmp_path):
        """A SKILL.md with only frontmatter still produces at least 1 task."""
        skill_dir = tmp_path / "minimal"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: minimal\ndescription: Does something\n---\n"
        )
        suite = generate_task_suite(skill_dir)
        assert len(suite["tasks"]) >= 1
        assert suite["tasks"][0]["id"] == "minimal-core-capability"

    def test_no_duplicate_ids_in_output(self, tmp_path):
        skill_dir = tmp_path / "dedup-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            """---
name: dedup
description: Test deduplication
---

## When to Use
- First scenario
- Second scenario

<example>
Example with "keyword"
</example>
"""
        )
        suite = generate_task_suite(skill_dir)
        ids = [t["id"] for t in suite["tasks"]]
        assert len(ids) == len(set(ids)), "Duplicate task IDs found"
