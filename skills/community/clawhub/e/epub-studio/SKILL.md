---
name: epub-studio
description: EPUB电子书生成器。Use when user wants to create professional EPUB ebooks from Markdown, text, or structured content. Supports chapters, TOC, cover image, metadata. 电子书、EPUB制作。
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "📚", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install ebooklib"
---

# EPUB Studio

专业EPUB电子书生成器，支持Markdown转EPUB、多章节、目录、封面。

## Features

- 📚 **EPUB格式**: 标准EPUB 3.0格式
- 📑 **多章节**: 自动生成章节
- 📋 **目录**: 自动生成TOC
- 🖼️ **封面**: 支持封面图片
- 📝 **Markdown输入**: 从Markdown生成
- ✅ **跨平台**: 支持所有电子书阅读器

## Trigger Conditions

- "生成电子书" / "Create ebook"
- "做一本EPUB" / "Make EPUB"
- "Markdown转EPUB"
- "epub-studio"

---

## Python Code

```python
import os
from ebooklib import epub

class EpubGenerator:
    def __init__(self, title, author='Unknown', language='zh'):
        self.book = epub.EpubBook()
        self.book.set_title(title)
        self.book.set_language(language)
        self.book.add_author(author)
        self.chapters = []
        
    def add_chapter(self, title, content, filename=None):
        """Add a chapter"""
        if filename is None:
            filename = f'chapter_{len(self.chapters)+1}.xhtml'
        
        chapter = epub.EpubHtml(title=title, file_name=filename)
        chapter.content = f'<h1>{title}</h1>{content}'
        
        self.book.add_item(chapter)
        self.chapters.append(chapter)
        return chapter
    
    def add_markdown_chapters(self, markdown_content):
        """Split markdown into chapters"""
        sections = markdown_content.split('\n# ')
        
        for i, section in enumerate(sections):
            if not section.strip():
                continue
            
            lines = section.split('\n')
            title = lines[0].replace('#', '').strip()
            content = '<br>'.join(lines[1:])
            
            self.add_chapter(title, content)
    
    def add_cover(self, image_path):
        """Add cover image"""
        with open(image_path, 'rb') as f:
            cover_image = f.read()
        
        self.book.set_cover('cover.jpg', cover_image)
    
    def set_toc(self):
        """Generate table of contents"""
        self.book.toc = self.chapters
        
        # Add navigation
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
    
    def add_spine(self):
        """Set reading order"""
        self.book.spine = ['nav'] + self.chapters
    
    def save(self, output_path):
        """Save EPUB file"""
        self.set_toc()
        self.add_spine()
        
        epub.write_epub(output_path, self.book, {})
        return output_path

# Example
gen = EpubGenerator('My Book', author='Author Name')
gen.add_chapter('Chapter 1', '<p>Content here...</p>')
gen.add_chapter('Chapter 2', '<p>More content...</p>')
gen.save('output.epub')
```

---

## Usage

```
User: "帮我把这篇Markdown做成电子书"
Agent: 使用 EpubGenerator 生成EPUB

User: "创建一本3章的电子书"
Agent: 分章生成EPUB
```

---

## Notes

- 使用ebooklib库
- 支持标准EPUB 3.0格式
- 兼容所有电子书阅读器
- 支持中英文
