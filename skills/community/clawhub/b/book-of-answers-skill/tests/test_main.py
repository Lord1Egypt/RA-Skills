import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import main
from router import route_question_to_book
from service import AnswerEntry
from storage import load_user_state


class AnswerLibraryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "book-of-answers-skill-test.sqlite3"
        os.environ["ANSWER_LIBRARY_DB"] = str(self.db_path)
        self.user_id = "test-user"
        self.base_time = datetime(2026, 4, 14, 10, 0, 0, tzinfo=timezone.utc)

    def tearDown(self) -> None:
        os.environ.pop("ANSWER_LIBRARY_DB", None)
        self.temp_dir.cleanup()

    def test_duplicate_question_within_five_minutes_returns_last_answer_with_source(self) -> None:
        with patch(
            "service.draw_answer",
            return_value=AnswerEntry(
                text="希望是件好东西，也许是世上最好的东西，好东西从不会消逝。",
                source="《肖申克的救赎》",
            ),
        ), patch("router.random.choice", return_value="《电影答案之书》"):
            main.handle_request(self.user_id, "明天会好吗", now=self.base_time)

        duplicate_response = main.handle_request(
            self.user_id,
            "明天会好吗",
            now=self.base_time + timedelta(seconds=120),
        )

        self.assertIn("你刚刚已经问过这个问题了", duplicate_response)
        self.assertIn("出处：《肖申克的救赎》", duplicate_response)

    def test_switch_book_follow_up_reuses_last_question_and_bypasses_duplicate_check(self) -> None:
        with patch("router.random.choice", return_value="《文学答案之书》"), patch(
            "service.draw_answer",
            return_value=AnswerEntry(text="凡是过去，皆为序章。", source="莎士比亚《暴风雨》"),
        ):
            main.handle_request(self.user_id, "明天会好吗", now=self.base_time)

        with patch(
            "service.draw_answer",
            return_value=AnswerEntry(
                text="跑，阿甘，快跑！",
                source="《阿甘正传》",
            ),
        ):
            response = main.handle_request(
                self.user_id,
                "那用电影版的再测一次",
                now=self.base_time + timedelta(seconds=60),
            )

        self.assertIn("《电影答案之书》", response)
        self.assertIn("出处：《阿甘正传》", response)
        state = load_user_state(self.user_id)
        self.assertEqual(state.last_question, "明天会好吗")
        self.assertEqual(state.last_book, "《电影答案之书》")

    def test_daily_fortune_uses_daily_prefix_and_source(self) -> None:
        with patch(
            "service.random.choice",
            side_effect=[
                "《音乐答案之书》",
                AnswerEntry(text="我和我最后的倔强，握紧双手绝对不放。", source="《倔强》"),
            ],
        ):
            response = main.handle_request(self.user_id, "每日一签", now=self.base_time)

        self.assertEqual(response, "【每日一签】\n「 我和我最后的倔强，握紧双手绝对不放。 」\n出处：《倔强》")

    def test_welcome_message_introduces_three_books_and_features(self) -> None:
        response = main.handle_request(self.user_id, "", now=self.base_time)
        self.assertIn("欢迎翻开答案之书", response)
        self.assertIn("《电影答案之书》", response)
        self.assertIn("《文学答案之书》", response)
        self.assertIn("《音乐答案之书》", response)
        self.assertIn("每日一签", response)

    def test_history_intent_returns_disabled_message(self) -> None:
        response = main.handle_request(self.user_id, "查看记录", now=self.base_time)
        self.assertEqual(response, "借阅记录功能已关闭，当前版本不会保存或展示历史记录。")

    def test_history_log_is_not_retained_after_answer(self) -> None:
        with patch(
            "service.draw_answer",
            return_value=AnswerEntry(text="凡是过去，皆为序章。", source="莎士比亚《暴风雨》"),
        ), patch("router.random.choice", return_value="《文学答案之书》"):
            main.handle_request(self.user_id, "明天会好吗", now=self.base_time)

        state = load_user_state(self.user_id)
        self.assertEqual(state.history_log, [])

    def test_default_route_is_random_between_three_books(self) -> None:
        with patch("router.random.choice", return_value="《音乐答案之书》"):
            decision = route_question_to_book("我只是想知道接下来会怎样")
        self.assertEqual(decision.book_name, "《音乐答案之书》")
        self.assertIn("fallback:random", decision.reasons)

    def test_router_prefers_movie_for_movie_language(self) -> None:
        decision = route_question_to_book("如果这是一部电影，现在会走向什么结局")
        self.assertEqual(decision.book_name, "《电影答案之书》")
        self.assertGreaterEqual(decision.confidence, 0.6)

    def test_router_prefers_literary_for_literary_language(self) -> None:
        decision = route_question_to_book("请用文学答案之书回答我，这一章该怎么写下去")
        self.assertEqual(decision.book_name, "《文学答案之书》")
        self.assertGreaterEqual(decision.confidence, 0.8)

    def test_router_prefers_music_for_music_language(self) -> None:
        decision = route_question_to_book("适合听什么歌，我想从歌词里找答案")
        self.assertEqual(decision.book_name, "《音乐答案之书》")
        self.assertGreaterEqual(decision.confidence, 0.6)

    def test_standard_response_contains_source_line(self) -> None:
        with patch(
            "service.draw_answer",
            return_value=AnswerEntry(text="凡是过去，皆为序章。", source="莎士比亚《暴风雨》"),
        ), patch("router.random.choice", return_value="《文学答案之书》"):
            response = main.handle_request(self.user_id, "明天会好吗", now=self.base_time)

        self.assertIn("出处：莎士比亚《暴风雨》", response)


if __name__ == "__main__":
    unittest.main()
