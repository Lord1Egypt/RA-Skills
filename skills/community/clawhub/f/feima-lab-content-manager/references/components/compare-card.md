# CompareCard 速查

**用途**：明显的 A vs B 对比，两列等长要点。

## 语法

    <CompareCard
      left='{"title":"方案 A","items":["简单","性能一般"]}'
      right='{"title":"方案 B","items":["复杂","性能优秀"]}'
    />

## Props

| 名称 | 类型 | 说明 |
|---|---|---|
| `left` | `{title, items}` (JSON 字符串) | 左侧卡片（背景蓝色调） |
| `right` | `{title, items}` (JSON 字符串) | 右侧卡片（背景绿色调） |

## 注意

- 两列内容应**等长、等重要度**（否则用列表）
- items 是扁平字符串数组，不支持嵌套结构
- 需要更复杂对比 → 用 markdown 表格

## 何时不用

- 两列长度严重不对称
- 要对比超过两项 → 用表格
- 对比项需要图片 → 用表格或 ImageCarousel
