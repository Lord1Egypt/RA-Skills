"""Offline regressions for release 1.2.0 data-integrity boundaries."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from unittest.mock import patch
import verify_references as v


class ReleaseBoundaries(unittest.TestCase):
    def setUp(self):
        self.entry = v.ReferenceEntry(1, 'Smith JA. DNA methylation in human embryos. Journal A. 2024.', 'ama', 'DNA methylation in human embryos', ['Smith JA'], 'Journal A', '2024', '', '', '', '')

    def run_cli(self, source, output, *args):
        return subprocess.run([sys.executable, str(Path(v.__file__)), str(source), '--input-mode', 'records', '--pipeline', 'format-only', '--output-dir', str(output), *args], capture_output=True, text=True)

    def write_source(self, path, entries=None):
        text = json.dumps(v.render_normalized_records(entries or [self.entry]))
        path.write_text(text)
        return text

    def test_duplicate_indices_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); source = root / 'input.json'; output = root / 'out'
            original = self.write_source(source, [self.entry, replace(self.entry, title='A different article title')])
            result = self.run_cli(source, output)
            self.assertEqual(result.returncode, 2)
            self.assertIn('Duplicate reference index', result.stderr)
            self.assertFalse(output.exists())
            self.assertEqual(source.read_text(), original)

    def test_source_collision_preserves_bytes_for_all_cleanup_modes(self):
        for cleanup in ('all', 'none', 'machine_records'):
            with self.subTest(cleanup=cleanup), tempfile.TemporaryDirectory() as td:
                root = Path(td); source = root / 'reference-normalized-records.json'
                original = self.write_source(source)
                result = self.run_cli(source, root, '--cleanup-process-files', cleanup)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(source.read_text(), original)
                self.assertEqual(list(root.iterdir()), [source])

    def test_detail_output_cannot_overwrite_input_or_other_output(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); source = root / 'input.json'; output = root / 'out'
            original = self.write_source(source)
            for target in (source, output / 'reference-audit-summary.md'):
                with self.subTest(target=target):
                    result = self.run_cli(source, output, '--output', str(target))
                    self.assertEqual(result.returncode, 2)
                    self.assertFalse(output.exists())
                    self.assertEqual(source.read_text(), original)

    def test_symlinks_and_hardlinks_cannot_bypass_source_protection(self):
        for link_type in ('symlink', 'hardlink'):
            with self.subTest(link_type=link_type), tempfile.TemporaryDirectory() as td:
                root = Path(td); source = root / 'input.json'; output = root / 'out'; output.mkdir()
                original = self.write_source(source); target = output / 'reference-normalized-records.json'
                if link_type == 'symlink': target.symlink_to(source)
                else: os.link(source, target)
                result = self.run_cli(source, output, '--cleanup-process-files', 'all')
                self.assertEqual(result.returncode, 2)
                self.assertEqual(source.read_text(), original)
                self.assertTrue(target.exists())

    def test_prior_artifact_is_protected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); source = root / 'input.json'; prior = root / 'reference-audit.json'
            self.write_source(source); prior.write_text('{"results": []}')
            result = self.run_cli(source, root, '--reuse-results', str(prior), '--keep-process-json')
            self.assertEqual(result.returncode, 2)
            self.assertEqual(prior.read_text(), '{"results": []}')

    def test_formatted_only_detail_contains_every_reference(self):
        entries = [self.entry, replace(self.entry, index=2)]
        results = v.format_only_results(entries, 'ama')
        report = v.render_detail(results, v.format_consistency(entries))
        self.assertIn('| formatted_only | 2 |', report)
        self.assertIn('### 1.', report)
        self.assertIn('### 2.', report)

    def test_provider_failures_are_not_successful_empty_results(self):
        responses = {'crossref': {'message': {'items': []}}, 'openalex': {'results': []}, 'pubmed': {'esearchresult': {'idlist': []}}}
        for provider, response in responses.items():
            with self.subTest(provider=provider):
                client = v.ApiClient(email='')
                search = getattr(client, provider + '_search')
                with patch.object(client, 'get_json', side_effect=TimeoutError):
                    self.assertEqual(search(self.entry.title), [])
                key = (provider, v.normalize_text(self.entry.title)[:240])
                self.assertEqual(client.search_failures[key], 'TimeoutError')
                with patch.object(client, 'get_json', return_value=response) as request:
                    self.assertEqual(search(self.entry.title), [])
                    request.assert_called_once()
                self.assertNotIn(key, client.search_failures)

    def test_timeout_stays_unresolved_and_unusable(self):
        client = v.ApiClient(email='')
        result = v.first_round_classification(self.entry, None, 'ama', 'report-only', False)
        with patch.object(client, 'get_json', side_effect=TimeoutError):
            v.recover_by_title([self.entry], [result], client, 'ama', 'corroborate', 'corroborate', 'report-only', False)
        v.describe_result(result, self.entry, 'verify', 'strict', ['Crossref', 'PubMed', 'OpenAlex'])
        self.assertEqual(result.status, 'unresolved')
        self.assertFalse(result.usable)
        self.assertTrue(result.fixed_reference.startswith(self.entry.original))
        self.assertIn("不可用", result.fixed_reference)
        self.assertIn('TimeoutError', ' '.join(result.issues))

    def test_malformed_response_and_incomplete_pubmed_fetch_are_failures(self):
        client = v.ApiClient(email='')
        with patch.object(client, 'get_json', return_value={}):
            client.crossref_search(self.entry.title)
        self.assertTrue(client.search_failures)
        with patch.object(client, 'get_json', return_value={'esearchresult': {'idlist': ['123']}}), patch.object(client, 'fetch_pubmed_pmids', return_value={'123': None}):
            client.pubmed_search(self.entry.title)
        self.assertIn(('pubmed', v.normalize_text(self.entry.title)[:240]), client.search_failures)

    def test_completed_empty_search_retains_existing_policy(self):
        client = v.ApiClient(email='')
        result = v.first_round_classification(self.entry, None, 'ama', 'report-only', False)
        with patch.object(client, 'get_json', return_value={'message': {'items': []}}):
            v.recover_by_title([self.entry], [result], client, 'ama', 'off', 'off', 'report-only', False)
        self.assertEqual(result.status, 'total_fabrication')


if __name__ == '__main__':
    unittest.main()
