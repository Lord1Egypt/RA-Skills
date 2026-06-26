"""Tests for parser.py (F1 · Multi-format parsing)."""
import pytest
import pandas as pd
import tempfile
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from parser import (
    parse_file, parse_text, _sniff_delimiter, _is_json,
    _parse_csv_str, _parse_json_str, _json_to_df,
    preview_text, load_sources,
)


class TestParseText:
    """parse_text() — clipboard / pasted text parsing."""

    def test_csv_basic(self):
        text = "姓名,年龄\n张三,25\n李四,30"
        df = parse_text(text)
        assert len(df) == 2
        assert list(df.columns) == ["姓名", "年龄"]
        assert df["姓名"][0] == "张三"

    def test_tsv(self):
        text = "姓名\t年龄\n王五\t28"
        df = parse_text(text)
        assert "姓名" in df.columns

    def test_json_array(self):
        text = '[{"name":"Alice","age":30},{"name":"Bob","age":25}]'
        df = parse_text(text)
        assert len(df) == 2
        assert "name" in df.columns or "name" in df.columns.str.lower()

    def test_json_object(self):
        text = '{"rows":[{"name":"Alice"},{"name":"Bob"}]}'
        df = parse_text(text)
        assert len(df) == 2

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="粘贴内容为空"):
            parse_text("")

    def test_strips_whitespace(self):
        text = "  姓名 , 年龄 \n  张三 , 25 "
        df = parse_text(text)
        assert df.columns[0].strip() == "姓名"


class TestParseFile:
    """parse_file() — file-based parsing."""

    def test_csv_roundtrip(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv",
                                          delete=False) as f:
            f.write("姓名,电话\n张三,13800138000\n李四,13900139000")
            path = f.name

        try:
            df = parse_file(path)
            assert len(df) == 2
            assert "姓名" in df.columns
        finally:
            Path(path).unlink()

    def test_xlsx_roundtrip(self):
        pytest.importorskip("openpyxl")
        df_orig = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            df_orig.to_excel(f.name, index=False)
            path = f.name

        try:
            df = parse_file(path)
            assert len(df) == 2
        finally:
            Path(path).unlink()

    def test_json_roundtrip(self):
        data = [{"name": "Alice", "score": 95}]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                          delete=False) as f:
            json.dump(data, f)
            path = f.name

        try:
            df = parse_file(path)
            assert len(df) == 1
        finally:
            Path(path).unlink()


class TestSniffDelimiter:
    def test_comma(self):
        assert _sniff_delimiter("a,b,c\n1,2,3") == ","

    def test_tab(self):
        assert _sniff_delimiter("a\tb\tc\n1\t2\t3") == "\t"


class TestIsJson:
    def test_array(self):
        assert _is_json('[{"a":1}]') is True

    def test_object(self):
        assert _is_json('{"a":1}') is True

    def test_not_json(self):
        assert _is_json("name,age\nAlice,30") is False


class TestLoadSources:
    def test_texts_only(self):
        texts = ["a,b\n1,2", "c,d\n3,4"]
        results = load_sources(sources=[], texts=texts)
        assert len(results) == 2
        assert results[0][0] == "粘贴数据_1"


class TestPreview:
    def test_preview_text(self):
        text = "\n".join([f"row_{i}" for i in range(100)])
        df = preview_text(text, n=5)
        assert len(df) == 5
