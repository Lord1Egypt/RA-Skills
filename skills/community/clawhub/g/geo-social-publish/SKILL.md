---
name: geo-social-publish
description: "[已废弃] 原 SAU 群发龙虾。请改用 SaaS 下载 Word/ZIP + 本机融媒宝批量发布；勿安装本 skill。"
requires:
  bins:
    - sau
---

# GEO 自媒体分发（已废弃）

**本 skill 已停用。** 群发请：

1. SaaS **内容生成** → 下载单篇 Word 或批次 ZIP（每篇一个 docx）
2. 安装 **融媒宝**（见 SaaS「群发助手安装指南」）批量导入发布

以下内容仅供历史参考，**不要**执行 sau 或 coordinator 群发分支。

## 本机 sau（协调器在群发前应完成）

### 1. 安装包

- SaaS 安装指南或同域下载：`https://ai.gaobobo.cn/downloads/social-auto-upload.zip`
- 解压到固定目录（示例 `C:\Users\birds\Desktop\local\social-auto-upload-main`）

### 2. 安装 CLI

在解压目录：

```bash
uv pip install -e .
# 无 uv 则：pip install -e .
```

### 3. PATH（Windows 常见：仅 venv 内有 sau）

当前终端执行（协调器执行 sau 前应等价执行）：

```powershell
$env:PATH += ";<解压目录>\.venv\Scripts"
sau --help
```

永久加入用户 PATH：将 `<解压目录>\.venv\Scripts` 写入系统环境变量。

### 4. 平台登录（需用户扫码）

对任务 `pendingSauPlatforms` 中每个平台（如 `kuaishou`、`bilibili`）：

```bash
sau kuaishou login
sau bilibili login
```

以 `sau --help` 为准替换子命令。Cookie 建议：`~/.qclaw/sau-cookies/{platform}/`

---

## API

- 基址：`https://ai.gaobobo.cn`
- `GEO_KEY`：`~/.qclaw/geo-api-key` 或 `~/.openclaw/geo-api-key`

## 1. 导出成稿

```bash
GEO_KEY=$(cat ~/.qclaw/geo-api-key 2>/dev/null || cat ~/.openclaw/geo-api-key 2>/dev/null)
CG_ID="CG-XXXXXXXX"
curl -s "https://ai.gaobobo.cn/api/geo/publish/export/$CG_ID" \
  -H "Authorization: Bearer $GEO_KEY"
```

得到 `title`、`plainText`、`htmlBody`、`brandName`。将 `htmlBody` 写入临时文件。

## 2. sau 发布

以 sau 仓库当前 CLI 为准（`install.md` / `docs/agent-bootstrap.md`）。示例（小红书）：

```bash
sau xiaohongshu upload-image \
  --title "标题" \
  --content-file ./tmp/article.html
```

## 3. 回写 SaaS

```bash
curl -s -X POST "https://ai.gaobobo.cn/api/geo/publish/social/report" \
  -H "Authorization: Bearer $GEO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "optimization_task_id": "OPT-XXX",
    "cycle_number": 1,
    "content_task_id": "CG-XXX",
    "platform": "xiaohongshu",
    "status": "success",
    "platform_url": "https://..."
  }'
```

`status` 可为 `success` 或 `failed`；失败时填 `error`。

## 4. 验证

`GET /api/geo/optimization/{OPT_ID}/cycles/latest` 中 `sauPublish.platforms.{slug}.status` 应为 `success`。

## 注意

- Cookie 仅存本机
- 网易 OAuth 发稿由 SaaS Celery 负责，与本 skill 并行
