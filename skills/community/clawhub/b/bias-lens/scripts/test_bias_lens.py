"""Offline checks for the catalog index. No API or credentials required."""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import bias_lens


class IndexTests(unittest.TestCase):
    def test_first_sentence_preserves_dotted_abbreviations(self):
        cases = [
            ('The G.I. Joe fallacy is mistaking knowledge for change. Knowing is not doing.',
             'The G.I. Joe fallacy is mistaking knowledge for change.'),
            ('An example, e.g. a familiar name, can mislead. Check the evidence.',
             'An example, e.g. a familiar name, can mislead.'),
            ('  One sentence. Another sentence.  ', 'One sentence.'),
            ('A question? More text.', 'A question?'),
            ('An exclamation! More text.', 'An exclamation!'),
            ('No terminator', 'No terminator'),
            ('', ''),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(bias_lens.first_sentence(text), expected)

    def test_index_keeps_complete_definition_and_catalog_tags(self):
        entries = {
            'g-i-joe-fallacy': {
                'body': ['The G.I. Joe fallacy is mistaking knowledge for change. More detail.'],
                'related': ['bias-blind-spot'],
            },
            'ad-hominem': {
                'body': ['Ad hominem attacks the person instead of the argument. More detail.'],
                'family': 'fallacy',
            },
            'fallback': {'body': []},
        }
        output = io.StringIO()
        with patch.object(bias_lens, 'catalog', return_value=entries), redirect_stdout(output):
            bias_lens.cmd_index(None)
        self.assertEqual(output.getvalue().splitlines(), [
            'ad-hominem [fallacy] | Ad hominem attacks the person instead of the argument.',
            'fallback | Description pending.',
            'g-i-joe-fallacy | The G.I. Joe fallacy is mistaking knowledge for change. | related: bias-blind-spot',
        ])


class CatalogClientTests(unittest.TestCase):
    def setUp(self):
        import copy
        import json
        import tempfile
        import threading
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.payload = {
            'schemaVersion': 1, 'language': 'en', 'catalogVersion': 'synthetic-version-1',
            'biases': [{'id': 'test-bias', 'name': 'Test bias', 'family': 'bias',
                        'url': 'https://example.org/biases/test-bias/',
                        'body': ['Public definition. Qualification stays here.'],
                        'examples': [{'label': 'hypothetical', 'text': 'Public example.'}],
                        'sources': ['https://example.org/research'], 'related': []}],
        }
        self.original = copy.deepcopy(self.payload)
        self.requests = []
        self.status = 200
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                owner.requests.append(dict(self.headers))
                if owner.status != 200:
                    self.send_response(owner.status)
                    self.end_headers()
                elif self.headers.get('If-None-Match') == '"test-etag"':
                    self.send_response(304)
                    self.end_headers()
                else:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('ETag', '"test-etag"')
                    self.end_headers()
                    self.wfile.write(json.dumps(owner.payload).encode())

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)
        self.environment = patch.dict('os.environ', {
            'BIAS_LENS_CATALOG_URL': f'http://127.0.0.1:{self.server.server_port}/catalog/',
            'XDG_CACHE_HOME': self.directory.name,
        })
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def test_index_fetches_without_credentials_and_detail_pins_snapshot(self):
        import argparse
        output = io.StringIO()
        with redirect_stdout(output):
            bias_lens.cmd_index(argparse.Namespace(offline=False))
        self.assertIn('test-bias | Public definition.', output.getvalue())
        self.assertNotIn('Authorization', self.requests[0])
        self.assertNotIn('Cookie', self.requests[0])
        self.payload['biases'][0]['body'] = ['Changed after index.']
        output = io.StringIO()
        with redirect_stdout(output):
            bias_lens.cmd_detail(argparse.Namespace(ids=['test-bias']))
        self.assertIn('Qualification stays here.', output.getvalue())
        self.assertIn('https://example.org/research', output.getvalue())
        self.assertNotIn('Changed after index.', output.getvalue())
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(bias_lens.catalog(refresh=True)['test-bias']['body'],
                         self.original['biases'][0]['body'])
        self.assertEqual(self.requests[-1]['If-None-Match'], '"test-etag"')

    def test_errors_do_not_silently_reuse_stale_data(self):
        bias_lens.catalog(refresh=True)
        self.status = 503
        with self.assertRaisesRegex(ValueError, 'HTTP 503'):
            bias_lens.catalog(refresh=True)
        self.assertIn('test-bias', bias_lens.catalog(offline=True))

    def test_offline_requires_cache_and_unknown_ids_fail(self):
        import argparse
        with self.assertRaisesRegex(ValueError, 'No cached catalog'):
            bias_lens.catalog(offline=True)
        bias_lens.catalog(refresh=True)
        with self.assertRaisesRegex(ValueError, 'Unknown bias ID'):
            bias_lens.cmd_detail(argparse.Namespace(ids=['missing']))

    def test_bad_schema_does_not_overwrite_good_snapshot(self):
        bias_lens.catalog(refresh=True)
        self.payload['schemaVersion'] = 2
        # Force a response body rather than the test server's conditional 304.
        from pathlib import Path
        import json
        path = next(Path(self.directory.name).rglob('*.json'))
        cached = json.loads(path.read_text())
        cached['etag'] = ''
        path.write_text(json.dumps(cached))
        with self.assertRaisesRegex(ValueError, 'Unsupported catalog schema'):
            bias_lens.catalog(refresh=True)
        self.assertIn('test-bias', bias_lens.catalog(offline=True))

    def test_invalid_entries_are_rejected(self):
        import copy
        for key, invalid in [('body', 'not paragraphs'), ('family', 'unknown'),
                             ('examples', [{'text': 'Missing label'}]), ('related', ['missing'])]:
            payload = copy.deepcopy(self.original)
            payload['biases'][0][key] = invalid
            with self.subTest(key=key), self.assertRaises(ValueError):
                bias_lens.validate_catalog(payload)
        self.payload['biases'].append(self.payload['biases'][0])
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            bias_lens.validate_catalog(self.payload)


if __name__ == '__main__':
    unittest.main()
