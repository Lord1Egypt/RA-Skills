# Enterprise Problem Discovery Field Manual

## 1. Research plan

The research goal is not to "gather requirements" but to reduce uncertainty about users, tasks, problems, values, and constraints.

The plan must at least state:

- Decisions to be changed;
- Current maximum hypothesis;
- What role evidence is required;
- Use interviews, observations, diaries or samples;
- limitations of each method;
- When evidence is considered sufficient.

## 2. Sampling roles

Cover at least: high-frequency users, low-frequency users, novices, experts, rejecters, supervisors, downstream recipients, technology/data, security/compliance.

Don’t just interview the most active “champions.” They are generally more tolerant of complexity and better able to work around problems.

## 3. 60-minute interview structure

1. 5 minutes: Role, responsibilities and recent work background;
2. 20 minutes: Step-by-step playback of the latest real mission;
3. 10 minutes: exceptions, waiting, rework and manual judgment;
4. 10 minutes: Existing tools, alternatives, and switching costs;
5. 10 minutes: Outcomes, impacts and consequences of not addressing;
6. 5 minutes: Verifiable materials, follow-up contacts, and confirmation.

## 4. Behavior questioning

- "Please open the most recent one and show it to me."
- "What did you order next?"
- "Why stop here?"
- "How do you know it's right?"
- "If it's wrong, who will find out first?"
- "What was the last exception?"
- "Which step should I ask someone else about?"
- "Which fields do you never trust?"
- "What private form or chat did you use?"
- "Who does the information go to when completed?"

## 5. Avoid inducement

Avoid: “Would you be able to do this much faster if it was automatically generated?”

Change the question: "How long did this step take each of the past three times? Why is it different?"

Avoid: “What is your biggest pain point?”

Ask instead: “Where did the latest rework begin? What were the consequences?”

## 6. On-site observation records

Record each step: timestamp, role, action, system, input, judgment, waiting, copy and paste, error, help, control point and result.

Distinguish between: the process described by users, the process specified in SOP, and the actual observed process.

## 7. Log analysis

First confirm the indicator definition, time window, missingness, duplication, label quality and selection bias.

Recommended segmentation: role, task type, difficulty, channel, shift, customer level, exception type and result.

The mean may mask the long tail, at least look at the median, quantiles, distribution and failure samples.

## 8. Problem clustering

Cluster according to real tasks and root causes, not according to function words proposed by customers.

For example, "need to search, need automatic reply, need intelligent Q&A" may all belong to "cannot quickly find the current effective policy."

## 9. Value chain

From task improvement to business results:

```text
Reduce lookups → Reduce processing time → Increase queue capacity → Improve response SLA
```

Each arrow is a hypothesis, requires data, and should not be written directly to determine ROI.

## 10. Constraint Map

- Technology: legacy systems, interfaces, performance, data quality;
- Risks: privacy, security, legal affairs, compliance, fairness;
- Organization: responsibilities, budget, procurement, motivation, support;
- Users: skills, trust, accessibility, networks and devices;
- Commercial: Time windows, customer commitments, strategic priorities.

## 11. Candidate comparison

Compare problem evidence, business impact, user frequency, verifiability, data preparation, customer input, risk and simpler alternatives.

Do not increase the priority because of "good AI display effect".

## 12. Discovery Workshop

Recommended 90 minutes:

1. Share evidence without first arguing for solutions;
2. Draw the current workflow;
3. Identify facts, assumptions and conflicts;
4. Write 2–4 problem statements;
5. Disproof and alternatives;
6. Score and select minimum POC candidates;
7. Clarify the action and owner for supplementing the certificate.

## 13. When to stop discovering

Adequacy is found when the team can describe key users, end-to-end tasks, issues, and impacts; knows key constraints and counterevidence; and can judge whether limited validation is worthwhile.

Discovery does not require eliminating all unknowns, but providing sufficient evidence for the next investment decision.
