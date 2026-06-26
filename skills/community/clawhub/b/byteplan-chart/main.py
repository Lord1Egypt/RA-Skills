#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BytePlan AI 图表生成技能
功能：
1. 从配置文件获取 API 凭证
2. 获取公钥并 RSA 加密密码
3. 自动获取 access_token
4. 调用 AI 接口识别 model_code
5. 执行 AI 分析请求
6. 使用 matplotlib 渲染图表为 PNG（纯 Python 方案）

用法：
    uv run python main.py <查询内容>
    
示例：
    uv run python main.py 查看不同性别分数段分布

依赖安装：
    uv pip install requests pycryptodome matplotlib numpy
"""

import os
import sys
import json
import re
import subprocess
import time
import hashlib
import base64
from pathlib import Path
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

# Windows 命令行编码兼容
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 手动加载 .env 文件
script_dir = Path(__file__).parent
env_file = script_dir / ".env"

if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# ==================== 配置区域（从 .env 读取）====================

# API 配置
BASE_URL = os.getenv("BYTEPLAN_BASE_URL", "https://uatapp.byteplan.com")
PUBLIC_KEY_URL = f"{BASE_URL}/base/util/get/publicKey"
LOGIN_URL = f"{BASE_URL}/base/login"
AI_BASE_URL = f"{BASE_URL}/ai/api/ai"

AUTH_USER = os.getenv("BYTEPLAN_AUTH_USER", "PC")
AUTH_PASS = os.getenv("BYTEPLAN_AUTH_PASS", "")

# 登录参数（publicKeyId 会在运行时动态获取）
LOGIN_PAYLOAD_TEMPLATE = {
    "username": os.getenv("BYTEPLAN_USERNAME", ""),
    "password": "",  # RSA 加密后填入
    "grant_type": os.getenv("BYTEPLAN_GRANT_TYPE", "password"),
    "scope": os.getenv("BYTEPLAN_SCOPE", "write"),
    "publicKeyId": "",  # 动态获取
}

# AI 请求通用参数
PAGE_CODE = os.getenv("BYTEPLAN_PAGE_CODE", "AI_REPORT")

def generate_agent_id():
    """生成唯一的 Agent ID（基于时间戳 + 随机数）"""
    import time
    import random
    # 生成 19 位数字 ID：时间戳后 10 位 + 随机 9 位
    timestamp_part = str(int(time.time() * 1000))[-10:]  # 毫秒时间戳后 10 位
    random_part = ''.join([str(random.randint(0, 9)) for _ in range(9)])  # 随机 9 位
    return timestamp_part + random_part

AGENT_ID = os.getenv("BYTEPLAN_AGENT_ID") or generate_agent_id()

# 图表配置
CHART_WIDTH = int(os.getenv("CHART_WIDTH", "800"))
CHART_HEIGHT = int(os.getenv("CHART_HEIGHT", "600"))
CHART_OUTPUT_DIR = script_dir / os.getenv("CHART_OUTPUT_DIR", "charts")

# ==================== 功能函数 ====================

def generate_eagleeye_headers():
    """生成 EagleEye 追踪头"""
    timestamp = int(time.time() * 1000)
    trace_id = f"7a08bd3a{timestamp}"
    session_id = f"6FmUFm9mk788CUq6d8djbsO111ph"
    app_name = "j1lq8luqau@ffc799a9f98ccdb"
    
    # 生成 sign（简化版本，实际可能需要更复杂的算法）
    sign_data = f"{timestamp}{session_id}{app_name}"
    sign = hashlib.md5(sign_data.encode()).hexdigest()
    
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,vi;q=0.6",
        "eagleeye-pappname": app_name,
        "eagleeye-sessionid": session_id,
        "eagleeye-traceid": trace_id,
        "priority": "u=1, i",
        "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sign": sign,
    }

def get_public_key():
    """获取 RSA 公钥"""
    print("🔑 正在获取公钥...")
    
    headers = generate_eagleeye_headers()
    headers["referrer"] = f"{BASE_URL}/"
    
    try:
        response = requests.get(
            PUBLIC_KEY_URL,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            key_id = data.get("id")
            key_content = data.get("key")
            
            if key_id and key_content:
                print(f"✅ 公钥获取成功")
                print(f"   Key ID: {key_id}")
                return key_id, key_content
            else:
                print(f"❌ 响应中未找到公钥信息")
                print(f"完整响应：{json.dumps(data, indent=2, ensure_ascii=False)}")
                return None, None
        else:
            print(f"❌ 请求失败，状态码：{response.status_code}")
            print(f"响应内容：{response.text}")
            return None, None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常：{e}")
        return None, None

def rsa_encrypt_password(password, public_key_pem):
    """使用 RSA 公钥加密密码"""
    print("🔐 正在加密密码...")
    
    try:
        # 导入公钥（处理可能的格式问题）
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5
        
        # 确保公钥格式正确
        key_pem = public_key_pem.strip()
        if not key_pem.startswith("-----BEGIN"):
            key_pem = "-----BEGIN PUBLIC KEY-----\n" + key_pem + "\n-----END PUBLIC KEY-----"
        
        key = RSA.import_key(key_pem)
        cipher = PKCS1_v1_5.new(key)
        
        # 加密密码
        encrypted = cipher.encrypt(password.encode('utf-8'))
        
        # Base64 编码
        encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
        
        print(f"✅ 密码加密成功")
        return encrypted_b64
        
    except Exception as e:
        print(f"❌ 密码加密失败：{e}")
        import traceback
        traceback.print_exc()
        return None

def get_access_token():
    """获取 access_token（先获取公钥，RSA 加密密码，再登录）"""
    import requests
    
    print("🔐 正在获取 access_token...")
    
    # 步骤 1: 获取公钥
    key_id, public_key_pem = get_public_key()
    if not key_id or not public_key_pem:
        print("❌ 无法获取公钥，终止流程")
        return None
    
    # 步骤 2: RSA 加密密码
    raw_password = os.getenv("BYTEPLAN_PASSWORD", "")
    encrypted_password = rsa_encrypt_password(raw_password, public_key_pem)
    if not encrypted_password:
        print("❌ 无法加密密码，终止流程")
        return None
    
    # 步骤 3: 准备登录参数
    login_payload = LOGIN_PAYLOAD_TEMPLATE.copy()
    login_payload["password"] = encrypted_password
    login_payload["publicKeyId"] = key_id
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(
            LOGIN_URL,
            data=login_payload,
            headers=headers,
            auth=(AUTH_USER, AUTH_PASS),
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                print(f"✅ Token 获取成功\n")
                return token
            else:
                print(f"❌ 响应中未找到 access_token")
                print(f"完整响应：{json.dumps(data, indent=2, ensure_ascii=False)}")
                return None
        else:
            print(f"❌ 请求失败，状态码：{response.status_code}")
            print(f"响应内容：{response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常：{e}")
        return None


def get_model_code(token, query):
    """第一步：获取 model_code"""
    import requests
    
    print("📡 步骤 1: 识别模型获取 model_code...")
    
    url = f"{AI_BASE_URL}/identify/model/code"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "x-page-code": PAGE_CODE
    }
    
    payload = {
        "agentId": AGENT_ID,
        "threadId": 1,
        "query": query,
        "systemPrompt": "",
        "args": {}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, stream=True, timeout=60)
        
        if response.status_code != 200:
            print(f"❌ 请求失败，状态码：{response.status_code}")
            print(f"响应内容：{response.text}")
            return None
        
        full_text = ""
        
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data:"):
                    data_str = decoded_line[5:]
                    if data_str.strip():
                        try:
                            data = json.loads(data_str)
                            text = data.get("text", "")
                            if text:
                                full_text += text
                        except json.JSONDecodeError:
                            pass
        
        print(f"📄 识别结果:\n{full_text}\n")
        
        # 提取 model_code
        model_codes = []
        try:
            # 尝试匹配 model_code 字段
            matches = re.findall(r'"model_code"\s*:\s*"([^"]+)"', full_text)
            if matches:
                model_codes = list(set(matches))  # 去重
                print(f"✅ 提取到 model_code: {model_codes}\n")
                return model_codes
            
            # 尝试解析 JSON result
            result_match = re.search(r'"result"\s*:\s*"([^"]+)"', full_text, re.DOTALL)
            if result_match:
                result_str = result_match.group(1).replace('\\n', '').replace('\\t', '').replace('\\"', '"')
                result_json = json.loads(result_str)
                if isinstance(result_json, list):
                    for item in result_json:
                        if "model_code" in item:
                            model_codes.append(item["model_code"])
                print(f"✅ 提取到 model_code: {model_codes}\n")
                return model_codes
                
        except Exception as e:
            print(f"⚠️ 解析 model_code 时出错：{e}")
        
        print("❌ 未提取到 model_code\n")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常：{e}")
        return None


def run_analysis(token, model_codes, query):
    """第二步：执行 AI 分析请求"""
    import requests
    
    print(f"📡 步骤 2: 执行 AI 分析 (query: {query.strip()})...")
    print(f"   使用 modelCodes: {model_codes}")
    print("=" * 60)
    
    url = f"{AI_BASE_URL}/analysis/agent"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "x-page-code": PAGE_CODE
    }
    
    payload = {
        "agentId": AGENT_ID,
        "query": query,
        "systemPrompt": "",
        "args": {
            "modelCodes": model_codes,
            "chartConfig": [],
            "userPrompt": [],
            "excelData": []
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, stream=True, timeout=120)
        
        if response.status_code != 200:
            print(f"\n❌ 请求失败，状态码：{response.status_code}")
            print(f"响应内容：{response.text}")
            return None
        
        # 流式输出并提取 AntVGenerateNode
        antv_full_text = ""
        in_antv_json = False
        
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                print(decoded_line)
                
                # 检测是否进入 AntVGenerateNode JSON 数据
                if "AntVGenerateNode" in decoded_line:
                    if "textType\":\"JSON" in decoded_line:
                        in_antv_json = True
                        antv_full_text = ""  # 重置
                    elif "textType\":\"TEXT" in decoded_line:
                        in_antv_json = False
                
                # 累积 AntVGenerateNode 的 JSON 数据
                if in_antv_json and decoded_line.startswith("data:"):
                    try:
                        data_str = decoded_line[5:]
                        data = json.loads(data_str)
                        text = data.get("text", "")
                        if text:
                            antv_full_text += text
                    except json.JSONDecodeError:
                        pass
        
        # 解析并打印 AntVGenerateNode 结果
        antv_json = None
        if antv_full_text:
            try:
                # 先解析 DataOutPutNode 的 JSON（处理多行 JSON）
                lines = antv_full_text.strip().split('\n')
                data_output = None
                for line in lines:
                    try:
                        data_output = json.loads(line)
                        break
                    except:
                        continue
                
                if not data_output:
                    data_output = json.loads(antv_full_text.split('\n')[0])
                
                # 提取 AntVGenerateNode 字段
                antv_escaped = data_output.get("AntVGenerateNode", "")
                if antv_escaped:
                    # 处理转义字符
                    antv_unescaped = antv_escaped.replace('\\"', '"').replace('\\\\', '\\').replace('\\n', '').replace('\\t', '')
                    antv_json = json.loads(antv_unescaped)
                    
                    print("\n" + "=" * 60)
                    print("📊 AntVGenerateNode 结果:")
                    print("=" * 60)
                    print(f"图表类型：{antv_json.get('type', 'N/A')}")
                    print(f"图表标题：{antv_json.get('config', {}).get('title', 'N/A')}")
                    print(f"X 轴字段：{antv_json.get('config', {}).get('xField', 'N/A')}")
                    print(f"Y 轴字段：{antv_json.get('config', {}).get('yField', 'N/A')}")
                    print(f"分组字段：{antv_json.get('config', {}).get('groupField', 'N/A')}")
                    print("\n数据:")
                    for item in antv_json.get('data', []):
                        print(f"  {item}")
                    print("=" * 60)
                    
            except Exception as e:
                print(f"\n⚠️ 解析 AntV 数据失败：{e}")
                # 尝试直接查找 AntVGenerateNode
                import re
                match = re.search(r'"AntVGenerateNode":"([^"]+)"', antv_full_text.replace('\n', ''))
                if match:
                    try:
                        antv_escaped = match.group(1)
                        antv_unescaped = antv_escaped.replace('\\"', '"').replace('\\\\', '\\').replace('\\n', '').replace('\\t', '')
                        antv_json = json.loads(antv_unescaped)
                        print("\n✅ 从原始数据中提取到 AntV 配置")
                    except Exception as e2:
                        print(f"⚠️ 提取失败：{e2}")
        
        print("=" * 60)
        print("\n✅ AI 分析完成\n")
        
        return antv_json
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求异常：{e}")
        return None


def render_chart(antv_json):
    """第三步：使用 matplotlib 渲染图表（纯 Python 方案）"""
    print("🎨 步骤 3: 渲染图表 (matplotlib)...")
    
    # 创建输出目录
    CHART_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成输出文件路径
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = CHART_OUTPUT_DIR / f"antv_chart_{timestamp}.png"
    
    # 调用 Python 渲染脚本
    render_script = script_dir / "render_chart.py"
    antv_json_str = json.dumps(antv_json, ensure_ascii=False)
    
    print(f"   使用脚本：{render_script}")
    
    try:
        # 使用 uv run python 运行渲染脚本（确保在虚拟环境中）
        result = subprocess.run(
            ['uv', 'run', 'python', str(render_script), antv_json_str, str(output_path)],
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8',
            cwd=str(script_dir)
        )
        
        if result.returncode == 0:
            print(f"   {result.stdout.strip()}")
            print(f"\n🎨 图表已生成：{output_path}")
            print("📌 使用图片查看器打开该文件\n")
            return str(output_path)
        else:
            print(f"   ⚠️ 渲染错误：{result.stderr.strip()}")
            return None
            
    except FileNotFoundError:
        print("   ⚠️ 未找到 uv 或 Python")
        return None
    except subprocess.TimeoutExpired:
        print("   ⚠️ 渲染超时")
        return None
    except Exception as e:
        print(f"   ⚠️ 渲染失败：{e}")
        return None


def main():
    """主流程"""
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("用法：uv run python main.py <查询内容>")
        print("示例：uv run python main.py 查看不同性别分数段分布")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    
    print("=" * 60)
    print("🤖 BytePlan AI 图表生成")
    print("=" * 60)
    print(f"📝 查询：{query.strip()}")
    print("=" * 60)
    print()
    
    # 步骤 1: 获取 token
    token = get_access_token()
    if not token:
        print("❌ 无法获取 token，终止流程")
        return
    
    # 步骤 2: 获取 model_code
    model_codes = get_model_code(token, query)
    if not model_codes:
        print("❌ 无法获取 model_code，终止流程")
        return
    
    # 步骤 3: 执行分析
    antv_json = run_analysis(token, model_codes, query)
    if not antv_json:
        print("❌ 无法获取图表数据，终止流程")
        return
    
    # 步骤 4: 渲染图表
    chart_path = render_chart(antv_json)
    if not chart_path:
        print("❌ 图表渲染失败")
        return
    
    print("🎉 全部流程完成！")
    print(f"📊 图表文件：{chart_path}")


if __name__ == "__main__":
    main()
