## Description:

Advanced browser automation via the Camoufox Firefox fork for authorized automation tasks that need anti-bot protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akdira](https://clawhub.ai/user/akdira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route authorized OpenClaw browser tasks through Camoufox when ordinary Playwright or Chromium automation is blocked. It supports navigation, page snapshots, element interaction, screenshots, JavaScript evaluation, search macros, and cookie-authenticated sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anti-detection browser automation can be used outside authorized workflows.

Mitigation: Use only for targets where the operator has explicit permission, and review applicable laws and target-site terms before automation.

Risk: Network exposure of the browser-control API can allow remote control of browsing sessions.

Mitigation: Bind the API to localhost, apply firewall controls for any network exposure, require a strong bearer token for every browser-control endpoint, and disable permissive CORS.

Risk: Imported cookies act as live account credentials.

Mitigation: Store cookie files with 600 permissions, import only authorized cookies, avoid diagnostic printing or sharing, delete cookies when no longer needed, and rotate sessions after suspected exposure.

Risk: Unverified binary download or curl-to-bash setup can increase supply-chain risk.

Mitigation: Pin and verify the Camoufox binary before use, and avoid curl-to-bash installation paths.

Risk: Relaxed container sandboxing can increase host exposure if browser content is malicious.

Mitigation: Do not run with seccomp=unconfined; keep browser execution in a tightly isolated environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/akdira/skills/camofox-default-browser)
- [Publisher Profile](https://clawhub.ai/user/akdira)
- [Artifact README](artifact/README.md)
- [API Reference](artifact/API.md)
- [Configuration Guide](artifact/CONFIGURATION.md)
- [Installation Guide](artifact/INSTALL.md)
- [Security Guidelines](artifact/SECURITY.md)
- [Camoufox Browser Repository](https://github.com/jo-inc/camofox-browser)
- [Camoufox Releases](https://github.com/jo-inc/camofox-browser/releases)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool calls, JSON API responses, text page snapshots, and screenshot data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and CAMOUFOX_EXECUTABLE; cookie import and sensitive browser-control operations should be protected with bearer-token authentication.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact SKILL.md says 1.2.0 and CHANGELOG top entry says 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
