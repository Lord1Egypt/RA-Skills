"""
Bank Statement Reconciler - Core Module
"""
from .parser import StatementParser, OrderParser, detect_format
from .matcher import ReconciliationMatcher
from .exporter import ReconciliationExporter
from .feishu_card import build_feishu_card
from .tier_config import TierConfig

__all__ = [
    "StatementParser",
    "OrderParser", 
    "ReconciliationMatcher",
    "ReconciliationExporter",
    "build_feishu_card",
    "TierConfig",
    "detect_format",
    "reconcile_bank_statements",
]


def reconcile_bank_statements(
    statement_file=None,
    statement_text=None,
    order_file=None,
    order_text=None,
    statement_type="auto",
    order_type="auto",
    match_mode="smart",
    amount_tolerance=0.01,
    date_range_days=3,
    tier=None,
):
    """
    Main entry point for bank statement reconciliation.
    
    Args:
        statement_file: Path to bank statement file
        statement_text: Raw bank statement text (alternative to file)
        order_file: Path to orders/invoices file
        order_text: Raw order text (alternative to file)
        statement_type: "auto", "boc", "icbc", "ccb", "alipay", "wechat", "paypal", "stripe", "amazon", "shopify", "temu"
        order_type: "auto", "invoice", "order"
        match_mode: "exact", "fuzzy", "smart"
        amount_tolerance: Amount tolerance for fuzzy matching (CNY)
        date_range_days: Date range for fuzzy matching
        tier: TierConfig instance
    
    Returns:
        dict with keys: matched, differences, unclaimed, unmatched_orders, summary, excel_path
    """
    if tier is None:
        tier = TierConfig()
    
    # Parse statements
    stmt_parser = StatementParser()
    if statement_file:
        transactions = stmt_parser.parse_file(statement_file, statement_type)
    else:
        transactions = stmt_parser.parse_text(statement_text, statement_type)
    
    # Parse orders
    ord_parser = OrderParser()
    if order_file:
        orders = ord_parser.parse_file(order_file, order_type)
    else:
        orders = ord_parser.parse_text(order_text, order_type)
    
    # Match
    matcher = ReconciliationMatcher(
        match_mode=match_mode,
        amount_tolerance=amount_tolerance,
        date_range_days=date_range_days,
        tier=tier,
    )
    result = matcher.match(transactions, orders)
    
    # Export Excel if tier supports
    excel_path = None
    if tier.can_export_excel() and (result["matched"] or result["differences"] or result["unclaimed"] or result["unmatched_orders"]):
        exporter = ReconciliationExporter()
        excel_path = exporter.export(result)
        result["excel_path"] = excel_path
    
    return result
