# Auto MD2IMG

自动将 Markdown 内容转换为图片发送，提升阅读体验。支持中文、Emoji、代码高亮、表格、引用等所有 Markdown 元素，生成 GitHub 风格的高清图片。

## ✨ 功能特性

- 🖼️ 自动将 Markdown 转换为高清图片
- 📄 支持智能分页，每页最多 500 行
- 🧱 按内容块切割，不切断标题、代码块、表格、列表等
- 🔢 自动添加页码标注
- 🀄 完美支持中文字体，无乱码
- 😊 支持彩色 Emoji 渲染
- 🎨 GitHub 风格渲染，语法高亮
- ⚡ 后台浏览器管理，重复转换性能提升 50%+
- 🧹 自动缓存清理，保护隐私，无残留文件

## 📦 安装

### 方式 1：作为独立项目使用
```bash
# 克隆项目
git clone <repository-url>
cd auto-md2img

# 安装依赖
npm install
```

### 方式 2：作为 OpenClaw 技能使用
```bash
# 从 ClawHub 安装
clawhub install auto-md2img
```

## 📖 使用方法

### 命令行使用
```bash
# 基本用法：转换 input.md 为图片，自动生成分页
node scripts/md_to_png.js input.md

# 指定输出路径
node scripts/md_to_png.js input.md output.png

# 自定义每页行数（默认 500 行）
node scripts/md_to_png.js input.md output.png 300
```

### 参数说明
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `inputFile` | string | ✅ | - | 输入的 Markdown 文件路径 |
| `outputPath` | string | ✅ | - | 输出图片路径 |
| `maxLinesPerPage` | number | ❌ | 500 | 每页最大行数 |
| `imageQuality` | number | ❌ | 80 | JPEG 图片质量（1-100） |
| `--debug` | flag | ❌ | - | 启用 Debug 模式，输出详细日志并保存分页内容 |

### Debug 模式
使用 `--debug` 参数启用调试模式：
```bash
node scripts/md_to_png.js input.md output.jpg --debug
```

Debug 模式会：
- 输出详细的处理过程日志
- 保存每页分割后的 Markdown 内容到 `output_page_*.md` 文件
- 生成详细的调试日志文件，便于问题排查

### 代码中使用
```javascript
const { convertMarkdown } = require('./scripts/md_to_png.js');

// 转换 Markdown 字符串为图片
const files = await convertMarkdown('# Hello World\n\n这是测试内容', '/tmp/output/');
console.log('生成的图片：', files);
```

## 🔧 配置说明

### 字体配置
- 默认字体：文泉驿微米黑、文泉驿正黑、Noto CJK SC、Noto Color Emoji
- 支持系统字体回退，自动适配环境中的中文字体
- 缺失字体时自动使用系统默认字体替代

### 输出配置
- 输出分辨率：2x（高清，Retina 屏幕友好）
- 最大宽度：900px，兼顾手机和桌面端显示
- 自动适应内容高度，无多余空白
- PNG 格式，无损压缩，文件体积小
- 智能分页，不切断任何内容块

### 安全配置
- 路径遍历防护，禁止输出到非指定目录
- 内容大小限制，最大支持 10MB 输入文件
- 文件名清理，移除非法字符
- 自动清理临时文件，无残留

## 🛠️ 技术栈
- Node.js >= 14
- Puppeteer（无头浏览器，负责截图）
- marked（Markdown 解析器）
- highlight.js（代码语法高亮）
- GitHub 风格 CSS 主题

## 🎯 示例
```bash
# 转换 README.md 为图片
node scripts/md_to_png.js README.md README.png

# 转换长文档，每页 300 行
node scripts/md_to_png.js long_document.md output.png 300

# 转换技术文档，包含大量代码和表格
node scripts/md_to_png.js tech_doc.md tech_doc.png
```

## 📝 注意事项
1. 首次转换需要下载浏览器内核，耗时约 1-2 分钟，后续转换速度快
2. 大文档可能会分成多页，自动添加 `_page1`, `_page2` 后缀
3. 图片文件会占用磁盘空间，建议定期清理输出目录
4. Linux 环境下可能需要安装额外的字体和依赖：
   ```bash
   # Ubuntu/Debian
   sudo apt install fonts-wqy-microhei fonts-wqy-zenhei fonts-noto-color-emoji libnss3 libxss1 libasound2
   ```

## 🤝 贡献
欢迎提交 Issue 和 Pull Request！

## 📄 许可证
MIT License

---
*从 OpenClaw 技能中独立出来的通用项目* 🎉
