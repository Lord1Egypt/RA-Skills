# -*- coding: utf-8 -*-
"""
做梦脚本 - 调用MiniMax M2.7分析MemPalace记忆碎片，提炼精华到当下文档

运行时间：每天凌晨2:00
使用模型：MiniMax M2.7
API：openai-compat

作者：小麦
日期：2026-04-10
版本：v5 (带通知)
"""
import sys
import os
import json
from datetime import datetime
import traceback
from pathlib import Path
import requests

# 设置UTF-8输出
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

WORKSPACE = 'C:/Users/18625/.openclaw/workspace'

# 加载配置
CONFIG_FILE = os.path.join(WORKSPACE, 'skills/continuous-learning/config/dream_config.json')

def load_config():
    """加载配置文件"""
    default_config = {
        'baseUrl': 'https://api.minimax.chat/v1',
        'apiKey': '',  # 用户通过配置文件设置
        'model': 'MiniMax-M2.7',
        'notification': {
            'enabled': True,
            'channel': 'openclaw-weixin',
            'queue_file': '.notification_queue.json'
        }
    }

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            default_config.update(user_config)
    except:
        pass

    return default_config

MINIMAX_CONFIG = load_config()

# 目标文档
TARGET_DOCS = {
    'SOUL': {
        'path': os.path.join(WORKSPACE, 'SOUL.md'),
        'purpose': '行为准则、个性偏好、沟通风格'
    },
    'AGENTS': {
        'path': os.path.join(WORKSPACE, 'AGENTS.md'),
        'purpose': '工作流程、代理规则、交互模式'
    },
    'MEMORY': {
        'path': os.path.join(WORKSPACE, 'MEMORY.md'),
        'purpose': '用户偏好、项目背景、长期记忆'
    },
    'TOOLS': {
        'path': os.path.join(WORKSPACE, 'TOOLS.md'),
        'purpose': '工具配置、集成注意事项、坑'
    },
    'BOOTSTRAP': {
        'path': os.path.join(WORKSPACE, 'BOOTSTRAP.md'),
        'purpose': '会话启动规则、预检清单'
    }
}

# 分析提示词
ANALYSIS_PROMPT = """## 做梦任务 - 分析MemPalace记忆碎片

我是小麦，需要在每天凌晨2:00将记忆宫殿中的碎片记忆整理到我的当下文档中。

### 我的当下文档结构
{doc_descriptions}

### 记忆碎片
以下是MemPalace中的日记条目({count}条)：
{entries_text}

### 分析要求

你现在需要完成以下任务：

1. **分类判断**：每个碎片应该归纳到哪个文档（SOUL/AGENTS/MEMORY/TOOLS/BOOTSTRAP）？

2. **价值判断**：这个碎片有无价值？请过滤掉：
   - 错误记录、异常堆栈
   - 临时测试、调试信息
   - 无意义的流水账
   - 重复的内容

3. **去重检查**：检查碎片是否与现有内容重复

4. **提炼精简**：将碎片提炼成简洁的条目

### 输出格式（严格JSON，不要有其他内容）

```json
{{
  "summary": "本次分析总结",
  "stats": {{
    "total_entries": 总条目数,
    "processed": 处理数,
    "valuable": 有价值数,
    "duplicates": 重复数,
    "noise": 噪音数
  }},
  "updates": [
    {{
      "doc": "SOUL",
      "reason": "这个碎片之所以应该记录到SOUL是因为...",
      "content": "提炼后的内容..."
    }}
  ]
}}
```

请开始分析，只返回上述JSON格式，不要有任何额外说明。"""

def queue_notification(message):
    """将通知存入队列"""
    try:
        # 从配置获取
        notification_config = MINIMAX_CONFIG.get('notification', {})
        queue_file = notification_config.get('queue_file', '.notification_queue.json')
        to_user = notification_config.get('to', '')  # 从配置设置

        if not to_user:
            # 默认：尝试从之前的配置读取或留空
            to_user = ''

        queue_path = os.path.join(WORKSPACE, queue_file)
        queue_dir = os.path.dirname(queue_path)
        os.makedirs(queue_dir, exist_ok=True)

        notifications = []

        if os.path.exists(queue_path):
            with open(queue_path, 'r', encoding='utf-8') as f:
                notifications = json.load(f)

        notification_item = {
            'message': message,
            'timestamp': datetime.now().isoformat()
        }

        if to_user:
            notification_item['to'] = to_user

        notifications.append(notification_item)

        with open(queue_path, 'w', encoding='utf-8') as f:
            json.dump(notifications, f, ensure_ascii=False, indent=2)

        print(f"[通知] 已加入发送队列")
        return True
    except Exception as e:
        print(f"[通知] 队列写入失败: {e}")
        return False

def read_mempalace_entries():
    """从MemPalace读取所有日记条目"""
    try:
        from chromadb import PersistentClient

        client = PersistentClient(path="C:/Users/18625/.mempalace/palace")
        collection = client.get_or_create_collection("mempalace_drawers")

        results = collection.get(include=["documents", "metadatas"])

        entries = []
        for doc, meta in zip(results['documents'], results['metadatas']):
            if meta.get('type') == 'diary_entry' or 'diary' in str(meta).lower():
                entries.append({
                    'document': doc,
                    'metadata': meta
                })

        return {
            'status': 'success',
            'entries': entries,
            'total': len(entries)
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }

def call_minimax_analysis(entries):
    """调用MiniMax M2.7分析记忆碎片"""
    try:
        # 构造entries文本
        entries_text = []
        for i, entry in enumerate(entries, 1):
            entries_text.append(f"条目{i}: {entry['document']}")
            if entry.get('metadata'):
                entries_text.append(f"  元数据: {json.dumps(entry['metadata'], ensure_ascii=False)}")

        # 构造文档描述
        doc_descriptions = json.dumps(TARGET_DOCS, indent=2, ensure_ascii=False)

        # 构造完整提示词
        user_prompt = ANALYSIS_PROMPT.format(
            doc_descriptions=doc_descriptions,
            count=len(entries),
            entries_text='\n'.join(entries_text)
        )

        # 调用MiniMax API（OpenAI兼容）
        url = f"{MINIMAX_CONFIG['baseUrl']}/chat/completions"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {MINIMAX_CONFIG["apiKey"]}'
        }

        payload = {
            'model': MINIMAX_CONFIG['model'],
            'messages': [
                {
                    'role': 'system',
                    'content': '你是一个专业的记忆分析师，擅长整理和提炼信息，只输出严格的JSON格式。'
                },
                {
                    'role': 'user',
                    'content': user_prompt
                }
            ],
            'temperature': 0.3
        }

        response = requests.post(url, headers=headers, json=payload, timeout=120)

        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']

            # 提取JSON
            import re
            json_match = re.search(r'```json\s*\n({[\s\S]*?})\s*```', content) or re.search(r'({[\s\S]*?})', content)

            if json_match:
                parsed_result = json.loads(json_match.group(1))
                return {
                    'status': 'success',
                    'result': parsed_result
                }
            else:
                return {
                    'status': 'error',
                    'error': '无法从响应中提取JSON',
                    'raw_response': content
                }
        else:
            return {
                'status': 'error',
                'error': f"MiniMax API错误: {response.status_code}",
                'response': response.text
            }

    except requests.exceptions.Timeout:
        return {
            'status': 'error',
            'error': 'API请求超时'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }

def check_duplicate(doc_path, content):
    """检查内容是否已存在于文档中"""
    if not os.path.exists(doc_path):
        return False

    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()

        # 简单关键词检查
        core_words = content.replace('\n', ' ').split()
        for word in core_words:
            if len(word) > 4 and word in existing_content:
                return True

        return False

    except Exception:
        return False

def safe_append(doc_path, reason, content):
    """安全追加内容到文档"""
    try:
        if not os.path.exists(doc_path):
            print(f"[WARNING] 文档不存在，创建: {doc_path}")
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(f"# {os.path.basename(doc_path)}\n\n")

        # 去重检查
        if check_duplicate(doc_path, content):
            print(f"[SKIP] 跳过重复内容: {content[:50]}...")
            return {'status': 'duplicate', 'doc': doc_path}

        # 追加内容
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        new_entry = f"""

## 记忆更新 - {timestamp}

**来源**: 记忆宫殿分析
**推理**: {reason}

{content}

---
"""

        with open(doc_path, 'a', encoding='utf-8') as f:
            f.write(new_entry)

        print(f"[OK] 追加到 {os.path.basename(doc_path)}: {content[:50]}...")
        return {'status': 'success', 'doc': doc_path}

    except Exception as e:
        return {
            'status': 'error',
            'doc': doc_path,
            'error': str(e),
            'traceback': traceback.format_exc()
        }

def apply_updates(updates):
    """应用更新到对应的文档"""
    results = []

    for update in updates:
        doc_name = update.get('doc')
        reason = update.get('reason', '')
        content = update.get('content', '')

        if doc_name not in TARGET_DOCS:
            print(f"[ERROR] 警告: 未知文档 {doc_name}")
            results.append({
                'status': 'error',
                'error': f'未知文档: {doc_name}'
            })
            continue

        doc_path = TARGET_DOCS[doc_name]['path']
        result = safe_append(doc_path, reason, content)
        results.append(result)

    return results

def run_dream_cycle():
    """执行一个做梦周期"""
    start_time = datetime.now()
    print(f"\n{'='*60}")
    print(f"[DREAM] 做梦开始于 {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # 1. 读取MemPalace记忆碎片
    print("[STEP 1] 读取MemPalace记忆碎片...")
    entries_result = read_mempalace_entries()

    if entries_result['status'] == 'error':
        print(f"[ERROR] 错误: {entries_result['error']}")

        # 发送错误通知
        error_msg = f"""❌ 做梦失败

阶段: 读取MemPalace
错误: {entries_result.get('error', '未知错误')}
🕒 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        queue_notification(error_msg)

        return entries_result

    entries = entries_result.get('entries', [])
    print(f"[OK] 读取了 {len(entries)} 条碎片\n")

    if not entries:
        print("[SKIP] 没有记忆碎片，跳过本次做梦")

        # 发送跳过通知
        skip_msg = f"""⏭️ 做梦跳过

原因: 无记忆碎片
🕒 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        queue_notification(skip_msg)

        return {'status': 'skipped', 'reason': 'no_entries'}

    # 2. 调用MiniMax分析
    print("[STEP 2] 调用MiniMax M2.7分析记忆碎片...")
    print(f"[INFO] 等待大模型分析...（可能需要几十秒）\n")
    analysis = call_minimax_analysis(entries)

    if analysis['status'] == 'error':
        print(f"[ERROR] 分析失败: {analysis['error']}")

        # 发送错误通知
        error_msg = f"""❌ 做梦失败

阶段: 分析记忆碎片
错误: {analysis.get('error', '未知错误')}
🕒 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        queue_notification(error_msg)

        return analysis

    result = analysis['result']
    stats = result.get('stats', {})
    updates = result.get('updates', [])

    print(f"[OK] 分析完成")
    print(f"  处理: {stats.get('processed')}/{stats.get('total_entries')}")
    print(f"  有价值: {stats.get('valuable')}")
    print(f"  重复: {stats.get('duplicates')}")
    print(f"  噪音: {stats.get('noise')}\n")

    # 3. 应用更新
    print(f"[STEP 3] 应用更新到文档...")
    print(f"[INFO] 共 {len(updates)} 条更新准备写入\n")

    results = apply_updates(updates)

    success_count = sum(1 for r in results if r.get('status') == 'success')
    duplicate_count = sum(1 for r in results if r.get('status') == 'duplicate')
    error_count = sum(1 for r in results if r.get('status') == 'error')

    print(f"\n[RESULT] 应用结果:")
    print(f"  成功: {success_count}")
    print(f"  跳过（重复）: {duplicate_count}")
    print(f"  失败: {error_count}\n")

    # 4. 汇总
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print(f"\n{'='*60}")
    print(f"[DREAM] 做梦完成于 {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[TIME] 耗时: {duration:.2f}秒")
    print(f"{'='*60}\n")

    # 发送完成通知
    success_msg = f"""🌙 做梦完成！

📊 分析结果:
  • 处理: {stats.get('processed')}/{stats.get('total_entries')} 条
  • 有价值: {stats.get('valuable')} 条
  • 去重: {stats.get('duplicates')} 条
  • 噪音: {stats.get('noise')} 条

📝 文档更新:
  • 成功: {success_count} 条
  • 跳过: {duplicate_count} 条
  • 失败: {error_count} 条

⏱️ 耗时: {duration:.2f}秒
🕒 时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
"""

    queue_notification(success_msg)

    return {
        'status': 'completed',
        'duration': duration,
        'stats': stats,
        'results': results
    }

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Dream Cycle v5 - MiniMax M2.7 with Notifications')
    parser.add_argument('--test', action='store_true', help='Test mode (no analysis)')
    args = parser.parse_args()

    if args.test:
        print("[TEST MODE] 只读取，不调用大模型\n")
        result = read_mempalace_entries()

        if result['status'] == 'success':
            print(f"[OK] 找到 {result['total']} 条碎片")
            if result['entries']:
                print("\n前3条:")
                for i, entry in enumerate(result['entries'][:3], 1):
                    print(f"{i}. {entry['document'][:100]}...")
                    print(f"   Meta: {entry.get('metadata', {})}")
        else:
            print(f"[ERROR] {result.get('error')}")
            if result.get('traceback'):
                print(result['traceback'])
    else:
        result = run_dream_cycle()
        print("\n[SUMMARY] 做梦汇报:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
