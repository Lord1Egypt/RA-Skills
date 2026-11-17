import os
import tempfile
import unittest

from codemap import index


class IndexTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        self.db = os.path.join(self.root, "index.db")
        self._write("a.py", "def alpha():\n    pass\n\nclass Beta:\n    def m(self):\n        pass\n")
        self._write("sub/b.ts", "export function gamma(x) {\n  return x;\n}\n")
        self._write("node_modules/skip.py", "def should_not_index():\n    pass\n")
        self._write("readme.md", "# not code\n")

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, rel, content):
        p = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write(content)
        return p

    def test_build_counts(self):
        res = index.build([self.root], db_path=self.db)
        # alpha, Beta, m, gamma = 4 (node_modules + md skipped)
        self.assertEqual(res["symbols"], 4)

    def test_find_exact(self):
        index.build([self.root], db_path=self.db)
        hits = index.find("alpha", db_path=self.db)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].kind, "function")
        self.assertTrue(hits[0].file.endswith("a.py"))
        self.assertEqual(hits[0].line, 1)

    def test_find_like(self):
        index.build([self.root], db_path=self.db)
        hits = index.find("amm", db_path=self.db, exact=False)
        self.assertEqual({h.name for h in hits}, {"gamma"})

    def test_find_kind_filter(self):
        index.build([self.root], db_path=self.db)
        self.assertEqual(index.find("Beta", db_path=self.db, kind="function"), [])
        self.assertEqual(len(index.find("Beta", db_path=self.db, kind="class")), 1)

    def test_node_modules_skipped(self):
        index.build([self.root], db_path=self.db)
        self.assertEqual(index.find("should_not_index", db_path=self.db), [])

    def test_outline(self):
        index.build([self.root], db_path=self.db)
        hits = index.outline(os.path.join(self.root, "a.py"), db_path=self.db)
        self.assertEqual([h.name for h in hits], ["alpha", "Beta", "m"])

    def test_rebuild_is_idempotent(self):
        index.build([self.root], db_path=self.db)
        index.build([self.root], db_path=self.db)
        self.assertEqual(len(index.find("alpha", db_path=self.db)), 1)

    def test_stats(self):
        index.build([self.root], db_path=self.db)
        s = index.stats(db_path=self.db)
        self.assertEqual(s["symbols"], 4)
        self.assertEqual(s["by_kind"].get("class"), 1)

    def test_compact_format(self):
        index.build([self.root], db_path=self.db)
        hit = index.find("alpha", db_path=self.db)[0]
        self.assertIn("a.py:1", hit.compact())
        self.assertIn("[function]", hit.compact())


if __name__ == "__main__":
    unittest.main()
