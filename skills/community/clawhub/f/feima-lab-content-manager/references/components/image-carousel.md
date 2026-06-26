# ImageCarousel 速查

**用途**：同主题的系列截图、流程截图、产品对比图。

## 语法

    <ImageCarousel images='[
      {"src":"./images/a.png","alt":"首页","caption":"改造前"},
      {"src":"./images/b.png","alt":"首页","caption":"改造后"},
      {"src":"./images/c.png","caption":"细节"}
    ]' />

## Props

| 名称 | 类型 | 说明 |
|---|---|---|
| `images` | `{src, alt?, caption?}[]` (JSON 字符串) | 图片数组 |

## 硬规则

- **至少 3 张图**才用 Carousel。≤2 张用普通 md 图片
- src 必须是**已本地化路径** `./images/xxx`（image-localize.mjs 会自动处理）
- 交互：左右按钮 + dot 导航 + 图片预加载

## 何时不用

- 图片数量 1-2 张
- 图片之间互不相关
- 需要并排对比查看 → 用表格嵌图或 CompareCard
