from pathlib import Path


def test_claude_md_contains_auto_routing_mapping() -> None:
    content = Path("CLAUDE.MD").read_text(encoding="utf-8")

    # Natural-language intents should map to MCP tools directly.
    assert "找/查/推荐某类 Engram" in content
    assert "search_engrams" in content
    assert "install_engram" in content
    assert "stats_engrams" in content
    assert "create_engram_assistant" in content


def test_claude_md_does_not_tell_user_to_run_cli_for_stats() -> None:
    content = Path("CLAUDE.MD").read_text(encoding="utf-8")
    assert "建议用户在终端运行" not in content
