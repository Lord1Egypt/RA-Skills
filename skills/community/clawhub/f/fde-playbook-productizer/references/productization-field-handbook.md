# FDE Productization Field Manual

## Productization is not about organizing documents

Productization requires new teams to discover, understand, configure, execute, validate, support, and evolve assets where the recurring benefits outweigh the maintenance costs.

## Identify duplicates

Document each deliverable: issues, users, tasks, inputs, rules, systems, risks, value, costs, failures, and variants.

Only the same technology does not count as business commonality; only the same customer language does not count.

## Variant classification

- Field mapping: configuration;
- Threshold/role: policy configuration;
- System API: Adapter;
- Domain policy: independent knowledge and rules;
- Core mission differences: may be different assets;
- Differences in risk levels: different governance models.

## Asset selection problem

- who consumes;
- where are the recurring costs;
- Need execution or guidance;
- Whether it relies on tools or code;
- Update frequency;
- How to verify;
- who maintains;
- Impact of failure.

## Script assets

Ideal for repetitive collaboration and decision-making processes. There must be entry conditions, roles, steps, gates, templates, exceptions and exits.

## Template assets

Suitable for handovers with stable structure but changing content. The template must contain field descriptions and quality rules, and cannot have an empty table.

## Component assets

Suitable for repetitive technical skills. Contains interfaces, versions, permissions, bugs, tests, observations, dependencies and compatibility.

## Skill Assets

Ideal for repetitive model-driven tasks. Includes triggers, workflows, tools, guardrails, assessments, and platform adaptation.

## Evaluate assets

Suitable for repeated judgments of similar quality. Contains sources, licenses, gold labels, scales, editions, contamination controls and updates.

## Product capability candidates

Cross-customer stability issues need to be weighed against value, returns to scale, maintenance commitments and roadmap. FDE submits evidence and does not make unilateral product decisions.

## Reuse experiments

Select an FDE that was not involved in the original project and an adjacent but different scenario; restrict it to only assets; record inquiries from the original author, configuration time, failures, results, and feedback.

## Reuse indicators

- Find the correct asset time;
- Configuration and delivery cycle;
- Number of times supported by the original author;
- First pass rate;
- Quality and value after reuse;
- Added number of new variants;
- Maintenance costs.

## Asset catalog fields

Name, Purpose, Trigger, N/A, Maturity, Version, Owner, Dependencies, Risk, Assessment, Recently Used, Supported, and Retired.

## Merge and Split

If multiple assets have the same core but different configurations, they will be merged; if the responsibilities, permissions or user results are different, they will be split. Don't build giant universal assets.

## Version

Document breaking, compatibility and revision changes; significant permissions, input or output changes require migration notes and re-evaluation.

## Feedback closed loop

Every reuse commit: success, failure, new cases, variants, customer restrictions, and suggestions. Real failures are prioritized for regression.

## Retirement

Trigger: No one uses, no one maintains, value decreases, risk increases, platform is incompatible, replaced by standard capabilities or license expires.

## Customer information cleaning

Remove names, data, internal policies, credentials, and proprietary configuration; retain abstract structures and authorized synthetic examples.

## Open source release

- Clarify license and source;
- Does not contain keys, customer data and dangerous default permissions;
- List of compatible platforms and dependencies;
- Provide minimal usage examples and evaluations;
- Conduct security review of scripts and external links;
- Maintenance releases, problem feedback and security reporting channels.

## Roadmap feedback package

Include cross-customer issues, evidence, value, current customization costs, commonalities/variations, advisory capabilities, risks, alternatives, and priorities rather than a “customer needs both.”

## Productization meeting

Involved in FDE, Product, Engineering, Security, Support and Commercial. Examine the evidence threshold first, and then discuss asset form and priority.

## Failure counterexample

- Copy the code after the single customer is successful;
-Make all variants into switches;
- No reuse testing for new users;
- Only development savings are calculated, not maintenance;
- Entering the standard directory without a Owner;
- Hide failures and applicability boundaries for the sake of publicity.
