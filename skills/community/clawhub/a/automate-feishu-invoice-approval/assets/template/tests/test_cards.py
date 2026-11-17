import unittest

from invoice_approval_bot.cards import (
    build_invoice_confirmation_card,
    build_invoice_decision_card,
)


class CardTests(unittest.TestCase):
    def setUp(self):
        self.invoice = {
            "expense_category": "交通",
            "total_amount": "88.50",
            "currency": "CNY",
            "invoice_number": "001",
            "issue_date": "2026-07-30",
            "seller_name": "某某出行有限公司",
            "approval_summary": "市内交通费用",
        }

    def test_confirmation_card_is_card_2_and_has_two_callbacks(self):
        card = build_invoice_confirmation_card(
            self.invoice,
            "om_source",
            dry_run=False,
        )
        self.assertEqual(card["schema"], "2.0")
        self.assertFalse(card["config"]["enable_forward"])
        buttons = []
        for element in card["body"]["elements"]:
            if element.get("tag") != "column_set":
                continue
            for column in element.get("columns", []):
                buttons.extend(
                    child
                    for child in column.get("elements", [])
                    if child.get("tag") == "button"
                )
        self.assertEqual(len(buttons), 2)
        self.assertEqual(
            {button["text"]["content"] for button in buttons},
            {"提交", "暂不提交"},
        )
        values = [button["behaviors"][0]["value"] for button in buttons]
        self.assertEqual(
            {value["action"] for value in values},
            {"submit", "decline"},
        )
        self.assertTrue(
            all(value["source_message_id"] == "om_source" for value in values)
        )

    def test_dynamic_markdown_is_escaped(self):
        invoice = dict(self.invoice, seller_name="测试*[公司](https://example.com)")
        card = build_invoice_confirmation_card(
            invoice,
            "om_source",
            dry_run=True,
        )
        serialized = str(card)
        self.assertNotIn("[公司](https://example.com)", serialized)
        self.assertIn("&#42;", serialized)

    def test_decision_card_has_no_buttons(self):
        card = build_invoice_decision_card(
            self.invoice,
            status="submitted",
            instance_code="INSTANCE",
        )
        self.assertEqual(card["schema"], "2.0")
        self.assertNotIn('"tag": "button"', str(card))


if __name__ == "__main__":
    unittest.main()
