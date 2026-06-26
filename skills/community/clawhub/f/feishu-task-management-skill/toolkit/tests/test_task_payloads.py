import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feishu_task_toolkit.tasks import (
    add_default_member_to_created_task,
    build_member_operation_payload,
    build_update_payload,
    parse_due_input,
    parse_member_args,
)


class TaskPayloadTests(unittest.TestCase):
    def test_build_member_operation_payload_uses_user_type_and_role(self) -> None:
        payload = build_member_operation_payload(["ou_default"])

        self.assertEqual(
            payload,
            {
                "members": [
                    {
                        "id": "ou_default",
                        "type": "user",
                        "role": "assignee",
                    }
                ]
            },
        )

    def test_add_default_member_to_created_task_success(self) -> None:
        class FakeService:
            def __init__(self) -> None:
                self.calls = []

            def add_members(self, task_guid, open_ids, raw_body=None):
                self.calls.append((task_guid, open_ids, raw_body))
                return {"ok": True}

        service = FakeService()
        created = {"task": {"guid": "task-guid"}}

        result = add_default_member_to_created_task(service, created, "ou_default")

        self.assertEqual(service.calls, [("task-guid", ["ou_default"], None)])
        self.assertEqual(result["default_member"]["open_id"], "ou_default")
        self.assertEqual(result["default_member"]["status"], "added")

    def test_add_default_member_to_created_task_reports_warning_on_failure(self) -> None:
        class FakeService:
            def add_members(self, task_guid, open_ids, raw_body=None):
                raise RuntimeError("boom")

        created = {"task": {"guid": "task-guid"}}

        result = add_default_member_to_created_task(FakeService(), created, "ou_default")

        self.assertEqual(result["default_member"]["status"], "failed")
        self.assertEqual(result["warnings"][0]["code"], "default_member_add_failed")

    def test_parse_due_date_as_all_day(self) -> None:
        due = parse_due_input(date_value="2026-03-10", datetime_value=None, clear=False)

        self.assertEqual(due["is_all_day"], True)
        self.assertEqual(due["timestamp"], "1773100800000")

    def test_parse_due_datetime_as_precise_timestamp(self) -> None:
        due = parse_due_input(date_value=None, datetime_value="2026-03-10 18:30", clear=False)

        self.assertEqual(due["is_all_day"], False)
        self.assertEqual(due["timestamp"], "1773138600000")

    def test_parse_due_clear_returns_null(self) -> None:
        due = parse_due_input(date_value=None, datetime_value=None, clear=True)

        self.assertIsNone(due)

    def test_build_update_payload_tracks_update_fields(self) -> None:
        payload = build_update_payload(
            summary="新的标题",
            description=None,
            start=None,
            due={"timestamp": "1773100800000", "is_all_day": True},
        )

        self.assertEqual(payload["task"]["summary"], "新的标题")
        self.assertEqual(payload["task"]["due"]["timestamp"], "1773100800000")
        self.assertEqual(set(payload["update_fields"]), {"summary", "due"})

    def test_parse_member_args_preserves_input_order(self) -> None:
        self.assertEqual(parse_member_args(["张三", "李四"]), ["张三", "李四"])


if __name__ == "__main__":
    unittest.main()
