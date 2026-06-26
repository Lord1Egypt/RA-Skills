## Description: <br>
每日趣味内容生成器，每天早上搜索网络并预缓存笑话、热梗和聊天技巧，供心跳或手动调用时随机取用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bcocgs21494](https://clawhub.ai/user/bcocgs21494) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to schedule or manually generate lighthearted Chinese jokes, meme explanations, and chat tips, then retrieve a cached random item for periodic sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator performs recurring web searches and caches generated entertainment content locally. <br>
Mitigation: Enable scheduled runs only when recurring web search is desired, and review cached content before using it in sensitive or public contexts. <br>
Risk: The generation script invokes local search tooling through the shell. <br>
Mitigation: Use the skill only in environments where the local mcporter/search tooling is installed and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bcocgs21494/daily-fun-content) <br>
- [Artifact README and usage](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses from helper scripts and Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Caches generated items in cache/daily-fun.json and returns one random cached item per retrieval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
