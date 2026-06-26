#!/usr/bin/env python3
"""Bootstrap a lightweight domain ontology for abstract writing."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LEXICON_PATH = ROOT / 'assets' / 'lexeme_types.json'


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-') or 'domain'


def load_lexicon() -> dict:
    return json.loads(LEXICON_PATH.read_text(encoding='utf-8'))


def classify_term(term: str, lexicon: dict) -> str:
    low = term.strip().lower()
    head = low.split()[-1]
    noun_types = lexicon['noun_types']
    if head in noun_types:
        return noun_types[head][0]
    if any(token in low for token in ['rule', 'constraint', 'budget', 'regulation']):
        return 'constraint'
    if any(token in low for token in ['task', 'mission', 'goal', 'workflow']):
        return 'task'
    if any(token in low for token in ['accuracy', 'latency', 'robustness', 'continuity', 'quality', 'rate']):
        return 'metric'
    if low.endswith('tion') or low.endswith('ing') or low.endswith('ment'):
        return 'process'
    if low.endswith('ity') or low.endswith('ness'):
        return 'quality'
    if any(token in low for token in ['model', 'framework', 'system', 'architecture', 'ontology', 'chain', 'network']):
        return 'artifact'
    return 'artifact'


def build_seed(domain: str, terms: list[str], lexicon: dict) -> dict:
    entities = []
    for term in terms:
        entity_type = classify_term(term, lexicon)
        entities.append({
            'id': slugify(term),
            'label': term,
            'type': entity_type,
        })

    relations = [
        {'predicate': 'enables', 'domain': 'artifact', 'range': 'task'},
        {'predicate': 'constrains', 'domain': 'constraint', 'range': 'task'},
        {'predicate': 'implemented_by', 'domain': 'artifact', 'range': 'process'},
        {'predicate': 'measured_by', 'domain': 'artifact', 'range': 'metric'},
        {'predicate': 'affects', 'domain': 'constraint', 'range': 'quality'},
    ]

    return {
        'domain': domain,
        'namespace': f'http://example.org/{slugify(domain)}#',
        'upper_types': ['quantity', 'quality', 'process', 'artifact', 'capability', 'relation', 'task', 'constraint', 'metric'],
        'entities': entities,
        'relations': relations,
    }


def to_turtle(seed: dict) -> str:
    ns = seed['namespace']
    lines = [
        f'@prefix : <{ns}> .',
        '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .',
        '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .',
        '',
    ]
    for upper in seed['upper_types']:
        class_name = upper[0].upper() + upper[1:]
        lines.append(f':{class_name} a rdfs:Class .')

    lines.append('')
    for entity in seed['entities']:
        class_name = entity['type'][0].upper() + entity['type'][1:]
        lines.append(f':{entity["id"]} a :{class_name} ; rdfs:label "{entity["label"]}" .')

    lines.append('')
    for rel in seed['relations']:
        lines.append(f':{rel["predicate"]} a rdf:Property .')

    return '\n'.join(lines) + '\n'


def download_ontology(url: str, outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    parsed = urlparse(url)
    filename = Path(parsed.path).name or 'downloaded_ontology.owl'
    destination = outdir / filename
    urllib.request.urlretrieve(url, destination)
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description='Bootstrap or download a lightweight ontology.')
    parser.add_argument('--domain', default='research-domain', help='Domain name for the local ontology seed.')
    parser.add_argument('--terms', default='', help='Comma-separated term list for the local ontology seed.')
    parser.add_argument('--terms-file', help='Optional text file with one term per line.')
    parser.add_argument('--download-url', help='Optional URL of a public ontology file to download.')
    parser.add_argument('--outdir', required=True, help='Output directory.')
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if args.download_url:
        downloaded = download_ontology(args.download_url, outdir)
        print(f'downloaded: {downloaded}')

    terms: list[str] = []
    if args.terms:
        terms.extend([item.strip() for item in args.terms.split(',') if item.strip()])
    if args.terms_file:
        file_terms = [line.strip() for line in Path(args.terms_file).read_text(encoding='utf-8').splitlines() if line.strip()]
        terms.extend(file_terms)

    if terms:
        lexicon = load_lexicon()
        seed = build_seed(args.domain, terms, lexicon)
        json_path = outdir / 'ontology_seed.json'
        ttl_path = outdir / 'ontology_seed.ttl'
        json_path.write_text(json.dumps(seed, indent=2, ensure_ascii=False), encoding='utf-8')
        ttl_path.write_text(to_turtle(seed), encoding='utf-8')
        print(f'wrote: {json_path}')
        print(f'wrote: {ttl_path}')
    elif not args.download_url:
        raise SystemExit('provide --terms, --terms-file, or --download-url')


if __name__ == '__main__':
    main()
