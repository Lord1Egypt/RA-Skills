---
name: volcengine-storage-tos
description: Object storage operations for Volcengine TOS (Tinder Object Storage). Use when users need bucket management, object upload/download, listing, deletion, presigned URLs, or storage troubleshooting.
---

Category: provider

# Volcengine TOS 对象存储

## Validation

```bash
mkdir -p output/volcengine-storage-tos
python -m py_compile skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py && echo "py_compile_ok" > output/volcengine-storage-tos/validate.txt
```

Pass criteria: command exits 0 and `output/volcengine-storage-tos/validate.txt` is generated.

## Output And Evidence

- Save operation results, manifests, and logs to `output/volcengine-storage-tos/`.
- Keep one validation log per execution.

## Prerequisites

- Python 3.8+
- Install TOS SDK: `pip install tos`
- Set environment variables:
  - `VOLCENGINE_ACCESS_KEY` — AK（AccessKey ID）
  - `VOLCENGINE_SECRET_KEY` — SK（SecretKey）
  - `VOLCENGINE_TOS_ENDPOINT` — TOS 服务端点，如 `tos-cn-beijing.volces.com`
  - `VOLCENGINE_TOS_REGION` — 地域，如 `cn-beijing`

Optional: use `.env` in repo root; script will auto-load.

## Normalized interface

### Subcommands

| Subcommand | Description |
|------------|-------------|
| `list-buckets` | 列举所有桶 |
| `create-bucket` | 创建桶 |
| `delete-bucket` | 删除桶（需为空桶） |
| `list-objects` | 列举桶内对象（支持 prefix/max-keys） |
| `upload` | 上传本地文件到桶 |
| `download` | 下载对象到本地文件 |
| `delete` | 删除对象 |
| `head` | 获取对象元数据（大小、类型、ETag） |
| `presign` | 生成预签名 URL |
| `copy` | 复制对象 |

### Common flags
- `--bucket` — 桶名
- `--key` — 对象键
- `--file` — 本地文件路径（上传/下载用）
- `--prefix` — 列举前缀
- `--max-keys` — 列举数量上限，默认 100
- `--expires` — 预签名有效期（秒），默认 3600
- `--print-json` — 输出 JSON 格式

## Quick start

```bash
# 列举所有桶
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py list-buckets

# 列举桶内对象
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py list-objects \
  --bucket my-bucket --prefix images/ --max-keys 50

# 上传文件
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py upload \
  --bucket my-bucket --key data/report.pdf --file ./report.pdf

# 下载文件
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py download \
  --bucket my-bucket --key data/report.pdf --file ./downloaded.pdf

# 获取元数据
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py head \
  --bucket my-bucket --key data/report.pdf

# 生成预签名 URL（1 小时有效）
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py presign \
  --bucket my-bucket --key data/report.pdf --expires 3600

# 删除对象（需显式确认 --confirm）
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py delete \
  --bucket my-bucket --key data/report.pdf --confirm
```

## Safety Rules

- **删除操作**（delete / delete-bucket）需传 `--confirm` 标志，防止误删。
- 上传时自动推断 Content-Type。
- 下载时验证写入文件的大小与 Content-Length 一致。

## Operational guidance

- 端点格式：`tos-{region}.volces.com`，如 `tos-cn-beijing.volces.com`。
- 桶名全局唯一，3-63 个小写字母/数字/短横线。
- 大文件（>100MB）建议使用分片上传（SDK 自动处理）；本脚本使用 `put_object_from_file`，对中小文件友好。
- 遇 403 请检查 AK/SK 及 IAM 策略。

## Output location

- Default output: `output/volcengine-storage-tos/`
- Override base dir with `OUTPUT_DIR`.

## Workflow

1) Confirm user intent, bucket, region, and whether the operation is read-only or mutating.
2) Run one minimal read-only query (list-buckets / head) to verify connectivity and permissions.
3) Execute the target operation with explicit parameters and bounded scope.
4) Verify results and save output/evidence files.

## References

- `references/api_reference.md` — SDK 方法与 API 映射
- `references/sources.md` — 官方文档链接
