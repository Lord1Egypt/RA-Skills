#!/usr/bin/env python3
"""
API Push Frontend Script - 将后端接口定义推送到前端数据接口平台

用法:
    python3 push_api_to_frontend.py --prdId <prdId> --file <api-definitions.json> [options]

示例:
    python3 push_api_to_frontend.py --prdId "PRD-2026-001" --file ./api-definitions.json
    python3 push_api_to_frontend.py --prdId "PRD-2026-001" --swagger ./swagger.json
    python3 push_api_to_frontend.py --prdId "PRD-2026-001" --file ./api.json --verify
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path


# 前端数据接口平台配置
FRONTEND_API_URL = "https://jffe.techgp.cn/md/api/uploadV4"
DEFAULT_TIMEOUT = 30  # 秒
MAX_RETRY_COUNT = 3  # 最大重试次数


def run_command(cmd, capture=True):
    """执行 shell 命令"""
    import subprocess
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def load_api_definitions(file_path):
    """加载接口定义文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 如果是数组，直接返回
        if isinstance(data, list):
            return data
        # 如果是对象，检查是否有 apis 字段
        elif isinstance(data, dict):
            if 'apis' in data:
                return data['apis']
            else:
                return [data]
        else:
            raise ValueError("无效的接口定义格式")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败：{e}")
        return None
    except Exception as e:
        print(f"❌ 读取文件失败：{e}")
        return None


def load_swagger(file_path):
    """加载并解析 Swagger/OpenAPI 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                import yaml
                swagger = yaml.safe_load(f)
            else:
                swagger = json.load(f)
        
        api_definitions = []
        
        # 解析 paths
        paths = swagger.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                if method in ['get', 'post', 'put', 'delete', 'patch']:
                    api_def = {
                        "name": details.get('summary', details.get('operationId', path)),
                        "path": path,
                        "method": method.upper(),
                        "description": details.get('description', ''),
                        "requestParams": [],
                        "responseSchema": {}
                    }
                    
                    # 解析请求参数
                    parameters = details.get('parameters', [])
                    for param in parameters:
                        api_def['requestParams'].append({
                            "name": param.get('name', ''),
                            "type": param.get('schema', {}).get('type', 'String'),
                            "required": param.get('required', False),
                            "description": param.get('description', '')
                        })
                    
                    # 解析响应
                    responses = details.get('responses', {})
                    if '200' in responses:
                        response = responses['200']
                        if 'content' in response:
                            content = response['content']
                            if 'application/json' in content:
                                api_def['responseSchema'] = content['application/json'].get('schema', {})
                    
                    api_definitions.append(api_def)
        
        return api_definitions
    except Exception as e:
        print(f"❌ 解析 Swagger 失败：{e}")
        return None


def validate_api_definitions(api_definitions):
    """验证接口定义"""
    if not api_definitions:
        return False, "接口定义不能为空"
    
    required_fields = ['name', 'path', 'method']
    valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
    
    for i, api in enumerate(api_definitions):
        for field in required_fields:
            if field not in api:
                return False, f"第 {i+1} 个接口缺少必填字段：{field}"
        
        if api['method'].upper() not in valid_methods:
            return False, f"第 {i+1} 个接口的 method 无效：{api['method']}"
    
    return True, "验证通过"


def push_to_frontend(prd_id, api_definitions, timeout=DEFAULT_TIMEOUT):
    """推送到前端数据接口平台"""
    payload = {
        "prdId": prd_id,
        "apis": api_definitions
    }
    
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    
    request = urllib.request.Request(
        FRONTEND_API_URL,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode('utf-8'))
            return True, result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ""
        return False, {
            "error": f"HTTP 错误：{e.code}",
            "message": error_body
        }
    except urllib.error.URLError as e:
        return False, {
            "error": "网络错误",
            "message": str(e.reason)
        }
    except json.JSONDecodeError as e:
        return False, {
            "error": "响应解析失败",
            "message": str(e)
        }
    except Exception as e:
        return False, {
            "error": "未知错误",
            "message": str(e)
        }


def save_push_history(prd_id, api_definitions, result, success):
    """保存推送历史"""
    history_file = Path(__file__).parent.parent / "api-push-frontend" / "references" / "push-history.md"
    history_file.parent.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "✅ 成功" if success else "❌ 失败"
    api_count = len(api_definitions)
    
    # 读取现有历史
    existing_content = ""
    if history_file.exists():
        with open(history_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # 添加新记录
    new_record = f"""
## {timestamp}

- **时间**: {timestamp}
- **prdId**: {prd_id}
- **接口数量**: {api_count}
- **状态**: {status}
- **响应**: ```json
{json.dumps(result, ensure_ascii=False, indent=2)}
```

---
"""
    
    # 写入文件（新记录在前）
    with open(history_file, 'w', encoding='utf-8') as f:
        f.write(f"# API 推送历史记录\n\n{new_record}{existing_content.replace('# API 推送历史记录\\n\\n', '')}")
    
    print(f"📝 推送历史已保存到：{history_file}")


def interactive_setup():
    """交互式设置"""
    print("\n🚀 API 推送到前端平台向导\n")
    
    # 1. 产品需求 ID
    prd_id = input("请输入产品需求 ID（prdId）: ").strip()
    if not prd_id:
        print("❌ 产品需求 ID 不能为空")
        return False
    
    # 2. 接口定义文件
    print("\n请选择接口定义来源:")
    print("  1. JSON 文件")
    print("  2. Swagger/OpenAPI 文件")
    print("  3. 直接输入接口定义（JSON 格式）")
    
    choice = input("选择 [1/2/3]: ").strip()
    
    api_definitions = None
    
    if choice == "1":
        file_path = input("请输入 JSON 文件路径：").strip()
        api_definitions = load_api_definitions(file_path)
    elif choice == "2":
        file_path = input("请输入 Swagger 文件路径：").strip()
        api_definitions = load_swagger(file_path)
    elif choice == "3":
        json_str = input("请输入接口定义 JSON（支持多行，输入 END 结束）:\n")
        lines = [json_str]
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        try:
            api_definitions = json.loads("\n".join(lines))
            if isinstance(api_definitions, dict):
                api_definitions = [api_definitions]
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失败：{e}")
            return False
    else:
        print("❌ 无效选择")
        return False
    
    if not api_definitions:
        print("❌ 无法加载接口定义")
        return False
    
    # 3. 验证
    valid, message = validate_api_definitions(api_definitions)
    if not valid:
        print(f"❌ 验证失败：{message}")
        return False
    
    # 4. 确认
    print(f"\n📋 推送摘要:")
    print(f"  prdId: {prd_id}")
    print(f"  接口数量：{len(api_definitions)}")
    print(f"  目标地址：{FRONTEND_API_URL}")
    
    confirm = input("\n确认推送？(y/n) [默认：y]: ").strip().lower()
    if confirm == "n":
        print("已取消")
        return False
    
    # 5. 执行推送
    print("\n🚀 正在推送...")
    success, result = push_to_frontend(prd_id, api_definitions)
    
    if success:
        print(f"\n✅ 推送成功！")
        print(f"响应：{json.dumps(result, ensure_ascii=False, indent=2)}")
        save_push_history(prd_id, api_definitions, result, True)
    else:
        print(f"\n❌ 推送失败！")
        print(f"错误：{json.dumps(result, ensure_ascii=False, indent=2)}")
        save_push_history(prd_id, api_definitions, result, False)
    
    return success


def main():
    parser = argparse.ArgumentParser(
        description="将后端 API 接口定义推送到前端数据接口平台",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 push_api_to_frontend.py --prdId PRD-2026-001 --file api-definitions.json
  python3 push_api_to_frontend.py --prdId PRD-2026-001 --swagger swagger.json
  python3 push_api_to_frontend.py --prdId PRD-2026-001 --file api.json --verify
        """
    )
    
    parser.add_argument("--prdId", "-p", required=False, help="产品需求 ID")
    parser.add_argument("--file", "-f", help="接口定义 JSON 文件路径")
    parser.add_argument("--swagger", "-s", help="Swagger/OpenAPI 文件路径")
    parser.add_argument("--timeout", "-t", type=int, default=DEFAULT_TIMEOUT, help=f"请求超时时间（秒）[默认：{DEFAULT_TIMEOUT}]")
    parser.add_argument("--verify", "-v", action="store_true", help="推送前验证接口定义")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式模式")
    
    args = parser.parse_args()
    
    # 交互式模式或没有提供必需参数
    if args.interactive or not args.prdId or (not args.file and not args.swagger):
        success = interactive_setup()
        sys.exit(0 if success else 1)
    
    # 命令行模式
    prd_id = args.prdId
    
    # 加载接口定义
    if args.swagger:
        print(f"📄 加载 Swagger 文件：{args.swagger}")
        api_definitions = load_swagger(args.swagger)
    else:
        print(f"📄 加载接口定义文件：{args.file}")
        api_definitions = load_api_definitions(args.file)
    
    if not api_definitions:
        print("❌ 无法加载接口定义")
        sys.exit(1)
    
    # 验证
    if args.verify:
        print("🔍 验证接口定义...")
        valid, message = validate_api_definitions(api_definitions)
        if not valid:
            print(f"❌ 验证失败：{message}")
            sys.exit(1)
        print("✅ 验证通过")
    
    # 推送
    print(f"\n🚀 正在推送到 {FRONTEND_API_URL}...")
    print(f"   prdId: {prd_id}")
    print(f"   接口数量：{len(api_definitions)}")
    
    success, result = push_to_frontend(prd_id, api_definitions, args.timeout)
    
    if success:
        print(f"\n✅ 推送成功！")
        print(f"响应：{json.dumps(result, ensure_ascii=False, indent=2)}")
        save_push_history(prd_id, api_definitions, result, True)
        sys.exit(0)
    else:
        print(f"\n❌ 推送失败！")
        print(f"错误：{json.dumps(result, ensure_ascii=False, indent=2)}")
        save_push_history(prd_id, api_definitions, result, False)
        sys.exit(1)


if __name__ == "__main__":
    main()
