import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import main
from service import AnswerEntry
from storage import connect_db, load_user_state


class AnswerLibraryIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "integration.sqlite3"
        os.environ["ANSWER_LIBRARY_DB"] = str(self.db_path)
        self.user_id = "integration-user"
        self.base_time = datetime(2026, 4, 14, 9, 0, 0, tzinfo=timezone.utc)

    def tearDown(self) -> None:
        os.environ.pop("ANSWER_LIBRARY_DB", None)
        self.temp_dir.cleanup()

    def test_daily_fortune_does_not_overwrite_switchable_question_context(self) -> None:
        with patch("router.random.choice", return_value="《文学答案之书》"), patch(
            "service.draw_answer",
            return_value=AnswerEntry(text="凡是过去，皆为序章。", source="莎士比亚《暴风雨》"),
        ):
            main.handle_request(self.user_id, "明天会好吗", now=self.base_time)

        with patch(
            "service.random.choice",
            side_effect=[
                "《音乐答案之书》",
                AnswerEntry(text="有时候，有时候，我会相信一切有尽头。", source="《红豆》"),
            ],
        ):
            main.handle_request(self.user_id, "每日一签", now=self.base_time + timedelta(minutes=1))

        with patch(
            "service.draw_answer",
            return_value=AnswerEntry(text="跑，阿甘，快跑！", source="《阿甘正传》"),
        ):
            response = main.handle_request(
                self.user_id,
                "换电影之书",
                now=self.base_time + timedelta(minutes=2),
            )

        self.assertIn("《电影答案之书》", response)
        state = load_user_state(self.user_id)
        self.assertEqual(state.last_question, "明天会好吗")

    def test_legacy_card_phrase_does_not_mutate_context(self) -> None:
        with patch("router.random.choice", return_value="《音乐答案之书》"), patch(
            "service.draw_answer",
            return_value=AnswerEntry(text="我就是我，是颜色不一样的烟火。", source="《我》"),
        ):
            main.handle_request(self.user_id, "明天会好吗", now=self.base_time)

        response = main.handle_request(self.user_id, "生成卡片", now=self.base_time + timedelta(seconds=10))

        state = load_user_state(self.user_id)
        self.assertEqual(state.last_question, "明天会好吗")
        self.assertEqual(response, "抱歉，图书馆灯光太暗，我没看清。请用文字提出具体的疑问。")

    def test_dirty_sqlite_state_recovers_without_crashing(self) -> None:
        with connect_db() as conn:
            conn.execute(
                """
                INSERT INTO user_state (
                    user_id,
                    last_question,
                    last_answer,
                    last_book,
                    last_timestamp,
                    history_log
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    self.user_id,
                    12345,
                    67890,
                    "《电影答案之书》",
                    "not-a-timestamp",
                    "{bad-json",
                ),
            )
            conn.commit()

        with patch("router.random.choice", return_value="《文学答案之书》"), patch(
            "service.draw_answer",
            return_value=AnswerEntry(text="满地都是六便士，他却抬头看见了月亮。", source="毛姆《月亮与六便士》"),
        ):
            response = main.handle_request(self.user_id, "一个新的问题", now=self.base_time)

        self.assertIn("《文学答案之书》", response)
        state = load_user_state(self.user_id)
        self.assertEqual(state.last_question, "一个新的问题")
        self.assertEqual(state.history_log, [])


if __name__ == "__main__":
    unittest.main()
