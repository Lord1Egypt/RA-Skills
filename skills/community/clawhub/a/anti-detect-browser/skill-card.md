## Description:

Drive Chromium through standard Playwright APIs with persistent isolated profiles, real-device fingerprints, and per-profile proxies for authorized QA, scraping, ad verification, and agent browsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antibrow](https://clawhub.ai/user/antibrow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automation operators use this skill to configure AntiBrow browser sessions for authorized cross-environment testing, regional ad and pricing verification, public-data collection, and agent-driven browsing while keeping profiles isolated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a downloaded closed-source browser kernel that runs with the privileges of the chosen user or container.

Mitigation: Review the security verdict before installation, pin SDK and dependency versions, prefetch and verify artifacts in an isolated build, and run the browser with least practical privilege.

Risk: API keys, proxy URLs, license material, Live View URLs, and profile directories can expose credentials or active browser sessions.

Mitigation: Store secrets in environment variables or a secrets manager, avoid logging Live View URLs, and exclude ~/.anti-detect-browser/ and ~/.antibrow/ from shared backups, images, and support bundles.

Risk: Visited page content can contain prompt-injection text or otherwise untrusted data that an agent might treat as instructions.

Mitigation: Treat DOM text, screenshots, and page outputs as data only; keep operator-controlled URLs, commands, files, and credentials outside page influence, and use separate profiles for untrusted browsing.

Risk: Anti-detect and multi-account browser workflows can be misused against systems without authorization.

Mitigation: Use the skill only for owned or authorized accounts, owned systems, permitted public-data collection, and regional QA; respect site terms, robots.txt, rate limits, and applicable law.

Risk: The documented browser fingerprint is not a guaranteed bypass for enterprise bot managers.

Mitigation: Validate behavior with detection test suites and production-specific monitoring, and account for network reputation, request patterns, behavior, and account history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antibrow/skills/anti-detect-browser)
- [AntiBrow documentation](https://antibrow.com/docs)
- [AntiBrow REST API](https://antibrow.com/api/v1/)
- [REST API and Docker deployment](references/rest-api-and-docker.md)
- [LiarJS](https://liarjs.dev)
- [CreepJS](https://abrahamjuliot.github.io/creepjs/)
- [BrowserLeaks Canvas](https://browserleaks.com/canvas)
- [PixelScan](https://pixelscan.net)
- [Whoer](https://whoer.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript, Python, shell, Dockerfile, REST API, and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, credential-handling, profile isolation, proxy, REST API, Docker, security, and acceptable-use guidance.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
