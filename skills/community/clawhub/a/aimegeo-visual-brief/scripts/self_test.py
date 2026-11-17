#!/usr/bin/env python3
"""Tests for the standalone local asset inventory validator."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_manifest import InvalidRecord, validate

class AssetInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup); self.root=Path(self.temp.name)
        from PIL import Image
        (self.root/"one.png").parent.mkdir(exist_ok=True)
        Image.new("RGB",(16,12),(30,60,90)).save(self.root/"one.png")
        self.record={"schema_version":1,"assets":[{"id":"diagram-1","file":"one.png","intended_use":"说明文配图","description":"蓝色方块示意图","alt_text":"浅色背景中的蓝色方块","rights_source":"由当前用户提供","review":"approved"}]}
    def test_local_image_is_decoded_and_counted(self):
        out=validate(self.record,self.root)
        self.assertEqual(out["summary"],{"assets":1,"available":1,"pending":0})
        self.assertEqual(out["assets"][0]["dimensions"],[16,12])
    def test_unreviewed_record_does_not_claim_a_deliverable(self):
        a=self.record["assets"][0]; a.update(file=None,review="needs_review")
        out=validate(self.record,self.root)
        self.assertEqual(out["summary"]["available"],0)
        self.assertEqual(out["assets"][0]["state"],"pending")
    def test_rejects_path_escape_and_symlink_escape(self):
        self.record["assets"][0]["file"]="../outside.png"
        with self.assertRaises(InvalidRecord): validate(self.record,self.root)
        with tempfile.TemporaryDirectory() as other:
            target=Path(other)/"outside.png"; target.write_bytes((self.root/"one.png").read_bytes())
            (self.root/"escape.png").symlink_to(target)
            self.record["assets"][0]["file"]="escape.png"
            with self.assertRaises(InvalidRecord): validate(self.record,self.root)
    def test_rejects_prompt_as_non_image_file(self):
        (self.root/"text.txt").write_text("not image")
        self.record["assets"][0]["file"]="text.txt"
        with self.assertRaises(InvalidRecord): validate(self.record,self.root)
    def test_duplicate_ids_and_files_are_rejected(self):
        self.record["assets"].append(dict(self.record["assets"][0],id="diagram-2"))
        with self.assertRaises(InvalidRecord): validate(self.record,self.root)
        self.record["assets"][1]["file"]="one.png"
        with self.assertRaises(InvalidRecord): validate(self.record,self.root)
    def test_cli_example_pending_state(self):
        data=json.loads((Path(__file__).resolve().parents[1]/"examples/assets.json").read_text())
        out=validate(data,self.root)
        self.assertEqual(out["summary"],{"assets":1,"available":0,"pending":1})

if __name__=="__main__": unittest.main()
