# Browser Opener Skill

一个跨平台的浏览器打开技能，支持多种浏览器（Chrome、Firefox、Edge、Safari）和URL启动功能。

## 功能特性

- 🌐 **跨平台支持**：Windows、macOS、Linux
- 🦴 **多浏览器支持**：Chrome、Firefox、Edge、Safari
- 🔗 **URL启动**：打开指定URL
- 🚪 **新窗口**：在新窗口中打开
- 👻 **隐私模式**：无痕/隐私浏览模式
- 🤖 **无头模式**：无GUI模式（用于测试）
- 🛡️ **错误处理**：全面的错误处理机制

## 安装和使用

### 1. 安装依赖

```bash
pip install webbrowser subprocess argparse
```

### 2. 基本使用

```bash
# 使用默认浏览器打开URL
python scripts/open_browser.py --url https://www.google.com

# 使用Chrome打开URL
python scripts/open_browser.py --url https://www.google.com --browser chrome

# 使用Firefox打开URL
python scripts/open_browser.py --url https://www.google.com --browser firefox

# 使用Edge打开URL
python scripts/open_browser.py --url https://www.google.com --browser edge
```

### 3. 高级选项

```bash
# 在新窗口中打开
python scripts/open_browser.py --url https://www.google.com --new-window

# 使用隐私模式
python scripts/open_browser.py --url https://www.google.com --incognito

# 使用无头模式
python scripts/open_browser.py --url https://www.google.com --headless

# 组合使用
python scripts/open_browser.py --url https://www.google.com --browser chrome --new-window --incognito
```

## 支持的浏览器

| 浏览器 | Windows | macOS | Linux | 命令 |
|--------|---------|-------|-------|------|
| Chrome | ✅ | ✅ | ✅ | `--browser chrome` |
| Firefox | ✅ | ✅ | ✅ | `--browser firefox` |
| Edge | ✅ | ✅ | ✅ | `--browser edge` |
| Safari | ❌ | ✅ | ❌ | `--browser safari` |

## Python API

```python
from scripts.open_browser import BrowserOpener

# 创建浏览器打开器实例
opener = BrowserOpener()

# 使用默认浏览器打开URL
opener.open_url("https://www.google.com")

# 使用指定浏览器打开URL
opener.open_url("https://www.google.com", browser_name="chrome")

# 使用隐私模式打开
opener.open_url("https://www.google.com", browser_name="firefox", incognito=True)

# 在新窗口中打开
opener.open_url("https://www.google.com", browser_name="edge", new_window=True)

# 使用无头模式
opener.open_url("https://www.google.com", browser_name="chrome", headless=True)
```

## 示例代码

查看 `examples/` 目录获取更多示例：

- `basic_usage.py` - 基本使用示例
- `batch_opening.py` - 批量打开URL示例
- `error_handling.py` - 错误处理示例

## 命令行选项

| 选项 | 描述 | 必需 | 默认值 |
|------|------|------|--------|
| `--url` | 要打开的URL | 是 | 无 |
| `--browser` | 使用的浏览器 | 否 | `default` |
| `--new-window` | 在新窗口中打开 | 否 | False |
| `--incognito` | 使用隐私模式 | 否 | False |
| `--headless` | 使用无头模式 | 否 | False |

## 浏览器特定选项

### Chrome
- `--incognito`: 无痕模式
- `--headless`: 无头模式
- `--new-window`: 新窗口
- `--disable-gpu`: 禁用GPU加速

### Firefox
- `--private-window`: 私有浏览模式
- `--headless`: 无头模式
- `--new-window`: 新窗口

### Edge
- `--inprivate`: InPrivate模式
- `--headless`: 无头模式
- `--new-window`: 新窗口

### Safari
- `--new-window`: 新窗口
- 注意：Safari不支持命令行无痕或无头模式

## 错误处理

脚本包含全面的错误处理：

- **无效URL**：验证URL格式并自动添加https://前缀
- **浏览器未找到**：检查浏览器是否已安装
- **权限问题**：处理权限错误
- **平台特定问题**：处理操作系统特定错误

## 故障排除

1. **浏览器未找到**：确保浏览器已正确安装
2. **权限错误**：确保有足够的权限启动浏览器
3. **URL无法打开**：检查URL格式和网络连接
4. **平台问题**：验证浏览器在您的平台上可用

## 开发

### 项目结构

```
browser-opener-skill/
├── SKILL.md              # 技能定义
├── README.md             # 说明文档
├── scripts/              # 脚本文件
│   └── open_browser.py   # 主要脚本
├── references/           # 参考文档
│   └── browser_support.md # 浏览器支持详情
└── examples/             # 示例代码
    ├── basic_usage.py    # 基本使用示例
    ├── batch_opening.py  # 批量打开示例
    └── error_handling.py # 错误处理示例
```

### 测试

```bash
# 运行基本使用示例
python examples/basic_usage.py

# 运行批量打开示例
python examples/batch_opening.py

# 运行错误处理示例
python examples/error_handling.py
```

## 许可证

MIT License