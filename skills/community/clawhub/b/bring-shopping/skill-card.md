## Description:

Manage Bring! shopping lists through an unofficial Node.js CLI using email/password login for listing lists and items, adding or removing items, and checking or unchecking items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutzenfriend](https://clawhub.ai/user/cutzenfriend)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to operate Bring! shopping lists from a shell-backed workflow when API-style access is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide Bring! account credentials to an unpinned third-party npm package.

Mitigation: Review and pin the npm package before installing; keep BRING_EMAIL and BRING_PASSWORD scoped to this CLI and consider using a dedicated Bring! account or password.

Risk: Remove, check, or uncheck commands can change the wrong shopping-list entry if the list or item name is ambiguous.

Mitigation: Run the lists or items command first and confirm the target list and item before remove, check, or uncheck operations.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, JSON]

**Output Format:** [Markdown guidance with shell commands; CLI responses are text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BRING_EMAIL and BRING_PASSWORD environment variables; defaults to the Willig list unless another list is supplied.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
