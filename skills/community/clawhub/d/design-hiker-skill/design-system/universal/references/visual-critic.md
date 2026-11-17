# Visual Critique Protocol

Use this file during L3.6 — after generating HTML, after taking a screenshot.
Do NOT evaluate from code alone. Look at the screenshot, then answer these questions.

---

## Step 1: First impression (2 seconds)

Look at the screenshot for 2 seconds, then answer:

1. **First word**: One word to describe the visual impression. Target: "clean". Red flags: "busy", "heavy", "colorful", "decorated".
2. **Eye entry point**: Where does your eye go first? Is that the intended primary content?
3. **Visual noise**: Is there anything that draws attention but shouldn't?

If the first impression is not "clean/simple/clear", proceed to the systematic check.

---

## Step 2: Systematic visual check

Answer each question. Any "NO" = specific issue to fix.

### Color
- [ ] Count distinct colors visible. Should be ≤ 3 (background, text, one accent). More than 3 = too many.
- [ ] Does the accent color appear on ONLY the most important element(s)? Not scattered everywhere.
- [ ] Are there any two different colors doing the same job (e.g., two different highlight colors for similar items)?

### Typography
- [ ] Is there ONE dominant font size in each content area? Multiple sizes in a list/table = problem.
- [ ] Is bold used SPARINGLY — only on content that genuinely needs emphasis?
- [ ] Do all items of the same type look identical (same size, same weight, same color)?

### Spacing & Layout
- [ ] Does the layout breathe? No elements cramped or touching?
- [ ] Are margins consistent — same type of element has same padding?
- [ ] Do related elements group visually (close together)? Do unrelated elements have clear separation?

### Dividers & Borders
- [ ] Are any divider lines clearly visible as solid lines? (Should be barely perceptible)
- [ ] Do any borders feel "boxy" or "heavy"? Cards should float, not be caged.
- [ ] Is there a clear background difference between different sections (header vs content)?

### Platform fit (check if this is a macOS app)
- [ ] Do buttons look compact (small, not pill-shaped touchscreen buttons)?
- [ ] Does the overall density feel like a desktop app, not a mobile app?
- [ ] Are any elements clearly oversized for their context?

### Information hierarchy
- [ ] Can you tell what's most important at a glance, without reading?
- [ ] Is hierarchy created by weight/position, NOT by color variety?
- [ ] Does secondary information visually recede (lighter, not colored)?

---

## Step 3: Issue report format

For each issue found, write:

```
VISUAL ISSUE: [short name]
Seen in screenshot: [describe exactly what you see]
Problem: [why it violates a principle]
Fix: [specific CSS change]
Priority: HIGH / MEDIUM / LOW
```

Example:
```
VISUAL ISSUE: Price font too large
Seen in screenshot: "35元/月" appears roughly 1.4x larger than surrounding text
Problem: Violates "one font size" rule — size variation adds visual noise without improving clarity
Fix: Remove font-size override on .val-price, set to same 15px as .val
Priority: HIGH
```

---

## Step 4: Decision

After listing all issues:

- **0 HIGH issues, ≤ 2 MEDIUM**: Acceptable. Proceed to L4.
- **Any HIGH issue OR > 2 MEDIUM**: Fix all HIGH issues, fix critical MEDIUM ones, re-screenshot.
- **Maximum 3 visual critique iterations**. After 3rd iteration, deliver with remaining issues noted.

---

## Common "AI design tells" to watch for

These are the most frequent visual problems Claude generates. Check for each explicitly:

1. **Too many distinct colors** — If you see more than 2 colors in the content area (not counting text gray), that's too many.
2. **Font size variation in lists/tables** — Every row should look the same height and weight.
3. **Emoji-based icons** — Any 🔍📦⚙️ in the UI chrome = fail. Must be SVG.
4. **Separator lines that look like table grid lines** — Should be nearly invisible.
5. **Buttons that look like mobile buttons** — Should be compact, 26-28px on desktop.
6. **Two different colors for the same semantic role** — e.g., blue for one recommendation and green for another when they're the same type of thing.
7. **Decorated "empty" space** — Gradient backgrounds, colored cards where white would work fine.


---

## Specific Prohibitions (from taste-skill production testing)

These are zero-tolerance rules extracted from real AI-generated page audits.
Check each one explicitly before delivering — do not rely on "I don't think I used it."

### Em-dash: ZERO TOLERANCE

Search the output for `—` and `–`. If found anywhere — headline, body, caption, button, attribution — the output is not done.

```
grep -c "—\|–" your-file.html   # must return 0
```

Replace with:
- Comma or period (in headlines)
- Regular hyphen ` - ` with spaces (in attribution)
- Two sentences, a colon, or parentheses (in body copy)
- Regular hyphen (in ranges: 2018-2026, €40-80k)

### Color

- No `#000000`. Use off-black (`#111111`, `#1a1a1a`)
- No AI purple / blue gradient glow as default accent
- One warm OR cool gray family per project — no mixing
- Accent color used identically across ALL sections (no warm-grey page with blue CTA in section 7)

### Typography

- No `Fraunces` or `Instrument Serif` as default display fonts (top two LLM-favourite serifs)
- No Inter as default unless brief explicitly asks for neutral/Linear style
- No oversized H1 that just screams — control hierarchy via weight + color, not raw scale
- No mixed font-family emphasis (don't inject a serif word into a sans headline "for interest")

### Content

- No `—` anywhere (see above)
- No "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize" in copy
- No "John Doe", "Acme", "SmartFlow" as placeholder content
- No `99.99%`, `50%`, `1,234,567` as data — use organic numbers
- No `V0.6`, `BETA`, `INVITE-ONLY` in hero area
- No `001 · Capabilities`, `00 / INDEX` style section eyebrows
- No `·` as the default separator for more than 1 item per line
