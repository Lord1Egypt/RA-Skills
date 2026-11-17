import pathlib
import sys
import unittest
from unittest.mock import patch


sys.path.insert(0, str(pathlib.Path(__file__).parents[1] / "scripts"))
import douyin_download as MODULE


class MediaToolDiscoveryTests(unittest.TestCase):
    def test_prefers_executable_found_on_path(self):
        with patch.object(MODULE.shutil, "which", return_value="/tools/ffmpeg"):
            self.assertEqual(MODULE.find_media_tool("ffmpeg"), "/tools/ffmpeg")

    def test_windows_does_not_use_macos_homebrew_path(self):
        with patch.object(MODULE.sys, "platform", "win32"), \
                patch.object(MODULE.shutil, "which", return_value=None), \
                patch.object(MODULE.os.path, "isfile", return_value=True):
            self.assertIsNone(MODULE.find_media_tool("ffprobe"))

    def test_apple_silicon_homebrew_path_is_fallback(self):
        with patch.object(MODULE.sys, "platform", "darwin"), \
                patch.object(MODULE.shutil, "which", return_value=None), \
                patch.object(MODULE.os.path, "isfile", return_value=True):
            self.assertEqual(
                MODULE.find_media_tool("ffprobe"), "/opt/homebrew/bin/ffprobe"
            )

    def test_missing_ffprobe_skips_probe_cleanly(self):
        with patch.object(MODULE, "FFPROBE_BIN", None):
            self.assertIsNone(MODULE.probe("unused.mp4"))


if __name__ == "__main__":
    unittest.main()
