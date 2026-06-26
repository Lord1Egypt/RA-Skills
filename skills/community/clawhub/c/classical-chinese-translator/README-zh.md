# Classical Chinese Translator (文言文翻译器)

## 项目概述
专业文言文翻译技能，基于《道德经讲义》成功翻译项目的经验开发，提供98.5+高质量标准的古典中文到现代白话文翻译服务。

## 功能特性

### 🎯 高质量翻译
- **98.5+质量标准**: 句对句准确翻译，非概括或意译
- **完全白话化**: 彻底避免文言文语序，使用自然现代汉语
- **术语充分解释**: 所有道家、佛家、儒家专业术语都有通俗说明
- **概念通俗化**: 复杂哲学和修炼概念用现代语言清晰表达

### 📚 格式支持
- **EPUB格式**: 完整支持EPUB 2.0/3.0电子书
- **AZW3/MOBI**: 支持Kindle格式转换
- **XHTML/HTML**: 支持网页格式文件
- **批量处理**: 支持章节批次处理确保质量控制

### 🔧 技术特性
- **内置术语词典**: 包含道家内丹修炼、佛家、儒家等专业术语
- **自定义词典**: 支持用户自定义术语解释
- **XML验证**: 内置XML/EPUB结构验证防止格式错误
- **安全设计**: 无网络访问，作用域文件系统访问

## 安装方法

### 通过OpenClaw SkillHub
```bash
openclaw skill install classical-chinese-translator
```

### 手动安装
复制整个目录到OpenClaw技能文件夹：
```bash
cp -r classical-chinese-translator ~/.openclaw/workspace/skills/
```

## 使用方法

### 基础翻译
```bash
classical-chinese-translator --input book.epub --output translated_book.epub --quality-standard 98.5
```

### 自定义术语词典
```bash
classical-chinese-translator --input text.xhtml --output translated.xhtml --terminology-dict daoist_terms.json
```

### 批量处理
```bash
classical-chinese-translator --input-dir chapters/ --output-dir translated/ --batch-size 3
```

## 质量标准 (98.5+分)

所有翻译遵循以下严格标准：
1. **完全白话化** - 无古典语法或句式结构
2. **术语充分解释** - 所有专业术语在括号中解释
3. **句对句准确性** - 精确翻译，非摘要或改写
4. **自然现代汉语** - 流畅、自然的现代语言表达
5. **文化背景准确** - 正确处理哲学和文化概念

## 安全性

本技能注重安全性设计：
- **无外部网络访问**
- **作用域文件系统访问**
- **XML/HTML内容输入验证**
- **安全文件路径处理防止目录遍历**
- **大文件处理内存限制**

## 成功案例

基于《道德经讲义》(黄元吉)的成功翻译项目：
- **82个文件** 全部按98.5+质量标准翻译
- **复杂HTML/XML结构** 完美保持
- **道家内丹术语** 专业处理
- **EPUB格式** 验证和兼容性保证

## 版权声明

**MIT开源协议**: 个人免费使用，商用必须标注来源

Copyright (c) 2026 WalterFeng(https://github.com/MrFengcn)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

**商业使用要求**: 必须在产品文档或关于页面中明确标注"Based on MrFengcn/Classical Chinese Translator Project"并提供项目链接。

## 技术支持

如需技术支持或功能请求，请在[GitHub仓库](https://github.com/MrFengcn/classical-chinese-translator)提交Issue。