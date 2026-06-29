# 豆包网页端登录与自动化参考

## 豆包网址

| 平台 | 网址 |
|------|------|
| 豆包网页版（推荐） | https://www.doubao.com/ |
| 豆包视频生成 | https://www.doubao.com/video-generator |

---

## 浏览器打开方式

### 方式一：OpenCLI Browser Bridge（推荐）

前提：已安装 OpenCLI + Browser Bridge 扩展（Chrome 应用商店）

```bash
# 打开豆包
opencli browser doubao open "https://www.doubao.com/"

# 查看页面状态（交互元素索引）
opencli browser doubao state

# 截图
opencli browser doubao screenshot <path>

# 点击某元素（用 state 输出的索引号）
opencli browser doubao click <index>

# 输入文字
opencli browser doubao type <index> "输入内容"

# 上传文件（如参考图片）
opencli browser doubao upload <index> /path/to/image.jpg
```

### 方式二：Playwright CDP（豆包自动化技能）

使用已安装的 `doubao-automation` 技能：

```bash
node ~/.workbuddy/skills/doubao-automation/scripts/doubao-automation.js \
  --action chat \
  --message "帮我生成一段关于...的视频"
```

支持的操作：`chat` / `generate-image` / `generate-video` / `image-to-video` / `download-last`

### 方式三：持久化 Chrome/Edge 用户数据

用 Playwright 启动带用户数据目录的浏览器，登录态会长期保存：

```javascript
const { chromium } = require('playwright-core');

// Chrome
const context = await chromium.launchPersistentContext(
  'C:\\Users\\Owner\\workbuddy-chrome-profile',
  { channel: 'chrome', headless: false }
);

// Edge
const context = await chromium.launchPersistentContext(
  'C:\\Users\\Owner\\workbuddy-edge-profile',
  { executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', headless: false }
);
```

---

## 登录方式

### 手机号登录（推荐）
1. 打开 https://www.doubao.com/
2. 点击右上角「登录 / 注册」
3. 选择「手机号登录」
4. 输入手机号 → 获取验证码 → 填入验证码

### 微信 / 抖音账号登录
1. 打开 https://www.doubao.com/
2. 点击右上角「登录 / 注册」
3. 选择「微信登录」或「抖音登录」
4. 用对应 App 扫码授权

### 登录态保持
- 登录成功后，Cookie 保存在浏览器中
- 使用同一浏览器会话（不清除 Cookie），登录态长期有效
- 建议用持久化用户数据目录（方式三），避免每次重新登录

---

## 视频生成页面操作指引

### 页面元素参考（豆包网页版）

| 功能 | 选择器参考 | 说明 |
|------|--------------|------|
| 视频生成入口 | `button:has-text("视频生成")` | 左侧菜单 |
| 提示词输入框 | `textarea` 或 `[placeholder*="描述"]` | 输入视频描述 |
| 生成比例选择 | `[class*="ratio"]` 或按钮组 | 16:9 或 9:16 |
| 开始生成按钮 | `button:has-text("生成")` | 提交生成请求 |
| 视频容器 | `[class*="video"]` | 生成后的视频区域 |
| 下载按钮 | `button:has-text("下载")` | 下载生成的视频 |

> **注意**：豆包页面是 React SPA，DOM 结构可能变化。建议每次用 `opencli browser doubao state` 或 Playwright `page.locator(...)` 动态查找元素。

---

## 常见问题

**Q：登录时收不到验证码？**
A：检查手机号是否正确，或切换至微信/抖音登录方式。

**Q：视频生成失败？**
A：豆包每日有生成次数限制（约 10 条视频）。如遇限制，等待次日或切换账号。

**Q：下载的视频画质不满意？**
A：豆包生成的视频分辨率为 720p 左右。如需更高质量，使用多模态云端生成（支持 1080p）。

**Q： browser 自动化点击无反应？**
A：React 页面可能需要 `force: true` 选项，或先用 `hover` 再 `click`。OpenCLI 的 `click` 命令支持 `--force` 选项。
