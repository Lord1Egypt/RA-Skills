## Description: <br>
AI-powered tour guide with backend API and offline fallback for personalized routes, photo spots, and cultural narration for scenic spots in China, with Chinese and English support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bitzhuyong](https://clawhub.ai/user/bitzhuyong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, tourism assistants, and agent developers use this skill for focused single-attraction visits in China: route planning, step-by-step guide narration, photo spot suggestions, and tour summaries in English or Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send user questions and conversation history to an under-disclosed HTTP backend. <br>
Mitigation: Use the skill only with a trusted documented backend, prefer HTTPS, avoid sensitive travel or family details, and keep local fallback available when remote use is not acceptable. <br>
Risk: Tour guidance may affect physical safety or rely on changing venue conditions. <br>
Mitigation: Treat routes, opening hours, crowd notes, and safety-sensitive guidance as advisory and verify current conditions with official venue sources before acting. <br>


## Reference(s): <br>
- [ChinaTour README](README.md) <br>
- [ChinaTour Skill Definition](SKILL.md) <br>
- [Development Guide](DEVELOPMENT.md) <br>
- [Guide Card Template](assets/guide-card-template.md) <br>
- [Attraction Reference Data](references/attractions/) <br>
- [Photo Spot Reference Data](references/photo-spots/) <br>
- [Culture Story Reference Data](references/culture-stories/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown-style conversational guidance with numbered options and optional structured API result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese output; may use local reference data when the backend API is unavailable.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
