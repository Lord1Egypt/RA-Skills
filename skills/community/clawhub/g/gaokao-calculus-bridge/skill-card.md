## Description: <br>
Gaokao Calculus Bridge helps agents connect 2026 Gaokao math reform themes with higher-math instruction by generating contextualized modeling problems, concept bridges, long-prompt analyses, project guides, and study paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daigxok](https://clawhub.ai/user/daigxok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, educators, students, and learning agents use this skill to turn high-school-to-college calculus topics into real-world modeling exercises, concept maps, project-based learning plans, and personalized study guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs local Python scripts with third-party dependencies. <br>
Mitigation: Install dependencies in a virtual environment and review unpinned packages before execution when reproducibility or supply-chain control matters. <br>
Risk: The release declares API-key configuration for integrations. <br>
Mitigation: Provide API keys only for integrations the user intends to use, and keep secrets in the agent or runtime environment rather than in skill content. <br>
Risk: Broad educational math triggers may activate for loosely related contextual math requests. <br>
Mitigation: Confirm the user wants the Gaokao-to-calculus bridge workflow before applying it to general math or modeling questions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daigxok/gaokao-calculus-bridge) <br>
- [Gaokao 2026 Reform Reference](references/gaokao_2026_reform.md) <br>
- [Mathematical Modeling Templates](references/modeling_templates.md) <br>
- [Real-World Case Library](references/real_world_cases.md) <br>
- [Project Guide Template](templates/project_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-oriented text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces educational math analyses, modeling prompts, learning plans, and local Python command invocations; scripts can emit markdown or JSON.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
