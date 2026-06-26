---
name: 班级小管家作业截图
slug: banjixiaoguanjia
version: 1.0.0
description: "自动化班级小管家作业截图工具。支持连接 Chrome 调试端口、进入指定课程、滚动查看学生列表、截取学生作业图片。专为小学数学老师设计，用于批量获取学生作业截图进行批改。"
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["node","npm"],"packages":["playwright"]},"os":["linux","darwin","win32"]}}
---

# 班级小管家作业截图

自动化班级小管家 (banjixiaoguanjia.com) 作业截图工具，支持批量获取学生作业图片。

## 功能特性

- 🔌 连接 Chrome 调试端口 (CDP)
- 📖 自动进入指定课程
- 👨‍🎓 滚动查看所有学生
- 📸 批量截取学生作业图片
- 🤖 支持 AI 图像分析 (GLM/MiniMax)

## 编码规范

**重要**: 所有文件、路径、目录统一使用 **UTF-8 编码**

- 脚本文件保存为 UTF-8 with BOM
- 文件路径处理使用 UTF-8 编码
- 输出报告使用 UTF-8 编码
- 避免使用 GBK/GB2312 编码

## 前置要求

1. **Chrome 浏览器** 已安装
2. **已登录** 班级小管家（首次使用需要手动登录）

> 💡 **提示**: 使用 `capture-new-browser.js` 脚本时，无需手动启动 Chrome 调试模式，脚本会自动处理浏览器启动和复用。

## 📖 脚本使用手册

**⚠️ 重要**: 
- 详细的脚本使用流程请查看 [`SCRIPT-GUIDE.md`](./SCRIPT-GUIDE.md)
- **必须严格按照 SCRIPT-GUIDE.md 使用脚本**，不要随意尝试目录下其他脚本
- 本目录下脚本众多，部分脚本有bug或已过时

---

## 快速开始

### 🆕 推荐使用脚本: `capture-new-browser.js` (v1.9.0+)

**最新版功能**:
- ✅ **自动复用浏览器**: 检测已打开的班级小管家页面，有则复用，无则启动新浏览器（开启调试端口 9222）
- ✅ **动态学生列表**: 自动获取学生列表，不固定学生名字，支持任意班级
- ✅ **智能截图**: 采用固定步长滚动（400像素），确保截图顺序正确
- ✅ **改正作业处理**: 自动检测"改正如下"标签，单独截图改正部分
- ✅ **浏览器保持打开**: 脚本结束时无限等待，防止浏览器被意外关闭
- ✅ **窗口大小**: 1280x1000（高度 1000）
- ✅ **使用本地 Chrome**: 不是 Chrome for Testing

**使用方法**:
```bash
node capture-new-browser.js "课程名称"
```

**示例**:
```bash
node capture-new-browser.js "二下(第38节)"
```

**输出位置**: `桌面/课程名称/`

**浏览器复用逻辑**:
1. 第一次运行：启动新浏览器，自动开启调试端口 9222
2. 后续运行：检测并复用已打开的浏览器，无需重新扫码登录
3. 脚本完成：浏览器保持打开，可继续手动查看和批改

---

### 旧版脚本（不推荐）

**截图 + AI分析作业数量**:
```bash
node capture-36-fixed.js "二下(第36节)"
```

> ⚠️ **注意**: 旧版脚本需要手动启动 Chrome 调试模式，且不会自动复用浏览器

---

## 核心 API

### 连接到 Chrome

```javascript
const { chromium } = require('playwright');
const browser = await chromium.connectOverCDP('http://localhost:9222');
```

### 进入课程

```javascript
// 启用辅助功能
await page.evaluate(() => {
  const el = document.querySelector('flt-semantics-placeholder');
  if (el) el.click();
});

// 查找并点击课程
await page.evaluate((courseName) => {
  const elements = document.querySelectorAll('flt-semantics[aria-label]');
  for (const el of elements) {
    const label = el.getAttribute('aria-label');
    if (label && label.includes(courseName)) {
      el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      break;
    }
  }
}, '三上(第11节)');
```

### 滚动查找课程（课程列表页面）

> ⚠️ **关键发现**: Flutter 页面需要使用 `scrollIntoView` 滚动到已知课程来触发动态加载更多课程！

**正确方法**:
```javascript
// 滚动到最后一个已知课程，触发 Flutter 加载更多
await page.evaluate(() => {
  const elements = document.querySelectorAll('flt-semantics[aria-label]');
  let lastCourseEl = null;
  
  for (const el of elements) {
    const label = el.getAttribute('aria-label');
    if (label && (label.includes('第') || label.includes('年级'))) {
      lastCourseEl = el;
    }
  }
  
  if (lastCourseEl) {
    lastCourseEl.scrollIntoView({ block: 'start' });
  }
});

await page.waitForTimeout(1500); // 等待加载完成
```

**完整查找流程**:
```javascript
async function findCourseWithScroll(courseName, maxScrolls = 20) {
  for (let i = 0; i < maxScrolls; i++) {
    // 1. 在当前视图查找目标课程
    const found = await page.evaluate((name) => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes(name)) {
          return { found: true, label };
        }
      }
      return { found: false };
    }, courseName);
    
    if (found.found) return found;
    
    // 2. 滚动到最后一个课程，触发加载更多
    await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      let lastCourseEl = null;
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && (label.includes('第') || label.includes('年级'))) {
          lastCourseEl = el;
        }
      }
      if (lastCourseEl) lastCourseEl.scrollIntoView({ block: 'start' });
    });
    
    await page.waitForTimeout(1500);
  }
}
```

### 滚动查看学生

```javascript
// 获取滚动容器
const scrollContainer = await page.evaluate(() => {
  return document.querySelector('[style*="overflow-y: scroll"]');
});

// 滚动到指定位置
await page.evaluate((scrollTop) => {
  const el = document.querySelector('[style*="overflow-y: scroll"]');
  if (el) el.scrollTop = scrollTop;
}, 100);
```

### 截图学生作业

```javascript
await page.screenshot({ 
  path: `screenshots/${studentName}.png`, 
  fullPage: true 
});
```

## 完整示例

```javascript
const { chromium } = require('playwright');

async function captureHomework(courseName, outputDir = './screenshots') {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  if (!page) {
    page = await context.newPage();
    await page.goto('https://service.banjixiaoguanjia.com/appweb/');
  }
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  // 进入课程
  await page.evaluate((name) => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.includes(name)) {
        el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        break;
      }
    }
  }, courseName);
  
  await page.waitForTimeout(4000);
  
  // 获取学生列表
  const students = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    const list = [];
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split('\n');
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          list.push(name);
        }
      }
    }
    return list;
  });
  
  // 截图每个学生
  for (const student of students) {
    await page.screenshot({ 
      path: `${outputDir}/${student}.png`, 
      fullPage: true 
    });
    console.log(`✓ 已截图: ${student}`);
  }
  
  await browser.close();
}
```

## 技术要点

### 课程详情页 vs 批改页面的区别

| 页面 | 学生信息格式 | 查找条件 |
|------|-------------|----------|
| **课程详情页** | `球球\n2026-03-21 14:20\n 1.听课顺序...` | `includes('2026-') && includes('课内')` |
| **批改页面** | `球球的作业(1/11)` | 匹配正则 `/(.+?)的作业\((\d+)\/(\d+)\)/` |

> ⚠️ **关键**: 两个页面的学生信息格式完全不同，不能用相同的查找条件！

### Flutter 页面特殊处理

1. **启用辅助功能**: 必须先点击 `flt-semantics-placeholder`
2. **点击方式**: 使用 `dispatchEvent(new MouseEvent('click', { bubbles: true }))`
3. **滚动容器**: 查找 `[style*="overflow-y: scroll"]` 元素
4. **语义元素**: 通过 `flt-semantics[aria-label]` 定位

### 【关键】滚动截图策略

> ⚠️ **重要发现**: 每次截图前必须先复位，否则 scrollTop 会累积导致截图错误！

**正确流程**:
```javascript
// 1. 先复位 scrollTop = -1000（关键！）
await page.evaluate(() => {
  const el = document.querySelector('[style*="overflow-y: scroll"]');
  if (el) el.scrollTop = -1000;
});

// 2. 等待复位完成
await page.waitForTimeout(500);

// 3. 设置具体的 scrollTop 值
await page.evaluate((scrollTop) => {
  const el = document.querySelector('[style*="overflow-y: scroll"]');
  if (el) el.scrollTop = scrollTop;
}, 12);  // 例如: Zoey 的位置

// 4. 等待滚动完成
await page.waitForTimeout(1000);

// 5. 截图
await page.screenshot({ path: 'Zoey.png' });
```

**二下第31节经验值**:

| 学生 | scrollTop | 说明 |
|------|-----------|------|
| 灿灿 | -3 | 只看到灿灿 |
| Zoey | 12 | 只看到Zoey和球球 |
| 球球 | 15 | 到底部，显示"没有更多了" |

**错误示范** (不复位):
```javascript
// ❌ 错误：不复位会导致 scrollTop 累积
await page.evaluate(() => {
  el.scrollTop = 12;  // 如果之前是 10，现在变成 22！
});
```

## 故障排除

### 无法连接到 Chrome
- 检查 Chrome 是否以 `--remote-debugging-port=9222` 启动
- 检查端口是否被占用: `curl http://localhost:9222/json/version`

### 找不到课程
- 确保已登录班级小管家
- 检查课程名称是否完全匹配（包含年级、班级信息）

### 点击无效
- 确保已启用辅助功能
- 使用 `dispatchEvent` 而非普通 `click()`

## Qwen3.5-Plus 图像分析

截图完成后，使用 **Qwen3.5-Plus** (通义千问) 分析学生作业提交情况。

### 依赖安装

```bash
pip install openai
```

### 环境变量设置

```bash
# Windows PowerShell
$env:DASHSCOPE_API_KEY="sk-your-api-key"

# Windows CMD
set DASHSCOPE_API_KEY=sk-your-api-key

# 永久设置（Windows）
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "sk-your-api-key", "User")
```

### 使用方法

```javascript
const { BanjixiaoguanjiaCapture } = require('./skills/banjixiaoguanjia');

const capture = new BanjixiaoguanjiaCapture();

// 截图并分析（自动使用 DASHSCOPE_API_KEY 环境变量）
const result = await capture.captureAndAnalyze('一下(第9节)');

// 输出分析结果
for (const item of result.analysis) {
  console.log(`学生: ${item.student}`);
  console.log(`分析: ${item.analysis}`);
}
```

### 分析结果示例

```
学生姓名：KIKI
课内作业：6张
奥数作业：7张
```

### API Key 获取

1. 访问 https://bailian.console.aliyun.com
2. 注册/登录阿里云账号
3. 在控制台获取 API Key

## 作业图片下载完整流程

### 流程概述

```
阶段1: AI分析（Qwen）
├── 截图所有学生作业
├── 使用Qwen分析每张截图
└── 获取：学生姓名 + 课内数量 + 奥数数量

阶段2: 下载原图
├── 进入课程 → 点击第一个学生图片 → 进入批改页面
├── 下载当前学生作业（先课内，后奥数）
├── 核对：本地文件数量 vs 分析结果数量
├── 点击左侧学生名字切换到下一个学生
├── 重复下载流程
└── 直到所有学生下载完成

阶段3: 最终核对
├── 检查每个学生文件夹
├── 核对课内/奥数图片数量
└── 确认全部下载成功
```

### 关键要点

1. **刷新会回到首页** - 操作过程中不能刷新页面
2. **学生切换** - 在批改页面左侧点击学生名字（页面不刷新，自动回到第1张）
3. **查看原图按钮** - 元素索引[8]，位置(814,0)，尺寸40x56
4. **图片切换** - 使用 `ArrowRight` 键切换到下一张
5. **作业顺序** - 先课内，后奥数
6. **以分析结果为准** - 多余图片不下载
7. **核对步骤** - 每个学生下载完成后，必须核对本地文件数量与AI分析结果是否一致

### 动态获取学生信息（关键修正）

> ⚠️ **重要**: 页面顶部元素[7]显示"学生名字的作业(X/Y)"，**不包含"返回"前缀**！
> 
> 页面结构：
> - 元素[6]: "返回" - 返回按钮
> - 元素[7]: "Zoey的作业(8/8)" - 学生名字和作业信息（**用这个！**）

```javascript
// 获取当前学生名字和图片位置
const currentInfo = await page.evaluate(() => {
  const elements = document.querySelectorAll('flt-semantics');
  
  // 优先检查元素[7]（页面顶部标题，不包含"返回"前缀）
  if (elements[7]) {
    const text = elements[7].textContent || elements[7].getAttribute('aria-label') || '';
    const match = text.match(/(.+?)的作业\((\d+)\/(\d+)\)/);
    if (match) {
      return {
        student: match[1].trim(),      // 学生名字（不含"返回"前缀）
        current: parseInt(match[2]),   // 当前图片位置
        total: parseInt(match[3])      // 总图片数
      };
    }
  }
  
  // 备用：遍历所有元素查找
  for (let i = 0; i < elements.length; i++) {
    const text = elements[i].textContent || elements[i].getAttribute('aria-label') || '';
    const match = text.match(/(.+?)的作业\((\d+)\/(\d+)\)/);
    if (match) {
      let studentName = match[1].trim();
      // 去掉"返回"前缀（兼容旧版本）
      studentName = studentName.replace(/^返回/, '');
      return {
        student: studentName,
        current: parseInt(match[2]),
        total: parseInt(match[3])
      };
    }
  }
  return null;
});

// 获取左侧学生列表（v8 动态获取）
const students = await page.evaluate(() => {
  const elements = document.querySelectorAll('flt-semantics');
  const studentList = [];
  
  for (let i = 0; i < elements.length; i++) {
    const text = elements[i].textContent || elements[i].getAttribute('aria-label') || '';
    // 匹配学生名字（短文本，排除各种UI元素）
    if (text.length > 0 && text.length < 20 && 
        !text.includes('作业') && !text.includes('图片') && 
        !text.includes('查看') && !text.includes('详情') &&
        !text.includes('2026-') && !text.includes('课内') &&
        !text.includes('奥数') && !text.includes('返回') &&
        !text.includes('已点评') && !text.includes('待点评') &&
        !text.includes('没有更多') && !text.includes('收起') &&
        !text.includes('点评') && !text.includes('全部') &&
        !text.includes('未点评') && !text.includes('帮助') &&
        !text.includes('快捷键') && !text.includes('设置') &&
        !text.includes('画笔') && !text.includes('旋转') &&
        !text.includes('文字') && !text.includes('橡皮擦') &&
        !text.includes('撤销') && !text.includes('放大') &&
        !text.includes('缩小') && !text.includes('上一张') &&
        !text.includes('下一张') && !text.includes('保存')) {
      studentList.push({
        index: i,
        name: text.trim()
      });
    }
  }
  
  return studentList;
});
```

### 下载单个学生作业（含核对）

```javascript
async function downloadStudentImages(page, studentName, keNeiCount, aoShuCount, outputDir) {
  const totalCount = keNeiCount + aoShuCount;
  
  // 创建目录
  const keNeiDir = path.join(outputDir, studentName, '课内');
  const aoShuDir = path.join(outputDir, studentName, '奥数');
  
  if (!fs.existsSync(keNeiDir)) fs.mkdirSync(keNeiDir, { recursive: true });
  if (!fs.existsSync(aoShuDir)) fs.mkdirSync(aoShuDir, { recursive: true });
  
  // 下载课内作业（第1到keNeiCount张）
  for (let i = 1; i <= keNeiCount; i++) {
    const savePath = path.join(keNeiDir, `图片${i}.jpg`);
    
    // 点击"查看原图"按钮（元素[8]）
    await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics');
      if (elements[8]) {
        elements[8].dispatchEvent(new MouseEvent('click', { bubbles: true }));
      }
    });
    
    await page.waitForTimeout(3000);
    
    // 获取图片URL并下载
    const context = page.context();
    const pages = context.pages();
    const newPage = pages.find(p => p !== page && p.url().includes('img.banjixiaoguanjia.com'));
    
    if (newPage) {
      const imageUrl = newPage.url();
      execSync(`curl -L -o "${savePath}" "${imageUrl}"`, { timeout: 30000 });
      await newPage.close();
      await page.waitForTimeout(500);
    }
    
    // 切换到下一张
    if (i < totalCount) {
      await page.keyboard.press('ArrowRight');
      await page.waitForTimeout(1500);
    }
  }
  
  // 下载奥数作业（第1到aoShuCount张）
  for (let i = 1; i <= aoShuCount; i++) {
    const savePath = path.join(aoShuDir, `图片${i}.jpg`);
    
    // 点击"查看原图"按钮
    await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics');
      if (elements[8]) {
        elements[8].dispatchEvent(new MouseEvent('click', { bubbles: true }));
      }
    });
    
    await page.waitForTimeout(3000);
    
    // 获取图片URL并下载
    const context = page.context();
    const pages = context.pages();
    const newPage = pages.find(p => p !== page && p.url().includes('img.banjixiaoguanjia.com'));
    
    if (newPage) {
      const imageUrl = newPage.url();
      execSync(`curl -L -o "${savePath}" "${imageUrl}"`, { timeout: 30000 });
      await newPage.close();
      await page.waitForTimeout(500);
    }
    
    // 切换到下一张
    if (i < aoShuCount) {
      await page.keyboard.press('ArrowRight');
      await page.waitForTimeout(1500);
    }
  }
  
  // ===== 核对步骤 =====
  console.log(`\n核对 ${studentName} 的下载结果...`);
  
  // 核对课内作业
  const keNeiFiles = fs.readdirSync(keNeiDir).filter(f => f.endsWith('.jpg'));
  console.log(`  课内作业: 预期 ${keNeiCount} 张, 实际 ${keNeiFiles.length} 张`);
  if (keNeiFiles.length !== keNeiCount) {
    console.log(`  ⚠️ 课内作业数量不匹配!`);
  } else {
    console.log(`  ✓ 课内作业核对通过`);
  }
  
  // 核对奥数作业
  const aoShuFiles = fs.readdirSync(aoShuDir).filter(f => f.endsWith('.jpg'));
  console.log(`  奥数作业: 预期 ${aoShuCount} 张, 实际 ${aoShuFiles.length} 张`);
  if (aoShuFiles.length !== aoShuCount) {
    console.log(`  ⚠️ 奥数作业数量不匹配!`);
  } else {
    console.log(`  ✓ 奥数作业核对通过`);
  }
  
  // 核对总数
  const totalFiles = keNeiFiles.length + aoShuFiles.length;
  console.log(`  总计: 预期 ${totalCount} 张, 实际 ${totalFiles} 张`);
  if (totalFiles !== totalCount) {
    console.log(`  ⚠️ 总数不匹配!`);
    return false;  // 返回失败状态
  } else {
    console.log(`  ✓ ${studentName} 全部核对通过`);
    return true;   // 返回成功状态
  }
}
```

### 切换到下一个学生（v8 动态获取 + 索引点击）

> ⚠️ **重要**: 切换学生后必须验证是否成功，并确保回到第1张图片！
> 
> **v8 改进**: 动态获取学生列表，通过索引点击，支持任意课程

```javascript
// 动态获取学生列表并切换到目标学生
async function switchToStudent(page, targetStudentName) {
  console.log(`切换到学生: ${targetStudentName}`);
  
  // 1. 获取左侧学生列表
  const students = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    const studentList = [];
    for (let i = 0; i < elements.length; i++) {
      const text = elements[i].textContent || elements[i].getAttribute('aria-label') || '';
      if (text.length > 0 && text.length < 20 && 
          !text.includes('作业') && !text.includes('图片') && 
          !text.includes('查看') && !text.includes('详情') &&
          !text.includes('2026-') && !text.includes('课内') &&
          !text.includes('奥数') && !text.includes('返回') &&
          !text.includes('已点评') && !text.includes('待点评') &&
          !text.includes('没有更多') && !text.includes('收起') &&
          !text.includes('点评') && !text.includes('全部') &&
          !text.includes('未点评') && !text.includes('帮助') &&
          !text.includes('快捷键') && !text.includes('设置') &&
          !text.includes('画笔') && !text.includes('旋转') &&
          !text.includes('文字') && !text.includes('橡皮擦') &&
          !text.includes('撤销') && !text.includes('放大') &&
          !text.includes('缩小') && !text.includes('上一张') &&
          !text.includes('下一张') && !text.includes('保存')) {
        studentList.push({ index: i, name: text.trim() });
      }
    }
    return studentList;
  });
  
  // 2. 查找目标学生
  const targetInfo = students.find(s => s.name === targetStudentName);
  if (!targetInfo) {
    console.log(`  ⚠️ 未在学生列表中找到 ${targetStudentName}`);
    return null;
  }
  
  // 3. 使用索引点击
  await page.evaluate((index) => {
    const elements = document.querySelectorAll('flt-semantics');
    if (elements[index]) {
      elements[index].dispatchEvent(new MouseEvent('click', { bubbles: true }));
    }
  }, targetInfo.index);
  
  // 4. 等待页面刷新（切换学生后会自动回到第1张图片）
  await page.waitForTimeout(4000);
  
  // 5. 验证切换是否成功（检查页面顶部元素[7]）
  const info = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    if (elements[7]) {
      const text = elements[7].textContent || elements[7].getAttribute('aria-label') || '';
      const match = text.match(/(.+?)的作业\((\d+)\/(\d+)\)/);
      if (match) {
        return {
          student: match[1].trim(),
          current: parseInt(match[2]),
          total: parseInt(match[3])
        };
      }
    }
    return null;
  });
  
  if (info && info.student === targetStudentName) {
    console.log(`✓ 已切换到 ${targetStudentName}: 第${info.current}/${info.total}张`);
    return info;
  } else {
    console.log(`  ⚠️ 切换后显示: ${info ? `${info.student} (第${info.current}/${info.total}张)` : '未知'}`);
    return null;
  }
}
```

## 作业分析功能

### 使用 `analyze-homework.js` 进行作业批改

```javascript
const { HomeworkAnalyzer } = require('./analyze-homework');

const analyzer = new HomeworkAnalyzer();

// 分析单个学生作业
await analyzer.analyze('一下(第9节)', '大瑀', '课内');

// 输出：
// - 一下(第9节)大瑀课内分析.txt
// - 一下(第9节)大瑀课内分析.docx
```

### 分析流程

```
阶段1: 准备
├── 检查答案文件（桌面/答案/课程名称/课内答案.png）
├── 获取作业图片
└── 统计图片数量

阶段2: AI分析（Qwen模型）
├── 优先批量分析（答案+所有作业图片）
├── 如果失败，切换到逐一分析
└── 生成批改结果

阶段3: 生成报告
├── 保存 TXT 文件
└── 生成 Word 文档（微软雅黑，优化排版）
```

### 提示词模板

**有答案时：**
```
第1张图片是XX答案.png，这是作业的标准答案，你需要认真参考答案进行作业批改。

帮我检查这些作业的对错...
```

**无答案时：**
```
帮我检查这些作业的对错...
```

### Word 排版格式（手机阅读优化版）

**设计目标**：适合手机阅读，字体大、布局简洁、层次清晰

- **页面边距**：窄边距（0.5英寸），内容更宽适合手机屏幕
- **字体**：微软雅黑
- **大标题**：20磅，📚表情+蓝色加粗居中
- **副标题**：12磅，灰色居中
- **章节标题**：16磅，▶符号+蓝色加粗
- **小节标题**：15磅，加粗，深灰色
- **正文**：14磅（手机阅读用大字体）
- **列表项**：数字用蓝色加粗，内容14磅
- **子项**：13磅，缩进显示
- **正确标记**：绿色 ✅
- **错误标记**：红色 ❌
- **页脚**：12磅，灰色居中

**排版特点**：
- 流式布局，去掉表格
- 章节间空行分隔
- 颜色区分对错
- 层次用缩进和符号区分

### 阶段5: 完成当前课程

```
阶段5: 完成当前课程
├── 所有作业下载和分析完成
├── 刷新班级小管家页面（自动回到首页）
└── 等待下一次作业批改命令
```

**操作：**
```javascript
// 刷新页面回到首页
await page.goto('https://service.banjixiaoguanjia.com/appweb/');
console.log('已回到首页，等待下一次作业批改命令');
```

## 相关技能

- **qwen35-plus-image-analyze**: 使用 Qwen3.5-Plus 分析作业图片
- **playwright**: 浏览器自动化基础

## 更新日志

### 1.0.0
- 初始版本
- 支持 Chrome CDP 连接
- 支持课程进入和学生截图

### 1.1.0
- 新增作业图片下载功能
- 使用 Qwen3.5-Plus 进行AI分析
- 支持动态获取学生列表
- 支持课内/奥数分类下载

### 1.2.0
- 新增作业分析功能
- 支持批量/逐一分析
- 自动生成 Word 报告
- 优化排版格式（微软雅黑）

### 1.3.0 (2026-03-22)
- **关键修正**: 页面顶部元素[7]显示"学生名字的作业(X/Y)"，不包含"返回"前缀
- **关键修正**: 切换学生后必须验证是否成功，通过检查页面顶部元素[7]核对"当前第几张/一共多少张"
- **关键修正**: 学生名字在左侧列表中的索引通常是固定的（如：球球在索引16，Zoey在索引17）
- **关键修正**: 课程详情页查找学生的条件应该是 `includes('2026-') && includes('课内')`，而不是 `includes('已点评')`
- 新增 `download-homework.js` 完整下载脚本
- 新增 `analyze-homework-ai.js` AI分析脚本
- **新增**: `SCRIPT-GUIDE.md` 脚本使用手册

### 1.4.0 (2026-03-22)
- **v8 改进**: `download-homework.js` 使用动态获取学生列表 + 索引点击的方式切换学生
- **移除**: 固定学生名字的专用脚本（如 download-zoey.js）
- **优势**: 支持任意课程，无需为每个课程创建专用脚本
- **新增**: `archived-scripts/` 脚本归档目录
- **规范**: 统一使用 UTF-8 编码处理文件、路径、目录

### 1.5.0 (2026-03-22)
- **文档更新**: 在 SCRIPT-GUIDE.md 和 SKILL.md 中明确标注推荐脚本
- **问题记录**: 标注 `capture-and-analyze-36.js` 有bug（学生数量判断死循环）
- **推荐脚本**: `capture-36-fixed.js` 作为截图+AI分析的标准脚本
- **重要提示**: 强调必须按照文档使用脚本，不要随意尝试其他脚本

### 1.6.0 (2026-03-23)
- **逻辑调整**: `download-homework.js` 新增"已点评"检查
  - 遍历学生列表时，检查每个学生是否有"已点评"标签
  - 有"已点评"标签 → 跳过该学生的作业下载
  - 无"已点评"标签 → 正常下载该学生作业
  - 在 `getStudentList()` 方法中返回 `skip` 字段标记是否需要跳过
  - 在 `switchToStudent()` 方法中检查 `skip` 字段并跳过已点评学生

### 1.7.0 (2026-03-23)
- **截图逻辑修复**: `capture-36-fixed.js` 修复截图定位问题
  - 问题: 使用 `getBoundingClientRect().top` 定位不准确，导致截图错误（如Zoey截图显示为球球作业）
  - 解决: 收集学生列表后**重新进入页面**，按顺序使用固定滚动步长（400px）截图
  - 关键: 不再依赖 `top` 值定位，而是按顺序滚动截图
- **"改正如下"处理**: `capture-36-fixed.js` 添加改正作业截图逻辑
  - 检测"改正如下"标签（收集学生列表时检查 `fullLabel`）
  - 单独截图改正部分（保存为 `学生名_改正.png`）
  - AI分析时提示不统计改正部分
- **"已点评"检测修复**: `download-homework.js` 修复学生名字提取逻辑
  - 问题: 左侧学生列表中的文本包含"已点评"、"良好"等标签，导致名字匹配失败
  - 解决: 提取学生名字时去掉"已点评"、评级（优秀/良好/合格/待改进）、数字括号、换行符等
  - 确保第一个学生也能正确检测"已点评"状态并跳过下载

### 1.9.0 (2026-03-29)
- **新版一键截图脚本**: `capture-new-browser.js` 正式发布
  - 自动复用浏览器：检测已打开的班级小管家页面，有则复用，无则启动新浏览器
  - 动态学生列表：自动获取学生列表，不固定学生名字，支持任意班级
  - 智能截图逻辑：采用固定步长滚动（400像素），确保截图顺序正确
  - 改正作业处理：检测"改正如下"标签，单独截图改正部分
  - 浏览器保持打开：脚本结束时无限等待，防止浏览器被意外关闭
  - 窗口大小：1280x1000，使用本地 Chrome

### 1.8.0 (2026-03-24)
- **Word报告手机阅读优化**: `analyze-homework.js` 重构Word生成逻辑
  - 页面边距缩小到0.5英寸，适合手机屏幕
  - 正文字体从12pt增大到14pt，章节标题16pt，大标题20pt
  - 去掉表格布局，改用流式排版
  - 添加📚表情符号和▶章节标记
  - 正确内容显示绿色，错误内容显示红色
  - 层次结构：大章节→小节→子项，用缩进和符号区分
