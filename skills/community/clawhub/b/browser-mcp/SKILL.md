---
name: browser-mcp
description: 使用 Chrome DevTools MCP 协议远程控制 Chrome 浏览器执行网页任务。当用户说"打开网站"、"帮我搜索"、"点进去看看"、"查看详情"、"操作网页"、"打开 ChatGPT/Gemini"等任何需要浏览器自动化执行的任务时触发。支持网站导航、元素交互、表单填写、多步骤跳转、信息提取、SSRF 白名单配置等完整功能。
---

# Chrome DevTools MCP Browser Skill

通过 Chrome DevTools MCP 协议连接浏览器，实现远程网页控制。

---

## 运行环境

### 当前配置
| 项目 | 值 |
|------|------|
| 操作系统 | Windows 11 Pro |
| 宿主软件 | QClaw (OpenClaw) |
| 浏览器 | Chrome (老板已登录的浏览器) |
| 连接方式 | Chrome DevTools MCP (`profile=user`) |

### 架构示意
```
┌─────────────────────────────────────────────────────────┐
│  QClaw / OpenClaw (本机 Windows 11)                     │
│                                                         │
│  browser(action="navigate", profile="user", ...)         │
│           ↓                                            │
│  Chrome DevTools MCP (CDP)                              │
│           ↓                                            │
│  ws://127.0.0.1:9222 (Chrome Remote Debugging)          │
│           ↓                                            │
│  Chrome Browser (老板的 Chrome) ← 直接操控已登录状态     │
└─────────────────────────────────────────────────────────┘
```

---

## 快速入门

### 1. 启动浏览器
```
browser(action="start", profile="user")
```

### 2. 打开网站
```
browser(action="navigate", profile="user", url="https://example.com")
```

### 3. 获取页面快照
```
browser(action="snapshot", profile="user", refs="aria")
```

### 4. 操作元素
```
browser(action="act", profile="user", ref="ref_id", kind="click")   // 点击
browser(action="act", profile="user", ref="ref_id", kind="type", text="内容")  // 输入
```

---

## 核心工作流

### 标准流程
```
启动浏览器 → 导航网址 → 获取快照 → 分析内容 → 操作元素 → 等待加载 → 循环重复
```

### 多步骤任务流程
```
1. browser(action="navigate", url="目标网址")
2. browser(action="snapshot", refs="aria")  ← 每次操作前必做
3. 分析快照中的 ref，找到目标元素
4. browser(action="act", kind="click/type/press", ref="xxx", ...)
5. browser(action="act", kind="wait", timeMs=2000)  // 等待加载
6. 返回步骤2，循环直到任务完成
```

---

## 完整 Action 速查

### 导航与控制
| Action | 说明 | 示例 |
|--------|------|------|
| `start` | 启动浏览器 | `browser(action="start", profile="user")` |
| `navigate` | 打开网址 | `browser(action="navigate", profile="user", url="...")` |
| `snapshot` | 获取页面快照 | `browser(action="snapshot", profile="user", refs="aria")` |
| `screenshot` | 截图 | `browser(action="screenshot", profile="user")` |
| `status` | 查看浏览器状态 | `browser(action="status", profile="user")` |
| `stop` | 关闭浏览器 | `browser(action="stop", profile="user")` |

### 元素操作
| Kind | 说明 | 参数 |
|------|------|------|
| `click` | 点击元素 | `ref="xxx"` |
| `type` | 输入文本 | `ref="xxx", text="内容"` |
| `press` | 按键 | `key="Enter"/"Escape"/"ArrowDown"/"ArrowUp"` |
| `select` | 下拉选择 | `ref="xxx", values=["选项"]` |
| `hover` | 悬停 | `ref="xxx"` |
| `wait` | 等待加载 | `timeMs=2000` |
| `scroll` | 滚动 | `width=0, height=500` |
| `close` | 关闭标签页 | - |

### 特殊操作
| 操作 | 代码 |
|------|------|
| 粘贴文本 | `browser(action="act", kind="press", key="Control+v")` |
| 全选 | `browser(action="act", kind="press", key="Control+a")` |
| 后退 | `browser(action="act", kind="press", key="Alt+ArrowLeft")` |
| Ctrl+点击新标签打开 | `browser(action="act", ref="xxx", kind="click", modifiers=["Control"])` |

---

## 常用 ref 模式

| 场景 | 方式 |
|------|------|
| 搜索框输入 | `browser(action="act", ref="搜索框ref", kind="type", text="关键词")` |
| 点击搜索/提交按钮 | `browser(action="act", ref="按钮ref", kind="click")` |
| 回车提交 | `browser(action="act", kind="press", key="Enter")` |
| ESC返回/关闭弹窗 | `browser(action="act", kind="press", key="Escape")` |
| 滚动浏览 | `browser(action="act", kind="scroll", height=800)` |
| 等待加载 | `browser(action="act", kind="wait", timeMs=3000)` |

---

## 实战模板

### 模板1：搜索任务
```
1. navigate → 打开搜索引擎（百度/Google）
2. snapshot → 找到搜索框 ref
3. type → 输入搜索关键词
4. press Enter → 提交搜索
5. wait 2s → 等待结果加载
6. snapshot → 查看搜索结果
7. click → 点击目标链接
```

### 模板2：登录后操作
```
1. navigate → 打开目标网站（已登录状态）
2. snapshot → 确认已登录
3. 执行后续操作...
```

### 模板3：多页面深入
```
1. navigate → 打开列表页
2. snapshot → 找到目标条目
3. click → 点进详情
4. wait → 等待加载
5. snapshot → 查看详情内容
6. 重复深入或返回继续
```

### 模板4：表单填写提交
```
1. navigate → 打开表单页
2. snapshot → 获取所有表单项 ref
3. type → 逐项填写（姓名、邮箱等）
4. select → 选择下拉选项
5. click → 提交按钮
6. wait → 等待响应
7. snapshot → 确认提交结果
```

---

## 运行环境配置

### Windows 11 + QClaw（当前）

#### 配置文件路径
`C:\Users\<your-username>\.qclaw\openclaw.json`

#### Chrome 远程调试配置
```json
"browser": {
  "ssrfPolicy": {
    "dangerouslyAllowPrivateNetwork": false,
    "allowedHostnames": [ ... ]
  },
  "profiles": {
    "user": {
      "driver": "existing-session",
      "attachOnly": true,
      "cdpPort": 9222,
      "cdpUrl": "http://127.0.0.1:9222",  // 本地调试端口，不要暴露
      "color": "#00AA00"
    }
  }
}
```

#### Chrome 启动方式
老板的 Chrome 需要开启远程调试：
1. 地址栏输入 `chrome://inspect/#remote-debugging`
2. 勾选 "Discover network targets"
3. 确认显示 `localhost:9222`

#### 启动 Chrome 命令（可选）
如果需要手动启动带调试端口的 Chrome：
```powershell
start chrome.exe --remote-debugging-port=9222
```

---

### Linux/Mac 远程连接 Windows Chrome（未来支持 🚧）

#### 场景说明
当 Agent 运行在 Linux 或 Mac 系统时，需要远程连接到 Windows 11 老板电脑上的 Chrome 浏览器。

#### 架构示意
```
┌──────────────────────────────┐      ┌──────────────────────────────┐
│  Linux / Mac (Agent)         │      │  Windows 11 (老板电脑)        │
│                              │      │                              │
│  QClaw / OpenClaw            │ ←──→ │  Chrome + 远程调试端口        │
│  browser(action=...,          │ CDP  │  chrome.exe --remote-        │
│    cdpUrl="ws://WIN_IP:9222")│      │    debugging-port=9222        │
└──────────────────────────────┘      └──────────────────────────────┘
```

#### Windows 端配置
1. 允许 Chrome 接受外部连接：
   ```powershell
   chrome.exe --remote-debugging-port=9222 --remote-allow-origins=*
   ```

2. 防火墙配置（允许 9222 端口入站）

3. 获取 Windows 电脑的局域网 IP（如 `192.168.1.100`）

#### Agent 端配置
```json
"browser": {
  "profiles": {
    "user": {
      "driver": "remote",
      "cdpUrl": "ws://<your-windows-ip>:9222",  // 替换为实际 IP
      "attachOnly": false,
      "color": "#00AA00"
    }
  }
}
```

#### 注意事项
- ⚠️ 仅在可信网络中使用
- ⚠️ 远程连接时老板的 Chrome 需要保持运行
- ⚠️ 老板电脑需要保持开机状态

---

## SSRF 白名单配置

### 问题现象
```
Blocked: resolves to private/internal/special-use IP address
```

### 解决方案
1. 编辑 `C:\Users\<your-username>\.qclaw\openclaw.json`
2. 找到 `browser.ssrfPolicy.allowedHostnames`
3. 添加目标域名（支持泛域名 `*.example.com`）
4. 重启 OpenClaw：`gateway(action=restart)`

### 当前白名单
```json
"allowedHostnames": [
  "*.chatgpt.com", "*.openai.com", "*.oaistatic.com",
  "*.gemini.google.com", "*.google.com",
  "*.twitter.com", "*.x.com",
  "*.facebook.com", "*.fbcdn.net",
  "*.github.com", "*.githubusercontent.com", "*.githubassets.com",
  "*.npmjs.org", "*.pypi.org", "*.pythonhosted.org",
  "*.cloudflare.com", "*.workers.dev", "*.vercel.app",
  "*.googleapis.com", "*.gstatic.com",
  "*.stackoverflow.com", "*.stackexchange.com"
]
```

---

## 注意事项

### 必须遵守
- **使用 `profile=user`**：连接老板的 Chrome，不是默认 profile
- **操作前先 snapshot**：每次页面变化后都要重新获取快照
- **操作后等待 1-2 秒**：让页面/内容完全加载
- **SSRF 白名单修改后重启**：配置不会自动生效

### 常见问题

| 问题 | 解决方法 |
|------|----------|
| 报错 "Blocked SSRF" | 添加域名到白名单，重启 OpenClaw |
| 点击没反应 | 重新 snapshot，ref 可能已变化 |
| 页面加载慢 | 增加 wait timeMs 值 |
| 浏览器超时 | 重启 OpenClaw 网关 |
| 输入内容丢失 | 使用 `fill` 替代 `type`，或先清空再输入 |

### ref 失效规律
- 页面刷新/导航后 ref 全部失效
- 点击链接跳转后 ref 全部失效
- 滚动不会导致 ref 失效
- 每次操作前都重新 snapshot 是最稳妥的

---

## Chrome 配置检查清单

> 老板的 Chrome 需开启远程调试才能连接：
> 1. 地址栏输入 `chrome://inspect/#remote-debugging`
> 2. 勾选 "Discover network targets"
> 3. 确认显示 `localhost:9222`

---

*最后更新：2026-03-25*
