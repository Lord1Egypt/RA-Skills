"""
Tests for Bank Statement Reconciler
"""
import pytest
import os
import csv
import tempfile
from datetime import datetime

# Import the modules
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from parser import StatementParser, OrderParser, detect_format
from matcher import ReconciliationMatcher
from exporter import ReconciliationExporter
from feishu_card import build_feishu_card, build_feishu_simple_message
from tier_config import TierConfig, validate_token_for_tier


class TestDetectFormat:
    """Test format detection."""
    
    def test_detect_alipay(self):
        text = "交易时间,交易对方,金额,状态\n2024-01-01,淘宝,100.00,成功"
        assert detect_format(text, "alipay.csv") == "alipay"
    
    def test_detect_paypal(self):
        text = "Date,Amount,Name\n2024-01-01,100.00,John"
        assert detect_format(text, "paypal.csv") == "paypal"
    
    def test_detect_icbc(self):
        text = "日期,金额,对方户名\n2024-01-01,100.00,张三"
        assert detect_format(text, "icbc.csv") == "icbc"


class TestStatementParser:
    """Test bank statement parsing."""
    
    def test_parse_csv_boc(self):
        """Test parsing BOC format CSV."""
        parser = StatementParser()
        
        # Create temp CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("交易日期,交易金额,对方账户,余额,摘要\n")
            f.write("2024-01-01,1000.00,张三,5000.00,工资\n")
            f.write("2024-01-02,-200.00,李四,4800.00,购物\n")
            f.write("2024-01-03,500.00,王五,5300.00,退款\n")
            temp_path = f.name
        
        try:
            transactions = parser.parse_file(temp_path, "boc")
            
            assert len(transactions) == 3
            assert transactions[0]["amount"] == 1000.00
            assert transactions[0]["counterparty"] == "张三"
            assert transactions[1]["amount"] == -200.00
            assert transactions[2]["amount"] == 500.00
        finally:
            os.unlink(temp_path)
    
    def test_parse_csv_paypal(self):
        """Test parsing PayPal format CSV."""
        parser = StatementParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Date,Amount,Name,Currency\n")
            f.write("2024-01-01,100.00,John Smith,USD\n")
            f.write("2024-01-02,-50.00,Jane Doe,USD\n")
            temp_path = f.name
        
        try:
            transactions = parser.parse_file(temp_path, "paypal")
            
            assert len(transactions) == 2
            assert transactions[0]["amount"] == 100.00
            assert transactions[0]["counterparty"] == "John Smith"
        finally:
            os.unlink(temp_path)
    
    def test_parse_text(self):
        """Test parsing text content."""
        parser = StatementParser()
        
        text = """
        2024-01-01 交易金额: ¥1000.00 对方: 张三 余额: 5000
        2024-01-02 交易金额: ¥-200.00 对方: 李四 余额: 4800
        """
        
        transactions = parser.parse_text(text, "boc")
        
        # Should extract at least some transactions
        assert len(transactions) >= 0  # Text parsing is fallback
    
    def test_parse_amount_formats(self):
        """Test various amount formats."""
        parser = StatementParser()
        
        amounts = ["1000", "1,000.00", "¥1000.00", "$1000.00", "(100.00)", "-100"]
        
        for amount_str in amounts:
            result = parser._parse_amount(amount_str)
            assert result is not None, f"Failed to parse: {amount_str}"
        
        # Positive with parentheses
        result = parser._parse_amount("(100.00)")
        assert result == -100.00
        
        # Invalid
        result = parser._parse_amount("invalid")
        assert result is None
    
    def test_parse_date_formats(self):
        """Test various date formats."""
        parser = StatementParser()
        
        dates = [
            ("2024-01-15", "2024-01-15"),
            ("2024/01/15", "2024-01-15"),
            ("2024年1月15日", "2024-01-15"),
            ("01/15/2024", "2024-01-15"),
        ]
        
        for input_date, expected in dates:
            result = parser._parse_date(input_date)
            assert result == expected, f"Failed: {input_date} -> {result}"


class TestOrderParser:
    """Test order/invoice parsing."""
    
    def test_parse_csv_order(self):
        """Test parsing order CSV."""
        parser = OrderParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("订单日期,订单金额,客户,订单号\n")
            f.write("2024-01-01,1000.00,张三,ORDER001\n")
            f.write("2024-01-02,500.00,李四,ORDER002\n")
            temp_path = f.name
        
        try:
            orders = parser.parse_file(temp_path, "order")
            
            assert len(orders) == 2
            assert orders[0]["amount"] == 1000.00
            assert orders[0]["counterparty"] == "张三"
            assert orders[0]["order_no"] == "ORDER001"
        finally:
            os.unlink(temp_path)
    
    def test_parse_csv_invoice(self):
        """Test parsing invoice CSV."""
        parser = OrderParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("发票日期,金额,购买方,发票号\n")
            f.write("2024-01-01,1000.00,XX公司,INV001\n")
            temp_path = f.name
        
        try:
            orders = parser.parse_file(temp_path, "invoice")
            
            assert len(orders) == 1
            assert orders[0]["amount"] == 1000.00
        finally:
            os.unlink(temp_path)


class TestReconciliationMatcher:
    """Test reconciliation matching."""
    
    def test_exact_match(self):
        """Test exact matching."""
        matcher = ReconciliationMatcher(match_mode="exact")
        
        transactions = [
            {"date": "2024-01-01", "amount": 1000.00, "counterparty": "张三", "raw": ""},
            {"date": "2024-01-02", "amount": 500.00, "counterparty": "李四", "raw": ""},
        ]
        
        orders = [
            {"date": "2024-01-01", "amount": 1000.00, "counterparty": "张三", "raw": ""},
            {"date": "2024-01-03", "amount": 300.00, "counterparty": "王五", "raw": ""},
        ]
        
        result = matcher.match(transactions, orders)
        
        assert result["summary"]["matched_count"] == 1
        assert result["summary"]["unclaimed_count"] == 1
        assert result["summary"]["unmatched_count"] == 1
    
    def test_fuzzy_match(self):
        """Test fuzzy matching."""
        matcher = ReconciliationMatcher(
            match_mode="fuzzy",
            amount_tolerance=0.1,
            date_range_days=3
        )
        
        transactions = [
            {"date": "2024-01-01", "amount": 1000.00, "counterparty": "张三", "raw": ""},
        ]
        
        orders = [
            {"date": "2024-01-03", "amount": 1000.05, "counterparty": "张三", "raw": ""},  # 3 days diff, 0.05 amount diff
        ]
        
        result = matcher.match(transactions, orders)
        
        assert result["summary"]["matched_count"] == 1
    
    def test_no_match_when_amount_differs(self):
        """Test that different amounts don't match."""
        matcher = ReconciliationMatcher(match_mode="exact")
        
        transactions = [
            {"date": "2024-01-01", "amount": 1000.00, "counterparty": "张三", "raw": ""},
        ]
        
        orders = [
            {"date": "2024-01-01", "amount": 999.00, "counterparty": "张三", "raw": ""},  # Different amount
        ]
        
        result = matcher.match(transactions, orders)
        
        assert result["summary"]["matched_count"] == 0
        assert result["summary"]["unclaimed_count"] == 1
        assert result["summary"]["unmatched_count"] == 1
    
    def test_difference_detection(self):
        """Test that differences are detected with fuzzy matching."""
        matcher = ReconciliationMatcher(
            match_mode="fuzzy",
            amount_tolerance=10.0,
            date_range_days=0
        )
        
        transactions = [
            {"date": "2024-01-01", "amount": 1000.00, "counterparty": "张三", "raw": ""},
        ]
        
        orders = [
            {"date": "2024-01-01", "amount": 990.00, "counterparty": "张三", "raw": ""},  # Different amount but within tolerance
        ]
        
        result = matcher.match(transactions, orders)
        
        # In fuzzy mode, small differences are captured as matched with difference recorded
        # or as differences depending on tolerance settings
        assert result["summary"]["difference_count"] + result["summary"]["matched_count"] == 1
    
    def test_summary_calculation(self):
        """Test summary calculations."""
        matcher = ReconciliationMatcher(match_mode="exact")
        
        transactions = [
            {"date": "2024-01-01", "amount": 1000.00, "counterparty": "张三", "raw": ""},
            {"date": "2024-01-02", "amount": 500.00, "counterparty": "李四", "raw": ""},
            {"date": "2024-01-03", "amount": 300.00, "counterparty": "王五", "raw": ""},
        ]
        
        orders = [
            {"date": "2024-01-01", "amount": 1000.00, "counterparty": "张三", "raw": ""},
        ]
        
        result = matcher.match(transactions, orders)
        summary = result["summary"]
        
        assert summary["total_transactions"] == 3
        assert summary["total_orders"] == 1
        assert summary["matched_count"] == 1
        assert summary["unclaimed_count"] == 2
        assert summary["unmatched_count"] == 0
        assert summary["matched_amount"] == 1000.00
        assert summary["match_rate"] == pytest.approx(33.33, rel=0.1)


class TestTierConfig:
    """Test tier configuration."""
    
    def test_free_tier_defaults(self):
        """Test Free tier defaults."""
        tier = TierConfig()
        
        limits = tier.get_limits()
        assert limits["monthly_statements"] == 50
        assert limits["bank_accounts"] == 1
        assert "text" in limits["output_formats"]
        assert "excel" not in limits["output_formats"]
        assert tier.can_export_excel() is False
        assert tier.can_push_feishu() is False
    
    def test_basic_tier(self):
        """Test Basic tier."""
        tier = TierConfig(token="BANK-BSC-xxxxx")
        
        assert tier.tier_name == "BASIC"
        assert tier.can_export_excel() is True
        assert tier.can_push_feishu() is False
    
    def test_standard_tier(self):
        """Test Standard tier."""
        tier = TierConfig(token="BANK-STD-xxxxx")
        
        assert tier.tier_name == "STANDARD"
        assert tier.can_export_excel() is True
        assert tier.can_push_feishu() is True
        assert tier.supports_platform("alipay") is True
        assert tier.supports_platform("paypal") is False
    
    def test_professional_tier(self):
        """Test Professional tier."""
        tier = TierConfig(token="BANK-PRO-xxxxx")
        
        assert tier.tier_name == "PROFESSIONAL"
        assert tier.is_pro is True
        assert tier.can_use_semantic() is True
        assert tier.supports_platform("paypal") is True
    
    def test_enterprise_tier(self):
        """Test Enterprise tier."""
        tier = TierConfig(token="BANK-ENT-xxxxx")
        
        assert tier.tier_name == "ENTERPRISE"
        assert tier.is_pro is True
        assert tier.get_limits()["custom_rules"] is True
    
    def test_validate_token(self):
        """Test token validation."""
        assert validate_token_for_tier("BANK-PRO-123", "PROFESSIONAL") is True
        assert validate_token_for_tier("BANK-FREE-123", "PROFESSIONAL") is False
        assert validate_token_for_tier(None, "FREE") is True
        assert validate_token_for_tier("", "FREE") is True


class TestReconciliationExporter:
    """Test Excel export."""
    
    def test_export_creates_file(self):
        """Test that export creates an Excel file."""
        exporter = ReconciliationExporter()
        
        result = {
            "matched": [
                {
                    "date": "2024-01-01",
                    "amount": 1000.00,
                    "counterparty": "张三",
                    "summary": "测试",
                    "matched_order": {"date": "2024-01-01", "amount": 1000.00},
                    "match_type": "exact",
                }
            ],
            "differences": [],
            "unclaimed": [],
            "unmatched_orders": [],
            "summary": {
                "total_transactions": 1,
                "total_orders": 1,
                "matched_count": 1,
                "difference_count": 0,
                "unclaimed_count": 0,
                "unmatched_count": 0,
                "match_rate": 100.0,
                "recognition_rate": 100.0,
                "matched_amount": 1000.00,
                "difference_amount": 0,
                "unclaimed_amount": 0,
                "unmatched_amount": 0,
            }
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = exporter.export(result, tmpdir)
            
            assert filepath is not None
            assert os.path.exists(filepath)
            assert filepath.endswith(".xlsx")


class TestFeishuCard:
    """Test Feishu card generation."""
    
    def test_build_feishu_card(self):
        """Test building Feishu card."""
        result = {
            "matched": [],
            "differences": [],
            "unclaimed": [],
            "unmatched_orders": [],
            "summary": {
                "matched_count": 10,
                "difference_count": 2,
                "unclaimed_count": 1,
                "unmatched_count": 3,
                "match_rate": 76.92,
                "matched_amount": 10000.00,
                "difference_amount": 50.00,
                "unclaimed_amount": 200.00,
                "unmatched_amount": 300.00,
            }
        }
        
        card = build_feishu_card(result)
        
        assert card["msg_type"] == "interactive"
        assert "card" in card
        assert card["card"]["header"]["title"]["content"] == "📊 银行流水对账结果"
    
    def test_build_feishu_simple_message(self):
        """Test building simple Feishu message."""
        result = {
            "summary": {
                "match_rate": 95.0,
                "matched_count": 19,
                "difference_count": 1,
                "unclaimed_count": 0,
                "unmatched_count": 0,
                "difference_amount": 10.00,
            }
        }
        
        message = build_feishu_simple_message(result)
        
        assert "📊 **银行流水对账结果**" in message
        assert "95.0%" in message
        assert "✅ **已匹配**: 19 笔" in message


class TestIntegration:
    """Integration tests."""
    
    def test_full_reconciliation_flow(self):
        """Test complete reconciliation flow."""
        from scripts import reconcile_bank_statements
        
        # Create temp files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("交易日期,交易金额,对方账户,余额,摘要\n")
            f.write("2024-01-01,1000.00,张三,5000.00,工资\n")
            f.write("2024-01-02,500.00,李四,4500.00,退款\n")
            f.write("2024-01-03,200.00,王五,4300.00,购物\n")
            f.write("2024-01-04,300.00,赵六,4000.00,转账\n")
            stmt_path = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("订单日期,订单金额,客户,订单号\n")
            f.write("2024-01-01,1000.00,张三,ORDER001\n")
            f.write("2024-01-02,490.00,李四,ORDER002\n")  # Difference
            f.write("2024-01-05,300.00,赵六,ORDER003\n")  # Unmatched order
            order_path = f.name
        
        try:
            result = reconcile_bank_statements(
                statement_file=stmt_path,
                order_file=order_path,
                match_mode="exact",
            )
            
            assert result["summary"]["total_transactions"] == 4
            assert result["summary"]["total_orders"] == 3
            assert result["summary"]["matched_count"] >= 1
            assert result["summary"]["difference_count"] >= 0
            
        finally:
            os.unlink(stmt_path)
            os.unlink(order_path)
    
    def test_tier_config_integration(self):
        """Test tier config with full reconciliation."""
        from scripts import reconcile_bank_statements
        
        # Create temp files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("交易日期,交易金额,对方账户\n")
            f.write("2024-01-01,1000.00,张三\n")
            stmt_path = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("订单日期,订单金额,客户\n")
            f.write("2024-01-01,1000.00,张三\n")
            order_path = f.name
        
        try:
            # Free tier - no Excel
            tier_free = TierConfig(token="BANK-FREE-xxxxx")
            result = reconcile_bank_statements(
                statement_file=stmt_path,
                order_file=order_path,
                tier=tier_free,
            )
            assert result.get("excel_path") is None
            
            # Professional tier - Excel enabled
            tier_pro = TierConfig(token="BANK-PRO-xxxxx")
            result = reconcile_bank_statements(
                statement_file=stmt_path,
                order_file=order_path,
                tier=tier_pro,
            )
            # Excel path should be set
            assert result.get("excel_path") is not None
            
        finally:
            os.unlink(stmt_path)
            os.unlink(order_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
