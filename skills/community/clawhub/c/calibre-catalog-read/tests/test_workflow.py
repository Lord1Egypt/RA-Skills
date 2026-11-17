import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts"
spec = importlib.util.spec_from_file_location("pipeline", SCRIPT / "run_analysis_pipeline.py")
pipe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipe)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="calibre-catalog-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.lib = self.root / "library"
        self.lib.mkdir()
        (self.lib / "metadata.db").write_text("")
        self.control = self.bin / "fake.json"
        self.control.write_text(json.dumps({"id": 1, "text": "Synthetic chapter. 日本語😀 Evidence and coverage.\n" * 80}))
        fake = r'''#!/usr/bin/env python3
import sys,json,pathlib
p=pathlib.Path(__file__).parent
c=json.loads((p/'fake.json').read_text())
a=sys.argv[1:]
with (p/'calls.jsonl').open('a') as out: out.write(json.dumps(a)+'\n')
if c.get('failure'):
 password=''
 if '--password' in a:
  arg=a[a.index('--password')+1]
  if arg.startswith('<f:'):password=pathlib.Path(arg[3:-1]).read_text()
 print('failure '+password,file=sys.stderr);sys.exit(2)
if a[0]=='list':
 if a[a.index('--with-library')+1].endswith('#-'):print('main\n日本語')
 else:print(json.dumps([{'id':c.get('id',1),'uuid':'book-uuid','title':'Synthetic','tags':c.get('tags',[]),'formats':['EPUB']}]))
elif a[0]=='export':
 assert '--dont-update-metadata' in a
 dest=pathlib.Path(a[a.index('--to-dir')+1]);dest.mkdir(exist_ok=True)
 (dest/'source.epub').write_bytes(b'Synthetic original EPUB bytes')
else:raise RuntimeError('unexpected mutation/command: '+a[0])
'''
        convert = r'''#!/usr/bin/env python3
import pathlib,sys,json
p=pathlib.Path(__file__).parent
c=json.loads((p/'fake.json').read_text())
pathlib.Path(sys.argv[2]).write_text(c['text'],encoding='utf-8')
'''
        for name, body in [("calibredb", fake), ("ebook-convert", convert)]:
            f = self.bin / name
            f.write_text(body)
            f.chmod(0o700)
        self.env = {"PATH": str(self.bin) + os.pathsep + os.environ["PATH"], "HOME": str(self.root), "LANG": "C.UTF-8"}
        self.state = self.root / "runs.json"

    def cli(self, name, *args, env=None):
        command = [sys.executable if name.endswith('.py') else 'node', str(SCRIPT / name), *map(str, args)]
        return subprocess.run(command, env={**self.env, **(env or {})}, cwd=self.root, capture_output=True, text=True, timeout=20)

    def prepare(self, run="run1", **control):
        if control:
            c = json.loads(self.control.read_text()); c.update(control); self.control.write_text(json.dumps(c))
        r = self.cli("run_analysis_pipeline.py", "prepare", "--with-library", self.lib, "--book-id", 1, "--run-id", run, "--cache-dir", self.root / "cache", "--chunk-chars", 1000)
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)

    def analysis(self, prepared, partial=False):
        m = pipe.read_json(prepared["prepared_input"])
        parts = m["source_files"][:1] if partial else m["source_files"]
        a = {k: m[k] for k in ("run_id", "book_id", "library_id", "file_hash", "lang")}
        a.update(summary="Synthetic verified analysis", highlights=["First", "Second"], reread=[{"section": "chapter", "page": "n/a", "chunk_id": parts[0]["id"], "reason": "Evidence"}], tags=["analysis"], coverage={"mode": "partial" if partial else "full", "expected_files": len(m["source_files"]), "read_files": len(parts), "read_chars": sum(p["chars"] for p in parts), "part_ids": [p["id"] for p in parts]})
        return a

    def finish(self, p, a, name="proposal.jsonl"):
        f = self.root / "analysis.json"; f.write_text(json.dumps(a))
        return self.cli("run_analysis_pipeline.py", "complete", "--prepared-input", p["prepared_input"], "--analysis-json", f, "--proposal-jsonl", self.root / name)

    def test_machine_json_and_exact_id(self):
        r = self.cli("calibredb_read.mjs", "id", "--book-id", 1, "--with-library", self.lib)
        self.assertEqual(r.returncode, 0, r.stderr); self.assertEqual(json.loads(r.stdout)["item"]["id"], 1)
        c = json.loads(self.control.read_text()); c["id"] = 2; self.control.write_text(json.dumps(c))
        r = self.cli("calibredb_read.mjs", "id", "--book-id", 1, "--with-library", self.lib)
        self.assertIsNone(json.loads(r.stdout)["item"])

    def test_help_and_unknown_flags(self):
        for script in ("calibredb_read.mjs", "prepare_subagent_input.mjs", "run_state.mjs", "handle_completion.mjs", "run_analysis_pipeline.py", "analysis_db.py"):
            self.assertEqual(self.cli(script, "--help").returncode, 0, script)
        self.assertNotEqual(self.cli("calibredb_read.mjs", "list", "--bogus", "x").returncode, 0)

    def test_libraries(self):
        r = self.cli("calibredb_read.mjs", "libraries", "--with-library", "http://example.invalid:8080/")
        self.assertEqual(json.loads(r.stdout)["items"], ["main", "日本語"])

    def test_japanese_library_id_is_literal_at_cli_boundary(self):
        endpoint = "http://example.invalid:8080/#日本語ライブラリ"
        r = self.cli("calibredb_read.mjs", "list", "--with-library", endpoint)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        call = json.loads((self.bin / "calls.jsonl").read_text().splitlines()[-1])
        self.assertEqual(call[call.index("--with-library") + 1], endpoint)
        r = self.cli("run_analysis_pipeline.py", "prepare", "--with-library", endpoint, "--book-id", 1, "--run-id", "japanese", "--cache-dir", self.root / "cache")
        self.assertEqual(r.returncode, 0, r.stderr)
        for line in (self.bin / "calls.jsonl").read_text().splitlines():
            call = json.loads(line)
            self.assertEqual(call[call.index("--with-library") + 1], endpoint)

    def test_failed_cli_redacts_password(self):
        self.control.write_text(json.dumps({"failure": True}))
        r = self.cli("calibredb_read.mjs", "list", "--with-library", self.lib, env={"CALIBRE_PASSWORD": "synthetic-secret"})
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("synthetic-secret", r.stdout + r.stderr)
        self.assertNotIn("synthetic-secret", (self.bin / "calls.jsonl").read_text())

    def test_prepare_then_complete_is_offline_and_readonly(self):
        p = self.prepare(); before = (self.bin / "calls.jsonl").read_text(); r = self.finish(p, self.analysis(p))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual((self.bin / "calls.jsonl").read_text(), before)
        proposal = pipe.read_json(self.root / "proposal.jsonl")
        self.assertEqual(proposal["expected_uuid"], "book-uuid")
        self.assertEqual(proposal["expected_library"], str(self.lib))
        self.assertEqual(set(json.loads(x)[0] for x in before.splitlines()), {"list", "export"})
        self.assertNotEqual(self.finish(p, self.analysis(p)).returncode, 0)

    def test_partial_coverage_and_wrong_target(self):
        p = self.prepare(); a = self.analysis(p, partial=True)
        self.assertEqual(self.finish(p, a).returncode, 0)
        a["book_id"] = 2
        self.assertNotEqual(self.finish(p, a, "wrong.jsonl").returncode, 0)

    def test_forged_coverage_rejected(self):
        p = self.prepare(); a = self.analysis(p)
        for coverage in [{"mode": "full", "expected_files": 0, "read_files": 0, "read_chars": 1, "part_ids": []}, {**a["coverage"], "read_chars": 1}, {**a["coverage"], "part_ids": ["missing"]}]:
            a["coverage"] = coverage
            self.assertNotEqual(self.finish(p, a).returncode, 0)
        self.assertFalse((self.root / "proposal.jsonl").exists())

    def test_prepared_source_tamper_rejected(self):
        p = self.prepare(); a = self.analysis(p); m = pipe.read_json(p["prepared_input"])
        Path(m["source_files"][0]["path"]).write_text("changed")
        self.assertNotEqual(self.finish(p, a).returncode, 0)

    def test_low_text_and_comic_do_not_create_proposal(self):
        p = self.prepare(text="short")
        self.assertEqual(p["reason"], "low_text_requires_confirmation")
        self.assertNotIn("prepared_input", p)
        p = self.prepare("run2", tags=["manga"])
        self.assertEqual(p["reason"], "excluded_content")

    def test_distinct_endpoint_identity(self):
        self.assertNotEqual(pipe.library_identity("http://one:8080/#main"), pipe.library_identity("http://two:8080/#main"))
        for value in ("http://user:secret@one:8080/#main", "http://one:8080/#library_id=main"):
            with self.assertRaises(ValueError): pipe.library_identity(value)

    def test_completion_binding_duplicate_and_corrupt_state(self):
        p = self.prepare(); a = self.analysis(p); f = self.root / "analysis.json"; f.write_text(json.dumps(a))
        r = self.cli("run_state.mjs", "upsert", "--run-id", "run1", "--input-json", p["prepared_input"], "--state", self.state)
        self.assertEqual(r.returncode, 0, r.stderr)
        args = ["--run-id", "run1", "--analysis-json", f, "--proposal-jsonl", self.root / "registered.jsonl", "--state", self.state]
        r = self.cli("handle_completion.mjs", *args); self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"], "proposal_created")
        f.unlink(); r = self.cli("handle_completion.mjs", *args)
        self.assertEqual(json.loads(r.stdout)["status"], "stale_or_duplicate")
        self.state.write_text("{corrupt")
        self.assertNotEqual(self.cli("handle_completion.mjs", *args).returncode, 0)
        self.assertEqual(self.state.read_text(), "{corrupt")

    def test_concurrent_completion_and_failed_run_not_retried(self):
        p = self.prepare(); f = self.root / "analysis.json"; f.write_text(json.dumps(self.analysis(p)))
        self.assertEqual(self.cli("run_state.mjs", "upsert", "--run-id", "run1", "--input-json", p["prepared_input"], "--state", self.state).returncode, 0)
        args = ['node', str(SCRIPT/'handle_completion.mjs'), '--run-id','run1','--analysis-json',str(f),'--proposal-jsonl',str(self.root/'one.jsonl'),'--state',str(self.state)]
        workers = [subprocess.Popen(args,env=self.env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for _ in range(2)]
        outputs = [w.communicate(timeout=20) for w in workers]
        created = sum(w.returncode == 0 and json.loads(o[0]).get('status') == 'proposal_created' for w,o in zip(workers,outputs))
        self.assertEqual(created,1)
        q = self.prepare('run2'); self.cli('run_state.mjs','upsert','--run-id','run2','--input-json',q['prepared_input'],'--state',self.state)
        self.cli('run_state.mjs','fail','--run-id','run2','--error','test','--state',self.state)
        r=self.cli('handle_completion.mjs','--run-id','run2','--analysis-json','/missing','--proposal-jsonl',self.root/'two.jsonl','--state',self.state)
        self.assertNotEqual(r.returncode,0)
        self.assertFalse((self.root/'two.jsonl').exists())


if __name__ == "__main__":
    unittest.main()
