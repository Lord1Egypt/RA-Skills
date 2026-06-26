"""
基础测试
"""
import pytest
from parsers.base_parser import (
    FinancialData, 
    ParseResult, 
    normalize_account_name, 
    extract_number
)


class TestFinancialData:
    """测试 FinancialData 类"""
    
    def test_basic_creation(self):
        """测试基本创建"""
        data = FinancialData(
            company_name="测试公司",
            report_period="2024年度"
        )
        assert data.company_name == "测试公司"
        assert data.report_period == "2024年度"
    
    def test_ratio_calculation(self):
        """测试比率计算"""
        data = FinancialData()
        data.balance_sheet = {
            '资产总计': 1000000,
            '负债合计': 500000,
        }
        
        ratio = data.get_ratio('负债合计', '资产总计')
        assert ratio == 0.5
    
    def test_to_dict(self):
        """测试转换为字典"""
        data = FinancialData(company_name="测试")
        result = data.to_dict()
        assert result['company_name'] == "测试"


class TestParseResult:
    """测试 ParseResult 类"""
    
    def test_success_result(self):
        """测试成功结果"""
        result = ParseResult(success=True, file_path="test.xlsx")
        assert result.success is True
        assert result.file_path == "test.xlsx"
    
    def test_add_error(self):
        """测试添加错误"""
        result = ParseResult(success=True, file_path="test.xlsx")
        result.add_error("测试错误")
        assert result.success is False
        assert "测试错误" in result.errors
    
    def test_add_warning(self):
        """测试添加警告"""
        result = ParseResult(success=True, file_path="test.xlsx")
        result.add_warning("测试警告")
        assert "测试警告" in result.warnings


class TestNormalizeAccountName:
    """测试科目名称标准化"""
    
    def test_standard_names(self):
        """测试标准科目"""
        assert normalize_account_name("货币资金") == "货币资金"
        assert normalize_account_name("营业收入") == "营业收入"
    
    def test_alias_names(self):
        """测试别名"""
        assert normalize_account_name("现金及现金等价物") == "货币资金"
        assert normalize_account_name("主营业务收入") == "营业收入"
    
    def test_with_spaces(self):
        """测试带空格的名称"""
        assert normalize_account_name(" 货币资金 ") == "货币资金"


class TestExtractNumber:
    """测试数值提取"""
    
    def test_integer(self):
        """测试整数"""
        assert extract_number(1000) == 1000.0
        assert extract_number("1000") == 1000.0
    
    def test_float(self):
        """测试浮点数"""
        assert extract_number(1234.56) == 1234.56
        assert extract_number("1234.56") == 1234.56
    
    def test_with_comma(self):
        """测试带千分位"""
        assert extract_number("1,000,000") == 1000000.0
        assert extract_number("1，000，000") == 1000000.0
    
    def test_with_currency(self):
        """测试带货币符号"""
        assert extract_number("¥1000") == 1000.0
        assert extract_number("1000元") == 1000.0
    
    def test_negative(self):
        """测试负数"""
        assert extract_number("-1000") == -1000.0
        assert extract_number("(1000)") == -1000.0
    
    def test_invalid(self):
        """测试无效输入"""
        assert extract_number("abc") is None
        assert extract_number(None) is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
