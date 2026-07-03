---
name: deckly-redesign
description: Redesign and beautify PowerPoint/PDF presentation decks into polished, on-brand slides using Deckly's AI. Use when the user wants to improve, beautify, restyle, or redesign a .pptx or .pdf deck, asks to "make slides look better", or mentions Deckly.
---

# Deckly Deck Redesign

Turn a rough `.pptx`/`.pdf` deck into polished slides via the Deckly API. This is an **interactive** workflow: pick an aesthetic, run a free preview, fine-tune individual slides, then render and download the full deck.

## Setup

The script uses only the Python 3 standard library — no `pip install` needed. All commands print JSON to stdout (parse this) and progress to stderr. Optional: `DECKLY_API_BASE` (default `https://deckly.art`).

```bash
python scripts/deckly.py <command> [args]
```

If the agent has no Python, use the raw HTTP flow in [reference.md](reference.md) instead.

## Authentication (onboard the user in-conversation)

A Deckly account is required only for paid actions and downloads. Resolve credentials in this order automatically: `DECKLY_TOKEN` → `DECKLY_API_KEY` → saved key at `~/.deckly/credentials` → `DECKLY_EMAIL` + `DECKLY_PASSWORD`.

**When a command reports "No credentials", do NOT send the user to a website.** Onboard them right in the chat:

1. Ask the user for an email + password (a new password they choose).
2. Run `signup`. Then ask the user for the 6-digit code from their inbox and run `verify`. This creates and saves an API key locally, so all later commands "just work".

```bash
python scripts/deckly.py signup --email user@example.com --password <chosen>
# user reads the 6-digit code from their email:
python scripts/deckly.py verify --email user@example.com --code 123456
```

**If `signup` returns `status: account_exists`**, the email already has a Deckly account. Tell the user it will use their existing account, then ask for their password and run `login` (required to fetch a key):

```bash
python scripts/deckly.py login --email user@example.com --password <their password>
```

Notes:
- `verify` and `login` both create and save a `dk_` API key to `~/.deckly/credentials` (chmod 600). After that, never ask for credentials again unless the user switches accounts.
- New accounts get a free 3-slide preview (0 credits) — perfect for a first trial run.
- To use a different account, the user can pass `DECKLY_EMAIL`/`DECKLY_PASSWORD` or delete `~/.deckly/credentials`.

## Credit model (tell the user before spending)

- **First-time accounts get one free preview**: 3 slides, 0 credits.
- Full redesign by selected slide count: 1–10 = 10 credits, 11–20 = 20, 21–60 = 40. Max 60 slides.
- Fine-tuning a single slide = 1 credit. **Reverting / switching versions = free.**
- Check balance and free-preview availability with `me` before any paid action.

## Interactive workflow

```
- [ ] 1. analyze the deck
- [ ] 2. present aesthetic options, get user's choice + any custom instruction
- [ ] 3. free preview (if available) or confirm credit cost, then redesign
- [ ] 4. show results, offer fine-tune loop
- [ ] 5. render full deck (continue) and download
```

**1. Analyze** — uploads, extracts, returns slide list + recommendations.

```bash
python scripts/deckly.py analyze deck.pptx
# -> project_id, slides[], recommended_slide_indices, free_preview_available, credit_balance
```

**2. Choose aesthetic** — list options and let the user pick. Do not auto-pick unless the user wants speed.

```bash
python scripts/deckly.py styles
# -> text_styles[] (style_preset "text_style:<id>") + template_themes[] (style_preset "<id>")
```

`style_preset` accepts: a `text_style:<id>` (e.g. `text_style:minimalist_corporate`), a template theme id (e.g. `dark-blue-business`), or any free-text style name (AI-generated). Also collect an optional `--custom` instruction from the user (e.g. "use our brand blue, keep it minimal").

**3. Redesign** — for first-time users this automatically runs as a free 3-slide preview. Otherwise confirm cost with `quote` first.

```bash
python scripts/deckly.py quote <project_id> --slides 1-12        # check cost / can_afford
python scripts/deckly.py redesign <project_id> --slides 1-12 \
    --style text_style:minimalist_corporate --custom "brand blue, minimal"
```

**4. Fine-tune loop** — repeat per slide based on user feedback.

```bash
python scripts/deckly.py finetune <project_id> --slide 3 --instruction "make the title bigger"  # 1 credit
python scripts/deckly.py revert   <project_id> --slide 3                                         # free
python scripts/deckly.py versions <project_id> --slide 3                                         # list versions
python scripts/deckly.py select   <project_id> --slide 3 --path "/storage/...png"                # free
```

**5. Finish** — if the deck was a free preview, `continue` renders the full paid deck. Then download.

```bash
python scripts/deckly.py continue <project_id>                 # pay full tier, render all selected
python scripts/deckly.py download <project_id> -o final.pptx
```

## One-shot (no interaction)

For "just redesign it fast". Defaults to the first style (`text_style:minimalist_corporate`) and the recommended slides. **Pays for the full deck** unless `--preview-only` is set.

```bash
python scripts/deckly.py oneshot deck.pptx -o final.pptx
python scripts/deckly.py oneshot deck.pptx --style dark-blue-business --slides 1-20
python scripts/deckly.py oneshot deck.pptx --preview-only      # free 3-slide preview only
```

## Notes

- All redesign steps are async; the script polls until done (default timeout 1800s, `--timeout` to change).
- `--slides` accepts lists and ranges: `1,3,5` or `1-10` or `1-5,8`.
- On failure the script exits non-zero with an `ERROR:` line on stderr (includes content-policy / insufficient-credit messages from the API).
- For full API/field details and the no-Python HTTP flow, see [reference.md](reference.md).
