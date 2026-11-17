"""CLI-level coverage of discovery, targeted editing, imports, and refactors."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / 'scripts' / 'vault.py'


class CapabilitiesCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'vault'
        self.root.mkdir()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith('OBSIDIAN_')}
        self.env.update(OBSIDIAN_VAULT_PATH=str(self.root), XDG_CACHE_HOME=str(self.base / 'cache'))

    def file(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        data = content.encode('utf-8') if isinstance(content, str) else content
        path.write_bytes(data)
        return hashlib.sha256(data).hexdigest()

    def input(self, name, content):
        path = self.base / name
        path.write_bytes(content.encode('utf-8') if isinstance(content, str) else content)
        return str(path)

    def cli(self, *args, code=0):
        result = subprocess.run([sys.executable, str(HELPER), *args], env=self.env,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def apply_move(self, source, destination, preview):
        return self.cli('move', source, destination, '--expected-sha256', preview['sha256'],
                        '--expected-plan-sha256', preview['plan_sha256'], '--apply')

    def apply_anchor(self, path, old, new, preview, code=0):
        return self.cli('refactor-anchor', path, '--old-anchor', old, '--new-anchor', new,
                        '--expected-sha256', preview['sha256'], '--expected-plan-sha256',
                        preview['plan_sha256'], '--apply', code=code)

    def test_listing_discovers_directories_and_checks_real_emptiness(self):
        self.file('Projects/Note.md', 'hello')
        (self.root / 'Projects/Empty').mkdir()
        self.file('Hidden/.keep', '')
        (self.root / 'Protected/.obsidian').mkdir(parents=True)
        outside = self.base / 'outside'
        outside.mkdir()
        (self.root / 'Linked/').mkdir()
        (self.root / 'Linked/child').symlink_to(outside, target_is_directory=True)
        self.file('Private/Secret.md', 'secret')
        (self.root / 'Alias').symlink_to(outside, target_is_directory=True)
        result = self.cli('--no-read', 'Private', 'list', '--type', 'all')
        self.assertEqual(result['files'], ['Hidden/.keep', 'Projects/Note.md'])
        self.assertEqual(result['directories'], ['Hidden', 'Linked', 'Projects', 'Projects/Empty', 'Protected'])
        self.assertEqual(self.cli('--no-read', 'Private', 'list', '--type', 'dirs', '--empty')['directories'],
                         ['Projects/Empty'])
        scoped = self.cli('list', '--under', 'Projects', '--type', 'all')
        self.assertEqual(scoped['files'], ['Projects/Note.md'])
        self.assertEqual(scoped['directories'], ['Projects/Empty'])
        self.assertEqual(self.cli('list', '--under', '.', '--type', 'dirs')['directories'],
                         ['Hidden', 'Linked', 'Private', 'Projects', 'Projects/Empty', 'Protected'])

    def test_scoped_discovery_does_not_read_outside_notes_but_resolves_outside_targets(self):
        self.file('Projects/Note.md', 'needle [[Target]] [target](../Target.md)')
        self.file('Target.md', b'\xff not UTF-8')
        self.file('Elsewhere/Broken.md', b'\xff')
        self.assertEqual(self.cli('search', 'needle', '--under', 'Projects')['matches'],
                         [{'path': 'Projects/Note.md', 'line': 1,
                           'text': 'needle [[Target]] [target](../Target.md)'}])
        edges = self.cli('links', '--under', 'Projects')['links']
        self.assertEqual([(e['source'], e['target']) for e in edges],
                         [('Projects/Note.md', 'Target.md'), ('Projects/Note.md', 'Target.md')])
        self.assertEqual(self.cli('links', 'Target.md', '--under', 'Projects')['links'], [])
        self.file('Elsewhere/Target.md', b'\xff')
        edges = self.cli('links', '--under', 'Projects')['links']
        self.assertEqual(edges[0]['state'], 'ambiguous')
        self.assertEqual(edges[1]['target'], 'Target.md')

    def test_scoped_discovery_cannot_bypass_path_restrictions(self):
        self.file('Private/Note.md', 'secret')
        (self.root / '.obsidian').mkdir()
        for command in (('list',), ('search', 'secret'), ('links',)):
            self.cli('--no-read', 'Private', *command, '--under', 'Private', code=1)
            self.cli(*command, '--under', '../outside', code=1)
            self.cli(*command, '--under', '.obsidian', code=1)
            self.cli(*command, '--under', 'Missing', code=1)
            self.cli(*command, '--under', 'Private/Note.md', code=1)

    @unittest.skipIf(os.geteuid() == 0, 'root bypasses directory read permissions')
    def test_discovery_fails_on_unreadable_scope_without_scanning_other_scopes(self):
        self.file('Allowed/Note.md', 'needle')
        self.file('Denied/Note.md', 'secret')
        denied = self.root / 'Denied'
        denied.chmod(0)
        self.addCleanup(denied.chmod, 0o700)
        self.cli('list', '--under', 'Denied', code=1)
        self.cli('list', '--type', 'all', code=1)
        self.assertEqual(self.cli('list', '--under', 'Allowed')['files'], ['Allowed/Note.md'])
        self.assertEqual(self.cli('search', 'needle', '--under', 'Allowed')['matches'],
                         [{'path': 'Allowed/Note.md', 'line': 1, 'text': 'needle'}])

    def test_append_and_replace_preserve_unrelated_bytes_and_require_fresh_hashes(self):
        original = b'---\r\naliases: [Example]\r\n---\r\n# Title\r\nbody\r\n'
        sha = self.file('Note.md', original)
        appended = b'\r\nextra\r\n'
        result = self.cli('append', 'Note.md', '--content-file', self.input('append.md', appended),
                          '--expected-sha256', sha)
        self.assertEqual((self.root / 'Note.md').read_bytes(), original + appended)
        self.cli('append', 'Note.md', '--content-file', self.input('stale.md', 'lost'),
                 '--expected-sha256', sha, code=1)
        replaced = self.cli('replace', 'Note.md', '--old-file', self.input('old.md', 'body'),
                            '--new-file', self.input('new.md', 'revised'), '--expected-sha256', result['sha256'])
        self.assertTrue(replaced['changed'])
        self.assertEqual((self.root / 'Note.md').read_bytes(), (original + appended).replace(b'body', b'revised'))

    def test_replace_refuses_missing_empty_and_overlapping_matches(self):
        sha = self.file('Note.md', 'aaa')
        new = self.input('new.md', 'replacement')
        for text in ('', 'absent', 'aa'):
            self.cli('replace', 'Note.md', '--old-file', self.input('old.md', text),
                     '--new-file', new, '--expected-sha256', sha, code=1)
            self.assertEqual((self.root / 'Note.md').read_text(), 'aaa')
        result = self.cli('replace', 'Note.md', '--old-file', self.input('old.md', 'aaa'),
                          '--new-file', self.input('new.md', ''), '--expected-sha256', sha)
        self.assertEqual((self.root / 'Note.md').read_bytes(), b'')
        self.assertTrue(result['changed'])

    def test_targeted_noops_skip_post_hook_but_stale_noops_fail(self):
        sha = self.file('Note.md', 'unchanged')
        self.env['OBSIDIAN_POST_COMMAND'] = 'exit 9'
        result = self.cli('append', 'Note.md', '--content-file', self.input('empty.md', ''),
                          '--expected-sha256', sha)
        self.assertFalse(result['changed'])
        result = self.cli('replace', 'Note.md', '--old-file', self.input('old.md', 'unchanged'),
                          '--new-file', self.input('new.md', 'unchanged'), '--expected-sha256', sha)
        self.assertFalse(result['changed'])
        self.file('Note.md', 'external update')
        self.cli('append', 'Note.md', '--content-file', self.input('empty.md', ''),
                 '--expected-sha256', sha, code=1)
        self.assertEqual((self.root / 'Note.md').read_text(), 'external update')

    def test_targeted_edits_obey_write_restrictions_and_file_types(self):
        sha = self.file('Archive/Note.md', 'hello')
        content = self.input('input.md', 'hello')
        for prefix in ('--read-only', '--no-read'):
            self.cli(prefix, 'Archive', 'append', 'Archive/Note.md', '--content-file', content,
                     '--expected-sha256', sha, code=1)
            self.cli(prefix, 'Archive', 'replace', 'Archive/Note.md', '--old-file', content,
                     '--new-file', content, '--expected-sha256', sha, code=1)
        binary_sha = self.file('Asset.txt', 'hello')
        self.cli('append', 'Asset.txt', '--content-file', content, '--expected-sha256', binary_sha, code=1)
        self.assertEqual((self.root / 'Archive/Note.md').read_text(), 'hello')

    def test_attachment_import_preserves_bytes_and_never_overwrites(self):
        (self.root / 'Attachments').mkdir()
        data = b'\x89PNG\x00\xff\r\n'
        source = self.input('external.png', data)
        self.cli('import-attachment', source, 'Attachments/image.png')
        self.assertEqual((self.root / 'Attachments/image.png').read_bytes(), data)
        self.assertEqual(Path(source).read_bytes(), data)
        self.cli('import-attachment', self.input('other.png', b'other'), 'Attachments/image.png', code=1)
        self.assertEqual((self.root / 'Attachments/image.png').read_bytes(), data)
        self.cli('import-attachment', source, 'Missing/image.png', code=1)
        self.cli('import-attachment', source, 'Attachments/Note.md', code=1)

    def test_attachment_import_cannot_bypass_source_or_destination_restrictions(self):
        self.file('Private/source.png', b'private')
        (self.root / 'Attachments').mkdir()
        source = str(self.root / 'Private/source.png')
        self.cli('--no-read', 'Private', 'import-attachment', source, 'Attachments/copy.png', code=1)
        self.cli('--read-only', 'Attachments', 'import-attachment', self.input('source.png', b'hi'),
                 'Attachments/copy.png', code=1)
        linked = self.base / 'linked.png'
        linked.symlink_to(Path(source))
        self.cli('import-attachment', str(linked), 'Attachments/copy.png', code=1)
        self.cli('import-attachment', 'relative.png', 'Attachments/copy.png', code=1)
        self.cli('import-attachment', self.input('source.png', b'hi'), '../escape.png', code=1)
        self.assertFalse((self.root / 'Attachments/copy.png').exists())

    def test_new_mutations_report_post_hook_failures_after_committing(self):
        sha = self.file('Note.md', 'hello')
        (self.root / 'Attachments').mkdir()
        self.env['OBSIDIAN_POST_COMMAND'] = 'exit 9'
        result = self.cli('append', 'Note.md', '--content-file', self.input('extra.md', '!'),
                          '--expected-sha256', sha, code=2)
        self.assertTrue(result['saved_locally'])
        self.assertEqual((self.root / 'Note.md').read_text(), 'hello!')
        result = self.cli('import-attachment', self.input('asset.png', b'asset'), 'Attachments/asset.png', code=2)
        self.assertTrue(result['saved_locally'])
        self.assertEqual((self.root / 'Attachments/asset.png').read_bytes(), b'asset')

    def test_attachment_import_rejects_symlink_parent_and_protected_source(self):
        (self.root / 'Attachments').mkdir()
        source_dir = self.base / 'source-dir'
        source_dir.mkdir()
        (source_dir / 'asset.png').write_bytes(b'asset')
        (self.base / 'source-link').symlink_to(source_dir, target_is_directory=True)
        self.cli('import-attachment', str(self.base / 'source-link/asset.png'),
                 'Attachments/asset.png', code=1)
        self.file('.obsidian/config.bin', b'protected')
        self.cli('import-attachment', str(self.root / '.obsidian/config.bin'),
                 'Attachments/config.bin', code=1)
        self.assertEqual(list((self.root / 'Attachments').iterdir()), [])

    def test_all_new_mutations_abort_before_changes_on_pre_hook_failure(self):
        sha = self.file('Note.md', '# Old\n')
        (self.root / 'Attachments').mkdir()
        (self.root / 'Old').mkdir()
        self.env['OBSIDIAN_PRE_COMMAND'] = 'exit 7'
        self.cli('append', 'Note.md', '--content-file', self.input('append.txt', 'extra'),
                 '--expected-sha256', sha, code=1)
        self.cli('replace', 'Note.md', '--old-file', self.input('old.txt', 'Old'),
                 '--new-file', self.input('new.txt', 'New'), '--expected-sha256', sha, code=1)
        self.cli('import-attachment', self.input('asset.png', b'asset'), 'Attachments/asset.png', code=1)
        self.cli('refactor-anchor', 'Note.md', '--old-anchor', 'Old', '--new-anchor', 'New', code=1)
        self.cli('move', 'Old', 'Moved', code=1)
        self.assertEqual((self.root / 'Note.md').read_text(), '# Old\n')
        self.assertTrue((self.root / 'Old').is_dir())
        self.assertFalse((self.root / 'Moved').exists())
        self.assertFalse((self.root / 'Attachments/asset.png').exists())

    def test_heading_refactor_preserves_markers_and_updates_only_matching_anchors(self):
        original = '---\r\ntags: [example]\r\n---\r\n## Old title  ##\r\n'
        original += '[self](#Old%20title)\r\n`# Old title`\r\n'
        self.file('Target.md', original)
        self.file('Other.md', '# Old title\n')
        index = ('[[Target#Old title|label]] ![[Target#Old title]]\n'
                 '[label](Target.md#Old%20title "title")\n'
                 '[ref]: Target.md#Old%20title\n'
                 '[[Target#Other]] [[Other#Old title]]\n'
                 '```md\n[[Target#Old title]]\n```\n')
        self.file('Index.md', index)
        preview = self.cli('refactor-anchor', 'Target.md', '--old-anchor', 'Old title', '--new-anchor', 'New title')
        self.assertFalse(preview['applied'])
        self.assertEqual((self.root / 'Target.md').read_bytes(), original.encode())
        self.apply_anchor('Target.md', 'Old title', 'New title', preview)
        self.assertEqual((self.root / 'Target.md').read_bytes(),
                         original.replace('## Old title  ##', '## New title  ##').replace('#Old%20title', '#New%20title').encode())
        expected = index.replace('Target#Old title', 'Target#New title').replace('Target.md#Old%20title', 'Target.md#New%20title')
        # Code examples are intentionally unchanged.
        expected = expected.replace('```md\n[[Target#New title]]', '```md\n[[Target#Old title]]')
        self.assertEqual((self.root / 'Index.md').read_text(), expected)
        self.assertEqual((self.root / 'Other.md').read_text(), '# Old title\n')

    def test_block_refactor_preserves_other_ids_and_encoded_fragments(self):
        self.file('Target.md', 'paragraph ^old-id\n\n^standalone\n\n`^old-id`\n')
        self.file('Index.md', '![[Target#^old-id|label]] [block](Target.md#%5Eold-id) [[Target#^standalone]]\n')
        preview = self.cli('refactor-anchor', 'Target.md', '--old-anchor', '^old-id', '--new-anchor', '^new-id')
        self.apply_anchor('Target.md', '^old-id', '^new-id', preview)
        self.assertEqual((self.root / 'Target.md').read_text(), 'paragraph ^new-id\n\n^standalone\n\n`^old-id`\n')
        text = (self.root / 'Index.md').read_text()
        self.assertIn('Target#^new-id|label', text)
        self.assertTrue('Target.md#%5Enew-id' in text or 'Target.md#^new-id' in text)
        self.assertIn('Target#^standalone', text)

    def test_anchor_refactor_rejects_collisions_ambiguity_and_unsupported_definitions(self):
        examples = ('# Old\n# Old\n', '# Old\n# New\n', 'Old\n===\n', '```md\n# Old\n```\n', '# **Old**\n')
        for original in examples:
            with self.subTest(original=original):
                self.file('Target.md', original)
                self.cli('refactor-anchor', 'Target.md', '--old-anchor', 'Old', '--new-anchor', 'New', code=1)
                self.assertEqual((self.root / 'Target.md').read_text(), original)
        self.file('Target.md', '# Old\n')
        self.file('Other/Target.md', '# Old\n')
        self.file('Index.md', '[[Target#Old]]')
        self.cli('refactor-anchor', 'Target.md', '--old-anchor', 'Old', '--new-anchor', 'New', code=1)
        self.assertEqual((self.root / 'Target.md').read_text(), '# Old\n')

    def test_anchor_refactor_obeys_restrictions_and_preview_snapshot(self):
        self.file('Target.md', '# Old\n')
        self.file('Archive/Index.md', '[[Target#Old]]')
        self.cli('--read-only', 'Archive', 'refactor-anchor', 'Target.md', '--old-anchor', 'Old', '--new-anchor', 'New', code=1)
        self.cli('--no-read', 'Private', 'refactor-anchor', 'Target.md', '--old-anchor', 'Old', '--new-anchor', 'New', code=1)
        preview = self.cli('refactor-anchor', 'Target.md', '--old-anchor', 'Old', '--new-anchor', 'New')
        self.file('New.md', '[[Target#Old]]')
        self.apply_anchor('Target.md', 'Old', 'New', preview, code=1)
        self.assertEqual((self.root / 'Target.md').read_text(), '# Old\n')
        self.assertEqual((self.root / 'Archive/Index.md').read_text(), '[[Target#Old]]')

    def test_directory_move_preserves_assets_empty_dirs_and_link_meaning(self):
        self.file('Old/Sub/Note.md', '# Note\r\n[asset](../asset.png) [outside](../../Outside.md)\r\n'
                  '[missing](missing.md#Heading)\r\n[[Old/Sub/Note#Note|self]]\r\n')
        self.file('Old/asset.png', b'\x89PNG\x00\xff')
        (self.root / 'Old/Empty').mkdir()
        (self.root / 'Archive').mkdir()
        self.file('Outside.md', '# Outside\n')
        self.file('Index.md', '[[Old/Sub/Note#Note|label]] ![[Old/asset.png]] [note](Old/Sub/Note.md#Note)')
        preview = self.cli('move', 'Old', 'Archive/Moved')
        self.assertEqual(preview['source_type'], 'directory')
        self.assertTrue((self.root / 'Old/Empty').is_dir())
        self.assertFalse((self.root / 'Archive/Moved').exists())
        self.apply_move('Old', 'Archive/Moved', preview)
        self.assertFalse((self.root / 'Old').exists())
        self.assertTrue((self.root / 'Archive/Moved/Empty').is_dir())
        self.assertEqual((self.root / 'Archive/Moved/asset.png').read_bytes(), b'\x89PNG\x00\xff')
        self.assertEqual((self.root / 'Archive/Moved/Sub/Note.md').read_bytes(),
                         b'# Note\r\n[asset](../asset.png) [outside](../../../Outside.md)\r\n'
                         b'[missing](missing.md#Heading)\r\n[[Archive/Moved/Sub/Note#Note|self]]\r\n')
        self.assertEqual((self.root / 'Index.md').read_text(),
                         '[[Archive/Moved/Sub/Note#Note|label]] ![[Archive/Moved/asset.png]] '
                         '[note](Archive/Moved/Sub/Note.md#Note)')

    def test_directory_move_invalidates_plan_for_assets_or_empty_directory_changes(self):
        for change in ('asset', 'empty-directory'):
            with self.subTest(change=change):
                self.file('Old/Note.md', 'note')
                self.file('Old/asset.png', b'original')
                preview = self.cli('move', 'Old', 'Moved')
                if change == 'asset':
                    self.file('Old/asset.png', b'changed')
                else:
                    (self.root / 'Old/AddedEmpty').mkdir(exist_ok=True)
                self.cli('move', 'Old', 'Moved', '--expected-sha256', preview['sha256'],
                         '--expected-plan-sha256', preview['plan_sha256'], '--apply', code=1)
                self.assertTrue((self.root / 'Old').is_dir())
                self.assertFalse((self.root / 'Moved').exists())

    def test_directory_move_refuses_restricted_descendants_symlinks_and_self_moves(self):
        self.file('Old/Note.md', 'note')
        self.cli('move', 'Old', 'Old/Inside', code=1)
        self.cli('--read-only', 'Old/Note.md', 'move', 'Old', 'Moved', code=1)
        self.cli('--read-only', 'Moved/Note.md', 'move', 'Old', 'Moved', code=1)
        self.cli('--no-read', 'Private', 'move', 'Old', 'Moved', code=1)
        (self.root / 'Old/.git').mkdir()
        self.cli('move', 'Old', 'Moved', code=1)
        (self.root / 'Old/.git').rmdir()
        (self.root / 'Old/Link').symlink_to(self.base, target_is_directory=True)
        self.cli('move', 'Old', 'Moved', code=1)
        self.assertEqual((self.root / 'Old/Note.md').read_text(), 'note')
        self.assertFalse((self.root / 'Moved').exists())

    def test_directory_move_rejects_stale_plan_new_backlink_or_existing_destination(self):
        self.file('Old/Note.md', 'note')
        preview = self.cli('move', 'Old', 'Moved')
        self.file('Index.md', '[[Old/Note]]')
        self.cli('move', 'Old', 'Moved', '--expected-sha256', preview['sha256'],
                 '--expected-plan-sha256', preview['plan_sha256'], '--apply', code=1)
        (self.root / 'Moved').mkdir()
        self.cli('move', 'Old', 'Moved', code=1)
        self.assertEqual((self.root / 'Old/Note.md').read_text(), 'note')
        self.assertEqual((self.root / 'Index.md').read_text(), '[[Old/Note]]')

    def test_empty_directory_move_preserves_nested_empty_directories(self):
        (self.root / 'Old/Nested/Empty').mkdir(parents=True)
        preview = self.cli('move', 'Old', 'Moved')
        self.apply_move('Old', 'Moved', preview)
        self.assertFalse((self.root / 'Old').exists())
        self.assertTrue((self.root / 'Moved/Nested/Empty').is_dir())

    def test_directory_destination_preserves_unrelated_suffix_link(self):
        self.file('Old/Note.md', '# Moved note\n')
        self.file('Other/Moved/Note.md', '# Existing note\n')
        self.file('Index.md', '[[Moved/Note#Existing note|label]]')
        preview = self.cli('move', 'Old', 'Moved')
        self.apply_move('Old', 'Moved', preview)
        self.assertEqual((self.root / 'Index.md').read_text(), '[[Other/Moved/Note#Existing note|label]]')
        self.assertEqual(self.cli('links', 'Index.md')['links'][0]['target'], 'Other/Moved/Note.md')

    def test_anchor_and_directory_move_report_local_changes_after_post_failure(self):
        self.file('Target.md', '# Old\n')
        self.file('Index.md', '[[Target#Old]]')
        anchor = self.cli('refactor-anchor', 'Target.md', '--old-anchor', 'Old', '--new-anchor', 'New')
        self.env['OBSIDIAN_POST_COMMAND'] = 'exit 9'
        result = self.apply_anchor('Target.md', 'Old', 'New', anchor, code=2)
        self.assertTrue(result['saved_locally'])
        self.assertEqual((self.root / 'Target.md').read_text(), '# New\n')
        self.assertEqual((self.root / 'Index.md').read_text(), '[[Target#New]]')
        del self.env['OBSIDIAN_POST_COMMAND']
        self.file('Old/Note.md', 'note')
        move = self.cli('move', 'Old', 'Moved')
        self.env['OBSIDIAN_POST_COMMAND'] = 'exit 9'
        result = self.cli('move', 'Old', 'Moved', '--expected-sha256', move['sha256'],
                          '--expected-plan-sha256', move['plan_sha256'], '--apply', code=2)
        self.assertTrue(result['saved_locally'])
        self.assertFalse((self.root / 'Old').exists())
        self.assertEqual((self.root / 'Moved/Note.md').read_text(), 'note')

    def test_standalone_block_anchor_and_collision_checks(self):
        self.file('Target.md', '^old-id\n\nparagraph ^new-id\n')
        self.cli('refactor-anchor', 'Target.md', '--old-anchor', '^old-id', '--new-anchor', '^new-id', code=1)
        self.file('Index.md', '[[Target#^old-id]]')
        preview = self.cli('refactor-anchor', 'Target.md', '--old-anchor', '^old-id', '--new-anchor', '^unique')
        self.apply_anchor('Target.md', '^old-id', '^unique', preview)
        self.assertEqual((self.root / 'Target.md').read_text(), '^unique\n\nparagraph ^new-id\n')
        self.assertEqual((self.root / 'Index.md').read_text(), '[[Target#^unique]]')


if __name__ == '__main__':
    unittest.main()
