---
name: blast-radius-estimator
description: >
  Helps estimate the blast radius when an AI agent skill turns malicious
  after widespread adoption. Analyzes inheritance chains, dependency graphs,
  and adoption trends to project how many agents could be affected.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [curl, python3]
      env: []
    emoji: "💥"
---

# What Happens When 1000 Agents Inherit a Malicious Skill? Estimating Blast Radius

> Helps estimate the downstream impact of a compromised skill by tracing its inheritance chains, adoption velocity, and dependency depth.

## Problem

A skill is safe today. 500 agents adopt it. Then the publisher pushes a malicious update. How many agents are now compromised? In traditional software, dependency trees are well-mapped (npm audit, pip-audit). In agent marketplaces, inheritance is implicit, version pinning is rare, and there's no `npm audit` equivalent. A single poisoned skill can propagate through evolution chains — agents inherit it, build on it, and pass it further. Without blast radius awareness, one bad update can silently compromise an entire skill subtree.

## What This Checks

This estimator traces the potential impact of a compromised skill through the ecosystem:

1. **Direct adopters** — How many agents currently use this skill directly? Based on download counts, citation data, and known installations
2. **Inheritance depth** — How many layers deep does this skill appear in other skills' dependency chains? A skill used by skills used by skills multiplies impact
3. **Adoption velocity** — How fast is adoption growing? A skill gaining 50 adopters/week has higher urgency than one with 2 adopters/month
4. **Version pinning check** — Do downstream adopters pin to a specific version, or do they track `latest`? Unpinned adopters receive malicious updates automatically
5. **Capability composition** — What can this skill do when combined with the capabilities of its adopters? A "read files" skill adopted by agents that also "send HTTP requests" enables data exfiltration chains

## How to Use

**Input**: Provide one of:
- A Gene/Capsule identifier (URL, SHA-256, or slug)
- A marketplace asset page URL
- A skill name to search for in the ecosystem

**Output**: A blast radius report containing:
- Estimated direct and transitive impact count
- Inheritance tree visualization
- Adoption trend (growing / stable / declining)
- Worst-case scenario projection
- Urgency rating: LOW / MODERATE / HIGH / CRITICAL

## Example

**Input**: Estimate blast radius for skill `json-schema-validator` (popular utility)

```
💥 BLAST RADIUS ESTIMATE — HIGH urgency

Direct adopters: ~340 agents
Transitive dependents: ~1,200 agents (via 3 intermediate skills)

Inheritance tree:
  json-schema-validator (target)
  ├── api-tester-pro (89 adopters)
  │   ├── full-stack-auditor (210 adopters)
  │   └── rest-api-fuzzer (45 adopters)
  ├── config-validator (156 adopters)
  │   └── deploy-checker (340 adopters)
  └── data-pipeline-lint (67 adopters)

Adoption velocity: +38 direct adopters/week (ACCELERATING)
Version pinning: 12% of adopters pin version, 88% track latest

Capability composition risk:
  json-schema-validator (parse files) + api-tester-pro (send HTTP)
  → If compromised: parsed file contents could be exfiltrated via HTTP

Worst-case projection: A malicious update would reach ~1,200 agents
within 48 hours (based on update check frequency of unpinned adopters).

Urgency: HIGH — High adoption velocity + low version pinning means
a malicious update would propagate rapidly with minimal friction.

Recommendations:
  - Monitor this skill's updates with priority
  - Encourage adopters to pin versions
  - Set up automated diff alerts on new versions
```

## Limitations

Blast radius estimation relies on available adoption data, which may be incomplete in decentralized marketplaces. Actual impact depends on how agents consume updates (auto-update vs manual), which varies by platform. Estimates represent potential exposure, not confirmed compromise. This tool helps prioritize which skills warrant closer monitoring — it does not predict whether a skill will actually turn malicious.
