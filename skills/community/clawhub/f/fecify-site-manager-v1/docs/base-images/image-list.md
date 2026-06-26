# 图片列表

`GET /api/skill/base-image/get-image-list`

## 请求参数（Query String）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `pageNum` | int | 选填 | 页码，不填默认第 1 页 |
| `pageSize` | int | 选填 | 每页数据个数，不填使用系统默认值 |
| `group_type` | string | 选填 | 图片分组，用于筛选指定类型图片 |
| `begin_at` | string | 选填 | 图片创建时间区间过滤—开始时间，格式 `YYYY-MM-DD`（如 `2025-05-01`） |
| `end_at` | string | 选填 | 图片创建时间区间过滤—结束时间，格式 `YYYY-MM-DD`（如 `2026-05-29`） |

### group_type 枚举

| 值 | 说明 |
|----|------|
| `product` | 商品图片 |
| `category` | 商品专辑图片 |
| `blog_article` | 博客文章图片 |
| `editor` | 编辑器里面的图片 |
| `common` | 通用图片 |

## 调用

```
node scripts/proxy/api-call.js GET /api/skill/base-image/get-image-list '{"pageNum":1,"pageSize":10,"group_type":"product","begin_at":"2025-05-01","end_at":"2026-05-29"}'
```

## 响应示例

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "upload_img_max_size": 40960,
        "upload_img_allow_types": ["image/gif", "image/jpeg", "image/png", "image/webp", "image/avif"],
        "list": [
            {
                "id": 49846,
                "name": "a5f51aa28b9c58e7f9b1943b584b0883.png",
                "path": "/product/15/image/2026/05/05/a5f51aa28b9c58e7f9b1943b584b0883.png",
                "group_type": "product",
                "shop_id": 15,
                "width": 1200,
                "height": 468,
                "ratio": "2.56"
            }
        ],
        "total": 3353,
        "pageSize": 10,
        "totalPage": 336
    }
}
```

## 返回字段

### data 顶层

| 字段 | 类型 | 说明 |
|------|------|------|
| `upload_img_max_size` | int | 系统配置：上传图片的最大尺寸（KB） |
| `upload_img_allow_types` | string[] | 系统配置：支持的上传图片 MIME 类型 |
| `list` | Array | 图片列表 |
| `total` | int | 所有数据的总行数 |
| `pageSize` | int | 每页数据个数 |
| `totalPage` | int | 总页数 |

### data.list[] 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 图片 ID |
| `name` | string | 图片名称（服务端存储的文件名） |
| `path` | string | 图片存储路径 |
| `group_type` | string | 图片分组 |
| `shop_id` | int | 店铺 ID |
| `width` | int | 图片宽度（像素） |
| `height` | int | 图片高度（像素） |
| `ratio` | string | 图片宽高比 = `width / height` |

## 注意事项

1. `pageNum`、`pageSize`、`group_type`、`begin_at`、`end_at` 均为选填参数
2. `begin_at` 和 `end_at` 配合使用可按图片创建时间进行区间过滤
3. `group_type` 必须从枚举值中选择
4. `upload_img_max_size` 和 `upload_img_allow_types` 为系统配置值，表示当前站点允许的上传限制
