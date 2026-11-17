"""Offline distribution checks, not model or dialect certification."""
import hashlib
import importlib.util
import shutil
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def builder(self):
        spec = importlib.util.spec_from_file_location('build_distribution', ROOT / 'scripts/build_distribution.py')
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def copy_source(self, target):
        names = json.loads((ROOT / 'distribution-files.json').read_text(encoding='utf-8'))['files']
        for name in names:
            dest = target / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        return names

    def test_private_material_is_rejected_before_archiving(self):
        mutations = [
            ('references/probe.md', 'gh' + 'p_' + 'a' * 30),
            ('references/probe.md', 'sk' + '-' + 'b' * 40),
            ('references/probe.md', 'Z' + ':/' + 'Users/example/private.txt'),
            ('references/probe.md', 'local' + '-' + 'a1b2c3d4e5'),
            ('references/probe.md', '-----BEGIN ' + 'PRIVATE KEY-----'),
            ('references/probe.md', 'Bearer ' + 'x' * 30),
            ('references/probe.md', 'api_key' + ' = ' + chr(34) + 'example-secret' + chr(34)),
            ('references/session.jsonl', '{}'),
            ('references/responses.json', '{}'),
            ('references/probe.db', 'database'),
            ('references/probe.zip', 'archive'),
            ('references/calibration.md', 'private preferences'),
        ]
        for name, text in mutations:
            with self.subTest(name=name, text_kind=text[:8]), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)
                names = self.copy_source(target)
                (target / name).write_text(text, encoding='utf-8')
                (target / 'distribution-files.json').write_text(json.dumps({'files': names + [name]}), encoding='utf-8')
                with self.assertRaises(ValueError):
                    self.builder().collect(target)

    def test_missing_local_reference_fails_closed(self):
        for link in ['[missing](references/absent.md)', '`references/absent.json`']:
            with self.subTest(link=link), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)
                self.copy_source(target)
                readme = target / 'README.md'
                readme.write_text(readme.read_text(encoding='utf-8') + '\n' + link, encoding='utf-8')
                with self.assertRaises(ValueError):
                    self.builder().collect(target)

    def test_reserved_and_case_colliding_members_rejected(self):
        for extra in ['MANIFEST.json', 'readme.md']:
            with self.subTest(extra=extra), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)
                names = self.copy_source(target)
                if extra == 'MANIFEST.json':
                    (target / extra).write_text('{}', encoding='utf-8')
                elif not (target / extra).exists():
                    shutil.copyfile(target / 'README.md', target / extra)
                (target / 'distribution-files.json').write_text(json.dumps({'files': names + [extra]}), encoding='utf-8')
                with self.assertRaises(ValueError):
                    self.builder().collect(target)

    def test_existing_path_and_schema_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            names = self.copy_source(target)
            for bad in [names + [names[0]], names + ['../outside.md'], names + ['absent.md'],
                        names + ['Z' + ':/' + 'outside.md'], names + ['references\\\\outside.md'],
                        [n for n in names if n != 'LICENSE'], [], [None], 'not-a-list']:
                with self.subTest(allowlist=bad):
                    (target / 'distribution-files.json').write_text(json.dumps({'files': bad}), encoding='utf-8')
                    with self.assertRaises(ValueError):
                        self.builder().collect(target)

    def test_unlisted_live_evidence_is_not_distributed(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            names = self.copy_source(target)
            (target / 'private').mkdir()
            (target / 'private' / 'responses.json').write_text('{}', encoding='utf-8')
            _, collected = self.builder().collect(target)
            self.assertEqual(set(collected), set(names))

    def test_build_is_allowlisted_reproducible_and_manifested(self):
        script = ROOT / 'scripts/build_distribution.py'
        self.assertTrue(script.is_file(), 'Distribution builder must exist')
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            command = [sys.executable, '-B', str(script), '--output-dir', str(output)]
            first = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(first.returncode, 0, first.stderr)
            archives = list(output.glob('*.zip'))
            self.assertEqual(len(archives), 1)
            data = archives[0].read_bytes()
            second = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(data, archives[0].read_bytes())
            allowlist = json.loads((ROOT / 'distribution-files.json').read_text(encoding='utf-8'))['files']
            with zipfile.ZipFile(archives[0]) as archive:
                self.assertIsNone(archive.testzip())
                prefix = 'emirati-arabic/'
                self.assertEqual(set(archive.namelist()), {prefix + n for n in allowlist} | {prefix + 'MANIFEST.json'})
                manifest = json.loads(archive.read(prefix + 'MANIFEST.json'))
                self.assertEqual(set(manifest['files']), set(allowlist))
                for name in allowlist:
                    actual = archive.read(prefix + name)
                    self.assertEqual(actual, (ROOT / name).read_bytes())
                    self.assertEqual(hashlib.sha256(actual).hexdigest(), manifest['files'][name])
                self.assertIn('LICENSE', allowlist)
                self.assertIn('THIRD_PARTY_NOTICES.md', allowlist)


if __name__ == '__main__':
    unittest.main()
