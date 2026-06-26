# CLAWHUB.md entry templates

Use these shapes when appending to repo root **`CLAWHUB.md`** (no secrets). IDs are optional; narrative bullets are enough.

---

## Success (numbered list item)

```markdown
N. **Short title**  
   - One concrete fact or working pattern.  
   - Optional: file path or curl.  
```

Example:

```markdown
11. **TIP-20 mint after `createSync`**  
   - Grant **`ISSUER_ROLE`** before **`mintSync`** if `hasRole(issuer)` is false; use **`writeContractSync(grantRole)`** not **`grantRolesSync`** (envelope `0x76` vs browser wallets).  
   - **`src/tempoTip20Launch.ts`**
```

---

## Failure (subsection)

```markdown
### N) Short title

**Symptom**
- What the user or agent saw.

**Cause**
- Root cause (stale server, wrong role, wrong network).

**Fix**
- Actionable steps; link to code or doc.
```

---

## One-line promotion (from a PR)

```markdown
- **PR #NN**: [area] — [one sentence]; see `path/to/file`.
```

---

## Related

- **`CLAWHUB.md`** in repo (canonical log)
- **Self-improving-agent** style: `.learnings/*.md` — optional; see **`assets/learnings/`** in this skill for stricter LRN/ERR formats if you maintain a parallel log
