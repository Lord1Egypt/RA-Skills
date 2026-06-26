# Electric Guitar Progress Tracking

Reference for file structure and logging format.

## Workspace Structure

```
~/electric-guitar/
├── repertoire.md      # Songs learned and in progress
├── sessions/
│   └── YYYY-MM.md     # Monthly practice logs
├── technique.md       # Scales, techniques, exercises
└── goals.md           # Short and long-term goals
```

## Repertoire Format

```markdown
# repertoire.md

## Currently Learning
- Comfortably Numb solo — Pink Floyd, started 2024-01-15
  - Struggle: bending vibrato in intro
  - Next: second solo phrasing

- Pride and Joy — SRV, started 2024-02-01
  - Working on: shuffle rhythm consistency

## Completed
- Smells Like Teen Spirit — Nirvana (1 week)
- Sweet Child O' Mine — GNR (intro took 3 weeks)
- Back in Black — AC/DC (rhythm focus)

## Want to Learn
- Cliffs of Dover — Eric Johnson (way above level, someday)
- Texas Flood — SRV (need better bending first)
```

## Technique Tracking

```markdown
# technique.md

## Scales (by position)
| Scale | Pos 1 | Pos 2 | Pos 3 | Pos 4 | Pos 5 |
|-------|-------|-------|-------|-------|-------|
| A minor pent | ✅ | ✅ | 🔄 | ❌ | ❌ |
| A major pent | ✅ | 🔄 | ❌ | ❌ | ❌ |
| A natural minor | 🔄 | ❌ | ❌ | ❌ | ❌ |

## Techniques
- Alternate picking: 16ths clean at 100 BPM
- Bending: half step reliable, whole step needs work
- Vibrato: inconsistent speed control
- Sweep picking: not started

## Exercises in Rotation
- Spider chromatic exercise (left hand)
- Paul Gilbert string skipping
- Pentatonic sequences (3s and 4s)
```

## Session Log Format

```markdown
# sessions/2024-02.md

## 2024-02-15 (45 min)
- Warm-up: chromatic spider, 5 min
- Comfortably Numb: intro bends, slow
- Worked vibrato on sustained bends
- Still inconsistent — need more isolated practice

## 2024-02-14 (30 min)
- Pride and Joy rhythm only
- Shuffle feel improving with click
- Tried at 90% tempo, sloppy — back to 80%
```

## Goals Format

```markdown
# goals.md

## This Month
- All 5 pentatonic positions connected
- Whole step bends in tune consistently
- Learn one blues shuffle song

## Longer Term
- Jam confidently over a 12-bar blues
- Build a 10-song setlist for open mic
- Start learning some jazz voicings
```

## Logging Triggers

Prompt user to log when:
- They mention practicing or learning songs
- They nail a new technique or tempo
- They struggle with something specific
- Weekly check-in if no recent logs
