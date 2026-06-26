---
name: feishu-bitable-upload
description: "Upload files (images, videos, attachments) to Feishu (Lark) Bitable (multi-dimensional table) and return the file_token. Auto-selects direct upload for files up to 20MB or chunked upload (prepare, part, finish) for larger files. Requires App ID and Secret (lark-cli does NOT cover the /drive/v1/medias/ API). Use when the user wants to: upload a file/image/video to Feishu Bitable, get a file_token from Feishu Drive API, upload attachments to 多维表格 (bitable), 上传文件到飞书多维表格, 获取 file_token."
---

# 上传素材到飞书多维表格（获取 file_token）

## 与官方 lark-* Skill 的定位

| 场景 | 工具 |
|---|---|
| 上传附件直接写入记录 | `lark-cli base +record-upload-attachment` |
| 上传文件到云空间 | `lark-cli drive +upload` |
| **上传素材获取独立 file_token** | **本 Skill** |

`lark-cli` 不覆盖 `/drive/v1/medias/` 素材接口，本 Skill 填补该空白。
获取到的 `file_token` 可用于后续写入多维表格附件字段。

## 依赖

- `bash`, `curl`, `python3`, `dd` — macOS/Linux 均内置
- 飞书 App 凭证（App ID + App Secret）

## 脚本

`scripts/feishu_upload.sh`

## 用法

```bash
# 参数模式
bash scripts/feishu_upload.sh <文件> --parent-node <APP_TOKEN> \
  --app-id <APP_ID> --app-secret <APP_SECRET>

# 环境变量模式
export FEISHU_PARENT_NODE=<APP_TOKEN>
export FEISHU_APP_ID=<APP_ID>
export FEISHU_APP_SECRET=<APP_SECRET>
bash scripts/feishu_upload.sh <文件>
```

`--parent-type` 可选（默认 `bitable_file`）：图片附件用 `bitable_image`。

成功后输出 `file_token: boxcnrHpsg1QDqXAAAyachabcef`

## 自动选择上传方式

| 文件大小 | 上传方式 | API |
|---|---|---|
| ≤ 20MB | 直接上传 | `POST /drive/v1/medias/upload_all` |
| > 20MB | 分片上传 | `upload_prepare` → `upload_part × N` → `upload_finish` |

> `upload_all` API 硬限制 20MB，超过必须分片（分片大小 4MB，由服务端返回）。

## 常见错误

| 错误码 | 原因 | 解决 |
|---|---|---|
| 1061004 | 无权限 | 确认应用有 `bitable:app` 权限且对目标表有编辑权限 |
| 1061044 | parent_node 不存在 | 检查多维表格 App Token 是否正确 |
| 1061043 | 文件超限 | 检查文件大小是否符合飞书限制 |
| 1061005 | Token 无效 | 检查 App ID / Secret 是否正确 |
