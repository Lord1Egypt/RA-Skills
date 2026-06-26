# 🚀 EPUB Converter 快速安装指南

## 一键安装

```bash
# 下载并安装技能
cp epub-converter.skill ~/.openclaw/workspace/skills/
```

## 验证安装

```bash
cd ~/.openclaw/workspace/skills/epub-converter
./test_skill.sh
```

## 立即使用

### 方法1：在OpenClaw对话中
直接上传EPUB文件并说：
```
"帮我把这本繁体书转成简体"
```

### 方法2：命令行
```bash
python3 ~/.openclaw/workspace/skills/epub-converter/scripts/convert_epub.py your_book.epub
```

## 首次运行

首次运行时会自动：
1. 创建虚拟环境（~/.openclaw/epub_venv）
2. 安装依赖库（ebooklib, opencc-python-reimplemented）
3. 执行转换

**预计耗时：** 30-60秒（仅首次）

## 完成！

现在你可以：
- ✅ 转换任何EPUB电子书的繁简体
- ✅ 在对话中直接使用
- ✅ 命令行批量处理
- ✅ 自动修复EPUB结构问题

## 需要帮助？

查看详细文档：
- `README.md` - 完整使用指南
- `EXAMPLES.md` - 实际使用案例
- `SKILL_SUMMARY.md` - 技能总结

---

**安装时间：** < 1分钟  
**学习时间：** < 5分钟  
**使用难度：** ⭐☆☆☆☆ (非常简单)
