## Description:

Browser Auto Download helps agents use Playwright-driven browser automation to navigate dynamic download pages, detect platform-specific files, click download controls, and save downloaded files locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronxx](https://clawhub.ai/user/aaronxx)

### License/Terms of Use:

MIT

## Use Case:

Developers and technical users use this skill to automate file downloads from dynamic webpages where direct curl or wget downloads are unreliable because links are generated client-side, hidden behind navigation, or require browser interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent-controlled browser may visit untrusted download pages and save unverified executable files locally.

Mitigation: Run the skill only on trusted URLs, use a dedicated output folder, inspect each downloaded file, and verify publisher signatures or checksums before opening or installing it.

Risk: Debug mode can save screenshots, HTML, and extracted text from pages that may contain private or authenticated content.

Mitigation: Avoid debug mode on sensitive pages unless the saved artifacts are expected, access-controlled, and cleaned up after review.

Risk: Automatic platform detection and fallback button clicking may select the wrong installer or package on complex pages.

Mitigation: Review the selected filename and platform metadata, and use a manual selector or disable auto-selection when the page offers multiple similar downloads.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaronxx/skills/browser-auto-download)
- [README](artifact/README.md)
- [Quick Start Guide](artifact/QUICKSTART.md)
- [User Guide](artifact/USER_GUIDE.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, JSON, Files]

**Output Format:** [Markdown guidance with shell commands and JSON download results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can save downloaded files to disk and, in debug mode, can save screenshots, HTML, and extracted text.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact files report 4.1.0 and 5.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
