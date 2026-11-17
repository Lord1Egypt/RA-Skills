# AstraFlow Agent Sandbox & UHost 架构与 API 速查

## 1. 产品边界说明

| 维度 | AstraFlow Agent Sandbox（云沙箱） | UCloud UHost（云主机/云服务器） |
|---|---|---|
| **定位** | 面向 AI Agent、临时代码运行、自动化测试的轻量级弹性环境 | 长期持有的完整云服务器（ECS） |
| **SDK / 管理** | `ucloud-sandbox`（Python SDK）+ `ucloud-sandbox-cli` | `ucloud` 官方 CLI（`ucloud uhost ...`） |
| **操作系统** | Ubuntu 22.04 LTS（仅 Linux 容器，无 Windows 模板） | 原生 Windows 2022/2019/2016、CentOS、Ubuntu、Debian |
| **公网网络** | 平台各地域共享出口网关（例如 `us-ca` 为洛杉矶数据中心出口；具体 IP 属性以实际观测和平台返回为准） | 可按产品与账号能力绑定 EIP；线路类型和 IP 属性以 UCloud 返回结果为准 |
| **计费与生命周期** | 单实例最大存活 24 小时，适合分钟/小时级任务 | 按小时（Dynamic）或按月/年，支持长期持续运行 |

## 2. 方案对比：如何实现「星图 + 美国沙箱 + 指定出口」？

目前业内与平台支持的实现路径主要有以下 3 种方式，各有优劣：

### 方案 A：沙箱内配置用户提供的浏览器代理（最简单、最快）
在创建沙箱时，通过 `--proxy` 参数将用户提供的代理配置给 Chrome 进程：
```bash
python3 /path/to/astraflow-remote-lab/scripts/manage_sandbox.py create \
  --region us-ca \
  --proxy "socks5://USER:PASSWORD@PROXY_HOST:PORT"
```
- **说明**：Chrome 流量可按需经用户提供的代理转发；不要据此断言代理是住宅 IP，也不要把代理凭据写入聊天、命令历史或日志。noVNC 路由不由该参数改变。

### 方案 B：沙箱 Web VNC 桥接 Windows 2022 UHost（免客户端，全套 Windows 环境）
用独立 Windows 2022 云主机打底，沙箱通过内网或公网 RDP 全屏拉起并输出 Web VNC：
- **核心优势**：环境完全是 Windows Server 2022；公网 IP、线路类型和可达性以 UCloud 实际返回及连通性验证为准；不应把“国际”“精品”或“原生”当作未经验证的结论；
- **成本与复杂度**：需要维护一台独立 UHost。

### 方案 C：沙箱内启动 WireGuard / Tailscale 节点（全局透明代理）
在沙箱内部安装 WireGuard 接入用户可控的网络节点：
- **核心优势**：沙箱全机命令行、DNS 和浏览器可按配置走节点；
- **成本与复杂度**：需要自行配置节点、路由和安全策略，且不代表节点具有住宅属性。

---

## 3. 常见实操坑点与经验

1. **Linux 进程名截断 (15 字符)**：
   `xfce4-screensaver` 在进程表中被截断为 `xfce4-screensav`。使用 `pkill -x xfce4-screensaver` 无法命中，必须使用 `pkill -f` 或脚本内匹配。
2. **多行脚本引号转义**：
   在 SDK 的 `commands.run()` 中拼接多行脚本容易因 shell 嵌套导致引号报错。最稳妥方案为 base64 编码投递到 `/home/user/` 后通过 bash 执行。
3. **HTTP 反向代理 ≠ TCP 转发**：
   沙箱的 `get_url(5900)` 是 HTTP(S) 网关，原生 VNC 客户端无法直连，必须通过 `websockify` 将 5900 端口包成 6080 WebSocket 端口。
4. **时区自洽**：
   沙箱默认系统时区为 `Etc/UTC`。切到 `us-ca` 地域时，需将系统 `/etc/localtime` 软链接至 `/usr/share/zoneinfo/America/Los_Angeles`，且已启动的浏览器进程需重启以加载新时区。
