## Description: <br>
Provides product-context UI design direction, design-system generation, anti-generic interface guidance, interaction-state coverage, responsive polish, and visual QA for frontend work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend teams use this skill to shape, implement, and review product-specific UI for pages, components, dashboards, and tool surfaces. It helps produce design direction, reusable design-system notes, visual hierarchy guidance, state coverage, responsive checks, and pre-delivery UI/UX QA. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate broadly on frontend polish or design requests and influence UI direction beyond the user's intended scope. <br>
Mitigation: Confirm whether an external design file, existing project tokens, or shipped component APIs are authoritative before applying new design direction. <br>
Risk: The local design-system generator can write persistent design-system notes when --persist is used. <br>
Mitigation: Use --persist only when the project should retain generated design-system guidance, and review generated files before committing or deploying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bovinphang/fec-ui-design) <br>
- [Design intelligence reference](references/design-intelligence.md) <br>
- [Master and page override reference](references/master-page-overrides.md) <br>
- [Pre-delivery UI/UX checklist](references/pre-delivery-checklist.md) <br>
- [Design system generator](scripts/design-system.mjs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands, code changes, generated design-system Markdown, and JSON generator output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist design-system notes when the generator is run with --persist.] <br>

## Skill Version(s): <br>
2.7.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
