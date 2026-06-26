import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from mcp.server.fastmcp import FastMCP
except Exception as e:
    raise RuntimeError(
        "未安装 MCP Python SDK，或当前 Python 版本不支持。"
        "请使用 Python 3.10+ 并执行：python3 -m pip install -r requirements.txt"
    ) from e
from src.feishu_api import FeishuClient

mcp = FastMCP("Feishu Doc Reviewer")

def _extract_comment_text(comment: dict) -> str:
    comment_content = comment.get("content", "")
    try:
        if isinstance(comment_content, str):
            content_obj = json.loads(comment_content)
            return content_obj.get("text", "")
        if isinstance(comment_content, dict):
            return comment_content.get("text", "")
    except Exception:
        return str(comment_content)
    return str(comment_content)


def _extract_block_text(block: dict) -> str:
    if block.get("block_type") != 2:
        return ""
    original_text = ""
    text_elements = block.get("text", {}).get("elements", [])
    for elem in text_elements:
        original_text += elem.get("text_run", {}).get("content", "")
    return original_text


@mcp.tool()
async def list_doc_comments(
    document_token: str,
    comment_keyword: str = None,
    include_solved: bool = False,
    include_processed: bool = False,
) -> str:
    feishu = FeishuClient()
    comments_data = feishu.get_comments(document_token)
    if not comments_data or "data" not in comments_data:
        return json.dumps({"ok": False, "error": "failed_to_fetch_comments"}, ensure_ascii=False)

    items = comments_data["data"].get("items", [])
    results = []
    for comment in items:
        if not include_solved and comment.get("solved"):
            continue

        is_processed = False
        if "reply_list" in comment:
            for reply in comment["reply_list"]:
                content = reply.get("content", {}).get("text", "")
                if "[AI-DONE]" in content:
                    is_processed = True
                    break
        if not include_processed and is_processed:
            continue

        target = comment.get("target", {})
        block_id = target.get("block_id")
        if not block_id:
            continue

        comment_text = _extract_comment_text(comment)
        if comment_keyword and comment_keyword not in comment_text:
            continue

        results.append(
            {
                "comment_id": comment.get("comment_id"),
                "block_id": block_id,
                "comment_text": comment_text,
            }
        )

    return json.dumps({"ok": True, "comments": results}, ensure_ascii=False)


@mcp.tool()
async def get_block_text(document_token: str, block_id: str) -> str:
    feishu = FeishuClient()
    block_data = feishu.get_block(document_token, block_id)
    if not block_data or "data" not in block_data:
        return json.dumps({"ok": False, "error": "failed_to_fetch_block"}, ensure_ascii=False)

    block = block_data["data"].get("block", {})
    return json.dumps(
        {
            "ok": True,
            "block_id": block_id,
            "block_type": block.get("block_type"),
            "text": _extract_block_text(block),
        },
        ensure_ascii=False,
    )


@mcp.tool()
async def update_block_text(
    document_token: str,
    block_id: str,
    new_text: str,
    reply_comment_id: str = None,
    reply_prefix: str = None,
    mark_as_done: bool = True,
) -> str:
    """
    更新文档块内容，并可选择回复评论和标记为已完成
    
    Args:
        document_token: 飞书文档 token
        block_id: 块 ID
        new_text: 新文本内容
        reply_comment_id: 要回复的评论 ID（可选）
        reply_prefix: 回复前缀（可选）
        mark_as_done: 是否标记评论为已解决（默认 True）
    """
    feishu = FeishuClient()
    before = None
    before_block_data = feishu.get_block(document_token, block_id)
    if before_block_data and "data" in before_block_data:
        before_block = before_block_data["data"].get("block", {})
        before = _extract_block_text(before_block)

    update_res = feishu.update_block(document_token, block_id, new_text)
    ok = bool(update_res and update_res.get("code") == 0)
    response = {"ok": ok, "block_id": block_id, "before": before, "after": new_text, "update_res": update_res}

    if ok and reply_comment_id:
        reply_lines = []
        if reply_prefix:
            reply_lines.append(reply_prefix)
        reply_lines.append("已根据建议修改。")
        reply_lines.append(f"修改前：{before or ''}")
        reply_lines.append(f"修改后：{new_text}")
        if mark_as_done:
            reply_lines.append("[AI-DONE]")
        reply_text = "\n".join(reply_lines)
        reply_res = feishu.reply_comment(document_token, reply_comment_id, reply_text)
        response["reply_res"] = reply_res
        
        # 标记评论为已解决
        if mark_as_done and reply_res and reply_res.get("code") == 0:
            resolve_res = feishu.resolve_comment(document_token, reply_comment_id)
            response["resolve_res"] = resolve_res
            if resolve_res and resolve_res.get("code") == 0:
                response["comment_solved"] = True

    return json.dumps(response, ensure_ascii=False)


@mcp.tool()
async def export_document_markdown(document_token: str) -> str:
    feishu = FeishuClient()
    res = feishu.export_markdown(document_token)
    if not res:
        return json.dumps({"ok": False, "error": "export_failed"}, ensure_ascii=False)
    return json.dumps({"ok": True, "res": res}, ensure_ascii=False)

@mcp.tool()
async def prepare_document_baseline(document_token: str) -> str:
    feishu = FeishuClient()
    export_res = feishu.export_markdown(document_token)
    if not export_res:
        return json.dumps({"ok": False, "error": "export_failed"}, ensure_ascii=False)

    baseline_schema = {
        "doc_goal": "一句话描述文档目标",
        "target_audience": "目标读者与使用场景",
        "tone": "整体语气/风格规范",
        "terminology": [{"term": "术语", "preferred": "推荐写法", "notes": "说明"}],
        "must_keep": ["不得改动的关键信息/字段/数字口径"],
        "structure": [{"section": "章节标题", "summary": "该章节要点"}],
        "editing_rules": ["后续逐条修改需要遵守的规则"],
    }

    host_prompt = (
        "你将得到一个飞书 docx 文档的 Markdown 导出结果（可能是正文、或下载链接/异步任务信息）。\n"
        "请先通读并输出一份'编辑基线'，用于后续按评论逐条改写时保持全篇一致。\n"
        "要求：\n"
        "1) 输出严格 JSON，字段结构必须匹配 baseline_schema\n"
        "2) 术语/口吻/不可改动约束要明确可执行\n"
        "3) 如果导出结果不是正文而是链接或任务信息，请说明下一步应如何获取正文后再生成基线\n"
    )

    return json.dumps(
        {
            "ok": True,
            "document_token": document_token,
            "baseline_schema": baseline_schema,
            "host_prompt": host_prompt,
            "export_markdown_result": export_res,
        },
        ensure_ascii=False,
    )


@mcp.tool()
async def process_comment(
    document_token: str,
    comment_id: str,
    reply_text: str = None,
    mark_as_done: bool = True,
) -> str:
    """
    处理飞书文档评论：回复评论并标记为已解决
    
    Args:
        document_token: 飞书文档 token
        comment_id: 评论 ID
        reply_text: 回复内容（可选，默认自动生成）
        mark_as_done: 是否标记为已解决（默认 True）
    
    Returns:
        JSON 格式的操作结果
    """
    import requests
    
    feishu = FeishuClient()
    result = {"ok": True, "comment_id": comment_id, "steps": {}}
    
    # 步骤 1: 获取评论详情
    url = f'{feishu.base_url}/drive/v1/files/{document_token}/comments'
    params = {"file_type": "docx"}
    headers = feishu._get_headers()
    
    response = requests.get(url, headers=headers, params=params)
    comments_data = response.json()
    
    if comments_data.get('code') != 0:
        return json.dumps({"ok": False, "error": f"获取评论失败：{comments_data.get('msg')}"}, ensure_ascii=False)
    
    comment = None
    for item in comments_data.get("data", {}).get("items", []):
        if item.get("comment_id") == comment_id:
            comment = item
            break
    
    if not comment:
        return json.dumps({"ok": False, "error": "评论未找到"}, ensure_ascii=False)
    
    result["comment_quote"] = comment.get("quote", "")[:200]
    result["steps"]["get_comment"] = "success"
    
    # 步骤 2: 回复评论
    if not reply_text:
        reply_text = "✅ 已处理。"
    
    reply_url = f'{feishu.base_url}/drive/v1/files/{document_token}/comments/{comment_id}/replies'
    reply_payload = {
        "content": {
            "elements": [
                {
                    "text_run": {
                        "text": reply_text
                    },
                    "type": "text_run"
                }
            ]
        }
    }
    
    reply_response = requests.post(reply_url, headers=headers, json=reply_payload, params=params)
    reply_result = reply_response.json()
    
    if reply_result.get('code') == 0:
        result["steps"]["reply"] = "success"
        result["reply_id"] = reply_result.get("data", {}).get("reply_id")
    else:
        result["steps"]["reply"] = f"failed: {reply_result.get('msg')}"
        result["ok"] = False
    
    # 步骤 3: 标记为已解决
    if mark_as_done and result["steps"]["reply"] == "success":
        resolve_url = f'{feishu.base_url}/drive/v1/files/{document_token}/comments/{comment_id}'
        resolve_payload = {"is_solved": True}
        
        resolve_response = requests.patch(resolve_url, headers=headers, json=resolve_payload, params=params)
        resolve_result = resolve_response.json()
        
        if resolve_result.get('code') == 0:
            result["steps"]["resolve"] = "success"
            result["comment_solved"] = True
        else:
            result["steps"]["resolve"] = f"failed: {resolve_result.get('msg')}"
    
    return json.dumps(result, ensure_ascii=False)


@mcp.tool()
async def add_document_summary(document_token: str, summary_text: str = None) -> str:
    """
    在飞书文档开头添加摘要
    
    Args:
        document_token: 飞书文档 token（从文档链接提取，如 doxcnABC123）
        summary_text: 摘要文本（可选，不提供则自动生成）
    
    Returns:
        JSON 格式的操作结果
    """
    feishu = FeishuClient()
    
    # 如果没有提供摘要，先获取文档内容并自动生成
    if not summary_text:
        # 获取文档第一个块作为标题
        blocks_data = feishu.get_blocks(document_token)
        if not blocks_data or "data" not in blocks_data:
            return json.dumps({"ok": False, "error": "failed_to_fetch_document"}, ensure_ascii=False)
        
        blocks = blocks_data.get("data", {}).get("blocks", [])
        if not blocks:
            return json.dumps({"ok": False, "error": "empty_document"}, ensure_ascii=False)
        
        # 简单分析文档结构生成摘要
        title = blocks[0].get("heading1", {}).get("elements", [{}])[0].get("text_run", {}).get("content", "文档")
        
        # 统计文档中的章节（heading2/heading3）
        sections = []
        for block in blocks[:50]:  # 只看前 50 个块
            if block.get("block_type") in [4, 5]:  # heading2, heading3
                content = ""
                if block.get("heading2"):
                    content = block["heading2"].get("elements", [{}])[0].get("text_run", {}).get("content", "")
                elif block.get("heading3"):
                    content = block["heading3"].get("elements", [{}])[0].get("text_run", {}).get("content", "")
                if content:
                    sections.append(content)
        
        # 生成摘要
        summary_text = f"📋 {title}\n\n本文档包含 {len(sections)} 个主要章节：\n"
        for i, section in enumerate(sections[:10], 1):
            summary_text += f"  {i}. {section}\n"
        summary_text += "\n适用场景：请参考文档详细内容"
    
    # 调用 API 添加摘要
    result = feishu.prepend_summary_to_document(document_token, summary_text)
    return json.dumps(result, ensure_ascii=False)

if __name__ == "__main__":
    # 运行 MCP Server
    mcp.run()
