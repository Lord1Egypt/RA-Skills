#!/usr/bin/env python3
"""
修复 process_comment 工具 - 确保评论处理完整
"""
import sys
sys.path.insert(0, '.')
from src.feishu_api import FeishuClient
import json
import requests

def process_comment_fixed(document_token, comment_id, reply_text=None, mark_as_done=True):
    """
    处理评论的完整流程
    
    Args:
        document_token: 文档 token
        comment_id: 评论 ID
        reply_text: 回复内容
        mark_as_done: 是否标记为已解决
    
    Returns:
        dict: 处理结果
    """
    api = FeishuClient()
    result = {
        "ok": True,
        "comment_id": comment_id,
        "steps": {}
    }
    
    # 步骤 1: 获取评论详情
    print(f"步骤 1: 获取评论 {comment_id}")
    url = f'{api.base_url}/drive/v1/files/{document_token}/comments'
    params = {"file_type": "docx"}
    headers = api._get_headers()
    
    response = requests.get(url, headers=headers, params=params)
    comments_data = response.json()
    
    if comments_data.get('code') != 0:
        result["ok"] = False
        result["error"] = f"获取评论失败：{comments_data.get('msg')}"
        return result
    
    # 找到目标评论
    comment = None
    for item in comments_data.get("data", {}).get("items", []):
        if item.get("comment_id") == comment_id:
            comment = item
            break
    
    if not comment:
        result["ok"] = False
        result["error"] = "评论未找到"
        return result
    
    result["comment_quote"] = comment.get("quote", "")[:100]
    result["steps"]["get_comment"] = "success"
    
    # 步骤 2: 回复评论
    print(f"步骤 2: 回复评论")
    if not reply_text:
        reply_text = "✅ 已处理。"
    
    reply_url = f'{api.base_url}/drive/v1/files/{document_token}/comments/{comment_id}/replies'
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
        print(f"✅ 回复成功：{reply_result.get('data', {}).get('reply_id')}")
    else:
        result["steps"]["reply"] = f"failed: {reply_result.get('msg')}"
        print(f"❌ 回复失败：{reply_result.get('msg')}")
    
    # 步骤 3: 标记为已解决
    if mark_as_done and result["steps"]["reply"] == "success":
        print(f"步骤 3: 标记为已解决")
        resolve_url = f'{api.base_url}/drive/v1/files/{document_token}/comments/{comment_id}'
        resolve_payload = {"is_solved": True}
        
        resolve_response = requests.patch(resolve_url, headers=headers, json=resolve_payload, params=params)
        resolve_result = resolve_response.json()
        
        if resolve_result.get('code') == 0:
            result["steps"]["resolve"] = "success"
            result["comment_solved"] = True
            print(f"✅ 评论已标记为已解决")
        else:
            result["steps"]["resolve"] = f"failed: {resolve_result.get('msg')}"
            print(f"❌ 标记失败：{resolve_result.get('msg')}")
    
    return result


# 测试
if __name__ == "__main__":
    doc_token = "doxcnABC123"
    comment_id = "YOUR_COMMENT_ID"
    
    print(f"=== 处理评论 {comment_id} ===\n")
    
    reply_text = """✅ 已处理！

文档摘要已优化并插入到合适位置。"""
    
    result = process_comment_fixed(doc_token, comment_id, reply_text, mark_as_done=True)
    
    print(f"\n=== 处理结果 ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
