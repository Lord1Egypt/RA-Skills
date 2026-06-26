## Description: <br>
Fetches Bilibili video danmaku from a video URL or BVID and produces keyword frequency, a PNG word cloud, sentiment distribution, and a Markdown public-opinion report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Smartloe](https://clawhub.ai/user/Smartloe) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and content operations teams use this skill to collect public Bilibili bullet comments and turn them into review-ready keyword, sentiment, word-cloud, and public-opinion artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs a local Python environment with third-party packages. <br>
Mitigation: Run it in an isolated virtual environment, review requirements.txt before installation, and install dependencies only from trusted package sources. <br>
Risk: Fetched danmaku and generated reports may contain user-generated public comments that should not be overshared without review. <br>
Mitigation: Use the skill for public Bilibili videos, choose the output directory deliberately, and review generated datasets and reports before sharing them. <br>
Risk: SnowNLP sentiment and keyword analysis can misread short comments, slang, memes, or domain-specific language. <br>
Mitigation: Treat outputs as rapid trend signals, manually review high-impact conclusions, and expand samples across pages or videos for stronger decisions. <br>


## Reference(s): <br>
- [Methodology](references/methodology.md) <br>
- [Default Stopwords](references/stopwords.default.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/Smartloe/bilibili-danmaku) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [CSV, JSON, TXT, PNG, and Markdown files generated under the selected output directory] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch output includes danmaku CSV/JSON/TXT and metadata JSON; analysis output includes top-word JSON, sentiment JSON, word-cloud PNG, and report Markdown.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
