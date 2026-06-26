# Playbooks — airport-pickup-service

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Airport Pickup

**Trigger:** "airport transfer"

```bash
flyai keyword-search --query "机场接送 {city}"
```

**Output emphasis:** Airport transfer services.

---

## Playbook B: Private Car

**Trigger:** "private airport car"

```bash
flyai keyword-search --query "机场专车 {city}"
```

**Output emphasis:** Private car service.

---

