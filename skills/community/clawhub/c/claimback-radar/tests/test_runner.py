import json
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from src.runner import ClaimbackRadar


class TestClaimbackRadar(unittest.TestCase):
    def setUp(self):
        self.radar = ClaimbackRadar(api_key="fake-key-for-testing")

    def test_load_prompt_exists(self):
        """System prompt file must load correctly."""
        self.assertIn("FUNCTION 1: EXTRACT", self.radar.system_prompt)
        self.assertIn("FUNCTION 2: DETECT & RECOMMEND", self.radar.system_prompt)

    @patch("src.runner.OpenAI")
    def test_run_returns_valid_structure(self, mock_openai_class):
        """Runner must return confirmation_card and action_receipts."""
        fake_response = {
            "confirmation_card": {
                "service_name": "Test",
                "provider": "TestCo",
                "amount": "10.00",
                "currency": "USD",
                "billing_cycle": "monthly"
            },
            "action_receipts": [
                {
                    "action_id": "act-test",
                    "action_type": "ignore",
                    "title": "Test action",
                    "priority": "low",
                    "reason": "Testing"
                }
            ],
            "risk_flags": [],
            "summary": "Test summary"
        }

        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = json.dumps(fake_response)
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai_class.return_value = mock_client

        radar = ClaimbackRadar(api_key="fake-key")
        result = radar.run({
            "source": "email_text",
            "content": "Test content",
            "current_date": "2026-04-22"
        })

        self.assertIn("confirmation_card", result)
        self.assertIn("action_receipts", result)
        self.assertEqual(result["confirmation_card"]["service_name"], "Test")

    @patch("src.runner.OpenAI")
    def test_run_raises_on_invalid_json(self, mock_openai_class):
        """Runner must raise ValueError when model returns invalid JSON."""
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "not valid json"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai_class.return_value = mock_client

        radar = ClaimbackRadar(api_key="fake-key")
        with self.assertRaises(ValueError):
            radar.run({
                "source": "email_text",
                "content": "Test",
                "current_date": "2026-04-22"
            })

    @patch("src.runner.OpenAI")
    def test_run_raises_on_missing_keys(self, mock_openai_class):
        """Runner must raise ValueError when output missing required keys."""
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = json.dumps({"wrong_key": "value"})
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai_class.return_value = mock_client

        radar = ClaimbackRadar(api_key="fake-key")
        with self.assertRaises(ValueError):
            radar.run({
                "source": "email_text",
                "content": "Test",
                "current_date": "2026-04-22"
            })


if __name__ == "__main__":
    unittest.main()