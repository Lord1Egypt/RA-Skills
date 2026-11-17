import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("redact", ROOT / "scripts" / "redact.py")
redact = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(redact)


class BoxParsingTests(unittest.TestCase):
    def test_text_box_exact_mapping(self):
        text, box = redact.parse_text_box("张三=1,2,30,40", (100, 100))
        self.assertEqual(text, "张三")
        self.assertEqual(box, (1, 2, 30, 40))

    def test_text_box_rejects_missing_text(self):
        with self.assertRaisesRegex(ValueError, "TEXT 不得为空"):
            redact.parse_text_box("=1,2,3,4", (100, 100))

    def test_rejects_reversed_box(self):
        with self.assertRaisesRegex(ValueError, "x1 < x2"):
            redact.validate_box((10, 2, 5, 20), (100, 100), "--box")

    def test_rejects_out_of_bounds_box(self):
        with self.assertRaisesRegex(ValueError, "超出图像范围"):
            redact.validate_box((1, 2, 101, 20), (100, 100), "--box")


class WorkflowTests(unittest.TestCase):
    def make_image(self, path, size=(80, 60)):
        Image.new("RGB", size, (220, 220, 220)).save(path)

    def manifests(self, directory):
        return list(Path(directory).glob("*_verification-manifest.json"))

    def test_text_box_bypasses_ocr_and_writes_source(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory) / "src.png"
            out = Path(directory) / "out.png"
            verify = Path(directory) / "verify"
            self.make_image(src)
            with mock.patch.object(
                redact, "find_text_boxes", side_effect=AssertionError("不应调用 OCR")
            ):
                result = redact.main(
                    [
                        "--src",
                        str(src),
                        "--text",
                        "张三",
                        "--text-box",
                        "张三=10,10,30,25",
                        "--out",
                        str(out),
                        "--verify-dir",
                        str(verify),
                    ]
                )
            self.assertEqual(result, 0)
            self.assertTrue(out.exists())
            manifest = json.loads(self.manifests(verify)[0].read_text())
            self.assertEqual(manifest["requestedTexts"][0]["method"], "text-box")
            self.assertEqual(manifest["status"], "completed")

    def test_low_score_target_fails_nonzero_without_success_images(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory) / "src.png"
            target = Path(directory) / "target.png"
            out = Path(directory) / "out.png"
            target_out = Path(directory) / "target-out"
            verify = Path(directory) / "verify"
            self.make_image(src)
            self.make_image(target)
            with mock.patch.object(
                redact, "match_transform", return_value=(1.0, 0, 0, 0.40)
            ):
                with self.assertRaises(SystemExit) as raised:
                    redact.main(
                        [
                            "--src",
                            str(src),
                            "--text",
                            "张三",
                            "--text-box",
                            "张三=10,10,30,25",
                            "--targets",
                            str(target),
                            "--out",
                            str(out),
                            "--target-out",
                            str(target_out),
                            "--verify-dir",
                            str(verify),
                        ]
                    )
            self.assertNotEqual(str(raised.exception), "0")
            self.assertFalse(out.exists())
            self.assertFalse((target_out / target.name).exists())
            manifest = json.loads(self.manifests(verify)[0].read_text())
            self.assertEqual(manifest["status"], "failed")
            self.assertEqual(manifest["targets"][0]["status"], "low_score")

    def test_each_target_status_is_written_to_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory) / "src.png"
            target = Path(directory) / "target.png"
            target_out = Path(directory) / "target-out"
            verify = Path(directory) / "verify"
            self.make_image(src)
            self.make_image(target)
            with mock.patch.object(
                redact, "match_transform", return_value=(1.0, 0, 0, 0.99)
            ):
                result = redact.main(
                    [
                        "--src",
                        str(src),
                        "--text",
                        "张三",
                        "--text-box",
                        "张三=10,10,30,25",
                        "--targets",
                        str(target),
                        "--target-out",
                        str(target_out),
                        "--verify-dir",
                        str(verify),
                    ]
                )
            self.assertEqual(result, 0)
            self.assertTrue((target_out / target.name).exists())
            manifest = json.loads(self.manifests(verify)[0].read_text())
            self.assertEqual(manifest["targets"][0]["status"], "written")
            self.assertGreaterEqual(manifest["targets"][0]["score"], 0.85)

    def test_invalid_cli_box_fails_before_output(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory) / "src.png"
            out = Path(directory) / "out.png"
            self.make_image(src)
            with self.assertRaises(SystemExit):
                redact.main(
                    [
                        "--src",
                        str(src),
                        "--box",
                        "0,0,1000,20",
                        "--out",
                        str(out),
                    ]
                )
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
