#!/usr/bin/env python3
"""
Cohere Command A Translate — State-of-the-art neural machine translation for 23 languages.

Usage:
    # Direct text (passes through agent context — wastes tokens)
    python3 translate.py "Hello, how are you?" --to ja

    # ✅ File-to-file (bypasses agent entirely — ZERO agent tokens)
    python3 translate.py --file input.txt --to ja --output translated.txt

    # Read from stdin
    cat input.txt | python3 translate.py --to ja

Setup:
    export COHERE_API_KEY="your-api-key"   # required

Supported languages (23):
    en, ja, zh, ko, fr, de, es, it, pt, ar, ru, pl, tr,
    vi, nl, cs, id, uk, ro, el, hi, he, fa

Model: command-a-translate-08-2025 (111B params, 8K input / 8K output)
Pricing: Free for trial API keys (1,000 calls/month, 20 req/min)
API key: https://dashboard.cohere.com/api-keys
"""

import sys
import json
import subprocess
import argparse
import os
import time
import re

API_URL = "https://api.cohere.ai/v2/chat"
MODEL = "command-a-translate-08-2025"

LANGUAGES = {
    "en": "English", "ja": "Japanese", "zh": "Chinese", "ko": "Korean",
    "fr": "French", "de": "German", "es": "Spanish", "it": "Italian",
    "pt": "Portuguese", "ar": "Arabic", "ru": "Russian", "pl": "Polish",
    "tr": "Turkish", "vi": "Vietnamese", "nl": "Dutch", "cs": "Czech",
    "id": "Indonesian", "uk": "Ukrainian", "ro": "Romanian", "el": "Greek",
    "hi": "Hindi", "he": "Hebrew", "fa": "Persian",
}

# ── chunking ──────────────────────────────────────────────
#
# Model: 8K input + 8K output tokens.
# Target: 6000 total tokens (3000 input, 3000 output) per chunk.
#
# Chunk size depends on the DENSER of source+target scripts:
#   Sparse      (~4.0 chars/token): Latin, Cyrillic, Greek
#   Dense       (~2.5 chars/token): Arabic, Hebrew, Devanagari, Thai
#   Very dense  (~1.5 chars/token): CJK, Hangul
#
# Formula: max_chars = 3000 × chars_per_token(denser_script)

TOTAL_TOKEN_BUDGET = 6000
INPUT_TOKEN_BUDGET = TOTAL_TOKEN_BUDGET // 2  # 3000

# chars-per-token estimates (conservative)
_CHARS_PER_TOKEN = {'sparse': 4.0, 'dense': 2.5, 'very_dense': 1.5}

# Language code → density tier (for target language, since we can't scan it yet)
_LANG_DENSITY = {}
for _code in ['en','fr','de','es','it','pt','ru','pl','tr','vi','nl','cs','id','uk','ro','el']:
    _LANG_DENSITY[_code] = 'sparse'
for _code in ['ar','he','hi','fa']:
    _LANG_DENSITY[_code] = 'dense'
for _code in ['ja','zh','ko']:
    _LANG_DENSITY[_code] = 'very_dense'

# Unicode ranges for token-dense scripts
_DENSE_SCRIPTS = [
    (0x0590, 0x05FF),   # Hebrew
    (0x0600, 0x06FF),   # Arabic
    (0x0750, 0x077F),   # Arabic Supplement
    (0x0900, 0x097F),   # Devanagari (Hindi, Marathi, Nepali, Sanskrit)
    (0x0980, 0x09FF),   # Bengali
    (0x0A00, 0x0A7F),   # Gurmukhi (Punjabi)
    (0x0A80, 0x0AFF),   # Gujarati
    (0x0B00, 0x0B7F),   # Oriya
    (0x0B80, 0x0BFF),   # Tamil
    (0x0C00, 0x0C7F),   # Telugu
    (0x0C80, 0x0CFF),   # Kannada
    (0x0D00, 0x0D7F),   # Malayalam
    (0x0E00, 0x0E7F),   # Thai
    (0xFB50, 0xFDFF),   # Arabic Presentation Forms-A
    (0xFE70, 0xFEFF),   # Arabic Presentation Forms-B
]

_VERY_DENSE_SCRIPTS = [
    (0x4E00, 0x9FFF),   # CJK Unified Ideographs
    (0x3040, 0x309F),   # Hiragana
    (0x30A0, 0x30FF),   # Katakana
    (0xAC00, 0xD7AF),   # Hangul Syllables
]

def _count_script_chars(text, ranges):
    """Count characters falling within given Unicode ranges."""
    return sum(1 for c in text 
               if any(lo <= ord(c) <= hi for lo, hi in ranges))

def _script_density(text):
    """Return 'sparse', 'dense', or 'very_dense' based on dominant script."""
    total = len(text)
    if not total:
        return 'sparse'
    vd = _count_script_chars(text, _VERY_DENSE_SCRIPTS) / total
    if vd > 0.3:
        return 'very_dense'
    d = _count_script_chars(text, _DENSE_SCRIPTS) / total
    if d > 0.3:
        return 'dense'
    return 'sparse'

# ~33-50% of 8K token window, adjusted by script density
# Replaced by dynamic calculation in chunk_text() below
def _lang_density(code):
    """Return density tier for a language code."""
    return _LANG_DENSITY.get(code, 'sparse')

def _max_density(a, b):
    """Return the denser of two density tiers."""
    order = {'sparse': 0, 'dense': 1, 'very_dense': 2}
    return a if order[a] >= order[b] else b

def chunk_text(text, target_lang=None, threshold=0.8):
    """Split text at natural boundaries, targeting ~3000 input tokens.
    
    Uses the DENSER of source+target scripts for safety:
      EN→JA: JA is very_dense (1.5) → 3000×1.5 = 4500 chars/chunk
      JA→EN: JA is very_dense (1.5) → 3000×1.5 = 4500 chars/chunk
      EN→FR: both sparse (4.0) → 3000×4.0 = 12000 → capped at 8000 chars
      AR→HE: both dense (2.5)  → 3000×2.5 = 7500 chars/chunk
    """
    src_density = _script_density(text)
    tgt_density = _lang_density(target_lang) if target_lang else src_density
    effective = _max_density(src_density, tgt_density)
    cpt = _CHARS_PER_TOKEN[effective]
    max_chars = min(int(INPUT_TOKEN_BUDGET * cpt), 8000)
    return _chunk_by_chars(text, max_chars=max_chars, threshold=threshold)

def _chunk_by_chars(text, max_chars=3000, threshold=0.8):
    """Split by characters, preferring natural boundaries.
    
    For all languages. No word-counting — character-based with sentence-aware
    separators works for both space-delimited and CJK text.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunk = text[start:end]
        
        if end == len(text) or len(chunk) < max_chars * threshold:
            chunks.append(chunk.strip())
            break
        
        # Find natural breaking point (paragraph → sentence → clause)
        split_point = None
        for sep in ["\n\n", "\n", ". ", "。", "? ", "？", "! ", "！", ".\n", "。\n", ") ", "）", "」"]:
            idx = chunk.rfind(sep)
            if idx != -1 and idx >= len(chunk) * threshold:
                split_point = idx + len(sep)
                break
        
        if split_point:
            chunks.append(chunk[:split_point].strip())
            start = start + split_point
        else:
            chunks.append(chunk.strip())
            start = end
    return chunks


# ── API call ───────────────────────────────────────────────

def _call_api(payload, api_key):
    """Single API call with retry on rate limit."""
    max_retries = 3
    for attempt in range(max_retries):
        result = subprocess.run(
            ["curl", "-s", "--request", "POST", API_URL,
             "--header", "accept: application/json",
             "--header", "content-type: application/json",
             "--header", f"Authorization: bearer {api_key}",
             "--data", json.dumps(payload)],
            capture_output=True, text=True, timeout=120
        )
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"error": f"Invalid JSON: {result.stdout[:200]}"}
        
        err_msg = str(data).lower()
        if "limit" in err_msg and "rate" in err_msg:
            wait = 65 if attempt == 0 else 120
            print(f"  ⏳ Rate limited — waiting {wait}s...", file=sys.stderr, flush=True)
            time.sleep(wait)
            continue
        
        if "error" in data:
            return {"error": "API_ERROR", "detail": str(data)[:300]}
        
        try:
            content = data["message"]["content"]
            text = content[0]["text"] if isinstance(content, list) else content["text"]
            usage = data.get("usage", {}).get("billed_units", {})
            return {
                "text": text,
                "tokens_in": usage.get("input_tokens", 0),
                "tokens_out": usage.get("output_tokens", 0),
                "finish_reason": data.get("finish_reason", "unknown"),
            }
        except (KeyError, IndexError, TypeError) as e:
            return {"error": f"Response format error: {e}", "raw": str(data)[:300]}
    
    return {"error": "RATE_LIMITED", "detail": "Max retries exhausted"}


# ── translate functions ────────────────────────────────────

def translate(text, target_lang="en", temperature=0.3, max_tokens=4000,
              system_prompt=None, cohere_key=None):
    """Translate a single text chunk."""
    api_key = cohere_key or os.environ.get("COHERE_API_KEY")
    if not api_key:
        return {"error": "COHERE_API_KEY not set."}

    lang_name = LANGUAGES.get(target_lang, target_lang)

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({
        "role": "user",
        "content": f"Translate everything that follows into {lang_name}:\n\n{text}"
    })

    return _call_api({
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }, api_key)

def translate_file(filepath, target_lang="en", output=None,
                   temperature=0.3, max_tokens=4000, system_prompt=None,
                   cohere_key=None, verbose=True):
    """
    Translate a file directly (bypasses agent context window).
    
    For small files: single API call.
    For large files: automatic chunking with rate-limit awareness.
    
    Args:
        filepath: Path to input file (or '-' for stdin)
        target_lang: Target language code
        output: Path to output file (or None for stdout)
        temperature: 0.1-1.0
        max_tokens: Per-chunk max tokens
        system_prompt: Optional system message
        cohere_key: API key
        verbose: Print progress to stderr
    """
    # Read input
    if filepath == "-":
        text = sys.stdin.read()
    else:
        if not os.path.exists(filepath):
            return {"error": f"File not found: {filepath}"}
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    
    if not text.strip():
        return {"error": "Input is empty"}
    
    # Chunk if needed (>~3000 chars for safety)
    if len(text) > 3000:
        chunks = chunk_text(text, target_lang=target_lang)
        if verbose:
            print(f"  📄 {len(text)} chars → {len(chunks)} chunks (auto-chunked)", file=sys.stderr, flush=True)
    else:
        chunks = [text]
    
    # Translate chunks
    results = []
    total_in = total_out = 0
    call_count = 0
    
    for i, chunk in enumerate(chunks):
        # Rate limit: 20 req/min → 3.2s spacing; pause every 20 calls
        if call_count > 0:
            if call_count % 20 == 0:
                if verbose:
                    print(f"  ⏳ Rate limit pause (65s) after {call_count} calls...", file=sys.stderr, flush=True)
                time.sleep(65)
            else:
                time.sleep(3.2)
        
        call_count += 1
        result = translate(chunk, target_lang, temperature, max_tokens, system_prompt, cohere_key)
        
        if "error" in result:
            if verbose:
                print(f"  ❌ Chunk {i+1}/{len(chunks)}: {result['error']}", file=sys.stderr, flush=True)
            results.append(f"[TRANSLATION ERROR: {result.get('error','')}]")
        else:
            results.append(result["text"])
            total_in += result.get("tokens_in", 0)
            total_out += result.get("tokens_out", 0)
            if verbose and len(chunks) > 1:
                print(f"  ✓ Chunk {i+1}/{len(chunks)} ({result.get('tokens_in',0)}→{result.get('tokens_out',0)} tokens)", file=sys.stderr, flush=True)
    
    output_text = "\n\n".join(results)
    
    if verbose:
        print(f"  ✅ Total: {total_in}→{total_out} billed tokens across {len(chunks)} chunks", file=sys.stderr, flush=True)
    
    # Write output
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(output_text)
        if verbose:
            print(f"  💾 Saved to: {output}", file=sys.stderr, flush=True)
        return {"file": output, "chars": len(output_text), "chunks": len(chunks),
                "tokens_in": total_in, "tokens_out": total_out}
    else:
        # stdout — only print the translation, no metadata
        return {"text": output_text, "chunks": len(chunks),
                "tokens_in": total_in, "tokens_out": total_out}


# ── CLI ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Cohere Command A Translate — SOTA translation for 23 languages",
        epilog="Set COHERE_API_KEY environment variable or pass --api-key.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # Input source (mutually exclusive in practice, but argparse allows both)
    parser.add_argument("text", nargs="?", help="Text to translate (passes through agent context)")
    parser.add_argument("--file", "-f", default=None,
                        help="Input file path (or '-' for stdin). Bypasses agent context — ZERO agent tokens!")
    parser.add_argument("--output", "-o", default=None,
                        help="Output file path (default: stdout)")
    
    # Translation options
    parser.add_argument("--to", "-t", default="en",
                        help="Target language code: ja, en, zh, ko, fr, de, es, ...")
    parser.add_argument("--temperature", type=float, default=0.3,
                        help="Temperature 0.1-1.0 (default: 0.3)")
    parser.add_argument("--max-tokens", type=int, default=4000,
                        help="Max output tokens per chunk (default: 4000)")
    parser.add_argument("--system-prompt", default=None,
                        help="System message for translation constraints")
    
    # Auth & output format
    parser.add_argument("--api-key", default=None,
                        help="Cohere API key (or set COHERE_API_KEY env var)")
    parser.add_argument("--json", action="store_true",
                        help="Output full JSON with token counts")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Suppress progress messages (stderr)")
    parser.add_argument("--list-languages", action="store_true",
                        help="List supported language codes")

    args = parser.parse_args()

    if args.list_languages:
        print("Supported languages (23):")
        for code, name in sorted(LANGUAGES.items()):
            print(f"  {code}: {name}")
        return

    if not args.text and not args.file:
        parser.error("Either provide text argument or --file/-f")

    # Determine input source
    verbose = not args.quiet
    
    if args.file:
        # ✅ FILE MODE — bypasses agent context entirely
        result = translate_file(
            filepath=args.file,
            target_lang=args.to,
            output=args.output,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            system_prompt=args.system_prompt,
            cohere_key=args.api_key,
            verbose=verbose,
        )
    else:
        # Direct text mode
        result = translate(
            text=args.text,
            target_lang=args.to,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            system_prompt=args.system_prompt,
            cohere_key=args.api_key,
        )
        # Add empty chunks count for uniform output
        result.setdefault("chunks", 1)

    if "error" in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        if "detail" in result:
            print(f"  {result['detail']}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif not args.file or not args.output:
        # If file→stdout or text→stdout, print just the translation
        print(result.get("text", result.get("file", "")))


if __name__ == "__main__":
    main()
