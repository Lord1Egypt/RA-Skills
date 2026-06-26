# Drakeling API Reference (Skill-Permitted Endpoints)

## GET /status

Returns the creature's current state.

**Request:**

```
GET http://127.0.0.1:52780/status
Authorization: Bearer <token>
```

**Response (200):**

```json
{
  "name": "Ember",
  "colour": "gold",
  "lifecycle_stage": "juvenile",
  "mood": 0.65,
  "energy": 0.48,
  "trust": 0.72,
  "loneliness": 0.15,
  "state_curiosity": 0.55,
  "stability": 0.60,
  "budget_exhausted": false,
  "budget_remaining_today": 8500
}
```

**Response (404):** No creature exists yet.

---

## POST /care

Sends a symbolic care event to the creature.

**Request:**

```
POST http://127.0.0.1:52780/care
Authorization: Bearer <token>
Content-Type: application/json

{ "type": "gentle_attention" }
```

Valid types: `gentle_attention`, `reassurance`, `quiet_presence`, `feed`.

**Response (200):**

```json
{
  "response": "...I felt you nearby. That was nice.",
  "state": {
    "mood": 0.70,
    "energy": 0.48,
    "trust": 0.72,
    "loneliness": 0.0,
    "state_curiosity": 0.55,
    "stability": 0.60
  }
}
```

The `response` field contains the creature's expression in its own words. It may be `null` if the creature's daily budget is exhausted.
