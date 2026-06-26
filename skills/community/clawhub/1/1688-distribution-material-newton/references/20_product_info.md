# 商品信息查询

## 功能说明

从用户 query 中提取商品 ID（offer_id），用于后续的标题优化、卖点生成、图片查询等操作。商品 ID 是一串纯数字（如 `745205218498`），通常出现在用户消息或 1688 商品链接中。

## 商品 ID 提取规则

1. **用户直接给出数字**：如 "帮我优化 745205218498 的标题" → offer_id = `745205218498`
2. **用户给出 1688 链接**：从 URL 中提取 offer_id 参数或路径中的数字串
   - `https://detail.1688.com/offer/745205218498.html` → offer_id = `745205218498`
3. **用户未提供**：提示用户提供商品 ID 或商品链接

## 获取商品主图信息

当需要获取商品的图片信息时，使用 `image_info` 命令：

```bash
python3 {baseDir}/cli.py image_info --offer_id 商品ID
```

- 只支持传入**一个**商品 ID
- 输出 `data.main_image_urls` 中**第一张为默认主图**
- 输出 `data.white_image_url` 为白底图（如有）

## 输出格式

```json
{
  "success": true,
  "markdown": "...",
  "data": {
    "main_image_urls": ["url1", "url2", ...],
    "white_image_url": "url"
  }
}
```

## 被引用场景

本子 skill 被以下流程引用：

- **图片优化**（`references/80_image_optimize.md`）：当用户提供商品 ID 而非图片 URL 时，先通过本 skill 获取主图 URL
- **抠图**（`references/50_cutout_image.md`）：当用户提供商品 ID 时，先获取主图再抠图
- **标题优化**（`references/60_title_optimize.md`）：需要商品 ID 作为输入
- **卖点生成**（`references/70_selling_point.md`）：需要商品 ID 作为输入
