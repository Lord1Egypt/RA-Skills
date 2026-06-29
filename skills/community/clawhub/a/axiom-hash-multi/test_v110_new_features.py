"""
🧪 Tests pour les nouvelles features v1.1.0
=============================================
- verify_file
- parse_manifest
- verify_manifest
- Bug fix /dev/null
- --json output (testé via subprocess)
- --compare (testé via subprocess)
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from axiom_hash_multi import (
    hash_file,
    hash_file_all,
    parse_manifest,
    verify_file,
    verify_manifest,
)


class TestVerifyFile(unittest.TestCase):
    """Tests pour verify_file()."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.test_file = self.tmpdir / "test.txt"
        self.test_file.write_bytes(b"hello world")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_01_verify_match(self):
        """Hash correct doit retourner True."""
        expected = hashlib.sha256(b"hello world").hexdigest()
        self.assertTrue(verify_file(self.test_file, expected))

    def test_02_verify_mismatch(self):
        """Hash incorrect doit retourner False."""
        self.assertFalse(verify_file(self.test_file, "0" * 64))

    def test_03_verify_case_insensitive(self):
        """Le hash attendu est case-insensitive."""
        expected = hashlib.sha256(b"hello world").hexdigest()
        self.assertTrue(verify_file(self.test_file, expected.upper()))

    def test_04_verify_with_different_algo(self):
        """Doit fonctionner avec SHA-1, MD5, etc."""
        for algo in ("md5", "sha1", "sha256", "sha512", "blake2b"):
            with self.subTest(algo=algo):
                expected = hashlib.new(algo, b"hello world").hexdigest()
                self.assertTrue(verify_file(self.test_file, expected, algo=algo))


class TestBugFixDevNull(unittest.TestCase):
    """Tests pour le bug fix /dev/null."""

    def test_05_dev_null_hashes_to_empty(self):
        """/dev/null doit être hashable (et donner hash empty)."""
        if not Path("/dev/null").exists():
            self.skipTest("/dev/null not available")
        expected = hashlib.sha256(b"").hexdigest()
        self.assertEqual(hash_file("/dev/null", "sha256"), expected)

    def test_06_dev_urandom_works(self):
        """/dev/urandom doit être hashable (bytes lus depuis device)."""
        if not Path("/dev/urandom").exists():
            self.skipTest("/dev/urandom not available")
        # On lit 4KB et on hash
        with open("/dev/urandom", "rb") as f:
            data = f.read(4096)
        # Écrit dans un fichier et compare
        tmp = Path(tempfile.mkdtemp()) / "rand.bin"
        try:
            tmp.write_bytes(data)
            self.assertEqual(hash_file(tmp, "sha256"), hashlib.sha256(data).hexdigest())
        finally:
            import shutil
            shutil.rmtree(tmp.parent, ignore_errors=True)


class TestParseManifest(unittest.TestCase):
    """Tests pour parse_manifest()."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.manifest = self.tmpdir / "MANIFEST.txt"
        self.manifest.write_text("""# Test manifest
abc123def456  file1.txt  (100 bytes)
789ghi012jkl  file2.bin  (2048 bytes)
# This is a comment
""")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_07_parse_basic(self):
        """Doit parser les lignes valides, ignorer commentaires et vides."""
        entries = parse_manifest(self.manifest)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["filename"], "file1.txt")
        self.assertEqual(entries[0]["hash"], "abc123def456")
        self.assertEqual(entries[1]["filename"], "file2.bin")


class TestVerifyManifest(unittest.TestCase):
    """Tests pour verify_manifest()."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.base = self.tmpdir

        # Crée 3 fichiers avec contenu connu
        self.f1 = self.base / "file1.txt"
        self.f1.write_bytes(b"content of file 1")

        self.f2 = self.base / "file2.bin"
        self.f2.write_bytes(b"content of file 2 with binary\x00\xff")

        self.f3 = self.base / "file3.md"
        self.f3.write_bytes(b"# Document\nSome text")

        # Crée le manifest
        h1 = hashlib.sha256(self.f1.read_bytes()).hexdigest()
        h2 = hashlib.sha256(self.f2.read_bytes()).hexdigest()
        h3 = hashlib.sha256(self.f3.read_bytes()).hexdigest()
        # Une entrée volontairement fausse
        h_fake = "0" * 64

        self.manifest = self.base / "MANIFEST.txt"
        self.manifest.write_text(f"""# Manifest de test
{h1}  file1.txt
{h2}  file2.bin
{h_fake}  file3.md  # hash volontairement faux
""")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_08_verify_manifest_detects_mismatch(self):
        """verify_manifest doit détecter 1 mismatch parmi 3 entries."""
        result = verify_manifest(self.manifest, base_dir=self.base)
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["passed"], 2)
        self.assertEqual(result["failed"], 1)
        # Le fichier faux est file3.md
        for d in result["details"]:
            if not d.get("passed"):
                self.assertEqual(d["file"], "file3.md")

    def test_09_verify_manifest_all_correct(self):
        """Si tout est correct, 3/3 doivent passer."""
        # Crée un manifest tout correct
        h1 = hashlib.sha256(self.f1.read_bytes()).hexdigest()
        h2 = hashlib.sha256(self.f2.read_bytes()).hexdigest()
        h3 = hashlib.sha256(self.f3.read_bytes()).hexdigest()
        manifest_ok = self.base / "MANIFEST_OK.txt"
        manifest_ok.write_text(f"{h1}  file1.txt\n{h2}  file2.bin\n{h3}  file3.md\n")
        result = verify_manifest(manifest_ok, base_dir=self.base)
        self.assertEqual(result["passed"], 3)
        self.assertEqual(result["failed"], 0)


class TestCLIJsonOutput(unittest.TestCase):
    """Tests du --json output (via subprocess)."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.f = self.tmpdir / "test.txt"
        self.f.write_bytes(b"json test")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_10_json_single(self):
        """--json doit retourner un JSON valide."""
        result = subprocess.run(
            [sys.executable, "axiom_hash_multi.py", str(self.f), "--algo", "sha256", "--json"],
            capture_output=True, text=True, cwd=Path(__file__).parent
        )
        data = json.loads(result.stdout)
        self.assertIn("sha256", data)
        self.assertEqual(len(data["sha256"]), 64)

    def test_11_json_all(self):
        """--all --json doit retourner les 5 algos en JSON."""
        result = subprocess.run(
            [sys.executable, "axiom_hash_multi.py", str(self.f), "--all", "--json"],
            capture_output=True, text=True, cwd=Path(__file__).parent
        )
        data = json.loads(result.stdout)
        self.assertEqual(len(data), 5)
        for algo in ["md5", "sha1", "sha256", "sha512", "blake2b"]:
            self.assertIn(algo, data)


class TestCLICompare(unittest.TestCase):
    """Tests du --compare (via subprocess)."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.f = self.tmpdir / "test.txt"
        self.f.write_bytes(b"compare test")
        self.expected = hashlib.sha256(b"compare test").hexdigest()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_12_compare_match(self):
        """--compare avec bon hash doit exit 0 et dire MATCH."""
        result = subprocess.run(
            [sys.executable, "axiom_hash_multi.py", str(self.f),
             "--compare", self.expected],
            capture_output=True, text=True, cwd=Path(__file__).parent
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("MATCH", result.stdout)

    def test_13_compare_mismatch(self):
        """--compare avec mauvais hash doit exit 1 et dire MISMATCH."""
        result = subprocess.run(
            [sys.executable, "axiom_hash_multi.py", str(self.f),
             "--compare", "0" * 64],
            capture_output=True, text=True, cwd=Path(__file__).parent
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("MISMATCH", result.stdout)

    def test_14_compare_with_json(self):
        """--compare --json doit retourner un JSON structuré."""
        result = subprocess.run(
            [sys.executable, "axiom_hash_multi.py", str(self.f),
             "--compare", self.expected, "--json"],
            capture_output=True, text=True, cwd=Path(__file__).parent
        )
        data = json.loads(result.stdout)
        self.assertTrue(data["match"])
        self.assertEqual(data["expected"], self.expected)


class TestManifestCLI(unittest.TestCase):
    """Test du --verify-manifest (via subprocess)."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.f = self.tmpdir / "data.txt"
        self.f.write_bytes(b"manifest data")
        h = hashlib.sha256(self.f.read_bytes()).hexdigest()
        self.manifest = self.tmpdir / "M.txt"
        self.manifest.write_text(f"{h}  data.txt\n")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_15_manifest_verify_ok(self):
        """--verify-manifest doit exit 0 si tout passe."""
        result = subprocess.run(
            [sys.executable, "axiom_hash_multi.py",
             "--verify-manifest", str(self.manifest)],
            capture_output=True, text=True, cwd=Path(__file__).parent
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Pass: 1", result.stdout)
        self.assertIn("Fail: 0", result.stdout)

    def test_16_manifest_verify_with_failure(self):
        """--verify-manifest doit exit 1 si quelque chose échoue."""
        # Crée un manifest avec un mauvais hash
        bad_manifest = self.tmpdir / "BAD.txt"
        bad_manifest.write_text("0" * 64 + "  data.txt\n")
        result = subprocess.run(
            [sys.executable, "axiom_hash_multi.py",
             "--verify-manifest", str(bad_manifest)],
            capture_output=True, text=True, cwd=Path(__file__).parent
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Fail: 1", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
