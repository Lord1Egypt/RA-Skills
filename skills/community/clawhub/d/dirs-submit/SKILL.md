---
name: dirs-submit
description:
  CLI tool for the `ship` command wrapping aidirs.org and backlinkdirs.com submission APIs. Use when the user
  needs to login, submit a URL, preview site metadata, check CLI version, or self-update the CLI from terminal.
  Supports browser login, per-site token storage, submit/fetch commands, version checks, and self-update.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://github.com/RobinWM/ship-skills#dirs-submit
---

# dirs-submit

Use `ship` to login, submit URLs, preview metadata, check versions, and self-update.

## Structure

- Read `references/config.md` when you need config shape or token storage details.
- Read `references/api.md` when you need request endpoints or payload examples.
- Read files under `examples/` when you need concrete success/error output examples.

## Workflow

### 1. Login — 浏览器授权

> 提交 URL 需要订阅计划。

```bash
ship login
```

可选指定站点：

```bash
ship login --site aidirs.org
ship login --site backlinkdirs.com
```

流程：

1. 选择站点（或通过 `--site` 指定）
2. 自动打开浏览器进入登录页
3. 用户在浏览器完成登录
4. CLI 在本地启动 localhost 回调接收 token
5. token 写入本地配置

成功输出：

```text
✅ Login successful
```

### 2. Token / Config 存储规则

配置文件路径：

```text
~/.config/ship/config.json
```

结构是**按站点分开存**：

```json
{
  "currentSite": "aidirs.org",
  "sites": {
    "aidirs.org": {
      "token": "xxx",
      "baseUrl": "https://aidirs.org"
    },
    "backlinkdirs.com": {
      "token": "yyy",
      "baseUrl": "https://backlinkdirs.com"
    }
  }
}
```

规则：

- 同一个站点再次登录，会覆盖该站点旧 token
- 不同站点互不覆盖
- `currentSite` 指向最后一次登录的站点
- 不传 `--site` 时，CLI 默认使用 `currentSite`

### 3. Submit — 提交 URL

```bash
ship submit <url>
```

示例：

```bash
ship submit https://example.com
ship submit https://example.com --site aidirs.org
ship submit https://example.com --site backlinkdirs.com
ship submit https://example.com --json
ship submit https://example.com --quiet
```

内部调用：

```http
POST /api/submit
Authorization: Bearer <token>
Content-Type: application/json

{ "link": "https://example.com" }
```

### 4. Fetch — 预览元数据

```bash
ship fetch <url>
```

示例：

```bash
ship fetch https://example.com
ship fetch https://example.com --site aidirs.org
ship fetch https://example.com --json
```

调用 `POST /api/fetch-website`，不创建提交记录。

### 5. Version / Update

```bash
ship version
ship version --latest
ship version --json
ship self-update
ship self-update --json
```

说明：

- `version --latest` 会检查 GitHub latest release
- `self-update` 会下载当前平台对应的 release asset 并替换本地可执行文件
- Windows 当前不做自动覆盖更新，会提示用户手动下载最新版本

## Result Interpretation

Skill 执行 CLI 后，应根据输出向用户自然语言转述：

- 成功提交 / 成功 fetch → 直接告知成功
- `401` → 告知 token 无效，建议重新运行 `ship login`
- `402` 或返回 `upgradeUrl` → 告知用户需要订阅，并附升级链接
- `400` → 直接转述具体错误
- 网络超时 / 网络错误 → 告知稍后重试

## 常见错误

| 状态码/情况 | 含义 | Skill 应告知用户 |
|---|---|---|
| 400 | URL 参数错误、重复站点等 | 直接告知具体错误原因 |
| 401 | Token 无效或未授权 | 提示重新运行 `ship login` |
| 402 | 需要订阅计划 | 友好提示订阅，并附 `upgradeUrl` |
| 500 | 服务器错误 | 告知稍后重试 |
| timeout/network | 网络超时或请求失败 | 告知网络问题并建议重试 |

## Environment / Config Reference

| 来源 | 键 | 说明 |
|---|---|---|
| 配置文件 | `~/.config/ship/config.json` | 本地存储多站点 token |
| 环境变量 | `DIRS_TOKEN` | Bearer Token（备用） |
| 环境变量 | `DIRS_BASE_URL` | API Base URL（备用） |
| CLI 参数 | `--site` | 显式切换站点 |

环境变量仍兼容，但优先推荐使用 `ship login` 写入配置。

## Examples

```bash
ship login --site aidirs.org
ship submit https://example.com --site aidirs.org
ship fetch https://example.com --site backlinkdirs.com --json
ship version --latest
ship self-update
```
