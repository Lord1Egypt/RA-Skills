# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code skill called **Factory Floor** — a startup operating system for prioritization and execution. It combines Goldratt's constraint thinking, Maurya's customer factory model, Sharp's brand growth laws, Ritson's marketing strategy discipline, and a strategic reasoning layer (Rumelt, Clausewitz, Dixit & Nalebuff), with JTBD as the strategic intelligence layer underneath.

## Architecture

The skill is **decision-tree routed**: SKILL.md is a thin router (~130 lines) with a decision tree that identifies the startup's stage and constraint, then instructs Claude to read the appropriate stage file. This keeps context lean — a day-1 founder never sees fever charts, and a year-3 company doesn't re-read the napkin test.

### SKILL.md (the router)

Contains: frontmatter, decision tree (stage routing + funnel break scan), symptom → constraint map, reference routing table, inline GOLEAN summary, and the core rule. **After triage, SKILL.md tells Claude to read one of the stage files.**

### stages/

Stage files are self-contained — each integrates the relevant parts of JTBD, Goldratt, Maurya, Sharp, and Ritson where they're needed, rather than referencing them as separate reading.

- `pre-revenue.md` — Day 1 through first paying customer. Problem validation, the five tests (not-not, job, Lean Canvas, napkin, Mafia Offer), JTBD basics (forces, canvas), solo-founder subordination, day-1 weekly review, worked example (killing an idea on the napkin).
- `restart.md` — Had customers, lost them, now at zero. Forensics-first approach (product failure vs. fit failure vs. sales execution failure), churned customer interviews, restart sequence, graduation criteria.
- `growth.md` — Post-revenue through ~$100K MRR, team under ~10. Full constraint cascade, "Before You Build" check (Sharp + Ritson integrated), brand building vs. activation, Goldratt's five steps + subordination matrix, customer factory, GOLEAN, WIP/buffer/estimation, JTBD in the weekly rhythm, two worked examples (growth stall + constraint shift), light weekly review.
- `scaling.md` — $100K+ MRR, 10+ people. Policy constraints, multi-team constraint work, hiring as elevation, multi-quarter initiatives, business model constraints, full CCPM + buffer management, timeline communication, worked example (hidden policy constraint), full weekly review.

### references/

Deep-dive concept files. Claude reads these when more detail is needed on a specific framework. Operational content (protocols, checklists, weekly routines) lives in the stage files; references hold theory, definitions, and methodology.

- `intake.md` — First conversation questions, funnel break scan protocol, vague-answer handling
- `misdiagnoses.md` — Nine common wrong diagnoses and the questions that expose them
- `coaching-patterns.md` — Diagnostic questions by situation, anti-patterns with probes, closing the loop
- `pillar-goldratt.md` — Theory of Constraints (Five Focusing Steps, throughput accounting, Little's Law, Drum-Buffer-Rope, context-switching tax)
- `pillar-maurya.md` — Customer Factory (blueprint, stage-constraint mapping, GOLEAN, referral loops, local vs. global optimization, Innovator's Bias/Gift)
- `pillar-sharp.md` — Mental & Physical Availability (CEPs, distinctiveness, reach vs frequency, laws of brand growth, CEP mapping exercise, physical availability audit, operational protocol)
- `pillar-ritson.md` — Marketing Strategy Discipline (Diagnosis → Strategy → Tactics, STP, positioning, differentiation + distinctiveness, Binet & Field budget allocation, brand codes, market orientation, positioning sprint)
- `jtbd.md` — Jobs To Be Done (forces of progress, switch interviews, Ulwick's job map, opportunity scoring, positioning from JTBD, demand generation vs. capture, hiring/firing)
- `pillar-strategy.md` — Strategic Thinking (Rumelt's kernel/crux/bad strategy signs, Clausewitz's fog/friction/center of gravity/culminating point, Dixit & Nalebuff's game theory for competitive dynamics)
- `estimation.md` — Estimation theory (why estimates fail, CCPM method, PERT, cycle time, Monte Carlo, cone of uncertainty, buffer sizing methods)
- `weekly-review.md` — Weekly review templates by stage
- `weekly-diagrams.md` — Customer Factory Funnel diagram template for the weekly constraint review

### scripts/

- `render-diagram.mjs` — Renders `.mmd` Mermaid files to SVG using `beautiful-mermaid`. Requires `npm install` in `scripts/` first.
- `package.json` — Declares `beautiful-mermaid` dependency

## Key Relationships

The framework flows in one direction: **JTBD provides the strategic intelligence** (what job does the customer hire you to do?), **Goldratt provides the system-level thinking** (find the constraint, exploit/subordinate/elevate), **Maurya maps it to the startup business model** (customer factory steps as the "machines"), **Sharp provides the diagnosis when the constraint is at the top of the funnel** (nobody knows you exist), **Ritson provides the strategic discipline that makes the other frameworks coherent** (diagnosis before strategy, strategy before tactics), and **Rumelt, Clausewitz, and Dixit & Nalebuff provide the strategic reasoning layer** (is this actually a strategy? how to operate under uncertainty, and what the other side will do).

JTBD sits underneath the other five — struggling moments are Category Entry Points, the four forces explain why customers flow (or don't) through the factory, and under-served outcomes tell you what to build.

When editing, maintain this hierarchy. Changes to core concepts in one pillar should be checked against the others for consistency. The stage files synthesize all six pillars — they should never contradict the reference files.

## Content Ownership

Operational content (what to do, when, how) belongs in stage files. Conceptual content (theory, definitions, methodology, research) belongs in references. If content appears in both places, the stage file is the authoritative operational version and the reference is the authoritative conceptual version. Don't duplicate — cross-reference.
