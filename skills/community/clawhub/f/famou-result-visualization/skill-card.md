## Description:

Creates an interactive HTML result-visualization page from a Python solution for FaMou or evolutionary optimization problems such as routing, scheduling, packing, graph coloring, and machine learning tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaom0](https://clawhub.ai/user/zhaom0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and optimization practitioners use this skill to inspect Python-coded final solutions and produce a visual page that makes the solution outcome easier to review, compare, and explain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML loads third-party CDN code when opened.

Mitigation: Remove or locally bundle CDN dependencies before using the output with confidential optimization data or in restricted environments.

Risk: Provided solution data can be embedded directly into the generated HTML.

Mitigation: Redact sensitive inputs, coordinates, schedules, scores, and business data before sharing or publishing the visualization.

Risk: The default output file can overwrite an existing famou_viz_result.html file.

Mitigation: Confirm the output path before writing and choose a unique filename when preserving prior visualizations matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaom0/skills/famou-result-visualization)
- [React CDN dependency](https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js)
- [ReactDOM CDN dependency](https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js)
- [Babel Standalone CDN dependency](https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.5/babel.min.js)
- [Tailwind CDN dependency](https://cdn.tailwindcss.com)
- [Google Fonts stylesheet](https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Noto+Sans+SC:wght@400;500;700&display=swap)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Self-contained HTML file with inline CSS and JavaScript, plus concise explanatory guidance when inputs are missing or ambiguous.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML may reference CDN-hosted React, Babel, Tailwind CSS, and Google Fonts unless dependencies are localized.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
