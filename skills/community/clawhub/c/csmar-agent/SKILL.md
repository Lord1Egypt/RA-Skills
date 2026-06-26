---
name: csmar-agent
user-invocable: true
description: 访问csmar公司提供的财报相关接口，当用户查询A股公司财报信息时使用，输出内容不添加最终总结文本,提示词财务,@csmar_agent,@csmar-agent关键词时调用。
metadata:
  openclaw:
    emoji: "🌊"
    requires:
      bins: ["python3"]
---


## Usage

```bash
python3 skills/csmar-agent/scripts/search.py '<query>'
```

## Request Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| query | str | yes | - | Search query |

## Examples

```bash
# Basic search
python scripts/search.py "平安银行最近三年财报"
```

## Rules
- Process only events where `event_type == "content"`.
- Read chunk text from `data.payload.content`.
- Print chunks with flush enabled to preserve real-time output.
- Skip empty or non-string chunk values.
- Do not print extra wrapping text before or after streamed content.

## Expected Output Style

- Terminal should show content as it arrives.
- No "summary", "done", or post-processing paragraph.
