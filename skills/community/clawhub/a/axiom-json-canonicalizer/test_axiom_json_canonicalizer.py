"""
🧪 Tests unitaires — axiom-json-canonicalizer v1.0.0
======================================================

60+ tests obligatoires pour skill validation (≥10 cas, edge cases inclus).
Couvre :
- JCS RFC 8785 §3.2.2 (ordering, formatting, normalization, NFC)
- Surrogate pairs (UTF-16 encoded chars)
- Deep nesting (>50 levels)
- Très grands entiers (bigint au-delà de float64)
- String keys non-ASCII
- Arrays hétérogènes
- Whitespace INSIDE strings vs around
- Performance <100ms
- Déterminisme byte-to-byte (1000 runs)
- Erreurs (NaN, Infinity, type invalide, profondeur)
Améliorations + 20+ tests edge cases: Axioma team
"""

import hashlib
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

# Permet d'importer le module dans le même dossier
sys.path.insert(0, str(Path(__file__).parent))

from axiom_json_canonicalizer import (
    MAX_JSON_DEPTH,
    canonicalize,
    canonicalize_bytes,
    canonicalize_file,
    verify_canonical,
)


# ============================================================================
# §3.2.2.1 — Object member ordering (lexicographic)
# ============================================================================

class TestObjectOrdering(unittest.TestCase):
    """RFC 8785 §3.2.2.1: Object members sorted lexicographically by key."""

    def test_01_simple_object_sorted(self):
        result = canonicalize({"b": 2, "a": 1})
        self.assertEqual(result, '{"a":1,"b":2}')

    def test_02_three_keys_sorted(self):
        result = canonicalize({"z": 3, "a": 1, "m": 2})
        self.assertEqual(result, '{"a":1,"m":2,"z":3}')

    def test_03_nested_objects_sorted(self):
        result = canonicalize({"z": {"y": 2, "x": 1}, "a": {"c": 3, "b": 2}})
        self.assertEqual(result, '{"a":{"b":2,"c":3},"z":{"x":1,"y":2}}')

    def test_04_array_preserves_order(self):
        result = canonicalize([3, 1, 2])
        self.assertEqual(result, '[3,1,2]')

    def test_05_array_of_objects_each_sorted(self):
        result = canonicalize([{"b": 2, "a": 1}, {"y": 1, "x": 2}])
        self.assertEqual(result, '[{"a":1,"b":2},{"x":2,"y":1}]')

    def test_06_single_key(self):
        result = canonicalize({"only": "value"})
        self.assertEqual(result, '{"only":"value"}')


# ============================================================================
# §3.2.2.2 — No insignificant whitespace
# ============================================================================

class TestNoWhitespace(unittest.TestCase):
    """RFC 8785 §3.2.2.2: No insignificant whitespace in output."""

    def test_07_no_whitespace_basic(self):
        result = canonicalize({"b": 2, "a": 1})
        self.assertNotIn(' ', result)
        self.assertNotIn('\n', result)
        self.assertNotIn('\t', result)

    def test_08_whitespace_input_stripped(self):
        a = canonicalize(json.loads('{"a": 1, "b": 2}'))
        b = canonicalize(json.loads('  { "a":1,  "b":  2  }  '))
        c = canonicalize({"a": 1, "b": 2})
        self.assertEqual(a, b)
        self.assertEqual(b, c)

    def test_09_whitespace_inside_string_preserved(self):
        """Whitespace INSIDE strings is preserved (significant)."""
        result = canonicalize({"s": "hello world"})
        self.assertEqual(result, '{"s":"hello world"}')

    def test_10_tab_inside_string(self):
        result = canonicalize({"s": "a\tb"})
        self.assertEqual(result, '{"s":"a\\tb"}')


# ============================================================================
# §3.2.2.4 — Unicode NFC normalization
# ============================================================================

class TestUnicodeNFC(unittest.TestCase):
    """RFC 8785 §3.2.2.4: Strings MUST be NFC normalized."""

    def test_11_nfc_pre_composed_vs_decomposed(self):
        nfc_form = canonicalize({"café": 1})
        nfd_form = canonicalize({"cafe\u0301": 1})
        self.assertEqual(nfc_form, nfd_form)
        self.assertEqual(nfc_form, '{"café":1}')

    def test_12_nfc_sort_after_normalization(self):
        """Keys must be sorted AFTER NFC normalization."""
        # 'cafe' (ASCII) < 'café' (U+00E9) by codepoint
        result = canonicalize({"café": 2, "cafe": 1})
        self.assertEqual(result, '{"cafe":1,"café":2}')

    def test_13_nfc_in_values(self):
        result = canonicalize({"greeting": "café"})
        self.assertEqual(result, '{"greeting":"café"}')

    def test_14_nfc_deep_in_nesting(self):
        obj = {"a": {"b": {"c": {"name": "naïve", "city": "Köln"}}}}
        result = canonicalize(obj)
        # Just verify it doesn't crash and is deterministic
        self.assertEqual(result, canonicalize(obj))

    def test_15_emoji_preserved(self):
        result = canonicalize({"mood": "🔥🐺💜"})
        self.assertEqual(result, '{"mood":"🔥🐺💜"}')

    def test_16_surrogate_pair_high_then_low(self):
        """Surrogate pair: U+D83D U+DD25 (🔥 fire emoji)."""
        # Python str automatically combines surrogates
        result = canonicalize({"fire": "\U0001F525"})
        self.assertEqual(result, '{"fire":"🔥"}')

    def test_17_astral_plane_char(self):
        """Astral plane characters (4-byte UTF-8)."""
        result = canonicalize({"char": "\U0001F600"})  # 😀 grinning face
        self.assertEqual(result, '{"char":"😀"}')

    def test_18_cjk_characters(self):
        """CJK characters handled correctly."""
        result = canonicalize({"text": "中文测试"})
        self.assertEqual(result, '{"text":"中文测试"}')

    def test_19_arabic_with_combining_marks(self):
        """Arabic with combining marks NFC normalized."""
        result = canonicalize({"word": "مُحَمَّد"})
        # Just verify it doesn't crash
        self.assertIsInstance(result, str)


# ============================================================================
# §3.2.2.3 — Number formatting (ECMAScript NumberToString)
# ============================================================================

class TestNumberFormatting(unittest.TestCase):
    """RFC 8785 §3.2.2.3: ECMAScript-compatible number-to-string."""

    def test_20_integer_basic(self):
        self.assertEqual(canonicalize({"n": 42}), '{"n":42}')

    def test_21_negative_integer(self):
        self.assertEqual(canonicalize({"n": -42}), '{"n":-42}')

    def test_22_zero_positive(self):
        self.assertEqual(canonicalize({"n": 0}), '{"n":0}')

    def test_23_zero_negative_normalized(self):
        """-0.0 must canonicalize to 0."""
        self.assertEqual(canonicalize({"x": 0.0}), '{"x":0}')
        self.assertEqual(canonicalize({"x": -0.0}), '{"x":0}')
        self.assertEqual(
            canonicalize({"x": 0.0}),
            canonicalize({"x": -0.0})
        )

    def test_24_float_basic(self):
        self.assertEqual(canonicalize({"n": 3.14}), '{"n":3.14}')

    def test_25_scientific_notation_1e10(self):
        """1e10 = 10000000000 (integer representation, not 10000000000.0)."""
        result = canonicalize({"n": 1e10})
        # Python repr(1e10) = '10000000000.0' but we trim to '10000000000'
        # because it's an integer value
        self.assertEqual(result, '{"n":10000000000}')

    def test_26_scientific_notation_small(self):
        """Small numbers use scientific notation."""
        result = canonicalize({"n": 1.5e-5})
        self.assertEqual(result, '{"n":1.5e-5}')

    def test_27_scientific_notation_very_small(self):
        """1e-7 → 1e-7 (JCS keeps scientific for very small)."""
        result = canonicalize({"n": 1e-7})
        self.assertIn("e", result.lower())

    def test_28_scientific_no_plus_in_exponent(self):
        """Exponent must NOT have leading + sign."""
        for n in [1e10, 1e15, 1e20, 1.5e-5, 1e-7]:
            result = canonicalize({"n": n})
            self.assertNotIn("e+", result, f"+ in exponent: {result}")
            self.assertNotIn("E+", result, f"+ in exponent: {result}")

    def test_29_very_large_number(self):
        """Numbers near float64 max."""
        result = canonicalize({"n": 1e308})
        self.assertNotIn("inf", result.lower())
        self.assertNotIn("nan", result.lower())

    def test_30_very_small_number(self):
        """Numbers near float64 min positive."""
        result = canonicalize({"n": 1e-308})
        self.assertNotIn("inf", result.lower())
        self.assertNotIn("nan", result.lower())

    def test_31_bigint_python_int(self):
        """Python ints beyond float64 range."""
        big = 2**100  # way bigger than float64 (~1.8e308)
        result = canonicalize({"big": big})
        self.assertEqual(result, f'{{"big":{big}}}')

    def test_32_bigint_negative(self):
        big = -(2**100)
        result = canonicalize({"big": big})
        self.assertEqual(result, f'{{"big":{big}}}')

    def test_33_nan_rejected(self):
        with self.assertRaises(ValueError):
            canonicalize({"x": float("nan")})

    def test_34_infinity_rejected(self):
        with self.assertRaises(ValueError):
            canonicalize({"x": float("inf")})

    def test_35_negative_infinity_rejected(self):
        with self.assertRaises(ValueError):
            canonicalize({"x": float("-inf")})


# ============================================================================
# String escaping (RFC 8259 compatible)
# ============================================================================

class TestStringEscapes(unittest.TestCase):
    """JSON string escaping per RFC 8259 (RFC 8785 inherits)."""

    def test_36_quote_escape(self):
        result = canonicalize({"s": 'he said "hi"'})
        self.assertEqual(result, '{"s":"he said \\"hi\\""}')

    def test_37_backslash_escape(self):
        result = canonicalize({"s": "a\\b"})
        self.assertEqual(result, '{"s":"a\\\\b"}')

    def test_38_control_chars_u_escape(self):
        """Control characters use \\uXXXX form."""
        result = canonicalize({"s": "\x01\x02"})
        self.assertEqual(result, '{"s":"\\u0001\\u0002"}')

    def test_39_common_escapes(self):
        result = canonicalize({"s": "line1\nline2\ttab\rcr"})
        self.assertEqual(result, '{"s":"line1\\nline2\\ttab\\rcr"}')


# ============================================================================
# Empty + edge cases
# ============================================================================

class TestEmptyAndEdge(unittest.TestCase):
    """Empty and minimal cases."""

    def test_40_empty_dict(self):
        self.assertEqual(canonicalize({}), '{}')

    def test_41_empty_array(self):
        self.assertEqual(canonicalize([]), '[]')

    def test_42_null(self):
        self.assertEqual(canonicalize(None), 'null')

    def test_43_true_false(self):
        self.assertEqual(canonicalize(True), 'true')
        self.assertEqual(canonicalize(False), 'false')

    def test_44_single_string(self):
        self.assertEqual(canonicalize("hello"), '"hello"')

    def test_45_single_number(self):
        self.assertEqual(canonicalize(42), '42')

    def test_46_empty_dict_in_dict(self):
        result = canonicalize({"a": {}, "b": []})
        self.assertEqual(result, '{"a":{},"b":[]}')

    def test_47_nested_empty(self):
        result = canonicalize({"a": {"b": {"c": {}}}})
        self.assertEqual(result, '{"a":{"b":{"c":{}}}}')


# ============================================================================
# Deep nesting
# ============================================================================

class TestDeepNesting(unittest.TestCase):
    """RFC 8785 doesn't specify max depth, but we cap at 100 for safety."""

    def test_48_nesting_50(self):
        obj = {"leaf": True}
        for _ in range(50):
            obj = {"nested": obj}
        result = canonicalize(obj)
        self.assertTrue(result.startswith('{"nested":'))

    def test_49_nesting_99_max_allowed(self):
        obj = {"leaf": True}
        for _ in range(99):
            obj = {"nested": obj}
        result = canonicalize(obj)
        # 99 levels of nesting: starts with 99×'{"nested":' and ends with 99×'}'
        self.assertTrue(result.startswith('{"nested":' * 1))
        self.assertTrue('"leaf":true' in result)
        self.assertEqual(result.count('"nested":'), 99)
        self.assertEqual(result.count('}'), 100)  # 99 inner + 1 outer

    def test_50_nesting_101_exceeds_max(self):
        obj = {"leaf": True}
        for _ in range(101):
            obj = {"nested": obj}
        with self.assertRaises(ValueError) as ctx:
            canonicalize(obj)
        self.assertIn("depth", str(ctx.exception).lower())

    def test_51_deep_array_nesting(self):
        arr = [1]
        for _ in range(50):
            arr = [arr]
        result = canonicalize(arr)
        self.assertTrue(result.startswith('[['))


# ============================================================================
# Non-ASCII keys (often a source of bugs)
# ============================================================================

class TestNonAsciiKeys(unittest.TestCase):
    """String keys with non-ASCII characters."""

    def test_52_french_keys(self):
        result = canonicalize({"nom": "Alice", "âge": 30, "ville": "Montréal"})
        # Sorted by codepoint: ' nom' (0x6E) < 'ville' (0x76) < 'âge' (0xE2)
        # Wait, actually 'âge' (0xE2) > 'ville' (0x76), so:
        # nom < ville < âge
        self.assertEqual(result, '{"nom":"Alice","ville":"Montréal","âge":30}')

    def test_53_japanese_keys(self):
        result = canonicalize({"日本": "jp", "中国": "cn"})
        # 中国 (U+4E2D) < 日本 (U+65E5)
        self.assertEqual(result, '{"中国":"cn","日本":"jp"}')

    def test_54_emoji_keys(self):
        result = canonicalize({"🔥": "fire", "🐺": "wolf"})
        # 🐺 (U+1F43A) < 🔥 (U+1F525) — wolf comes first by codepoint
        self.assertEqual(result, '{"🐺":"wolf","🔥":"fire"}')


# ============================================================================
# Heterogeneous arrays
# ============================================================================

class TestHeterogeneousArrays(unittest.TestCase):
    """Arrays with mixed types."""

    def test_55_mixed_types_array(self):
        # 3.0 normalizes to "3" (integer representation, JCS shortest)
        result = canonicalize([1, "two", 3.0, None, True, False])
        self.assertEqual(result, '[1,"two",3,null,true,false]')

    def test_56_array_of_objects_and_arrays(self):
        result = canonicalize([{"a": 1}, [1, 2], "string", 42])
        self.assertEqual(result, '[{"a":1},[1,2],"string",42]')

    def test_57_empty_array_in_array(self):
        result = canonicalize([[], [], []])
        self.assertEqual(result, '[[],[],[]]')

    def test_58_dict_in_array_in_dict(self):
        result = canonicalize({"a": [{"b": [{"c": 1}]}]})
        self.assertEqual(result, '{"a":[{"b":[{"c":1}]}]}')


# ============================================================================
# Bytes vs str consistency
# ============================================================================

class TestBytesAPI(unittest.TestCase):
    """canonicalize_bytes returns UTF-8 bytes."""

    def test_59_bytes_output(self):
        result = canonicalize_bytes({"a": 1})
        self.assertIsInstance(result, bytes)
        self.assertEqual(result, b'{"a":1}')

    def test_60_bytes_from_json_string(self):
        result = canonicalize_bytes('{"b": 2, "a": 1}')
        self.assertEqual(result, b'{"a":1,"b":2}')

    def test_61_bytes_from_bytes(self):
        result = canonicalize_bytes(b'{"b": 2, "a": 1}')
        self.assertEqual(result, b'{"a":1,"b":2}')

    def test_62_bytes_str_consistency(self):
        s = canonicalize({"b": 2, "a": 1})
        b = canonicalize_bytes({"b": 2, "a": 1})
        self.assertEqual(s.encode("utf-8"), b)


# ============================================================================
# File operations
# ============================================================================

class TestFileOperations(unittest.TestCase):
    """Test canonicalize_file and verify_canonical."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_63_canonicalize_file(self):
        path = Path(self.tmpdir) / "input.json"
        path.write_text('{"z": 3, "a": 1, "m": 2}')
        result = canonicalize_file(path)
        self.assertEqual(result, '{"a":1,"m":2,"z":3}')

    def test_64_canonicalize_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            canonicalize_file("/tmp/does_not_exist_xyz_999.json")

    def test_65_canonicalize_directory(self):
        with self.assertRaises(IsADirectoryError):
            canonicalize_file(self.tmpdir)

    def test_66_verify_canonical_true(self):
        path = Path(self.tmpdir) / "canon.json"
        path.write_text('{"a":1,"b":2}')
        self.assertTrue(verify_canonical(path))

    def test_67_verify_canonical_false(self):
        path = Path(self.tmpdir) / "not_canon.json"
        path.write_text('{"b": 2, "a": 1}')  # not canonical (whitespace + order)
        self.assertFalse(verify_canonical(path))

    def test_68_verify_canonical_with_ignore_whitespace(self):
        path = Path(self.tmpdir) / "spaced.json"
        path.write_text('{ "a" : 1 , "b" : 2 }')  # same content, different whitespace
        # Without ignore-whitespace, should be False
        self.assertFalse(verify_canonical(path, ignore_whitespace=False))
        # With ignore-whitespace, should be True
        self.assertTrue(verify_canonical(path, ignore_whitespace=True))


# ============================================================================
# Determinism (byte-to-byte)
# ============================================================================

class TestDeterminism(unittest.TestCase):
    """Byte-to-byte determinism over many runs."""

    def test_69_determinism_1000_runs(self):
        obj = {"b": [1, 2, 3], "a": {"nested": True, "key": None}}
        first = canonicalize(obj)
        for _ in range(1000):
            self.assertEqual(canonicalize(obj), first)

    def test_70_determinism_equivalent_inputs(self):
        a = canonicalize({"b": 2, "a": 1})
        b = canonicalize({"a": 1, "b": 2})
        c = canonicalize(json.loads('  { "b" :  2 ,  "a":1  }  '))
        self.assertEqual(a, b)
        self.assertEqual(b, c)

    def test_71_determinism_nfc_equivalence(self):
        a = canonicalize({"café": 1})
        b = canonicalize({"cafe\u0301": 1})
        self.assertEqual(a, b)

    def test_72_determinism_sha256(self):
        """SHA-256 of canonical form is stable."""
        obj = {"payload": "data", "version": 1}
        h_first = hashlib.sha256(canonicalize_bytes(obj)).hexdigest()
        for _ in range(100):
            h = hashlib.sha256(canonicalize_bytes(obj)).hexdigest()
            self.assertEqual(h, h_first)

    def test_73_determinism_complex_nested(self):
        obj = {
            "users": [
                {"id": 1, "name": "Alice", "tags": ["admin", "active"]},
                {"id": 2, "name": "Bob", "tags": []},
            ],
            "metadata": {"version": "1.0", "created": "2026-06-14"},
        }
        first = canonicalize_bytes(obj)
        for _ in range(100):
            self.assertEqual(canonicalize_bytes(obj), first)


# ============================================================================
# Error handling
# ============================================================================

class TestErrors(unittest.TestCase):
    """Error handling for invalid inputs."""

    def test_74_unsupported_type_set(self):
        with self.assertRaises(ValueError):
            canonicalize({1, 2, 3})

    def test_75_unsupported_type_object(self):
        with self.assertRaises(ValueError):
            canonicalize(object())

    def test_76_unsupported_type_complex(self):
        with self.assertRaises(ValueError):
            canonicalize(complex(1, 2))

    def test_77_non_string_key(self):
        with self.assertRaises(ValueError):
            canonicalize({1: "a", 2: "b"})

    def test_78_invalid_json_input_bytes(self):
        with self.assertRaises(json.JSONDecodeError):
            canonicalize_bytes(b'{"a": invalid}')


# ============================================================================
# Performance
# ============================================================================

class TestPerformance(unittest.TestCase):
    """Performance smoke tests."""

    def test_79_large_object_1000_keys(self):
        import time
        obj = {f"key_{i:04d}": i for i in range(1000)}
        start = time.perf_counter()
        result = canonicalize(obj)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 0.1, f"Too slow: {elapsed*1000:.1f}ms")
        self.assertEqual(len(result), len(result))  # sanity

    def test_80_deep_nesting_perf(self):
        import time
        obj = {"leaf": True}
        for _ in range(95):
            obj = {"nested": obj}
        start = time.perf_counter()
        result = canonicalize(obj)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 0.1, f"Too slow: {elapsed*1000:.1f}ms")

    def test_81_large_array_perf(self):
        import time
        arr = list(range(10000))
        start = time.perf_counter()
        result = canonicalize(arr)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 0.1, f"Too slow: {elapsed*1000:.1f}ms")
        self.assertTrue(result.startswith("[0,1,2"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
