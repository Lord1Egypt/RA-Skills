"""Tests for field_identifier.py (F2 · Intelligent field identification)."""
import pytest
import pandas as pd
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from field_identifier import (
    identify_fields, FieldType, FieldInfo,
    _avg_match_score, _gender_score, _date_score, _address_score,
    FIELD_TYPE_LABELS,
)
import re


class TestIdentifyFields:
    def _identify(self, data: dict, **kwargs):
        df = pd.DataFrame(data)
        return identify_fields(df, **kwargs)

    def test_phone(self):
        result = self._identify({"电话": ["13800138000", "13900139000", "13712345678"]})
        assert result["电话"].field_type == FieldType.PHONE
        assert result["电话"].confidence > 0.8

    def test_email(self):
        result = self._identify({"邮箱": ["a@test.com", "b@example.com"]})
        assert result["邮箱"].field_type == FieldType.EMAIL
        # Confidence = 0.7*1.0 + 0.3*0.9 (name bonus)
        assert result["邮箱"].confidence == 0.97

    def test_date(self):
        result = self._identify({"日期": ["2024-01-01", "2024-12-31", "2024/06/15"]})
        assert result["日期"].field_type == FieldType.DATE
        assert result["日期"].confidence > 0.5

    def test_amount(self):
        result = self._identify({"金额": ["¥100.50", "200.00", "¥50"]})
        assert result["金额"].field_type == FieldType.AMOUNT

    def test_gender(self):
        result = self._identify({"性别": ["男", "女", "男", "女"]})
        assert result["性别"].field_type == FieldType.GENDER

    def test_name(self):
        result = self._identify({"姓名": ["张三", "李四", "王五"]})
        assert result["姓名"].field_type == FieldType.NAME

    def test_order_no(self):
        result = self._identify({"订单号": ["DD20240001", "ORDER123456"]})
        assert result["订单号"].field_type == FieldType.ORDER_NO

    def test_unknown_column(self):
        result = self._identify({"乱七八糟列": ["abc", "def"]})
        assert result["乱七八糟列"].field_type in (FieldType.TEXT, FieldType.UNKNOWN)

    def test_custom_rules_override(self):
        result = self._identify(
            {"mycol": ["13800138000", "13900139000"]},
            custom_rules={"mycol": "phone"},
        )
        assert result["mycol"].field_type == FieldType.PHONE
        assert result["mycol"].confidence == 1.0

    def test_sku(self):
        result = self._identify({"SKU": ["SKU12345678", "ABC-12345"]})
        assert result["SKU"].field_type == FieldType.SKU

    def test_ip_address(self):
        result = self._identify({"IP地址": ["192.168.1.1", "10.0.0.1"]})
        assert result["IP地址"].field_type == FieldType.IP_ADDRESS

    def test_id_card(self):
        result = self._identify({"身份证": ["110101199001011234", "11010119900101123X"]})
        assert result["身份证"].field_type == FieldType.ID_CARD


class TestFieldTypeLabels:
    def test_all_types_have_labels(self):
        for ft in FieldType:
            label = FIELD_TYPE_LABELS.get(ft)
            assert label is not None
            assert len(label) > 0


class TestScoreHelpers:
    def test_gender_score(self):
        s = pd.Series(["男", "女", "男", "女", "M", "F"])
        score = _gender_score(s)
        assert score > 0

    def test_gender_score_low_for_random_strings(self):
        s = pd.Series(["asdf", "qwer", "zxcv"])
        score = _gender_score(s)
        assert score < 0.5

    def test_date_score(self):
        s = pd.Series(["2024-01-01", "2024-12-31"])
        score = _date_score(s)
        assert score > 0.5

    def test_address_score(self):
        s = pd.Series(["北京市朝阳区建国路1号", "上海市浦东新区世纪大道100号"])
        score = _address_score(s)
        assert score > 0.5

    def test_address_score_low(self):
        s = pd.Series(["abc", "def", "ghi"])
        score = _address_score(s)
        assert score < 0.2
