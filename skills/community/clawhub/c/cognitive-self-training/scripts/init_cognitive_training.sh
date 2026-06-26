#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
STORE="$ROOT/.cognitive-training"
TODAY="$(date +%Y-%m-%d)"
MONTH="$(date +%Y-%m)"

mkdir -p "$STORE/inbox" "$STORE/daily" "$STORE/dreams" "$STORE/archive"

create_if_missing() {
  local path="$1"
  local content="$2"
  if [ ! -f "$path" ]; then
    printf "%s\n" "$content" > "$path"
  fi
}

create_if_missing "$STORE/README.md" "# Cognitive Training Store

This directory stores agent learning, recall cards, concept links, mistakes, and daily strategy.
Do not store secrets, tokens, private keys, raw environment dumps, or sensitive personal data."

create_if_missing "$STORE/principles.md" "# Principles

Durable rules promoted from repeated successful recall or user-confirmed importance.
"

create_if_missing "$STORE/strategy.md" "# Strategy

## Strategy $TODAY
- Focus:
- Why it matters:
- Practice:
- Prevention rule:
- Next evidence to seek:
"

create_if_missing "$STORE/schedule.md" "# Dream Schedule

Status: manual
Time: not-set
Timezone: local
Scope: project
Last configured: $TODAY

Prompt:
Run cognitive-self-training dream review. Read today's cognitive training files, randomly select an enabled dream style, write the result with exactly these top-level sections: Dream Review, Dream Recurrence Statement, Tian-Dao Deduction, Research Hypotheses, Tomorrow's Practice, Store Updates, Summary Narrative. Create due recall cards, update graph links, and propose tomorrow's strategy. Do not store secrets or raw private transcripts.
"

create_if_missing "$STORE/dream-style-config.md" "# Dream Style Config

Mode: random
Fixed style: research-lab
Enabled styles:
- joyful-festival
- elegy-rain
- school-classroom
- research-lab
- field-training
- battlefield-command
- courtroom-trial
- sea-voyage
- mountain-pilgrimage
- marketplace-negotiation
- workshop-forge
- hospital-rounds
- library-archive
- city-crisis-room
- theater-rehearsal
- desert-caravan
- monastic-scriptorium
- imperial-council
- frontier-outpost
- observatory-night
- archaeological-dig
- garden-cultivation
- engineering-bridge
- newsroom-deadline
- diplomatic-summit
- village-council
- train-journey
- kitchen-service
- disaster-drill
- startup-garage

Weights:
- research-lab: 2
- field-training: 2
- school-classroom: 2
- library-archive: 2
- joyful-festival: 1
- elegy-rain: 1
- battlefield-command: 1
- courtroom-trial: 1
- sea-voyage: 1
- mountain-pilgrimage: 1
- marketplace-negotiation: 1
- workshop-forge: 1
- hospital-rounds: 1
- city-crisis-room: 1
- theater-rehearsal: 1
- desert-caravan: 1
- monastic-scriptorium: 1
- imperial-council: 1
- frontier-outpost: 1
- observatory-night: 1
- archaeological-dig: 1
- garden-cultivation: 1
- engineering-bridge: 1
- newsroom-deadline: 1
- diplomatic-summit: 1
- village-council: 1
- train-journey: 1
- kitchen-service: 1
- disaster-drill: 1
- startup-garage: 1

Safety fallback: research-lab
"

create_if_missing "$STORE/cards.md" "# Cards

Spaced-repetition cards. Review entries with Due <= today.
"

create_if_missing "$STORE/graph.md" "# Concept Graph

Track causal links, analogies, applications, and counterexamples.
"

create_if_missing "$STORE/mistakes.md" "# Mistakes

Recurring mistakes, root causes, and prevention rules.
"

create_if_missing "$STORE/inbox/$TODAY.md" "# Inbox $TODAY

Raw captures for today's learning.
"

create_if_missing "$STORE/daily/$TODAY.md" "# Daily Cognitive Review $TODAY

## Learned Today

## Recall Results

## Connections

## Mistakes Or Gaps

## Tomorrow Strategy

## Promotions
"

create_if_missing "$STORE/dreams/$TODAY.md" "# Dream Review $TODAY

## Dream Review

## Dream Recurrence Statement

## Tian-Dao Deduction

## Research Hypotheses

## Tomorrow's Practice

## Store Updates

## Summary Narrative
"

create_if_missing "$STORE/archive/$MONTH.md" "# Archive $MONTH

Retired, stale, or low-value training entries.
"

echo "Initialized cognitive training store at $STORE"
