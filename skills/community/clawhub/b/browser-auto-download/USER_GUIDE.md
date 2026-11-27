# Browser Auto Download v1.0.6 - 用户快速指南

> 响应语言：请使用用户所用的语言。本文档中英双语，不强制单一语言。
> Respond in the user's language; this guide is bilingual.

## ⚠️ 安全须知 / Safety Notice

- **下载内容一律视为不可信。** 本技能不扫描、不签名、不沙箱化文件。打开或安装前，请核对发布方签名或 SHA-256。
- **优先使用独立输出目录。** 默认写入 `~/Downloads/browser-auto-download`，可用 `--output` 指定更隔离的目录。
- **可执行文件默认被拦截。** 保存 `.exe`、`.msi`、`.dmg` 等需要 `--sha256 <摘要>` 或显式 `--acknowledge-executable`。
- **默认只允许同站导航。** 跨站目标需加 `--allow-external-hosts`，请先确认打印出的 URL。
- **调试产物可能含敏感信息。** `--debug` 会保存截图、HTML 和文本，可能包含凭据或个人信息；脱敏仅为尽力而为，用后请删除。

Do not point this skill at authenticated or private pages you are not authorized
to automate.

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt   # 固定 playwright==1.65.0
playwright install chromium
```

### 基本使用
```bash
# 自动检测模式
python scripts/auto_download.py --url "https://example.com/download"

# 使用预设快捷方式
python scripts/auto_download.py --eclipse    # Eclipse IDE
python scripts/auto_download.py --golang     # Golang
python scripts/auto_download.py --wechat     # 微信开发者工具
```

## 📊 版本要点

### v1.0.6 安全加固
- ✅ 依赖固定为 `playwright==1.65.0`
- ✅ 浏览器层拦截跨站文档请求与重定向，点击无法绕过同站限制
- ✅ 最终下载 URL 跨站时直接拒绝并删除文件
- ✅ 默认仅允许同站导航，跨站需 `--allow-external-hosts`
- ✅ 页面提供的文件名会被净化，无法逃逸输出目录
- ✅ 可执行文件需 `--sha256` 或 `--acknowledge-executable`
- ✅ 每次下载输出 SHA-256 摘要
- ✅ 调试产物尽力脱敏，并写入提示文件
- ✅ 清单声明 network / filesystem / browser / process 权限

### v5.0.0 性能提升
- ✅ 成功率提升 50%（~60% → ~90%）
- ✅ 增强的等待时间优化
- ✅ 更好的 JavaScript 渲染处理

### 调试模式（注意敏感信息）
```bash
# 启用调试模式（保存截图和HTML）
python scripts/auto_download.py --url "URL" --debug
```

调试产物可能包含会话状态、凭据或个人信息，脱敏并不保证彻底。查看后请删除
`Downloads/browser-auto-download/browser-auto-download-debug/`。

## 📖 完整文档

- **README.md** - 完整功能说明和示例
- **CHANGELOG.md** - 版本历史
- **QUICKSTART.md** - 快速参考指南
- **CONTRIBUTING.md** - 贡献指南

## 💡 使用建议

### 最佳实践
1. **优先使用直接下载链接**（如果有）
2. **遇到问题时使用调试模式**
3. **复杂页面可增加等待时间**

### 示例代码
```python
from scripts.auto_download import auto_download

# 基本使用
result = auto_download(
    url="https://example.com/download",
    headless=False  # 可见模式（便于调试）
)

if result:
    print(f"下载成功: {result['path']}")
    print(f"文件大小: {result['size_mb']:.1f} MB")
```

## 🆘 获取帮助

```bash
# 查看所有选项
python scripts/auto_download.py --help
```

## 📞 支持

- **问题反馈**: https://github.com/openclaw/browser-auto-download/issues
- **Discord**: https://discord.gg/clawd
- **ClawHub**: https://clawhub.com/skills/browser-auto-download

---

**版本**: 1.0.6 | **发布日期**: 2026-11-27 | **状态**: ✅ 生产就绪（含安全加固）
