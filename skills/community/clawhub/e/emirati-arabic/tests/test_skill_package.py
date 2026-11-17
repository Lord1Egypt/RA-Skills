"""Packaging/privacy checks, not a linguistic fluency benchmark."""
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOWS_PATH_PATTERN = r'\b[A-Za-z]:[\\/]'

class SkillPackageTests(unittest.TestCase):
    def test_windows_path_detector_distinguishes_web_urls(self):
        self.assertIsNone(re.search(WINDOWS_PATH_PATTERN, 'https://example.invalid/skill'))
        self.assertIsNotNone(re.search(WINDOWS_PATH_PATTERN, 'Z' + ':/' + 'Users/example/file'))
    def test_frontmatter(self):
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        match = re.match(r'\A---\n(.*?)\n---(?:\n|\Z)', text, re.DOTALL)
        self.assertIsNotNone(match, 'Frontmatter needs opening and closing delimiter lines')
        front = match.group(1)
        for key in ('name', 'description', 'version', 'author', 'license', 'platforms'):
            self.assertRegex(front, rf'(?m)^{key}: .+')
        description = re.search(r'(?m)^description: (.+)$', front).group(1)
        self.assertLessEqual(len(description), 60)
        self.assertTrue(description.endswith('.'))
        self.assertIn('name: emirati-arabic', front)
        self.assertIn('license: MIT', front)
        self.assertIn('author: Binablan, Hermes Agent', front)

    def test_linked_skill_references_exist(self):
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        refs = set(re.findall(r'`(references/[^`]+\.md)`', text))
        self.assertEqual(refs, {'references/sources.md', 'references/examples.md',
                                'references/abu-dhabi.md', 'references/abu-dhabi-sources.md',
                                'references/abu-dhabi-examples.md', 'references/evaluation.md',
                                'references/owner-examples.md',
                                'references/conversation-behavior.md',
                                'references/conversation-evaluation.md'})
        for ref in refs:
            self.assertTrue((ROOT / ref).is_file(), ref)

    def test_readme_local_links(self):
        text = (ROOT / 'README.md').read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if not target.startswith(('http:', 'https:', '#')):
                self.assertTrue((ROOT / target).is_file(), target)

    def test_no_private_material_in_publishable_files(self):
        # Character classes keep literal detectors from matching their own source.
        # Detect home paths rather than embedding a particular machine username.
        forbidden = [WINDOWS_PATH_PATTERN, r'(?i)\blocal[-][a-f0-9]{5,}\b',
                     r'(?i)/(?:home|users)/[^/\s]+', r'(?i)tail[a-z0-9]+\.ts\.net',
                     r'(?i)conduit[:]//', r'(?i)gh[pousr]_[A-Za-z0-9]{12,}',
                     r'(?i)HERMES[_]HOME', '[ا]لعينة القديمة', '[ا]لعيّنة القديمة']
        excluded = {'.git', '__pycache__', '.cache', '.pytest_cache',
                    '.mypy_cache', '.ruff_cache', '.venv', 'venv'}
        for directory, directories, filenames in os.walk(ROOT):
            directories[:] = [name for name in directories if name not in excluded]
            for filename in filenames:
                path = Path(directory) / filename
                if filename == '.git' or path.is_symlink():
                    continue
                # Include extensionless files, config, and Python tests themselves.
                text = path.read_text(encoding='utf-8', errors='replace')
                for pattern in forbidden:
                    self.assertIsNone(re.search(pattern, text),
                                      f'{path.relative_to(ROOT)}: {pattern}')

    def test_no_source_book_or_media(self):
        forbidden = {'.pdf', '.png', '.jpg', '.jpeg', '.zip', '.env'}
        for path in ROOT.rglob('*'):
            if '.git' in path.relative_to(ROOT).parts:
                continue
            if path.is_file():
                self.assertNotIn(path.suffix.lower(), forbidden)
                self.assertFalse(path.name.startswith('.env'))

    def test_scope_and_license_boundaries(self):
        source = (ROOT / 'references/sources.md').read_text(encoding='utf-8')
        self.assertIn('| 49 |', source)
        self.assertIn('| 52 |', source)
        self.assertIn('not distributed', source)
        self.assertIn('not** been reviewed', source)
        notice = (ROOT / 'THIRD_PARTY_NOTICES.md').read_text(encoding='utf-8')
        self.assertIn('not covered', notice)
        self.assertIn('not included', notice)
        self.assertIn('Copyright (c) 2026 Binablan', (ROOT / 'LICENSE').read_text())

if __name__ == '__main__':
    unittest.main()
