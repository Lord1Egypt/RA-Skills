## Description: <br>
FeedNest helps an agent read and manage articles, highlights, notes, tags, saved links, reading stats, and text-to-speech workflows from a user's FeedNest account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LucaIaconelli](https://clawhub.ai/user/LucaIaconelli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate on a user's selected FeedNest sources, including reading feeds, summarizing retrieved article content, managing highlights and notes, tagging articles, saving links, and generating audio. It is intended for workflows grounded in the user's own trusted feeds rather than open-web search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The FeedNest API key grants access to the user's FeedNest account. <br>
Mitigation: Treat the API key like a password and install the skill only when the user trusts FeedNest and the @feednest/openclaw plugin. <br>
Risk: Bulk or destructive operations can mark many items read or remove notes, highlights, or tags. <br>
Mitigation: Confirm with the user before bulk or destructive changes and review the affected items before executing the action. <br>


## Reference(s): <br>
- [FeedNest skill page](https://clawhub.ai/LucaIaconelli/feednest) <br>
- [FeedNest website](https://www.feednest.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with tool names, parameter guidance, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the FeedNest plugin, a FeedNest Pro account, and a FeedNest API key.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
