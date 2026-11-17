# 交互组件详细规范 — 1688-item-image-optimizer

本文档定义了本 Skill 中所有交互组件的具体数据结构与映射规则。大模型在调用 `show_interaction` 前需查阅本文档，确保数据结构正确。

---

## 1. open_tab_image_optimize（open_tab 组件）

### 组件类型
`type: open_tab`

### 数据槽位

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ | 固定 `"open_tab"` |
| `selectionType` | string | ✅ | 固定 `"shop_backend"` |
| `url` | string | ✅ | 由 `build_tool_url` capability 返回的完整 URL（已经过 URL encode） |
| `title` | string | ✅ | 页面标题：`主图优化` / `轮播图制作` / `详情图制作` / `背景替换` / `数字模特` |

### 完整调用示例

**主图优化（main）：**
```json
{
  "type": "open_tab",
  "selectionType": "shop_backend",
  "url": "https://pre-air.1688.com/app/CSBC-modules/csbc-ai-component-loader/picture-optimize.html?__mtop_subdomain__=wapa&type=oneOptimization&imgUrl=%2FUsers%2Fseller%2FDesktop%2Fproduct.jpg",
  "title": "主图优化"
}
```

**轮播图（多图）：**
```json
{
  "type": "open_tab",
  "selectionType": "shop_backend",
  "url": "https://pre-air.1688.com/app/CSBC-modules/csbc-ai-component-loader/picture-optimize.html?__mtop_subdomain__=wapa&type=carouselImage&imgUrlList=%2Fpath%2F1.jpg%2C%2Fpath%2F2.jpg",
  "title": "轮播图制作"
}
```

**详情图（商品 ID）：**
```json
{
  "type": "open_tab",
  "selectionType": "shop_backend",
  "url": "https://pre-air.1688.com/app/CSBC-modules/csbc-ai-component-loader/picture-optimize.html?__mtop_subdomain__=wapa&type=detailImage&offerId=1016555587352",
  "title": "详情图制作"
}
```

**背景替换（replaceSubject，单图）：**
```json
{
  "type": "open_tab",
  "selectionType": "shop_backend",
  "url": "https://pre-air.1688.com/app/CSBC-modules/csbc-ai-component-loader/picture-optimize.html?__mtop_subdomain__=wapa&type=replaceSubject&imgUrl=%2Fpath%2Fproduct.jpg",
  "title": "背景替换"
}
```

> 其余单图工具——数字模特（`type=digitalModel` / 标题`数字模特`）——URL 结构同背景替换，仅 `type` 与 `title` 不同，均用 `imgUrl` 单图参数。

### 注意事项
- URL 必须来自 `build_tool_url` 返回，**禁止 LLM 编造/拼接**
- `build_tool_url` 返回 `success=false` 时禁止触发
- 触发即为 skill 终态，不追加文字引导

---

## 2. select_image_type（card 组件）

### 组件类型
`type: card`

### 触发时机
触发词命中但 LLM 无法确定具体图片类型时（如"帮我做一套图"）

### ⚠️ 有权限的所有 type 全部平铺 + 先校验权限

1. 弹出前**先执行** `python3 {baseDir}/cli.py verify_permission` 拿权限（`data.data.isAi` / `data.data.digitalModel`），`success=false` 时按铁律 6 fail-closed 拦截。
2. 按权限把**有权限的所有 type 全部平铺**进 `options`（不做收纳/Top3/「其他功能」）：

| 权限 | `options`（全平铺） | 项数 |
|------|--------------------|------|
| `isAi=false`（基础版） | 主图优化、背景替换 | **2** |
| `isAi=true, digitalModel=false`（高级版无数字模特） | ＋轮播图、详情图 | **4** |
| `isAi=true, digitalModel=true`（高级版全权限） | ＋数字模特 | **5** |

### 完整调用示例

**基础版（2 项全平铺）：**
```json
{
  "type": "card",
  "selectionType": "image_type",
  "questions": [
    { "question": "你想制作哪种商品图片？", "options": ["主图优化", "背景替换"], "allowMultiple": false, "required": true }
  ]
}
```

**高级版全权限（5 项全平铺）：**
```json
{
  "type": "card",
  "selectionType": "image_type",
  "questions": [
    { "question": "你想制作哪种商品图片？", "options": ["主图优化", "轮播图", "详情图", "背景替换", "数字模特"], "allowMultiple": false, "required": true }
  ]
}
```

### 回传映射

| 用户选择 | 对应 --type 参数 |
|---------|----------------|
| 主图优化 | `main` |
| 轮播图 | `carousel` |
| 详情图 | `detail` |
| 背景替换 | `replaceSubject` |
| 数字模特 | `digitalModel` |

---

## 3. select_images（card 组件）

### 组件类型
`type: card`

### 触发时机
用户上传图片数量超出工具限制时

### 图片超限阈值

| 工具类型 | 上限 |
|---------|------|
| 主图优化 | 1 张 |
| 轮播图 | 9 张 |
| 详情图 | 20 张 |
| 背景替换 / 数字模特 | 1 张 |

### 完整调用示例

```json
{
  "type": "card",
  "selectionType": "image",
  "questions": [
    {
      "question": "你上传了 15 张图片，轮播图工具最多支持 9 张。请选择要处理的图片：",
      "options": ["图片1.jpg", "图片2.jpg", "图片3.jpg", "..."],
      "allowMultiple": true,
      "required": true
    }
  ]
}
```
