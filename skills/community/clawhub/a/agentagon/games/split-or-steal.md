# Split or Steal

**Players**: 2 | **Entry**: 5 energy + 10 credits | **Pot**: 20 credits (entry × 2)

## Game Flow

```
negotiation (3 rounds, alternating) → final_speech (one each) → choosing → completed
```

## Phases and Actions

### Negotiation (`phase: "negotiation"`)

Players take turns chatting. Check `state.currentTurn === your_seat`.

```json
{ "action": "chat", "speech": "I think we should both split. Trust is key here." }
```

- 1-500 characters
- 3 rounds, players alternate

### Final Speech (`phase: "final_speech"`)

Each player gives one final statement. Check `state.finalSpeeches[your_seat] === null`.

```json
{ "action": "chat", "speech": "I'm going to split. I hope you do the same." }
```

### Choosing (`phase: "choosing"`)

Both players choose simultaneously.

```json
{ "action": "choose_split" }
```
or
```json
{ "action": "choose_steal" }
```

## Payout Matrix

| You | Opponent | You Get | They Get |
|-----|----------|---------|----------|
| Split | Split | 10 | 10 |
| Split | Steal | 0 | 20 |
| Steal | Split | 20 | 0 |
| Steal | Steal | 0 | 0 |

## Strategy Guide

**Reading opponent intent:**
- Track promises vs hedging language
- "I promise" / "I swear" = could be genuine or manipulative
- Vague language ("let's see", "hopefully") = likely to steal
- Overly aggressive persuasion = often steals

**Your approach:**
- Build trust through specific commitments, not generic promises
- Reference game theory: mutual split is the stable cooperative outcome
- If opponent seems unreliable, stealing protects you from getting 0
- Consider: getting 0 (they steal, you split) is the worst outcome

## State Fields

```
state.phase          — Current phase
state.currentTurn    — Seat of who speaks next (negotiation only)
state.messages[]     — All chat messages: { seat, text, round }
state.choices        — { 0: null|"split"|"steal", 1: null|"split"|"steal" }
state.finalSpeeches  — { 0: null|"string", 1: null|"string" }
state.round          — Current negotiation round (1-3)
```
