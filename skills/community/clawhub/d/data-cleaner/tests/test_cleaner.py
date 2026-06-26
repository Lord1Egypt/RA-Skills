"""Tests for cleaner.py (F3 · Core cleaning engine)."""
import pytest
import pandas as pd
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from cleaner import (
    DataCleaner, clean_dataframe, CleaningReport,
)
from field_identifier import FieldType, FieldInfo


def fi(name: str, ftype: FieldType = FieldType.TEXT, confidence: float = 0.9) -> FieldInfo:
    return FieldInfo(field_type=ftype, confidence=confidence, samples=[])


class TestPhoneFormatting:
    """Phone number format unification."""

    def _clean_phone(self, vals, strategy="auto", dedup="exact"):
        df = pd.DataFrame({"电话": vals})
        field_info = {"电话": fi("电话", FieldType.PHONE)}
        cleaner = DataCleaner(field_info, fill_strategy=strategy, dedup_strategy=dedup)
        result, _ = cleaner.clean(df)
        return result["电话"].tolist()

    def test_formats_various_phones(self):
        # Verify each variant of the same phone normalises to the same output
        # We use monkey-patch to disable deduplication so all rows are preserved
        import cleaner as cmod
        original = cmod.DataCleaner._deduplicate
        def noop(self, df):
            return df, 0, []
        cmod.DataCleaner._deduplicate = noop
        try:
            vals = ["13800138000", "138-0013-8000", "138 0013 8000", "8613800138000"]
            out = self._clean_phone(vals)
            # All should be normalised to the same format
            assert out[0] == "138-0013-8000"
            assert out[1] == "138-0013-8000"
            assert out[2] == "138-0013-8000"
            assert out[3] == "138-0013-8000"
        finally:
            cmod.DataCleaner._deduplicate = original

    def test_unknown_preserved(self):
        out = self._clean_phone(["未知", ""])
        assert "未知" in out


class TestDateFormatting:
    """Date format unification to YYYY-MM-DD."""

    def _clean_date(self, vals):
        df = pd.DataFrame({"日期": vals})
        field_info = {"日期": fi("日期", FieldType.DATE)}
        cleaner = DataCleaner(field_info)
        result, _ = cleaner.clean(df)
        return result["日期"].tolist()

    def test_chinese_format(self):
        out = self._clean_date(["2024年1月5日", "2024年12月31日"])
        assert out[0] == "2024-01-05"
        assert out[1] == "2024-12-31"

    def test_iso_format_unchanged(self):
        out = self._clean_date(["2024-01-05"])
        assert out[0] == "2024-01-05"

    def test_yyyymmdd(self):
        out = self._clean_date(["20240105"])
        assert out[0] == "2024-01-05"

    def test_slash_format(self):
        out = self._clean_date(["2024/01/05"])
        assert out[0] == "2024-01-05"


class TestAmountFormatting:
    """Amount → two decimal places."""

    def _clean_amount(self, vals):
        df = pd.DataFrame({"金额": vals})
        field_info = {"金额": fi("金额", FieldType.AMOUNT)}
        cleaner = DataCleaner(field_info)
        result, _ = cleaner.clean(df)
        return result["金额"].tolist()

    def test_two_decimals(self):
        out = self._clean_amount(["100", "123.4", "¥1,234.56", "$99.9"])
        assert "100.00" in out
        assert "123.40" in out

    def test_currency_symbols_stripped(self):
        out = self._clean_amount(["¥100", "$50.5", "€25"])
        assert "100.00" in out
        assert "50.50" in out


class TestDeduplication:
    """Row deduplication."""

    def test_exact_dedup(self):
        df = pd.DataFrame({
            "姓名": ["张三", "李四", "张三", "王五"],
            "电话": ["138", "139", "138", "140"],
        })
        field_info = {
            "姓名": fi("姓名", FieldType.NAME),
            "电话": fi("电话", FieldType.PHONE),
        }
        cleaner = DataCleaner(field_info, dedup_strategy="exact")
        result, report = cleaner.clean(df)
        assert len(result) == 3
        assert report.duplicates_removed == 1

    def test_no_dedup_when_no_duplicates(self):
        df = pd.DataFrame({"A": [1, 2, 3]})
        field_info = {"A": fi("A", FieldType.NUMBER)}
        cleaner = DataCleaner(field_info)
        result, report = cleaner.clean(df)
        assert len(result) == 3
        assert report.duplicates_removed == 0


class TestMissingImputation:
    """Missing value imputation."""

    def _impute(self, vals, ftype=FieldType.TEXT, strategy="auto"):
        df = pd.DataFrame({"字段": vals})
        field_info = {"字段": fi("字段", ftype)}
        cleaner = DataCleaner(field_info, fill_strategy=strategy)
        result, _ = cleaner.clean(df)
        return result["字段"].tolist()

    def test_gender_mode_fill(self):
        vals = ["男", "女", "男", "", ""]
        out = self._impute(vals, FieldType.GENDER, strategy="mode")
        assert "" not in out

    def test_leave_blank_preserves_nan(self):
        vals = ["abc", "", "def"]
        out = self._impute(vals, strategy="leave_blank")
        assert "" in out

    def test_auto_fill_uses_unknown(self):
        vals = ["name", "", "another"]
        out = self._impute(vals, FieldType.TEXT, strategy="auto")
        assert "未知" in out


class TestAddressStandardisation:
    def _clean_addr(self, vals):
        df = pd.DataFrame({"地址": vals})
        field_info = {"地址": fi("地址", FieldType.ADDRESS)}
        cleaner = DataCleaner(field_info)
        result, _ = cleaner.clean(df)
        return result["地址"].tolist()

    def test_expands_abbrev_province(self):
        out = self._clean_addr(["北京朝阳区建国路1号"])
        assert "北京市" in out[0]

    def test_strips_excess_whitespace(self):
        out = self._clean_addr(["北京市, 朝阳区, 建国路1号"])
        assert "  " not in out[0]


class TestCleanDataframe:
    """Integration: clean_dataframe() convenience function."""

    def test_full_pipeline(self):
        # Rows 0 and 2 are identical on all columns → 1 duplicate removed
        df = pd.DataFrame({
            "姓名": ["张三", "李四", "张三", "王五"],
            "电话": ["13800138000", "13900139000", "13800138000", "14000140000"],
            "金额": ["100.00", "200.50", "100.00", "300.00"],
        })
        field_info = {
            "姓名": fi("姓名", FieldType.NAME),
            "电话": fi("电话", FieldType.PHONE),
            "金额": fi("金额", FieldType.AMOUNT),
        }
        result, report = clean_dataframe(df, field_info)

        assert len(result) == 3       # 1 exact dup removed
        assert report.duplicates_removed == 1
        assert report.formatted_cells > 0
        assert "138-0013-8000" in result["电话"].tolist()


class TestCleaningReport:
    def test_report_fields(self):
        df = pd.DataFrame({"A": [1, 2]})
        field_info = {"A": fi("A", FieldType.NUMBER)}
        cleaner = DataCleaner(field_info)
        _, report = cleaner.clean(df)
        assert isinstance(report, CleaningReport)
        assert report.original_rows == 2
        assert report.duplicates_removed == 0
        assert "原始行数" in report.summary()
