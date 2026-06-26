## Description: <br>
Provides Git and CNB Open API workflows for cloning, committing, pushing, branch management, Merge Request management, pipeline triggering, and build-result lookup on CNB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twksos](https://clawhub.ai/user/twksos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to operate CNB repositories and pipelines through Git commands and CNB Open API calls. It helps configure required tokens, Git identity, Merge Requests, reviews, labels, reviewers, pipeline triggers, and build-result inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides repository write operations such as pushes, merges, reviews, labels, reviewers, and pipeline triggers. <br>
Mitigation: Use least-privilege CNB tokens and require explicit approval after verifying the owner, repository, branch, Merge Request, and build identifiers. <br>
Risk: CNB credentials and Git identity settings can be mishandled if stored in source-controlled files or exposed in command history or logs. <br>
Mitigation: Inject sensitive tokens through secrets, keep /workspace/.env out of commits, avoid printing tokens, and rotate credentials regularly. <br>
Risk: Pipeline triggers and retries can start privileged CI/CD work in the wrong repository, branch, or event context. <br>
Mitigation: Confirm pipeline target details before triggering or retrying builds, and avoid sensitive operations from untrusted event contexts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twksos/cnb-cool-git) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/twksos) <br>
- [CNB API endpoint](https://api.cnb.cool) <br>
- [CNB repository host](https://cnb.cool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with environment-variable tables, Git commands, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CNB Git and API tokens plus Git user name and email; outputs operational guidance rather than executing commands itself.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
