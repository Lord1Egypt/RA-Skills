#!/usr/bin/env python3
"""
Coze 工作流调用脚本 (使用 cozepy 库)

用法:
    python3 run_workflow.py <workflow_id> [input_text]

示例:
    python3 run_workflow.py 7610360135081295918 "姓名: 张三, 邮箱: test@example.com"
"""

import sys
import json
from cozepy import COZE_CN_BASE_URL, Coze, TokenAuth

# 从 tokens.md 读取令牌
def get_auth_token():
    token_file = "/Users/hanjin/.openclaw/workspace-prod/coze/coze-tokens.md"
    try:
        with open(token_file, 'r') as f:
            content = f.read()
            for line in content.split('\n'):
                if 'Bearer' in line and 'sat_' in line:
                    return line.replace('Bearer ', '').strip()
    except Exception as e:
        print(f"Error reading token file: {e}", file=sys.stderr)
        return None
    return None

def run_workflow(workflow_id, input_text=None):
    """调用 Coze 工作流"""
    
    auth_token = get_auth_token()
    if not auth_token:
        print("Error: Could not read auth token", file=sys.stderr)
        return None
    
    try:
        coze = Coze(auth=TokenAuth(token=auth_token), base_url=COZE_CN_BASE_URL)
        
        # 构建参数
        parameters = {"input": input_text} if input_text else {}
        
        # 调用工作流
        run_result = coze.workflows.runs.create(
            workflow_id=workflow_id,
            parameters=parameters
        )
        
        return run_result
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return {"error": str(e)}

def extract_markdown_content(result):
    """从结果中提取 Markdown 内容"""
    if not result:
        return "无返回结果"
    
    # 如果是字典
    if isinstance(result, dict):
        data_str = result.get('data', '')
    else:
        data_str = getattr(result, 'data', '')
    
    # 解析 data_str 中的 JSON
    try:
        data_json = json.loads(data_str)
        markdown_content = data_json.get('data', '').strip()
        return markdown_content if markdown_content else str(result)
    except (json.JSONDecodeError, TypeError):
        return str(data_str) if data_str else str(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    workflow_id = sys.argv[1]
    input_text = sys.argv[2] if len(sys.argv) > 2 else "测试"
    
    print(f"调用工作流 {workflow_id} ...")
    result = run_workflow(workflow_id, input_text)
    
    if result:
        # 尝试提取 Markdown 内容
        content = extract_markdown_content(result)
        print(content)
    else:
        print("调用失败", file=sys.stderr)
        sys.exit(1)