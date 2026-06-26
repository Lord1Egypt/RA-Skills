> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 6.12 POST /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/references/create

为指定资产新建一张**参考图**（上传原图并生成缩略图）。

**鉴权与权限：**

- 需携带 `Authorization: Bearer <token>`。
- 需具备该 `play_id` 的访问权限（服务端会校验项目可访问性）。

**路径参数（Path）：**

| 参数         | 必填 | 类型 | 说明 |
|--------------|------|------|------|
| `play_id`    | 是   | int  | 剧目 ID |
| `asset_type` | 是   | int  | 资产类型：1 场景、2 角色、3 道具、4 平面、5 其他 |
| `asset_id`   | 是   | int/string | 资产 ID |

**请求体（multipart/form-data）：**

| 字段     | 必填 | 类型   | 说明 |
|----------|------|--------|------|
| `name`   | 是   | string | 参考图名称 |
| `image`  | 是   | file   | 图片文件（二进制） |

支持图片扩展名：`.jpg`、`.jpeg`、`.png`、`.gif`、`.bmp`、`.webp`、`.tiff`。  
若上传文件后缀不在支持范围内，服务端会尝试从 `name` 推断后缀；仍无效时默认落盘为 `.png`。

**请求示例（curl）：**

```bash
curl -X POST "https://idrama.lingban.cn/openapi/drama/123/assets/2/456/general/references/create" \
  -H "Authorization: Bearer <TOKEN>" \
  -F "name=角色A_正面参考图" \
  -F "image=@/path/to/reference.png"
```

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "id": "1",
    "name": "角色A_正面参考图",
    "image": "1_角色A_正面参考图.png"
  }
}
```

| 字段    | 类型   | 说明 |
|---------|--------|------|
| `id`    | string | 新建参考图 ID（同一资产下递增） |
| `name`  | string | 参考图名称（请求中的 `name`） |
| `image` | string | 参考图原图文件名（落盘后名称） |

**错误响应示例：**

- 缺少 `image` 或 `name`：HTTP **500**。
- 资产不存在、资产类型与路径不一致、保存文件失败等：HTTP **500**。

```json
{
  "code": -1,
  "msg": {
    "error": "name required"
  }
}
```

```json
{
  "code": -1,
  "msg": {
    "error": "image file required"
  }
}
```
