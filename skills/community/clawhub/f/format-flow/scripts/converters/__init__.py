#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
转换器模块
"""

from .word_to_pdf import (
    convert_word_to_pdf,
    batch_convert_word_to_pdf
)

from .word_to_markdown import (
    convert_word_to_markdown,
    batch_convert_word_to_markdown
)

from .pdf_to_markdown import (
    convert_pdf_to_markdown,
    batch_convert_pdf_to_markdown
)

from .markdown_to_word import (
    convert_markdown_to_word,
    batch_convert_markdown_to_word
)

from .web_to_markdown import (
    convert_url_to_markdown,
    convert_html_file_to_markdown,
    batch_convert_urls_to_markdown
)

from .text_formatter import (
    format_notes,
    batch_format_notes
)

from .excel_to_json import (
    convert_excel_to_json,
    batch_convert_excel_to_json,
    get_sheet_names
)

from .image_processor import (
    compress_image,
    convert_image_format,
    resize_image,
    rotate_image,
    crop_image,
    batch_compress_images,
    batch_convert_format
)

__all__ = [
    # Word ↔ PDF ↔ Markdown
    'convert_word_to_pdf',
    'batch_convert_word_to_pdf',
    'convert_word_to_markdown',
    'batch_convert_word_to_markdown',
    'convert_pdf_to_markdown',
    'batch_convert_pdf_to_markdown',
    'convert_markdown_to_word',
    'batch_convert_markdown_to_word',
    
    # Web → Markdown
    'convert_url_to_markdown',
    'convert_html_file_to_markdown',
    'batch_convert_urls_to_markdown',
    
    # Text Formatter
    'format_notes',
    'batch_format_notes',
    
    # Excel → JSON
    'convert_excel_to_json',
    'batch_convert_excel_to_json',
    'get_sheet_names',
    
    # Image Processor
    'compress_image',
    'convert_image_format',
    'resize_image',
    'rotate_image',
    'crop_image',
    'batch_compress_images',
    'batch_convert_format',
]
