#!/usr/bin/env python3
"""
deep-digest: 深度内容萃取
Extracts cognitive patterns, key insights, and action signals from text.
"""

import json
import sys
import os


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path) as f:
        return json.load(f)


def build_prompt(text: str, mode: str = "full") -> str:
    structure = {
        "full": "全部三区",
        "facts-only": "仅事实摘要",
        "patterns-only": "仅模式发现",
        "signals-only": "仅信号与行动",
    }

    prompt = f"""你将得到一段原始文本。请按照以下三区结构进行分析。

## 分析模式：{structure.get(mode, '全部三区')}

### 📋 事实摘要
如果包含事实层分析，请提取：
- 时间线 / 序列
- 关键人物或角色
- 事件或论点
- 数据或引用（如有）

### 🧠 模式发现（这是核心价值）
如果包含模式层分析，请识别：
- 重复出现的主题
- 隐性假设（作者/发言者默认了什么）
- 认知转变（世界观被敲碎或重塑的瞬间）
- 行为或决策模式
- 矛盾或张力点
- **注意：不是总结内容，是识别模式**

### ⚡ 信号与行动
如果包含信号层分析，请输出：
- 可操作的行动项
- 值得深挖的方向
- 风险或警告信号
- 优先级排序

---

原始文本：
```
{text}
```
"""
    return prompt


def main():
    # Read input
    try:
        # Try stdin first (pipe mode)
        if not sys.stdin.isatty():
            text = sys.stdin.read()
        else:
            # Read from config or args
            config = load_config()
            text = config.get("inputs", {}).get("text", "")
            if not text:
                print(json.dumps({
                    "error": "No input text provided. Pipe text or set 'text' in config.",
                    "usage": "cat file.txt | openclaw skill run deep-digest"
                }))
                return 1
    except Exception as e:
        print(json.dumps({"error": f"Cannot read input: {e}"}))
        return 1

    # Determine mode
    mode = "full"
    try:
        if not sys.stdin.isatty():
            mode = os.environ.get("DEEP_DIGEST_MODE", "full")
        else:
            config = load_config()
            mode = config.get("inputs", {}).get("mode", "full")
    except:
        pass

    # Build prompt
    prompt = build_prompt(text.strip(), mode)

    # Output the prompt for the AI model
    # In OpenClaw, the skill's output is passed to the configured AI model
    print(json.dumps({
        "prompt": prompt,
        "mode": mode,
        "input_length": len(text.strip()),
        "sections": ["facts", "patterns", "signals"] if mode == "full" else [mode.replace("-only", "")],
        "note": "This prompt is designed to be consumed by the OpenClaw AI model for processing."
    }))


if __name__ == "__main__":
    sys.exit(main())
