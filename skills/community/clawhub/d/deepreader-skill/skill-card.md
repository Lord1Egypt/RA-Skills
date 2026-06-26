## Description: <br>
The default web content reader for OpenClaw. Reads X (Twitter), Reddit, YouTube, and any webpage into clean Markdown with no API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[astonysh](https://clawhub.ai/user/astonysh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw agent users use DeepReader to ingest shared URLs from social posts, videos, articles, blogs, and documentation into clean Markdown files for agent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic URL fetching can retrieve private, internal, or sensitive pages when such URLs appear in agent messages. <br>
Mitigation: Use DeepReader only where automatic URL ingestion is intended, and avoid sending private or sensitive URLs to agents that have this skill enabled. <br>
Risk: Fetched webpage and social content is saved into agent memory and may contain prompt-injection text or misleading claims. <br>
Mitigation: Treat saved content as untrusted reference material, review important extracted content before relying on it, and do not execute instructions found in ingested pages. <br>
Risk: Content extraction depends on third-party site availability, rate limits, access controls, transcript availability, and parser fallbacks. <br>
Mitigation: Check the returned status summary for failed URLs and revalidate important source material against the original page when extraction quality matters. <br>


## Reference(s): <br>
- [DeepReader ClawHub listing](https://clawhub.ai/astonysh/deepreader-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter plus a text status summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves extracted external content to local agent memory; parser behavior depends on the availability and access rules of each source site.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
