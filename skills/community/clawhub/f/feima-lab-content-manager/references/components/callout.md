# Callout 速查

**用途**：补充说明、提示、警告、结论强调。分 4 种语义。

## 语法

    <Callout type="tip" title="可选标题">
    正文，支持 **粗体** / 链接 / 列表
    </Callout>

## Props

| 名称 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `type` | `"tip" \| "warning" \| "info" \| "error"` | `"info"` | 语义类型，决定配色和图标 |
| `title` | `string` | — | 可选标题 |

## 语义选择

| type | 图标 | 何时用 |
|---|---|---|
| `tip` | 💡 | 技巧、最佳实践、小贴士 |
| `info` | ℹ️ | 补充信息、背景说明 |
| `warning` | ⚠️ | 注意事项、常见坑、非致命警告 |
| `error` | ❌ | 严重错误、不要这样做 |

## 示例

    <Callout type="warning" title="注意">
    该接口需要管理员权限才能调用。
    </Callout>

## 何时不用

- 一句普通补充 → 用纯 md 段落
- 需要折叠的次要信息 → 用 `Collapse`
