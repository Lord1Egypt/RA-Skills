## Description: <br>
Publish editorial and dynamic section content with blog-publish, enforce quality gates for hot/news/ai_news, and sync repository skills to ClawHub via clawhub sync --all. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeguooooo](https://clawhub.ai/user/leeguooooo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operators use this skill to publish or update Misonote editorial posts, dynamic hot/news/ai_news briefs, and uploaded media while applying dry-run checks and source-grounded quality gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can publish or update public blog content, upload media, and sync skills when real commands are run. <br>
Mitigation: Run dry-run commands first, verify the active account with whoami, and approve the exact posts, uploads, and sync changes before executing publish, update, upload, or sync-all commands. <br>
Risk: Authentication mistakes or token misuse could publish through the wrong account or fail in automation. <br>
Mitigation: Verify the npm package source, confirm the active account, use service tokens deliberately in CI, and rotate PUBLISH_API_TOKEN after unauthorized automation failures. <br>
Risk: Dynamic news or hot briefs could contain weak evidence, unsupported interpretations, repeated links, placeholders, or leaked internal producer metadata. <br>
Mitigation: Apply the stated quality gates: require source and evidence anchors, executable actions, P0/P1/P2 impact labels, markdown links, placeholder checks, and no public producer leakage before publishing. <br>


## Reference(s): <br>
- [Blog Content Publish on ClawHub](https://clawhub.ai/leeguooooo/blog-content-publish) <br>
- [Misonote Blog](https://blog.misonote.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, input fields, and content templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run checks, dynamic-section quality gates, and public-content publishing guardrails.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
