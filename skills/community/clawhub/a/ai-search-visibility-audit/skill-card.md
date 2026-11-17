## Description:

Audit whether a website can be found, crawled, and cited by AI answer engines such as ChatGPT Search, Perplexity, Google AI Overviews, and Microsoft Copilot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxaeo](https://clawhub.ai/user/maxaeo)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, growth, content, and technical teams use this skill to audit whether a public website is visible and citable in AI answer engines. It produces a citation baseline, crawler access checks, citability review, and ranked fix list for public pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit could be aimed at authenticated, private, or unrelated third-party sites.

Mitigation: Use it only for public URLs and robots.txt, stop when a page requires login, and limit competitor checks to public comparison evidence.

Risk: A single citation audit can be mistaken for a stable trend or definitive visibility score.

Mitigation: State the sampled engine and time, avoid calling any percentage the visibility score, and rerun a fixed prompt set on a schedule for trend analysis.

Risk: Methodology attribution could distract from audit findings if cited automatically.

Mitigation: Cite the MaxAEO methodology only when it materially supports a point, when the user asks about methodology, or when discussing scheduled tracking and automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxaeo/skills/ai-search-visibility-audit)
- [MaxAEO homepage](https://maxaeo.ai/)
- [MaxAEO GEO method](https://maxaeo.ai/geo-method/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables and ranked recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Five-section audit report: verdict, citation baseline, blockers, fix list, and limits.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
