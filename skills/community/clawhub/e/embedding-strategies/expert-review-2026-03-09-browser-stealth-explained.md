# 浏览器伪装与反检测详解

**生成时间：** 2026-03-09 09:12

---

## 🎯 什么是浏览器伪装？

**简单说：** 让自动化脚本看起来像真实用户在操作浏览器，而不是机器人在跑脚本。

---

## 🔍 为什么要伪装？

### 网站如何检测机器人？

网站会通过多种方式判断你是不是真人：

### 1️⃣ 检查自动化标志

**检测点：** `navigator.webdriver`

**机器人：**
```javascript
navigator.webdriver === true  // ❌ 暴露了！
```

**真人：**
```javascript
navigator.webdriver === undefined  // ✅ 正常
```

**伪装方法：**
```javascript
// 启动时隐藏
args: ['--disable-blink-features=AutomationControlled']
```

---

### 2️⃣ 检查 User-Agent

**检测点：** 浏览器标识字符串

**机器人（默认）：**
```
"HeadlessChrome/120.0.0.0"  // ❌ 一看就是机器人
```

**真人：**
```
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"  // ✅ 正常
```

**伪装方法：**
```javascript
userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...'
```

---

### 3️⃣ 检查视口大小

**检测点：** 浏览器窗口尺寸

**机器人：**
```javascript
viewport: { width: 800, height: 600 }  // ❌ 默认尺寸，可疑
```

**真人：**
```javascript
viewport: { width: 1920, height: 1080 }  // ✅ 常见分辨率
```

**伪装方法：**
```javascript
viewport: { width: 1920, height: 1080 }
```

---

### 4️⃣ 检查时区/语言

**检测点：** 系统时区和语言设置

**机器人：**
```javascript
locale: 'en'  // ❌ 只有语言代码
timezoneId: 'UTC'  // ❌ 协调世界时
```

**真人（中国用户）：**
```javascript
locale: 'zh-CN'  // ✅ 简体中文
timezoneId: 'Asia/Shanghai'  // ✅ 上海时区
```

**伪装方法：**
```javascript
locale: 'zh-CN',
timezoneId: 'Asia/Shanghai'
```

---

### 5️⃣ 检查浏览器插件

**检测点：** 已安装的插件列表

**机器人：**
```javascript
navigator.plugins.length === 0  // ❌ 没有插件，可疑
```

**真人：**
```javascript
navigator.plugins.length === 5  // ✅ 有正常插件
```

**伪装方法：** 使用 stealth 插件自动处理

---

### 6️⃣ 检查 Canvas 指纹

**检测点：** Canvas 渲染特征

**原理：** 不同 GPU/驱动渲染的图像有微小差异

**检测代码：**
```javascript
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
ctx.fillText('Hello', 0, 0);
const fingerprint = canvas.toDataURL();  // 唯一指纹
```

**伪装方法：** 使用 stealth 插件添加噪声

---

### 7️⃣ 检查 WebGL 指纹

**检测点：** WebGL 渲染器信息

**检测代码：**
```javascript
const gl = canvas.getContext('webgl');
const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
// 返回："Google SwiftShader"（机器人常见）
```

**真人：**
```
"NVIDIA GeForce RTX 3080"  // 真实显卡
```

---

### 8️⃣ 检查行为模式

**检测点：** 鼠标移动、点击、滚动

**机器人：**
- ❌ 直线移动鼠标
- ❌ 瞬间点击
- ❌ 匀速滚动

**真人：**
- ✅ 曲线移动鼠标
- ✅ 有点击延迟
- ✅ 加速/减速滚动

**伪装方法：**
```javascript
// 模拟真实用户行为
await page.mouse.move(x, y, { steps: 10 });  // 分步移动
await page.click('button', { delay: 100 });  // 延迟点击
```

---

## 🛡️ Playwright 伪装方案

### 基础伪装（手动配置）

```javascript
const { chromium } = require('playwright');

const browser = await chromium.launch({
  headless: true,
  args: [
    '--disable-blink-features=AutomationControlled',
    '--no-sandbox',
  ]
});

const context = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
  viewport: { width: 1920, height: 1080 },
  locale: 'zh-CN',
  timezoneId: 'Asia/Shanghai'
});
```

---

### 高级伪装（stealth 插件）

```javascript
const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth');

// 启用 stealth 模式
chromium.use(stealth());

const browser = await chromium.launch({
  headless: true,
});

const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
});
```

**stealth 插件自动处理：**
- ✅ 隐藏 `navigator.webdriver`
- ✅ 伪装插件列表
- ✅ 伪装 WebGL 厂商
- ✅ 伪装 Canvas 指纹
- ✅ 隐藏自动化特征

---

## 📊 伪装效果对比

| 检测项 | 未伪装 | 基础伪装 | stealth 插件 |
|--------|--------|---------|-------------|
| navigator.webdriver | ❌ true | ✅ undefined | ✅ undefined |
| User-Agent | ❌ HeadlessChrome | ✅ 正常 | ✅ 正常 |
| 视口大小 | ⚠️ 默认 | ✅ 1920x1080 | ✅ 1920x1080 |
| 时区/语言 | ⚠️ UTC/en | ✅ Asia/Shanghai | ✅ 继承系统 |
| 插件列表 | ❌ 0 个 | ⚠️ 手动配置 | ✅ 自动伪装 |
| Canvas 指纹 | ❌ 无噪声 | ⚠️ 无噪声 | ✅ 添加噪声 |
| WebGL 信息 | ❌ SwiftShader | ⚠️ 未处理 | ✅ 伪装 |
| 行为模式 | ❌ 机械 | ⚠️ 需手动 | ⚠️ 需手动 |

---

## 🎯 实际应用场景

### 场景 1：HTML 转 PDF（你的需求）

**需要伪装吗？** ❌ **不需要！**

**原因：**
- 本地文件（file://协议）
- 没有反爬机制
- 不需要隐藏身份

**配置：**
```javascript
// 简单配置即可
const browser = await chromium.launch({ headless: true });
```

---

### 场景 2：抓取公开网页

**需要伪装吗？** ⚠️ **建议基础伪装**

**原因：**
- 可能有基础反爬
- 避免被识别为机器人
- 防止 IP 被封

**配置：**
```javascript
const context = await browser.newContext({
  userAgent: 'Mozilla/5.0...',
  viewport: { width: 1920, height: 1080 },
});
```

---

### 场景 3：抓取受保护网页

**需要伪装吗？** ✅ **必须 stealth 插件**

**原因：**
- 有高级反爬（Cloudflare 等）
- 检测自动化特征
- 需要完整伪装

**配置：**
```javascript
const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth');
chromium.use(stealth());
```

---

## ⚖️ 伪装的成本

### 时间成本

| 伪装级别 | 配置时间 | 运行时间 |
|---------|---------|---------|
| 无伪装 | 0 分钟 | 正常 |
| 基础伪装 | +1 分钟 | 正常 |
| stealth 插件 | +2 分钟 | +10-20% |

### 资源成本

| 伪装级别 | 内存占用 | CPU 占用 |
|---------|---------|---------|
| 无伪装 | 正常 | 正常 |
| 基础伪装 | 正常 | 正常 |
| stealth 插件 | +5-10% | +10-20% |

---

## 💡 关键洞察

### 1. 伪装不是万能的

**现实：**
- ✅ 基础反爬：伪装有效
- ⚠️ 中级反爬：可能有效
- ❌ 高级反爬（Cloudflare Bot Management）：很难绕过

### 2. 行为伪装比技术伪装更重要

**检测趋势：**
- 2020 年：主要检测技术特征（webdriver、User-Agent）
- 2024 年：主要检测行为模式（鼠标、点击、滚动）
- 2026 年：AI 行为分析（打字节奏、浏览习惯）

### 3. 本地 HTML 转 PDF 不需要伪装

**你的场景：**
- ✅ 本地文件，没有反爬
- ✅ 简单配置即可
- ✅ 不需要 stealth 插件

---

## 📝 总结

**浏览器伪装 = 让机器人看起来像真人**

**伪装内容：**
1. 隐藏自动化标志（navigator.webdriver）
2. 伪装 User-Agent（浏览器标识）
3. 伪装视口大小（1920x1080）
4. 伪装时区/语言（Asia/Shanghai）
5. 伪装插件列表
6. 伪装 Canvas/WebGL 指纹
7. 模拟真实行为（鼠标/点击/滚动）

**你的场景（HTML 转 PDF）：**
- ❌ 不需要伪装（本地文件）
- ✅ 简单配置即可
- ✅ 专注核心功能

---

_报告生成时间：2026-03-09 09:12_
