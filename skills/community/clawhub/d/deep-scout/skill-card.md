## Description: <br>
Multi-stage deep intelligence pipeline (Search -> Filter -> Fetch -> Synthesize) that turns a query into a structured research report with full source citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JonathanJing](https://clawhub.ai/user/JonathanJing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to turn a web research question into a filtered, fetched, and synthesized Markdown report or comparison with source citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and fetched web content may be sent through search, fetch, crawl, browser, and LLM tools. <br>
Mitigation: Avoid secrets, private account pages, regulated data, and confidential internal URLs; use --no-browser or --no-firecrawl when a narrower research path is needed. <br>
Risk: Generated reports can contain stale, incomplete, or misinterpreted web evidence. <br>
Mitigation: Review cited sources and check important claims before relying on the report. <br>
Risk: Optional file output can create local reports that persist beyond the session. <br>
Mitigation: Choose output paths deliberately and keep generated reports within the intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JonathanJing/deep-scout) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research reports or comparison tables with source citations; optional local file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default depth is 5 fetched URLs; reports target concise Markdown with source links and can disable browser or Firecrawl fallback.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
