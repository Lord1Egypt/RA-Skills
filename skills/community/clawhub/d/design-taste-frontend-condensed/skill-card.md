## Description: <br>
Anti-slop frontend skill for landing pages, portfolios, and redesigns. The agent reads the brief, infers the right design direction, and ships interfaces that do not look templated. Real design systems when applicable, audit-first on redesigns, strict pre-flight check. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akdira](https://clawhub.ai/user/akdira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design-focused agents use this skill to build or redesign landing pages, portfolios, and marketing pages with stronger visual direction, real design-system choices, asset planning, motion discipline, and pre-flight design checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may steer agents toward adding frontend packages or using external visual assets. <br>
Mitigation: Review proposed install commands, package choices, and external asset URLs before approving project changes. <br>
Risk: Strong visual-design rules may be inappropriate for dashboards, data tables, or multi-step product UI. <br>
Mitigation: Apply the skill only to landing pages, portfolios, marketing pages, and relevant redesign surfaces, and override it when the product workflow requires a different interface pattern. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/akdira/design-taste-frontend) <br>
- [Material Web](https://github.com/material-components/material-web) <br>
- [Fluent UI](https://github.com/microsoft/fluentui) <br>
- [Carbon Design System](https://carbondesignsystem.com/) <br>
- [GOV.UK Frontend](https://github.com/alphagov/govuk-frontend) <br>
- [U.S. Web Design System](https://github.com/uswds/uswds) <br>
- [Tailwind CSS v4](https://tailwindcss.com/blog/tailwindcss-v4) <br>
- [Radix Themes](https://github.com/radix-ui/themes) <br>
- [shadcn/ui](https://github.com/shadcn-ui/ui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, install commands, implementation constraints, and frontend code recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to add frontend packages, use generated or web-hosted visual assets, and run design pre-flight checks before final output.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
