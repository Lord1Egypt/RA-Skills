# API Notes - API 使用说明

## Free Dictionary API

This skill uses the free Dictionary API at:
https://dictionaryapi.dev/

**Key points:**
- No API key required
- Free for non-commercial use
- Rate limited (unknown limit, but ~3 requests/second seems safe)
- Provides American English phonetics by default

## IPA Format Notes

The API returns IPA (International Phonetic Alphabet) phonetics in **American English** pronunciation.

### Common American IPA symbols:

| Symbol | Example | Description |
|--------|---------|-------------|
| `/ə/` | *about* | schwa |
| `/ɑː/` | *father* | broad a |
| `/æ/` | *cat* | short a |
| `/eɪ/` | *day* | long a |
| `/iː/` | *see* | long e |
| `/ɪ/` | *sit* | short i |
| `/aɪ/` | *my* | long i |
| `/oʊ/` | *go* | long o (American) |
| `/ʊ/` | *book* | short u |
| `/uː/` | *too* | long u |
| `/ɜːr/` | *bird* | rhotic er |
| `/ər/` | *worker* | schwa+r |
| `/ɝ/` | *world* | stressed er (American) |

## American vs British Differences

Key differences in pronunciation that affect transcription:

1. **-er ending**: American /ɝ/ vs British /ɜː/
   - *world*: AmE /wɝld/ vs BrE /wɜːld/
   
2. **-t- between vowels**: Flap consonant /ɾ/ in American
   - *water*: AmE /ˈwɑːtər/ -> pronounced /ˈwɑːɾər/

3. **o**: AmE /oʊ/ vs BrE /əʊ/
   - *go*: AmE /ɡoʊ/ vs BrE /ɡəʊ/

4. **a**: AmE /æ/ vs BrE /ɑː/ in words like *dance*, *path*

This skill **prefers American pronunciation** when available, which matches what the Dictionary API provides.

## Handling Failed Lookups

- If a word is not found (404), the phonetic field is left empty
- The `is_valid` flag is set to `False`
- Failed words are still included in output for manual correction
- Common reasons for failure:
  - Proper nouns (names, places)
  - Very technical jargon
  - Non-English words
  - Typographical errors

## Extending to Other Pronunciation Sources

If you need higher reliability, you can modify the script to use:

- Merriam-Webster API (requires API key)
- Oxford Dictionaries API (requires API key)
- Wiktionary parser
- CMU Pronouncing Dictionary (offline, no rate limits but American only)

The CMU dictionary has ~135k words in phonetic format and works completely offline.
