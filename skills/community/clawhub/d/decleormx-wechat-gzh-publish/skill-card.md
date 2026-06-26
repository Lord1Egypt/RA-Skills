## Description: <br>
Automates WeChat Official Account article publishing, including login reuse, title and body entry, AI-generated cover imagery, draft saving, and direct publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XIEBBS](https://clawhub.ai/user/XIEBBS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and agents managing WeChat Official Accounts use this skill to prepare drafts or publish posts from text or files, with optional AI imagery, summary, comment, and reward settings. Operators should review drafts before live publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live WeChat Official Account posts using saved account cookies with limited safety gates. <br>
Mitigation: Use --draft first, manually review the article and generated cover, and only run direct publishing when intended. <br>
Risk: Saved cookies in ~/.wechat_mp/cookies.json can grant account access if exposed. <br>
Mitigation: Protect or delete the cookie file when it is not needed, and re-authenticate deliberately. <br>
Risk: Untrusted content files or generated images may be inserted into public posts. <br>
Mitigation: Use trusted content files and manually review generated imagery before publication. <br>
Risk: Unpinned Playwright dependency updates may change browser automation behavior. <br>
Mitigation: Consider pinning the Playwright dependency for reproducible operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/XIEBBS/decleormx-wechat-gzh-publish) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with shell command examples and CLI status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update ~/.wechat_mp/cookies.json and /tmp/mp_debug_*.png while operating the publishing workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
