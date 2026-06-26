from __future__ import annotations

from .models import RefundRules


class AfterSalesRuleEngine:
    """Turn refund rules and user questions into a service reply."""

    def generate_response(self, user_input: str, rules: RefundRules) -> str:
        normalized = user_input.strip()
        if not normalized:
            return "请告诉我您遇到的售后问题，我会根据当前售后规则为您处理。"

        lowered = normalized.lower()

        if any(token in normalized for token in ("拆", "打开", "开封")):
            if rules.unboxing_allowed:
                return (
                    "可以为您处理。根据当前售后规则，商品拆封后仍支持退货，"
                    f"具体以“{rules.refund_policy}”执行，{self._shipping_sentence(rules)}"
                )
            return (
                "当前规则下，商品拆封后暂不支持直接退货。"
                f"现行政策为“{rules.refund_policy}”，如商品存在质量问题，我可以继续帮您登记售后。"
            )

        if any(token in normalized for token in ("运费", "邮费", "快递费")):
            return (
                f"关于退换货运费，当前规则为由{rules.shipping_fee_by}承担。"
                f"另外，本店售后政策为“{rules.refund_policy}”。"
            )

        if any(token in normalized for token in ("退货", "退款", "换货", "售后")) or "return" in lowered:
            return (
                f"可以为您说明售后规则：{rules.summary()}"
                "如果您愿意，我可以继续根据商品状态帮您判断是否满足退换条件。"
            )

        return (
            "我已进入电商售后客服模式。"
            f"当前规则为：{rules.summary()}"
            "请继续描述订单状态、是否拆封、是否有质量问题，我会给您更准确的处理建议。"
        )

    @staticmethod
    def _shipping_sentence(rules: RefundRules) -> str:
        return f"退换货运费由{rules.shipping_fee_by}承担。"
