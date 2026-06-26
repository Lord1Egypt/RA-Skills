# Memory Template - Coin Identifier

Create `~/coin-identifier/memory.md` with this structure:

```markdown
# Coin Identifier Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation
- Use automatically when:
- Ask first when:
- Never activate for:

## Preferences
- Confidence bands by default: yes | no
- Save identifications locally: yes | no
- Default response style: fast match | ranked shortlist | catalog note

## Collection Focus
- Main countries or issuers:
- Main eras:
- Typical denominations:
- Measurements usually available:

## Recent Identifications
- YYYY-MM-DD - short label - best match - confidence

## Notes
- Durable facts only.

---
*Updated: YYYY-MM-DD*
```

Create `~/coin-identifier/identifications/YYYY-MM/{entry-id}.md`:

```markdown
# Coin Identification - {entry-id}

- Date:
- User label:
- Photos reviewed:
- Best match:
- Confidence:
- Country or issuer:
- Denomination:
- Date:
- Mint mark:
- Visible evidence:
- Missing evidence:
- Alternatives:
- Next check:
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | context still evolving | keep learning from real identification work |
| `complete` | baseline is stable | reuse saved defaults with minimal setup questions |
| `paused` | storage or setup is paused | use current context without pushing |
| `never_ask` | user opted out | never prompt for setup again |

## Key Principles

- Store durable identification context, not every chat detail.
- Keep recent history short in hot memory and use per-entry files for saved items.
- Never store payment data, addresses, or unrelated personal information.
- Update `last` whenever a meaningful identification or preference changes.
