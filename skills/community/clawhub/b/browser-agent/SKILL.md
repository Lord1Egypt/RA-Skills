# browser-agent 技能

## 描述

浏览器自动化 Agent 技能，基于 Chrome DevTools Protocol (CDP) 和 WebSocket 实现 AI 对浏览器的直接控制。支持 OpenClaw 浏览器工具的原生集成，让 AI 能够像人类一样操作浏览器。

## 核心能力

- **CDP 直连** - 通过 WebSocket 连接 Chrome 远程调试端口，绕过安全提示弹窗
- **会话保持** - 复用已登录的浏览器会话（cookie、登录状态、后台权限）
- **多场景自动化** - 支持数据抓取、表单填写、内容发布、跨平台同步等
- **Windows 兼容** - 解决 Windows 平台 Chrome CDP 连接超时问题

## 适用场景

1. **跨平台数据同步** - Notion ↔ 飞书、GitHub star 整理、Analytics 数据查询
2. **内容管理** - 批量删除/发布 Twitter 帖子、管理社交媒体
3. **数据采集** - 抓取网页内容、监控价格变化、收集竞品信息
4. **自动化测试** - UI 测试、流程验证、回归测试

## 使用方法

### 前置条件

**方式 1: 使用 OpenClaw 内置浏览器（推荐）**

OpenClaw 的 browser 工具已自动配置 CDP，无需额外设置：
```python
browser(action="start")  # 自动启动并配置
```

**方式 2: 自行启动 Chrome**

需要添加 `--remote-allow-origins` 标志允许 WebSocket 连接：
```bash
# Windows
chrome.exe --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="C:\chrome-profile"

# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --remote-allow-origins=* \
  --user-data-dir="/tmp/chrome-profile"
```

⚠️ **注意**: Chrome 90+ 版本默认拒绝 WebSocket 连接，必须添加 `--remote-allow-origins=*` 或指定具体 origin。

### 脚本调用

```bash
# 检查浏览器连接
python skills/browser-agent/scripts/browser_agent.py --check

# 执行页面自动化任务
python skills/browser-agent/scripts/browser_agent.py --url "https://example.com" --action "screenshot"

# 执行自定义脚本
python skills/browser-agent/scripts/browser_agent.py --script "my_automation.py"
```

### OpenClaw 浏览器工具集成

```python
# OpenClaw 内置 browser 工具已支持 CDP
browser(action="start")  # 启动浏览器
browser(action="navigate", url="https://x.com")  # 导航
browser(action="snapshot", refs="aria")  # 获取页面快照
browser(action="act", kind="click", ref="e123")  # 点击元素
browser(action="act", kind="type", text="内容")  # 输入文本
```

## 技术架构

```
┌─────────────────┐     WebSocket      ┌─────────────────┐
│   AI Agent      │ ◄────────────────► │  Chrome CDP     │
│  (OpenClaw)     │   CDP Protocol     │  (Port 9222)    │
└─────────────────┘                    └─────────────────┘
        │                                       │
        │                                       ▼
        │                            ┌─────────────────┐
        │                            │   Browser UI    │
        │                            │  (Visible/Headless)
        ▼                            └─────────────────┘
┌─────────────────┐
│  Skill Scripts  │
│  - browser_agent.py  │
│  - cdp_connector.py  │
│  - session_manager.py│
└─────────────────┘
```

## 注意事项

- **安全性**：CDP 端口仅监听 localhost，不要暴露到公网
- **会话超时**：长时间空闲后可能需要重新 allow 连接
- **资源占用**：每个 CDP 会话约占用 50-100MB 内存
- **网站兼容性**：部分网站（如银行、高安全站点）可能阻止自动化

## 故障排查

### 问题：连接超时
```bash
# 检查 Chrome 是否启动
netstat -ano | findstr 9222

# 重启 Chrome 远程调试
taskkill /F /IM chrome.exe
chrome.exe --remote-debugging-port=9222
```

### 问题：安全提示弹窗
- 使用 WebSocket 直连方案（见 `scripts/cdp_connector.py`）
- 或在 Chrome 中手动点击"允许"

### 问题：会话丢失
- 使用 `--user-data-dir` 固定配置文件目录
- 实现会话保持机制（见 `scripts/session_manager.py`）

## 参考资源

- [Chrome DevTools Protocol 文档](https://chromedevtools.github.io/devtools-protocol/)
- [OpenClaw Browser 工具](../../docs/browser.md)
- [PageAgent - 阿里开源项目](https://github.com/alibaba/page-agent)

## 更新日志

- **v1.0** (2026-03-18) - 初始版本
  - CDP WebSocket 直连支持
  - Windows 平台兼容
  - 会话保持机制
  - OpenClaw browser 工具集成
