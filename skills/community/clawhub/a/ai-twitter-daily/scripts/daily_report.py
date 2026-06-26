#!/usr/bin/env python3
import requests
import sys
import json
import os

API_URL = os.getenv("GROK_API_URL", "https://api.cheaprouter.club/v1/chat/completions")
API_KEY = os.getenv("GROK_API_KEY")
MODEL = os.getenv("GROK_MODEL", "grok-4.20-beta")

if not API_KEY:
    print("❌ 错误: 请设置环境变量 GROK_API_KEY", file=sys.stderr)
    print("示例: export GROK_API_KEY='your-api-key'", file=sys.stderr)
    sys.exit(1)

USERS = """
@karpathy (Andrej Karpathy - AI工程与教学)
@ylecun (Yann LeCun - Meta Chief AI Scientist)
@AndrewYNg (Andrew Ng - AI教育与落地)
@fchollet (François Chollet - Keras作者、ARC-AGI)
@drfeifei (Fei-Fei Li - 斯坦福AI、计算机视觉)
@geoffreyhinton (Geoffrey Hinton - AI教父)
@demishassabis (Demis Hassabis - DeepMind联合创始人)
@jeffdean (Jeff Dean - Google DeepMind Chief Scientist)
@goodfellow_ian (Ian Goodfellow - GANs发明者)
@soumithchintala (Soumith Chintala - PyTorch核心开发者)
@DrJimFan (Jim Fan - NVIDIA具身智能/机器人)
@_akhaliq (AK - AI论文每日推送)
@rasbt (Sebastian Raschka - 实用ML/DL教程)
@lilianweng (Lilian Weng - OpenAI研究员、安全对齐)
@steipete (Peter Steinberger - OpenAI agents/OpenClaw)
@OpenAI (OpenAI官方)
@AnthropicAI (Anthropic官方)
@claudeai (Claude官方)
@xai (xAI/Grok官方)
@DeepSeek_AI (DeepSeek官方)
@huggingface (Hugging Face官方)
@SchmidhuberAI (Jürgen Schmidhuber - AI先驱)
"""

PROMPT = f"""请帮我查询过去24小时内以下用户的动态。要求总结出：

1. **用户互动关系**：这些用户互动的人（谁回复/转推/提到/互关了谁）
2. **高频提及内容**：AI模型、公司、论文、工具、项目、事件（包括具体名称、链接、版本号）
3. **热点观点**：对AGI时间表、开源vs闭源、安全/对齐、具身智能、多模态、新架构、Agent进展等的观点
4. **整体总结**：当天AI领域最新的发展和讨论热点

用户列表：
{USERS}

请用中文回答，结构清晰，用表格或分点呈现，便于每日跟踪。
"""

def query_grok(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": True
    }
    
    response = requests.post(API_URL, headers=headers, json=payload, timeout=180, stream=True)
    
    if response.status_code != 200:
        print(f"HTTP {response.status_code}: {response.text}", file=sys.stderr)
        response.raise_for_status()
    
    content = ""
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = line[6:]
                if data == '[DONE]':
                    break
                try:
                    chunk = json.loads(data)
                    delta = chunk['choices'][0]['delta']
                    if 'content' in delta:
                        content += delta['content']
                except:
                    pass
    
    return content

if __name__ == "__main__":
    try:
        print("🔍 正在查询AI Twitter日报...")
        result = query_grok(PROMPT)
        print("\n" + "="*60)
        print("📊 AI Twitter 日报")
        print("="*60 + "\n")
        print(result)
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)
