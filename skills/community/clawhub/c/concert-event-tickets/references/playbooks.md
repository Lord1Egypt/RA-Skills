# Playbooks — concert-event-tickets

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Concerts

**Trigger:** "concert tickets"

```bash
flyai search-poi --city-name "{city}" --category "演出赛事"
```

**Output emphasis:** Live performances and concerts.

---

## Playbook B: Sports Events

**Trigger:** "sports tickets"

```bash
flyai search-poi --city-name "{city}" --category "体育场馆"
```

**Output emphasis:** Sports events and venues.

---

## Playbook C: Theater

**Trigger:** "theater show"

```bash
flyai search-poi --city-name "{city}" --category "剧院剧场"
```

**Output emphasis:** Theater and drama shows.

---

