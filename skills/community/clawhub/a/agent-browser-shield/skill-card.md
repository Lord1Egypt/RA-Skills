## Description: <br>
Agent Browser Shield helps agents install and operate a Chromium extension that masks sensitive data, reduces dark patterns, and strips prompt-injection surfaces before page content reaches the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pixiebrix](https://clawhub.ai/user/pixiebrix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill at browser-session bootstrap to configure Agent Browser Shield for local Chromium or Browserbase sessions. The skill also defines the agent behavior contract for handling extension DOM markers, masked content, checkout flags, and rewritten page elements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The extension can access and modify protected browser pages, including hiding or rewriting page content. <br>
Mitigation: Use a dedicated browser profile, verify the extension source, and review extension options before enabling it for agent browsing. <br>
Risk: Browserbase setup requires a Browserbase API key. <br>
Mitigation: Provide the key only through the intended Browserbase setup flow and avoid exposing it in chat, logs, or shared configuration. <br>
Risk: Revealed placeholder content may contain untrusted instructions or sensitive data. <br>
Mitigation: Leave placeholders hidden unless the user explicitly asks to reveal them, treat revealed text as untrusted input, and do not reconstruct masked PII or secrets. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/pixiebrix/agent-browser-shield) <br>
- [Chrome Web Store extension](https://chromewebstore.google.com/detail/agent-browser-shield/gnejacdioaelglahihpagpfjpddpnamd) <br>
- [Hosted extension ZIP](https://github.com/pixiebrix/agent-browser-shield/releases/latest/download/agent-browser-shield-extension.zip) <br>
- [Browserbase browse CLI documentation](https://docs.browserbase.com/integrations/skills/browse-cli) <br>
- [Issue tracker](https://github.com/pixiebrix/agent-browser-shield/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Browserbase API key handling guidance, extension installation steps, and DOM-marker behavior rules.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
