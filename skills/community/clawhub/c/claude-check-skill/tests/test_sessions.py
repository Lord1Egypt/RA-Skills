import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("sessions", Path(__file__).parents[1] / "scripts/sessions.py")
sessions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sessions)

LINES = [
    {"type": "user", "timestamp": "2026-10-27T08:00:00Z", "message": {"role": "user", "content": "请检查演示项目的配置"}},
    {"type": "assistant", "timestamp": "2026-10-27T08:01:00Z", "message": {"role": "assistant", "content": [
        {"type": "text", "text": "配置已找到"},
        {"type": "tool_use", "name": "x", "input": {"secret": "TOOL-SECRET-NOT-EXPORTED"}}]}},
    {"type": "progress", "data": {"message": "忽略"}},
]


class SessionsTest(unittest.TestCase):
    def tmp_root(self, tmp):
        proj = Path(tmp) / "demo-project"
        proj.mkdir()
        (proj / "s.jsonl").write_text("\n".join(json.dumps(x) for x in LINES), encoding="utf-8")
        return Path(tmp)

    def test_scan_and_parse(self):
        with tempfile.TemporaryDirectory() as tmp:
            items, partial = sessions.scan(self.tmp_root(tmp))
            self.assertEqual(len(items), 1)
            s = items[0]
            self.assertEqual(s["turns"], 2)  # progress 行被忽略
            self.assertEqual(s["title"], "请检查演示项目的配置")
            self.assertEqual(s["project"], "demo-project")

    def test_export_excludes_tool_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            items, _ = sessions.scan(self.tmp_root(tmp))
            md = sessions.markdown(items[0])
            self.assertIn("配置已找到", md)
            self.assertNotIn("TOOL-SECRET-NOT-EXPORTED", md)

    def test_keyword_and_date_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = sessions.scan(self.tmp_root(tmp))[0][0]
            self.assertTrue(sessions.match(s, "演示", "", "", ""))
            self.assertFalse(sessions.match(s, "不存在的词", "", "", ""))
            self.assertFalse(sessions.match(s, "", "", "2027-01-01", ""))
            self.assertTrue(sessions.match(s, "", "demo-project", "2026-01-01", "2026-12-31"))

    def test_symlink_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.tmp_root(tmp)
            link = root / "demo-project" / "link.jsonl"
            try:
                link.symlink_to(root / "demo-project" / "s.jsonl")
            except OSError:
                self.skipTest("无法创建符号链接")
            items, _ = sessions.scan(root)
            self.assertEqual(len(items), 1)  # 只有真实文件，符号链接被跳过

    def test_home_root_rejected(self):
        with self.assertRaises(SystemExit):
            sessions.scan(Path.home())


if __name__ == "__main__":
    unittest.main()
