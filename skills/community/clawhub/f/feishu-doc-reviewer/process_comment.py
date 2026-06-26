#!/usr/bin/env python3
"""
飞书文档评论处理工具

支持处理文档评论的完整流程：
1. 获取评论详情（包括引用的原文）
2. 根据批注要求删除或修改原文
3. 回复评论说明处理结果
4. 标记评论为已解决

使用方法:
    python process_comment.py <document_token> <comment_id> [action]
    
    action: delete | delete_selected | modify | custom
    - delete: 删除整个段落（清空块）
    - delete_selected: 只删除批注选中的文本（保留块中其他内容）⭐推荐
    - modify: 修改段落内容（需要额外传入新内容）
    - custom: 自定义处理（仅回复评论）
"""
import sys
sys.path.insert(0, '.')
from src.feishu_api import FeishuClient
import json
import argparse
import requests


def get_comment_details(api, document_token, comment_id):
    """获取评论详情"""
    url = f'{api.base_url}/drive/v1/files/{document_token}/comments'
    params = {"file_type": "docx"}
    headers = api._get_headers()
    
    response = requests.get(url, headers=headers, params=params)
    comments_data = response.json()
    
    if comments_data.get('code') != 0:
        return None, f"获取评论失败：{comments_data.get('msg')}"
    
    # 找到目标评论
    for item in comments_data.get("data", {}).get("items", []):
        if item.get("comment_id") == comment_id:
            return item, None
    
    return None, "评论未找到"


def extract_block_id_from_quote(api, document_token, comment):
    """
    从评论的 quote 中提取 block_id
    
    策略：
    1. 首先尝试从评论对象中直接获取 block_id（如果有）
    2. 遍历文档块，匹配 quote 内容
    3. 使用 quote 的前 N 个字符进行模糊匹配
    """
    # 尝试从 comment 对象中获取 block_id（某些 API 版本可能包含）
    if "block_id" in comment:
        return comment["block_id"]
    
    # 获取 quote 内容（批注选中的文本）
    quote = comment.get("quote", "")
    if not quote:
        return None
    
    # 取 quote 的前 100 个字符用于匹配（避免过长）
    quote_prefix = quote[:100].strip()
    
    # 遍历文档块匹配内容
    blocks_data = api.get_blocks(document_token)
    if not blocks_data or "data" not in blocks_data:
        return None
    
    blocks = blocks_data.get("data", {}).get("blocks", [])
    
    # 最佳匹配：完整 quote 前缀在块内容中
    for block in blocks:
        block_type = block.get("block_type")
        content = get_block_content(block)
        
        if quote_prefix in content:
            return block.get("block_id")
    
    # 次佳匹配：quote 的关键词在块内容中
    keywords = quote_prefix.split('\n')[0][:50]  # 取第一行的前 50 个字符
    for block in blocks:
        content = get_block_content(block)
        if keywords.strip() in content:
            return block.get("block_id")
    
    return None


def get_block_content(block):
    """提取块的文本内容"""
    block_type = block.get("block_type")
    content = ""
    
    if block_type == 1:  # heading1
        content = block.get("heading1", {}).get("elements", [{}])[0].get("text_run", {}).get("content", "")
    elif block_type == 2:  # text
        elements = block.get("text", {}).get("elements", [])
        content = "".join(elem.get("text_run", {}).get("content", "") for elem in elements)
    elif block_type == 3:  # heading2
        content = block.get("heading2", {}).get("elements", [{}])[0].get("text_run", {}).get("content", "")
    elif block_type == 4:  # heading3
        content = block.get("heading3", {}).get("elements", [{}])[0].get("text_run", {}).get("content", "")
    
    return content


def process_comment(document_token, comment_id, block_id, action="delete_selected", new_content=None, reply_prefix="[AI-DONE]"):
    """
    处理评论的完整流程
    
    Args:
        document_token: 文档 token
        comment_id: 评论 ID
        block_id: 要处理的块 ID
        action: 处理动作
            - "delete": 删除整个块（清空内容）
            - "delete_selected": 只删除选中的文本（保留块中其他内容）⭐推荐
            - "modify": 修改块内容
            - "custom": 仅回复评论
        new_content: 新内容（当 action="modify" 时使用）
        reply_prefix: 回复前缀，默认 "[AI-DONE]"
    
    Returns:
        dict: 处理结果
    """
    api = FeishuClient()
    result = {
        "ok": True,
        "comment_id": comment_id,
        "block_id": block_id,
        "action": action,
        "steps": {}
    }
    
    # 步骤 1: 获取评论详情
    print(f"步骤 1: 获取评论 {comment_id}")
    comment, error = get_comment_details(api, document_token, comment_id)
    
    if error:
        result["ok"] = False
        result["error"] = error
        return result
    
    result["comment_quote"] = comment.get("quote", "")[:100]
    result["steps"]["get_comment"] = "success"
    
    # 步骤 2: 处理文档块
    print(f"步骤 2: 处理文档块 (action={action})")
    
    if action == "delete":
        # 删除整个块（清空内容）
        print("  → 清空整个块内容")
        update_result = api.delete_block(document_token, block_id)
        if update_result.get("ok"):
            result["steps"]["delete_block"] = "success"
            print(f"  ✅ 块内容已清空")
        else:
            result["steps"]["delete_block"] = f"failed: {update_result.get('error')}"
            print(f"  ❌ 删除失败：{update_result.get('error')}")
            result["ok"] = False
    
    elif action == "delete_selected":
        # 只删除选中的文本（从 quote 中获取）
        text_to_delete = comment.get("quote", "")
        if not text_to_delete:
            result["ok"] = False
            result["error"] = "无法获取批注选中的文本"
            return result
        
        print(f"  → 删除选中文本：{text_to_delete[:50]}...")
        update_result = api.delete_text_from_block(document_token, block_id, text_to_delete)
        if update_result.get("ok"):
            result["steps"]["delete_selected"] = "success"
            result["new_content"] = update_result.get("new_content", "")[:100]
            print(f"  ✅ 选中文本已删除")
        else:
            result["steps"]["delete_selected"] = f"failed: {update_result.get('error')}"
            print(f"  ❌ 删除失败：{update_result.get('error')}")
            result["ok"] = False
    
    elif action == "modify":
        # 修改块内容
        if not new_content:
            result["ok"] = False
            result["error"] = "modify action requires new_content"
            return result
        
        print(f"  → 更新块内容")
        update_result = api.update_block(document_token, block_id, new_content)
        if update_result.get("code") == 0:
            result["steps"]["update_block"] = "success"
            print(f"  ✅ 块内容已更新")
        else:
            result["steps"]["update_block"] = f"failed: {update_result.get('msg')}"
            print(f"  ❌ 更新失败：{update_result.get('msg')}")
            result["ok"] = False
    
    # 步骤 3: 回复评论
    print(f"步骤 3: 回复评论")
    if action == "delete":
        reply_text = f"{reply_prefix} 已删除整个段落。"
    elif action == "delete_selected":
        reply_text = f"{reply_prefix} 已按批注要求删除选中内容。"
    elif action == "modify":
        reply_text = f"{reply_prefix} 已按批注要求修改内容。"
    else:
        reply_text = f"{reply_prefix} 已处理。"
    
    reply_result = api.reply_comment(document_token, comment_id, reply_text)
    
    if reply_result.get("code") == 0:
        result["steps"]["reply"] = "success"
        result["reply_id"] = reply_result.get("data", {}).get("reply_id")
        print(f"  ✅ 回复成功：{result['reply_id']}")
    else:
        result["steps"]["reply"] = f"failed: {reply_result.get('msg')}"
        print(f"  ❌ 回复失败：{reply_result.get('msg')}")
        result["ok"] = False
    
    # 步骤 4: 标记为已解决
    if result["ok"]:
        print(f"步骤 4: 标记评论为已解决")
        resolve_result = api.resolve_comment(document_token, comment_id)
        
        if resolve_result and resolve_result.get("code") == 0:
            result["steps"]["resolve"] = "success"
            result["comment_solved"] = True
            print(f"  ✅ 评论已标记为已解决")
        else:
            result["steps"]["resolve"] = f"failed: {resolve_result.get('msg') if resolve_result else 'unknown'}"
            print(f"  ❌ 标记失败：{resolve_result.get('msg') if resolve_result else 'unknown error'}")
            # 标记失败不影响整体结果
    
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="飞书文档评论处理工具")
    parser.add_argument("document_token", help="文档 token")
    parser.add_argument("comment_id", help="评论 ID")
    parser.add_argument("--action", choices=["delete", "delete_selected", "modify", "custom"], default="delete_selected",
                        help="处理动作：delete=删除整个段落，delete_selected=只删除选中内容⭐推荐，modify=修改内容，custom=仅回复")
    parser.add_argument("--new-content", help="新内容（当 action=modify 时使用）")
    parser.add_argument("--block-id", help="块 ID（可选，不传则自动从评论中识别）")
    parser.add_argument("--reply-prefix", default="[AI-DONE]", help="回复前缀")
    
    args = parser.parse_args()
    
    print(f"=== 处理评论 {args.comment_id} ===\n")
    print(f"文档：{args.document_token}")
    print(f"动作：{args.action}")
    print()
    
    api = FeishuClient()
    
    # 获取评论详情
    comment, error = get_comment_details(api, args.document_token, args.comment_id)
    if error:
        print(f"❌ {error}")
        sys.exit(1)
    
    print(f"批注内容：{comment.get('quote', '')[:100]}...")
    print(f"批注要求：{comment.get('reply_list', {}).get('replies', [{}])[0].get('content', {}).get('elements', [{}])[0].get('text_run', {}).get('text', '未知')}")
    
    # 获取或识别 block_id
    block_id = args.block_id
    if not block_id:
        print("\n自动识别块 ID...")
        block_id = extract_block_id_from_quote(api, args.document_token, comment)
        
        if not block_id:
            print("❌ 无法识别块 ID，请手动指定 --block-id")
            sys.exit(1)
        
        print(f"识别到块 ID: {block_id}")
    
    # 处理评论
    result = process_comment(
        args.document_token,
        args.comment_id,
        block_id,
        action=args.action,
        new_content=args.new_content,
        reply_prefix=args.reply_prefix
    )
    
    print(f"\n=== 处理结果 ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result["ok"]:
        print("\n✅ 评论处理完成！")
        sys.exit(0)
    else:
        print(f"\n❌ 处理失败：{result.get('error', 'unknown')}")
        sys.exit(1)
