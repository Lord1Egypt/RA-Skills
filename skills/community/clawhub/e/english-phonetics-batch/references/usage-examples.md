# Usage Examples - 使用示例

## Example 1: Basic bulk processing from plain word list

**Input file `words.txt`:**
```
apple
banana
cherry
date
elderberry
fig
grape
```

**Command:**
```bash
python english_phonetics_batch.py words.txt output.txt
```

**Output file `output.txt`:**
```
apple /ˈæpl/ noun
banana /bəˈnænə/ noun
cherry /ˈtʃeri/ noun
date /deɪt/ noun
elderberry /ˈɛldərˌbɛri/ noun
fig /fɪɡ/ noun
grape /ɡreɪp/ noun
```

## Example 2: Check and fix existing file with corrupted phonetics

**Input file `corrupted_vocab.txt` (has ? placeholders from encoding issues):**
```
apple /?pl/
banana /b??n?n?/
cherry /?t?eri/
```

**Command:**
```bash
python english_phonetics_batch.py corrupted_vocab.txt fixed_vocab.txt --check
```

**Output:** Fixes all invalid phonetics containing question marks.

## Example 3: Output as CSV for spreadsheets

**Command:**
```bash
python english_phonetics_batch.py words.txt output.csv --format csv
```

**Output:**
```csv
word,phonetic_american,part_of_speech,is_valid
apple,"/ˈæpl/","noun",True
banana,"/bəˈnænə/","noun",True
cherry,"/ˈtʃeri/","noun",True
```

## Example 4: Output as Markdown table

**Command:**
```bash
python english_phonetics_batch.py words.txt output.md --format markdown
```

**Output:**

| Word | American IPA | Part of Speech |
|------|--------------|----------------|
| apple | /ˈæpl/ | noun |
| banana | /bəˈnænə/ | noun |
| cherry | /ˈtʃeri/ | noun |

## Example 5: Python API integration

```python
from english_phonetics_batch import PhoneticsBatch, WordPhonetic

# Create processor with custom delay (faster for small lists)
processor = PhoneticsBatch(delay_ms=100)

# Process single word
result = processor.fetch_phonetic("hello")
print(f"hello → {result.phonetic}")

# Process multiple words
words = ["one", "two", "three", "four", "five"]
results = processor.process_words(words)

# Access results
for r in results:
    if r.is_valid:
        print(f"{r.word}: {r.phonetic} ({r.part_of_speech})")
    else:
        print(f"{r.word}: NOT FOUND in dictionary")

# Save in any format
processor.save_results(results, "my_words.txt", format="text")
processor.save_results(results, "my_words.csv", format="csv")
processor.save_results(results, "my_words.md", format="markdown")
```

## Example 6: Working with different input formats

The tool automatically extracts just the first token from each line, so inputs like this work fine:

```
1 apple
2 banana
3 cherry
```

The numbers will be ignored and it will process `apple`, `banana`, `cherry`.

## Example 7: Large lists with custom retries and delay

For vocabularies with thousands of words, increase delay and retries for reliability:

```bash
python english_phonetics_batch.py 1000words.txt output.txt --delay 500 --retries 5
```

This gives:
- 500ms between requests (safer for the API)
- Up to 5 retries if you hit rate limiting
- Exponential backoff on retries

## Example 8: Processing statistics

After completion, the tool prints a complete summary:

```
==================================================
Processing Summary:
  Total words:    100
  Success:        94
  Failed:         6
  Retries:        3
  Success rate:   94.0%
==================================================
```

Failed words are still included in output with empty phonetics - you can manually fix them later.

## Rate Limiting and Retries

The default delay is 300ms between requests with 3 retries. This works well for most cases:

| List Size | Delay | Retries |
|-----------|-------|---------|
| < 50 words | 100-200ms | 3 |
| 50-500 words | 300ms | 3 |
| 500-2000 words | 500ms | 5 |
| > 2000 words | 1000ms | 5 |

## Working with different input formats

The tool automatically cleans up common input formats:

**Numbered word lists:**
```
1 apple
2 banana
3 cherry
```
Automatically strips the numbers and processes `apple`, `banana`, `cherry`.

**Existing markup:**
```
apple [noun] /something/
banana (noun) /something/
```
Automatically removes existing brackets/phonetics and re-processes clean.
