## Description: <br>
Maintains an AI product manager campus recruiting resume workspace by extracting work logs, deduplicating resume points, building Chinese resume drafts, creating dashboard previews, and exporting PDF versions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songnb1021](https://clawhub.ai/user/songnb1021) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and early-career AI product manager candidates use this skill to turn work logs and experience notes into reusable resume points, one-page Chinese resume drafts, gap lists, dashboard previews, and PDF exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume workspaces can contain sensitive personal and career data. <br>
Mitigation: Keep the workspace private, avoid adding secrets, and review generated resume files before sharing or exporting. <br>
Risk: Generated HTML and PDF outputs may include incorrect, incomplete, or over-specific resume claims. <br>
Mitigation: Review all generated files, especially gap markers and quantified results, before using them for applications. <br>
Risk: The dashboard preview loads JavaScript libraries from public CDNs. <br>
Mitigation: Review CDN references before opening or sharing the dashboard in environments that restrict external resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songnb1021/ai-pm-resume-hub) <br>
- [Tailwind CSS CDN](https://cdn.tailwindcss.com) <br>
- [Marked CDN](https://cdn.jsdelivr.net/npm/marked/marked.min.js) <br>
- [DOMPurify CDN](https://cdn.jsdelivr.net/npm/dompurify@3.0.8/dist/purify.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, HTML dashboard, PDF files, and concise chat summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes resume materials under career/ai-pm-campus/ and may run local Python scripts for dashboard and PDF export.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
