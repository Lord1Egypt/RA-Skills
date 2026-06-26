## Description: <br>
Searches Gaoding Design templates for posters, business cards, banners, ecommerce images, and similar design assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gezilinll](https://clawhub.ai/user/gezilinll) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Design and marketing users use this skill through an OpenClaw agent to search Chinese Gaoding templates by natural-language keywords, preview candidate templates, and optionally edit or export selected designs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Gaoding account credentials and saves reusable login cookies locally. <br>
Mitigation: Use a dedicated or low-privilege Gaoding account, restrict access to the .env file, and clear saved cookies when the task is complete. <br>
Risk: The skill includes edit and export actions that can affect account-hosted design work. <br>
Mitigation: Review the selected template and requested changes before allowing edit or export actions to run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gezilinll/gaoding-template-recommend) <br>
- [Gaoding Design](https://www.gaoding.com) <br>
- [OpenClaw](https://github.com/nicepkg/openclaw) <br>
- [Troubleshooting notes](docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [JSON results with screenshot and exported-file paths, plus Markdown-facing template titles and preview links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gaoding credentials and a Playwright browser session; search output normally includes template IDs, titles, preview URLs, and a local screenshot path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
