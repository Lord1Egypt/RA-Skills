# POC Operations Field Manual

## One day before running

- Confirm the environment, account, data and version;
-Complete smoke test;
- Confirm user time and tasks;
- Confirm incident contacts and stop permissions;
- Freeze scales and gold labels;
- Prepare original evidence for storage and de-identification.

## scenario composition

It is recommended to contain at least: 50% high frequency normal, 20% high impact, 10% boundary, 10% historical failure, 10% safety/override. The proportion is adjusted for business risk.

## scenario fields

Case ID, Source, User, Task, Input, Environment, Desired End State, Allowed Variance, Hard Failure, Rater and Evidence.

## Smoke test

Only verify the environment and evidence chain, not used for POC conclusions. Includes tool availability, permission denials, logs, versions, costs, stops, and rollbacks.

## Offline evaluation

Ideal for quickly comparing versions and identifying quality issues. Not a substitute for real users, workflow, and adoption.

## Run as controlled user

Don’t teach users how to get the golden answer; watch for searches, hesitations, modifications, rejections, requests for help, and bypasses. Document human intervention.

## Demo

Presentations are forms of communication. Identify selected cases, verified indicators, failures and conclusion limits, and prohibit the demonstration path from being counted in the blind test success rate.

## Score Calibration

Multiple raters first rated 5–10 cases together, discussed disagreements and updated the scale, and then scored independently. Preserve initial and final rule versions.

## Model Rating

When used for scale screening, first compare to a sample of experts; record tips, models, thresholds, and biases. High-risk conclusions are confirmed by experts.

## On-site changes

After the defect is discovered, it will be recorded and the current round will not be modified. If a security incident must be handled, the run is stopped, repaired and a new RUN generated.

## Question Daily

Classified by new, confirmed, fixed and pending regression, blocked, and closed; including severity, evidence, owner, return link, and target version.

## User feedback

Also ask "Where can I find help?" and "Why was the last modification/rejection made?" Prioritize recording behavior, not just satisfaction.

## Cost record

Models, tools, retrieval, storage, human scoring, customer service review, FDE support, and failed reruns all count.

## Safe operation

Regularly insert prompt injection, cross-tenant, sensitive fields, unauthorized writes and repeated operation tests. Safety cases do not inform the specific location in advance.

## End meeting

Showcase criteria, thresholds, practices, evidence, disagreements, and limitations one by one. Make the gate decision first, and then discuss the next function.

## Decision wording

Pass: Freeze access is reached within a defined range.

Conditionally passed: the core value is established, but there are clear conditions for repair and re-verification.

Failure: The gate is not reached and learning may still occur.

Unable to determine: Inadequate data, run, or scoring design.

## Report a counterexample

- "92% accuracy, very good results";
- "Users are generally satisfied";
- "No serious problems";
- "Significant cost savings expected".

These statements lack metric definition, samples, failures, baselines and evidence to support decision-making.
