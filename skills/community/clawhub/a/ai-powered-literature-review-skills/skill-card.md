## Description:

Helps an agent conduct bilingual academic literature reviews by generating search strategies, collecting paper metadata through browser-based database searches, deduplicating results, formatting GB/T 7714-2015 citations, and drafting Markdown review documents.

This skill is for research and development only.

## Publisher:

[stephenlzc](https://clawhub.ai/user/stephenlzc)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and academic writers use this skill to plan Chinese and English literature searches, organize retrieved paper metadata, and produce structured literature review drafts with standardized citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation may use cookies, login sessions, and page content from a user's active browser context.

Mitigation: Run the skill in a dedicated browser profile or isolated container with no unrelated logged-in accounts.

Risk: Network access to academic databases and DOI services can trigger site rate limits, access controls, or terms-of-service concerns.

Mitigation: Use institution-approved access, keep search volume modest, and confirm that database terms allow the planned automated browsing.

Risk: The provided Docker Compose file should not be treated as a complete domain allowlist or security boundary.

Mitigation: Enforce reviewed network egress restrictions outside the Compose file when deployment requires domain allowlisting.

Risk: Natural-language installation guidance may encourage an assistant to clone and install code without human review.

Mitigation: Install from a manually reviewed, pinned release and inspect the skill, scripts, and configuration before enabling it.

Risk: Broad writable permissions such as chmod 777 can expose session and output data to unintended local access.

Mitigation: Use least-privilege permissions for writable session and output directories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stephenlzc/skills/ai-powered-literature-review-skills)
- [Academic Database Access Guide](references/database-access.md)
- [CNKI Search Guide](references/cnki-guide.md)
- [GB/T 7714-2015 Citation Rules](references/gb-t-7714-2015.md)
- [CNKI Advanced Search](https://kns.cnki.net/kns8/AdvSearch)
- [Web of Science Advanced Search](https://www.webofscience.com/wos/woscc/advanced-search)
- [ScienceDirect Search](https://www.sciencedirect.com/search)
- [PubMed Advanced Search](https://pubmed.ncbi.nlm.nih.gov/advanced/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents with structured JSON session data, browser automation guidance, and GB/T 7714-2015 citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates session and output files such as paper metadata, deduplicated paper lists, paper analyses, reference lists, drafts, review reports, and final literature reviews.]

## Skill Version(s):

3.1.0 (source: server release metadata and install.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
