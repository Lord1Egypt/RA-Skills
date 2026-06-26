#!/usr/bin/env python3
"""
Gaokao English Vocabulary Data Generator

Generates vocab_data.js from a structured vocabulary source.
Demonstrates the data generation workflow including word/phrase classification,
mastery assignment, and JS output formatting.

Usage:
    python generate_vocab.py input.jsonl output_vocab_data.js

Input format (JSONL, one entry per line):
    Word:   {"w":"abandon","s":"vt.","m":"放弃","c":28,"v":"must","p":"əˈbændən"}
    Phrase: {"w":"a great deal of","s":"phr.","m":"大量的","c":15,"i":"normal"}
    Wrong:  {"w":"accommodate","s":"vt.","m":"容纳","c":22,"v":"145","e":true,"t":"易写成accomodate","p":"əˈkɒmədeɪt"}

Output format: var VOCAB = [...];
"""

import json
import sys
import os

def classify_word_level(count):
    """Classify a word into level 1-6 based on exam frequency count."""
    if count >= 40: return 1
    if count >= 20: return 2
    if count >= 10: return 3
    if count >= 5:  return 4
    if count >= 2:  return 5
    return 6

def classify_phrase_level(count):
    """Classify a phrase into level p1-p6 based on exam frequency count."""
    if count >= 20: return 'p1'
    if count >= 12: return 'p2'
    if count >= 8:  return 'p3'
    if count >= 5:  return 'p4'
    if count >= 3:  return 'p5'
    return 'p6'

def convert_entry(entry):
    """Convert raw input entry to the VOCAB data format."""
    if entry.get('s') == 'phr.':
        # Phrase format (flat)
        result = {
            'w': entry['w'],
            's': 'phr.',
            'm': entry.get('m', ''),
            'c': entry.get('c', 0),
            'i': entry.get('i', entry.get('v', 'normal'))
        }
        if entry.get('e'):
            result['e'] = True
            if entry.get('t'):
                result['t'] = entry['t']
        return result
    else:
        # Word format (d array)
        count = entry.get('c', 0)
        level = entry.get('l', classify_word_level(count))
        result = {
            'w': entry['w'],
            's': entry.get('s', ''),
            'd': [{'m': entry.get('m', ''), 'c': count}],
            'l': level,
            'v': entry.get('v', 'normal')
        }
        if entry.get('p'):
            result['p'] = entry['p']
        if entry.get('e'):
            result['e'] = True
            if entry.get('t'):
                result['t'] = entry['t']
        return result

def sort_key(item):
    """Sort: words before phrases, then by level, then by count desc, then alphabetically."""
    is_phrase = 1 if item.get('s') == 'phr.' else 0
    level = item.get('l', 6)
    word = item.get('w', '').lower()
    if item.get('s') == 'phr.':
        count = item.get('c', 0)
    else:
        count = max((d.get('c', 0) for d in item.get('d', [])), default=0)
    return (is_phrase, level, -count, word)

def generate(input_path, output_path):
    """Read input JSONL, convert, sort, and write vocab_data.js."""
    entries = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

    # Convert all entries
    vocab = [convert_entry(e) for e in entries]

    # Deduplicate by word
    seen = set()
    unique = []
    for item in vocab:
        key = item['w'].lower()
        if key not in seen:
            seen.add(key)
            unique.append(item)

    # Sort
    unique.sort(key=sort_key)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('var VOCAB = ')
        json.dump(unique, f, ensure_ascii=False, separators=(',', ':'))
        f.write(';\n')

    # Stats
    words = [v for v in unique if v.get('s') != 'phr.']
    phrases = [v for v in unique if v.get('s') == 'phr.']
    cnt_145 = sum(1 for v in unique if v.get('v') == '145' or v.get('i') == '145')
    cnt_wrong = sum(1 for v in unique if v.get('e'))

    print(f"Generated: {output_path}")
    print(f"  Total: {len(unique)} (Words: {len(words)}, Phrases: {len(phrases)})")
    print(f"  145-essential: {cnt_145}, Wrong-word: {cnt_wrong}")

    # Level distribution
    from collections import Counter
    levels = Counter()
    for v in unique:
        if v.get('s') == 'phr.':
            c = v.get('c', 0)
            levels[classify_phrase_level(c)] += 1
        else:
            levels[v.get('l', 6)] += 1
    print("  Level distribution:")
    for lv in [1,2,3,4,5,6,'p1','p2','p3','p4','p5','p6']:
        print(f"    {lv}: {levels.get(lv, 0)}")

    # Check empty levels
    empty = [lv for lv in [1,2,3,4,5,6,'p1','p2','p3','p4','p5','p6'] if levels.get(lv, 0) == 0]
    if empty:
        print(f"  WARNING: Empty levels: {empty}")
    else:
        print("  All 12 levels are non-empty!")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python generate_vocab.py <input.jsonl> <output.js>")
        sys.exit(1)
    generate(sys.argv[1], sys.argv[2])
