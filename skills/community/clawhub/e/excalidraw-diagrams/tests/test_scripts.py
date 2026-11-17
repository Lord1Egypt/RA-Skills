import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_diagram as bd  # noqa: E402
import validate as val  # noqa: E402

EXAMPLES = sorted((ROOT / "examples").glob("*.json"))


def spec(**extra):
    base = {
        "nodes": [{"id": "a", "label": "Start"}, {"id": "b", "label": "Middle"}, {"id": "c", "label": "End"}],
        "edges": [{"from": "a", "to": "b"}, {"from": "b", "to": "c", "label": "next"}],
    }
    base.update(extra)
    return base


class BuildTests(unittest.TestCase):
    def test_output_is_deterministic(self):
        first, _ = bd.build(spec(), "excalidraw")
        second, _ = bd.build(spec(), "excalidraw")
        self.assertEqual(first, second)

    def test_examples_build_and_validate_cleanly(self):
        self.assertTrue(EXAMPLES)
        with tempfile.TemporaryDirectory() as tmp:
            for example in EXAMPLES:
                raw = json.loads(example.read_text(encoding="utf-8"))
                for fmt, name in (("excalidraw", "x.excalidraw"), ("obsidian", "x.excalidraw.md")):
                    content, info = bd.build(raw, fmt)
                    out = Path(tmp) / name
                    out.write_text(content, encoding="utf-8")
                    result = val.validate(out)
                    self.assertTrue(result["ok"], (example.name, fmt, result["errors"]))
                    self.assertEqual(result["warnings"], [], (example.name, fmt))
                    self.assertEqual(info["warnings"], [], example.name)

    def test_bindings_are_two_way(self):
        content, _ = bd.build(spec(), "excalidraw")
        elements = {el["id"]: el for el in json.loads(content)["elements"]}
        arrows = [el for el in elements.values() if el["type"] == "arrow"]
        self.assertEqual(len(arrows), 2)
        for arrow in arrows:
            for side in ("startBinding", "endBinding"):
                target = elements[arrow[side]["elementId"]]
                self.assertIn(arrow["id"], [b["id"] for b in target["boundElements"]])
        labels = [el for el in elements.values() if el["type"] == "text" and el["containerId"]]
        self.assertEqual(len(labels), 4)  # three node labels and one edge label
        for label in labels:
            self.assertIn(label["id"], [b["id"] for b in elements[label["containerId"]]["boundElements"]])

    def test_all_text_uses_requested_font(self):
        content, _ = bd.build(spec(title="T"), "excalidraw")
        fonts = {el["fontFamily"] for el in json.loads(content)["elements"] if el["type"] == "text"}
        self.assertEqual(fonts, {5})
        content, _ = bd.build(spec(font="virgil"), "excalidraw")
        fonts = {el["fontFamily"] for el in json.loads(content)["elements"] if el["type"] == "text"}
        self.assertEqual(fonts, {1})

    def test_cycles_lay_out_and_back_edge_detours(self):
        raw = spec()
        raw["edges"].append({"from": "c", "to": "a"})
        content, info = bd.build(raw, "excalidraw")
        self.assertEqual(info["warnings"], [])
        back = [el for el in json.loads(content)["elements"] if el["type"] == "arrow"][-1]
        self.assertEqual(len(back["points"]), 4)

    def test_nodes_do_not_overlap(self):
        raw = {
            "groups": [{"id": "g", "label": "G"}],
            "nodes": [{"id": f"n{i}", "label": f"Node {i}", "group": "g" if i % 2 else None} for i in range(9)],
            "edges": [{"from": "n0", "to": f"n{i}"} for i in range(1, 9)],
        }
        for direction in ("TB", "LR"):
            raw["direction"] = direction
            content, _ = bd.build(raw, "excalidraw")
            elements = json.loads(content)["elements"]
            _, warnings, _ = val.check_elements(elements)
            self.assertFalse([w for w in warnings if "overlap" in w], direction)

    def test_obsidian_wrapper(self):
        content, _ = bd.build(spec(), "obsidian", ["excalidraw", "architecture"])
        self.assertIn("excalidraw-plugin: parsed", content)
        self.assertIn("tags: [excalidraw, architecture]", content)
        self.assertRegex(content, r"## Text Elements\nStart \^[0-9A-Za-z]{20}\n")
        self.assertIn("%%\n## Drawing\n```json\n", content)
        self.assertIn(bd.OBSIDIAN_SOURCE, content)

    def test_spec_errors(self):
        bad_specs = [
            {"nodes": []},
            {"nodes": [{"id": "a"}, {"id": "a"}]},
            {"nodes": [{"id": "a"}], "edges": [{"from": "a", "to": "zzz"}]},
            {"nodes": [{"id": "a", "shape": "hexagon"}]},
            {"nodes": [{"id": "a", "color": "teal"}]},
            {"nodes": [{"id": "a", "group": "nope"}]},
            {"nodes": [{"id": "a"}], "direction": "RL"},
        ]
        for raw in bad_specs:
            with self.assertRaises(bd.SpecError, msg=raw):
                bd.build(raw, "excalidraw")


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        from io import StringIO
        from contextlib import redirect_stdout

        buf = StringIO()
        with redirect_stdout(buf):
            code = bd.main(list(args))
        return code, buf.getvalue()

    def test_refuses_to_overwrite_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "spec.json"
            spec_path.write_text(json.dumps(spec()), encoding="utf-8")
            out = Path(tmp) / "d.excalidraw.md"
            code, _ = self.run_cli("--spec", str(spec_path), "--out", str(out))
            self.assertEqual(code, 0)
            out.write_text("user edits", encoding="utf-8")
            code, text = self.run_cli("--spec", str(spec_path), "--out", str(out))
            self.assertEqual(code, 1)
            self.assertIn("already exists", json.loads(text)["error"])
            self.assertEqual(out.read_text(encoding="utf-8"), "user edits")
            code, _ = self.run_cli("--spec", str(spec_path), "--out", str(out), "--force")
            self.assertEqual(code, 0)
            self.assertTrue(val.validate(out)["ok"])

    def test_missing_folder_and_unknown_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "spec.json"
            spec_path.write_text(json.dumps(spec()), encoding="utf-8")
            code, text = self.run_cli("--spec", str(spec_path), "--out", str(Path(tmp) / "no" / "d.excalidraw"))
            self.assertEqual(code, 1)
            self.assertIn("folder does not exist", text)
            self.assertFalse((Path(tmp) / "no").exists())
            code, text = self.run_cli("--spec", str(spec_path), "--out", str(Path(tmp) / "d.txt"))
            self.assertEqual(code, 1)


class ValidateTests(unittest.TestCase):
    def test_detects_broken_bindings(self):
        content, _ = bd.build(spec(), "excalidraw")
        data = json.loads(content)
        for el in data["elements"]:
            if el["type"] in bd.SHAPES:
                el["boundElements"] = None
        errors, _, _ = val.check_elements(data["elements"])
        self.assertTrue(any("does not list this arrow" in e for e in errors))
        self.assertTrue(any("does not list this text" in e for e in errors))

    def test_detects_bad_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.md"
            path.write_text("# just a note\n", encoding="utf-8")
            result = val.validate(path)
            self.assertFalse(result["ok"])


    def test_malformed_elements_return_errors(self):
        content, _ = bd.build(spec(), "excalidraw")
        cases = [("id", []), ("type", []), ("x", "bad"), ("width", float("nan")),
                 ("opacity", "opaque"), ("boundElements", [None]),
                 ("boundElements", [{"id": [], "type": "text"}]),
                 ("containerId", []), ("startBinding", "bad"), ("fontFamily", [])]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                elements = json.loads(content)["elements"]
                elements[0][field] = value
                errors, _, _ = val.check_elements(elements)
                self.assertTrue(errors)

    def test_invalid_utf8_returns_json_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invalid.excalidraw"
            path.write_bytes(b"\xff")
            self.assertFalse(val.validate(path)["ok"])

    def test_frontmatter_key_in_body_is_not_frontmatter(self):
        content, _ = bd.build(spec(), "obsidian")
        content = content.replace("excalidraw-plugin: parsed", "", 1)
        content += "\nexcalidraw-plugin: parsed\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invalid.md"
            path.write_text(content, encoding="utf-8")
            self.assertFalse(val.validate(path)["ok"])

    def test_reverse_arrow_binding_is_checked(self):
        content, _ = bd.build(spec(), "excalidraw")
        elements = json.loads(content)["elements"]
        arrow = next(el for el in elements if el["type"] == "arrow")
        arrow["startBinding"] = None
        errors, _, _ = val.check_elements(elements)
        self.assertTrue(any("bind back" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
