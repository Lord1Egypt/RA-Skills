---
version: "1.0.1"
name: dandan-humanize-text
description: AI 生成文本人性化改写工具。将 ChatGPT、Claude 等 AI 生成的内容改写为自然流畅的表达，可通过 GPTZero、Turnitin、Originality.ai 等工具检测。适用于需要人感、避免 AI 检测、或润色 AI 草稿的场景。跨平台支持（macOS/Linux/Windows）。
metadata: {"openclaw": {"emoji": "✍️"}}
---


# Humanize AI Text ✍️

将 AI 生成文本改写为自然、不可检测的人文表达。

## 触发条件

- AI 生成的文字需要更自然
- 希望绕过 AI 内容检测（GPTZero、Turnitin 等）
- 需要润色 AI 草稿
- 用户说"改写得更自然"、"去 AI 味"、"人性化"

## 核心改写原则

### 1. 加入人类写作特征
- 轻微不完美（偶有小重复、括号补充）
- 具体例子和个人经历
- 情绪波动（兴奋→平静→反思）
- 非正式表达和口语化

### 2. 移除 AI 典型模式
- 删除绝对化表述（"必须"、"毫无疑问"）
- 减少过度礼貌（删除"当然"、"当然可以"）
- 去掉过度总结的开头
- 删除机械的"首先...其次...最后"

### 3. 调整句式结构
- 长句拆短
- 减少"并且"、"因此"等连接词
- 用主动语态替代被动语态

## 跨平台用法

### macOS / Linux
```bash
# 调用 Python 脚本改写
python3 /path/to/transform.py "AI 文本内容"

# 检测是否像 AI（需要网络）
curl -s "https://api.gptzero.me/v1/check" \
  -H "Content-Type: application/json" \
  -d '{"text": "待检测文本"}'

# 或调用 detect.py（本地检测）
python3 scripts/detect.py "待检测文本"
```

### Windows (PowerShell)
```powershell
# 调用 Python 脚本改写
python scripts\transform.py "AI 文本内容"

# 检测
$body = @{"text" = "待检测文本"} | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.gptzero.me/v1/check" -Method POST -Body $body -ContentType "application/json"
```

## 改写模式库（来自 patterns.json）

### 模式1：断句法
```
AI: "首先，我们需要明确目标。其次，制定计划。最后，执行实施。"
改写: "目标是什么？得先想清楚。然后计划怎么走。到这一步再动手。"
```

### 模式2：口语化
```
AI: "因此，我们得出结论：沟通是团队协作的关键因素。"
改写: "说白了，团队合不来就是沟通没到位。"
```

### 模式3：增补细节
```
AI: "这个工具有很多优点。"
改写: "用了一阵子，确实顺手——最明显的感觉是快，平时要手动搞半小时的事，它五分钟搞定。"
```

### 模式4：情绪加入
```
AI: "实验结果显示该假设成立。"
改写: "跑完数据，发现还真蒙对了！当然也有几个意外值，回头再细查。"
```

## 使用决策树

```
1. 用户提供 AI 文本？
   → 进入改写流程

2. 目标是什么？
   → 通过 AI 检测 → 应用强改写模式
   → 更自然可读 → 轻度润色
   → 保留原意改写 → 中度调整

3. 是否需要检测？
   → 是 → 用 GPTZero / Originality.ai 初检
   → 否 → 直接改写输出
```

## 输出格式

```markdown
## 人性化改写结果

### 原文（AI 风格）
[原始文本]

### 改写后（自然风格）
[改写文本]

### 改写说明
- 应用模式：[列出所用改写模式]
- 检测预期：[通过/不确定/可能触发]
- 主要改动：[2-3 个关键改动点]
```

## 依赖

- Python 3.7+
- 无外部 API 依赖（patterns.json 本地运行）
- 可选：GPTZero API（网络检测）

## 文件结构

```
humanize-text/
├── SKILL.md
├── scripts/
│   ├── transform.py   # 改写主脚本
│   ├── detect.py     # 检测脚本（本地规则）
│   └── patterns.json # 改写模式库
```
