"""飞书发票确认卡片的 Card 2.0 构造函数。"""

from __future__ import annotations

import html
from typing import Any, Dict, Mapping, Optional


MARKDOWN_SPECIALS = {
    ord("*"): "&#42;",
    ord("~"): "&#126;",
    ord(">"): "&#62;",
    ord("["): "&#91;",
    ord("]"): "&#93;",
    ord("("): "&#40;",
    ord(")"): "&#41;",
    ord("#"): "&#35;",
    ord(":"): "&#58;",
    ord("_"): "&#95;",
}


def _md(value: Any) -> str:
    """转义动态票面文字，避免被卡片 Markdown 当作样式或链接解析。"""

    return html.escape(str(value or "—"), quote=False).translate(MARKDOWN_SPECIALS)


def _base_config(summary: str) -> Dict[str, Any]:
    return {
        "update_multi": True,
        "width_mode": "default",
        "enable_forward": False,
        "summary": {"content": summary},
        "style": {
            "text_size": {
                "caption": {
                    "default": "notation",
                    "pc": "notation",
                    "mobile": "notation",
                }
            },
            "color": {
                "cus-primary-bg": {
                    "light_mode": "rgba(30,120,255,0.08)",
                    "dark_mode": "rgba(80,150,255,0.12)",
                },
                "cus-muted": {
                    "light_mode": "rgba(100,106,115,1)",
                    "dark_mode": "rgba(150,155,163,1)",
                },
            },
        },
    }


def build_invoice_confirmation_card(
    invoice: Mapping[str, Any],
    source_message_id: str,
    *,
    dry_run: bool,
) -> Dict[str, Any]:
    """生成包含审批预览与确认按钮的 Card 2.0 卡片。"""

    category = _md(invoice.get("expense_category"))
    amount = _md(invoice.get("total_amount"))
    currency = _md(invoice.get("currency") or "CNY")
    status_label = "演练待确认" if dry_run else "待确认"

    elements = [
        {
            "tag": "column_set",
            "flex_mode": "none",
            "horizontal_spacing": "12px",
            "margin": "0px 0px 12px 0px",
            "columns": [
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "background_style": "cus-primary-bg",
                    "padding": "12px",
                    "vertical_spacing": "2px",
                    "elements": [
                        {
                            "tag": "markdown",
                            "content": f"**<font color='blue'>{category}</font>**",
                            "text_align": "center",
                        },
                        {
                            "tag": "markdown",
                            "content": "<font color='grey'>报销类型</font>",
                            "text_align": "center",
                            "text_size": "caption",
                        },
                    ],
                },
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "background_style": "cus-primary-bg",
                    "padding": "12px",
                    "vertical_spacing": "2px",
                    "elements": [
                        {
                            "tag": "markdown",
                            "content": (
                                f"## <font color='blue'>{amount}</font>"
                            ),
                            "text_align": "center",
                        },
                        {
                            "tag": "markdown",
                            "content": f"<font color='grey'>价税合计（{currency}）</font>",
                            "text_align": "center",
                            "text_size": "caption",
                        },
                    ],
                },
            ],
        },
        {
            "tag": "div",
            "margin": "0px 0px 12px 0px",
            "fields": [
                {
                    "is_short": True,
                    "text": {
                        "tag": "lark_md",
                        "content": f"**发票号码**\n{_md(invoice.get('invoice_number'))}",
                    },
                },
                {
                    "is_short": True,
                    "text": {
                        "tag": "lark_md",
                        "content": f"**开票日期**\n{_md(invoice.get('issue_date'))}",
                    },
                },
                {
                    "is_short": False,
                    "text": {
                        "tag": "lark_md",
                        "content": f"**销售方**\n{_md(invoice.get('seller_name'))}",
                    },
                },
                {
                    "is_short": False,
                    "text": {
                        "tag": "lark_md",
                        "content": "**附件**\n原发票图片将在确认后随审批提交",
                    },
                },
            ],
        },
        {
            "tag": "div",
            "margin": "0px 0px 12px 0px",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**报销事由**\n{_md(invoice.get('approval_summary'))}"
                ),
                "lines": 3,
            },
        },
    ]

    if dry_run:
        elements.append(
            {
                "tag": "markdown",
                "content": (
                    "<text_tag color='yellow'>演练模式</text_tag> "
                    "点击确认只会生成审批请求，不会上传附件或创建真实审批。"
                ),
                "margin": "0px 0px 12px 0px",
            }
        )

    elements.append(
        {
            "tag": "column_set",
            "flex_mode": "none",
            "horizontal_spacing": "12px",
            "columns": [
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "elements": [
                        {
                            "tag": "button",
                            "element_id": "submitButton",
                            "text": {
                                "tag": "plain_text",
                                "content": "提交",
                            },
                            "type": "primary_filled",
                            "width": "fill",
                            "behaviors": [
                                {
                                    "type": "callback",
                                    "value": {
                                        "action": "submit",
                                        "source_message_id": source_message_id,
                                    },
                                }
                            ],
                        }
                    ],
                },
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "elements": [
                        {
                            "tag": "button",
                            "element_id": "declineButton",
                            "text": {
                                "tag": "plain_text",
                                "content": "暂不提交",
                            },
                            "type": "default",
                            "width": "fill",
                            "behaviors": [
                                {
                                    "type": "callback",
                                    "value": {
                                        "action": "decline",
                                        "source_message_id": source_message_id,
                                    },
                                }
                            ],
                        }
                    ],
                },
            ],
        }
    )

    return {
        "schema": "2.0",
        "config": _base_config("发票报销待确认"),
        "header": {
            "title": {"tag": "plain_text", "content": "发票报销确认"},
            "subtitle": {
                "tag": "plain_text",
                "content": "请核对识别结果后选择是否提交",
            },
            "template": "blue",
            "icon": {"tag": "standard_icon", "token": "approval_colorful"},
            "text_tag_list": [
                {
                    "tag": "text_tag",
                    "text": {"tag": "plain_text", "content": status_label},
                    "color": "yellow",
                }
            ],
        },
        "body": {
            "direction": "vertical",
            "padding": "12px 12px 20px 12px",
            "vertical_spacing": "0px",
            "elements": elements,
        },
    }


def build_invoice_decision_card(
    invoice: Mapping[str, Any],
    *,
    status: str,
    instance_code: Optional[str] = None,
) -> Dict[str, Any]:
    """生成按钮处理后的最终状态卡片。"""

    states = {
        "submitted": (
            "费用报销已提交",
            "审批创建成功",
            "green",
            "green",
            "green-50",
        ),
        "confirmed_dry_run": (
            "演练确认完成",
            "未创建真实审批",
            "yellow",
            "yellow",
            "yellow-50",
        ),
        "ready_for_review": (
            "表单已确认",
            "系统未启用审批提交",
            "yellow",
            "yellow",
            "yellow-50",
        ),
        "declined": (
            "已暂不提交",
            "本次发票不会进入审批",
            "grey",
            "neutral",
            "grey-50",
        ),
        "duplicate": (
            "检测到重复发票",
            "该发票已有审批记录",
            "orange",
            "orange",
            "orange-50",
        ),
        "failed": (
            "审批提交失败",
            "请重新发送发票后再试",
            "red",
            "red",
            "red-50",
        ),
    }
    title, conclusion, template, tag_color, background = states.get(
        status, states["failed"]
    )
    result_line = (
        f"\n**审批实例**\n{_md(instance_code)}" if instance_code else ""
    )

    return {
        "schema": "2.0",
        "config": _base_config(title),
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": template,
            "icon": {"tag": "standard_icon", "token": "approval_colorful"},
            "text_tag_list": [
                {
                    "tag": "text_tag",
                    "text": {"tag": "plain_text", "content": conclusion},
                    "color": tag_color,
                }
            ],
        },
        "body": {
            "direction": "vertical",
            "padding": "12px 12px 20px 12px",
            "vertical_spacing": "12px",
            "elements": [
                {
                    "tag": "column_set",
                    "flex_mode": "none",
                    "background_style": background,
                    "columns": [
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "padding": "12px",
                            "elements": [
                                {
                                    "tag": "markdown",
                                    "content": f"**{_md(conclusion)}**",
                                    "text_align": "center",
                                }
                            ],
                        }
                    ],
                },
                {
                    "tag": "div",
                    "fields": [
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": (
                                    "**报销类型**\n"
                                    f"{_md(invoice.get('expense_category'))}"
                                ),
                            },
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": (
                                    "**价税合计**\n"
                                    f"{_md(invoice.get('total_amount'))} "
                                    f"{_md(invoice.get('currency') or 'CNY')}"
                                ),
                            },
                        },
                        {
                            "is_short": False,
                            "text": {
                                "tag": "lark_md",
                                "content": (
                                    "**报销事由**\n"
                                    f"{_md(invoice.get('approval_summary'))}"
                                    f"{result_line}"
                                ),
                            },
                        },
                    ],
                },
            ],
        },
    }
