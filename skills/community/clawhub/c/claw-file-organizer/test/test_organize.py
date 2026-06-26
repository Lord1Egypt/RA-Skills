#!/usr/bin/env python3
"""Tests for file-organizer."""

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import organize


class TestCategories(unittest.TestCase):
    def test_image_extensions(self):
        self.assertEqual(organize.get_category("photo.jpg"), "images")
        self.assertEqual(organize.get_category("icon.PNG"), "images")
        self.assertEqual(organize.get_category("diagram.svg"), "images")
        self.assertEqual(organize.get_category("animation.webp"), "images")

    def test_document_extensions(self):
        self.assertEqual(organize.get_category("report.pdf"), "documents")
        self.assertEqual(organize.get_category("notes.txt"), "documents")
        self.assertEqual(organize.get_category("presentation.pptx"), "documents")

    def test_audio_extensions(self):
        self.assertEqual(organize.get_category("song.mp3"), "audio")
        self.assertEqual(organize.get_category("track.flac"), "audio")

    def test_video_extensions(self):
        self.assertEqual(organize.get_category("clip.mp4"), "video")
        self.assertEqual(organize.get_category("movie.mkv"), "video")

    def test_archive_extensions(self):
        self.assertEqual(organize.get_category("backup.zip"), "archives")
        self.assertEqual(organize.get_category("source.tar.gz"), "archives")

    def test_code_extensions(self):
        self.assertEqual(organize.get_category("script.py"), "code")
        self.assertEqual(organize.get_category("page.html"), "code")

    def test_data_extensions(self):
        self.assertEqual(organize.get_category("data.csv"), "data")

    def test_other(self):
        self.assertEqual(organize.get_category("unknown.xyz"), "other")
        self.assertEqual(organize.get_category("no_extension"), "other")


class TestRename(unittest.TestCase):
    def test_sanitize_basic(self):
        result = organize.sanitize_name("My Document.pdf", None, "{name}_{date}")
        self.assertEqual(result, "My_Document.pdf")

    def test_sanitize_with_date(self):
        result = organize.sanitize_name("report 2025-03-15.pdf", "2025-03-15", "{name}_{date}")
        self.assertEqual(result, "report_2025-03-15.pdf")

    def test_sanitize_no_pattern(self):
        result = organize.sanitize_name("file with spaces.txt", None, "none")
        self.assertEqual(result, "file_with_spaces.txt")

    def test_sanitize_special_chars(self):
        result = organize.sanitize_name("file (v2).pdf", None, "none")
        self.assertEqual(result, "file_v2.pdf")

    def test_extract_date(self):
        self.assertEqual(organize.extract_date("report_2025-03-15.pdf"), ("2025", "03", "15"))
        self.assertEqual(organize.extract_date("doc_v1.0.txt"), None)

    def test_extract_date_dmy(self):
        result = organize.extract_date("report_15_03_2025.pdf")
        self.assertEqual(result, ("2025", "03", "15"))

    def test_extract_date_str(self):
        self.assertEqual(organize.extract_date_str("report_2025-03-15.pdf"), "2025-03-15")
        self.assertEqual(organize.extract_date_str("doc_v1.0.txt"), None)


class TestExclude(unittest.TestCase):
    def test_tmp_excluded(self):
        self.assertTrue(organize.should_exclude("test.tmp", ["*.tmp"]))

    def test_txt_not_excluded(self):
        self.assertFalse(organize.should_exclude("notes.txt", ["*.tmp"]))

    def test_ds_store_excluded(self):
        self.assertTrue(organize.should_exclude(".DS_Store", [".DS_Store"]))


class TestOrganizeDryRun(unittest.TestCase):
    def test_dry_run_no_moves(self):
        """Dry run should not move any files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            test_files = [
                "photo.jpg",
                "report.pdf",
                "song.mp3",
            ]
            for f in test_files:
                Path(tmpdir, f).touch()

            result = organize.organize_directory(tmpdir, tmpdir, organize.DEFAULT_CONFIG, dry_run=True)
            self.assertIsNotNone(result)
            self.assertEqual(len(result["moves"]), 0)
            self.assertEqual(result["counts"]["images"], 1)
            self.assertEqual(result["counts"]["documents"], 1)
            self.assertEqual(result["counts"]["audio"], 1)

            # Verify files still in original location
            for f in test_files:
                self.assertTrue(os.path.exists(os.path.join(tmpdir, f)))


class TestUndo(unittest.TestCase):
    def test_undo_restores_files(self):
        """Test that undo restores files to original location."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup
            source = os.path.join(tmpdir, "downloads")
            target = os.path.join(tmpdir, "organized")
            log_file = os.path.join(target, "ORGANIZE_LOG.json")
            os.makedirs(source)
            os.makedirs(target)

            # Create a test file
            test_file = os.path.join(source, "photo.jpg")
            Path(test_file).touch()

            # Organize (move)
            result = organize.organize_directory(source, target, organize.DEFAULT_CONFIG)
            self.assertEqual(len(result["moves"]), 1)
            new_path = result["moves"][0]["new"]
            self.assertTrue(os.path.exists(new_path))
            self.assertFalse(os.path.exists(test_file))

            # Save log for undo
            with open(log_file, "w") as f:
                json.dump([result], f)

            # Undo
            undo_result = organize.undo_operation(log_file)
            self.assertEqual(undo_result["restored"], 1)

            # Verify restored
            self.assertTrue(os.path.exists(test_file))


class TestIntegration(unittest.TestCase):
    def test_full_workflow(self):
        """End-to-end test: create files, organize, verify structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, "downloads")
            target = os.path.join(tmpdir, "organized")
            os.makedirs(source)

            # Create test files across categories
            test_files = [
                ("photo.jpg", "images"),
                ("report.pdf", "documents"),
                ("song.mp3", "audio"),
                ("video.mp4", "video"),
                ("archive.zip", "archives"),
                ("script.py", "code"),
                ("data.csv", "data"),
            ]
            for fname, _ in test_files:
                Path(source, fname).touch()

            config = organize.DEFAULT_CONFIG.copy()
            config["rename_pattern"] = "none"

            result = organize.organize_directory(source, target, config, dry_run=False)
            self.assertEqual(result["counts"], {cat: 1 for _, cat in test_files})
            self.assertEqual(len(result["moves"]), len(test_files))

            # Verify folder structure
            for _, expected_cat in test_files:
                cat_dir = os.path.join(target, expected_cat)
                self.assertTrue(os.path.isdir(cat_dir))


if __name__ == "__main__":
    unittest.main(verbosity=2)
