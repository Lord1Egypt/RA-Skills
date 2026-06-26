# Classical Chinese Translator Skill

## Overview
Professional skill for translating Classical Chinese texts to modern vernacular Chinese with high-quality standards (98.5+ points). Supports EPUB/AZW3/MOBI electronic book format conversion, preservation of original structure, and specialized terminology handling for philosophical, medical, and cultivation texts.

## Features
- **High-Quality Translation**: Sentence-by-sentence accurate translation with 98.5+ quality standard
- **Format Preservation**: Maintains original EPUB/HTML structure while replacing content
- **Specialized Terminology**: Handles Daoist, Buddhist, Confucian, and medical terminology with proper explanations
- **Batch Processing**: Processes chapters in batches for quality control
- **Validation**: Built-in XML/EPUB validation to prevent formatting errors
- **Custom Rules**: Configurable translation rules for different text types

## Requirements
- Python 3.6+
- ebooklib library (`pip install ebooklib`)
- lxml library (`pip install lxml`)
- Optional: mobi tools for AZW3 conversion

## Usage Examples

### Basic Translation
```bash
classical-chinese-translator --input book.epub --output translated_book.epub --quality-standard 98.5
```

### With Custom Terminology Dictionary
```bash
classical-chinese-translator --input text.xhtml --output translated.xhtml --terminology-dict daoist_terms.json
```

### Batch Processing
```bash
classical-chinese-translator --input-dir chapters/ --output-dir translated/ --batch-size 3
```

### Format Conversion + Translation
```bash
classical-chinese-translator --convert azw3 --input book.azw3 --output book_translated.epub
```

## Configuration Options

### Quality Standards
- `--quality-standard 98.5`: Enforce high-quality translation rules
- `--modern-syntax-only`: Force completely modern sentence structures
- `--explain-terms`: Automatically explain specialized terminology in parentheses

### Format Handling
- `--preserve-original`: Keep original files as backup
- `--validate-xml`: Validate XML/HTML structure before and after processing
- `--epub-check`: Run epubcheck validation on output

### Special Cases
- `--exclude-patterns`: Exclude specific patterns from translation (e.g., "按：此书旧无作者姓氏.*")
- `--custom-rules`: Apply custom translation rules for specific text types

## Security Considerations
- Input sanitization for XML/HTML content
- Safe file path handling to prevent directory traversal
- Memory limits for large file processing
- No external network calls during processing

## Error Handling
- Detailed error reporting for XML/HTML parsing issues
- Graceful degradation for malformed input files
- Automatic backup creation before processing
- Validation failure rollback

## Performance
- Optimized for large electronic books (1000+ pages)
- Memory-efficient processing for resource-constrained environments
- Parallel processing support for batch operations

## Compatibility
- EPUB 2.0/3.0
- AZW3 (via mobi-tools conversion)
- MOBI (via mobi-tools conversion)
- Plain XHTML/HTML files
- UTF-8 encoded text files

## Quality Assurance
All translations follow the 98.5-point quality standard:
1. Complete vernacular modernization (no classical syntax)
2. Comprehensive terminology explanation
3. Sentence-by-sentence accuracy (not summary/paraphrase)
4. Natural modern Chinese expression
5. Proper handling of cultural and philosophical concepts

## Installation
This skill is compatible with OpenClaw skillhub and can be installed via:
```bash
openclaw skill install classical-chinese-translator
```

Or manually by copying the skill directory to `~/.openclaw/workspace/skills/`