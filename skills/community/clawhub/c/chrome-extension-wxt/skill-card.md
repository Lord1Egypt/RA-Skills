## Description: <br>
Build Chrome extensions using the WXT framework with TypeScript, React, Vue, or Svelte. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to create and package browser extensions with WXT, Manifest V3, and modern UI frameworks. It provides starter commands, project structure, configuration patterns, API examples, and security guidance for cross-browser extension work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated extension examples may request privacy-sensitive browser permissions such as tabs, cookies, history, webRequest, host permissions, or script injection. <br>
Mitigation: Review generated manifests and code before use, request only necessary permissions, avoid <all_urls> unless strictly required, and inspect sensitive browser API usage before loading or publishing an extension. <br>
Risk: Extension guidance may involve user credentials, API keys, or actions that affect user data or purchases. <br>
Mitigation: Do not store API keys in sync storage, add consent or confirmation for destructive or purchase-related actions, and review credential handling before deployment. <br>
Risk: Starter code and configuration suggestions may be incomplete for a production extension security review. <br>
Mitigation: Treat the skill output as starter guidance, then perform project-specific security, privacy, and Chrome Web Store policy review. <br>


## Reference(s): <br>
- [Chrome Extension Best Practices with WXT](artifact/references/best-practices.md) <br>
- [Chrome 140+ Features](artifact/references/chrome-140-features.md) <br>
- [Chrome Extension API Reference](artifact/references/chrome-api.md) <br>
- [React Integration with WXT](artifact/references/react-integration.md) <br>
- [WXT API Reference](artifact/references/wxt-api.md) <br>
- [WXT Docs](https://wxt.dev) <br>
- [Chrome Extension Docs](https://developer.chrome.com/docs/extensions) <br>
- [MDN Mozilla Add-ons Docs](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, shell command, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser extension development guidance; no commands are executed by the skill itself.] <br>

## Skill Version(s): <br>
1.1.1 (source: SKILL.md frontmatter metadata and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
