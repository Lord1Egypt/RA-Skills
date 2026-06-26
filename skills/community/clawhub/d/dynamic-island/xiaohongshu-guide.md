# OpenClaw 灵动岛 — 让你的 Mac 也有灵动岛！

实时显示多个 AI Agent 工作状态，思考中、执行工具、搞定了... 一眼看清楚。完成任务还会晃一下 + 音效提示，超有灵性！

已开源，3步就能跑起来

---

## 它长什么样？

屏幕最上方正中间，一颗半透明毛玻璃药丸，悬浮在所有窗口之上。

5种状态自动切换，使用 emolog 可爱图标：

| 状态 | 说明 |
|------|------|
| 待命/休眠 | 没连上或等待任务 |
| 收到消息 | 有人@它了 |
| 思考中 | 正在干活 |
| 搞定了 | 任务完成（药丸晃动 + 玻璃音效！） |
| 出错了 | 出问题了（低音提示） |

---

## 多 Agent 支持

- 同时管理多个 Agent，每个显示各自的状态和名字
- **鼠标悬停自动展开**，看到所有 Agent 列表
- 每个 Agent 显示最近 2 条对话消息
- **光标跟随高亮**，移到哪个 Agent 哪个就亮
- 点击 Agent 名字直接跳转飞书聊天
- 待命时紧凑显示：emoji 左侧 + Agent 数量右侧

---

## 安装步骤

**前置条件：**
- macOS 13 以上
- 装了 Xcode Command Line Tools（终端输 `xcode-select --install`）
- Python 3.9+

**第一步：下载项目**

打开终端，粘贴：

```bash
git clone https://github.com/zhixiangshon-cell/openclaw-dynamic-island.git
cd openclaw-dynamic-island
```

**第二步：装依赖**

```bash
pip3 install websockets
```

**第三步：配置**

```bash
cp config.example.json config.json
```

然后用任意编辑器打开 config.json，改两个地方：`agent_names` 和 `agent_links`

怎么找你的 agent 文件夹名？终端输入：

```bash
ls ~/.openclaw/agents/
```

会列出你所有的 agent，比如：

```
main
feishu-dm
my-group-chat
```

把这些名字填到 config.json 里，给每个取个好认的名字：

```json
{
  "agents_dir": "~/.openclaw/agents",
  "http_port": 7788,
  "ws_port": 7789,
  "agent_names": {
    "main": "主力",
    "feishu-dm": "小秘书",
    "my-group-chat": "团队群"
  },
  "agent_links": {
    "feishu-dm": "lark://applink.feishu.cn/client/chat/open?openId=xxx"
  }
}
```

- 左边 = 文件夹名（不要改），右边 = 灵动岛上显示的名字（随便取）
- `agent_links` 配了就能点击跳转飞书聊天（可选）
- 只有一个 agent？那就只写一行
- 不配名字也能用，灵动岛就只显示状态不显示名字

**第四步：启动！**

```bash
./start.sh
```

灵动岛就出现在屏幕顶部了！

停止：`./start.sh stop`
重启：`./start.sh restart`

---

## 想开机自动启动？

终端执行两行命令：

```bash
sed "s|__INSTALL_DIR__|$(pwd)|g" com.openclaw.face.plist > ~/Library/LaunchAgents/com.openclaw.face.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.face.plist
```

以后每次开机，灵动岛自动出现。

不想要了？卸载也是两行：

```bash
launchctl unload ~/Library/LaunchAgents/com.openclaw.face.plist
rm ~/Library/LaunchAgents/com.openclaw.face.plist
```

---

## 多 Agent 效果

配了多个 agent 名字后，灵动岛会自动区分：

- 思考中 · 小秘书  ← 私聊 agent 在干活
- 收到消息 · 团队群  ← 群聊 agent 收到新消息
- 搞定了 · 主力      ← 主 agent 完成任务（药丸晃动！）

鼠标悬停展开后，还能看到每个 Agent 最近的对话内容。

---

## 原理简单说

- `server.py` 监控 Agent 的会话日志文件，检测到状态变化就通过 WebSocket 推送
- `widget.swift` 用 macOS 原生 NSPanel 画了一个毛玻璃药丸窗口，支持 hover 检测
- 里面嵌了一个透明 WebView 渲染 emolog 图标和多 Agent 状态
- 完成任务时 JS 通知 Swift 晃动窗口 + 播放音效

---

## 项目地址

https://github.com/zhixiangshon-cell/openclaw-dynamic-island

觉得有用的话给个 Star 吧！有问题直接提 Issue。
