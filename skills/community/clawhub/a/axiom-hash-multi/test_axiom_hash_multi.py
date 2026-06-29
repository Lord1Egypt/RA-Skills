"""
🧪 Tests unitaires — axiom-hash-multi
=====================================

Tests obligatoires pour skill validation (≥10 cas, edge cases inclus).
Couvre :
- Hachage de base (vecteurs de test RFC)
- Edge cases (vide, unicode, binaire, gros)
- Multi-algorithmes
- Fichiers
- Erreurs
"""

import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Permet d'importer le module dans le même dossier
sys.path.insert(0, str(Path(__file__).parent))

from axiom_hash_multi import (
    SUPPORTED_ALGORITHMS,
    hash_all,
    hash_bytes,
    hash_file,
    hash_file_all,
)


class TestHashBytes(unittest.TestCase):
    """Tests pour hash_bytes()."""

    def test_01_sha256_empty(self):
        """Hash de la chaîne vide (vecteur de test RFC)."""
        # SHA-256("") = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        self.assertEqual(
            hash_bytes(b"", "sha256"),
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        )

    def test_02_sha256_hello(self):
        """Hash de 'hello' (vecteur de test RFC)."""
        # SHA-256("hello") = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
        self.assertEqual(
            hash_bytes(b"hello", "sha256"),
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        )

    def test_03_sha1_abc(self):
        """Hash de 'abc' en SHA-1 (vecteur de test RFC 3174)."""
        # SHA-1("abc") = a9993e364706816aba3e25717850c26c9cd0d89d
        self.assertEqual(
            hash_bytes(b"abc", "sha1"),
            "a9993e364706816aba3e25717850c26c9cd0d89d"
        )

    def test_04_md5_hello_world(self):
        """Hash de 'hello world' en MD5 (vecteur de test)."""
        # MD5("hello world") = 5eb63bbbe01eeed093cb22bb8f5acdc3
        self.assertEqual(
            hash_bytes(b"hello world", "md5"),
            "5eb63bbbe01eeed093cb22bb8f5acdc3"
        )

    def test_05_sha512_empty(self):
        """Hash SHA-512 de la chaîne vide."""
        expected = (
            "cf83e1357eefb8bdf1542850d66d8007"
            "d620e4050b5715dc83f4a921d36ce9ce"
            "47d0d13c5d85f2b0ff8318d2877eec2f"
            "63b931bd47417a81a538327af927da3e"
        )
        self.assertEqual(hash_bytes(b"", "sha512"), expected)

    def test_06_blake2b_hello(self):
        """Hash BLAKE2b de 'hello'."""
        expected = hashlib.blake2b(b"hello", digest_size=64).hexdigest()
        self.assertEqual(hash_bytes(b"hello", "blake2b"), expected)

    def test_07_unicode_emoji(self):
        """Hash avec caractères Unicode (emoji 🐺)."""
        data = "Axioma team —  💜".encode("utf-8")
        digest = hash_bytes(data, "sha256")
        # Doit être un hash valide de 64 hex chars
        self.assertEqual(len(digest), 64)
        # Et doit être déterministe
        self.assertEqual(digest, hash_bytes(data, "sha256"))

    def test_08_binary_with_null_bytes(self):
        """Hash de bytes avec null bytes (edge case)."""
        data = b"\x00\x01\x02\x00\xff\xfe"
        digest = hash_bytes(data, "sha256")
        self.assertEqual(len(digest), 64)
        # Doit être déterministe
        self.assertEqual(digest, hash_bytes(data, "sha256"))

    def test_09_large_data(self):
        """Hash de gros volume (1 MB) — perf test."""
        data = b"a" * (1024 * 1024)  # 1 MB
        import time
        start = time.perf_counter()
        digest = hash_bytes(data, "sha256")
        elapsed = time.perf_counter() - start
        # Doit finir en <100ms pour 1 MB
        self.assertLess(elapsed, 0.1, f"Trop lent : {elapsed*1000:.1f}ms")
        self.assertEqual(len(digest), 64)


class TestHashAll(unittest.TestCase):
    """Tests pour hash_all()."""

    def test_10_all_algorithms_returned(self):
        """hash_all doit retourner les 5 algorithmes."""
        results = hash_all(b"test")
        self.assertEqual(set(results.keys()), set(SUPPORTED_ALGORITHMS))

    def test_11_all_algorithms_match_individual(self):
        """hash_all(x)[algo] doit matcher hash_bytes(x, algo)."""
        data = b"deterministic test data"
        results = hash_all(data)
        for algo in SUPPORTED_ALGORITHMS:
            self.assertEqual(
                results[algo],
                hash_bytes(data, algo),
                f"Mismatch pour {algo}"
            )

    def test_12_all_algorithms_correct_format(self):
        """Chaque hash doit avoir la bonne longueur hex."""
        results = hash_all(b"x")
        expected_lengths = {
            "md5": 32,
            "sha1": 40,
            "sha256": 64,
            "sha512": 128,
            "blake2b": 128,  # 64 bytes * 2
        }
        for algo, expected_len in expected_lengths.items():
            self.assertEqual(
                len(results[algo]),
                expected_len,
                f"{algo} : longueur incorrecte"
            )


class TestHashFile(unittest.TestCase):
    """Tests pour hash_file() et hash_file_all()."""

    def setUp(self):
        """Crée un fichier temporaire pour les tests."""
        self.tmpdir = tempfile.mkdtemp()
        self.test_file = Path(self.tmpdir) / "test.txt"
        self.test_file.write_bytes(b"hello world\n")

    def test_13_hash_file_basic(self):
        """Hash d'un fichier basique."""
        digest = hash_file(self.test_file, "sha256")
        expected = hashlib.sha256(b"hello world\n").hexdigest()
        self.assertEqual(digest, expected)

    def test_14_hash_file_all(self):
        """hash_file_all doit retourner 5 algos en 1 passe."""
        results = hash_file_all(self.test_file)
        self.assertEqual(set(results.keys()), set(SUPPORTED_ALGORITHMS))
        # Compare avec hashlib direct
        for algo, h_func in [
            ("md5", hashlib.md5),
            ("sha1", hashlib.sha1),
            ("sha256", hashlib.sha256),
            ("sha512", hashlib.sha512),
        ]:
            expected = h_func(b"hello world\n").hexdigest()
            self.assertEqual(results[algo], expected, f"Mismatch {algo}")

    def test_15_hash_large_file_streaming(self):
        """Hash d'un gros fichier (10 MB) — vérifie le streaming."""
        big_file = Path(self.tmpdir) / "big.bin"
        big_file.write_bytes(b"x" * (10 * 1024 * 1024))  # 10 MB
        digest = hash_file(big_file, "sha256")
        expected = hashlib.sha256(b"x" * (10 * 1024 * 1024)).hexdigest()
        self.assertEqual(digest, expected)

    def test_16_hash_nonexistent_file(self):
        """Doit lever FileNotFoundError pour fichier inexistant."""
        with self.assertRaises(FileNotFoundError):
            hash_file("/tmp/does_not_exist_xyz_999.txt", "sha256")

    def test_17_hash_directory_error(self):
        """Doit lever IsADirectoryError si input est un dossier."""
        with self.assertRaises(IsADirectoryError):
            hash_file(self.tmpdir, "sha256")

    def test_18_hash_empty_file(self):
        """Hash d'un fichier vide (edge case)."""
        empty_file = Path(self.tmpdir) / "empty.txt"
        empty_file.touch()
        digest = hash_file(empty_file, "sha256")
        expected = hashlib.sha256(b"").hexdigest()
        self.assertEqual(digest, expected)


class TestErrors(unittest.TestCase):
    """Tests des erreurs."""

    def test_19_invalid_algo(self):
        """Doit lever ValueError pour algo non supporté."""
        with self.assertRaises(ValueError):
            hash_bytes(b"x", algo="invalid_algo")

    def test_20_invalid_algo_file(self):
        """Doit lever ValueError pour algo non supporté (fichier)."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"x")
            tmppath = f.name
        try:
            with self.assertRaises(ValueError):
                hash_file(tmppath, algo="sha999")
        finally:
            os.unlink(tmppath)

    def test_21_type_error_on_string(self):
        """Doit lever TypeError si input n'est pas bytes."""
        with self.assertRaises(TypeError):
            hash_bytes("not bytes", "sha256")  # type: ignore

    def test_22_type_error_on_int(self):
        """Doit lever TypeError pour int."""
        with self.assertRaises(TypeError):
            hash_bytes(42, "sha256")  # type: ignore


class TestDeterminism(unittest.TestCase):
    """Tests de déterminisme byte-to-byte."""

    def test_23_determinism_1000_runs(self):
        """1000 exécutions doivent donner exactement le même hash."""
        data = b"determinism test"
        first = hash_bytes(data, "sha256")
        for _ in range(1000):
            self.assertEqual(hash_bytes(data, "sha256"), first)

    def test_24_determinism_all_algos(self):
        """Déterminisme sur tous les algos."""
        data = b"multi algo test"
        for algo in SUPPORTED_ALGORITHMS:
            first = hash_bytes(data, algo)
            for _ in range(100):
                self.assertEqual(hash_bytes(data, algo), first)


if __name__ == "__main__":
    unittest.main(verbosity=2)
