---
name: alist-cli
displayName: "AList CLI (Cloud Storage CLI for AList)"
version: 1.6.2
description: |
  AList file management CLI for OpenClaw. Supports upload, download, list, mkdir, rm, mv, search, url.
  Auth via environment variables with auto-refresh. Trigger: file management, AList operations, upload/download.
---

# AList CLI

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)
- **GitHub**: https://github.com/KinemaClawWorkspace/alist-cli

AList file management CLI. Auth token managed via environment variables with auto-login and auto-refresh.

## ⚠️ Before First Use | 首次使用必读

**首次使用此 skill 前，必须先读取 [ONBOARDING.md](ONBOARDING.md) 完成环境配置。**

- **环境不可用**（命令不存在、依赖缺失、连接失败）→ 读取 [ONBOARDING.md](ONBOARDING.md) 按步骤排查修复
- **首次配置** → 读取 [ONBOARDING.md](ONBOARDING.md) 完成 6 步配置
- **配置完成后** → 直接使用下方 Run Commands

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ALIST_URL` | ✅ | AList server URL (e.g. `https://your-alist-server`) |
| `ALIST_USERNAME` | ✅ | Login username |
| `ALIST_PASSWORD` | ✅ | Login password |
| `ALIST_AUTH_TOKEN` | ❌ | Auth token (auto-obtained via login, skip manual set) |
| `ALIST_USER_INFO` | ❌ | User info JSON (auto-obtained via login, skip manual set) |

## Run Commands

```bash
alist-cli <command> [args]
```

### Commands

| Command | Description |
|---------|-------------|
| `login [username] [password]` | Login (outputs export statements to source) |
| `ls [path]` | List files |
| `get <path>` | Get file info + all URLs |
| `url <path>` | Get preview/download URLs for file or folder |
| `mkdir <path>` | Create folder |
| `upload <local> <remote>` | Upload file (outputs preview + download URL) |
| `rm <path>` | Delete file |
| `mv <src> <dst>` | Move file |
| `search <keyword> [path]` | Search files |
| `whoami` | Current user info |

## Upload Behavior | 上传行为

**上传前必须判断文件用途，选择正确的目标路径：**

### 判断规则

| 场景 | 目标路径 | 说明 |
|------|---------|------|
| **外部访问**（分享给他人、公开文件） | `/public/...` | Guest 可见，预览和下载链接无需登录 |
| **内部使用**（个人文件、工具输出、临时文件） | `/private/storage/...` | 需要登录才能访问 |

**如何判断：**
1. 用户明确说"分享给 XX"、"发给别人"、"外部" → `/public/`
2. 用户说"内部"、"私有"、"自己看"、"备份" → `/private/storage/`
3. 用户未说明 → **必须询问**文件用途
4. 批量上传多个文件到同一个目标 → 可以创建新文件夹整理
5. 单个文件 → 一般直接上传到已有目录，不新建文件夹（除非用户指定或目标目录为空）

### 文件夹创建规则

- ❌ 不要随意创建新文件夹
- ✅ 用户明确要求时才创建
- ✅ 批量上传且目标目录为空时，可以创建子文件夹
- ✅ 用户指定路径时，自动创建（mkdir -p 行为由 API 保证）

## URL Rules

AList 文件有两种链接：

### 1. 预览链接

```
{ALIST_URL}{path}
```

- 从 raw_url 去掉 `/p` 前缀和 `?sign=xxx` 参数
- **内部文件**（`/private/`）：需要 AList 登录态才能预览
- **外部文件**（`/public/`）：无需登录即可预览
- 例: `https://cloud.example.com/public/docs/notes.md`

### 2. 下载直链

```
API 返回的 raw_url 字段（包含 /p/ 前缀和 ?sign 签名）
```

- 直接下载文件，无需登录，curl/wget 可用
- 签名有时效性，过期后需重新通过 API 获取
- 例: `https://cloud.example.com/p/public/docs/notes.md?sign=abc123=:0`
- **分享文件时优先使用此链接**

### Directory Structure | 目录结构

```
/ (root)
├── public/        ← 外部访问（guest 挂载点）
│   └── ...
└── private/       ← 内部文件（需登录）
    └── storage/   ← 用户存储
        └── ...
```

### Path Mapping

```
user_path (用户输入)  →  real_path (AList API 使用)
/public/docs/a.md    →  /public/docs/a.md       (外部)
/private/storage/a   →  /private/storage/a       (内部)
```

- `base_path` 通过登录自动获取（`/api/me` 接口），当前为 `/`
- 预览链接基于 `real_path`（去掉 `/p` 和 `?sign`）
- 下载直链使用 API 返回的 `raw_url`

## Auth Behavior

- **Auto-login**: Script checks `ALIST_AUTH_TOKEN` on startup. If missing, auto-logins with `ALIST_USERNAME` + `ALIST_PASSWORD`.
- **Auto-refresh**: If API returns 401, automatically re-logins and retries.
- **Manual login**: `alist login` command outputs `export` statements. User should `eval $(alist login)` or manually `source` them.

## References

- `references/openapi.json` - AList API specification
