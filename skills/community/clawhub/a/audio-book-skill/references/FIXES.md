# Narration quality fixes — verified vs. suspected

This file separates fixes that were **verified** against real long-form
production from behaviors that are **suspected** or defensive. Trust the
verified section; treat the suspected section as leads, not guarantees.

---

## VERIFIED (reproduced on real multi-part long-form renders)

### 1. Mid-sentence awkward pauses = surviving soft line breaks
**Symptom:** the narrator pauses at odd spots inside a sentence instead of
reading it straight through, so a single sentence sounds like choppy
fragments.

**Root cause (confirmed):** Markdown/manuscript prose is hard-wrapped at
~70–80 characters. Each of those line breaks sits *inside* a sentence.
The Kokoro G2P frontend can treat a line break as a phrase boundary and
insert a pause. On one real document, 299 of 398 non-empty lines ended
mid-sentence — every one a candidate pause.

**Fix:** unwrap soft (mid-sentence) line breaks into full paragraphs;
keep only blank-line paragraph breaks. After the fix, nearly every line
ends in real sentence/clause punctuation. Implemented in
`prepare_manuscript.py::normalize_prosody`.

**Verify:**
```bash
# mid-sentence line count should be near zero after prepare
grep -cE '[a-zA-Z,]$' narration.txt
grep -cE '.' narration.txt      # total non-empty, for ratio
```

### 2. Abbreviation periods read as full stops
**Symptom:** a pitch drop / pause mid-sentence at "U.S.", "e.g.", "Dr.",
"St.", etc., as if the sentence ended.

**Fix:** convert common abbreviations to pause-free spoken forms before
synthesis (`U.S.` → `US`, `e.g.` → `for example`, `Dr.` → `Doctor`, …).
Implemented in `prepare_manuscript.py` (`_ABBREV`). Note `St.` → `Saint`
is right for names/places but wrong for "Street" — review if your corpus
uses the latter.

### 3. Accent is a voice choice, not a filter
**Symptom:** wanting a British (or other) accent.

**Fact:** Kokoro ships native voices per accent. Pick a voice id in the
right family AND set the matching G2P language code — do not "filter" an
American voice. British English female voices: `bf_alice`, `bf_emma`,
`bf_isabella`, `bf_lily`. British male: `bm_daniel`, `bm_fable`,
`bm_george`, `bm_lewis`. Set `--lang b` (British G2P) with a `bf_`/`bm_`
voice; `--lang a` (American) with `af_`/`am_`. A `bf_` voice under the
American pipeline logs a language-mismatch warning and uses American
phonemization even though the timbre is British — set `--lang b` for
correct British pronunciation.

### 4. Sources/bibliography should not be narrated (when that's the intent)
**Symptom:** the narration reads a long list of citations/URLs at the end.

**Fix:** for description-bound bibliographies, drop the trailing
Sources/Bibliography section from the narration script (keep a real
closing line if one follows it). Configurable: `--drop-sources` in
`prepare_manuscript.py`. Off by default — many audiobooks *should* read
their back-matter. Retain the sources separately for a description/
companion file; attribution is preserved, just relocated.

### 5. Lossless intermediate, single final encode
**Symptom:** quality erosion from repeated lossy encoding.

**Fix:** assemble chunk WAVs into a lossless WAV master via ffmpeg
`concat` **stream copy** (no re-encode), then encode MP3 once from the
master. Implemented in `narrate.py` (`_concat_wavs`, `encode_mp3`).

### 6. Don't over-interrupt long renders
**Symptom:** a truncated/corrupt output on long jobs.

**Cause (observed):** aggressively polling/killing a long-running
synthesis or ffmpeg process can SIGKILL it mid-write. Background long
renders and poll on 30–60s intervals, not continuously.

### 7. GPU memory contention OOMs Kokoro
**Symptom:** an immediate Metal "Insufficient Memory" error on the first
inference, even though Kokoro-82M is small.

**Cause (observed on Apple Silicon):** another large local model server
(e.g. a multi-billion-parameter MLX/LLM server) holding most of unified
memory starves Kokoro's Metal command buffer. Check for and stop such a
process before rendering.

---

## SUSPECTED / DEFENSIVE (not independently confirmed here)

- **Roman-numeral labels** ("Part I" → possibly read as "Part Eye"): a
  numeral→word pass is defensive. Confirmed on some frontends; treat as
  corpus-dependent. Apply only if your manuscript uses Roman-numeral
  section labels.
- **Slash alternatives** ("Tartary/Tartaria" → "Tartary or Tartaria"):
  reads more naturally, but only apply between bare word tokens (never on
  dates/fractions like 3/4).
- **Phonemizer "words count mismatch" warning:** benign in observed runs
  (fires on long single-line paragraphs); audio came out clean. Not a
  proven failure signal — do not treat it as one without evidence.
- **Very long sentences (60+ words):** commas/semicolons act as short
  pauses; do not invent punctuation that changes meaning.
