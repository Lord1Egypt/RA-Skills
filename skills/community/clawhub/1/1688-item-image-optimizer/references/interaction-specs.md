# 交互组件详细规范

本文档定义了 1688-item-image-optimizer Skill 中所有交互组件的具体数据结构与映射规则。大模型在调用 `show_interaction` 前需查阅本文档，确保数据结构正确。

---

## 0. open_tab_image_optimize (Open Tab 组件)

### 组件类型

`type: open_tab` — 根据上下文是否包含商品 ID，输出对应的 JSON 唤起图片优化页面，**流程到此结束，禁止反问用户，禁止调用任何 CLI 命令，禁止执行任何额外逻辑。**

### 分支 A — 上下文中未包含商品 ID

直接返回以下 JSON：

```json
{
  "type": "open_tab",
  "selectionType": "shop_backend",
  "url": "https://air.1688.com/app/CSBC-modules/csbc-ai-component-loader/picture-optimize.html",
  "pageTitle": "图片优化",
  "pageDescription": "自动为商品主图增加热卖元素，以获取更多的买家点击与下单",
  "icon": "https://img.alicdn.com/imgextra/i4/O1CN01mrO0tG29hOrSoKhyr_!!6000000008099-2-tps-80-80.png"
}
```

### 分支 B — 上下文中包含商品 ID

将商品 ID 拼接到 URL 的 `offerId` 参数中，返回以下 JSON（示例中 `123123` 替换为实际商品 ID）：

```json
{
  "type": "open_tab",
  "selectionType": "shop_backend",
  "url": "https://air.1688.com/app/CSBC-modules/csbc-ai-component-loader/picture-optimize.html?offerId=123123",
  "pageTitle": "图片优化",
  "pageDescription": "自动为商品主图增加热卖元素，以获取更多的买家点击与下单",
  "icon": "https://img.alicdn.com/imgextra/i4/O1CN01mrO0tG29hOrSoKhyr_!!6000000008099-2-tps-80-80.png"
}
```

### 行为说明

- 该交互为 **fire-and-forget** 模式，输出 JSON 后流程即结束，无需任何后续步骤
- 聊天区会同步出现一张只读气泡卡片

---
