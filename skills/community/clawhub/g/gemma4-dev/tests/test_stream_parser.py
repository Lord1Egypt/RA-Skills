"""
Comprehensive unit tests for GemmaThoughtStreamParser.
Tests multi-block reasoning isolation, split tag boundaries, and zero-leakage guarantees.
"""

import unittest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from stream_parser import GemmaThoughtStreamParser


class TestGemmaThoughtStreamParser(unittest.TestCase):

    def test_standard_single_stream(self):
        parser = GemmaThoughtStreamParser()
        chunks = [
            "<thought>\nThinking through the problem step by step.\n</thought>\n",
            "Here is the final answer."
        ]
        for c in chunks:
            list(parser.feed(c))
        list(parser.finalize())

        thought, response = parser.get_summary()
        self.assertEqual(thought, "Thinking through the problem step by step.")
        self.assertEqual(response, "Here is the final answer.")

    def test_multiple_thought_blocks(self):
        """Verify that multiple thought blocks across a stream are completely isolated."""
        parser = GemmaThoughtStreamParser()
        chunks = [
            "<thought>Step 1: Planning</thought>First response section. ",
            "<thought>Step 2: Verification</thought>Second response section."
        ]
        for c in chunks:
            list(parser.feed(c))
        list(parser.finalize())

        thought, response = parser.get_summary()
        self.assertIn("Step 1: Planning", thought)
        self.assertIn("Step 2: Verification", thought)
        self.assertNotIn("Step 1: Planning", response)
        self.assertNotIn("Step 2: Verification", response)
        self.assertNotIn("<thought>", response)
        self.assertNotIn("</thought>", response)
        self.assertEqual(response, "First response section. Second response section.")

    def test_split_across_secondary_thought_tags(self):
        """Verify split tags across chunks for subsequent thought blocks."""
        parser = GemmaThoughtStreamParser()
        chunks = [
            "Response start. ",
            "<th", "ought>", "Intermediate thought", "</th", "ought>",
            " Response middle. ",
            "<th", "ought>", "Second thought", "</th", "ought>",
            " Response end."
        ]
        for c in chunks:
            list(parser.feed(c))
        list(parser.finalize())

        thought, response = parser.get_summary()
        self.assertIn("Intermediate thought", thought)
        self.assertIn("Second thought", thought)
        self.assertEqual(response, "Response start.  Response middle.  Response end.")
        self.assertNotIn("<thought>", response)
        self.assertNotIn("Intermediate thought", response)

    def test_no_thought_tags(self):
        parser = GemmaThoughtStreamParser()
        chunks = ["Direct ", "response ", "without ", "any ", "thinking."]
        for c in chunks:
            list(parser.feed(c))
        list(parser.finalize())

        thought, response = parser.get_summary()
        self.assertEqual(thought, "")
        self.assertEqual(response, "Direct response without any thinking.")

    def test_unclosed_subsequent_thought_fail_closed(self):
        """Ensure an unclosed thought block at stream end does NOT leak into response."""
        parser = GemmaThoughtStreamParser()
        chunks = [
            "<thought>Initial thought</thought>Public text. ",
            "<thought>Sensitive internal reasoning that gets truncated"
        ]
        for c in chunks:
            list(parser.feed(c))
        list(parser.finalize())

        thought, response = parser.get_summary()
        self.assertIn("Sensitive internal reasoning that gets truncated", thought)
        self.assertNotIn("Sensitive internal reasoning that gets truncated", response)
        self.assertEqual(response, "Public text.")

    def test_empty_thought_blocks(self):
        parser = GemmaThoughtStreamParser()
        chunks = ["<thought></thought>Response only."]
        for c in chunks:
            list(parser.feed(c))
        list(parser.finalize())

        thought, response = parser.get_summary()
        self.assertEqual(thought, "")
        self.assertEqual(response, "Response only.")

    def test_single_character_streaming_multiple_blocks(self):
        parser = GemmaThoughtStreamParser()
        full_text = "<thought>T1</thought>R1<thought>T2</thought>R2"
        for char in full_text:
            list(parser.feed(char))
        list(parser.finalize())

        thought, response = parser.get_summary()
        self.assertEqual(thought, "T1T2")
        self.assertEqual(response, "R1R2")

    def test_zero_leakage_invariant(self):
        """Fuzz-like invariant check: enclosed thought text must never appear in response."""
        parser = GemmaThoughtStreamParser()
        test_payload = (
            "Prefix "
            "<thought>SECRET_KEY_12345</thought>"
            " In-between "
            "<thought>PASS_67890</thought>"
            " Suffix"
        )
        for i in range(len(test_payload)):
            list(parser.feed(test_payload[i]))
        list(parser.finalize())

        thought, response = parser.get_summary()
        self.assertIn("SECRET_KEY_12345", thought)
        self.assertIn("PASS_67890", thought)
        self.assertNotIn("SECRET_KEY_12345", response)
        self.assertNotIn("PASS_67890", response)
        self.assertEqual(response, "Prefix  In-between  Suffix")


if __name__ == "__main__":
    unittest.main()
