## Description: <br>
Generates a browser-openable, single-file HTML deliverable from complex AI outputs such as reports, analyses, specs, reviews, notes, dashboards, posters, and product mockups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ysredcity](https://clawhub.ai/user/ysredcity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and team members use this skill to turn complex AI-generated deliverables into polished, shareable single-file HTML documents. It is intended for readable final artifacts such as research reports, data summaries, proposal comparisons, requirements notes, meeting notes, review pages, one-page summaries, and lightweight product interface mockups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML may reference allowlisted CDN resources, which can be unsuitable for sensitive or offline environments. <br>
Mitigation: For sensitive or offline use, instruct the agent to avoid CDN resources and produce a fully self-contained HTML file. <br>
Risk: The skill defaults toward Chinese prose and HTML deliverables, which may not match every requested audience or format. <br>
Mitigation: State the desired output language and final format when a different language or non-HTML deliverable is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ysredcity/anything-to-html) <br>
- [Anything to HTML Visual Language Tokens](references/design-tokens.md) <br>
- [Article Archetype Guide](references/archetype-article.md) <br>
- [Dashboard Archetype Guide](references/archetype-dashboard.md) <br>
- [Poster Archetype Guide](references/archetype-poster.md) <br>
- [Product Interface Archetype Guide](references/archetype-app-screen.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Markdown, Guidance] <br>
**Output Format:** [Single-file HTML with inline CSS and optional inline or allowlisted CDN JavaScript] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated artifact is designed to open directly in a browser and to remain readable as structured text for later AI processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
