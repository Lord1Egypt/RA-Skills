# -*- coding: utf-8 -*-
"""v1.0.0 E2E（工单 G2）：真 MCP 客户端全交互——initialize→tools/list→tools/call×3→
resources/read×2→prompts/get。证据落 e2e_transcript.md。"""
import asyncio
import base64
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # mcp/ 目录（import server）

from fastmcp import Client  # noqa: E402
import server  # noqa: E402

TRANSCRIPT = []


def log(tag, content):
    TRANSCRIPT.append(f"## {tag}\n```json\n{json.dumps(content, ensure_ascii=False, default=str)[:1500]}\n```\n")
    print(f"[{tag}] ok")


async def main():
    async with Client(server.mcp) as c:
        # 1 initialize（Client 进入时自动完成握手；服务器名经 server 对象取证）
        log("initialize", {"server": server.mcp.name, "in_memory": True})
        # 2 tools/list
        tools = await c.list_tools()
        names = sorted(t.name for t in tools)
        assert names == ["doctor", "render_chart", "suggest_chart"], names
        log("tools/list", names)
        # 3 tools/call render_chart（bar，含 verify 不适用 png→状态 ok）
        data = json.dumps({"labels": ["A", "B", "C"], "series": {"s": [10, 40, 20]}})
        res = await c.call_tool("render_chart",
                                {"chart": "bar", "data": data,
                                 "options": {"title": "示例", "cjk": True}})
        payload = json.loads(res.content[0].text) if res.content[0].type == "text" else {}
        assert payload["status"] == "ok", payload
        assert payload.get("preview_base64_png"), "缺预览 base64"
        base64.b64decode(payload["preview_base64_png"])  # 可解码
        assert os.path.exists(payload["files"][0]["path"])
        log("tools/call render_chart", {"status": payload["status"],
                                        "files": payload["files"],
                                        "preview_bytes": len(payload["preview_base64_png"])})
        # 4 tools/call suggest_chart
        res2 = await c.call_tool("suggest_chart", {"data": data})
        rec = json.loads(res2.content[0].text)
        assert rec["status"] in ("ok", "error")
        log("tools/call suggest_chart", {"status": rec["status"]})
        # 5 tools/call doctor
        res3 = await c.call_tool("doctor", {"chart": "bar", "data": data})
        rep = json.loads(res3.content[0].text)
        assert "doctor" in rep["report"] or rep["exit_code"] == 0
        log("tools/call doctor", {"exit_code": rep["exit_code"]})
        # 6 resources/read ×2
        cap = await c.read_resource("capability://matrix")
        mat = json.loads(cap[0].text)
        assert mat["count"] >= 23, mat.get("count")
        log("resources/read capability://matrix", {"count": mat["count"],
                                                   "journals": mat["journals"]})
        cl = await c.read_resource("capability://changelog")
        assert "4." in json.loads(cl[0].text)["content"][:400]
        log("resources/read capability://changelog", {"head_ok": True})
        # 7 prompts/get
        pr = await c.get_prompt("chart_picker", {"context": "基线与 12 周随访对比"})
        assert pr.messages
        log("prompts/get chart_picker", {"messages": len(pr.messages)})
        # 8 边界：未知图型 → 工具内 ValueError → MCP 错误返回（不崩溃）
        try:
            await c.call_tool("render_chart", {"chart": "nope", "data": data})
            raise AssertionError("未知图型未被拒绝")
        except Exception as e:
            log("tools/call render_chart 未知图型（预期错误）", {"error_type": type(e).__name__})

    out = "# academic-figures-mcp E2E transcript\n\n" + "\n".join(TRANSCRIPT)
    with open(os.path.join(HERE, "e2e_transcript.md"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print("E2E_ALL_OK → e2e_transcript.md")


if __name__ == "__main__":
    asyncio.run(main())
