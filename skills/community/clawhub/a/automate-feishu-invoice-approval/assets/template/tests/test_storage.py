import tempfile
import unittest
from pathlib import Path

from invoice_approval_bot.storage import SubmissionStore


class StorageTests(unittest.TestCase):
    def test_event_and_message_are_idempotent_and_duplicate_invoice_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            store = SubmissionStore(Path(directory) / "records.sqlite3")
            event = {
                "event_id": "evt-1",
                "message_id": "om_1",
                "chat_id": "oc_1",
                "sender_id": "ou_1",
            }
            self.assertTrue(store.begin(event))
            self.assertFalse(store.begin(event))
            store.update(
                "om_1",
                status="submitted",
                invoice_fingerprint="fingerprint",
                instance_code="INSTANCE-1",
                invoice_json={"invoice_number": "1"},
            )
            self.assertEqual(
                store.duplicate_instance("fingerprint", "om_2"), "INSTANCE-1"
            )
            self.assertIsNone(store.duplicate_instance("other", "om_2"))
            self.assertEqual(store.get("om_1")["status"], "submitted")
            store.close()

    def test_card_decision_can_only_be_claimed_once_by_original_sender(self):
        with tempfile.TemporaryDirectory() as directory:
            store = SubmissionStore(Path(directory) / "records.sqlite3")
            event = {
                "event_id": "evt-card",
                "message_id": "om_source",
                "chat_id": "oc_1",
                "sender_id": "ou_owner",
            }
            self.assertTrue(store.begin(event))
            store.update(
                "om_source",
                status="pending_confirmation",
                card_message_id="om_card",
            )
            self.assertFalse(
                store.claim_decision(
                    "om_source",
                    card_message_id="om_card",
                    event_id="evt-unauthorized",
                    operator_id="ou_other",
                    action="submit",
                )
            )
            self.assertTrue(
                store.claim_decision(
                    "om_source",
                    card_message_id="om_card",
                    event_id="evt-submit",
                    operator_id="ou_owner",
                    action="submit",
                )
            )
            self.assertFalse(
                store.claim_decision(
                    "om_source",
                    card_message_id="om_card",
                    event_id="evt-submit-again",
                    operator_id="ou_owner",
                    action="submit",
                )
            )
            record = store.get("om_source")
            self.assertEqual(record["decision_event_id"], "evt-submit")
            self.assertEqual(record["decision_action"], "submit")
            store.close()


if __name__ == "__main__":
    unittest.main()
