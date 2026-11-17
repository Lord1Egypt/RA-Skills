# -*- coding: utf-8 -*-
"""0.11.0 回归:qc 渲染对账(PNG 解码/大底真伪/板外入侵)。"""
import json
import os
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import qc_kit  # noqa: E402
import token_sheet  # noqa: E402

DP = ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"]


def write_png(path, w, h, rows, filters=None):
    """rows = list of scanlines(list of (r,g,b));filters 缺省全 0(None)。"""
    ch = 3
    raw = bytearray()
    for y, row in enumerate(rows):
        ft = filters[y] if filters else 0
        raw.append(ft)
        if ft == 0:
            for (r, g, b) in row:
                raw += bytes((r, g, b))
        elif ft == 2:  # up: raw = 当前行 - 前一行
            prev = rows[y - 1]
            for i, (r, g, b) in enumerate(row):
                pr, pg, pb = prev[i]
                raw += bytes(((r - pr) & 0xFF, (g - pg) & 0xFF, (b - pb) & 0xFF))
        elif ft == 1:  # sub
            prev = row
            for i, (r, g, b) in enumerate(row):
                if i:
                    pr, pg, pb = prev[i - 1]
                    raw += bytes(((r - pr) & 0xFF, (g - pg) & 0xFF, (b - pb) & 0xFF))
                else:
                    raw += bytes((r, g, b))

    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw)))
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)


def solid_row(w, rgb):
    return [rgb] * w


class TestPngDecode(unittest.TestCase):
    """纯 stdlib 解码器:过滤 0/1/2 三路径+往返一致。"""

    def test_roundtrip_filters(self):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "t.png")
            r, g_, b_, w_ = (200, 60, 40), (10, 80, 120), (239, 246, 224), (255, 255, 255)
            rows = [solid_row(6, w_), solid_row(6, r), solid_row(6, g_), solid_row(6, b_)]
            write_png(p, 6, 4, rows, filters=[0, 1, 2, 0])
            w, h, pixels = qc_kit.decode_png(p)
            self.assertEqual((w, h), (6, 4))
            self.assertEqual(pixels[0], w_)
            self.assertEqual(pixels[7], r)      # 第 2 行(sub 过滤)
            self.assertEqual(pixels[12 + 3], g_)  # 第 3 行(up 过滤)
            self.assertEqual(pixels[-1], b_)


class TestQcVerdicts(unittest.TestCase):
    """大底真伪与板外入侵的裁决。"""

    def _img(self, td, name, bands):
        """bands = [(hex, share)] → 竖条带图(每条带 ≥3 行)。"""
        rows, rgbs = [], []
        for hx, _sh in bands:
            rgb = tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))
            rgbs.append(rgb)
        total = 24
        shares = [max(3, round(s * total)) for _, s in bands]
        shares[-1] = total - sum(shares[:-1])
        for rgb, n in zip(rgbs, shares):
            rows += [solid_row(8, rgb) for _ in range(n)]
        p = os.path.join(td, name)
        write_png(p, 8, total, rows)
        return p

    def test_pass_on_palette(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._img(td, "ok.png", [("EFF6E0", 0.5), ("124559", 0.25),
                                         ("AEC3B0", 0.15), ("01161E", 0.1)])
            payload = qc_kit.qc_image(p, DP, bg="EFF6E0")
            self.assertEqual(payload["verdict"], "PASS",
                             json.dumps(payload["findings"], ensure_ascii=False))

    def test_bg_mismatch_fail(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._img(td, "bad.png", [("FFFFFF", 0.6), ("124559", 0.3), ("AEC3B0", 0.1)])
            payload = qc_kit.qc_image(p, DP, bg="EFF6E0")
            checks = {f["check"] for f in payload["findings"]}
            self.assertIn("bg_mismatch", checks)
            self.assertEqual(payload["verdict"], "FAIL")

    def test_off_palette_fail(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._img(td, "intruder.png", [("EFF6E0", 0.5), ("7C5CFF", 0.3), ("124559", 0.2)])
            payload = qc_kit.qc_image(p, DP, bg="EFF6E0")
            checks = {f["check"] for f in payload["findings"]}
            self.assertIn("off_palette", checks)
            self.assertEqual(payload["verdict"], "FAIL")


class TestCliEndToEnd(unittest.TestCase):
    def test_qc_cli_with_tokens(self):
        engine = os.path.join(ROOT, "scripts", "palette_forge.py")
        with tempfile.TemporaryDirectory() as td:
            tok = os.path.join(td, "tokens")
            token_sheet.emit(DP, "Deep Pine", out_base=tok)
            tk = json.load(open(tok + ".json", encoding="utf-8"))
            bg = tk["tokens"]["bg"].lstrip("#")
            rgb = tuple(int(bg[i:i + 2], 16) for i in (0, 2, 4))
            p = os.path.join(td, "shot.png")
            rows = [solid_row(10, rgb) for _ in range(10)]
            write_png(p, 10, 10, rows)
            r = subprocess.run(
                [sys.executable, engine, "qc", p, "--tokens", tok + ".json"],
                capture_output=True, text=True, timeout=120)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("PASS", r.stdout)


if __name__ == "__main__":
    unittest.main()
