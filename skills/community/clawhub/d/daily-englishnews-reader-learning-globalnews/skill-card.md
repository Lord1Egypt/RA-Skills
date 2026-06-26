## Description: <br>
Generates CEFR-adapted English reading materials from current RSS articles using the i+1 learning approach and creates a Feishu cloud document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chegangan](https://clawhub.ai/user/chegangan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners and educators use this skill to create four English reading passages from global news, business, technology, and culture or science sources. The generated material includes CEFR-level rewriting, i+1 vocabulary explanations, original source links, and a Feishu document link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the user to authorize a Lark/Feishu integration that can create cloud documents. <br>
Mitigation: Authorize only in the intended workspace and review the requested permissions before use. <br>
Risk: The setup flow installs npm and pip dependencies before the reading workflow runs. <br>
Mitigation: Review install prompts and dependency sources in the target environment before approving installation. <br>
Risk: The skill stores generated article metadata in config/sent_articles.json for deduplication. <br>
Mitigation: Review or clear config/sent_articles.json when local reading history should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chegangan/daily-englishnews-reader-learning-globalnews) <br>
- [Al Jazeera English RSS source](https://morss.it/:format=json/https://www.aljazeera.com/xml/rss/all.xml) <br>
- [Vox Business RSS source](https://morss.it/:format=json/https://www.vox.com/rss/business-and-finance/index.xml) <br>
- [Cloudflare Blog RSS source](https://morss.it/:format=json/https://blog.cloudflare.com/rss/) <br>
- [The Conversation RSS source](https://morss.it/:format=json/https://theconversation.com/us/articles.atom) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style reading material and a Feishu document link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured RSS sources, user reading settings, and local article history for deduplication.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
