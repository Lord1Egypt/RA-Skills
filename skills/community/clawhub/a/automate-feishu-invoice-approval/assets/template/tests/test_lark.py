import unittest

from invoice_approval_bot.lark import _find_image_key, _find_string, _redact


class LarkTests(unittest.TestCase):
    def test_find_image_key_in_nested_or_rendered_content(self):
        self.assertEqual(_find_image_key("[Image: img_v3_abc-123]"), "img_v3_abc-123")
        self.assertEqual(
            _find_image_key({"content": '{"image_key":"img_v3_nested"}'}),
            "img_v3_nested",
        )

    def test_redacts_tokens(self):
        self.assertNotIn(
            "t-abcdefghijklmnop",
            _redact("Authorization: Bearer abcdef t-abcdefghijklmnop"),
        )
        self.assertNotIn("Bearer abcdef", _redact("Bearer abcdef"))

    def test_find_string_in_cli_response_envelope(self):
        self.assertEqual(
            _find_string(
                {"ok": True, "data": {"message": {"message_id": "om_card"}}},
                "message_id",
            ),
            "om_card",
        )


if __name__ == "__main__":
    unittest.main()
