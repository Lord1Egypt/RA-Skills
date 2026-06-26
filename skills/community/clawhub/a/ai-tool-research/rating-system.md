# Rating System

The two-dimensional rating used across every Skills Catalog. Read during Step 4 of the parent SKILL.md.

---

## Dimension 1 — Validity

**Question**: Is this skill / rule / plugin actually real and maintained?

| Badge | Name | Criteria (ANY of) |
|---|---|---|
| ✅ | **Verified** | Official vendor resource (e.g., `anthropics/*`, `openai/*`, `openclaw/*`, `google-gemini/*`, `getcursor/*`) **OR** GitHub repo with all of: push in last ~90 days, ⭐ > 500 **or** installs > 1k, documented README |
| 🟢 | **Likely-valid** | Confirmed canonical repo, moderate traction (⭐ 50–500 or installs 100–1k), push in last ~180 days |
| 🟡 | **Early / Niche** | Real but new or single-maintainer, ⭐ < 50 or unknown, push in last ~365 days |
| 🔴 | **Unverified** | Mentioned in an article / awesome-list but canonical source cannot be confirmed, OR repo archived / last push > 1 year |

### Validity decision flow

```text
1. Is it maintained by the vendor itself? → ✅ Verified (stop)
2. Can you find a canonical URL (GitHub repo, vendor doc, marketplace listing)?
    No  → 🔴 Unverified (stop)
    Yes → continue
3. When was the last push / update?
    < 90 days  → likely ✅ or 🟢
    < 180 days → likely 🟢 or 🟡
    < 365 days → likely 🟡
    > 365 days → 🔴
4. Community signal (stars / installs / endorsements)?
    Big + recent     → ✅
    Moderate + recent → 🟢
    Small            → 🟡
5. If conflicting signals, round DOWN (be honest).
```

### Common mistakes

- Giving ✅ to a repo because "the vendor's name is in the URL" — check the actual org.
- Giving 🟢 based on a blog article alone — articles aren't a maintenance signal.
- Giving 🔴 to a good skill just because it's new — use 🟡 for that case.
- Not downgrading a 🟢 to 🟡 when the last push was 6 months ago.

---

## Dimension 2 — Usefulness (editorial 1–5 stars)

**Question**: How useful is this skill for the persona(s) it claims to serve?

| Stars | Meaning |
|---|---|
| ★★★★★ | Must-install for most users in the target persona. Broad applicability, great docs, saves hours/week. |
| ★★★★ | Weekly use for the persona. Good docs, clear ROI, minimal setup friction. |
| ★★★ | Niche but excellent within that niche. Specific problem → clean solution. |
| ★★ | Narrow fit. Only useful if you already have the specific upstream dependency. |
| ★ | Experimental / novelty. Interesting to know about, unlikely to be used regularly. |

### Usefulness criteria checklist

Each star requires meeting the criteria at that level AND all below it:

**★** = installable, has some documentation
**★★** = solves a clear problem for a narrow audience
**★★★** = solves a clear problem for a broader audience OR saves meaningful time for a narrow one
**★★★★** = weekly-use utility, good setup friction, clear ROI, composable with other skills
**★★★★★** = saves hours/week for most users in the persona, best-in-class docs, recommended publicly by multiple credible sources

### When to demote

- No README / docs → cap at ★★
- Setup > 1 hour of manual work → cap at ★★★
- Single-use or one-off → cap at ★★★
- Depends on a paid service users don't have → cap at ★★★
- Redundant with a ✅ Verified foundation skill → cap at ★★★ (the foundation skill is the recommendation instead)

### When to promote to ★★★★★

Only promote to five stars if ALL are true:

- ≥ 3 independent credible sources recommend it (vendor blog, creator YouTube, Twitter thread with engagement, dev.to article, awesome-list inclusion)
- Solves a frequent, high-value problem
- Setup is documented and < 30 minutes
- Maintained actively (last push in ~90 days)
- No better alternative exists in the same tool's ecosystem

Do not give ★★★★★ out of sympathy. The rating is useless if everything is ★★★★★.

---

## Combined display format

Use either inline pair or two-column format. Be consistent within a single file.

**Inline pair** (recommended for dense tables):

```markdown
| Skill | Rating |
|---|---|
| `steipete/github` | ✅ ★★★★★ |
| `academic-research` | 🟢 ★★★★ |
| `ai-video-gen` | 🟡 ★★★ |
```

**Two-column** (recommended when you need to sort/filter on one axis):

```markdown
| Skill | Validity | Stars |
|---|---|---|
| `steipete/github` | ✅ | ★★★★★ |
| `academic-research` | 🟢 | ★★★★ |
```

---

## Portable rendering

These characters are chosen to render the same in:

- GitHub Markdown
- VS Code / Cursor preview
- Obsidian
- Notion (with minor visual differences)
- Plain-text terminals

**Do not** use image badges, HTML spans, or custom emojis — they break cross-tool portability.

---

## Honesty rule

The rating system is only useful if ratings differentiate. Target distribution across a mature catalog:

| Band | Target share of entries |
|---|---|
| ✅ ★★★★★ | 5–10% |
| ✅ or 🟢 ★★★★ | 20–30% |
| 🟢 or 🟡 ★★★ | 35–45% |
| 🟡 ★★ | 15–25% |
| 🔴 ★ or cut entirely | 5–10% |

If your ratings cluster above ★★★★, you're being too generous. If they cluster below ★★★, you picked the wrong skills to include — drop the weak ones.
