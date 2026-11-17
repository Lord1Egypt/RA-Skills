## Description:

Pre-investment research and deal-memo generation for angel investors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

External angel investors use this skill to research current private companies, validate public evidence against founder or deck claims, prepare founder-call questions, and produce a nine-section local deal memo. The memo separates verified facts from claims and avoids invest/pass recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential deck details or private company context could be exposed through web searches or external tools.

Mitigation: Use only generic derived search targets and do not paste private deck numbers, customer names, roadmap details, or other non-public notes into searches or external tools.

Risk: A diligence memo could be mistaken for investment advice.

Mitigation: Keep the output as evidence and questions only; the skill explicitly avoids invest/pass recommendations and uses a verdict scaffold that leaves the decision to the human investor.

Risk: Startup funding, traction, hiring, and customer information can be stale, unavailable, or only company-claimed.

Mitigation: Require fetched URLs for factual claims, date each cited fact, mark gaps as could not verify, and distinguish independent verification from company claims.

Risk: Running the skill can create a local memo containing company names, round details, and user-provided context.

Mitigation: Treat generated diligence files as sensitive local work product and avoid sharing them unless the user explicitly requests it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/conorbronsdon/skills/cot-angel-diligence)
- [Publisher Profile](https://clawhub.ai/user/conorbronsdon)
- [README](artifact/README.md)
- [Research Prompt Templates](artifact/patterns/research-prompts.md)
- [Illustrative Memo](artifact/examples/illustrative-memo.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown memo with inline citations and a source list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local nine-section diligence memo and summarizes the Snapshot and Verdict scaffold for review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
