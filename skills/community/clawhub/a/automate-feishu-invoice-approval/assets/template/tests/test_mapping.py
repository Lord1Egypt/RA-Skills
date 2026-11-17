import unittest

from invoice_approval_bot.errors import MappingError
from invoice_approval_bot.mapping import (
    invoice_context,
    mapping_needs_upload,
    missing_required_fields,
    render_form,
)


class MappingTests(unittest.TestCase):
    def test_render_preserves_typed_full_token(self):
        mapping = {
            "form": [
                {"id": "date", "type": "date", "value": "{{invoice.issue_date_ms}}"},
                {
                    "id": "image",
                    "type": "image",
                    "value": ["{{approval_file.image_code}}"],
                },
                {
                    "id": "note",
                    "type": "input",
                    "value": "票号 {{invoice.invoice_number}}",
                },
            ]
        }
        context = {
            "invoice": {
                "issue_date_ms": "1785340800000",
                "invoice_number": "00123456",
            },
            "approval_file": {"image_code": "FILE-CODE"},
        }
        rendered = render_form(mapping, context)
        self.assertEqual(rendered[0]["value"], "1785340800000")
        self.assertEqual(rendered[1]["value"], ["FILE-CODE"])
        self.assertEqual(rendered[2]["value"], "票号 00123456")

    def test_omit_missing_optional_field(self):
        mapping = {
            "form": [
                {
                    "id": "remark",
                    "type": "input",
                    "value": "{{invoice.remarks}}",
                    "omit_if_missing": "invoice.remarks",
                }
            ]
        }
        self.assertEqual(render_form(mapping, {"invoice": {"remarks": None}}), [])

    def test_invoice_context_adds_date_and_cents(self):
        context = invoice_context(
            {
                "issue_date": "2026-07-30",
                "total_amount": "12.345",
                "expense_category": "交通",
                "approval_summary": "市内交通费用",
                "items": [{"name": "服务"}, {"name": None}],
            },
            {"交通": "OPTION-TRAFFIC"},
        )
        self.assertTrue(context["issue_date_ms"].isdigit())
        self.assertEqual(
            context["issue_date_rfc3339"], "2026-07-30T00:00:00+08:00"
        )
        self.assertEqual(context["total_amount_cents"], "1235")
        self.assertEqual(context["total_amount_number"], 12.345)
        self.assertEqual(context["item_summary"], "服务")
        self.assertEqual(context["expense_item_content"], "服务")
        self.assertEqual(context["expense_category_value"], "OPTION-TRAFFIC")

    def test_invoice_context_rejects_unmapped_expense_category(self):
        with self.assertRaisesRegex(MappingError, "没有对应的飞书选项 ID"):
            invoice_context(
                {
                    "expense_category": "不存在的类型",
                    "approval_summary": "测试费用",
                },
                {"其他": "OPTION-OTHER"},
            )

    def test_required_and_upload_detection(self):
        invoice = {"invoice_number": "1", "seller_name": None}
        self.assertEqual(
            missing_required_fields(invoice, ["invoice_number", "seller_name"]),
            ["seller_name"],
        )
        mapping = {"form": [{"value": ["{{approval_file.image_code}}"]}]}
        self.assertTrue(mapping_needs_upload(mapping, "image"))
        self.assertFalse(mapping_needs_upload(mapping, "attachment"))


if __name__ == "__main__":
    unittest.main()
