import unittest

from codemap.extractors import extract_python, extract_jsts, extract


class TestPython(unittest.TestCase):
    def test_function_and_class_and_method(self):
        src = (
            "import os\n"
            "\n"
            "def top_level(a, b):\n"
            "    return a + b\n"
            "\n"
            "class Widget:\n"
            "    def method(self):\n"
            "        pass\n"
            "    async def afetch(self, url):\n"
            "        pass\n"
        )
        syms = {(s.name, s.kind, s.line) for s in extract_python(src)}
        self.assertIn(("top_level", "function", 3), syms)
        self.assertIn(("Widget", "class", 6), syms)
        self.assertIn(("method", "method", 7), syms)
        self.assertIn(("afetch", "method", 9), syms)

    def test_signature_trimmed(self):
        src = "def foo(x, y):\n    pass\n"
        s = extract_python(src)[0]
        self.assertEqual(s.signature, "def foo(x, y)")

    def test_no_false_positive_on_word_def(self):
        src = "# the default value is set here\nx = 'define'\n"
        self.assertEqual(extract_python(src), [])


class TestJsTs(unittest.TestCase):
    def test_function_declaration(self):
        src = "export function makeRoute(req) {\n  return req;\n}\n"
        syms = {(s.name, s.kind) for s in extract_jsts(src, "ts")}
        self.assertIn(("makeRoute", "function"), syms)

    def test_arrow_const(self):
        src = "export const handler = async (req, res) => {\n};\n"
        syms = {(s.name, s.kind) for s in extract_jsts(src, "ts")}
        self.assertIn(("handler", "function"), syms)

    def test_class_interface_type(self):
        src = (
            "export class Pipeline {}\n"
            "interface Stage { id: string }\n"
            "type Ref = string | number;\n"
        )
        syms = {(s.name, s.kind) for s in extract_jsts(src, "ts")}
        self.assertIn(("Pipeline", "class"), syms)
        self.assertIn(("Stage", "interface"), syms)
        self.assertIn(("Ref", "type"), syms)

    def test_no_dupe_for_arrow_and_const(self):
        src = "const x = (a) => a;\n"
        self.assertEqual(len([s for s in extract_jsts(src) if s.name == "x"]), 1)


class TestDispatch(unittest.TestCase):
    def test_dispatch_by_extension(self):
        self.assertTrue(extract("foo.py", "def a():\n pass\n"))
        self.assertTrue(extract("foo.tsx", "export const C = () => null;\n"))
        self.assertEqual(extract("foo.md", "# heading\n"), [])


if __name__ == "__main__":
    unittest.main()
