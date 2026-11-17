## Description:

Browser Js provides lightweight Chrome DevTools Protocol browser control for AI agents, with compact indexed outputs for browsing, clicking, typing, uploading files, extracting content, screenshots, and coordinate-based interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaihazher](https://clawhub.ai/user/shaihazher)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Browser Js to let an agent drive a local Chrome or Chromium session through CDP for web navigation, form interaction, file upload, content extraction, and visual verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over a signed-in local browser profile.

Mitigation: Use a dedicated non-personal browser profile, keep CDP bound to localhost, and avoid sensitive financial or account-management sites.

Risk: The file upload command can submit local files through the controlled browser.

Mitigation: Confirm every upload path and target page before allowing the command to run.

Risk: The server security guidance flags dependency update work before relying on the release.

Mitigation: Update the ws dependency and regenerate the lockfile before production use.

## Reference(s):

- [ClawHub Browser Js release page](https://clawhub.ai/shaihazher/skills/browser-js)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown instructions plus CLI text output and optional PNG screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visible text output is capped at 8KB, element HTML output is capped at 10KB, and screenshots are written to a supplied path or /tmp.]

## Skill Version(s):

1.5.0 (source: server release metadata, target metadata, and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
