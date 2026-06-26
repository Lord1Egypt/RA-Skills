## Description: <br>
Browser Steel helps agents automate JS-heavy web pages with Steel CLI by default and a Python Playwright fallback for custom browser flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyanmi](https://clawhub.ai/user/xyanmi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation-focused agents use this skill to scrape, capture, debug, and interact with browser pages through Steel sessions or one-shot commands. It is suited for workflows that need live page content, screenshots, PDFs, form filling, session reuse, or selector-heavy Playwright plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact browser automation can act on authenticated sites or sensitive workflows. <br>
Mitigation: Use a scoped Steel API key, run only against sites where automation is authorized, and review target URLs and commands before execution. <br>
Risk: Authenticated session reuse and cookie import can expose account state or cross-site cookies. <br>
Mitigation: Keep cookie files site-specific, pass cookies only at runtime, avoid publishing cookies or local profiles, and stop named sessions after use. <br>
Risk: Proxy, stealth, and CAPTCHA-solving options can be misused or violate site policies. <br>
Mitigation: Use those options only with explicit authorization and prefer standard scrape, screenshot, or PDF commands when anti-bot bypass behavior is not required. <br>
Risk: Python plan files can drive arbitrary browser interactions and evaluate page scripts. <br>
Mitigation: Review plan files before running them, keep plan inputs task-specific, and use the Python runtime only when CLI commands are insufficient. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/xyanmi/browser-steel) <br>
- [Steel CLI documentation](https://docs.steel.dev/overview/steel-cli) <br>
- [Steel agent documentation index](https://docs.steel.dev/llms-full.txt) <br>
- [Steel Playwright Python guide](https://docs.steel.dev/overview/guides/playwright-python) <br>
- [Runtime modes](references/runtime-modes.md) <br>
- [CLI workflows](references/cli-workflows.md) <br>
- [Python plan runner](references/python-plan.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Configuration guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON command results, screenshots, PDFs, and extracted page text or HTML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require STEEL_API_KEY, Steel CLI or npx, python3, and optional Playwright/Steel Python packages for Python plans.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
