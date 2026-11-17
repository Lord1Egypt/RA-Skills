## Description:

Queries the Bana real-estate API for supported Chinese cities, communities, second-hand homes, rentals, and new-house listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiongweixp](https://clawhub.ai/user/xiongweixp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query Bana real-estate data for Chinese cities, including community listings, second-hand homes, rentals, new homes, and filtered searches by district, business circle, keyword, or page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Bana AppID and SecureKey locally by default.

Mitigation: Use one-time credential mode when persistence is not needed, clear saved credentials after use, and avoid sharing or repeating the SecureKey.

Risk: Most methods can spend account balance after fee notification without a separate confirmation step.

Mitigation: State the method, call count, and estimated fee before paid calls; keep batch calls sequential and stop on balance or service errors.

Risk: Credential-file and base-URL behavior can be influenced by environment variables.

Mitigation: Run only in trusted environments and use alternate credential paths or base URLs only when intentionally configured by the user.

## Reference(s):

- [Bana Real Estate API Reference](artifact/references/api.md)
- [Bana Skill Center](https://wxpub.aibana.art)
- [ClawHub Skill Page](https://clawhub.ai/xiongweixp/skills/bana-realestate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with command examples and summarized JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Bana AppID and SecureKey credentials; paid methods should include fee notice before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
