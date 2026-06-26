---
name: dingtalk-csa
description: 钉盘助手 (DingTalk Cloud Storage Assistant) - 管理钉钉云盘空间、文件和文档。用当用户要求读写钉盘文件、管理团队空间、上传下载文档、操作adoc文档时触发。也适用于钉钉文件分析、报告生成、团队协作等场景。触发词：钉盘、钉钉云盘、DingTalk storage、钉钉文件、钉钉文档。
metadata:
  openclaw:
    requires:
      env:
        DINGTALK_APP_KEY: "钉钉应用 AppKey"
        DINGTALK_APP_SECRET: "钉钉应用 AppSecret（敏感凭据，切勿明文写在配置文件中）"
---

# 钉盘助手 DingTalk Cloud Storage Assistant

管理钉钉云盘：团队空间、文件上传下载、钉钉文档读写、团队协作。

## 🔒 安全模型：读任意，写受限

**核心原则：AI 可以读取任何可访问的空间，但只能写入指定的文件夹。**

这确保了：
- ✅ AI 可以读取团队共享文件（用于分析、总结等）
- ✅ AI 只能在预批准的协作文件夹中写入
- ❌ 重要文件不会被意外修改或覆盖

### 配置写入白名单

在 SKILL.md 的 `ALLOWED_WRITE_PATHS` 中配置允许写入的位置：

```yaml
# === 写入白名单 ===
# AI 只能写入以下位置
ALLOWED_WRITE_PATHS:
  - spaceId: "YOUR_SPACE_ID"
    parentDentryId: "YOUR_FOLDER_ID"
    path: "/AI_Collab"
    description: "AI协作文件夹 - AI只允许写入此文件夹"
```

**执行规则：**
1. **读取**：允许访问任何空间/文件夹 ✅
2. **写入**（上传文件、创建文档、创建文件夹）：仅在白名单内 ✅
3. **删除**：不允许 ❌
4. 任何写入操作前，必须先检查目标路径是否在白名单中

## 🔑 认证

所有 API 调用需要 access token，通过以下方式获取：

```bash
curl -X POST 'https://api.dingtalk.com/v1.0/oauth2/accessToken' \
  -H 'Content-Type: application/json' \
  -d '{"appKey": "'"$DINGTALK_APP_KEY"'", "appSecret": "'"$DINGTALK_APP_SECRET"'"}'
```

**环境变量配置：**
- `DINGTALK_APP_KEY` — 钉钉应用的 AppKey
- `DINGTALK_APP_SECRET` — 钉钉应用的 AppSecret（⚠️ 绝不要明文写在代码或配置文件中）

Token 有效期 2 小时，请缓存避免重复请求。

## 核心操作

### 1. 列出空间（读 ✅）

```bash
# 企业空间
curl -X GET "https://api.dingtalk.com/v1.0/drive/spaces?unionId=<unionId>&spaceType=org&maxResults=50" \
  -H "x-acs-dingtalk-access-token: <TOKEN>"
```

### 2. 列出文件（读 ✅）

```bash
curl -X POST "https://api.dingtalk.com/v1.0/storage/spaces/{spaceId}/dentries/listAll" \
  -H "x-acs-dingtalk-access-token: <TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"unionId": "<unionId>"}'
```

### 3. 读取文档内容（读 ✅）

.adoc 格式的钉钉文档，用 `uuid` 作为 documentId：

```bash
curl -X GET "https://api.dingtalk.com/v1.0/doc/suites/documents/{documentId}/blocks?operatorId=<unionId>" \
  -H "x-acs-dingtalk-access-token: <TOKEN>"
```

### 4. 写入文档内容（写 ⚠️ 检查白名单）

```bash
# 覆写整个文档（Markdown格式）
curl -X POST "https://api.dingtalk.com/v1.0/doc/suites/documents/{documentId}/overwriteContent?operatorId=<unionId>" \
  -H "x-acs-dingtalk-access-token: <TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"content": "# Markdown Content", "dataType": "markdown"}'

# 追加内容到文档
curl -X POST "https://api.dingtalk.com/v1.0/doc/suites/documents/{documentId}/content?operatorId=<unionId>" \
  -H "x-acs-dingtalk-access-token: <TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"content": {"type": "markdown", "content": "## New Section"}}'
```

### 5. 创建文件夹（写 ⚠️ 检查白名单）

```bash
curl -X POST "https://api.dingtalk.com/v1.0/storage/spaces/{spaceId}/dentries/{parentId}/folders" \
  -H "x-acs-dingtalk-access-token: <TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"unionId": "<unionId>", "name": "New Folder"}'
```

### 6. 上传文件（写 ⚠️ 检查白名单）

3步流程，详见 [references/upload-guide.md](references/upload-guide.md)

### 7. 下载文件（读 ✅）

```bash
curl -X POST "https://api.dingtalk.com/v1.0/storage/spaces/{spaceId}/dentries/{dentryId}/downloadInfos/query?unionId=<unionId>" \
  -H "x-acs-dingtalk-access-token: <TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"option": {"version": 1}}'
```

## 必需权限

详见 [references/permissions.md](references/permissions.md)

核心权限（7个）：
1. `Storage.Space.Read` - 钉盘应用盘空间读
2. `Storage.Space.Write` - 钉盘应用盘空间写
3. `Storage.File.Read` - 钉盘应用文件读
4. `Storage.File.Write` - 钉盘应用文件写
5. `Storage.UploadInfo.Read` - 钉盘上传信息读
6. `Storage.DownloadInfo.Read` - 钉盘下载信息读
7. `企业存储文件下载信息读权限` - 企业存储文件下载（配合#6）

## 参考文档

- [permissions.md](references/permissions.md) - 完整权限清单和开通指南
- [permission-list-share.md](references/permission-list-share.md) - 可分享给管理员的权限清单
- [upload-guide.md](references/upload-guide.md) - 3步上传流程详解