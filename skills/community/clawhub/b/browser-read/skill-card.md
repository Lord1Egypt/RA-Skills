## Description:

Extract readable content from browser pages as markdown when web_fetch fails and the page is already open in the browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bill492](https://clawhub.ai/user/bill492)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract readable markdown and page metadata from browser pages that require session context, block normal fetching, or render dynamic content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose visible text and URLs from authenticated or sensitive pages opened in the browser.

Mitigation: Use it only on pages whose content is intended to be shared with the agent; avoid banking, email, admin, HR, private internal, or similarly sensitive pages unless sharing that content is intentional.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [JSON object containing markdown content and page metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes title, excerpt, byline, site name, content length, URL, and a plain-text fallback when markdown extraction fails.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
