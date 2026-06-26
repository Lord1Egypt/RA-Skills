#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOCX Generator Skill - 初始化模块
"""

from .docx_generator import (
    DocxGenerator,
    create_simple_document,
    create_report,
    DocxGeneratorError,
    ValidationError
)

__all__ = [
    'DocxGenerator',
    'create_simple_document',
    'create_report',
    'DocxGeneratorError',
    'ValidationError'
]

__version__ = '2.0.0'
