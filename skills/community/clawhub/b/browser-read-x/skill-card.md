## Description:

Extract the main X/Twitter post or article content from a page that is already open in the browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bill492](https://clawhub.ai/user/bill492)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract the main post or article text from an already-open X/Twitter page when normal web fetching is blocked, authenticated, or too noisy. It is suited for pulling the central content body while reducing surrounding UI chrome, prompts, reaction metrics, and promotional blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and return text from the browser page where it is executed, including logged-in or authenticated X/Twitter pages.

Mitigation: Use it only on pages whose contents are intended to be shared with the agent, and review extracted content before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bill492/skills/browser-read-x)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [JSON object containing extracted page text and page metadata fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes title, content, excerpt, byline, siteName, length, url, and extraction status when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
