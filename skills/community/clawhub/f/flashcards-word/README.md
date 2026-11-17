# Word / Vocabulary Flashcards (printable Word .docx)

Build **print-and-cut flashcards** for a ~5-year-old as a clean Word `.docx` file.
Each A4 page holds **4 cards in the four corners**. Front = a cute picture + the big
word; back = the word only (for recall / tracing). The layout is **double-sided
mirror-aligned**, so when you flip a sheet you printed double-sided, every back-word
lands exactly under its picture.

Works for **English** words out of the box (this repo), and the same recipe extends to
**Chinese hanzi + pinyin** (see the `hanzi-flashcards-word` companion).

> 🌏 Chinese readers: see the [中文 README (`README.zh.md`)](README.zh.md).

```
        +---------------------+---------------------+
        |   🐱                |   🐶                |
        |   cat               |   dog               |   <- front page (picture + word)
        +---------------------+---------------------+
        |   🐦                |   🐟                |
        |   bird              |   fish              |
        +---------------------+---------------------+

        +---------------------+---------------------+
        |                     |                     |
        |        dog          |        cat          |   <- back page (word only,
        +---------------------+---------------------+      left/right mirrored for
        |                     |                     |       double-sided long-edge flip)
        |        fish         |        bird         |
        +---------------------+---------------------+
```

---

## 1. Requirements

- **Python** 3.9+
- **Python packages:** `pip install -r requirements.txt`  →  installs `Pillow` and `python-docx`
- **`rsvg-convert`** (to turn emoji SVG into crisp PNG). Install:
  - Debian/Ubuntu: `sudo apt-get install -y librsvg2-bin`
  - macOS: `brew install librsvg`
- **`curl`** (already on most systems)
- **A bold sans font** readable by Pillow (defaults to DejaVu Sans Bold; Liberation /
  Noto Sans also work). Find one with `fc-list | grep -i sans`.

> ⚠️ Run everything in a **real shell**. The Pillow / python-docx imports will fail in
> sandboxes/REPLs that don't have them installed.

---

## 2. Quickstart (English, 40 words)

```bash
# 0) get the scripts however you like (this repo, or a skill package), into a work dir
cd my-flashcards          # contains: scripts/ , requirements.txt

# 1) install
pip install -r requirements.txt
sudo apt-get install -y librsvg2-bin     # if rsvg-convert is missing

# 2) validate the word list (counts, multiples-of-4, no dupes)
python3 scripts/words100.py

# 3) download the emoji artwork (SVG -> 256px PNG), race-free
python3 scripts/download_emoji.py

# 4) render front+back PNGs for every word
python3 scripts/generate_all.py

# 5) assemble the double-sided .docx
python3 scripts/build_docx.py
```

Output: `English_Words_DoubleSided.docx` (one A4 sheet = 4 cards = 1 front + 1 back).

Or just: `make cards` (runs all four steps in order).

---

## 3. The word list — `scripts/words100.py`

The whole content is one Python list:

```python
WORDS = [
    (word, "", emoji),        # (label shown on card) ("" unused) (picture codepoint)
    ...
]
```

- **`word`** — the label printed large on the card. Keep it **short and simple** for a
  5-year-old. Lower/upper case is fine; the renderer keeps what you type.
- **`""`** — an intentionally-empty middle slot (kept so the tuple shape matches the
  Chinese/pinyin variant, where this holds the pinyin). The English renderer ignores it.
- **`emoji`** — any Twemoji codepoint used as the picture. ZWJ / VS16 sequences are OK
  (e.g. `"🍦"`, `"🦆"`) — the downloader strips the invisible modifiers when forming the
  file name.

**Rules:**
- `len(WORDS)` must be a **multiple of 4** (4 → 1 sheet, 8 → 2, 100 → 25).
- Words must be **unique**.
- Run `python3 scripts/words100.py` after each edit to self-check (it asserts all three).

---

## 4. Examples

### Example A — Add 8 more food words (batch grows 40 → 48, still ÷4-clean)
Edit `scripts/words100.py`, append to `WORDS` (anywhere in the list):
```python
    ("pasta",      "", "🍝"),
    ("rice",       "", "🍚"),
    ("bread",      "", "🍞"),
    ("carrot",     "", "🥕"),
    ("tomato",     "", "🍅"),
    ("pepper",     "", "🌶️"),
    ("potato",     "", "🥔"),
    ("mushroom",   "", "🍄"),
```
→ `python3 scripts/words100.py` should print `OK: 48 unique English words`. Re-run steps 3–5.

### Example B — A small theme set (e.g. "colours", 8 words, 1 sheet pair)
Replace `WORDS` with exactly 8:
```python
WORDS = [
    ("red",    "", "🔴"),
    ("blue",   "", "🔵"),
    ("yellow", "", "🟡"),
    ("green",  "", "🟢"),
    ("orange", "", "🟠"),
    ("purple", "", "🟣"),
    ("pink",   "", "🌸"),
    ("brown",  "", "🟤"),
]
```
→ step 5 writes a 2-sheet docx (1 front page + 1 back page).

### Example C — Reuse one picture for two similar words (allowed)
```python
    ("sun",  "", "☀️"),
    ("star", "", "⭐"),        # different emoji, different picture
    # but sharing IS fine / expected when the picture genuinely fits both:
    ("ear",  "", "👂"),
    ("hear", "", "👂"),        # intentional shared image -> reported, not an error
```
The downloader **md5-collision-checks** at the end; intentional shared images are listed
as `intentional shared images: [...]` and are fine. Only *unintended* collisions matter.

### Example D — Chinese / pinyin (the companion skill)
Same layout, but the middle slot carries **pinyin with precomposed diacritics** and the
font is a CJK face with tonal marks:
```python
WORDS = [
    ("日", "rì",   None),     # None -> hand-drawn card, or
    ("火", "huǒ",  "🔥"),     # emoji picture
    ...
]
```
Use a CJK font (`EN_FONT`/`CJK_FONT` → e.g. WenQuanYi Zen Hei / Noto Sans CJK). The rest
of the pipeline (download → render → .docx + mirror alignment) is identical.

### Example E — A number card without an emoji (draw it yourself)
Some items aren't emoji (e.g. the digit 1–10 keycap, custom art). Set the emoji slot to a
custom marker and drop a pre-rendered PNG named to match:
```python
    ("one", "", "D1"),        # "D1" tells the pipeline: use pre_one_front/back.png
```
Place `pre_one_front.png` and `pre_one_back.png` next to the scripts and the renderer
copies them straight through.

---

## 5. How the layout works (so you don't need to trust your eyes)

**Aspect.** A4 portrait with 10 mm margins → usable 190×277 mm. A 2×2 cell is
95×138.5 mm. The per-card image is generated at the same **≈95:135** aspect, so
`add_picture(width=Mm(95), height=Mm(135))` fits with **no stretching**.

**Borderless 2×2 table per page.** One borderless table, 2×2, images fill each cell.
Extra pages use `document.add_section(NEW_PAGE)` (NOT a broken manual page-break).

**Double-sided mirror alignment (the key trick).** Word's default double-sided flip is
**long-edge flip = mirror left ↔ right**. So the back page swaps the two columns:

```
front:                 back (columns swapped):
 w0  w1                  w1  w0
 w2  w3                  w3  w2
```
The scripts assert this for **every** card pair, not just a sample:
```python
mirror = {"TL":"TR", "TR":"TL", "BL":"BR", "BR":"BL"}
for pos, word in front.items():
    assert back[mirror[pos]] == word, f"misaligned {pos}"
```

### Print settings (tell the end user!)
- **双面打印 → 长边翻转** (double-sided, **long-edge flip**).
- **实际大小 / do NOT "fit to page"** — no scaling.
- **157 gsm+ card stock** for durability (or print on regular paper, then glue onto card).
- Cut along the seams between the four cards.

---

## 6. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `ModuleNotFoundError: Pillow / docx` | Not a real Python env. Run in a shell with `pip install -r requirements.txt`. |
| `rsvg-convert: command not found` | `sudo apt-get install -y librsvg2-bin` (or `brew install librsvg`). |
| Emoji 404 on download | VS16/ZWJ sequence — the script already strips it; if a custom one 404s, use its base codepoint. |
| Word renders as boxes / tofu | Font lacks glyphs. Set `EN_FONT` to a font that has them (or use the CJK face for hanzi). |
| A word is clipped | The auto-fit handles this; if still tight, shorten the word or bump the min size floor in `generate_all.py`. |
| Shared temp-file corruption under parallel download | Already fixed (per-codepoint temp path + dedupe-by-unique-codepoint before the parallel pass). |

---

## 7. Re-running / idempotency

The pipeline is safe to re-run. `download_emoji.py` clears old PNGs and regenerates
`emoji/_final.json`; `generate_all.py` overwrites `all_front/` & `all_back/`;
`build_docx.py` re-writes the `.docx`. Use `make clean` to wipe generated artifacts
(`emoji/ all_front/ all_back/` + the docx) and start fresh.

---

## 8. Project layout

```
flashcards-word/
├── README.md                 # English
├── README.zh.md              # 中文说明
├── LICENSE                   # MIT
├── Makefile                  # `make cards` / `make clean`
├── requirements.txt          # Pillow, python-docx
├── .env.example              # EMOJI_OUT / EN_FONT / OUT_DOCX overrides
├── SKILL.md                  # full spec: recipes, pitfalls, verification checklists
└── scripts/
    ├── words100.py           # the word list + emoji  (EDIT THIS)
    ├── download_emoji.py     # Twemoji SVG -> PNG (race-free, md5-checked)
    ├── generate_all.py       # renders front+back card PNGs (auto-fit big word)
    └── build_docx.py         # double-sided 2x2 borderless .docx assembler
```

## 9. License

MIT — see `LICENSE`. Emoji artwork is from [Twemoji](https://github.com/twitter/twemoji)
(Creative Commons / free for use).
