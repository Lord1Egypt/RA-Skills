"""
Feishu Card Builder for Reconciliation Results
"""
from typing import Dict, List


def build_feishu_card(result: Dict) -> Dict:
    """
    Build Feishu interactive card for reconciliation results.
    
    Args:
        result: Reconciliation result dict
    
    Returns:
        Feishu card content dict
    """
    summary = result.get("summary", {})
    matched = result.get("matched", [])
    differences = result.get("differences", [])
    unclaimed = result.get("unclaimed", [])
    unmatched_orders = result.get("unmatched_orders", [])
    
    # Determine color based on match rate
    match_rate = summary.get("match_rate", 0)
    if match_rate >= 90:
        template = "green"
    elif match_rate >= 70:
        template = "yellow"
    else:
        template = "red"
    
    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "📊 银行流水对账结果"
                },
                "template": template
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**对账时间**: {summary.get('reconcile_time', 'N/A')}"
                    }
                },
                {"tag": "hr"},
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "### 📈 匹配概况"
                    }
                },
                {
                    "tag": "column_set",
                    "flex_mode": "BetweenBaseline",
                    "horizontal_spacing": "large",
                    "elements": [
                        {
                            "tag": "column",
                            "width": " stretched",
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": f"**匹配率**\n**{match_rate:.1f}%**"
                                    }
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "stretched",
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": f"**已匹配**\n**{summary.get('matched_count', 0)} 笔**"
                                    }
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "stretched",
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": f"**差异**\n**{summary.get('difference_count', 0)} 笔**"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {"tag": "hr"},
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "### 💰 金额汇总"
                    }
                },
                {
                    "tag": "column_set",
                    "flex_mode": "BetweenBaseline",
                    "horizontal_spacing": "large",
                    "elements": [
                        {
                            "tag": "column",
                            "width": "stretched",
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": f"已匹配金额\n**¥{summary.get('matched_amount', 0):,.2f}**"
                                    }
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "stretched",
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": f"差异金额\n**¥{summary.get('difference_amount', 0):,.2f}**"
                                    }
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "stretched",
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": f"未认领\n**¥{summary.get('unclaimed_amount', 0):,.2f}**"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {"tag": "hr"},
            ]
        }
    }
    
    # Add details if there are issues
    if unclaimed:
        card["card"]["elements"].append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"⚠️ **未认领**: {len(unclaimed)} 笔（有钱没订单）"
            }
        })
    
    if unmatched_orders:
        card["card"]["elements"].append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"⚠️ **未核销**: {len(unmatched_orders)} 笔（有订单没收钱）"
            }
        })
    
    # Add Excel download if available
    if result.get("excel_path"):
        card["card"]["elements"].append({"tag": "hr"})
        card["card"]["elements"].append({
            "tag": "note",
            "elements": [
                {
                    "tag": "plain_text",
                    "content": f"📎 详细报告已导出: {result['excel_path']}"
                }
            ]
        })
    
    # Add action buttons
    if unclaimed or unmatched_orders:
        card["card"]["elements"].append({"tag": "hr"})
        card["card"]["elements"].append({
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": "标记已处理"
                    },
                    "type": "primary"
                },
                {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": "标记待追款"
                    },
                    "type": "warning"
                },
                {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": "标记坏账"
                    },
                    "type": "danger"
                }
            ]
        })
    
    return card


def build_feishu_simple_message(result: Dict) -> str:
    """
    Build simple Feishu text message for reconciliation results.
    
    Returns:
        Markdown formatted text
    """
    summary = result.get("summary", {})
    
    match_rate = summary.get("match_rate", 0)
    
    emoji = "✅" if match_rate >= 90 else "⚠️" if match_rate >= 70 else "❌"
    
    lines = [
        f"📊 **银行流水对账结果**",
        "",
        f"📊 **匹配率**: {match_rate:.1f}%",
        f"✅ **已匹配**: {summary.get('matched_count', 0)} 笔",
        f"⚠️ **差异**: {summary.get('difference_count', 0)} 笔",
        f"💰 **差异金额**: ¥{summary.get('difference_amount', 0):,.2f}",
        f"❗ **未认领**: {summary.get('unclaimed_count', 0)} 笔",
        f"❗ **未核销**: {summary.get('unmatched_count', 0)} 笔",
        "",
    ]
    
    if result.get("excel_path"):
        lines.append(f"📎 详细报告: {result['excel_path']}")
    
    return "\n".join(lines)
