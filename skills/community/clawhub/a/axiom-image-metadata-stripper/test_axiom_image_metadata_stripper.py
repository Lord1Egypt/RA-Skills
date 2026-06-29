"""Tests — axiom-image-metadata-stripper """

from pathlib import Path
import os
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from axiom_image_metadata_stripper import (
    analyze,
    detect_format,
    strip_jpeg,
    strip_metadata,
    strip_png,
)


# Minimal valid JPEG: SOI + minimal APP0 + SOF + SOS + EOI
MINIMAL_JPEG = bytes.fromhex(
    "ffd8ffe000104a46494600010100000100010000"
    "ffdb004300080606070605080707070909080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720222c231c1c2837292c30313434341f27393d38323c2e333432"
    "ffc00011080001000103012200021101031101"
    "ffc4001f0000010501010101010100000000000000000102030405060708090a0b"
    "ffda0008010100003f00fb"
    "ffd9"
)


# Minimal valid PNG: signature + IHDR + IDAT + IEND (with proper CRCs)
import zlib
def _crc(chunk_type_and_data):
    return zlib.crc32(chunk_type_and_data) & 0xFFFFFFFF

ihdr_data = b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00"
ihdr = b"\x00\x00\x00\x0d" + b"IHDR" + ihdr_data + struct.pack(">I", _crc(b"IHDR" + ihdr_data))

idat_data = b"\x08\x99c\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4"
idat = b"\x00\x00\x00\x0c" + b"IDAT" + idat_data + struct.pack(">I", _crc(b"IDAT" + idat_data))

iend = b"\x00\x00\x00\x00" + b"IEND" + struct.pack(">I", _crc(b"IEND"))

MINIMAL_PNG = b"\x89PNG\r\n\x1a\n" + ihdr + idat + iend


class TestDetectFormat(unittest.TestCase):
    def test_01_jpeg(self):
        self.assertEqual(detect_format(MINIMAL_JPEG), "jpeg")

    def test_02_png(self):
        self.assertEqual(detect_format(MINIMAL_PNG), "png")

    def test_03_unknown(self):
        self.assertEqual(detect_format(b"random data"), "unknown")


class TestStripJpeg(unittest.TestCase):
    def test_04_keeps_soi(self):
        result = strip_jpeg(MINIMAL_JPEG)
        self.assertTrue(result.startswith(b"\xff\xd8"))

    def test_05_keeps_eoi(self):
        result = strip_jpeg(MINIMAL_JPEG)
        self.assertTrue(result.endswith(b"\xff\xd9"))

    def test_06_removes_app0(self):
        # Add an APP0 segment and verify it's stripped
        jpeg_with_app0 = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xd9"
        result = strip_jpeg(jpeg_with_app0)
        self.assertNotIn(b"JFIF", result)


class TestStripPng(unittest.TestCase):
    def test_07_keeps_signature(self):
        result = strip_png(MINIMAL_PNG)
        self.assertEqual(result[:8], b"\x89PNG\r\n\x1a\n")

    def test_08_removes_text_chunks(self):
        # Add a tEXt chunk
        text_chunk = b"\x00\x00\x00\x05" + b"tEXt" + b"kdvds" + b"\x00\x00\x00\x00"  # CRC fake
        png_with_text = MINIMAL_PNG[:-12] + text_chunk + MINIMAL_PNG[-12:]
        result = strip_png(png_with_text)
        self.assertNotIn(b"tEXt", result)


class TestStripMetadata(unittest.TestCase):
    def test_09_jpeg_strip(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(MINIMAL_JPEG)
            f.flush()
            in_path = f.name
        out_path = in_path + ".stripped"
        result = strip_metadata(in_path, out_path)
        self.assertEqual(result["format"], "jpeg")
        os.unlink(in_path)
        os.unlink(out_path)

    def test_10_png_strip(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(MINIMAL_PNG)
            f.flush()
            in_path = f.name
        out_path = in_path + ".stripped"
        result = strip_metadata(in_path, out_path)
        self.assertEqual(result["format"], "png")
        os.unlink(in_path)
        os.unlink(out_path)


class TestDeterminism(unittest.TestCase):
    def test_11_1000_runs(self):
        for _ in range(1000):
            result1 = strip_jpeg(MINIMAL_JPEG)
            result2 = strip_jpeg(MINIMAL_JPEG)
            self.assertEqual(result1, result2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
