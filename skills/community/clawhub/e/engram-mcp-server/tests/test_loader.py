import json
import re
from pathlib import Path

from engram_server.loader import EngramLoader


FIXTURES_DIR = Path(__file__).parent / "fixtures"
EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"


def _concrete_example_dirs() -> list[Path]:
    """Return non-template examples that should be fully runnable."""
    return sorted(
        d for d in EXAMPLES_DIR.iterdir()
        if d.is_dir() and not d.name.startswith("_") and d.name != "template"
    )


def test_list_engrams_returns_expected_items() -> None:
    loader = EngramLoader(FIXTURES_DIR)

    items = loader.list_engrams()
    names = {item["name"] for item in items}

    assert {"fitness-coach", "contract-lawyer"}.issubset(names)


def test_get_engram_info_returns_meta() -> None:
    loader = EngramLoader(FIXTURES_DIR)

    info = loader.get_engram_info("fitness-coach")

    assert info is not None
    assert info["name"] == "fitness-coach"
    assert "10年教练经验" in info["description"]
    assert info["knowledge_count"] == 5
    assert info["examples_count"] == 3


def test_load_file_supports_nested_paths() -> None:
    loader = EngramLoader(FIXTURES_DIR)

    role = loader.load_file("fitness-coach", "role.md")
    knowledge = loader.load_file("fitness-coach", "knowledge/增肌训练基础.md")

    assert role is not None
    assert "专业健身教练" in role
    assert knowledge is not None
    assert "渐进超负荷" in knowledge


def test_load_file_returns_none_for_invalid_or_missing_file() -> None:
    loader = EngramLoader(FIXTURES_DIR)

    missing = loader.load_file("fitness-coach", "knowledge/不存在.md")
    escaped = loader.load_file("fitness-coach", "../contract-lawyer/meta.json")

    assert missing is None
    assert escaped is None


def test_list_files_returns_markdown_in_subdir() -> None:
    loader = EngramLoader(FIXTURES_DIR)

    files = loader.list_files("fitness-coach", "knowledge")

    assert files
    assert files[0] == "knowledge/_index.md"
    assert "knowledge/增肌训练基础.md" in files


def test_load_engram_base_returns_role_workflow_rules_and_indexes() -> None:
    loader = EngramLoader(FIXTURES_DIR)

    content = loader.load_engram_base("fitness-coach")

    assert content is not None
    assert "## 角色" in content
    assert "专业健身教练" in content
    assert "## 工作流程" in content
    assert "明确目标与限制条件" in content
    assert "## 规则" in content
    assert "常见错误" in content
    assert "## 知识索引" in content
    assert "knowledge/膝关节损伤训练.md" in content
    assert "摘要：" in content
    assert "## 案例索引" in content
    assert "examples/膝盖疼的上班族.md" in content
    assert "uses:" in content


def test_empty_directory_does_not_raise(tmp_path: Path) -> None:
    loader = EngramLoader(tmp_path)

    assert loader.list_engrams() == []


def test_missing_meta_directory_is_skipped(tmp_path: Path) -> None:
    (tmp_path / "no-meta").mkdir(parents=True)
    (tmp_path / "has-meta").mkdir(parents=True)
    (tmp_path / "has-meta" / "meta.json").write_text(
        '{"name": "has-meta", "description": "ok"}', encoding="utf-8"
    )

    loader = EngramLoader(tmp_path)
    items = loader.list_engrams()

    assert len(items) == 1
    assert items[0]["name"] == "has-meta"


def _make_engram(tmp_path: Path, name: str = "test-expert") -> EngramLoader:
    """Helper to create a minimal engram for write/memory tests."""
    engram_dir = tmp_path / name
    engram_dir.mkdir()
    (engram_dir / "meta.json").write_text(
        f'{{"name": "{name}", "description": "test"}}', encoding="utf-8"
    )
    (engram_dir / "role.md").write_text("# test role", encoding="utf-8")
    return EngramLoader(tmp_path)


def test_write_file_creates_and_overwrites(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    assert loader.write_file("test-expert", "knowledge/topic.md", "v1")
    assert (tmp_path / "test-expert" / "knowledge" / "topic.md").read_text() == "v1"

    assert loader.write_file("test-expert", "knowledge/topic.md", "v2")
    assert (tmp_path / "test-expert" / "knowledge" / "topic.md").read_text() == "v2"


def test_write_file_append_mode(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    loader.write_file("test-expert", "notes.md", "line1\n")
    loader.write_file("test-expert", "notes.md", "line2\n", append=True)

    content = (tmp_path / "test-expert" / "notes.md").read_text()
    assert "line1" in content
    assert "line2" in content


def test_write_file_blocks_path_traversal(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    assert loader.write_file("test-expert", "../escape.md", "bad") is False


def test_capture_memory_creates_entry_and_index(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    ok = loader.capture_memory(
        "test-expert", "用户膝盖有旧伤", "user-profile", "膝关节活动度受限"
    )
    assert ok is True

    memory_dir = tmp_path / "test-expert" / "memory"
    assert memory_dir.is_dir()

    category_file = memory_dir / "user-profile.md"
    assert category_file.is_file()
    text = category_file.read_text()
    assert "用户膝盖有旧伤" in text
    assert "type:general" in text

    index_file = memory_dir / "_index.md"
    assert index_file.is_file()
    index_content = index_file.read_text()
    assert "膝关节活动度受限" in index_content
    assert "memory/user-profile.md" in index_content
    assert "[general]" in index_content


def test_capture_memory_with_type_and_tags(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    ok = loader.capture_memory(
        "test-expert",
        "用户偏好晨练，不喜欢夜间训练",
        "preferences",
        "偏好晨练",
        memory_type="preference",
        tags=["fitness", "schedule"],
    )
    assert ok is True

    category_file = tmp_path / "test-expert" / "memory" / "preferences.md"
    text = category_file.read_text()
    assert "type:preference" in text
    assert "tags:fitness,schedule" in text

    index_content = (tmp_path / "test-expert" / "memory" / "_index.md").read_text()
    assert "[preference]" in index_content
    assert "[fitness,schedule]" in index_content


def test_capture_memory_with_conversation_id(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    ok = loader.capture_memory(
        "test-expert",
        "本次对话决定从3x/week开始",
        "decisions",
        "初始训练频率3次/周",
        memory_type="decision",
        conversation_id="session-abc123",
    )
    assert ok is True

    text = (tmp_path / "test-expert" / "memory" / "decisions.md").read_text()
    assert "conv:session-abc123" in text
    assert "type:decision" in text


def test_capture_tool_trace_creates_structured_memory(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    ok = loader.capture_tool_trace(
        "test-expert",
        tool_name="search_engrams",
        intent="查找营养相关专家",
        result_summary="命中 3 个候选专家",
        args_summary='query="nutrition"',
        status="ok",
    )
    assert ok is True

    trace_file = tmp_path / "test-expert" / "memory" / "tool-trace.md"
    text = trace_file.read_text(encoding="utf-8")
    assert "tool: search_engrams" in text
    assert "intent: 查找营养相关专家" in text
    assert "result: 命中 3 个候选专家" in text
    assert "type:tool_trace" in text

    index_text = (tmp_path / "test-expert" / "memory" / "_index.md").read_text(
        encoding="utf-8"
    )
    assert "`memory/tool-trace.md`" in index_text
    assert "search_engrams [ok]" in index_text


def test_list_recent_memory_summaries_returns_latest_entries(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)
    for idx in range(3):
        loader.capture_tool_trace(
            "test-expert",
            tool_name="read_engram_file",
            intent=f"读取知识文件{idx}",
            result_summary=f"读取成功{idx}",
            status="ok",
        )
        loader._throttle_cache.clear()

    latest_two = loader.list_recent_memory_summaries(
        "test-expert", "tool-trace", limit=2
    )
    assert len(latest_two) == 2
    assert "读取知识文件0" not in "\n".join(latest_two)
    assert "读取知识文件2" in "\n".join(latest_two)


def test_capture_memory_throttle(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)
    content = "用户膝盖有旧伤"

    loader.capture_memory("test-expert", content, "user-profile", "膝关节活动度受限")
    loader.capture_memory("test-expert", content, "user-profile", "膝关节活动度受限")

    text = (tmp_path / "test-expert" / "memory" / "user-profile.md").read_text()
    # Only one entry should exist (second call throttled)
    assert text.count("用户膝盖有旧伤") == 1


def test_consolidate_memory_archives_and_replaces(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    # Add some raw entries first
    loader.capture_memory("test-expert", "偏好晨练", "preferences", "喜欢早上训练", memory_type="preference")
    # bypass throttle by using different content
    loader._throttle_cache.clear()
    loader.capture_memory("test-expert", "家有哑铃", "preferences", "居家训练设备", memory_type="preference")

    # Consolidate
    ok = loader.consolidate_memory(
        "test-expert",
        "preferences",
        "【训练时间】偏好晨练。【设备】家有哑铃。",
        "训练偏好摘要",
    )
    assert ok is True

    memory_dir = tmp_path / "test-expert" / "memory"

    # Archive file should exist and contain original entries
    archive = memory_dir / "preferences-archive.md"
    assert archive.is_file()
    archive_text = archive.read_text()
    assert "偏好晨练" in archive_text
    assert "家有哑铃" in archive_text

    # Category file should now contain only consolidated content
    cat_text = (memory_dir / "preferences.md").read_text()
    assert "type:consolidated" in cat_text
    assert "【训练时间】" in cat_text
    assert "type:preference" not in cat_text  # raw entry format gone

    # Index should have exactly one entry for this category
    index_text = (memory_dir / "_index.md").read_text()
    assert index_text.count("`memory/preferences.md`") == 1
    assert "[consolidated]" in index_text
    assert "训练偏好摘要" in index_text


def test_consolidate_memory_multiple_rounds(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    loader.capture_memory("test-expert", "内容A", "history", "摘要A", memory_type="history")
    loader.consolidate_memory("test-expert", "history", "第一次压缩内容", "第一次压缩")
    loader._throttle_cache.clear()
    loader.capture_memory("test-expert", "内容B", "history", "摘要B", memory_type="history")
    loader.consolidate_memory("test-expert", "history", "第二次压缩内容", "第二次压缩")

    archive = tmp_path / "test-expert" / "memory" / "history-archive.md"
    archive_text = archive.read_text()
    # Both rounds should be in archive
    assert "第一次压缩内容" in archive_text
    assert "内容B" in archive_text

    index_text = (tmp_path / "test-expert" / "memory" / "_index.md").read_text()
    assert index_text.count("`memory/history.md`") == 1
    assert "第二次压缩" in index_text


def test_count_memory_entries(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    assert loader.count_memory_entries("test-expert", "preferences") == 0
    loader.capture_memory("test-expert", "内容1", "preferences", "摘要1")
    assert loader.count_memory_entries("test-expert", "preferences") == 1
    loader._throttle_cache.clear()
    loader.capture_memory("test-expert", "内容2", "preferences", "摘要2")
    assert loader.count_memory_entries("test-expert", "preferences") == 2

    loader.capture_memory(
        "test-expert", "喜欢早上训练", "preferences", "偏好晨练"
    )

    base = loader.load_engram_base("test-expert")
    assert base is not None
    assert "## 动态记忆" in base
    assert "偏好晨练" in base


def test_delete_memory_removes_entry_and_index(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    loader.capture_memory("test-expert", "用户左膝旧伤", "user-profile", "膝关节受限", memory_type="fact")

    ok = loader.delete_memory("test-expert", "user-profile", "膝关节受限")
    assert ok is True

    index_text = (tmp_path / "test-expert" / "memory" / "_index.md").read_text()
    assert "膝关节受限" not in index_text

    cat_text = (tmp_path / "test-expert" / "memory" / "user-profile.md").read_text()
    assert "用户左膝旧伤" not in cat_text


def test_delete_memory_returns_false_for_missing_summary(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)
    loader.capture_memory("test-expert", "内容", "user-profile", "真实摘要")

    ok = loader.delete_memory("test-expert", "user-profile", "不存在的摘要")
    assert ok is False


def test_correct_memory_updates_content_and_index(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    loader.capture_memory(
        "test-expert", "用户体重80kg", "user-profile", "体重80kg", memory_type="fact"
    )

    ok = loader.correct_memory(
        "test-expert",
        "user-profile",
        "体重80kg",
        "用户体重75kg（已减重）",
        "体重75kg",
        memory_type="fact",
    )
    assert ok is True

    index_text = (tmp_path / "test-expert" / "memory" / "_index.md").read_text()
    assert "体重75kg" in index_text
    assert "体重80kg" not in index_text

    cat_text = (tmp_path / "test-expert" / "memory" / "user-profile.md").read_text()
    assert "用户体重75kg" in cat_text
    assert "用户体重80kg" not in cat_text


def test_correct_memory_returns_false_for_missing_summary(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)
    loader.capture_memory("test-expert", "内容", "user-profile", "真实摘要")

    ok = loader.correct_memory(
        "test-expert", "user-profile", "不存在的摘要", "新内容", "新摘要"
    )
    assert ok is False


def test_add_knowledge_creates_file_and_updates_index(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)
    (tmp_path / "test-expert" / "knowledge").mkdir()
    (tmp_path / "test-expert" / "knowledge" / "_index.md").write_text(
        "- `knowledge/existing.md` - 已有知识\n", encoding="utf-8"
    )

    ok = loader.add_knowledge(
        "test-expert",
        "new-topic",
        "# 新知识\n\n这是新增的知识内容。",
        "新增主题的核心要点",
    )
    assert ok is True

    knowledge_file = tmp_path / "test-expert" / "knowledge" / "new-topic.md"
    assert knowledge_file.is_file()
    assert "新增的知识内容" in knowledge_file.read_text()

    index_text = (tmp_path / "test-expert" / "knowledge" / "_index.md").read_text()
    assert "knowledge/new-topic.md" in index_text
    assert "新增主题的核心要点" in index_text
    assert "已有知识" in index_text  # existing entry preserved


def test_add_knowledge_auto_adds_md_extension(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)
    (tmp_path / "test-expert" / "knowledge").mkdir()
    (tmp_path / "test-expert" / "knowledge" / "_index.md").write_text("", encoding="utf-8")

    loader.add_knowledge("test-expert", "topic-no-ext", "内容", "摘要")

    assert (tmp_path / "test-expert" / "knowledge" / "topic-no-ext.md").is_file()


def test_add_knowledge_nested_prefers_subdir_index(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)
    (tmp_path / "test-expert" / "knowledge" / "训练基础").mkdir(parents=True)
    (tmp_path / "test-expert" / "knowledge" / "_index.md").write_text(
        "- `knowledge/existing.md` - 顶层\n", encoding="utf-8"
    )
    (tmp_path / "test-expert" / "knowledge" / "训练基础" / "_index.md").write_text(
        "- `knowledge/训练基础/existing.md` - 子目录\n", encoding="utf-8"
    )

    ok = loader.add_knowledge(
        "test-expert",
        "训练基础/深蹲模式",
        "# 深蹲模式\n正文",
        "分组知识条目",
    )
    assert ok is True

    nested_file = tmp_path / "test-expert" / "knowledge" / "训练基础" / "深蹲模式.md"
    assert nested_file.is_file()
    nested_index = (
        tmp_path / "test-expert" / "knowledge" / "训练基础" / "_index.md"
    ).read_text(encoding="utf-8")
    top_index = (tmp_path / "test-expert" / "knowledge" / "_index.md").read_text(
        encoding="utf-8"
    )
    assert "knowledge/训练基础/深蹲模式.md" in nested_index
    assert "knowledge/训练基础/深蹲模式.md" not in top_index


def test_add_knowledge_nested_without_subdir_index_falls_back_to_top_index(
    tmp_path: Path,
) -> None:
    loader = _make_engram(tmp_path)
    (tmp_path / "test-expert" / "knowledge" / "训练基础").mkdir(parents=True)
    (tmp_path / "test-expert" / "knowledge" / "_index.md").write_text(
        "", encoding="utf-8"
    )

    ok = loader.add_knowledge(
        "test-expert",
        "训练基础/核心稳定",
        "# 核心稳定\n正文",
        "未建子索引时追加到顶层",
    )
    assert ok is True

    top_index = (tmp_path / "test-expert" / "knowledge" / "_index.md").read_text(
        encoding="utf-8"
    )
    assert "knowledge/训练基础/核心稳定.md" in top_index


def test_expired_memory_is_archived_on_load(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)
    loader.capture_memory(
        "test-expert",
        "这是一个会过期的状态",
        "status",
        "临时状态",
        memory_type="fact",
        expires="2000-01-01",
    )

    loaded = loader.load_engram_base("test-expert")
    assert loaded is not None
    assert "临时状态" not in loaded

    memory_dir = tmp_path / "test-expert" / "memory"
    expired_file = memory_dir / "status-expired.md"
    assert expired_file.is_file()
    assert "这是一个会过期的状态" in expired_file.read_text(encoding="utf-8")

    status_file = memory_dir / "status.md"
    assert "这是一个会过期的状态" not in status_file.read_text(encoding="utf-8")
    assert "临时状态" not in (memory_dir / "_index.md").read_text(encoding="utf-8")


def test_hot_index_contains_category_summaries(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)
    loader.capture_memory(
        "test-expert", "偏好晨练", "preferences", "喜欢早晨训练", memory_type="preference"
    )
    loader.capture_memory(
        "test-expert", "完成第一次训练", "history", "第一次训练已完成", memory_type="history"
    )

    index_text = (tmp_path / "test-expert" / "memory" / "_index.md").read_text(encoding="utf-8")
    assert "## 分类摘要" in index_text
    assert "`preferences`" in index_text
    assert "`history`" in index_text
    assert "## 最近记忆（最多50条）" in index_text


def test_consolidation_hint_threshold_is_30(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)
    for i in range(29):
        loader.capture_memory("test-expert", f"内容{i}", "history", f"摘要{i}")

    loaded_29 = loader.load_engram_base("test-expert")
    assert loaded_29 is not None
    assert "💡 当前共" not in loaded_29

    loader.capture_memory("test-expert", "内容29", "history", "摘要29")
    loaded_30 = loader.load_engram_base("test-expert")
    assert loaded_30 is not None
    assert "💡 当前共 30 条记忆" in loaded_30


def test_global_memory_is_loaded_across_engrams(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path, "expert-a")
    _make_engram(tmp_path, "expert-b")

    ok = loader.capture_memory(
        "expert-a",
        "用户居住在深圳",
        "user-profile",
        "居住地：深圳",
        memory_type="fact",
        is_global=True,
    )
    assert ok is True

    loaded = loader.load_engram_base("expert-b")
    assert loaded is not None
    assert "## 全局用户记忆" in loaded
    assert "居住地：深圳" in loaded


def test_loader_reads_from_project_and_global_roots(tmp_path: Path) -> None:
    project_root = tmp_path / "project-engram"
    global_root = tmp_path / "global-engram"
    project_root.mkdir()
    global_root.mkdir()
    _make_engram(project_root, "project-only")
    _make_engram(global_root, "global-only")

    shared_project = project_root / "shared-expert" / "meta.json"
    shared_project.parent.mkdir(parents=True)
    shared_project.write_text(
        '{"name":"shared-expert","description":"project version"}',
        encoding="utf-8",
    )
    (shared_project.parent / "role.md").write_text("project role", encoding="utf-8")

    shared_global = global_root / "shared-expert" / "meta.json"
    shared_global.parent.mkdir(parents=True)
    shared_global.write_text(
        '{"name":"shared-expert","description":"global version"}',
        encoding="utf-8",
    )
    (shared_global.parent / "role.md").write_text("global role", encoding="utf-8")

    loader = EngramLoader(
        packs_dir=[project_root, global_root],
        default_packs_dir=global_root,
    )
    listed = loader.list_engrams()
    names = [item["name"] for item in listed]

    assert {"project-only", "global-only", "shared-expert"}.issubset(set(names))
    assert names.count("shared-expert") == 1
    assert loader.get_engram_info("shared-expert")["description"] == "project version"

    ok = loader.capture_memory(
        "shared-expert",
        "全局偏好：中文回复",
        "profile",
        "语言偏好：中文",
        is_global=True,
    )
    assert ok is True
    assert (global_root / "_global" / "memory" / "_index.md").is_file()


def test_load_engram_base_supports_parent_knowledge_inheritance(tmp_path: Path) -> None:
    parent = tmp_path / "parent"
    parent.mkdir()
    (parent / "meta.json").write_text(
        '{"name":"parent","description":"parent"}',
        encoding="utf-8",
    )
    (parent / "role.md").write_text("parent role", encoding="utf-8")
    (parent / "knowledge").mkdir()
    (parent / "knowledge" / "_index.md").write_text(
        "- `knowledge/base.md` - 父知识摘要",
        encoding="utf-8",
    )

    child = tmp_path / "child"
    child.mkdir()
    (child / "meta.json").write_text(
        '{"name":"child","description":"child","extends":"parent"}',
        encoding="utf-8",
    )
    (child / "role.md").write_text("child role", encoding="utf-8")

    loader = EngramLoader(tmp_path)
    loaded = loader.load_engram_base("child")
    assert loaded is not None
    assert "## 继承知识索引（来自 parent）" in loaded
    assert "knowledge/base.md" in loaded


def test_onboarding_prompt_only_shows_before_first_memory(tmp_path: Path) -> None:
    engram_dir = tmp_path / "guide-expert"
    engram_dir.mkdir()
    (engram_dir / "meta.json").write_text(
        '{"name":"guide-expert","description":"guide"}',
        encoding="utf-8",
    )
    (engram_dir / "role.md").write_text("role", encoding="utf-8")
    (engram_dir / "rules.md").write_text(
        "# 规则\n\n## Onboarding\n- 了解用户目标\n- 了解用户约束\n",
        encoding="utf-8",
    )

    loader = EngramLoader(tmp_path)
    first_loaded = loader.load_engram_base("guide-expert")
    assert first_loaded is not None
    assert "## 首次引导" in first_loaded

    loader.capture_memory("guide-expert", "用户目标是减脂", "user-profile", "目标：减脂")
    second_loaded = loader.load_engram_base("guide-expert")
    assert second_loaded is not None
    assert "## 首次引导" not in second_loaded


def test_all_example_rules_have_onboarding_section() -> None:
    missing = []
    for rules_file in sorted(EXAMPLES_DIR.glob("*/rules.md")):
        content = rules_file.read_text(encoding="utf-8")
        if "## Onboarding" not in content:
            missing.append(str(rules_file))
    assert missing == []


def test_concrete_examples_have_required_core_files() -> None:
    required = (
        "meta.json",
        "role.md",
        "rules.md",
        "workflow.md",
        "knowledge/_index.md",
        "examples/_index.md",
        "memory/_index.md",
    )
    missing: list[str] = []
    for engram_dir in _concrete_example_dirs():
        for rel in required:
            if not (engram_dir / rel).is_file():
                missing.append(f"{engram_dir.name}/{rel}")
    assert missing == []


def test_concrete_example_indexes_only_reference_existing_files() -> None:
    missing_refs: list[str] = []
    for engram_dir in _concrete_example_dirs():
        for index_rel in ("knowledge/_index.md", "examples/_index.md", "memory/_index.md"):
            index_file = engram_dir / index_rel
            content = index_file.read_text(encoding="utf-8")
            for token in re.findall(r"`([^`]+)`", content):
                if not token.startswith(("knowledge/", "examples/", "memory/")):
                    continue
                if not (engram_dir / token).is_file():
                    missing_refs.append(f"{engram_dir.name}:{index_rel}:{token}")
    assert missing_refs == []


def test_concrete_examples_meta_counts_match_real_files() -> None:
    mismatches: list[str] = []
    for engram_dir in _concrete_example_dirs():
        meta = json.loads((engram_dir / "meta.json").read_text(encoding="utf-8"))
        knowledge_count = len([
            f for f in (engram_dir / "knowledge").glob("*.md")
            if f.name != "_index.md"
        ])
        examples_count = len([
            f for f in (engram_dir / "examples").glob("*.md")
            if f.name != "_index.md"
        ])
        if meta.get("knowledge_count") != knowledge_count:
            mismatches.append(
                f"{engram_dir.name}:knowledge_count={meta.get('knowledge_count')} actual={knowledge_count}"
            )
        if meta.get("examples_count") != examples_count:
            mismatches.append(
                f"{engram_dir.name}:examples_count={meta.get('examples_count')} actual={examples_count}"
            )
    assert mismatches == []


def test_each_concrete_example_has_expires_and_confidence_memory_samples() -> None:
    missing_markers: list[str] = []
    for engram_dir in _concrete_example_dirs():
        merged = "\n".join(
            f.read_text(encoding="utf-8")
            for f in sorted((engram_dir / "memory").glob("*.md"))
        )
        for marker in ("expires:", "type:inferred", "type:stated"):
            if marker not in merged:
                missing_markers.append(f"{engram_dir.name}:{marker}")
    assert missing_markers == []
