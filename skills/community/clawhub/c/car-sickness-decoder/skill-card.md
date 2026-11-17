## Description:

Use when a child (or adult) gets carsick — before a trip to prevent it, mid-episode to manage it, or when episodes keep repeating. Classifies the trigger pattern (classic motion sickness vs vestibular migraine vs anxiety-conditioned), builds the seating/food/timing/cadence protocol, prices OTC antiemetic dosing by weight with hard age gates, and flags the red flags that need a doctor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Caregivers and adults use this skill to classify carsickness patterns, plan prevention and mid-episode care for trips, review age- and weight-banded over-the-counter medication guidance, and identify symptoms that call for medical care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security assessment reports that the dosing tool may return a dose when age is omitted, creating a risk of an inappropriate dose, especially for a child.

Mitigation: Consider the assessment's DO_NOT_INSTALL recommendation. If using the skill, do not rely on medication guidance without confirming age; check the product label and consult a pediatrician or pharmacist before giving medication.

## Reference(s):

- [ClawHub release](https://clawhub.ai/voronindenis5/skills/car-sickness-decoder)
- [Motion Sickness: Mechanism, Classification, Protocols, Dosing](artifact/references/motion-sickness-guide.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Analysis]

**Output Format:** [Plain-text triage results, trip plans, medication guidance, and episode-log summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational guidance; directs users to medical care for listed red flags.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
