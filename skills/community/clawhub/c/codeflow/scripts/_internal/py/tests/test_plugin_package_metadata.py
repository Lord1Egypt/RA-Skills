import json
import os
import unittest


TESTS_DIR = os.path.dirname(__file__)
PY_DIR = os.path.abspath(os.path.join(TESTS_DIR, ".."))
SKILL_DIR = os.path.abspath(os.path.join(PY_DIR, "..", "..", ".."))
PLUGIN_PACKAGE = os.path.join(SKILL_DIR, "extensions", "codeflow-enforcer", "package.json")


class PluginPackageMetadataTests(unittest.TestCase):
    def test_package_declares_openclaw_extensions_entry(self):
        with open(PLUGIN_PACKAGE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIsInstance(data, dict)
        openclaw = data.get("openclaw")
        self.assertIsInstance(openclaw, dict)
        extensions = openclaw.get("extensions")
        self.assertIsInstance(extensions, list)
        self.assertIn("./index.js", extensions)


if __name__ == "__main__":
    unittest.main()
