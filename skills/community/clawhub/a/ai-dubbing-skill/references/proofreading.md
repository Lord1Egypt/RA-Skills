# Proofreading: fixes.json

Transcription engines mishear names, brands, numbers and jargon, and often drop punctuation.
Captions with a wrong name are worse than none. So before anything is burned in:

1. `python3 <skill>/scripts/fix.py dub.json --report`: unsure words (low confidence),
   words close to a `vocab` name, numbers split in two.
2. Read every line of `work/<id>/transcript.txt` (lines are numbered `L1`, `L2`...).
3. Write `work/<id>/fixes.json`. Never edit transcript.json: transcribing again overwrites it.

```json
{
  "lines": {
    "2": "cursing our names because we accepted some feature that was complicated and hard to train, and in the end, hard to operate."
  },
  "replace": {"Benkin": "Behnken", "Kubernetties": "Kubernetes"},
  "emphasis": ["cursing our names", "so easy"],
  "fillers": "remove",
  "profanity": "keep",
  "sounds": {"12.4": "[laughter]"}
}
```

- `lines`: the full corrected text of a line. Unchanged words keep their exact times; changed or
  added words share the time of the words they replace. Fix punctuation here too: captions break
  at sentence ends and commas.
- `replace`: single whole words, everywhere in the video (case-sensitive; punctuation around the
  word is kept). For phrases, use `lines`.
- `emphasis`: words or phrases the style colours as keywords (most styles: green or yellow). One
  or two per sentence at most: the number, the name, the payoff. Stressing everything stresses nothing.
- `fillers`: `remove` (default: um, uh, erm, hmm) or `keep` (verbatim, for accessibility work).
- `profanity`: `keep` (default), `mask` (f***) or `remove`.
- `sounds`: meaningful sounds at a second, for accessible captions. Always in the SRT; burned in
  only for outputs with `"sounds": true`.

Rules:

- Write what was said. Don't improve grammar, cut sentences or add words that weren't spoken.
  ("hard to operate" may be fixed to "and in the end, hard to operate" only if those words were said.)
- Numbers as digits ("17,500 miles", "9 or 10 minutes"); units as said.
- Ask the user only what you can't know: how a person or product is spelled.
