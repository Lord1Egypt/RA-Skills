# 上传图片

`POST /api/skill/base-image/upload`

## 请求参数（Body - JSON）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image_base64encode` | string | ✅ 必填 | 图片的 Base64 编码字符串。**不要带 `data:image/png;base64,` 前缀，只传纯 base64 部分** |
| `image_name` | string | ✅ 必填 | 图片名称，需含正确的文件扩展名（如 `test.jpg`、`6666.png`） |
| `group_type` | string | 选填 | 图片业务类型，不填默认为 `product` |

> 支持的图片格式：`jpg`、`gif`、`png`、`webp`、`avif`

### group_type 枚举

| 值 | 说明 |
|----|------|
| `product` | 商品图片（默认） |
| `category` | 商品专辑图片 |
| `blog_article` | 博客文章图片 |
| `editor` | 编辑器里面的图片 |
| `common` | 通用图片 |

## 调用

```
node scripts/proxy/api-call.js POST /api/skill/base-image/upload '{"image_base64encode":"iVBORw0KGgo...","image_name":"product.jpg","group_type":"product"}'
```

## 响应

**`code` 为 `200` 表示调用成功；`code` 不为 `200` 表示调用失败。**

### 成功响应

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "name": "a5f51aa28b9c58e7f9b1943b584b0883.png",
        "path": "/product/15/image/2026/05/05/a5f51aa28b9c58e7f9b1943b584b0883.png",
        "width": 1200,
        "height": 468,
        "ratio": 2.56,
        "group_type": "product",
        "ext": "png",
        "size": 45727,
        "md5": "ec6b3c25bfb6282d0a4ec200db09f8f3",
        "year": "2026",
        "month": "05"
    }
}
```

## 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | Number | 状态码，`200` 表示成功 |
| `message` | String | 执行结果的文字描述 |
| `name` | string | 图片名称（服务端生成的文件名，可能与传入的 `image_name` 不同） |
| `path` | string | **图片存储路径** — 用于后续业务（如商品 `images[].src`、专辑等） |
| `width` | int | 图片宽度（像素） |
| `height` | int | 图片高度（像素） |
| `ratio` | float | 宽高比 |
| `group_type` | string | 图片业务类型 |
| `ext` | string | 图片文件后缀 |
| `size` | int | 图片大小（字节） |
| `md5` | string | 图片 MD5 编码 |
| `year` | string | 年 |
| `month` | string | 月 |

## 注意事项

1. `image_base64encode` 字段只需传入纯 base64 字符串，**不要**带 `data:image/png;base64,` 等前缀
2. `image_name` 需包含正确的文件扩展名（如 `.png`、`.jpg`）
3. `group_type` 必须从枚举值中选择，否则可能导致上传失败
4. 上传成功后，服务端会重新命名文件（返回的 `name` 可能与传入的 `image_name` 不同）
5. 错误时 `code` 不为 `200`，`message` 包含具体错误描述（如格式不支持、大小超限等）
