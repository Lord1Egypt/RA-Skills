## Description: <br>
Use when recreating, rewriting, or remixing a TikTok reference video into a new product-fit version. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newt0n](https://clawhub.ai/user/newt0n) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, sellers, and their agents use this skill to analyze a TikTok reference video and draft a differentiated product-fit version, such as a concept, script, storyboard, visual direction, or shot list. It helps adapt reference structure and style without making a one-to-one copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TikTok reference URLs and derived analysis artifacts may contain sensitive or private creative or product context. <br>
Mitigation: Use only reference material the user is comfortable sending to CreatOK, avoid unnecessary private product details, and review or delete generated .artifacts directories after use. <br>
Risk: Local artifact retention and weak path containment can leave detailed analysis files on disk longer than expected. <br>
Mitigation: Use controlled run identifiers, keep artifacts in the intended skill workspace, and document cleanup or retention behavior before broad deployment. <br>
Risk: The skill requires a CreatOK API key and network access to the CreatOK Open Skills API. <br>
Mitigation: Use a revocable CreatOK API key, store it in the CREATOK_API_KEY environment variable, and rotate or revoke it if exposed. <br>
Risk: Recreating a TikTok too closely can create similarity or copyright concerns. <br>
Mitigation: Apply the skill's required structure rewrite, expression rewrite, and style differentiation before producing a final creative draft. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/newt0n/creatok-recreate-video) <br>
- [Common Rules](references/common-rules.md) <br>
- [CreatOK API Key Setup](https://www.creatok.ai/app/workspace/api-keys) <br>
- [CreatOK Service](https://www.creatok.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Conversation-ready creative direction plus JSON source artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes recreate source artifacts under recreate-video/.artifacts/<run_id>/ and prepares a handoff for video generation when requested.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
