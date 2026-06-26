# Timeline 速查

**用途**：分步骤流程、时间顺序事件、操作指南。

## 语法

    <Timeline steps='[
      {"title":"步骤 1","description":"详细说明"},
      {"title":"步骤 2","description":"..."},
      {"title":"步骤 3"}
    ]' />

## Props

| 名称 | 类型 | 说明 |
|---|---|---|
| `steps` | `{title, description?}[]` (JSON 字符串) | 步骤数组，≥3 步才用 |

## 硬规则

- **至少 3 步**才用 Timeline。2 步及以下用有序列表 `1. 2.`
- 每步 title 必填，description 可选
- description 不超过 2-3 行（否则考虑拆小节）

## 何时不用

- 只有 1-2 步 → 有序列表
- 步骤有分支/条件 → 流程图（目前 skill 不支持，改用 md 描述）
