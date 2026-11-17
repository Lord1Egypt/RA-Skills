# Preferences Template — Brief

Create `~/Clawic/data/brief/preferences.md` with the structure below when the first feedback signal arrives. Learned format preferences only, updated from explicit feedback; one preference per line, each tagged with a level. Declared preferences do not belong here — they go to `config.yaml` (see `setup.md`).

**Rules:**
- Record only explicit signals ("too long", "where are the numbers?") — never inferences from silence
- 2+ consistent signals → mark `pattern`
- Explicit user approval → `confirmed`; never promote silently
- `locked` only after a confirmed preference is reinforced across multiple briefs
- One contradicting signal demotes a `pattern`; a contradicted `confirmed` → ask, never flip silently
- Signal-to-dimension mapping and full level rules: `dimensions.md`

---

### Scope
<!-- What they typically need briefs for. Format: "type: context (level)" -->

### Content
<!-- What to include/exclude. Format: "element: preference (level)" -->

### Structure
<!-- How they like briefs organized. Format: "aspect: preference (level)" -->

### Format
<!-- Delivery preferences. Format: "dimension: preference (level)" -->

### Timing
<!-- When they want briefs. Format: "trigger: timing (level)" -->

### Depth
<!-- Detail level preferences. Format: "type: depth (level)" -->

---

## Per-Type Overrides

Different brief types may have different preferences:

### Executive Briefs
<!-- Overrides for executive summaries -->

### Project Briefs
<!-- Overrides for project updates -->

### Meeting Briefs
<!-- Overrides for meeting prep -->

### Handoff Briefs
<!-- Overrides for handoffs -->

---

*Empty sections = defaults apply. Check this file before writing any brief.*
