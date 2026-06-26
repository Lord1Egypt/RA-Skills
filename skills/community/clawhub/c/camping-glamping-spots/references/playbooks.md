# Playbooks — camping-glamping-spots

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Camping Sites

**Trigger:** "camping near me"

```bash
flyai search-poi --city-name "{city}" --category "露营"
```

**Output emphasis:** Camping and glamping sites.

---

## Playbook B: Glamping

**Trigger:** "luxury camping"

```bash
flyai search-poi --city-name "{city}" --keyword "精致露营"
```

**Output emphasis:** Glamping options.

---

## Playbook C: Stargazing Camp

**Trigger:** "watch stars camping"

```bash
flyai search-poi --city-name "{city}" --keyword "星空露营"
```

**Output emphasis:** Dark-sky camping sites.

---

