#!/usr/bin/env python3
"""
English Phonetics Batch - Bulk IPA transcription tool for English words
Supports American English pronunciation (IPA)

Usage:
  python english_phonetics_batch.py input.txt output.txt [--format text|csv|markdown] [--check] [--delay MS] [--retries N]
  
Examples:
  python english_phonetics_batch.py words.txt output.txt
  python english_phonetics_batch.py corrupted.txt fixed.txt --check
  python english_phonetics_batch.py words.txt output.csv --format csv --delay 500
"""

import re
import time
import argparse
import requests
from typing import List, Dict, Optional, Tuple


class WordPhonetic:
    """Container for a word with its American IPA phonetic transcription"""
    def __init__(self, word: str, phonetic: str = "", part_of_speech: str = ""):
        self.word = word.strip().lower()
        self.phonetic = phonetic
        self.part_of_speech = part_of_speech
        self.is_valid = bool(phonetic)


class PhoneticsBatch:
    """
    Batch process English words to add American IPA phonetics.
    
    Features:
    - Automatic retry on network errors
    - Progress tracking with statistics
    - Rate limiting to avoid API blocks
    - Multiple output formats
    - Check and fix mode for corrupted phonetics
    """
    
    def __init__(self, delay_ms: int = 300, max_retries: int = 3):
        self.delay_ms = delay_ms
        self.max_retries = max_retries
        self.session = requests.Session()
        self.base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "retries": 0
        }
    
    def clean_word(self, word: str) -> str:
        """
        Clean up word input, remove existing phonetics, numbers, and extra characters.
        Handles common input formats where words are numbered or have extra markup.
        Also handles cases like "markn" where word is joined with part of speech abbreviation.
        """
        # Remove anything in brackets, parentheses, or slashes (existing phonetics)
        word = re.sub(r'[\/\[\(\{].*[\/\]\)\}]', '', word)
        # Remove leading numbers and dots (common in word lists: "1. apple")
        word = re.sub(r'^[\d\.\-\s]+', '', word)
        # Split word from joined part-of-speech: "markn" -> "mark", "immatureadj" -> "immature", "testv." -> "test"
        # Common abbreviations: n, v, adj, adv, vt, vi, etc.
        # Handle both "wordadj" and "wordadj." formats
        word = re.sub(r'([a-zA-Z]+)(n|v|adj|adv|vt|vi|pron|prep|conj|interj)\.?$', r'\1', word)
        # Also handle case where the entire line is "wordadj.  definition" (stop at first space/punctuation)
        word = re.sub(r'^([a-zA-Z]+)(n|v|adj|adv|vt|vi|pron|prep|conj|interj)\.?[\s。；，].*$', r'\1', word)
        # Remove remaining non-alphabetic characters except hyphens and apostrophes
        word = re.sub(r'[^a-zA-Z\-\']', '', word)
        return word.strip()
    
    def has_invalid_phonetic(self, phonetic: str) -> bool:
        """
        Check if existing phonetic is invalid.
        Common issues: contains ? from encoding errors, too short, empty.
        """
        if not phonetic or len(phonetic) < 2:
            return True
        return '?' in phonetic
    
    def extract_american_phonetic(self, data: List) -> Optional[str]:
        """
        Extract American English IPA phonetic from API response.
        Prefers American pronunciation if audio tag indicates US pronunciation.
        """
        for entry in data:
            # Top-level phonetic field
            if 'phonetic' in entry and entry['phonetic']:
                return entry['phonetic']
            
            # Check phonetics array - this is where audio metadata lives
            if 'phonetics' in entry:
                # First pass: look explicitly for American pronunciation
                for phonetic in entry['phonetics']:
                    if phonetic.get('audio') and 'us-' in phonetic['audio']:
                        if phonetic.get('text'):
                            return phonetic['text']
                
                # Second pass: take first available phonetic text
                for phonetic in entry['phonetics']:
                    if phonetic.get('text'):
                        return phonetic['text']
        
        return None
    
    def extract_first_part_of_speech(self, data: List) -> str:
        """Extract the most common meaning's part of speech."""
        for entry in data:
            if 'meanings' in entry and len(entry['meanings']) > 0:
                return entry['meanings'][0].get('partOfSpeech', '')
        return ''
    
    def fetch_phonetic(self, word: str, retry_count: int = 0) -> WordPhonetic:
        """
        Fetch phonetic for a single word from API.
        Includes automatic retry for network errors with exponential backoff.
        """
        cleaned_word = self.clean_word(word)
        if not cleaned_word:
            self.stats['failed'] += 1
            return WordPhonetic(word, "", "")
        
        try:
            response = self.session.get(
                f"{self.base_url}{cleaned_word}",
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                phonetic = self.extract_american_phonetic(data)
                pos = self.extract_first_part_of_speech(data)
                
                if phonetic:
                    # Ensure phonetic is properly wrapped in slashes
                    if not phonetic.startswith('/'):
                        phonetic = f'/{phonetic}/'
                    if not phonetic.endswith('/'):
                        phonetic = f'{phonetic}/'
                
                if phonetic:
                    self.stats['success'] += 1
                else:
                    self.stats['failed'] += 1
                
                return WordPhonetic(cleaned_word, phonetic or "", pos)
                
            elif response.status_code == 429 and retry_count < self.max_retries:
                # Rate limited - retry with backoff
                self.stats['retries'] += 1
                backoff_ms = self.delay_ms * (2 ** retry_count)
                print(f"  Rate limited for '{cleaned_word}', retrying in {backoff_ms}ms...")
                time.sleep(backoff_ms / 1000)
                return self.fetch_phonetic(word, retry_count + 1)
                
            else:
                print(f"  Warning: Failed to fetch '{cleaned_word}' - HTTP {response.status_code}")
                self.stats['failed'] += 1
                return WordPhonetic(cleaned_word, "", "")
                
        except Exception as e:
            if retry_count < self.max_retries:
                self.stats['retries'] += 1
                backoff_ms = self.delay_ms * (2 ** retry_count)
                print(f"  Error fetching '{cleaned_word}': {str(e)}, retrying...")
                time.sleep(backoff_ms / 1000)
                return self.fetch_phonetic(word, retry_count + 1)
            else:
                print(f"  Error fetching '{cleaned_word}' after {self.max_retries} retries: {str(e)}")
                self.stats['failed'] += 1
                return WordPhonetic(cleaned_word, "", "")
                
        finally:
            # Rate limiting between requests
            if self.delay_ms > 0:
                time.sleep(self.delay_ms / 1000)
    
    def process_words(self, words: List[str], show_progress: bool = True) -> List[WordPhonetic]:
        """
        Process a list of words, return results with progress tracking.
        """
        results = []
        total = len(words)
        self.stats['total'] = total
        
        for i, word in enumerate(words):
            word = word.strip()
            if not word or word.startswith('#'):
                continue
            
            if show_progress:
                print(f"[{i+1}/{total}] Processing: {word}")
            
            result = self.fetch_phonetic(word)
            results.append(result)
        
        return results
    
    def process_file(self, input_path: str, output_path: str, format: str = "text") -> int:
        """
        Process words from a text file (one word per line).
        Automatically skips comments and empty lines.
        """
        words = []
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Extract just the word from the beginning of the line
                parts = re.split(r'[\t\s]+', line, 1)
                words.append(parts[0])
        
        results = self.process_words(words)
        self.save_results(results, output_path, format)
        self.print_stats()
        
        return self.stats['failed']
    
    def check_existing_file(self, input_path: str, output_path: str, format: str = "text") -> int:
        """
        Check and fix existing file with phonetics.
        Re-fetches words that have invalid phonetics (containing ? or too short).
        Handles common formatting issues like "markn.标记；分数；目标/" where word and part-of-speech are joined.
        """
        results = []
        total_lines = 0
        needs_refetch = 0
        
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                total_lines += 1
                # Extract the word before any slashes, Chinese characters, or punctuation
                # Handles formats like: "markn.标记；分数；目标/" or "mark /mɑːrk/ n. ..."
                match = re.match(r'^([^/；，。\u4e00-\u9fff]+)', line)
                if match:
                    raw_word = match.group(1)
                    word = self.clean_word(raw_word)
                else:
                    parts = re.split(r'[\t\s]+', line, 1)
                    word = self.clean_word(parts[0]) if parts else ""
                
                if not word:
                    continue
                
                # Check if we need to refetch
                need_refetch = False
                # Look for existing phonetic between slashes
                phonetic_match = re.search(r'\/([^\/]+)\/', line)
                if not phonetic_match:
                    need_refetch = True
                else:
                    existing = f"/{phonetic_match.group(1)}/"
                    if self.has_invalid_phonetic(existing):
                        need_refetch = True
                
                if need_refetch:
                    needs_refetch += 1
                    print(f"[{needs_refetch}] Refetching: {word}")
                    result = self.fetch_phonetic(word)
                    results.append(result)
                else:
                    # Extract part of speech after phonetic
                    pos_match = re.search(r'\/[^\/]+\/\s*([a-z]+)\.?', line)
                    pos = pos_match.group(1) if pos_match else ""
                    results.append(WordPhonetic(word, existing, pos))
        
        self.stats['total'] = total_lines
        self.stats['failed'] = sum(1 for r in results if not r.is_valid)
        self.stats['success'] = len(results) - self.stats['failed']
        
        self.save_results(results, output_path, format)
        
        print(f"\nComplete! Checked {total_lines} words, {needs_refetch} needed refetch.")
        self.print_stats()
        
        return self.stats['failed']
    
    def save_results(self, results: List[WordPhonetic], output_path: str, format: str = "text"):
        """
        Save results to file in specified format.
        Supports: text, csv, markdown
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            if format == "csv":
                f.write("word,phonetic_american,part_of_speech,is_valid\n")
                for r in results:
                    phonetic = r.phonetic.replace('"', '""')
                    pos = r.part_of_speech.replace('"', '""')
                    f.write(f'"{r.word}","{phonetic}","{pos}",{r.is_valid}\n')
            
            elif format == "markdown":
                f.write("| Word | American IPA | Part of Speech |\n")
                f.write("|------|--------------|----------------|\n")
                for r in results:
                    f.write(f"| {r.word} | {r.phonetic} | {r.part_of_speech} |\n")
            
            else: # text format (default)
                for r in results:
                    if r.part_of_speech:
                        f.write(f"{r.word} {r.phonetic} {r.part_of_speech}\n")
                    else:
                        f.write(f"{r.word} {r.phonetic}\n")
        
        print(f"\nResults saved to {output_path}")
    
    def print_stats(self):
        """Print processing statistics summary."""
        print("\n" + "="*50)
        print(f"Processing Summary:")
        print(f"  Total words:    {self.stats['total']}")
        print(f"  Success:        {self.stats['success']}")
        print(f"  Failed:         {self.stats['failed']}")
        print(f"  Retries:        {self.stats['retries']}")
        if self.stats['total'] > 0:
            success_rate = (self.stats['success'] / self.stats['total']) * 100
            print(f"  Success rate:   {success_rate:.1f}%")
        print("="*50)


def main():
    """Command line interface with full argument parsing."""
    parser = argparse.ArgumentParser(
        description='Batch add American IPA phonetics to English word lists',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input', help='Input text file (one word per line)')
    parser.add_argument('output', help='Output file path')
    parser.add_argument(
        '--format',
        choices=['text', 'csv', 'markdown'],
        default='text',
        help='Output format'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check and fix existing file with invalid phonetics (fixes ? placeholders)'
    )
    parser.add_argument(
        '--delay',
        type=int,
        default=300,
        help='Delay between requests in milliseconds (increase for large lists)'
    )
    parser.add_argument(
        '--retries',
        type=int,
        default=3,
        help='Maximum retries for failed requests'
    )
    
    args = parser.parse_args()
    
    processor = PhoneticsBatch(delay_ms=args.delay, max_retries=args.retries)
    
    if args.check:
        failed = processor.check_existing_file(args.input, args.output, args.format)
    else:
        failed = processor.process_file(args.input, args.output, args.format)
    
    return failed


if __name__ == "__main__":
    exit(main())
