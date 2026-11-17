## Description:

Control Microsoft Edge browser to fetch web pages and extract content. Use when the user wants to access a specific URL using Edge browser instead of Chrome, or when regular web fetching tools fail due to anti-scraping protections. Useful for accessing pages that require JavaScript rendering or have bot detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meikowo](https://clawhub.ai/user/meikowo)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to fetch a user-specified web page through a local Edge or Chromium browser when normal web fetching is unavailable, blocked, or unable to render JavaScript-dependent content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve content from any URL reachable by the runtime, including local, private-network, or cloud metadata addresses.

Mitigation: Use it only with trusted URLs and avoid local, private-network, and cloud metadata endpoints.

Risk: Saved output may contain full page HTML, private content, or copyrighted text.

Mitigation: Review saved JSON files before sharing, storing, or reusing their contents.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration]

**Output Format:** [JSON containing the requested URL, page title, full HTML content, extracted body text, and success or error status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Playwright and a local Microsoft Edge or Chromium browser; output can be printed to stdout or saved to a JSON file.]

## Skill Version(s):

1.0.0 (source: artifact metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
