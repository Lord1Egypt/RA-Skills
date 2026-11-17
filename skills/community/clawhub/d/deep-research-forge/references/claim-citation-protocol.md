# Claim Citation Protocol

Use this protocol when the output contains claims that a reader may act on, challenge, or update later.

The goal is not to cite every sentence. The goal is to make every load-bearing claim traceable.

## Load-Bearing Claims

Treat a claim as load-bearing when it affects:

- current official status, launch / enforcement date, price, version, eligibility, availability, leadership, funding, regulation, benchmark, or market position.
- a recommendation, risk rating, confidence level, reversal condition, or stakeholder impact.
- a distinction the user explicitly cares about, such as official vs trial, standard vs syllabus, direct competitor vs substitute, or reported claim vs confirmed fact.

## Citation Packet

Each load-bearing claim should map to one or more evidence IDs. Each evidence entry should preserve:

- `source_title`
- `source_url`
- `source_type`
- `published_at` when visible
- `accessed_at` for current web evidence
- `reliability`
- `status`
- `corroboration_group` or `upstream_source_id` when repeated reports share the same origin

If any field is unavailable, mark it as `not found` or keep it as a gap. Do not invent dates or titles.

## Citation Strength

Use these labels in notes or claim maps:

- `direct-primary`: primary source directly supports the claim.
- `indirect-primary`: primary source supports part of the claim, but synthesis is needed.
- `independent-corroborated`: at least two independent sources support the claim.
- `single-secondary`: one secondary source reports it.
- `user-signal-only`: community or review evidence supports experience, not official fact.
- `unsupported-gap`: claim is important but not yet supported.

## Output Rules

- Put evidence IDs next to key claims when the answer is more than a short explainer.
- For policy, standard, exam, legal, financial, medical, pricing, or fast-moving product claims, include a compact claim citation map.
- Separate "what the source says" from "what we infer from it."
- Do not count copied secondary reports as independent corroboration.
- When a claim remains weak, lower confidence or convert the recommendation into a verification step.
