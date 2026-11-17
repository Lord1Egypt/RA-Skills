## Description:

Helps an agent create, save, update, and publish CSDN blog articles from Markdown using local Node.js scripts and user-provided CSDN session headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation users can use this skill to prepare Markdown articles, save them as CSDN drafts, update existing CSDN articles, or publish completed posts after reviewing required publication metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses active CSDN session cookies and signing headers stored in plaintext local configuration.

Mitigation: Treat csdn_config.json like a password file: keep it out of shared repositories, restrict local access, avoid pasting it into prompts or logs, and refresh or revoke the CSDN session if exposure is suspected.

Risk: The scripts can save, update, or publish content to the user's CSDN account.

Mitigation: Use draft mode first, review article content and publication metadata in CSDN, and confirm article IDs before update or publish operations.

Risk: CSDN request headers and signatures may expire or fail after reuse.

Mitigation: Regenerate the full request header set from an active CSDN editor session when authentication or signature errors occur.

Risk: Local file-to-article mappings can point update or publish commands at the wrong article if stale.

Mitigation: Check csdn_article_map.json before relying on automatic ID reuse, or pass the intended article ID explicitly.

## Reference(s):

- [CSDN Blog API Reference](artifact/references/api_reference.md)
- [CSDN Article Publish Troubleshooting](artifact/references/troubleshooting.md)
- [CSDN Markdown Editor](https://editor.csdn.net/md/)
- [CSDN saveArticle API Endpoint](https://bizapi.csdn.net/blog-console-api/v3/mdeditor/saveArticle)
- [ClawHub Skill Page](https://clawhub.ai/wuchubuzai2018/skills/csdn-article-publish)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown article files and csdn_article_map.json when the provided scripts are executed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
