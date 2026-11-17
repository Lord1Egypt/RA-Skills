from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "scripts" / "create_safe_zone_overlay.py"


class OverlayTests(unittest.TestCase):
    def run_generator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(GEN), *args], text=True, capture_output=True)

    def test_playback_profile_matches_documented_bottom_boundary_and_transparency(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "guide.png"
            result = self.run_generator("--profile", "douyin-playback-reference", "--output", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("safe_rect=x=86, y=170, width=908, height=1462", result.stdout)
            with Image.open(out) as opened:
                image = opened.convert("RGBA")
            self.assertEqual(image.size, (1080, 1920))
            self.assertEqual(image.getpixel((500, 1631))[3], 0)
            self.assertGreater(image.getpixel((500, 1633))[3], 0)

    def test_cover_profile_canvas_and_override(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "cover.png"
            result = self.run_generator("--profile", "douyin-cover-3x4", "--top", "100", "--output", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(out) as image:
                self.assertEqual(image.size, (1080, 1440))
            self.assertIn("y=100", result.stdout)

    def test_impossible_or_negative_margins_fail_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "bad.png"
            negative = self.run_generator("--left", "-1", "--output", str(out))
            self.assertNotEqual(negative.returncode, 0)
            impossible = self.run_generator("--top", "1920", "--output", str(out))
            self.assertNotEqual(impossible.returncode, 0)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
