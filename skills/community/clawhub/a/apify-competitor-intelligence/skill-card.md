## Description:

Analyze competitor strategies, content, pricing, ads, and market positioning across Google Maps, Booking.com, Facebook, Instagram, YouTube, and TikTok.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apify](https://clawhub.ai/user/apify)

### License/Terms of Use:


## Use Case:

External users and business analysts use this skill to select and run Apify Actors for competitor research across local listings, travel, social media, ads, reviews, and video platforms, then summarize or export the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start Apify Actor runs with the configured token, which may consume account resources.

Mitigation: Use a dedicated low-privilege Apify token with spend limits and keep Actor choices within the documented catalog.

Risk: Scraped outputs may contain inaccurate, sensitive, or otherwise untrusted public data.

Mitigation: Avoid sensitive input, review generated CSV or JSON before reuse, and treat exported files as untrusted data.

Risk: The mcpc installation path is unpinned, so dependency changes can affect behavior.

Mitigation: Pin and review the @apify/mcpc package version in managed environments before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apify/skills/apify-competitor-intelligence)
- [Apify](https://apify.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands; optional CSV or JSON exports from Apify Actor runs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN, Node.js, and mcpc; quick-answer mode prints a small result sample while file mode exports CSV or JSON data.]

## Skill Version(s):

1.0.1 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
