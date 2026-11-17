"""Consumer-visible CLI contracts; all vaults and hooks are temporary."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'scripts' / 'vault.py'


class VaultCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'vault'
        self.root.mkdir()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith('OBSIDIAN_')}
        self.env.update(OBSIDIAN_VAULT_PATH=str(self.root), XDG_CACHE_HOME=str(self.base / 'cache'))

    def note(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode('utf-8'))
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def cli(self, *args, code=0):
        result = subprocess.run([sys.executable, str(HELPER), *args], env=self.env,
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def content(self, text):
        path = self.base / 'content.md'
        path.write_bytes(text.encode('utf-8'))
        return str(path)

    def test_mkdir_enables_note_creation_and_existing_directory_is_noop(self):
        log = self.base / 'hooks'
        self.env['OBSIDIAN_PRE_COMMAND'] = f"printf 'pre\\n' >> '{log}'"
        self.env['OBSIDIAN_POST_COMMAND'] = f"printf 'post\\n' >> '{log}'"
        first = self.cli('mkdir', 'Inbox/')
        self.assertEqual(first['created_directories'], ['Inbox'])
        self.assertTrue(first['changed'])
        second = self.cli('mkdir', 'Inbox')
        self.assertFalse(second['changed'])
        self.assertEqual(second['created_directories'], [])
        self.assertEqual(log.read_text(), 'pre\npost\npre\n')
        self.cli('create', 'Inbox/Example.md', '--content-file', self.content('# Example\n'))
        self.assertEqual((self.root / 'Inbox/Example.md').read_text(), '# Example\n')

    def test_mkdir_parents_are_explicit_and_existing_file_is_preserved(self):
        self.cli('mkdir', 'Projects/New/Notes', code=1)
        self.assertFalse((self.root / 'Projects').exists())
        result = self.cli('mkdir', 'Projects/New/Notes', '--parents')
        self.assertEqual(result['created_directories'], ['Projects', 'Projects/New', 'Projects/New/Notes'])
        self.assertTrue((self.root / 'Projects/New/Notes').is_dir())
        self.note('Conflict.md', 'preserve me')
        self.cli('mkdir', 'Conflict.md', code=1)
        self.cli('mkdir', 'Conflict.md/Child', '--parents', code=1)
        self.assertEqual((self.root / 'Conflict.md').read_text(), 'preserve me')
        self.cli('read', 'Projects/New/Notes', code=1)

    def test_mkdir_enforces_rules_before_creating_parents(self):
        self.cli('--read-only', 'Archive', 'mkdir', 'Archive/New', '--parents', code=1)
        self.cli('--no-read', 'Private', 'mkdir', 'Private/New', '--parents', code=1)
        self.cli('mkdir', 'New/.obsidian/Child', '--parents', code=1)
        self.cli('mkdir', 'New/../Escaped', '--parents', code=1)
        self.cli('mkdir', str(self.base / 'outside'), code=1)
        self.assertEqual(list(self.root.iterdir()), [])
        outside = self.base / 'outside'
        outside.mkdir()
        (self.root / 'Link').symlink_to(outside, target_is_directory=True)
        self.cli('mkdir', 'Link/Child', '--parents', code=1)
        self.assertFalse((outside / 'Child').exists())
        self.cli('mkdir', 'Link', code=1)

    def test_mkdir_respects_hook_failures(self):
        self.env['OBSIDIAN_PRE_COMMAND'] = 'exit 7'
        self.cli('mkdir', 'Blocked', code=1)
        self.assertFalse((self.root / 'Blocked').exists())
        del self.env['OBSIDIAN_PRE_COMMAND']
        self.env['OBSIDIAN_POST_COMMAND'] = 'exit 9'
        result = self.cli('mkdir', 'Inbox', code=2)
        self.assertTrue(result['saved_locally'])
        self.assertEqual(result['synchronization'], 'failed')
        self.assertEqual(result['result']['created_directories'], ['Inbox'])
        self.assertTrue((self.root / 'Inbox').is_dir())

    def test_mkdir_does_not_initialize_missing_vault_root(self):
        missing = self.base / 'missing-vault'
        self.env['OBSIDIAN_VAULT_PATH'] = str(missing)
        self.cli('mkdir', 'Inbox', '--parents', code=1)
        self.assertFalse(missing.exists())

    def test_rmdir_preview_and_apply_remove_only_named_directory(self):
        (self.root / 'Parent/Empty').mkdir(parents=True)
        log = self.base / 'hooks'
        self.env['OBSIDIAN_PRE_COMMAND'] = f"printf 'pre\\n' >> '{log}'"
        self.env['OBSIDIAN_POST_COMMAND'] = f"printf 'post\\n' >> '{log}'"
        preview = self.cli('rmdir', 'Parent/Empty/')
        self.assertFalse(preview['applied'])
        self.assertTrue((self.root / 'Parent/Empty').is_dir())
        result = self.cli('rmdir', 'Parent/Empty', '--apply')
        self.assertTrue(result['applied'])
        self.assertFalse((self.root / 'Parent/Empty').exists())
        self.assertTrue((self.root / 'Parent').is_dir())
        self.cli('rmdir', 'Parent/Empty', '--apply', code=1)
        self.assertEqual(log.read_text(), 'pre\npre\npost\npre\n')

    def test_rmdir_refuses_any_contents_without_recursive_deletion(self):
        for entry in ('note.md', '.hidden', 'subdirectory'):
            with self.subTest(entry=entry):
                folder = self.root / entry
                folder.mkdir()
                child = folder / entry
                if entry == 'subdirectory':
                    child.mkdir()
                else:
                    child.write_text('preserve me')
                self.cli('rmdir', entry, code=1)
                self.cli('rmdir', entry, '--apply', code=1)
                self.assertTrue(child.exists())
                if child.is_file():
                    self.assertEqual(child.read_text(), 'preserve me')

    def test_rmdir_rechecks_contents_after_preview(self):
        (self.root / 'Empty').mkdir()
        self.cli('rmdir', 'Empty')
        self.note('Empty/New.md', 'concurrent content')
        self.cli('rmdir', 'Empty', '--apply', code=1)
        self.assertEqual((self.root / 'Empty/New.md').read_text(), 'concurrent content')

    def test_rmdir_enforces_access_rules_and_root_protections(self):
        for name in ('Archive', 'Private', '.obsidian', '.git', '.trash'):
            (self.root / name).mkdir()
        self.cli('--read-only', 'Archive', 'rmdir', 'Archive', '--apply', code=1)
        self.cli('--no-read', 'Private', 'rmdir', 'Private', '--apply', code=1)
        for name in ('.obsidian', '.git', '.trash', '.', '', '..', str(self.root)):
            with self.subTest(path=name):
                self.cli('rmdir', name, '--apply', code=1)
        for name in ('Archive', 'Private', '.obsidian', '.git', '.trash'):
            self.assertTrue((self.root / name).is_dir())
        outside = self.base / 'outside'
        outside.mkdir()
        (outside / 'Child').mkdir()
        (self.root / 'Link').symlink_to(outside, target_is_directory=True)
        self.cli('rmdir', 'Link', '--apply', code=1)
        self.cli('rmdir', 'Link/Child', '--apply', code=1)
        self.assertTrue((outside / 'Child').is_dir())
        self.assertTrue(self.root.is_dir())

    def test_rmdir_refuses_file_targets(self):
        self.note('Keep.md', 'preserve me')
        self.cli('rmdir', 'Keep.md', '--apply', code=1)
        self.assertEqual((self.root / 'Keep.md').read_text(), 'preserve me')

    def test_rmdir_preserves_directory_on_pre_failure_and_reports_post_failure(self):
        (self.root / 'Empty').mkdir()
        self.env['OBSIDIAN_PRE_COMMAND'] = 'exit 7'
        self.cli('rmdir', 'Empty', '--apply', code=1)
        self.assertTrue((self.root / 'Empty').is_dir())
        del self.env['OBSIDIAN_PRE_COMMAND']
        self.env['OBSIDIAN_POST_COMMAND'] = 'exit 9'
        result = self.cli('rmdir', 'Empty', '--apply', code=2)
        self.assertTrue(result['saved_locally'])
        self.assertEqual(result['synchronization'], 'failed')
        self.assertTrue(result['result']['applied'])
        self.assertFalse((self.root / 'Empty').exists())

    def test_create_read_write_and_stale_hash(self):
        self.cli('create', 'A.md', '--content-file', self.content('---\ntags: [a]\n---\nhello\n'))
        read = self.cli('read', 'A.md')
        updated = '---\ntags: [a]\n---\nworld\n'
        self.cli('write', 'A.md', '--content-file', self.content(updated), '--expected-sha256', read['sha256'])
        self.cli('write', 'A.md', '--content-file', self.content('lost'), '--expected-sha256', read['sha256'], code=1)
        self.assertEqual((self.root / 'A.md').read_text(), updated)
        self.cli('create', 'A.md', '--content-file', self.content('overwrite'), code=1)
        self.assertEqual((self.root / 'A.md').read_text(), updated)

    def test_links_exclude_code_and_preserve_anchors(self):
        self.note('Target.md', '# Heading\nblock ^id\n')
        self.note('Index.md', '[[Target#Heading|label]] ![[Target#^id]] [label](Target.md#Heading)\n'
                  '[reference]: <Target.md#Heading> "title"\n'
                  '`[[Target]]`\n````md\n[[Target]]\n```\n[[Target]]\n````\n'
                  '<!-- [[Target]] -->\n    [[Target]]\n\\[[Target]]\n')
        links = self.cli('backlinks', 'Target.md')['links']
        self.assertEqual([e['raw'] for e in links], ['Target#Heading', 'Target#^id', 'Target.md#Heading', 'Target.md#Heading'])

    def test_duplicate_basename_is_ambiguous_even_with_root_match(self):
        self.note('Target.md', 'root')
        self.note('Other/Target.md', 'other')
        self.note('Index.md', '[[Target]]')
        result = self.cli('links', 'Index.md')['links'][0]
        self.assertEqual(result['state'], 'ambiguous')
        self.cli('move', 'Target.md', 'Renamed.md', code=1)

    def test_move_refactors_inbound_and_outbound_preserving_bytes(self):
        sha = self.note('Old/Note.md', '---\r\naliases: [Example]\r\n---\r\n'
                        '[asset](../Assets/pic.png) [missing](missing.md#x) [[Target]]\r\n'
                        '[self](#Heading)\r\n`[[Old/Note]]`\r\n')
        self.note('Target.md', 'target')
        (self.root / 'Assets').mkdir()
        (self.root / 'Assets/pic.png').write_bytes(b'\x89PNG\x00')
        self.note('Index.md', '[[Old/Note#Heading|label]] ![[Old/Note#^block]]\n'
                  '[label](Old/Note.md#Heading "title")\n'
                  '[ref]: Old/Note.md#Heading\n')
        (self.root / 'Archive/Deep').mkdir(parents=True)
        before = (self.root / 'Index.md').read_bytes()
        preview = self.cli('move', 'Old/Note.md', 'Archive/Deep/Renamed.md')
        self.assertFalse(preview['applied'])
        self.assertEqual((self.root / 'Index.md').read_bytes(), before)
        self.cli('move', 'Old/Note.md', 'Archive/Deep/Renamed.md', '--expected-sha256', sha,
                 '--expected-plan-sha256', preview['plan_sha256'], '--apply')
        self.assertFalse((self.root / 'Old/Note.md').exists())
        moved = (self.root / 'Archive/Deep/Renamed.md').read_bytes()
        self.assertEqual(moved, b'---\r\naliases: [Example]\r\n---\r\n'
                         b'[asset](../../Assets/pic.png) [missing](../../Old/missing.md#x) [[Target]]\r\n'
                         b'[self](#Heading)\r\n`[[Old/Note]]`\r\n')
        self.assertEqual((self.root / 'Index.md').read_text(),
                         '[[Archive/Deep/Renamed#Heading|label]] ![[Archive/Deep/Renamed#^block]]\n'
                         '[label](Archive/Deep/Renamed.md#Heading "title")\n'
                         '[ref]: Archive/Deep/Renamed.md#Heading\n')
        self.assertEqual(len(self.cli('backlinks', 'Archive/Deep/Renamed.md')['links']), 5)

    def test_new_backlink_invalidates_authorized_move_plan(self):
        sha = self.note('Target.md', 'hello')
        preview = self.cli('move', 'Target.md', 'Renamed.md')
        self.note('New.md', '[[Target]]')
        result = self.cli('move', 'Target.md', 'Renamed.md', '--expected-sha256', sha,
                          '--expected-plan-sha256', preview['plan_sha256'], '--apply', code=1)
        self.assertIn('stale', result['error'])
        self.assertTrue((self.root / 'Target.md').exists())
        self.assertFalse((self.root / 'Renamed.md').exists())
        self.assertEqual((self.root / 'New.md').read_text(), '[[Target]]')

    def test_changed_backlink_invalidates_authorized_delete_plan(self):
        sha = self.note('Target.md', 'hello')
        self.note('Index.md', '[[Target]]')
        preview = self.cli('delete', 'Target.md', '--expected-sha256', sha)
        self.note('Index.md', '[[Target]] plus new user content')
        self.cli('delete', 'Target.md', '--expected-sha256', sha, '--expected-plan-sha256',
                 preview['plan_sha256'], '--apply', '--allow-referenced', code=1)
        self.assertTrue((self.root / 'Target.md').exists())

    def test_attachment_move_preserves_bytes_and_encoded_markdown_links(self):
        (self.root / 'Assets').mkdir()
        asset = self.root / 'Assets/image one.png'
        asset.write_bytes(b'\\x89PNG\\x00\\xff')
        self.note('Index.md', '![[Assets/image one.png]] ![image](Assets/image%20one.png)')
        preview = self.cli('move', 'Assets/image one.png', 'Assets/image two.png')
        self.cli('move', 'Assets/image one.png', 'Assets/image two.png',
                 '--expected-sha256', preview['sha256'], '--expected-plan-sha256',
                 preview['plan_sha256'], '--apply')
        self.assertEqual((self.root / 'Assets/image two.png').read_bytes(), b'\\x89PNG\\x00\\xff')
        self.assertEqual((self.root / 'Index.md').read_text(),
                         '![[Assets/image two.png]] ![image](Assets/image%20two.png)')

    def test_unresolved_relative_wikilink_refuses_move(self):
        self.note('Old/Note.md', '[[./Missing]]')
        self.cli('move', 'Old/Note.md', 'New.md', code=1)
        self.assertEqual((self.root / 'Old/Note.md').read_text(), '[[./Missing]]')

    def test_move_refuses_new_ambiguous_root_link(self):
        self.note('Source.md', 'hello')
        self.note('Other/Renamed.md', 'other')
        self.note('Index.md', '[[Source]]')
        self.cli('move', 'Source.md', 'Renamed.md', code=1)
        self.assertTrue((self.root / 'Source.md').exists())
        self.assertFalse((self.root / 'Renamed.md').exists())

    def test_move_preserves_other_links_made_ambiguous_by_destination(self):
        self.note('Source.md', 'hello')
        self.note('Other/Renamed.md', 'other')
        self.note('Index.md', '[[Renamed]]')
        preview = self.cli('move', 'Source.md', 'Renamed.md')
        self.cli('move', 'Source.md', 'Renamed.md', '--expected-sha256', preview['sha256'],
                 '--expected-plan-sha256', preview['plan_sha256'], '--apply')
        self.assertEqual((self.root / 'Index.md').read_text(), '[[Other/Renamed]]')
        self.assertEqual(self.cli('links', 'Index.md')['links'][0]['target'], 'Other/Renamed.md')

    def test_read_only_incoming_reference_blocks_move_without_mutation(self):
        self.note('Target.md', 'hello')
        self.note('Archive/Index.md', '[[Target]]')
        self.cli('--read-only', 'Archive', 'move', 'Target.md', 'Renamed.md', code=1)
        self.assertTrue((self.root / 'Target.md').exists())
        self.assertFalse((self.root / 'Renamed.md').exists())
        self.assertEqual((self.root / 'Archive/Index.md').read_text(), '[[Target]]')

    def test_restrictions_symlinks_and_traversal(self):
        self.note('Private/Secret.md', 'secret')
        self.note('.obsidian/Config.md', 'secret')
        self.note('Public.md', 'public')
        (self.root / 'Escape.md').symlink_to(self.base / 'outside.md')
        self.cli('read', 'Escape.md', code=1)
        self.cli('read', '../outside.md', code=1)
        self.cli('read', '.obsidian/Config.md', code=1)
        self.cli('--no-read', 'Private', 'read', 'Private/Secret.md', code=1)
        self.assertEqual(self.cli('--no-read', 'Private', 'list')['files'], ['Public.md'])
        self.cli('--no-read', 'Private', 'move', 'Public.md', 'New.md', code=1)
        self.assertFalse(self.cli('--no-read', 'Private', 'links')['complete'])

    def test_delete_requires_reference_override_and_fresh_hash(self):
        sha = self.note('Target.md', 'hello')
        self.note('Index.md', '[[Target]]')
        preview = self.cli('delete', 'Target.md', '--expected-sha256', sha)
        self.assertEqual(preview['references'][0]['source'], 'Index.md')
        self.cli('delete', 'Target.md', '--expected-sha256', sha,
                 '--expected-plan-sha256', preview['plan_sha256'], '--apply', code=1)
        self.assertTrue((self.root / 'Target.md').exists())
        self.cli('delete', 'Target.md', '--expected-sha256', sha,
                 '--expected-plan-sha256', preview['plan_sha256'], '--apply', '--allow-referenced')
        self.assertFalse((self.root / 'Target.md').exists())
        self.assertEqual(self.cli('links', 'Index.md')['links'][0]['state'], 'unresolved')

    def test_hooks_fail_closed_and_report_committed_local_write(self):
        log = self.base / 'hooks'
        self.env['OBSIDIAN_PRE_COMMAND'] = f"printf 'pre\\n' >> '{log}'"
        self.env['OBSIDIAN_POST_COMMAND'] = f"printf 'post\\n' >> '{log}'"
        self.cli('create', 'A.md', '--content-file', self.content('a'))
        read = self.cli('read', 'A.md')
        self.cli('write', 'A.md', '--content-file', self.content('a'), '--expected-sha256', read['sha256'])
        self.assertEqual(log.read_text(), 'pre\npost\npre\npre\n')
        self.env['OBSIDIAN_PRE_COMMAND'] = 'exit 7'
        self.cli('create', 'B.md', '--content-file', self.content('b'), code=1)
        self.assertFalse((self.root / 'B.md').exists())
        del self.env['OBSIDIAN_PRE_COMMAND']
        self.env['OBSIDIAN_POST_COMMAND'] = 'exit 9'
        result = self.cli('create', 'B.md', '--content-file', self.content('b'), code=2)
        self.assertTrue(result['saved_locally'])
        self.assertEqual(result['synchronization'], 'failed')
        self.assertEqual((self.root / 'B.md').read_text(), 'b')

    def test_rules_are_loaded_after_pre_hook_and_missing_rules_stop_writes(self):
        rules = self.base / 'rules.md'
        self.env['OBSIDIAN_VAULT_RULES'] = str(rules)
        self.cli('create', 'A.md', '--content-file', self.content('a'), code=1)
        self.assertFalse((self.root / 'A.md').exists())
        self.env['OBSIDIAN_PRE_COMMAND'] = f"printf 'Use Inbox\\n' > '{rules}'"
        self.assertEqual(self.cli('rules')['rules']['content'], 'Use Inbox\n')

    def test_cooperating_lock_blocks_second_operation(self):
        import fcntl
        directory = self.base / 'cache/openclaw-obsidian'
        directory.mkdir(parents=True)
        key = hashlib.sha256(str(self.root).encode()).hexdigest()
        with (directory / (key + '.lock')).open('a') as handle:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = self.cli('status', code=1)
            self.assertIn('cooperating', result['error'])


if __name__ == '__main__':
    unittest.main()
