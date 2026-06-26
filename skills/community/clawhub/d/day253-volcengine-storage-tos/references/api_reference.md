# Volcengine TOS SDK (Python) API 参考

本技能使用 [ve-tos-python-sdk](https://github.com/volcengine/ve-tos-python-sdk) (`pip install tos`)。

## 客户端初始化

```python
import tos
client = tos.TosClientV2(ak, sk, endpoint, region)
```

- `ak` / `sk`：火山引擎 IAM AccessKey / SecretKey
- `endpoint`：`tos-{region}.volces.com`，如 `tos-cn-beijing.volces.com`
- `region`：如 `cn-beijing`

## SDK 方法 → 脚本子命令映射

| 脚本子命令 | SDK 方法 | REST API |
|-----------|----------|----------|
| `list-buckets` | `client.list_buckets()` | `GET /` |
| `create-bucket` | `client.create_bucket(bucket)` | `PUT /{bucket}` |
| `delete-bucket` | `client.delete_bucket(bucket)` | `DELETE /{bucket}` |
| `list-objects` | `client.list_objects_type2(bucket, prefix, max_keys)` | `GET /{bucket}?list-type=2` |
| `upload` | `client.put_object_from_file(bucket, key, file_path, content_type)` | `PUT /{bucket}/{key}` |
| `download` | `client.get_object_to_file(bucket, key, file_path)` | `GET /{bucket}/{key}` |
| `delete` | `client.delete_object(bucket, key)` | `DELETE /{bucket}/{key}` |
| `head` | `client.head_object(bucket, key)` | `HEAD /{bucket}/{key}` |
| `presign` | `client.pre_signed_url(method, bucket, key, expires)` | (客户端签名) |
| `copy` | `client.copy_object(dst_bucket, dst_key, src_bucket, src_key)` | `PUT /{bucket}/{key}` + `x-tos-copy-source` |

## 常用响应字段

### list_buckets
- `resp.buckets[].name` — 桶名
- `resp.buckets[].location` — 地域
- `resp.buckets[].creation_date` — 创建时间

### list_objects_type2
- `resp.contents[].key` — 对象键
- `resp.contents[].size` — 大小（字节）
- `resp.contents[].last_modified` — 最后修改时间
- `resp.is_truncated` — 是否还有更多

### head_object
- `resp.content_length` — 大小
- `resp.content_type` — MIME 类型
- `resp.etag` — ETag
- `resp.last_modified` — 最后修改
- `resp.storage_class` — 存储类型

### put_object_from_file / put_object
- `resp.etag` — 上传后的 ETag
- `resp.status_code` — HTTP 状态码

### pre_signed_url
- `resp.signed_url` — 完整预签名 URL

## 异常类型

| 异常 | 说明 |
|------|------|
| `tos.exceptions.TosClientError` | 客户端错误（参数、网络等） |
| `tos.exceptions.TosServerError` | 服务端错误，含 `code`、`message`、`request_id` |

## 常见 HTTP 错误码

| 状态码 | 说明 |
|--------|------|
| 403 | AccessDenied — AK/SK 错误或无权限 |
| 404 | NoSuchBucket / NoSuchKey |
| 409 | BucketAlreadyExists / BucketNotEmpty |
| 429 | TooManyRequests — 请求过频 |
