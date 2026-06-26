import os
import json
import glob
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

# ================= Configuration =================
# Dynamic paths relative to the user's home directory
HOME_DIR = Path(os.path.expanduser("~"))
WORKSPACE_DIR = HOME_DIR / ".openclaw" / "workspace"
SESSIONS_DIR = HOME_DIR / ".openclaw" / "agents" / "main" / "sessions"
SKILL_DIR = WORKSPACE_DIR / "skills" / "auto-distiller"
TOPICS_DIR = WORKSPACE_DIR / "memory" / "topics"
STATE_FILE = SKILL_DIR / "state.json"

# Attempt to load a generic .env file from the workspace if it exists
load_dotenv(WORKSPACE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

# Model for distillation (Using a fast/cheap model to save costs, adjust as needed)
DISTILL_MODEL = "gemini-2.5-flash"
CHUNK_SIZE_MESSAGES = 200  # Process up to 200 messages at a time

# ================= Initialize =================
if not API_KEY:
    print("❌ 错误: 找不到 GEMINI_API_KEY 环境变量，请确保 ~/.openclaw/workspace/gemini/.env 文件存在并包含密钥。")
    exit(1)

client = genai.Client(api_key=API_KEY)
TOPICS_DIR.mkdir(parents=True, exist_ok=True)
SKILL_DIR.mkdir(parents=True, exist_ok=True)

# ================= Functions =================
def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

def get_existing_topics():
    topics = []
    for f in TOPICS_DIR.glob("*.md"):
        topics.append(f.stem)
    return topics

def distill_chunk(session_id, start_line, end_line, conversation_text, existing_topics):
    print(f"🧠 正在蒸馏 {session_id} (行 {start_line}-{end_line})...")
    
    prompt = f"""
你是一个高级知识提取引擎。你的任务是将冗长的聊天记录（流水账）提炼成高密度的、结构化的长期记忆卡片。

【现有主题列表】
{', '.join(existing_topics) if existing_topics else '无（你可以创建新主题）'}

【规则】
1. 忽略闲聊、调试错误输出(Tracebacks)、纯情绪发泄的内容。
2. 提取出事实、重要决定、有价值的代码片段、配置经验等核心知识。
3. 必须过滤并打码所有真实的 API Keys、密码等敏感信息。
4. 尽量将提取的知识归类到【现有主题列表】中。只有当现有主题完全不匹配时，才创建新的简短且高度概括的主题名称（英文或拼音/中文皆可，作为文件名，不要包含特殊符号）。
5. 必须返回一个严格的 JSON 数组格式（不要包含 markdown 代码块包裹，纯文本 JSON）。

【返回格式示例】
[
  {{
    "topic_filename": "feishu_api",
    "topic_title": "飞书 API 开发经验",
    "keywords": ["飞书", "权限", "报错", "subagent"],
    "facts": [
      "主会话无法直接调用 feishu_perm，必须通过 mode='run' 唤醒子代理执行。",
      "上下文超过 128k 会导致 API temporarily overloaded。"
    ],
    "snippets": ["// 核心代码片段示例..."]
  }}
]

【待处理的对话内容 (来源文件: {session_id}.jsonl, 行号: {start_line} - {end_line})】
{conversation_text}
"""
    try:
        response = client.models.generate_content(
            model=DISTILL_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"❌ 蒸馏失败: {e}")
        return []

def append_to_topic_file(topic_data, session_id, start_line, end_line):
    filename = topic_data.get("topic_filename", "unclassified").replace(" ", "_").replace("/", "-")
    filepath = TOPICS_DIR / f"{filename}.md"
    
    is_new = not filepath.exists()
    
    with open(filepath, 'a', encoding='utf-8') as f:
        if is_new:
            f.write(f"# 🏷️ 主题：{topic_data.get('topic_title', filename)}\n\n")
        
        f.write(f"## 🕒 更新日志 (来自 {session_id})\n")
        f.write(f"- **关键词**：`[{', '.join(topic_data.get('keywords', []))}]`\n")
        f.write(f"- **🔗 溯源指针**: `~/.openclaw/agents/main/sessions/{session_id}.jsonl` (Lines: {start_line} - {end_line})\n\n")
        
        facts = topic_data.get("facts", [])
        if facts:
            f.write("### 💡 核心事实/决定\n")
            for fact in facts:
                f.write(f"- {fact}\n")
            f.write("\n")
            
        snippets = topic_data.get("snippets", [])
        if snippets:
            f.write("### 💻 关键片段\n")
            for snippet in snippets:
                f.write("```\n")
                f.write(f"{snippet}\n")
                f.write("```\n")
            f.write("\n")
        
        f.write("---\n\n")
    print(f"✅ 已写入/更新记忆主题: {filename}.md")

# ================= Main Pipeline =================
def run():
    print("🚀 Auto-Memory-Distiller 启动...")
    state = load_state()
    session_files = list(SESSIONS_DIR.glob("*.jsonl"))
    
    for session_file in session_files:
        session_id = session_file.stem
        # 跳过空文件或非对话的内部锁文件
        if not session_file.is_file() or session_file.stat().st_size == 0:
            continue
            
        last_read_line = state.get(session_id, 0)
        
        # Read new lines
        with open(session_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        total_lines = len(lines)
        if last_read_line >= total_lines:
            continue # 没有新内容
            
        print(f"🔍 发现新内容: {session_id} ({total_lines - last_read_line} 行)")
        
        # 分块处理
        current_line = last_read_line
        while current_line < total_lines:
            chunk_end = min(current_line + CHUNK_SIZE_MESSAGES, total_lines)
            chunk_lines = lines[current_line:chunk_end]
            
            # 解析 JSONL 为纯文本对话
            conversation_text = ""
            for i, line in enumerate(chunk_lines):
                try:
                    data = json.loads(line)
                    role = data.get("message", {}).get("role", "unknown").upper()
                    content_list = data.get("message", {}).get("content", [])
                    text = "".join([c.get("text", "") for c in content_list if c.get("type") == "text"])
                    if text.strip():
                        conversation_text += f"[{current_line + i + 1}] {role}: {text}\n"
                except:
                    continue
            
            if conversation_text.strip():
                existing_topics = get_existing_topics()
                results = distill_chunk(session_id, current_line + 1, chunk_end, conversation_text, existing_topics)
                
                for topic_data in results:
                    append_to_topic_file(topic_data, session_id, current_line + 1, chunk_end)
            
            current_line = chunk_end
            # 更新游标状态并保存，防止中断后重复跑
            state[session_id] = current_line
            save_state(state)

    print("🎉 蒸馏任务完成！")

if __name__ == "__main__":
    run()
