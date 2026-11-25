#!/usr/bin/env python3
"""Read the public, regularly updated bias catalog. Python standard library only."""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

CATALOG_URL = 'https://tarot.catarchy.space/api/public/v1/catalog/'


def validate_catalog(value):
    if not isinstance(value, dict) or type(value.get('schemaVersion')) is not int or value['schemaVersion'] != 1:
        raise ValueError('Unsupported catalog schema; expected schemaVersion 1.')
    if value.get('language') != 'en' or not isinstance(value.get('catalogVersion'), str) or not value['catalogVersion']:
        raise ValueError('Catalog needs an English language tag and a catalogVersion.')
    if not isinstance(value.get('biases'), list):
        raise ValueError('Catalog biases must be a list.')
    ids = set()
    for entry in value['biases']:
        if not isinstance(entry, dict) or not all(isinstance(entry.get(key), str) and entry[key]
                                                for key in ('id', 'name', 'url')):
            raise ValueError('Each catalog entry needs an id, name and url.')
        if entry['id'] in ids or entry.get('family') not in ('bias', 'distortion', 'fallacy'):
            raise ValueError('Catalog contains a duplicate ID or unsupported family.')
        ids.add(entry['id'])
        for key in ('body', 'sources', 'related'):
            if not isinstance(entry.get(key), list) or not all(isinstance(item, str) for item in entry[key]):
                raise ValueError(f'Catalog {key} must be a list of strings.')
        if not isinstance(entry.get('examples'), list) or not all(
                isinstance(example, dict) and all(isinstance(example.get(key), str) for key in ('label', 'text'))
                for example in entry['examples']):
            raise ValueError('Catalog examples need label and text strings.')
    if any(related not in ids for entry in value['biases'] for related in entry['related']):
        raise ValueError('Catalog has an unknown related ID.')
    return value


def catalog(refresh=False, offline=False):
    url = os.environ.get('BIAS_LENS_CATALOG_URL', CATALOG_URL)
    cache_root = Path(os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache')) / 'bias-lens'
    cache_path = cache_root / (hashlib.sha256(url.encode()).hexdigest() + '.json')
    cached = None
    if cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text())
            validate_catalog(cached['catalog'])
            if not isinstance(cached.get('etag'), str):
                raise ValueError('Invalid cached ETag.')
        except (ValueError, KeyError, TypeError):
            if offline or not refresh:
                raise ValueError('Invalid catalog cache. Run index again to refresh it.') from None
            cached = None
    if offline or (cached and not refresh):
        if cached is None:
            raise ValueError('No cached catalog. Run index online first.')
        payload = cached['catalog']
    else:
        headers = {'Accept': 'application/json', 'User-Agent': 'bias-lens/1'}
        if cached and cached['etag']:
            headers['If-None-Match'] = cached['etag']
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:
                payload = validate_catalog(json.load(response))
                etag = response.headers.get('ETag', '')
        except HTTPError as error:
            error.close()
            if error.code != 304 or cached is None:
                raise ValueError(f'Catalog returned HTTP {error.code}. Check the endpoint or use index --offline with an existing cache.') from None
            payload, etag = cached['catalog'], cached['etag']
        except (URLError, TimeoutError) as error:
            raise ValueError('Cannot reach the catalog. Retry, or use index --offline with an existing cache.') from error
        cache_root.mkdir(parents=True, exist_ok=True)
        # Replace atomically so an interrupted write cannot destroy the previous snapshot.
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', dir=cache_root, delete=False) as output:
                temporary = Path(output.name)
                json.dump({'etag': etag, 'catalog': payload}, output, ensure_ascii=False)
            temporary.replace(cache_path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    print(f'Catalog version: {payload["catalogVersion"]}', file=sys.stderr)
    return {entry['id']: entry for entry in payload['biases']}


def first_sentence(text):
    text = text.strip()
    for match in re.finditer(r'[.!?](?=\s|$)', text):
        sentence = text[:match.end()]
        # Dotted abbreviations such as G.I. are part of the definition.
        if match.group() == '.' and re.search(r'\b(?:[A-Za-z]\.){2,}$', sentence):
            continue
        return sentence
    return text


def cmd_index(args):
    for ident, entry in sorted(catalog(refresh=True, offline=getattr(args, 'offline', False)).items()):
        definition = first_sentence(entry['body'][0]) if entry['body'] else 'Description pending.'
        related = ', '.join(entry.get('related') or [])
        family = entry.get('family', 'bias')
        tag = '' if family == 'bias' else f' [{family}]'
        print(f'{ident}{tag} | {definition}' + (f' | related: {related}' if related else ''))


def cmd_detail(args):
    entries = catalog(offline=True)
    unknown = [ident for ident in args.ids if ident not in entries]
    if unknown:
        raise ValueError('Unknown bias ID(s): ' + ', '.join(unknown))
    for ident in args.ids:
        entry = entries.get(ident)
        print(f'## {entry["name"]} ({ident})\n{entry["url"]}\n')
        print('\n\n'.join(entry['body']) + '\n')
        for example in entry.get('examples') or []:
            print(f'Example ({example["label"]}): {example["text"]}\n')
        if entry['sources']:
            print('Sources:\n' + '\n'.join(entry['sources']) + '\n')
        if entry.get('related'):
            print('Related: ' + ', '.join(entry['related']) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    index = sub.add_parser('index', help='Fetch a catalog snapshot; print id | definition | related.')
    index.add_argument('--offline', action='store_true', help='Explicitly reuse the cached snapshot.')
    index.set_defaults(func=cmd_index)
    p = sub.add_parser('detail', help='Full description, public examples and related IDs.')
    p.add_argument('ids', nargs='+')
    p.set_defaults(func=cmd_detail)
    args = parser.parse_args()
    try:
        args.func(args)
    except (ValueError, OSError) as error:
        print(f'bias-lens: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
