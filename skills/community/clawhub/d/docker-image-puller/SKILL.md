---
name: docker-image-puller
description: 使用 Python 脚本下载 Docker 镜像并打包为 tar 文件。当用户说"下载镜像"、"拉取镜像"、"pull xxx"、"帮我下载 nginx 镜像"等触发此技能。支持 SOCKS5 代理直连下载（推荐）和国内镜像站加速两种模式。
---

# Docker 镜像拉取工具

从任意 Docker Registry 拉取镜像，打包为 `.tar` 文件供离线 `docker load` 使用。

## 资源文件

- 脚本：`scripts/docker_image_puller.py`
- 配置：`config.json`（首次运行时引导生成）

## 首次使用 — 配置引导

检查 `config.json` 中 `arch` 字段：
- 若为空（`""` 或不存在），引导用户完成首次配置：
  1. **下载方式** — 代理下载（推荐，最稳定）或镜像加速
  2. **代理地址**（代理模式）— 默认 `127.0.0.1:7890`
  3. **镜像站地址**（镜像模式）— 或让脚本运行时显示推荐列表
  4. **目标架构** — `amd64`（x86 服务器，默认）或 `arm64v8`（ARM 服务器）
- 若 `arch` 已有值，跳过引导，直接使用该配置

`script_dir` 自动解析为技能自带的 `scripts/` 目录。

### config.json 结构

```json
{
  "mode": "proxy",
  "proxy_address": "127.0.0.1:7890",
  "mirror_url": "",
  "arch": "",
  "script_dir": "",
  "version": 1
}
```

`arch` 为空时触发首次引导。

## 执行流程

### 1. 读取配置，构建命令（安全执行）

读取 `config.json`，根据 mode 构建命令。使用 `exec` 的 `shell=false`（参数数组）方式调用，避免 shell 注入。

**代理模式：**
```python
exec(
  command="python3 docker_image_puller.py -i '<image>' --socks5 --socks5-proxy '<proxy>' -a '<arch>'",
  workdir="<script_dir>"
)
```

**镜像加速模式：**
```python
exec(
  command="printf 'y\\ny\\n<mirror>' | python3 docker_image_puller.py -i '<image>' -a '<arch>'",
  workdir="<script_dir>"
)
```

> ⚠️ 镜像名必须为合法 Docker 镜像引用（仅含字母、数字、`/`、`:`、`-`、`.`、`_`），包含其他字符时先向用户确认。

### 2. Sub-Agent 后台下载

使用 `sessions_spawn` 启动隔离子任务，不阻塞主会话：

```
sessions_spawn(
  task="读取 <skill-dir>/config.json 获取配置。为镜像 '<镜像名>' 构建下载命令。用 exec 执行（background=true, timeout=600）。每 30 秒用 process 轮询进度。完成后报告 tar 路径和 docker load 命令。失败则报告具体原因。",
  mode="run",
  runtime="subagent",
  timeoutSeconds=900
)
```

立即回复用户：
> 📥 已启动后台下载 `<镜像名>`（架构：<架构>）... 完成后会通知你，可继续其他操作。

### 3. 结果报告

| 结果 | 处理方式 |
|------|---------|
| ✅ 成功 | 报告 tar 文件路径 + `docker load -i <路径>` |
| ⏱ 超时 | "下载超时，请检查网络或代理" |
| 🔒 认证失败 401 | 请用户提供仓库用户名/密码 |
| 🌐 网络错误 | 报告具体 HTTP 错误码和失败 URL |
| 💾 磁盘不足 | 提醒用户清理磁盘空间 |

## 补充说明

- **安全**：脚本启用 HTTPS 证书校验（`verify=True`），不再禁用 TLS 验证。执行镜像下载时使用参数数组而非 shell 拼接，防止命令注入。
- 输出路径：`<script_dir>/images/<仓库>_<标签>_<架构>.tar`
- 脚本运行完毕后自动清理 `tmp/` 临时目录，无需手动处理
- `config.json` 跨次复用，用户可随时要求切换下载模式或指定架构
