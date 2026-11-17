## Description:

Measures page performance, cumulative layout shift, theme flicker, visual stability, and browser network activity with ready-to-run Playwright scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to verify local or authorized web applications before and after changes by measuring load behavior, network timing, cumulative layout shift, and theme flicker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser checks can load supplied URLs.

Mitigation: Run the skill only against local or otherwise authorized web applications.

Risk: The flicker check writes screenshots to /tmp/flicker-early.png and /tmp/flicker-final.png, which may retain page contents on disk.

Mitigation: Avoid using the flicker check on pages with sensitive data, or remove the temporary screenshots after the run.

Risk: Runtime package resolution can pull dependencies that are not pinned locally.

Mitigation: Prefer pinned local dependencies or run with npx --no-install.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/fix-visual-stability-browser-testing)
- [Publisher profile](https://clawhub.ai/user/wu-uk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled scripts report browser performance metrics, network request timings, CLS ratings, and flicker diagnosis results.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
