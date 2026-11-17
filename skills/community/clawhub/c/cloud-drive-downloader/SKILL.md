---
name: cloud-drive-downloader
slug: cloud-drive-downloader
displayName: 网盘通
version: 0.20.2
platforms: [macos, windows, linux]
author: lis
license: CC-BY-NC-SA-4.0
description: "网盘下载调度层；不破解登录/付费/限速。触发词：网盘通、百度网盘、夸克。"
metadata:
  version: "0.20.1"
i18n:
  en: README.en.md
  zh: README.md
locale: zh-CN
locales: [zh-CN, en-US]
---

# 网盘通 · 通用下载调度层

网盘通不是 NAS 专用工具。它是一个跨 macOS / Windows / Linux 的下载调度层：
接收用户提供的链接、磁力、种子或公开搜索关键词，选择本机或远端引擎执行下载。

```
用户链接
  └─→ Agent / MCP / CLI ─┐
  └─→ Web UI ────────────┼─→ pan 调度层 ─→ 本机引擎
  └─→ 浏览器插件 ────────┘             └─→ Docker/远程引擎
```

核心原则：只走**官方网页会话、官方接口、用户在官方网页触发的下载 URL**和通用直链；不破解、不伪造登录态、不绕过验证码/风控/会员/付费/DRM/限速。官方不给直链时安全失败。
插件不读取网页登录态，只投递用户主动提供的链接。需要登录时**只用统一入口** `pan login <网盘> --qr`（百度扫码写 BaiduPCS-Go），禁止临时脚本直连网盘登录接口。用户对下载内容的合法性负全责；平台限制与工具失败如实报告。

## 三类通用入口

| 入口 | 典型用法 | 依赖 |
|---|---|---|
| Agent / MCP / CLI | `pan.py get`、`pan_get`、`pan_get_plan` | Python 3 与所选引擎；无服务模式可直接调 CLI |
| Web UI | 浏览器打开 `http://127.0.0.1:<port>`、`http://<nas>:<port>` 或 `http://<server>:<port>` | `pan serve` |
| 浏览器插件 | 粘贴或右键投递链接到本机 / NAS / 服务器地址 | Chrome 或 Edge 开发者模式加载插件 |

部署形态按需选择：`local` 是默认本机模式；`nas_docker` 和 `server_docker` 只是 Docker 部署模式，不是前置条件。

## 配置优先级

`CLI 参数 > 环境变量 > config.json > 内置默认值`。

示例统一使用占位符：`<api-url>`、`<download-dir>`、`<port>`、`<pan-root>`。

## 三系统用法

三平台入口一致：`python3 <pan-root>/scripts/pan.py download <url> -d <下载目录>`；macOS/Windows 用 venv + `requirements.txt`，Linux 另装 `secret-tool` 存凭据；Web UI 本机 `/login` 登录页与 `/live` 进度页：`http://127.0.0.1:<port>/login`、`http://127.0.0.1:<port>/live`。各系统依赖安装、路径写法、Web UI 与 MCP 接线细节见 `references/44-三系统安装与用法.md`。

## 常用命令

```bash
python3 <pan-root>/scripts/pan.py route "<链接>" --json --brief
python3 <pan-root>/scripts/pan.py auth "<链接>" --json
python3 <pan-root>/scripts/pan.py engines "<链接>" --json
python3 <pan-root>/scripts/pan.py detect "<链接>"
python3 <pan-root>/scripts/pan.py test "<链接>" --pwd <提取码>
python3 <pan-root>/scripts/pan.py get "<链接>" --pwd <码> --dry-run
python3 <pan-root>/scripts/pan.py get "<链接>" --to <download-dir>
python3 <pan-root>/scripts/pan.py serve --host 127.0.0.1 --port <port>
python3 <pan-root>/scripts/pan.py setup --mode local --root <download-dir> --port <port>
```

公开搜索、网页候选、磁力/种子仍只处理用户主动提供的候选或公开源；不解析需登录的分享页，不绕过平台限制。

## 部署模式

```bash
# 本机模式（默认）
python3 <pan-root>/scripts/pan.py setup --mode local --root <download-dir> --port <port>

# NAS 或服务器 Docker（可选）
python3 <pan-root>/scripts/pan.py docker --out ./pan-docker
cd ./pan-docker && bash install.sh
# Web UI：http://<nas>:<port> 或 http://<server>:<port>
```

远程 SSH/存储模式见 `references/21-远程NAS与私有存储.md`；Docker 详情见 `references/33-Docker部署与一键搜索.md`。

## Agent / MCP

无服务模式：Agent 直接调用 `<pan-root>/scripts/pan.py`，不启动 Web UI。推荐先 `get --dry-run --json`，核对缺失项后再实际下载。

MCP 工具：

- `pan_get`：执行下载，默认 `dry_run=true`。
- `pan_task`：查看或控制任务。
- `pan_get_plan`：只读生成下载计划，不读取凭据明文。

通用 MCP 客户端配置（stdio）：

```json
{
  "mcpServers": {
    "pan-cloud-drive": {
      "command": "python3",
      "args": ["<pan-root>/scripts/pan_mcp.py"]
    }
  }
}
```

Codex 配置：

```toml
[mcp_servers.pan-cloud-drive]
command = "python3"
args = ["<pan-root>/scripts/pan_mcp.py"]
enabled = true
```

## 凭据与合规

- 密码、Cookie、Token 只允许通过系统凭据库保存：macOS Keychain / Windows Credential Manager / Linux secret-tool。
- 配置只保存 `credential:名称` 引用；不在聊天、命令行、日志、config.json 明文保存。
- 不绕过验证码、风控、限速、会员鉴权；不做危险删除；用户对下载内容的版权与授权负责。
- 网页/爬虫/搜索候选在下载前请自行确认有权访问；`--assume-own` 用于你确已获得授权的场景。

## 代码结构

`scripts/pan.py`（CLI 入口）、`scripts/pan_mcp.py`（MCP）、`agents/`、`docker/`、`extensions/`、`references/`（40+ 分网盘与部署文档）。详细目录树、模块职责与依赖见 `references/43-代码结构与目录.md`。

## 单实例与续传安全（v0.16.0 硬规则）

2026-10-15 实测教训：同来源起多个下载进程会互相抢带宽/覆盖断点，表现为"跑了很久没进展"。

- **同一 `(drive, source, target)` 只允许一个下载进程**；计划步骤/官方网页路径带锁，抢不到直接退出码 `9`。
  查看/清理：`pan guard status`、`pan guard clean`。
- **续传一律禁止 `--ow`**：会让已下分片从头重下；计划构建阶段自动剥离（含 config 里写死的）。
- **后台常驻用双 fork**：`pan guard daemon --cmd '...' --log <日志>`，不要用 `nohup ... &`。
- **限速如实报告、不混同登录失败**：`pan guard speed --target <目录>` 采样；低于 200 KB/s 判定为
  网盘侧限速/免费账号特征，输出明确提示，不破解限速。`pan guard eta` 换算剩余时间。
- **错误分类**：`pan guard error --text '<原始错误>'` → login_required / dlink_missing / captcha /
  risk_control / http_403 / not_found / disk_full / throttle，并给处置建议。
- **扫码稳定**：百度只走 `pan login baidu --qr`；每次生成时间戳+随机后缀的唯一二维码文件，避免扫到缓存旧码。

详见 `references/39-单实例与续传安全.md`。

## 测试

```bash
python3 <pan-root>/scripts/self_test.py
python3 <pan-root>/scripts/pan.py docker check --json
```

## 支持边界

- 已登记网盘与四类非百度路由（官方网页会话桥/浏览器直链桥/AList/OAuth-WebDAV）见 `references/40-网盘支持矩阵.md`。
- 各盘真机验证的最小授权方式见 `references/41-真机验证权限清单.md`；未授权前对应盘标记「待用户提供」，不虚报真机结果。
- 未登记盘名一律标“不支持/需接入”，不得当作 HTTP 直链抓取分享页；接入流程见 `references/06-扩展新网盘.md`。
- 非会员提速的诚实路径（换赛道 123 云盘/夸克/PikPak 离线 + 自动分片 + 闲时队列）见 `references/42-换赛道提速指南.md`；v0.20.0 起 http 直链单连接被限自动切分片，`pan idle` 提供闲时队列与守护。

## 权限边界

- 公司数据上云、删除原始资料、未授权系统级配置变更仍需用户确认。
- 本 Skill 只做下载能力调度，不替代专业判定，不新增解析分享页或绕过平台限制能力。
