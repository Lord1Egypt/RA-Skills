---
name: canvas-connector
description: 把本机 LobsterAI 接入「无限画布」平台。首次下载连接器、启动本地服务，并生成"打开即自动连接"的画布链接；本地模式不限次数。
---

# 画布连接器（Infinite Canvas Connector）

把用户电脑上的 LobsterAI 接入画布平台，让画布右侧「AI 助手」面板直接使用本机 LobsterAI（本地模式不限次数）。

## 何时使用

- 用户说「连上画布」「连接 XX 画布」「把画布接上」等，或提到「画布连接器」。

## 使用步骤（按顺序）

1. 运行连接信息脚本（需要 Node.js ≥ 20；把用户提供的画布地址用 `--canvas` 传入）：

   ```bash
   node {baseDir}/scripts/connect.mjs --canvas <画布地址，如 https://aicanvas.miaotuntu.com>
   ```

2. 若输出 JSON 中 `needStart` 为 `true`：先按输出里的 `startCommand` 在后台启动连接器（终端命令），等待约 2 秒后**再次运行第 1 步**。
3. 当输出包含 `pageUrl`（形如 `https://…/app/#agentUrl=…&agentToken=…`）时：用浏览器打开它（可直接打开，或把链接给用户点开）——画布会自动填入连接信息并完成连接。
4. 告知用户：连接器已在本机运行，回到画布右侧「AI 助手」面板即可对话（本地模式不消耗云端次数）。
5. 停止连接器（用户要求时）：结束名含 `canvas-agent.mjs` 的 node 进程（例如 `pkill -f canvas-agent.mjs`）。

## 说明

- 连接器默认监听 `http://127.0.0.1:17371`；配置（含 Connect token）在 `~/.infinite-canvas/canvas-agent.json`；
- 重复运行是安全的：已在运行时会直接返回连接信息；
- 连接器文件下载带 **SHA-256 校验**，校验失败会拒绝安装；「打开即连」链接仅对官方画布域名携带令牌，自定义域名需按脚本提示手动填写；
- 云端模式（画布内点「连接云端助手」）无需本技能；
- 本技能不包含任何系统级危险操作，所有命令均由你在对话中按用户意图执行。
