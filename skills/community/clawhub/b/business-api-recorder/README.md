# Business API Recorder

> 通过Chrome扩展自动拦截浏览器API，分析业务流程并生成完整的AI重构文档。

---

## 📦 Meta Information

| Field | Value |
|-------|-------|
| **Name** | `business-api-recorder` |
| **Version** | `1.0.0` |
| **Description** | 通过Chrome扩展控制浏览器，自动拦截并分析 Web 应用的 API 调用，生成完整的业务文档和接口清单 |
| **Author** | 周坚 `zhoujdev@163.com` |
| **License** | MIT |
| **Homepage** | https://github.com/[your-repo]/business-api-recorder |
| **Keywords** | `api-recorder`, `browser-automation`, `api-documentation`, `business-analysis`, `chrome-extension`, `network-monitoring` |
| **Category** | Developer Tools / API Documentation |

---

## ⚙️ Dependencies

### Required Dependencies

| Dependency | Version | Description |
|------------|---------|-------------|
| OpenClaw CLI | Latest | AI agent orchestration platform - https://docs.openclaw.ai |
| Chrome Extension | Latest | Browser extension for Chrome DevTools Protocol control - https://docs.openclaw.ai/tools/chrome-extension |

### OpenClaw Capabilities

This skill requires the following OpenClaw capabilities:
- `browser` - Control Chrome browser via extension
- `write` - Save analysis results
- `exec` - Run shell commands

---

## 🎯 Use Cases

- ✅ 实时拦截浏览器的 fetch/XMLHttpRequest
- ✅ 记录完整的请求/响应日志
- ✅ 分析业务流程和分支场景
- ✅ 生成 12-chapter implementation document for AI
- ✅ 创建 API inventory and data dictionary
- ✅ Capture data relationships and validation rules

---

## 🚀 Quick Start

### 1. Install OpenClaw

```bash
# Install via official installer
curl -sSL https://install.openclaw.ai | sh

# Or visit https://docs.openclaw.ai for detailed instructions
```

### 2. Install Chrome Extension

```bash
# Install to local machine
openclaw browser extension install

# View extension path
openclaw browser extension path

# Expected output:
# ~/.openclaw/browser-extensions/openclaw-relay/
```

Then in Chrome:
1. Open `chrome://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the extension directory
4. Configure: Port=`18792`, Gateway Token=`<your-OPENCLAW_GATEWAY_TOKEN>`

### 3. Start Recording

Login to your target system in Chrome, click the OpenClaw extension icon (Badge `ON`), then in your OpenClaw agent:

```python
# 1. Check browser connection
browser(action="tabs", profile="chrome")

# 2. Inject monitoring script
browser(action="act", kind="evaluate", profile="chrome", fn="<从 get-monitor.sh 获取的脚本>")

# 3. Execute business operations...

# 4. Export API logs
browser(action="act", kind="evaluate", profile="chrome", fn="JSON.stringify(window.__OPENCLAW_NETWORK_LOG__, null, 2)")

# 5. Generate implementation document (参考 DOCUMENT_TEMPLATE.md)
```

---

## 📁 File Structure

```
business-api-recorder/
├── SKILL.md                    # 使用文档
├── README.md                   # 本文件
├── DOCUMENT_TEMPLATE.md         # AI重构文档模板 (12章节)
├── LICENSE                     # MIT 许可证
└── scripts/
    ├── network-monitor.js      # 网络监控脚本 (核心)
    └── get-monitor.sh          # 获取脚本工具
```

---

## 📄 Preview Output

After completing one business analysis, the following files will be generated:

```
output/
├── [业务功能]-完整实现文档.md      # 主要交付物
├── [业务功能]-api-log.json          # 完整日志
└── [业务功能]-api-report.md         # 简要报告
```

---

## 🔑 Key API Functions

Once the monitoring script is injected, the following functions are available in browser console:

| Function | Description |
|----------|-------------|
| `__openclaw_getNetworkLog()` | 获取完整日志 |
| `__openclaw_getStats()` | 获取统计信息 |
| `__openclaw_clearNetworkLog()` | 清空日志 |

---

## ⚡ Workflow

```
1. 连接浏览器 2. 打开URL 3. 注入监控 4. 分析页面 5. 执行操作 6. 提取日志 7. 生成文档
```

---

## 📚 Documentation

- **详细使用**: `SKILL.md`
- **文档模板**: `DOCUMENT_TEMPLATE.md`
- **OpenClaw文档**: https://docs.openclaw.ai
- **Chrome扩展**: https://docs.openclaw.ai/tools/chrome-extension

---

## 🐛 Troubleshooting

### Badge shows `!`

```bash
# Check Gateway status
openclaw gateway status

# Verify Token matches OPENCLAW_API_TOKEN
openclaw config show
```

### No requests captured

- Confirm monitoring script is injected (console shows "✅ 网络监控已启动")
- Check if requests are made after injection
- Some cross-origin requests may not be fully interceptable

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Submit pull requests

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) file.

---

## 👏 Acknowledgments

- OpenClaw team for the excellent AI orchestration platform
- Chrome DevTools Protocol for browser control capabilities

---

**Author**: 周坚  
**Email**: zhoujdev@163.com