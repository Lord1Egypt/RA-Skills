#!/usr/bin/env python3
"""renumber.py 测试"""
import sys, pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
import renumber

SAMPLE = """# 测试报告

## Part 1 背景

内容

### 1.1 子节

### 1.2 子节

## Part 2 分析

内容

### 2.1 子节

## Part 3 方案

内容
"""


def test_shift_after():
    result = renumber.shift_after(SAMPLE, after_n=1)
    assert '## Part 3' in result
    assert '## Part 4' in result
    assert '### 3.1' in result


def test_shift_after_no_parts():
    with pytest.raises(SystemExit):
        renumber.shift_after('# 无章节', after_n=1)


def test_shift_after_invalid_n():
    with pytest.raises(SystemExit):
        renumber.shift_after(SAMPLE, after_n=99)


def test_fix_numbering():
    broken = "## Part 1\n## Part 3\n## Part 5\n### 5.1 子节\n"
    result = renumber.fix_numbering(broken)
    assert '## Part 1' in result
    assert '## Part 2' in result
    assert '## Part 3' in result
    # Part 5 → Part 3, so 5.1 → 3.1
    assert '### 3.1' in result
    assert '## Part 5' not in result
