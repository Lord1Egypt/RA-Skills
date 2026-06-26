## Description: <br>
Uses a logged-in Brave browser session to browse X/Twitter and Facebook user pages and extract recent posts, profile details, login status, and engagement data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sean810720](https://clawhub.ai/user/sean810720) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to collect recent public social posts and profile fields from X/Twitter or Facebook through a logged-in browser session for monitoring, research, or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates through a real logged-in browser session/profile and can report details from that context. <br>
Mitigation: Use a dedicated Brave or Chrome profile with a non-sensitive social account rather than a normal personal browser session. <br>
Risk: Returned social posts are untrusted external content. <br>
Mitigation: Review or sanitize extracted post text before using it in downstream prompts, automation, analysis, or publication. <br>
Risk: The browser-control behavior has limited containment. <br>
Mitigation: Install only after review and run it in an isolated environment appropriate for logged-in social browsing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sean810720/brave-loggedin-tag-browsing) <br>
- [Publisher Profile](https://clawhub.ai/user/sean810720) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Structured JSON object containing username, platform, login status, profile, posts, and metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Post count and engagement fields depend on platform selectors, login state, and the requested maxPosts/includeStats options.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
