## Description: <br>
This skill helps an agent generate Chinese web-novel chapters, convert them for Fanqie, and publish them through a configured Fanqie writer account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenjiahui11](https://clawhub.ai/user/chenjiahui11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers and publishing operators use this skill to take a Chinese novel idea or existing chapter files through generation, formatting, review, and publication to a Fanqie writer account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can publish generated or converted chapters to a live Fanqie author account. <br>
Mitigation: Review every generated chapter manually and run status checks before allowing publication. <br>
Risk: The Fanqie cookie file grants account access if exposed. <br>
Mitigation: Protect the cookie file like a password, restrict file access, and rotate credentials if the file is shared or leaked. <br>
Risk: Batch or automatic publication can make multiple external changes quickly. <br>
Mitigation: Use single-chapter publishing or conservative intervals unless the operator has intentionally approved batch posting. <br>
Risk: The workflow depends on separate generation and publishing skills. <br>
Mitigation: Verify and configure open-novel-writing, novel-generator, and fanqie-publisher before relying on end-to-end automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenjiahui11/fanqie-novel-auto-publish) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/chenjiahui11) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown chapter files, command-line status text, and publishing result messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live Fanqie account actions when dependencies and account cookies are configured.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
