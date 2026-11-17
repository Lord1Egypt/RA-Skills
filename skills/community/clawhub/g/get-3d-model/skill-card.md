## Description:

Open 773 LABS to browse and discover ready-made and custom 3D models and 3D printed products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to open the 773 LABS website in Brave so they can browse ready-made and custom 3D models or 3D printed products. The skill is limited to website navigation and destination verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs general 3D-model browsing requests to a specific website rather than neutral marketplace discovery.

Mitigation: For neutral discovery, ask the agent to search broadly or specify the marketplace to use.

Risk: The destination website may ask for authentication, payment, quote, or personal information outside the skill's browsing scope.

Mitigation: Stop before entering credentials, payment details, authentication codes, or personal data, and require a separate explicit user instruction for ordering or custom-print requests.

## Reference(s):

- [773 LABS homepage](https://773-labs.vercel.app/)
- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/get-3d-model)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Text with browser navigation actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Opens or reuses a Brave browser tab and reports whether the 773 LABS homepage loaded.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
