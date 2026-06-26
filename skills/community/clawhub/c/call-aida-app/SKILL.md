name: aida-llm-invoke
description: >
  调用 AI 搭（aida）chat-messages 接口。当用户说「调用 aida」「aida LLM」「生成变更报告」「AI 搭」且提供 appid、query、inputs 时使用。
  Use when: 调用 aida、AI 搭、生成变更报告、aida LLM 分析。
  NOT for: OpenAI、Claude 等公网 LLM。
metadata:
  openclaw:
    emoji: "🤖"
---

# Aida LLM Invoke

## When to Use

- 用户说「调用 aida」「用 aida 生成报告」「AI 搭分析」等
- 用户提供了 appid、query、inputs 三个参数
- 需要调用 aida.vip.sankuai.com 的 chat-messages 接口

## Instructions

1. 使用 **exec** 或 **bash** 工具运行本技能的 `main.py`：
   ```
   python3 main.py --appid <用户提供的appid> --query "<用户提供的query>" --inputs '<用户提供的inputs的JSON字符串>'
   ```
2. 工作目录必须为技能目录（含 main.py 的文件夹），例如：
   - `~/.openclaw/skills/aida-llm-invoke/`（推荐放 managed 目录）
   - 或 `~/.openclaw/workspace/skills/aida-llm-invoke/`
3. 若 inputs 含特殊字符，可改用 stdin：
   ```
   echo '{"appid":"xxx","query":"xxx","inputs":{...}}' | python3 main.py
   ```
4. 解析输出 JSON 中的 `data` 或 `raw_answer` 返回给用户

## Safety Rules

- appid 必须由用户提供，不可硬编码
- 仅用于 aida 内部服务

## Common Patterns

```bash
# 示例：生成变更报告
python3 main.py --appid app-xxx --query "生成变更报告" --inputs '{"tree":"{}","mis":"user01","triggerType":"manual"}'
```
