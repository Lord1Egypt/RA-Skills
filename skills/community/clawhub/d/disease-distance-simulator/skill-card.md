## Description: <br>
Guides a conversational agent to collect health, lifestyle, occupation, and family-history details, query epidemiology references, and produce an educational major-disease risk timeline with action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwbwin](https://clawhub.ai/user/wwbwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent to simulate a personalized major-disease risk timeline for health education, prevention planning, and discussion preparation. The output should be treated as educational guidance, not medical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global; outputs rely primarily on China-focused actuarial and cancer statistics unless the agent retrieves region-specific sources. <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for sensitive health, lifestyle, occupation, and family-history information. <br>
Mitigation: Avoid names and precise identifiers, collect only details needed for the educational report, and remind users not to share unnecessary personal information. <br>
Risk: The skill may use sensitive health details in external searches. <br>
Mitigation: Ask for confirmation before external searches and use minimized or generalized search terms. <br>
Risk: The report may be mistaken for medical advice. <br>
Mitigation: Keep the report framed as health education and direct users with health concerns to qualified medical professionals. <br>


## Reference(s): <br>
- [Artifact skill source](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/wwbwin/disease-distance-simulator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wwbwin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown educational report with tables and timeline-style visualization] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes health-education disclaimers and should avoid medical diagnosis or treatment advice.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
