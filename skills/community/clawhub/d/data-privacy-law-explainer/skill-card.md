## Description:

Explains U.S. state-by-state consumer data-privacy law, including applicability thresholds, privacy-policy duties, consumer rights, opt-outs, private rights of action, and enforcement, using bundled source-cited jurisdiction snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to understand U.S. state consumer privacy-law requirements, compare state rules, and locate source-cited explanations for privacy policies, consumer rights requests, opt-outs, and enforcement. It is for general legal information and should not be used as legal advice or a final compliance verdict.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Users may treat legal-information summaries as legal advice or as a final compliance determination for their specific facts.

Mitigation: State that answers are general legal information, do not give yes-or-no compliance verdicts for a user's business, and direct users to qualified privacy counsel for fact-specific advice.

Risk: Privacy law may have changed after a bundled jurisdiction snapshot.

Mitigation: Lead with the snapshot and last-reviewed dates, cite the bundled sources, and recommend checking the canonical source before relying on the answer.

Risk: The optional unpinned `npx skills add open-agreements/open-agreements` suggestion may install code that has not been separately reviewed.

Mitigation: Avoid running that command unless the package or repository is separately trusted, reviewed, or pinned to a reviewed version.

Risk: A refresh workflow could expose user facts if used incorrectly.

Mitigation: Fetch only the fixed canonical jurisdiction URL after user approval, and do not send the user's facts, data inventory, or policies upstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/skills/data-privacy-law-explainer)
- [OpenAgreements privacy practice notes](https://openagreements.org/legal/privacy)
- [Bundled jurisdiction manifest](artifact/manifest.json)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with source citations and jurisdiction snapshot dates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline bundled content for 51 U.S. jurisdictions; optional user-approved refresh fetches only fixed canonical URLs.]

## Skill Version(s):

0.3.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
