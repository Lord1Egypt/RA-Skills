#!/usr/bin/env python3
"""Unit tests for scripts/detect.py.

Stdlib only (unittest). No network. Run via:
    python -m unittest evals.test_detect -v
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

# Make scripts/ importable when run from repo root.
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from detect import classify  # noqa: E402


class TestDetect(unittest.TestCase):
    """Each test asserts the full JSON payload contract."""

    def _classify(self, url: str) -> dict:
        return classify(url)

    # --- platform_video ---

    def test_x_twitter_video(self):
        r = self._classify("https://x.com/HarrisDecodes/status/2107839872144900463/video/1")
        self.assertEqual(r["kind"], "platform_video")
        self.assertEqual(r["suggested_tool"], "yt-dlp")
        self.assertEqual(r["host"], "x.com")
        self.assertIn("2107839872144900463", r["dest_name"])
        self.assertTrue(r["dest_name"].endswith(".mp4"))
        self.assertIn("ffprobe", r["verify_cmd"])
        self.assertEqual(r["install_hint"]["name"], "yt-dlp")

    def test_twitter_short_domain(self):
        r = self._classify("https://twitter.com/foo/status/1234567890/video/1")
        self.assertEqual(r["kind"], "platform_video")
        self.assertEqual(r["suggested_tool"], "yt-dlp")
        self.assertIn("1234567890", r["dest_name"])

    def test_youtube_watch(self):
        r = self._classify("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertEqual(r["kind"], "platform_video")
        self.assertEqual(r["suggested_tool"], "yt-dlp")
        self.assertIn("dQw4w9WgXcQ", r["dest_name"])

    def test_youtube_short(self):
        r = self._classify("https://youtu.be/dQw4w9WgXcQ")
        self.assertEqual(r["kind"], "platform_video")
        self.assertIn("dQw4w9WgXcQ", r["dest_name"])

    def test_bilibili(self):
        r = self._classify("https://www.bilibili.com/video/BV1x411c7mD/")
        self.assertEqual(r["kind"], "platform_video")
        self.assertEqual(r["suggested_tool"], "yt-dlp")

    def test_douyin(self):
        r = self._classify("https://www.douyin.com/video/7365934524233212345")
        self.assertEqual(r["kind"], "platform_video")

    # --- direct_file ---

    def test_direct_mp4(self):
        r = self._classify("https://example.com/path/to/video.mp4")
        self.assertEqual(r["kind"], "direct_file")
        self.assertEqual(r["suggested_tool"], "curl")
        self.assertEqual(r["dest_name"], "video.mp4")
        self.assertIn("ffprobe", r["verify_cmd"])

    def test_direct_pdf(self):
        r = self._classify("https://example.com/report.pdf")
        self.assertEqual(r["kind"], "direct_file")
        self.assertEqual(r["suggested_tool"], "curl")
        self.assertEqual(r["dest_name"], "report.pdf")
        self.assertEqual(r["verify_cmd"], "file")

    def test_direct_archive(self):
        r = self._classify("https://cdn.example.com/files/backup.tar.gz")
        self.assertEqual(r["kind"], "direct_file")
        self.assertEqual(r["suggested_tool"], "curl")
        self.assertEqual(r["dest_name"], "backup.tar.gz")
        self.assertEqual(r["verify_cmd"], "file")

    def test_direct_image(self):
        r = self._classify("https://img.example.com/photo.jpg")
        self.assertEqual(r["kind"], "direct_file")
        self.assertEqual(r["suggested_tool"], "curl")
        self.assertEqual(r["dest_name"], "photo.jpg")

    # --- torrent ---

    def test_torrent_file_url(self):
        r = self._classify("https://tracker.example.com/movies/some-movie.torrent")
        self.assertEqual(r["kind"], "torrent")
        self.assertEqual(r["suggested_tool"], "curl")
        self.assertEqual(r["dest_name"], "some-movie.torrent")
        self.assertEqual(r["verify_cmd"], "file")
        # v0.2: install_hint 空（curl 不需要装 aria2）
        self.assertEqual(r["install_hint"], {})
        # v0.2: user_action 提示用户
        self.assertIn("user_action", r)
        self.assertIn(".torrent 文件本体", r["user_action"])

    # --- magnet ---

    def test_magnet_with_dn(self):
        r = self._classify("magnet:?xt=urn:btih:abc123def&dn=Test%20Movie")
        self.assertEqual(r["kind"], "magnet")
        self.assertEqual(r["suggested_tool"], "none")
        self.assertEqual(r["dest_name"], "Test Movie")
        # v0.2: 不再需要 aria2c
        self.assertEqual(r["install_hint"], {})
        # v0.2: user_action 提示用客户端
        self.assertIn("user_action", r)
        self.assertIn("客户端", r["user_action"])
        # v0.2: reason 说明为什么不处理
        self.assertIn("reason", r)
        self.assertIn("元数据", r["reason"])

    def test_magnet_without_dn(self):
        r = self._classify("magnet:?xt=urn:btih:abc123def")
        self.assertEqual(r["kind"], "magnet")
        self.assertEqual(r["dest_name"], "magnet-download")

    # --- unknown ---

    def test_unknown_bare_page(self):
        r = self._classify("https://some-site.com/some/path")
        self.assertEqual(r["kind"], "unknown")
        self.assertEqual(r["suggested_tool"], "curl")

    def test_unknown_alfafile_short_link(self):
        # CGPersia-style resource aggregator: not in platform whitelist,
        # path is /file/SHORT_ID with no extension.
        r = self._classify("https://alfafile.net/file/AXAFy")
        self.assertEqual(r["kind"], "unknown")
        self.assertEqual(r["suggested_tool"], "curl")

    # --- edge cases ---

    def test_platform_site_wins_over_extension(self):
        # Even if a YouTube URL somehow had an extension, platform check comes first.
        r = self._classify("https://www.youtube.com/some/video.mp4")
        self.assertEqual(r["kind"], "platform_video")

    def test_json_is_serializable(self):
        # Sanity check: contract is a plain dict with JSON-serializable fields.
        r = self._classify("https://example.com/x.mp4")
        serialized = json.dumps(r, ensure_ascii=False)
        self.assertIsInstance(serialized, str)
        self.assertIn('"kind"', serialized)
        self.assertIn('"dest_name"', serialized)
        self.assertIn('"suggested_tool"', serialized)
        self.assertIn('"verify_cmd"', serialized)
        self.assertIn('"install_hint"', serialized)
        # v0.2: new fields
        self.assertIn('"user_action"', serialized)
        self.assertIn('"reason"', serialized)

    # --- cloud_drive (v0.2) ---

    def test_cloud_drive_baidu_pan(self):
        r = self._classify("https://pan.baidu.com/s/1aBcDeFgHijKlMn")
        self.assertEqual(r["kind"], "cloud_drive")
        self.assertEqual(r["suggested_tool"], "none")
        self.assertIsNone(r["dest_name"])
        self.assertIsNone(r["verify_cmd"])
        self.assertEqual(r["install_hint"], {})
        self.assertIn("百度网盘", r["user_action"])
        self.assertIn("转存", r["user_action"])

    def test_cloud_drive_baidu_yun(self):
        r = self._classify("https://yun.baidu.com/s/xyz")
        self.assertEqual(r["kind"], "cloud_drive")
        self.assertIn("百度网盘", r["user_action"])

    def test_cloud_drive_quark(self):
        r = self._classify("https://pan.quark.cn/s/abc123")
        self.assertEqual(r["kind"], "cloud_drive")
        self.assertIn("夸克网盘", r["user_action"])

    def test_cloud_drive_aliyundrive(self):
        r = self._classify("https://www.aliyundrive.com/s/xyz")
        self.assertEqual(r["kind"], "cloud_drive")
        self.assertIn("阿里云盘", r["user_action"])

    def test_cloud_drive_alipan(self):
        r = self._classify("https://www.alipan.com/s/abc")
        self.assertEqual(r["kind"], "cloud_drive")
        self.assertIn("阿里云盘", r["user_action"])

    def test_cloud_drive_115(self):
        r = self._classify("https://115.com/snapshot/abc123")
        self.assertEqual(r["kind"], "cloud_drive")
        self.assertIn("115 网盘", r["user_action"])

    def test_cloud_drive_115cdn(self):
        r = self._classify("https://115cdn.com/x")
        self.assertEqual(r["kind"], "cloud_drive")
        self.assertIn("115 网盘", r["user_action"])

    def test_cloud_drive_tianyi(self):
        r = self._classify("https://cloud.189.cn/t/abc")
        self.assertEqual(r["kind"], "cloud_drive")
        self.assertIn("天翼云盘", r["user_action"])

    def test_cloud_drive_weiyun(self):
        r = self._classify("https://wl.123pan.com/s/abc")
        self.assertEqual(r["kind"], "cloud_drive")
        self.assertIn("腾讯微云", r["user_action"])

    def test_cloud_drive_wenku(self):
        r = self._classify("https://wenku.baidu.com/view/abc")
        self.assertEqual(r["kind"], "cloud_drive")
        self.assertIn("百度文库", r["user_action"])

    def test_cloud_drive_all_have_reason(self):
        """Every cloud_drive result has a reason field."""
        for host in ("pan.baidu.com", "yun.baidu.com", "pan.quark.cn",
                     "www.aliyundrive.com", "www.alipan.com",
                     "115.com", "115cdn.com", "cloud.189.cn",
                     "wl.123pan.com", "wenku.baidu.com"):
            r = self._classify(f"https://{host}/x")
            self.assertEqual(r["kind"], "cloud_drive", f"host={host}")
            self.assertIsNotNone(r["reason"], f"host={host}")
            self.assertIn("转存", r["reason"], f"host={host}")

    # --- edge cases (v0.2) ---

    def test_empty_string(self):
        r = self._classify("")
        self.assertEqual(r["kind"], "unknown")
        self.assertEqual(r["suggested_tool"], "curl")
        self.assertEqual(r["host"], "")

    def test_file_scheme(self):
        # file:// with .mp4 extension is classified as direct_file (extension-based)
        # We don't special-case file:// — caller can decide whether to handle it.
        r = self._classify("file:///Users/foo/bar.mp4")
        self.assertEqual(r["kind"], "direct_file")
        self.assertEqual(r["host"], "")

    def test_javascript_scheme(self):
        r = self._classify("javascript:alert(1)")
        self.assertEqual(r["kind"], "unknown")

    def test_url_with_credentials(self):
        r = self._classify("https://user:pass@example.com/file.mp4")
        self.assertEqual(r["kind"], "direct_file")
        self.assertEqual(r["dest_name"], "file.mp4")
        # credentials should not leak into dest_name
        self.assertNotIn("user:pass", r["dest_name"])

    def test_ipv6_address(self):
        r = self._classify("https://[::1]:8080/file.mp4")
        self.assertEqual(r["kind"], "direct_file")
        self.assertEqual(r["dest_name"], "file.mp4")

    def test_long_url(self):
        long_query = "a" * 4500
        url = f"https://example.com/file.mp4?{long_query}"
        r = self._classify(url)
        self.assertEqual(r["kind"], "direct_file")
        self.assertEqual(r["dest_name"], "file.mp4")

    def test_emoji_in_path(self):
        # URL-encoded waving hand emoji 👋
        r = self._classify("https://example.com/%F0%9F%91%8B-video.mp4")
        self.assertEqual(r["kind"], "direct_file")
        self.assertIn("-video.mp4", r["dest_name"])
        self.assertEqual(len(r["dest_name"]), len("-video.mp4") + 1)

    # --- dest_name sanitization (v0.2, A6) ---

    def test_sanitize_path_traversal_encoded(self):
        r = self._classify("https://evil.com/%2e%2e%2fpasswd")
        # After URL decode: ../../passwd → path traversal → download
        self.assertNotIn("..", r["dest_name"])
        self.assertEqual(r["dest_name"], "download")

    def test_sanitize_shell_dollar(self):
        r = self._classify("https://evil.com/foo$bar.mp4")
        self.assertEqual(r["dest_name"], "foo_bar.mp4")

    def test_sanitize_shell_pipe(self):
        r = self._classify("https://evil.com/a|b/c|d.mp4")
        # / and | both replaced with _
        self.assertEqual(r["dest_name"], "c_d.mp4")

    def test_sanitize_control_char(self):
        # URL-encoded newline %0A
        r = self._classify("https://evil.com/foo%0Abar.mp4")
        self.assertNotIn("\n", r["dest_name"])
        self.assertEqual(r["dest_name"], "foobar.mp4")

    def test_sanitize_url_with_spaces(self):
        r = self._classify("https://example.com/my%20file.mp4")
        self.assertEqual(r["dest_name"], "my file.mp4")

    def test_sanitize_emoji(self):
        # URL-encoded moon face 🌝
        r = self._classify("https://example.com/%F0%9F%8C%9D.mp4")
        self.assertEqual(r["dest_name"], "\U0001F31D.mp4")


if __name__ == "__main__":
    unittest.main(verbosity=2)
