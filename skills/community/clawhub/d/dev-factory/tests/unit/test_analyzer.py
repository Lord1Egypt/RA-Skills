"""Cycle 6: Analyzer regex 강화 테스트"""

import pytest
from builder.correction.analyzer import ErrorAnalyzer


@pytest.fixture
def analyzer():
    return ErrorAnalyzer()


@pytest.mark.parametrize("error_output,expected_file,expected_line", [
    ('File "src/main.py", line 10', "src/main.py", 10),
    ("src/main.py:10: error: undefined variable", "src/main.py", 10),
    ('  File "src/main.py", line 10, in some_function', "src/main.py", 10),
    ("unknown format without file info", None, None),
])
def test_error_location_parsed_correctly(analyzer, error_output, expected_file, expected_line):
    file_path, line_number = analyzer._extract_location(error_output)
    assert file_path == expected_file
    assert line_number == expected_line


def test_extract_location_standard_format(analyzer):
    output = 'Traceback (most recent call last):\n  File "src/main.py", line 42, in func\n    x = y[1]\nKeyError: 1'
    file_path, line_number = analyzer._extract_location(output)
    assert file_path == "src/main.py"
    assert line_number == 42


def test_extract_location_short_format(analyzer):
    output = "src/utils.py:15: error: name 'foo' is not defined"
    file_path, line_number = analyzer._extract_location(output)
    assert file_path == "src/utils.py"
    assert line_number == 15


def test_extract_location_indented_format(analyzer):
    output = '  File "tests/test_main.py", line 7, in test_func'
    file_path, line_number = analyzer._extract_location(output)
    assert file_path == "tests/test_main.py"
    assert line_number == 7


def test_extract_location_unknown_format(analyzer):
    file_path, line_number = analyzer._extract_location("some random error text")
    assert file_path is None
    assert line_number is None


def test_extract_location_prefers_first_match(analyzer):
    """여러 파일 경로가 있을 때 첫 번째 match 반환"""
    output = 'File "src/a.py", line 1\nFile "src/b.py", line 2'
    file_path, line_number = analyzer._extract_location(output)
    assert file_path == "src/a.py"
    assert line_number == 1
