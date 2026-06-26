# Business Opportunity Skills Report & Screenshot

生成商机发现 Skills 推荐报告，并用 Chromium 打开页面进行全页滚动截屏保存。

## 功能特点

1. **智能搜索**: 调用 ClawHub API 搜索商机相关 Skills
2. **Fallback 机制**: 当 API 限流或失败时，自动使用预设的 15 个热门商机 Skills 数据
3. **详细报告**: 生成美观的 HTML 报告，包含分类展示
4. **自动截屏**: 启动 Chromium 浏览器并自动截取全页图片

## 预设数据（API 失败时使用）

当 ClawHub API 超速限流时，会自动使用以下预设 Skills：

### 🔍 商机发现
- opportunity-discovery
- business-opportunity-detector
- opportunity-assessment

### 📊 市场分析
- market-environment-analysis
- market-analysis-cn
- market-sentiment-pulse

### 💼 商业战略
- business-development
- business
- startup

### 🎯 获客引流
- lead-generation
- lead-researcher

### 🛠️ 创业工具
- startup-toolkit
- startup-financial-modeling
- competitor-analysis

## 输入参数

- `query`: 搜索关键词（可选，默认 "opportunity"）
- `output_name`: 输出文件名（可选，默认 "商业发现-${日期}"）

## 输出

- HTML 报告文件（保存在 workspace 根目录）
- Chromium 浏览器打开页面
- 全页截屏保存到 output 目录（文件名：${output_name}.jpg）

## 依赖

- `clawhub` CLI
- `chromium-browser`
- `puppeteer-core` npm 包
- WSL2 环境 + DISPLAY=:0

## 安装依赖

```bash
cd /home/xiaoduo/.openclaw/workspace-product/skills/business-opportunity-screenshot
npm install puppeteer-core
```

## 使用方法

```bash
# 基本用法
node scripts/screenshot.js

# 指定搜索关键词
node scripts/screenshot.js business

# 指定输出名称
node scripts/screenshot.js opportunity "商机报告-2026-03-16"
```

## 关键工具

### 1. ClawHub 搜索
```bash
clawhub search <关键词>
```

### 2. 获取 Skill 详情
```bash
clawhub inspect <skill-slug>
```

### 3. 启动 Chromium（调试模式）
```bash
export DISPLAY=":0" && chromium-browser --remote-debugging-port=9222 <url>
```

### 4. Puppeteer 连接截屏
```javascript
const puppeteer = require('puppeteer-core');
const browser = await puppeteer.connect({ browserURL: 'http://localhost:9222' });
await page.screenshot({ path: 'output.jpg', fullPage: true });
```

## 触发词

- 商机发现报告
- 商机 skills 截图
- 商业机会 skills 报告
- 生成商机发现页面并截屏
