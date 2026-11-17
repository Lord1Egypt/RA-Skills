## Description:

Discover RSS and Atom feeds for websites by checking HTML alternate links and common feed paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangzhe1991](https://clawhub.ai/user/yangzhe1991)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to locate RSS or Atom feed URLs for websites they want to follow, monitor, or add to feed readers and news aggregation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can make unrestricted network requests to user-supplied URLs and followed redirects, including internal or local services.

Mitigation: Use only explicit public http/https website URLs, and avoid running the skill where the agent can reach private networks, localhost admin services, or cloud metadata endpoints unless those destinations are blocked by the runtime.

Risk: Automated feed discovery may be blocked, rate limited, or miss feeds on JavaScript-rendered sites.

Mitigation: Treat missing results as inconclusive; verify important feeds manually through the site's RSS or subscribe links or a trusted feed reader.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Terminal text listing discovered feed URLs, status messages, and follow-up tips.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a website URL input; results depend on network access and the target site's feed support.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
