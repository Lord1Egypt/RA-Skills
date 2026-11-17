import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from codemap.cli import main


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "i.db")
        p = os.path.join(self.tmp.name, "x.py")
        with open(p, "w") as fh:
            fh.write("def hello(name):\n    return name\n")
        self.src = p

    def tearDown(self):
        self.tmp.cleanup()

    def test_build_then_find(self):
        code, _, err = run(["--db", self.db, "build", self.tmp.name])
        self.assertEqual(code, 0)
        self.assertIn("indexed", err)
        code, out, _ = run(["--db", self.db, "find", "hello"])
        self.assertEqual(code, 0)
        self.assertIn("x.py:1", out)
        self.assertIn("[function]", out)

    def test_find_missing_exits_one(self):
        run(["--db", self.db, "build", self.tmp.name])
        code, _, err = run(["--db", self.db, "find", "nope"])
        self.assertEqual(code, 1)

    def test_find_json(self):
        run(["--db", self.db, "build", self.tmp.name])
        code, out, _ = run(["--db", self.db, "find", "hello", "--json"])
        self.assertIn('"name": "hello"', out)

    def test_file_outline(self):
        run(["--db", self.db, "build", self.tmp.name])
        code, out, _ = run(["--db", self.db, "file", self.src])
        self.assertEqual(code, 0)
        self.assertIn("hello", out)

    def test_stats(self):
        run(["--db", self.db, "build", self.tmp.name])
        code, out, _ = run(["--db", self.db, "stats"])
        self.assertIn('"symbols": 1', out)


if __name__ == "__main__":
    unittest.main()
