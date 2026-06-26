# 商品图片查询

## 功能说明

通过商品 ID 获取商品的主图 URL 列表，供图片优化、抠图等后续操作使用。

## CLI 调用

```bash
python3 {baseDir}/cli.py image_info --offer_id 商品ID
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--offer_id` / `-o` | 是 | 1688 商品 ID（纯数字） |

## 输出格式

```json
{
  "success": true,
  "markdown": "商品 123456 的主图信息：...",
  "data": {
    "main_image_urls": ["url1", "url2", "url3", ...],
    "white_image_url": "url"
  }
}
```

## 输出字段说明

- `main_image_urls`：商品主图 URL 列表，**第 1 张为默认主图**
- `white_image_url`：白底图 URL（如有）

## 结果展示

向用户展示所有主图，标记默认主图：

```
商品 123456 的主图信息：

1. （默认主图）![主图1](url1)
2. ![主图2](url2)
...

白底图：![白底图](white_url)
```

## 与其他子 skill 的关系

本子 skill 是**图片优化**（`references/80_image_optimize.md`）的组成部分：

- 图片优化 = 商品图片查询（本 skill） + 图片编辑（`references/40_image_edit.md`）
- 当用户提供商品 ID 而非直接提供图片 URL 时，需要先调用本 skill 获取主图 URL

## 异常处理

| 错误场景 | 处理方式 |
|----------|----------|
| success=false + "AK 未配置" | 触发 AK 配置流程（`references/10_ak_configure.md`） |
| 返回空的 main_image_urls | 提示用户确认商品 ID 是否正确 |
| 商品不存在 | 提示用户检查商品 ID |
