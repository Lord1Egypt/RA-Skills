#!/usr/bin/env python3
"""validate.py 测试"""
import sys, json, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
import validate

VALID = """# 报告

## 目录

- [Part 1 背景](#part-1-背景)
- [Part 2 分析](#part-2-分析)

## Part 1 背景

内容

### 1.1 详情

内容

## Part 2 分析

| 列1 | 列2 |
|-----|-----|
| A   | B   |
"""


def test_toc_consistency_pass():
    hds = validate.headings(VALID)
    ok, detail = validate.check_toc(VALID, hds)
    assert ok


def test_number_continuity_pass():
    hds = validate.headings(VALID)
    ok, detail = validate.check_numbers(hds)
    assert ok


def test_number_continuity_gap():
    hds = validate.headings("## Part 1\n## Part 3\n")
    ok, detail = validate.check_numbers(hds)
    assert not ok


def test_empty_sections():
    empty_doc = "## Part 1 标题\n\n## Part 2 有内容\n\n正文"
    hds = validate.headings(empty_doc)
    ok, detail = validate.check_empty(empty_doc, hds)
    assert not ok


def test_tables_detected():
    ok, detail = validate.check_tables(VALID)
    assert ok
    assert '1 个' in str(detail)


def test_full_report_structure():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(VALID)
        f.flush()
        report = validate.validate(f.name)
    assert 'report' in report
    assert 'summary' in report
    assert 'checks' in report
    assert len(report['checks']) == 5
    Path(f.name).unlink()
