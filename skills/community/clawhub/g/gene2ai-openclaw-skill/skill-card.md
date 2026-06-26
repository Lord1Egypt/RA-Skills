## Description: <br>
Your personal health data hub for AI agents: query genomic insights, upload medical documents, record daily health metrics, explore genomic-lab cross-references, receive personalized daily health briefings, and get contextual health advice woven into everyday conversations using the user's genetic and clinical data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangchen](https://clawhub.ai/user/gangchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to connect Gene2AI health profiles with conversational health workflows, including genomic queries, health-document uploads, daily metrics, and personalized health briefings. It is intended for agents configured with a profile-scoped Gene2AI API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags sensitive medical and genetic information, persistent agent memory, and proactive messages as requiring review. <br>
Mitigation: Install only if the user trusts Gene2AI with health data, avoid cross-session memory for health profile details unless explicitly desired, and enable daily briefings or proactive messages only deliberately. <br>
Risk: Messaging previews or briefings may expose sensitive health inferences. <br>
Mitigation: Keep announcement text high level, avoid raw genetic variants or lab values in previews, and discuss details only in direct conversation after the user engages. <br>
Risk: A configured API key grants access to a profile-scoped health profile. <br>
Mitigation: Use separate keys for separate profiles and revoke or rotate the Gene2AI API key when the skill is no longer in use. <br>


## Reference(s): <br>
- [Gene2AI Guide](https://gene2.ai/guide) <br>
- [ClawHub Skill Page](https://clawhub.ai/gangchen/gene2ai-openclaw-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference sensitive medical and genetic profile data returned by Gene2AI APIs when configured with GENE2AI_API_KEY.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata; artifact frontmatter lists 3.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
