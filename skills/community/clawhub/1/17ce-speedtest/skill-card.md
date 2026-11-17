## Description:

17CE Global Website Speed Test Tool. Tests HTTP response time, Time to First Byte (TTFB), and DNS resolution time from monitoring nodes globally via WebSocket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vangen](https://clawhub.ai/user/vangen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and support engineers use this skill to test website reachability and latency from distributed 17CE monitoring nodes. It can return structured JSON, HTML reports, and Markdown summaries for comparing HTTP status, total response time, TTFB, and DNS latency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send tested URLs and optional request details to a third-party testing service.

Mitigation: Use only test targets you are authorized to probe, avoid private or internal URLs, and require confirmation before external or bulk tests.

Risk: The release distributes shared 17CE API credentials.

Mitigation: Use protected per-user credentials instead of the bundled shared account.

Risk: Cookie forwarding can expose sensitive session data.

Mitigation: Disable cookie forwarding by default and avoid passing production cookies.

Risk: Generated HTML reports may include untrusted target or result values.

Mitigation: Escape generated HTML fields before display or sharing.

Risk: Dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [17CE Official Website](https://www.17ce.com/)
- [17ce Speedtest ClawHub Release](https://clawhub.ai/vangen/skills/17ce-speedtest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON, HTML reports, console text, and Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to 17CE and tested targets; can use user-supplied URL, ISP, area, node count, timeout, Host, Cookie, and User-Agent parameters.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
