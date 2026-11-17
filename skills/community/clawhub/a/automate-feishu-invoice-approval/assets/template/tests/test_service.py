import json
import tempfile
import unittest
from pathlib import Path

from invoice_approval_bot.config import Settings
from invoice_approval_bot.service import (
    InvoiceApprovalService,
    buyer_header_mismatches,
    invoice_fingerprint,
)
from invoice_approval_bot.risk import invoice_risk_reasons

REQUIRED_BUYER_NAME = "测试科技有限公司"
REQUIRED_BUYER_TAX_ID = "91330000TEST123456"


class FakeLark:
    def __init__(self, image_path):
        self.image_path = image_path
        self.upload_calls = 0
        self.create_calls = 0
        self.replies = []
        self.cards = []
        self.card_updates = []

    def resolve_image_key(self, event):
        return "img_test"

    def download_image(self, message_id, image_key, output_dir):
        return self.image_path

    def upload_approval_file(self, image_path, upload_type):
        self.upload_calls += 1
        return "REAL-FILE-CODE"

    def create_approval(self, payload):
        self.create_calls += 1
        return {"code": 0, "data": {"instance_code": "INSTANCE"}}

    def reply(self, message_id, text, idempotency_key):
        self.replies.append(text)

    def send_card(self, user_id, card, idempotency_key):
        self.cards.append((user_id, card, idempotency_key))
        return "om_confirmation_card"

    def update_card(self, token, card):
        self.card_updates.append((token, card))


class FakeVision:
    def __init__(self, **overrides):
        self.overrides = overrides

    def extract(self, image_path, message_id):
        invoice = {
            "document_type": "invoice",
            "invoice_code": "CODE",
            "invoice_number": "0001",
            "issue_date": "2026-07-30",
            "buyer_name": REQUIRED_BUYER_NAME,
            "buyer_tax_id": REQUIRED_BUYER_TAX_ID,
            "seller_name": "示例科技有限公司",
            "seller_tax_id": "TAX-1",
            "amount_excluding_tax": "94.34",
            "tax_amount": "5.66",
            "total_amount": "100.00",
            "expense_category": "其他",
            "approval_summary": "测试发票费用",
            "currency": "CNY",
            "items": [
                {
                    "name": "技术服务费",
                    "amount": "94.34",
                    "tax_rate": "6%",
                    "tax_amount": "5.66",
                }
            ],
            "overall_confidence": 0.99,
            "needs_review": False,
            "review_reasons": [],
        }
        invoice.update(self.overrides)
        return invoice


class ServiceTests(unittest.TestCase):
    def _create_service(self, root, *, dry_run, vision):
        (root / "config").mkdir()
        mapping_path = root / "config" / "approval_mapping.json"
        mapping_path.write_text(
            json.dumps(
                {
                    "approval_code": "APPROVAL",
                    "required_invoice_fields": [
                        "invoice_number",
                        "issue_date",
                        "seller_name",
                        "seller_tax_id",
                        "total_amount",
                    ],
                    "form": [
                        {
                            "id": "image",
                            "type": "image",
                            "value": ["{{approval_file.image_code}}"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        schema_path = root / "config" / "invoice-output.schema.json"
        schema_path.write_text("{}", encoding="utf-8")
        image_path = root / "invoice.png"
        image_path.write_bytes(b"fake image bytes")
        data_dir = root / "data"
        settings = Settings(
            project_dir=root,
            data_dir=data_dir,
            database_path=data_dir / "records.sqlite3",
            mapping_path=mapping_path,
            invoice_schema_path=schema_path,
            approval_code=None,
            auto_submit=True,
            dry_run=dry_run,
            reply_enabled=True,
            min_confidence=0.9,
            allowed_senders=frozenset(),
            required_buyer_name=REQUIRED_BUYER_NAME,
            required_buyer_tax_id=REQUIRED_BUYER_TAX_ID,
            codex_bin="codex",
            codex_model=None,
            codex_timeout_seconds=10,
            lark_cli_bin="lark-cli",
            lark_ready_timeout_seconds=10,
        )
        lark = FakeLark(image_path)
        service = InvoiceApprovalService(settings, lark=lark, vision=vision)
        return service, lark

    def _card_action(self, *, action, event_id):
        return {
            "type": "card.action.trigger",
            "event_id": event_id,
            "message_id": "om_confirmation_card",
            "operator_id": "ou_1",
            "token": "card-update-token",
            "action_value": json.dumps(
                {
                    "action": action,
                    "source_message_id": "om_1",
                }
            ),
        }

    def test_fingerprint_is_stable_and_uses_invoice_identity(self):
        invoice = {
            "seller_tax_id": "tax-1",
            "invoice_code": "code",
            "invoice_number": "0001",
            "issue_date": "2026-07-30",
            "total_amount": "100.00",
        }
        self.assertEqual(invoice_fingerprint(invoice), invoice_fingerprint(dict(invoice)))
        changed = dict(invoice, invoice_number="0002")
        self.assertNotEqual(invoice_fingerprint(invoice), invoice_fingerprint(changed))

    def test_buyer_header_mismatches_identifies_each_invalid_field(self):
        valid_invoice = {
            "buyer_name": REQUIRED_BUYER_NAME,
            "buyer_tax_id": REQUIRED_BUYER_TAX_ID,
        }
        self.assertEqual(
            buyer_header_mismatches(
                valid_invoice, REQUIRED_BUYER_NAME, REQUIRED_BUYER_TAX_ID
            ),
            [],
        )
        self.assertEqual(
            buyer_header_mismatches(
                {
                    "buyer_name": " 测试科技 有限公司 ",
                    "buyer_tax_id": "91330000 TEST123456",
                },
                REQUIRED_BUYER_NAME,
                REQUIRED_BUYER_TAX_ID,
            ),
            [],
        )
        self.assertEqual(
            buyer_header_mismatches(
                {
                    "buyer_name": "示例智能\u200b(杭州)\u00a0科技有限公司",
                    "buyer_tax_id": REQUIRED_BUYER_TAX_ID.lower(),
                },
                "示例智能(杭州)科技有限公司",
                REQUIRED_BUYER_TAX_ID,
            ),
            [],
        )

        wrong_name = dict(valid_invoice, buyer_name="其他公司")
        wrong_name_reasons = buyer_header_mismatches(
            wrong_name, REQUIRED_BUYER_NAME, REQUIRED_BUYER_TAX_ID
        )
        self.assertEqual(len(wrong_name_reasons), 1)
        self.assertIn("购方名称不符合要求", wrong_name_reasons[0])

        wrong_tax_id = dict(valid_invoice, buyer_tax_id="WRONG-TAX-ID")
        wrong_tax_reasons = buyer_header_mismatches(
            wrong_tax_id, REQUIRED_BUYER_NAME, REQUIRED_BUYER_TAX_ID
        )
        self.assertEqual(len(wrong_tax_reasons), 1)
        self.assertIn("购方税号不符合要求", wrong_tax_reasons[0])

        self.assertEqual(
            len(
                buyer_header_mismatches(
                    {"buyer_name": "其他公司", "buyer_tax_id": "WRONG-TAX-ID"},
                    REQUIRED_BUYER_NAME,
                    REQUIRED_BUYER_TAX_ID,
                )
            ),
            2,
        )

    def test_invalid_buyer_header_is_rejected_and_replied(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            service, lark = self._create_service(
                root,
                dry_run=False,
                vision=FakeVision(
                    buyer_name="其他公司",
                    buyer_tax_id="WRONG-TAX-ID",
                ),
            )
            service.process_event(
                {
                    "event_id": "evt-invalid-header",
                    "message_id": "om_invalid_header",
                    "message_type": "image",
                    "chat_id": "oc_1",
                    "sender_id": "ou_1",
                    "content": "[Image: img_test]",
                }
            )

            record = service.store.get("om_invalid_header")
            self.assertEqual(record["status"], "buyer_header_mismatch")
            self.assertIn("购方名称不符合要求", record["error"])
            self.assertIn("购方税号不符合要求", record["error"])
            self.assertEqual(lark.upload_calls, 0)
            self.assertEqual(lark.create_calls, 0)
            self.assertEqual(len(lark.replies), 1)
            self.assertIn("购方名称不符合要求", lark.replies[0])
            self.assertIn("购方税号不符合要求", lark.replies[0])

    def test_invoice_risk_detects_individual_equipment_and_tax_mismatch(self):
        invoice = FakeVision(
            seller_name="张三",
            expense_category="设备",
            items=[
                {
                    "name": "办公电脑",
                    "amount": "1000.00",
                    "tax_rate": "13%",
                    "tax_amount": "***",
                }
            ],
            amount_excluding_tax="1000.00",
            tax_amount="0.00",
            total_amount="1000.00",
        ).extract(None, "test")
        reasons = invoice_risk_reasons(invoice)
        self.assertTrue(any("疑似个人" in reason for reason in reasons))
        self.assertTrue(any("整票税额为0" in reason for reason in reasons))
        self.assertTrue(any("税额显示为“***”" in reason for reason in reasons))

    def test_risky_invoice_is_rejected_before_confirmation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            service, lark = self._create_service(
                root,
                dry_run=True,
                vision=FakeVision(
                    seller_name="张三",
                    expense_category="设备",
                    items=[
                        {
                            "name": "办公电脑",
                            "amount": "1000.00",
                            "tax_rate": "13%",
                            "tax_amount": "***",
                        }
                    ],
                    tax_amount="0.00",
                ),
            )
            service.process_event(
                {
                    "event_id": "evt-risk",
                    "message_id": "om_risk",
                    "message_type": "image",
                    "chat_id": "oc_1",
                    "sender_id": "ou_1",
                    "content": "[Image: img_test]",
                }
            )
            record = service.store.get("om_risk")
            self.assertEqual(record["status"], "invoice_risk_rejected")
            self.assertIn("发票存在风险，未提交审批", lark.replies[0])
            self.assertEqual(len(lark.cards), 0)
            self.assertEqual(lark.upload_calls, 0)
            self.assertEqual(lark.create_calls, 0)

    def test_dry_run_does_not_upload_or_create_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            service, lark = self._create_service(
                root,
                dry_run=True,
                vision=FakeVision(),
            )
            service.process_event(
                {
                    "event_id": "evt-1",
                    "message_id": "om_1",
                    "message_type": "image",
                    "chat_id": "oc_1",
                    "sender_id": "ou_1",
                    "content": "[Image: img_test]",
                }
            )
            record = service.store.get("om_1")
            self.assertEqual(record["status"], "pending_confirmation")
            self.assertEqual(record["card_message_id"], "om_confirmation_card")
            self.assertEqual(len(lark.cards), 1)
            self.assertEqual(lark.upload_calls, 0)
            self.assertEqual(lark.create_calls, 0)

            service.process_card_action(
                self._card_action(action="submit", event_id="card-event-submit")
            )
            record = service.store.get("om_1")
            self.assertEqual(record["status"], "confirmed_dry_run")
            self.assertIn("DRY_RUN_IMAGE_CODE", record["approval_request_json"])
            self.assertEqual(lark.upload_calls, 0)
            self.assertEqual(lark.create_calls, 0)
            self.assertEqual(len(lark.card_updates), 1)

    def test_real_approval_waits_for_submit_button(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            service, lark = self._create_service(
                root,
                dry_run=False,
                vision=FakeVision(),
            )
            service.process_event(
                {
                    "event_id": "evt-1",
                    "message_id": "om_1",
                    "message_type": "image",
                    "chat_id": "oc_1",
                    "sender_id": "ou_1",
                    "content": "[Image: img_test]",
                }
            )
            self.assertEqual(
                service.store.get("om_1")["status"], "pending_confirmation"
            )
            self.assertEqual(lark.upload_calls, 0)
            self.assertEqual(lark.create_calls, 0)

            service.process_card_action(
                self._card_action(action="submit", event_id="card-event-submit")
            )
            record = service.store.get("om_1")
            self.assertEqual(record["status"], "submitted")
            self.assertEqual(record["instance_code"], "INSTANCE")
            self.assertEqual(lark.upload_calls, 1)
            self.assertEqual(lark.create_calls, 1)
            self.assertEqual(len(lark.card_updates), 1)

    def test_decline_button_never_uploads_or_creates_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            service, lark = self._create_service(
                root,
                dry_run=False,
                vision=FakeVision(),
            )
            service.process_event(
                {
                    "event_id": "evt-1",
                    "message_id": "om_1",
                    "message_type": "image",
                    "chat_id": "oc_1",
                    "sender_id": "ou_1",
                    "content": "[Image: img_test]",
                }
            )
            service.process_card_action(
                self._card_action(action="decline", event_id="card-event-decline")
            )
            record = service.store.get("om_1")
            self.assertEqual(record["status"], "declined")
            self.assertEqual(lark.upload_calls, 0)
            self.assertEqual(lark.create_calls, 0)
            self.assertEqual(len(lark.card_updates), 1)


if __name__ == "__main__":
    unittest.main()
