"""Installation drift detection must inspect bytes, not just versions or timestamps."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from verify_expert_install import compare

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.inst=self.root/'install';self.inst.mkdir();self.zip=self.root/'release.zip'
        self.manifest={'version':'3.0.2','local_revision':'release-20261113','build_id':'test'}
        self.entries={'assets/skill-version.json':json.dumps(self.manifest).encode(),'scripts/test.py':b'print("synthetic")'}
        for n,b in self.entries.items():p=self.inst/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        self.write_zip()
    def tearDown(self):self.tmp.cleanup()
    def write_zip(self):
        with zipfile.ZipFile(self.zip,'w') as z:
            for n,b in self.entries.items():z.writestr(n,b)
    def test_equal(self):self.assertTrue(compare(self.zip,self.inst)['matched'])
    def test_only_manifest_revision_mismatch(self):
        p=self.inst/'assets/skill-version.json';v=dict(self.manifest,local_revision='local-r4');p.write_text(json.dumps(v));r=compare(self.zip,self.inst);self.assertFalse(r['matched']);self.assertEqual(['assets/skill-version.json'],[v['file'] for v in r['different']]);self.assertEqual('local-r4',r['metadata'][0]['installed']['local_revision'])
    def test_same_version_not_proof_of_same_code(self):
        (self.inst/'scripts/test.py').write_text('changed');r=compare(self.zip,self.inst);self.assertFalse(r['matched']);self.assertEqual('scripts/test.py',r['different'][0]['file'])
    def test_missing(self):
        (self.inst/'scripts/test.py').unlink();self.assertEqual('scripts/test.py',compare(self.zip,self.inst)['missing'][0]['file'])
    def test_extra_runtime_file_ignored(self):
        (self.inst/'downloaded_at').write_text('runtime');self.assertTrue(compare(self.zip,self.inst)['matched'])
    def test_no_auto_repair(self):
        p=self.inst/'scripts/test.py';p.write_text('preserve');compare(self.zip,self.inst);self.assertEqual('preserve',p.read_text())
    def test_traversal_refused(self):
        self.entries['../escape']=b'unsafe';self.write_zip()
        with self.assertRaises(ValueError):compare(self.zip,self.inst)
    def test_reference_doc_keeps_assertion_boundaries(self):
        t=(Path(__file__).resolve().parents[2]/'references/专家实测与证据交付.md').read_text(encoding='utf-8')
        for text in ['首次失败','多目标受理','实际去重','verify_expert_install.py']:self.assertIn(text,t)
if __name__=='__main__':unittest.main()
