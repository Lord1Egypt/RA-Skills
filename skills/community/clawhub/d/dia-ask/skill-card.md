## Description:

Prompt The Browser Company's Dia from the command line and get its assistant's answer back as an exact text file for reading and researching logged-in or JavaScript-heavy pages in a real browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[germankovacevic-lab](https://clawhub.ai/user/germankovacevic-lab)

### License/Terms of Use:

MIT

## Use Case:

Developers and technical users use this skill to delegate read-only browser research prompts to a local Dia session and retrieve the assistant's response from a file. It is intended for pages that require an authenticated or JavaScript-heavy browser session, while actions such as clicking or submitting remain outside the skill's scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read content available in the user's logged-in Dia browser session.

Mitigation: Avoid using it on banking, admin, HR, or confidential tabs, and review prompts before sending them to Dia.

Risk: Accessibility automation and fallback clipboard behavior can expose or misroute sensitive prompt or page data.

Mitigation: Grant Accessibility only after review, use --no-fallback for sensitive prompts, and keep other Dia tasks idle while the command runs.

Risk: The output file lookup can be confused by unrelated Dia output files.

Mitigation: Run one Dia task at a time and verify the returned file path and file contents before using the result.

Risk: The integration relies on unofficial Dia UI automation that can break after Dia updates.

Mitigation: Re-test the workflow after Dia updates and treat the implementation as auditable automation rather than a stable official API.

## Reference(s):

- [Dia Browser](https://www.diabrowser.com/)
- [AgentNeo](https://agneo.app)
- [ClawHub skill page](https://clawhub.ai/germankovacevic-lab/skills/dia-ask)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; Dia responses are written to md, txt, json, or csv files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The command prints the absolute path to the generated answer file and requires macOS, Dia, Node.js >= 18, and Accessibility permission.]

## Skill Version(s):

0.1.3 (source: package.json and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
