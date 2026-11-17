import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, "skills/agy-ppt/scripts")
sys.path.insert(0, "skills/agy-ppt/tests")

from helpers.fake_ocr_provider import FakeOCRProvider
from manage_ocr_providers import main as cli_main
from ocr_providers import (
    OCRConfigurationStore, OCRError, OCRProviderCapabilities,
    OCRProviderConfiguration, OCRProviderManager,
)


class Provider(FakeOCRProvider):
    def __init__(self, provider_id="custom", provider_version="2.0.0", *, capabilities=None):
        super().__init__(provider_id=provider_id, provider_version=provider_version)
        self._capabilities = capabilities
        self.probes = 0

    @property
    def capabilities(self):
        return self._capabilities or OCRProviderCapabilities(
            True, True, "local", False, bounding_boxes=True, confidence=True
        )


class ManagementTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.project = root / "project"
        self.user = root / "user"
        self.project.mkdir()
        self.user.mkdir()
        self.default = Provider("tesseract", "phase15.1")
        self.custom = Provider("custom", "2.0.0")
        self.store = OCRConfigurationStore(self.project, self.user)
        self.manager = OCRProviderManager(
            {"tesseract": self.default, "custom": self.custom}, self.store
        )

    def tearDown(self):
        self.temp.cleanup()


class ConfigurationModelTests(ManagementTestCase):
    def test_serialization_is_canonical_and_stable(self):
        config = OCRProviderConfiguration("custom", True)
        self.assertEqual(config.to_json(), '{"allow_fallback":true,"provider":"custom"}\n')
        self.assertEqual(OCRProviderConfiguration.from_bytes(config.to_json().encode()), config)

    def test_rejects_duplicate_unknown_missing_and_invalid_fields(self):
        samples = (
            b'{"provider":"a","provider":"b","allow_fallback":false}',
            b'{"provider":"a","allow_fallback":false,"token":"secret"}',
            b'{"provider":"a"}', b'[]', b'not-json', b'\xff',
            b'{"provider":"a","allow_fallback":1}',
        )
        for raw in samples:
            with self.subTest(raw=raw):
                with self.assertRaises(OCRError) as caught:
                    OCRProviderConfiguration.from_bytes(raw)
                self.assertEqual(caught.exception.error_code, "OCR_PROVIDER_CONTRACT_INVALID")

    def test_provider_identifier_is_not_trimmed_or_aliased(self):
        for value in ("", " custom", "custom "):
            with self.assertRaises(OCRError):
                OCRProviderConfiguration(value)

    def test_oversized_config_is_rejected(self):
        path = self.project / ".agy" / "ocr-provider.json"
        path.parent.mkdir()
        path.write_bytes(b"x" * 16_385)
        with self.assertRaises(OCRError):
            self.store.read("project")


class ConfigurationStoreTests(ManagementTestCase):
    def test_project_and_user_locations_are_separate(self):
        self.store.write("project", OCRProviderConfiguration("custom", True))
        self.store.write("user", OCRProviderConfiguration("tesseract", False))
        self.assertEqual(self.store.read("project").provider, "custom")
        self.assertEqual(self.store.read("user").provider, "tesseract")
        self.assertTrue((self.project / ".agy" / "ocr-provider.json").exists())
        self.assertTrue((self.user / "agy-ppt" / "ocr-provider.json").exists())

    def test_write_is_private_and_leaves_no_temp_file(self):
        self.store.write("project", OCRProviderConfiguration("custom"))
        path = self.project / ".agy" / "ocr-provider.json"
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        self.assertFalse((path.parent / ".ocr-provider.json.tmp").exists())

    def test_failed_replace_preserves_previous_config(self):
        self.store.write("project", OCRProviderConfiguration("custom"))
        with patch("ocr_providers.management.os.replace", side_effect=OSError("injected")):
            with self.assertRaises(OCRError):
                self.store.write("project", OCRProviderConfiguration("tesseract"))
        self.assertEqual(self.store.read("project").provider, "custom")

    def test_unset_is_idempotent_and_reveals_absence(self):
        self.store.write("user", OCRProviderConfiguration("custom"))
        self.assertTrue(self.store.unset("user"))
        self.assertFalse(self.store.unset("user"))
        self.assertIsNone(self.store.read("user"))

    def test_symlink_file_and_directory_are_rejected(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        directory = self.project / ".agy"
        directory.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(OCRError):
            self.store.write("project", OCRProviderConfiguration("custom"))

    def test_invalid_scope_is_rejected(self):
        with self.assertRaises(OCRError):
            self.store.read("system")


class DiscoveryAndResolutionTests(ManagementTestCase):
    def test_listing_is_sorted_observational_and_has_no_ocr_calls(self):
        rows = self.manager.list_providers()
        self.assertEqual([row["provider_id"] for row in rows], ["custom", "tesseract"])
        self.assertTrue(rows[1]["default"])
        self.assertEqual(rows[0]["capabilities"]["execution_location"], "local")
        self.assertEqual(self.custom.calls + self.default.calls, [])

    def test_listing_reports_contract_failure_without_throwing(self):
        invalid = Provider("invalid", capabilities=OCRProviderCapabilities(False, True, "local", False))
        rows = OCRProviderManager({"invalid": invalid}, self.store, default="invalid").list_providers()
        self.assertFalse(rows[0]["available"])
        self.assertEqual(rows[0]["availability_error"], "OCR_PROVIDER_CAPABILITY_MISSING")

    def test_registry_key_must_equal_provider_id(self):
        with self.assertRaises(OCRError):
            OCRProviderManager({"alias": self.custom}, self.store)

    def test_no_config_uses_default(self):
        value = self.manager.effective()
        self.assertEqual((value.selected_provider, value.selection_origin), ("tesseract", "default"))
        self.assertFalse(value.allow_fallback)

    def test_frozen_precedence_and_layer_reveal(self):
        self.store.write("user", OCRProviderConfiguration("custom", True))
        self.assertEqual(self.manager.effective().selection_origin, "user")
        self.store.write("project", OCRProviderConfiguration("tesseract", False))
        self.assertEqual(self.manager.effective().selection_origin, "project")
        explicit = self.manager.effective(explicit="custom")
        self.assertEqual((explicit.selected_provider, explicit.selection_origin), ("custom", "explicit"))
        self.assertFalse(explicit.allow_fallback)
        self.store.unset("project")
        self.assertEqual(self.manager.effective().selection_origin, "user")
        self.store.unset("user")
        self.assertEqual(self.manager.effective().selection_origin, "default")

    def test_fallback_is_opt_in_and_single_default_is_visible(self):
        self.store.write("project", OCRProviderConfiguration("custom", True))
        value = self.manager.effective()
        self.assertTrue(value.allow_fallback)
        self.assertEqual(value.fallback_provider, "tesseract")
        self.store.write("project", OCRProviderConfiguration("tesseract", True))
        self.assertIsNone(self.manager.effective().fallback_provider)

    def test_unknown_provider_keeps_frozen_error(self):
        with self.assertRaises(OCRError) as caught:
            self.manager.effective(explicit="typo")
        self.assertEqual(caught.exception.error_code, "OCR_PROVIDER_NOT_FOUND")

    def test_effective_output_is_stable_and_path_free(self):
        first = self.manager.effective().to_dict()
        second = self.manager.effective().to_dict()
        self.assertEqual(first, second)
        payload = json.dumps(first, sort_keys=True)
        self.assertNotIn(self.temp.name, payload)


class ValidationAndMutationTests(ManagementTestCase):
    def test_validate_uses_non_ocr_probe(self):
        seen = []
        def probe(provider, languages):
            seen.append((provider.provider_id, languages))
            return {"engine_version": "9.1"}
        manager = OCRProviderManager(
            dict(self.manager.providers), self.store, validation_probes={"custom": probe}
        )
        result = manager.validate(provider_id="custom", languages=("eng",))
        self.assertEqual(result["details"], {"engine_version": "9.1"})
        self.assertEqual(seen, [("custom", ("eng",))])
        self.assertEqual(self.custom.calls, [])

    def test_validate_effective_selection(self):
        self.store.write("project", OCRProviderConfiguration("custom"))
        self.assertEqual(self.manager.validate()["provider_id"], "custom")

    def test_validation_preserves_machine_errors(self):
        codes = (
            "OCR_PROVIDER_VERSION_UNAVAILABLE", "OCR_PROVIDER_VERSION_UNSUPPORTED",
            "OCR_MODEL_CHANGED", "OCR_LANGUAGE_UNSUPPORTED", "OCR_PROVIDER_CAPABILITY_MISSING",
        )
        for code in codes:
            def probe(provider, languages, code=code):
                raise OCRError("bounded failure", code)
            manager = OCRProviderManager(
                dict(self.manager.providers), self.store, validation_probes={"custom": probe}
            )
            with self.subTest(code=code):
                with self.assertRaises(OCRError) as caught:
                    manager.validate(provider_id="custom")
                self.assertEqual(caught.exception.error_code, code)
                self.assertEqual(self.custom.calls, [])

    def test_missing_and_invalid_contract_errors_are_preserved(self):
        with self.assertRaises(OCRError) as caught:
            self.manager.validate(provider_id="missing")
        self.assertEqual(caught.exception.error_code, "OCR_PROVIDER_NOT_FOUND")
        invalid = Provider("invalid", provider_version="unknown")
        manager = OCRProviderManager({"invalid": invalid}, self.store, default="invalid")
        with self.assertRaises(OCRError) as caught:
            manager.validate(provider_id="invalid")
        self.assertEqual(caught.exception.error_code, "OCR_PROVIDER_VERSION_UNAVAILABLE")

    def test_set_validates_provider_and_preserves_fallback_when_unspecified(self):
        first = self.manager.set("project", "custom", allow_fallback=True)
        second = self.manager.set("project", "tesseract")
        self.assertTrue(first.allow_fallback)
        self.assertTrue(second.allow_fallback)
        self.assertEqual(self.default.calls + self.custom.calls, [])

    def test_set_rejects_unknown_provider_and_nonboolean_fallback(self):
        with self.assertRaises(OCRError) as caught:
            self.manager.set("project", "missing")
        self.assertEqual(caught.exception.error_code, "OCR_PROVIDER_NOT_FOUND")
        with self.assertRaises(OCRError):
            self.manager.set("project", "custom", allow_fallback=1)
        self.assertIsNone(self.store.read("project"))

    def test_secret_fields_are_rejected_without_value_leakage(self):
        secret = "super-secret-token"
        raw = json.dumps({"provider": "custom", "allow_fallback": False, "api_key": secret}).encode()
        with self.assertRaises(OCRError) as caught:
            OCRProviderConfiguration.from_bytes(raw)
        self.assertNotIn(secret, str(caught.exception))
        self.assertNotIn(secret, json.dumps(self.manager.list_providers()))

    def test_all_management_operations_have_zero_ocr_side_effects(self):
        self.manager.list_providers()
        self.manager.effective()
        self.manager.validate(provider_id="custom")
        self.manager.set("project", "custom")
        self.manager.unset("project")
        self.assertEqual(self.custom.calls + self.default.calls, [])


class CLITests(ManagementTestCase):
    def run_cli(self, manager, *arguments):
        output = io.StringIO()
        with patch("manage_ocr_providers._manager", return_value=manager), patch("sys.stdout", output):
            code = cli_main(list(arguments))
        return code, json.loads(output.getvalue())

    def test_list_show_set_unset_are_machine_readable_and_non_ocr(self):
        code, listed = self.run_cli(self.manager, "list")
        self.assertEqual(code, 0)
        self.assertEqual([p["provider_id"] for p in listed["providers"]], ["custom", "tesseract"])
        self.assertEqual(self.run_cli(self.manager, "show")[1]["selection_origin"], "default")
        self.assertEqual(self.run_cli(self.manager, "set", "--scope", "project", "--provider", "custom")[0], 0)
        self.assertTrue(self.run_cli(self.manager, "unset", "--scope", "project")[1]["removed"])
        self.assertEqual(self.custom.calls + self.default.calls, [])

    def test_cli_error_includes_exact_code_without_path(self):
        code, payload = self.run_cli(self.manager, "validate", "--provider", "missing")
        self.assertEqual(code, 1)
        self.assertEqual(payload["error_code"], "OCR_PROVIDER_NOT_FOUND")
        self.assertNotIn(self.temp.name, json.dumps(payload))

    def test_validate_cli_does_not_create_evidence(self):
        code, payload = self.run_cli(self.manager, "validate", "--provider", "custom")
        self.assertEqual((code, payload["valid"]), (0, True))
        self.assertEqual(self.custom.calls, [])


if __name__ == "__main__":
    unittest.main()
