#!/usr/bin/env python3
"""
deep-digest: 深度内容萃取 V1.1
Extracts cognitive patterns, key insights, and action signals from text.
V1.1: 增加 Evaluator veto 机制（Generator/Checker 分离）
"""

import json
import sys
import os


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path) as f:
        return json.load(f)


def build_generator_prompt(text: str, mode: str = "full", previous_output: str = None, veto_feedback: str = None) -> str:
    """构建 Generator prompt，支持 veto 后的重试"""
    structure = {
        "full": "全部三区",
        "facts-only": "仅事实摘要",
        "patterns-only": "仅模式发现",
        "signals-only": "仅信号与行动",
    }

    retry_context = ""
    if previous_output and veto_feedback:
        retry_context = f"""

---

## ⚠️ 上次输出被 veto，需要改进

**上次输出：**
```
{previous_output}
```

**评估器反馈：**
{veto_feedback}

**要求：针对反馈改进，不要重复相同的错误。**

"""

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
- 可操作的行动项（必须是可执行的，不能是"思考一下"这类模糊表述）
- 值得深挖的方向
- 风险或警告信号
- 优先级排序
{retry_context}
---

原始文本：
```
{text}
```
"""
    return prompt


def build_evaluator_prompt(generator_output: str, original_text: str, mode: str = "full") -> str:
    """构建 Evaluator prompt — 独立评估器，挑剔地检查输出质量"""

    prompt = f"""你是一个独立的评估器（Evaluator），你的职责是挑剔地检查 Generator 的输出质量。

## 评估标准

### 1. 模式发现质量（权重 40%）
- 是否识别出真正的模式（不是简单的总结）？
- 是否发现了隐性假设或认知转变？
- 是否识别了矛盾或张力点？
- **扣分项**：模式发现空洞（如"文章讨论了多个话题"）、没有洞察、只是复述内容

### 2. 行动项可操作性（权重 30%）
- 每个行动项是否可执行（有明确的主体、动作、对象）？
- 是否避免了模糊表述（"思考一下"、"深入了解"等）？
- **扣分项**：行动项是"想法"而非"行动"

### 3. 认知转变成立性（权重 20%）
- 声称的"认知转变"是否真的改变了世界观？
- 是否有原文证据支持？
- **扣分项**：认知转变只是"学到了新知识"而非世界观重塑

### 4. 与原文关联性（权重 10%）
- 分析是否忠实于原文？
- 是否有过度解读或幻觉？

---

## Generator 输出

```
{generator_output}
```

---

## 原始文本（用于验证）

```
{original_text[:2000]}{"..." if len(original_text) > 2000 else ""}
```

---

## 输出格式

请输出 JSON：

```json
{{
  "overall_score": 0.0-1.0,
  "pass": true/false,
  "scores": {{
    "pattern_quality": 0.0-1.0,
    "action_operability": 0.0-1.0,
    "cognitive_validity": 0.0-1.0,
    "text_relevance": 0.0-1.0
  }},
  "issues": [
    "具体问题1",
    "具体问题2"
  ],
  "improvement_suggestions": "给 Generator 的改进建议（如果 pass=false）"
}}
```

**判断标准：overall_score >= 0.6 且 pass=true 才通过**
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

    # Load config
    config = load_config()
    inputs = config.get("inputs", {})

    # Determine parameters
    mode = inputs.get("mode", "full")
    enable_veto = inputs.get("enable_veto", True)
    veto_threshold = inputs.get("veto_threshold", 0.6)
    max_retries = inputs.get("max_retries", 2)

    # Build generator prompt
    prompt = build_generator_prompt(text.strip(), mode)

    # Output the processing plan
    output = {
        "version": "1.1.0",
        "mode": mode,
        "input_length": len(text.strip()),
        "sections": ["facts", "patterns", "signals"] if mode == "full" else [mode.replace("-only", "")],
        "veto_enabled": enable_veto,
        "workflow": []
    }

    if enable_veto:
        output["workflow"] = [
            {
                "step": 1,
                "role": "generator",
                "prompt": prompt,
                "description": "生成三区分析"
            },
            {
                "step": 2,
                "role": "evaluator",
                "prompt_template": "build_evaluator_prompt(generator_output, original_text, mode)",
                "description": "独立评估器检查输出质量",
                "threshold": veto_threshold
            },
            {
                "step": 3,
                "role": "decision",
                "logic": f"if evaluator.pass and evaluator.score >= {veto_threshold}: accept; else: retry (max {max_retries} times)",
                "description": "veto 决策"
            }
        ]
        output["veto_config"] = {
            "threshold": veto_threshold,
            "max_retries": max_retries,
            "reference": "Spotify LLM-as-judge veto 25% 实测数据"
        }
    else:
        output["workflow"] = [
            {
                "step": 1,
                "role": "generator",
                "prompt": prompt,
                "description": "生成三区分析（无 veto 检查）"
            }
        ]

    output["note"] = "V1.1: Generator/Evaluator 分离架构。veto 机制参考 Spotify LLM-as-judge 实测数据。"

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    sys.exit(main())