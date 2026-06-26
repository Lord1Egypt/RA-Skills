## Description: <br>
Cosdesign Standalone generates structured prompts and design-system outputs for analyzing public or authorized web pages, extracting colors, typography, spacing, layout, component patterns, and exportable CSS variables, design tokens, Tailwind configuration, or HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmofang](https://clawhub.ai/user/cosmofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, developers, and agents use this skill to inspect public or authorized web pages and turn visual style evidence into reusable design specifications, comparison reports, tokens, CSS variables, Tailwind configuration, or HTML reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may fetch URLs containing confidential context, tokens, internal services, or content the user is not authorized to analyze. <br>
Mitigation: Use only public or authorized URLs and remove tokens or sensitive context from links before analysis. <br>
Risk: The skill may retain local URL analysis history in data/analysis-history.json. <br>
Mitigation: Monitor or delete data/analysis-history.json when local analysis history should not be retained. <br>
Risk: Generated design specifications can be incorrect if the target page blocks fetching, changes dynamically, or exposes incomplete style information. <br>
Mitigation: Review generated palettes, typography, spacing, and exported configuration against the live page before reuse. <br>


## Reference(s): <br>
- [Cosdesign Standalone ClawHub Listing](https://clawhub.ai/cosmofang/cosdesign-standalone) <br>
- [CosDesign Homepage](https://github.com/Cosmofang/cosdesign) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prompts and generated design specifications, with optional JSON, CSS variables, Tailwind configuration, or HTML report output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append local analysis history to data/analysis-history.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
