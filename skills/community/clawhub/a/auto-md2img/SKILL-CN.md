---
name: auto-md2img
emoji: 🖼️
description: 自动将 Markdown 内容转换为 GitHub 风格图片，支持按高度分页、JPEG质量调整，完整支持中文、智能分页、Emoji、语法高亮
author: OpenClaw Community
version: 1.3.1
license: MIT
tags: ["markdown", "图片", "转换", "md2img", "puppeteer", "分页", "质量调整", "中文"]
---

# 🥑 Auto MD2IMG 技能

自动将 Markdown 内容转换为图片发送，支持任意消息平台，大幅提升阅读体验。

---

## ✨ 功能特性

- 🖼️ 自动将 Markdown 转换为高清图片
- 📄 支持智能分页，默认每页 500 行，支持自定义
- 🧱 按内容块切割，不切断标题、代码块、表格、列表等
- 🔢 自动添加页码标注
- 🀄 完美支持中文字体，无乱码
- 😊 支持彩色 Emoji 渲染
- 🎨 GitHub 风格渲染，代码语法高亮
- 📸 自动识别 JPEG/PNG 格式，支持质量调整
- 🔍 Debug 模式，输出详细日志并保存分页内容
- ⚡ 后台浏览器管理，重复转换性能提升 50%+
- 🧹 自动缓存清理，保护隐私，无残留文件

---

## 📖 使用方法

当需要向用户回复 Markdown 格式内容时：

### 基本用法

1. 将 Markdown 内容保存到临时文件（或直接传入字符串）
2. 调用 `scripts/md_to_png.js` 生成图片
3. 使用 `<img>` 标签发送图片给用户
4. 根据不同消息平台使用对应的图片标签嵌入路径
5. 图片生成失败时，回退为发送纯文本 Markdown

### 脚本调用

```bash
# 基本用法
node scripts/md_to_png.js input.md

# 指定输出路径
node scripts/md_to_png.js input.md output.jpg

# 自定义每页行数（默认 500 行）
node scripts/md_to_png.js input.md output.jpg 300

# 自定义图片质量（JPEG 格式，1-100，默认 80）
node scripts/md_to_png.js input.md output.jpg 300 75

# 启用 Debug 模式（输出详细日志 + 保存分页内容）
node scripts/md_to_png.js input.md output.jpg --debug
```

### 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `inputFile` | string | ✅ | - | 输入的 Markdown 文件路径 |
| `outputPath` | string | ❌ | 当前目录 | 输出图片路径 |
| `maxLinesPerPage` | number | ❌ | 500 | 每页最大行数 |
| `imageQuality` | number | ❌ | 80 | JPEG 图片质量（1-100） |
| `--debug` | flag | ❌ | - | 启用 Debug 模式 |

---

## 🔧 配置说明

### 字体配置
- 默认字体：文泉驿微米黑、文泉驿正黑、Noto CJK SC、Noto Color Emoji
- 支持系统字体回退，自动适配环境中的中文字体

### 输出配置
- 输出分辨率：2x（高清，Retina 屏幕友好）
- 最大宽度：900px，兼顾手机和桌面端显示
- 自动适应内容高度，无多余空白
- 自动识别 JPEG/PNG 格式，根据文件扩展名选择
- 默认 JPEG 质量：80%，平衡画质和文件大小

### 分页配置
- 默认每页最大行数：500（行数分页模式）
- **新增：高度分页模式**：按像素高度阈值分割（`--height` 参数），与行数无关
- 按内容块智能分割
- 不切断标题、代码块、引用、表格、列表等内容块
- 设置 `--height 0` 可完全禁用分页，输出单张长图

### Debug 模式
使用 `--debug` 标志启用时：
- 输出详细处理日志（内容块检测、分割点、渲染步骤）
- 保存中间 HTML 渲染文件用于调试
- 保存原始分页分割内容为单独文本文件
- 包含性能分析的时序指标

---

## 📂 脚本路径

`scripts/md_to_png.js` - 核心 Markdown 转图片工具

`scripts/md_to_png.js` 功能：
- 读取 Markdown 文件
- 智能内容块分割
- HTML 渲染
- Puppeteer 截图
- 缓存清理

---

## 🎯 使用示例

### 示例 1：简单转换

```javascript
import { exec } from 'child_process';
import path from 'path';

const markdownContent = `# 你好，世界\n\n这是测试内容。`;

// 保存到临时文件
const tempFile = path.join('/tmp', 'temp.md');
fs.writeFileSync(tempFile, markdownContent);

// 调用转换脚本
exec(`node scripts/md_to_png.js ${tempFile}`, (error, stdout, stderr) => {
  if (error) {
    console.error('转换失败:', error);
    return;
  }
  console.log('转换成功:', stdout);
});
```

### 示例 2：在聊天应用中使用

```javascript
// 需要回复 Markdown 内容时
async function replyWithMarkdown(content, outputDir) {
  try {
    // 调用 md2img 转换
    const baseName = `reply_${Date.now()}`;
    const files = await convertMarkdown(content, outputDir, baseName);
    
    // 使用 <img> 标签发送图片
    for (const file of files) {
      await sendMessage(`<img src="${file.path}">`);
    }
  } catch (error) {
    // 失败时回退为纯文本
    await sendMessage(content);
  }
}
```

### 示例 3：高度分页模式

```bash
# 按2000像素高度分割，适合手机阅读
node scripts/md_to_png.js 长文章.md ./output --height 2000

# 不使用分页，输出单张长图
node scripts/md_to_png.js 短笔记.md ./output --height 0

# 结合JPEG质量调整，适合快速分享
node scripts/md_to_png.js 报告.md ./output 500 60 --height 1500
```

### 示例 4：Debug 模式

```bash
# 启用Debug模式排查转换问题
node scripts/md_to_png.js 有问题的内容.md ./output --debug
```

---

## 🔒 安全特性

- ✅ 路径遍历防护（输出目录白名单）
- ✅ 文件名清理（非法字符替换）
- ✅ 内容大小限制（最大 10MB）
- ✅ 行数范围校验（10-10000 行）
- ✅ 可配置的缓存清理策略

---

## 📊 性能指标

| 指标 | 值 |
|------|-----|
| 首次浏览器启动 | ~260ms |
| 小文档转换（200字） | ~2.3s |
| 中等文档转换（2KB） | ~2.6s |
| 大文档转换（5KB） | ~3.6s |
| 重复转换性能提升 | 4.5%（单次）/ 50-70%（批量） |

---

## 🎨 渲染效果

支持的 Markdown 元素：
- ✅ 标题（H1-H6）
- ✅ 文本样式（粗体、斜体、删除线、行内代码）
- ✅ 代码块（语法高亮）
- ✅ 列表（有序、无序）
- ✅ 表格
- ✅ 引用块
- ✅ 链接
- ✅ 图片
- ✅ Emoji

## 🆕 v1.3.1 新增功能

- 📏 高度分页模式（基于像素分割，不依赖行数统计）
- 📸 JPEG 质量调整（1-100，平衡画质和文件大小）
- 🔍 Debug 模式，便于排查转换问题
- ⚡ 重复转换性能提升 50%+
- 🧹 更积极的缓存清理机制，隐私保护更好
- 📁 **自动创建目录**：输出目录不存在时自动创建，无需手动提前创建
- 🐛 修复输出目录不存在时报错 `ENOENT` 问题
- 🐛 修复 PNG 格式 `quality` 参数报错问题
- 🐛 修复 JPEG 质量设置不生效的 Bug

---

## 🛠️ 技术栈

- Node.js >= 14
- Puppeteer（无头浏览器，负责截图）
- marked（Markdown 解析器）
- GitHub 风格 CSS 主题

---

## 📝 触发场景

所有需要输出 Markdown 格式内容的回复场景：
- 代码片段分享
- 技术文档回复
- 表格数据展示
- 列表整理
- 长文本格式化
- 用户输入中文时使用本技能

---

## ⚠️ 注意事项

1. 首次转换需要启动浏览器，速度稍慢
2. 批量转换时建议启用 `skipCacheClear` 配置
3. 大文档可能会分成多页，自动添加 `_page1`, `_page2` 后缀
4. 图片文件会占用磁盘空间，建议定期清理输出目录
5. Linux 环境下可能需要安装额外的字体和依赖：
   ```bash
   # Ubuntu/Debian
   sudo apt install fonts-wqy-microhei fonts-wqy-zenhei fonts-noto-color-emoji libnss3 libxss1 libasound2
   ```

---

**Auto MD2IMG 技能 - 让 Markdown 回复更美观！** 🎉
