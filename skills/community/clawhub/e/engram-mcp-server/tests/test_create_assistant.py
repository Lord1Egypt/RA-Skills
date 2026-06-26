from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


REPO_ROOT = Path(__file__).resolve().parents[1]


def _result_text(result) -> str:
    return "\n".join(
        item.text for item in result.content if hasattr(item, "text") and item.text
    )


async def _open_session(packs_dir: Path) -> ClientSession:
    server = StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "engram_server.server",
            "serve",
            "--packs-dir",
            str(packs_dir),
        ],
        cwd=str(packs_dir),
    )

    stdio = stdio_client(server)
    read_stream, write_stream = await stdio.__aenter__()
    session_ctx = ClientSession(read_stream, write_stream)
    session = await session_ctx.__aenter__()
    await session.initialize()

    session._test_stdio_ctx = stdio  # type: ignore[attr-defined]
    session._test_session_ctx = session_ctx  # type: ignore[attr-defined]
    return session


async def _close_session(session: ClientSession) -> None:
    await session._test_session_ctx.__aexit__(None, None, None)  # type: ignore[attr-defined]
    await session._test_stdio_ctx.__aexit__(None, None, None)  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_create_assistant_guided_auto_fill_and_finalize(tmp_path: Path) -> None:
    session = await _open_session(tmp_path)
    try:
        draft_raw = _result_text(
            await session.call_tool(
                "create_engram_assistant",
                {
                    "mode": "guided",
                    "topic": "健身康复教练",
                    "name": "rehab-coach",
                    "style": "你来",
                    "constraints": "你来",
                },
            )
        )
        payload = json.loads(draft_raw)
        draft_json = json.dumps(payload["draft"], ensure_ascii=False)

        finalized = _result_text(
            await session.call_tool(
                "finalize_engram_draft",
                {
                    "draft_json": draft_json,
                    "confirm": True,
                    "nested": True,
                },
            )
        )
    finally:
        await _close_session(session)

    assert payload["requires_confirmation"] is True
    assert "style" in payload["draft"]["auto_filled_fields"]
    assert "constraints" in payload["draft"]["auto_filled_fields"]
    assert "创建完成：rehab-coach" in finalized
    assert "草稿已通过 lint 校验" in finalized

    target = tmp_path / ".claude" / "engram" / "rehab-coach"
    assert (target / "knowledge" / "_index.md").is_file()
    example_file = target / "examples" / "典型场景.md"
    assert example_file.is_file()
    assert (target / "memory" / "_index.md").is_file()
    example_text = example_file.read_text(encoding="utf-8")
    assert "id:" in example_text
    assert "title:" in example_text
    assert "uses:" in example_text
    assert "tags:" in example_text
    assert "updated_at:" in example_text
    assert "## 背景" in example_text
    assert "## 评估过程" in example_text
    assert "## 最终方案" in example_text
    assert "## 结果复盘" in example_text


@pytest.mark.asyncio
async def test_create_assistant_from_conversation_and_cancel(tmp_path: Path) -> None:
    session = await _open_session(tmp_path)
    try:
        draft_raw = _result_text(
            await session.call_tool(
                "create_engram_assistant",
                {
                    "mode": "from_conversation",
                    "name": "ops-coach",
                    "topic": "上线运维顾问",
                    "conversation": (
                        "我们讨论了发布前检查清单和回滚预案。"
                        "还明确了异常时先止血再定位。"
                    ),
                },
            )
        )
        payload = json.loads(draft_raw)
        draft_json = json.dumps(payload, ensure_ascii=False)

        canceled = _result_text(
            await session.call_tool(
                "finalize_engram_draft",
                {
                    "draft_json": draft_json,
                    "confirm": False,
                },
            )
        )
    finally:
        await _close_session(session)

    knowledge_text = payload["draft"]["knowledge"][0]["content"]
    assert "发布前检查清单" in knowledge_text
    assert "已取消创建" in canceled
    assert not (tmp_path / ".claude" / "engram" / "ops-coach").exists()
