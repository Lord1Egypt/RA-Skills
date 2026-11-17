#!/usr/bin/env python3
"""Business regression checks; no network, media tools, icon or license checks."""

import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
from build_metadata import InputError, build, handoff, iso_duration, read_document


ROOT = Path(__file__).resolve().parents[1]
INVALID_TIMEZONE_OFFSETS = (
    "+08:60", "-08:60", "+00:60", "-00:60", "+23:60", "-23:60",
    "+08:99", "-08:99", "+24:00", "-24:00",
)


def sample():
    return read_document(ROOT / "examples/success/input.json")


def audio():
    return read_document(ROOT / "examples/success/audio-input.json")


class MetadataTests(unittest.TestCase):
    def test_sample_three_screenshots_and_one_video(self):
        source = sample()
        result = build(source)
        self.assertEqual(result["summary"], {
            "total": 4, "by_type": {"image": 3, "video": 1, "audio": 0},
            "needs_information": 4,
            "by_evidence": {"reviewed": 0, "user_description": 3, "unavailable": 1}})
        image, video = result["assets"][0], result["assets"][3]
        self.assertEqual(image["suggested_filename"], "教程-新建项目-入口.PNG")
        self.assertEqual(image["alt"], source["assets"][0]["alt"])
        self.assertEqual(image["evidence"]["kind"], "user_description")
        self.assertEqual(image["schema"]["jsonld"]["@type"], "ImageObject")
        self.assertEqual(video["suggested_filename"], "教程-项目操作演示.MOV")
        self.assertNotIn("alt", video)
        self.assertIsNone(video["description"])
        self.assertIsNone(video["caption"])
        self.assertEqual(video["duration_iso8601"], "PT2M5S")
        self.assertIsNone(video["upload_date"])
        self.assertIsNone(video["thumbnail_url"])
        self.assertIsNone(video["chapters"])
        self.assertEqual(video["subtitles"]["status"], "missing")
        self.assertTrue({"evidence", "upload_date", "thumbnail_url", "subtitles", "chapters"}
                        <= set(video["gaps"]))
        self.assertNotIn("uploadDate", video["schema"]["jsonld"])
        self.assertEqual(video["schema"]["status"], "partial")

    def test_audio_keeps_suffix_and_has_no_image_or_video_fields(self):
        asset = build(audio())["assets"][0]
        self.assertEqual(asset["suggested_filename"], "操作完成-提示音.WAV")
        self.assertEqual(asset["schema"]["jsonld"]["@type"], "AudioObject")
        self.assertEqual(asset["duration_iso8601"], "PT1.25S")
        for field in ("alt", "decorative", "thumbnail_url", "subtitles"):
            self.assertNotIn(field, asset)
        self.assertEqual(asset["transcript"]["status"], "not_applicable")
        self.assertNotIn("transcript", asset["gaps"])
        self.assertIn("upload_date", asset["gaps"])

    def test_unavailable_media_stays_unknown_not_empty_alt(self):
        source = {"assets": [copy.deepcopy(sample()["assets"][3])]}
        asset = source["assets"][0]
        asset["type"], asset["original_filename"] = "image", "未知.png"
        for field in ("duration_seconds", "upload_date", "thumbnail_url", "subtitles", "chapters"):
            asset.pop(field, None)
        result = build(source)["assets"][0]
        self.assertIsNone(result["alt"])
        self.assertIn("evidence", result["gaps"])
        self.assertIn("alt", result["gaps"])
        self.assertNotIn("description", result["schema"]["jsonld"])

    def test_unseen_description_failure_fixture(self):
        with self.assertRaisesRegex(InputError, "unavailable evidence cannot support"):
            build(read_document(ROOT / "examples/failure/unseen-description.json"))

    def test_mismatched_type_failure_fixture(self):
        with self.assertRaisesRegex(InputError, "extension does not match video"):
            build(read_document(ROOT / "examples/failure/type-mismatch.json"))

    def test_decorative_image_explicit_empty_alt_no_schema(self):
        raw = sample()["assets"][0]
        raw.update({"decorative": True, "alt": ""})
        result = build({"assets": [raw]})["assets"][0]
        self.assertEqual(result["alt"], "")
        self.assertEqual(result["schema"]["status"], "not_applicable")
        self.assertIsNone(result["schema"]["jsonld"])
        raw["alt"] = "装饰背景"
        with self.assertRaisesRegex(InputError, "decorative image requires empty alt"):
            build({"assets": [raw]})

    def test_empty_alt_is_not_a_substitute_for_missing_info(self):
        raw = sample()["assets"][0]
        raw["alt"] = ""
        with self.assertRaisesRegex(InputError, "empty alt requires decorative true"):
            build({"assets": [raw]})

    def test_no_descriptive_prose_is_generated_from_evidence(self):
        raw = sample()["assets"][0]
        raw.pop("alt")
        raw.pop("caption")
        result = build({"assets": [raw]})["assets"][0]
        self.assertIsNone(result["alt"])
        self.assertIsNone(result["caption"])
        self.assertIn("alt", result["gaps"])

    def test_safe_chinese_collision_names_do_not_rename_sources(self):
        raw = sample()["assets"][0]
        raw["filename_stem"] = '../教程:入口?* "'
        twin = copy.deepcopy(raw)
        twin["id"], twin["original_filename"] = "twin", "另图.png"
        source = {"assets": [raw, twin]}
        before = copy.deepcopy(source)
        assets = build(source)["assets"]
        self.assertEqual(assets[0]["suggested_filename"], "教程-入口.PNG")
        self.assertEqual(assets[1]["suggested_filename"], "教程-入口-2.png")
        self.assertEqual(source, before)
        raw["filename_stem"] = "CON"
        self.assertEqual(build({"assets": [raw]})["assets"][0]["suggested_filename"], "asset-CON.PNG")
        raw["original_filename"] = "../原图.png"
        with self.assertRaisesRegex(InputError, "expected basename"):
            build({"assets": [raw]})

    def test_complete_video_schema_uses_only_supplied_facts(self):
        raw = sample()["assets"][3]
        raw.update({
            "evidence": {"kind": "user_description", "scope": "excerpt",
                         "reference": "受控样例，用户说明00:00–00:10片段",
                         "details": "开头介绍项目操作流程。"},
            "description": "开头介绍项目操作流程。", "caption": "项目操作演示开头片段。",
            "upload_date": "2026-10-18T10:00:00+08:00",
            "content_url": "https://example.com/media/demo.MOV",
            "thumbnail_url": "https://example.com/media/cover.png",
            "page_url": "https://example.com/tutorial",
            "chapters": [{"start_seconds": 0, "title": "流程介绍"}],
            "subtitles": {"status": "provided", "reference": "用户附件：片段字幕.vtt"}})
        asset = build({"assets": [raw]})["assets"][0]
        schema = asset["schema"]
        self.assertEqual(schema["status"], "fields_present")
        self.assertEqual(asset["status"], "ready_for_review")
        self.assertEqual(schema["missing_fields"], [])
        self.assertEqual(schema["jsonld"]["@type"], "VideoObject")
        self.assertEqual(schema["jsonld"]["uploadDate"], raw["upload_date"])
        self.assertEqual(schema["jsonld"]["isPartOf"], {"@id": raw["page_url"]})
        self.assertEqual(schema["jsonld"]["hasPart"], [
            {"@type": "Clip", "name": "流程介绍", "startOffset": 0}])
        self.assertEqual(asset["evidence"]["scope"], "excerpt")

    def test_missing_duration_and_date_are_pending(self):
        raw = sample()["assets"][3]
        raw.pop("duration_seconds")
        asset = build({"assets": [raw]})["assets"][0]
        self.assertIsNone(asset["duration_iso8601"])
        self.assertIn("duration_seconds", asset["gaps"])
        self.assertIn("upload_date", asset["gaps"])
        self.assertNotIn("duration", asset["schema"]["jsonld"])
        self.assertNotIn("uploadDate", asset["schema"]["jsonld"])

    def test_duration_numeric_boundaries_and_iso_conversion(self):
        self.assertEqual(iso_duration(60), "PT1M")
        self.assertEqual(iso_duration(3600), "PT1H")
        self.assertEqual(iso_duration(3661.25), "PT1H1M1.25S")
        self.assertEqual(iso_duration(0.01), "PT0.01S")
        for invalid in (0, -2, True, "125", float("nan"), float("inf")):
            with self.subTest(value=invalid):
                raw = audio()["assets"][0]
                raw["duration_seconds"] = invalid
                with self.assertRaises(InputError):
                    build({"assets": [raw]})

    def test_large_and_tiny_finite_durations_preserve_exact_seconds(self):
        original_precision = getcontext().prec
        for value in (1e32, 10 ** 32 + 1, 1e308, 5e-324):
            with self.subTest(value=value):
                duration = iso_duration(value)
                parts = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?", duration)
                self.assertIsNotNone(parts, duration)
                hours, minutes, seconds = (Fraction(p or "0") for p in parts.groups())
                self.assertEqual(hours * 3600 + minutes * 60 + seconds,
                                 Fraction(Decimal(str(value))))
                self.assertEqual(getcontext().prec, original_precision)

    def test_large_duration_cli_delivers_metadata_without_traceback(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            source = temp / "large-duration.json"
            for index, value in enumerate((1e32, 1e308)):
                with self.subTest(value=value):
                    data = audio()
                    data["assets"][0]["duration_seconds"] = value
                    source.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
                    out = temp / str(index)
                    done = subprocess.run([sys.executable, str(ROOT / "scripts/build_metadata.py"),
                                           "--input", str(source), "--output-dir", str(out)],
                                          capture_output=True, text=True)
                    self.assertEqual((done.returncode, done.stderr), (0, ""))
                    asset = read_document(out / "媒体元信息.json")["assets"][0]
                    self.assertEqual(asset["duration_seconds"], value)
                    self.assertEqual(asset["schema"]["jsonld"]["duration"], asset["duration_iso8601"])
                    self.assertIn(asset["duration_iso8601"],
                                  (out / "图注与字幕交接清单.md").read_text(encoding="utf-8"))

    def test_impossible_dates_and_unzoned_times_rejected(self):
        for invalid in ("2026-02-30", "2026-10-18T10:00:00", "yesterday"):
            with self.subTest(value=invalid):
                raw = audio()["assets"][0]
                raw["upload_date"] = invalid
                with self.assertRaises(InputError):
                    build({"assets": [raw]})

    def test_valid_upload_dates_preserved_in_metadata_and_jsonld(self):
        valid_dates = (
            "2026-10-18", "2026-10-18T10:00:00Z",
            "2026-10-18T10:00:00.123456Z",
            *(f"2026-10-18T10:00:00{offset}" for offset in (
                "+00:00", "-00:00", "+08:00", "+00:59", "-00:59",
                "+08:59", "-08:59", "+23:59", "-23:59")),
            "2026-10-18T10:00:00.123456-08:59",
        )
        for raw in (audio()["assets"][0], sample()["assets"][3]):
            for value in valid_dates:
                with self.subTest(kind=raw["type"], value=value):
                    raw["upload_date"] = value
                    asset = build({"assets": [raw]})["assets"][0]
                    self.assertEqual(asset["upload_date"], value)
                    self.assertEqual(asset["schema"]["jsonld"]["uploadDate"], value)
                    self.assertNotIn("upload_date", asset["gaps"])

    def test_invalid_timezone_components_rejected_without_normalization(self):
        for raw in (audio()["assets"][0], sample()["assets"][3]):
            for offset in INVALID_TIMEZONE_OFFSETS:
                for fraction in ("", ".123456"):
                    value = f"2026-10-18T10:00:00{fraction}{offset}"
                    with self.subTest(kind=raw["type"], value=value):
                        raw["upload_date"] = value
                        with self.assertRaises(InputError):
                            build({"assets": [raw]})

    def test_cli_invalid_timezone_exits_two_without_writing_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "input.json"
            output_dir = Path(temp) / "out"
            rejected_dir = Path(temp) / "rejected"
            cli = [sys.executable, str(ROOT / "scripts/build_metadata.py"),
                   "--input", str(source)]
            for raw in (audio()["assets"][0], sample()["assets"][3]):
                raw["upload_date"] = "2026-10-18T10:00:00+08:59"
                source.write_text(json.dumps({"assets": [raw]}), encoding="utf-8")
                success = subprocess.run(cli + ["--output-dir", str(output_dir)],
                                         capture_output=True, text=True)
                self.assertEqual(success.returncode, 0, success.stderr)
                asset = read_document(output_dir / "媒体元信息.json")["assets"][0]
                self.assertEqual(asset["upload_date"], raw["upload_date"])
                self.assertEqual(asset["schema"]["jsonld"]["uploadDate"], raw["upload_date"])
                before = {path.name: path.read_bytes() for path in output_dir.iterdir()}
                for offset in INVALID_TIMEZONE_OFFSETS:
                    raw["upload_date"] = f"2026-10-18T10:00:00{offset}"
                    source.write_text(json.dumps({"assets": [raw]}), encoding="utf-8")
                    for target in (output_dir, rejected_dir):
                        with self.subTest(kind=raw["type"], offset=offset, target=target.name):
                            failure = subprocess.run(cli + ["--output-dir", str(target)],
                                                     capture_output=True, text=True)
                            self.assertEqual(failure.returncode, 2, failure.stderr)
                            self.assertIn("assets[0].upload_date:", failure.stderr)
                            self.assertNotIn("Traceback", failure.stderr)
                            self.assertEqual(failure.stdout, "")
                            self.assertFalse(rejected_dir.exists())
                            self.assertEqual(
                                {path.name: path.read_bytes() for path in output_dir.iterdir()}, before)

    def test_chapters_must_be_ordered_and_inside_duration(self):
        for points in ([0, 0], [20, 10], [-1], [125], [126]):
            with self.subTest(points=points):
                raw = sample()["assets"][3]
                raw["chapters"] = [{"start_seconds": p, "title": "已提供章节"} for p in points]
                with self.assertRaises(InputError):
                    build({"assets": [raw]})

    def test_attachment_claims_need_reference_or_reason(self):
        for invalid in ({"status": "provided"}, {"status": "not_applicable"},
                        {"status": "missing", "reference": "不应被当作已提供"}):
            raw = sample()["assets"][3]
            raw["subtitles"] = invalid
            with self.assertRaises(InputError):
                build({"assets": [raw]})

    def test_batch_and_type_specific_validation(self):
        with self.assertRaises(InputError):
            build({"assets": []})
        source = sample()
        source["assets"][1]["id"] = source["assets"][0]["id"]
        with self.assertRaisesRegex(InputError, "duplicate id"):
            build(source)
        raw = audio()["assets"][0]
        raw["alt"] = "音频不应有alt"
        with self.assertRaisesRegex(InputError, "unsupported fields: alt"):
            build({"assets": [raw]})
        raw.pop("alt")
        raw["brand"] = "不会自动加入品牌词"
        with self.assertRaisesRegex(InputError, "unsupported fields: brand"):
            build({"assets": [raw]})

    def test_url_field_does_not_accept_a_local_path_or_credentials(self):
        for invalid in ("./video.MOV", "file:///tmp/media.MOV", "https://name:secret@example.com/x",
                        "https://example.com:abc/video.MOV", "https://example.com:99999/video.MOV"):
            raw = sample()["assets"][3]
            raw["content_url"] = invalid
            with self.assertRaises(InputError):
                build({"assets": [raw]})
        raw["content_url"] = "https://example.com:8443/video.MOV"
        self.assertEqual(build({"assets": [raw]})["assets"][0]["content_url"], raw["content_url"])

    def test_handoff_preserves_alt_and_exposes_missing_video_fields(self):
        result = build(sample())
        text = handoff(result)
        self.assertIn(json.dumps(result["assets"][0]["alt"], ensure_ascii=False), text)
        self.assertIn("已确认时长", handoff(build({"assets": [{
            "id": "unknown", "type": "video", "original_filename": "未知.mp4",
            "evidence": {"kind": "unavailable", "scope": "none", "reference": "未提供视频"}}]})))
        self.assertIn("实际上传日期", text)
        self.assertIn("字幕文件或不适用说明", text)
        self.assertIn("带时间点的章节", text)

    def test_cli_success_and_invalid_input_does_not_replace_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            cli = [sys.executable, str(ROOT / "scripts/build_metadata.py")]
            run = subprocess.run(cli + ["--input", str(ROOT / "examples/success/input.json"),
                                        "--output-dir", temp], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            output = Path(temp) / "媒体元信息.json"
            expected = build(sample())
            self.assertEqual(read_document(output), expected)
            self.assertEqual((Path(temp) / "图注与字幕交接清单.md").read_text(encoding="utf-8"), handoff(expected))
            self.assertEqual(json.loads(run.stdout), expected["summary"])
            before = output.read_bytes()
            failure = subprocess.run(cli + ["--input", str(ROOT / "examples/failure/unseen-description.json"),
                                            "--output-dir", temp], capture_output=True, text=True)
            self.assertEqual(failure.returncode, 2)
            self.assertIn("unavailable evidence cannot support", failure.stderr)
            self.assertEqual(output.read_bytes(), before)

    def test_malformed_json_duplicate_keys_and_nan_fail_cleanly(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "invalid.json"
            for content in ('{"assets":', '{"assets": [], "assets": []}', '{"assets": NaN}'):
                with self.subTest(content=content):
                    source.write_text(content, encoding="utf-8")
                    run = subprocess.run([sys.executable, str(ROOT / "scripts/build_metadata.py"),
                                          "--input", str(source), "--output-dir", str(Path(temp) / "out")],
                                         capture_output=True, text=True)
                    self.assertEqual(run.returncode, 2)
                    self.assertIn("ERROR:", run.stderr)
                    self.assertNotIn("Traceback", run.stderr)
                    self.assertFalse((Path(temp) / "out").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
