#!/usr/bin/env python3
"""
Batch add word cards to Anki via AnkiConnect.
Supports Spanish with Chinese translations.

Usage:
  python batch_add.py --deck "综西单词::综西单词3" --model "西语" cards.txt

Input formats (cards.txt):
  1. TSV:   word<TAB>translation<TAB>example (optional)
  2. JSON:  [{"word":"...","meaning":"...","example":"...","tags":["..."]},...]
"""

import sys, json, csv, urllib.request, urllib.error

ANKI_CONNECT_URL = 'http://127.0.0.1:8765'
OK = '[OK]'
FAIL = '[FAIL]'

def anki(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params})
    req = urllib.request.Request(ANKI_CONNECT_URL, data=payload.encode('utf-8'),
                                 headers={'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode('utf-8'))
        if result.get('error'):
            raise RuntimeError("AnkiConnect error: " + result['error'])
        return result['result']
    except urllib.error.URLError as e:
        raise RuntimeError("Cannot connect to AnkiConnect. Is Anki running?\n" + str(e))

def resolve_model(model):
    names = anki('modelNames')
    if model in names:
        return model
    for n in names:
        if model.lower() in n.lower():
            return n
    raise RuntimeError("Model not found. Available: " + str(names))

def resolve_deck(deck):
    names = anki('deckNames')
    if deck in names:
        return deck
    for n in names:
        if deck.lower() in n.lower():
            return n
    raise RuntimeError("Deck not found. Available: " + str(names))

def add_card(deck, model, fields, tags=None):
    return anki('addNote', note={
        "deckName": deck, "modelName": model, "fields": fields,
        "options": {"allowDuplicate": False}, "tags": tags or []
    })

def parse_input(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    if content.startswith('[') or content.startswith('{'):
        data = json.loads(content)
        return data if isinstance(data, list) else [data]
    entries = []
    for row in csv.reader(content.split('\n'), delimiter='\t'):
        row = [c.strip() for c in row if c.strip()]
        if not row: continue
        e = {"word": row[0]}
        if len(row) >= 2: e["meaning"] = row[1]
        if len(row) >= 3: e["example"] = row[2]
        entries.append(e)
    return entries


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Batch add Anki cards')
    p.add_argument('input', help='Input file (tsv/json)')
    p.add_argument('--deck', '-d', default='Default')
    p.add_argument('--model', '-m', default='西语')
    p.add_argument('--field-word', default='单词')
    p.add_argument('--field-meaning', default='简明释义')
    p.add_argument('--field-example', default='例句1')
    p.add_argument('--field-example2', default='例句2')
    p.add_argument('--tags', '-t', default='auto')
    p.add_argument('--test', action='store_true', help='Dry run')
    args = p.parse_args()

    print('Resolving deck: ' + args.deck)
    deck = resolve_deck(args.deck)
    print('  -> ' + deck)
    print('Resolving model: ' + args.model)
    model = resolve_model(args.model)
    print('  -> ' + model)
    fields_list = anki('modelFieldNames', modelName=model)
    print('Fields: ' + str(fields_list))

    entries = parse_input(args.input)
    print('')
    print('Parsed ' + str(len(entries)) + ' card(s)')

    if args.test:
        for e in entries:
            print('  ' + e.get("word","?") + ' -> ' + e.get("meaning",""))
        sys.exit(0)

    ok = 0
    errs = []
    for i, entry in enumerate(entries):
        word = entry.get('word', '').strip()
        if not word: continue
        fields = {}
        for k, v in entry.items():
            if k == 'tags': continue
            if k == 'word': fields[args.field_word] = v
            elif k == 'meaning': fields[args.field_meaning] = v
            elif k == 'example': fields.setdefault(args.field_example, v)
            elif k == 'example_cn': fields.setdefault(args.field_example2, v)
            else: fields[k] = v
        for f in fields_list:
            if f not in fields: fields[f] = ''
        tags = entry.get('tags', [])
        if not tags and args.tags and args.tags != 'auto':
            tags = [t.strip() for t in args.tags.split(',')]
        elif not tags:
            tags = ['auto-import']
        try:
            nid = add_card(deck, model, fields, tags)
            ok += 1
            print(OK + ' ' + str(i+1) + '/' + str(len(entries)) + ' ' + word)
        except Exception as e:
            errs.append((word, str(e)))
            print(FAIL + ' ' + str(i+1) + '/' + str(len(entries)) + ' ' + word + ': ' + str(e))

    print('')
    print('Done: ' + str(ok) + ' added, ' + str(len(errs)) + ' errors')
    for w, e in errs:
        print('  ' + FAIL + ' ' + w + ': ' + e)
