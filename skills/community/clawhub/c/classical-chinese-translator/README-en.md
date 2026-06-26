# Classical Chinese Translator

## Project Overview
Professional Classical Chinese translation skill developed based on the successful 《Tao Te Ching Commentary》 translation project, providing high-quality (98.5+ standard) translation service from Classical Chinese to modern vernacular Chinese.

## Features

### 🎯 High-Quality Translation
- **98.5+ Quality Standard**: Sentence-by-sentence accurate translation, not summary or paraphrase
- **Complete Vernacular Modernization**: Completely avoids classical Chinese syntax, uses natural modern Chinese
- **Comprehensive Terminology Explanation**: All Daoist, Buddhist, and Confucian specialized terms have clear explanations
- **Concept Simplification**: Complex philosophical and cultivation concepts expressed clearly in modern language

### 📚 Format Support
- **EPUB Format**: Full support for EPUB 2.0/3.0 e-books
- **AZW3/MOBI**: Supports Kindle format conversion
- **XHTML/HTML**: Supports web format files
- **Batch Processing**: Supports chapter batch processing for quality control

### 🔧 Technical Features
- **Built-in Terminology Dictionary**: Includes Daoist inner alchemy, Buddhist, Confucian and other specialized terms
- **Custom Dictionary**: Supports user-defined terminology explanations
- **XML Validation**: Built-in XML/EPUB structure validation to prevent formatting errors
- **Security Design**: No network access, scoped file system access

## Installation

### Via OpenClaw SkillHub
```bash
openclaw skill install classical-chinese-translator
```

### Manual Installation
Copy the entire directory to your OpenClaw skills folder:
```bash
cp -r classical-chinese-translator ~/.openclaw/workspace/skills/
```

## Usage

### Basic Translation
```bash
classical-chinese-translator --input book.epub --output translated_book.epub --quality-standard 98.5
```

### Custom Terminology Dictionary
```bash
classical-chinese-translator --input text.xhtml --output translated.xhtml --terminology-dict daoist_terms.json
```

### Batch Processing
```bash
classical-chinese-translator --input-dir chapters/ --output-dir translated/ --batch-size 3
```

## Quality Standard (98.5+ Points)

All translations follow these strict standards:
1. **Complete Vernacular Modernization** - No classical grammar or sentence structures
2. **Comprehensive Terminology Explanation** - All specialized terms explained in parentheses
3. **Sentence-by-Sentence Accuracy** - Precise translation, not summary or rewriting
4. **Natural Modern Chinese Expression** - Fluent, natural modern language expression
5. **Cultural Context Accuracy** - Proper handling of philosophical and cultural concepts

## Security

This skill is designed with security in mind:
- **No external network access**
- **Scoped file system access**
- **XML/HTML content input validation**
- **Safe file path handling to prevent directory traversal**
- **Memory limits for large file processing**

## Success Case

Based on the successful translation of 《Tao Te Ching Commentary》 (Huang Yuanji's commentary):
- **82 files** all translated with 98.5+ quality standard
- **Complex HTML/XML structure** perfectly preserved
- **Daoist inner alchemy terminology** professionally handled
- **EPUB format** validation and compatibility guaranteed

## Copyright Notice

**MIT Open Source License**: Free for personal use, commercial use must credit the source

Copyright (c) 2026 WalterFeng(https://github.com/MrFengcn)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

**Commercial Use Requirement**: Must clearly state "Based on MrFengcn/Classical Chinese Translator Project" in product documentation or about page with project link.

## Support

For technical support or feature requests, please open an issue on the [GitHub repository](https://github.com/MrFengcn/classical-chinese-translator).