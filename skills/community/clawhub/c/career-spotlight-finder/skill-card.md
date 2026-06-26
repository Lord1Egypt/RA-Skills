## Description: <br>
Discovers hidden strengths, industry terminology, and career narratives from past projects, articles, or code for resumes, self-introductions, and personal branding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realzst](https://clawhub.ai/user/realzst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers, developers, researchers, and other professionals use this skill to turn project repositories, papers, documents, URLs, and career materials into a coherent positioning strategy, aggregated career report, resume bullets, LinkedIn summary, elevator pitch, and casual introduction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read user-selected projects, documents, and URLs that may contain confidential or sensitive material. <br>
Mitigation: Provide narrow input paths and avoid folders or URLs that contain secrets or unrelated confidential information. <br>
Risk: Derived career summaries and copy are persistently stored under ~/.career-spotlight/. <br>
Mitigation: Delete ~/.career-spotlight/ when the retained profile, reports, copy, and history are no longer needed. <br>
Risk: Generated career copy may need human review before it is shared publicly or used in applications. <br>
Mitigation: Review generated resume bullets, summaries, and introductions before sharing them. <br>


## Reference(s): <br>
- [Career Spotlight Finder ClawHub Page](https://clawhub.ai/realzst/career-spotlight-finder) <br>
- [Career Spotlight Finder Homepage](https://github.com/RealZST/career-spotlight-finder) <br>
- [README](README.md) <br>
- [Input Collection Guide](guides/input-collection-guide.md) <br>
- [Project Analysis Guide](guides/project-analysis-guide.md) <br>
- [Domain Positioning Guide](guides/domain-positioning-guide.md) <br>
- [Narrative Synthesis Guide](guides/narrative-synthesis-guide.md) <br>
- [Copywriting Guide](guides/copywriting-guide.md) <br>
- [AI Infrastructure Industry Terms](references/industry-terms-ai-infra.md) <br>
- [Machine Learning Industry Terms](references/industry-terms-ml.md) <br>
- [Software Engineering Industry Terms](references/industry-terms-swe.md) <br>
- [Data Engineering Industry Terms](references/industry-terms-data.md) <br>
- [Security Industry Terms](references/industry-terms-security.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports and copy files with conversational review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes per-project analyses, an aggregated report, copy variants, and archived history under ~/.career-spotlight/.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
