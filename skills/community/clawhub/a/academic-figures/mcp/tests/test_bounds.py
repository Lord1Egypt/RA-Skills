# -*- coding: utf-8 -*-
"""v1.0.0 边界加固测试（工单 G5）：数据上限/图型白名单/dpi 域/选项映射/单图语义。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server  # noqa: E402


class TestBounds(unittest.TestCase):
    def test_unknown_chart_rejected(self):
        with self.assertRaises(ValueError):
            server.render_chart_impl("not_a_chart", '{"labels":["A"],"series":{"s":[1]}}')

    def test_data_size_cap(self):
        big = "x" * (server.MAX_DATA_BYTES + 10)
        with self.assertRaises(ValueError):
            server.render_chart_impl("bar", big)

    def test_dpi_domain(self):
        for bad in (0, 71, 601, "abc", None):
            with self.assertRaises(ValueError):
                server.render_chart_impl("bar", '{"labels":["A"],"series":{"s":[1]}}', dpi=bad)

    def test_data_must_be_nonempty_str(self):
        for bad in ("", "   ", None, 123):
            with self.assertRaises(ValueError):
                server.render_chart_impl("bar", bad)

    def test_option_whitelist_mapping(self):
        cmd = server._build_cmd(
            "bar", "in.json", "out.png", 150,
            {"title": "T", "subtitle": "S", "verify": True, "cjk": True,
             "legend_outside": True, "peak_label": True, "bogus_key": "x",
             "journal": "nature", "multi_format": "png,pdf"}, "png")
        joined = " ".join(cmd)
        for want in ("--title T", "--subtitle S", "--verify", "--cjk",
                     "--legend-outside", "--peak-label", "--journal nature"):
            self.assertIn(want, joined)
        self.assertNotIn("bogus_key", joined)
        self.assertIn("--multi-format png,pdf", joined)

    def test_json_csv_sniff(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            for data, ext in (('{"labels":["A"]}', "json"), ("a,b\n1,2\n", "csv")):
                inp = os.path.join(td, "in." + ext)
                with open(inp, "w") as fh:
                    fh.write(data)
                cmd = server._build_cmd("bar", inp, os.path.join(td, "o.png"), 80, {}, "png")
                self.assertTrue(cmd[cmd.index("-d") + 1].endswith(ext))


if __name__ == "__main__":
    unittest.main()
