# Auto-Memory-Distiller

## 简介 (Introduction)
这是一个在后台静默运行的 OpenClaw 长期记忆自动提炼技能 (Skill)。
它负责将无序的超长对话流水账 (JSONL 记录)，增量转化为结构化、按主题分类、可溯源的长期知识库 (Markdown 记忆卡片)。

## 特性 (Features)
1. **增量游标 (Incremental)**：通过 `state.json` 记录每个 Session 的已读行数，每次只处理新增对话，绝不重复消耗 Token。
2. **主题聚合 (Topic Merge)**：自动读取已有的主题目录，将新知识合并入旧主题，防止知识碎片化。
3. **安全过滤 (Redaction)**：利用大模型清洗真实的 API Key 和无关痛痒的报错日志。
4. **溯源指针 (Pointers)**：生成的知识卡片永远带上原始对话的物理文件路径和行号。

## 依赖配置 (Prerequisites)
脚本默认使用 Gemini API，依赖以下 Python 库：
```bash
pip install google-genai python-dotenv
```
请在系统的环境变量，或者 `~/.openclaw/workspace/.env` 中配置你的密钥：
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## 使用方法 (Usage)
无需人工干预。建议把该脚本绑定到系统的 crontab 或者通过 OpenClaw 的 heartbeat 在闲暇时自动触发：

```bash
# 手动运行
python ~/.openclaw/workspace/skills/auto-distiller/distiller.py
```

## 存储目录 (Directory Structure)
- `distiller.py`: 核心脚本。
- `state.json`: 游标记录文件（自动生成）。
- 输出的记忆目录: `~/.openclaw/workspace/memory/topics/*.md`
