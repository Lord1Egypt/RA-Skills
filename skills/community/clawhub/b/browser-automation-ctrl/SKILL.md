# Browser Control Skill

浏览器控制工具 - 通过 Selenium 实现浏览器自动化控制。

## 功能列表 (35+ 命令)

### 基础操作
| 命令 | 说明 |
|------|------|
| `open <url>` | 打开网页 |
| `screenshot` | 网页截图 |
| `screenshotb64` | 网页截图(base64) |
| `fullscreen` | 全页面截图 |
| `js <script>` | 执行 JavaScript |
| `cookies` | 获取 Cookies |
| `setcookie <name> <value>` | 设置 Cookie |
| `clearcookies` | 清除 Cookies |
| `source` | 获取页面源码 |
| `title` | 获取标题 |
| `url` | 获取当前 URL |

### 元素操作
| 命令 | 说明 |
|------|------|
| `find <selector>` | 查找元素 |
| `click <selector>` | 点击元素 |
| `fill <selector> <text>` | 填写输入框 |
| `submit <selector>` | 提交表单 |
| `hover <selector>` | 悬停 |
| `attr <selector> <name>` | 获取元素属性 |

### 导航操作
| 命令 | 说明 |
|------|------|
| `back` | 后退 |
| `forward` | 前进 |
| `refresh` | 刷新 |
| `wait <seconds>` | 等待 |
| `scroll [x] [y]` | 滚动页面 |
| `scrollto <selector>` | 滚动到元素 |
| `waitelem <selector>` | 等待元素出现 |

### 标签页操作
| 命令 | 说明 |
|------|------|
| `newtab <url>` | 新建标签页 |
| `switchtab <index>` | 切换标签页 |
| `closetab` | 关闭标签页 |
| `tabs` | 获取所有标签页 |

### 高级功能
| 命令 | 说明 |
|------|------|
| `links` | 获取所有链接 |
| `images` | 获取所有图片 |
| `size` | 获取页面尺寸 |
| `ua <user-agent>` | 设置 User-Agent |
| `proxy <address>` | 设置代理 |

## 依赖安装

```bash
pip install selenium
```

需要 Chrome 浏览器和 ChromeDriver。

## 使用示例

```bash
# 打开网页并截图
python scripts/browser_ctrl.py open https://www.baidu.com
python scripts/browser_ctrl.py screenshot

# 查找元素并填写
python scripts/browser_ctrl.py find "#kw"
python scripts/browser_ctrl.py fill "#kw" "搜索内容"
python scripts/browser_ctrl.py click "#su"

# 获取页面所有链接
python scripts/browser_ctrl.py links

# 设置代理
python scripts/browser_ctrl.py proxy "http://127.0.0.1:8080"

# 设置 User-Agent
python scripts/browser_ctrl.py ua "Mozilla/5.0..."
```

## 触发关键词

- "打开网页"、"浏览器"
- "网页截图"
- "执行 JS"
- "点击"、"填写"
- "前进"、"后退"
- "获取链接"、"获取图片"
- "设置代理"

## 注意事项

- 需要安装 Chrome 浏览器
- 需要 chromedriver 与 Chrome 版本匹配
- 无头模式运行（不显示浏览器窗口）
- 截图保存在 ~/Pictures/OpenClaw/
- 支持 CSS 选择器和 XPath
