# EPUB Chinese Converter Skill

一个万无一失的EPUB繁简转换技能，可以将繁体中文电子书转换为简体中文，或反向转换。

## 特性

✅ **自动依赖管理** - 首次运行自动安装所需库  
✅ **双向转换** - 支持繁→简和简→繁  
✅ **完整转换** - 转换所有文本内容和元数据  
✅ **自动修复** - 修复常见的EPUB结构问题  
✅ **保持格式** - 保留原始排版和样式  

## 安装

将 `epub-converter.skill` 文件放入你的技能目录：

```bash
# 方法1：直接复制
cp epub-converter.skill ~/.openclaw/workspace/skills/

# 方法2：使用OpenClaw安装
openclaw skills install epub-converter.skill
```

## 使用方法

### 在对话中使用

直接向OpenClaw发送EPUB文件并说：

```
"帮我把这本繁体书转成简体"
"将这个EPUB转换为简体中文"
"Convert this to Traditional Chinese"
```

### 命令行使用

也可以直接运行脚本：

```bash
# 繁体转简体（默认）
python3 scripts/convert_epub.py input.epub

# 简体转繁体
python3 scripts/convert_epub.py input.epub --direction s2t

# 指定输出文件名
python3 scripts/convert_epub.py input.epub -o output.epub
```

## 工作原理

1. **自动安装依赖** - 在 `~/.openclaw/epub_venv` 创建虚拟环境
2. **解析EPUB** - 使用 ebooklib 读取电子书结构
3. **转换文本** - 使用 OpenCC 转换所有中文内容
4. **修复结构** - 自动修复目录和元数据问题
5. **保存文件** - 生成新的EPUB文件

## 技术细节

**依赖库：**
- `ebooklib` - EPUB文件处理
- `opencc-python-reimplemented` - 中文繁简转换

**转换范围：**
- ✅ 所有章节内容
- ✅ 书籍元数据（标题、作者等）
- ✅ 目录结构
- ❌ 图片文件（无需转换）
- ❌ CSS样式（无需转换）

## 故障排除

**问题：依赖安装失败**

手动安装：
```bash
python3 -m venv ~/.openclaw/epub_venv
source ~/.openclaw/epub_venv/bin/activate
pip install ebooklib opencc-python-reimplemented
```

**问题：EPUB文件损坏**

脚本会自动修复常见问题：
- 缺失的目录条目ID
- 格式错误的EPUB头
- 编码问题

**问题：转换失败**

检查：
1. 文件是否为有效的EPUB格式（不是PDF）
2. 文件是否有DRM保护
3. 文件大小是否合理（建议<100MB）

## 示例

**基础转换：**
```bash
python3 scripts/convert_epub.py "自我升级第一原理.epub"
# 输出: 自我升级第一原理_简体.epub
```

**自定义输出：**
```bash
python3 scripts/convert_epub.py input.epub -o simplified.epub
```

**反向转换：**
```bash
python3 scripts/convert_epub.py simplified.epub --direction s2t
# 输出: simplified_繁體.epub
```

## 成功标志

转换成功时会显示：
- ✅ 成功读取EPUB
- ✅ 成功转换 X 个文档
- 📝 转换后书名
- 🎉 转换完成！
- 文件大小对比

输出的EPUB可以在任何标准电子书阅读器中打开（Apple Books、Calibre等）。

## 版本信息

- **版本**: 1.0.0
- **创建日期**: 2026-03-13
- **测试状态**: ✅ 已通过实际文件测试

## 许可

MIT License
