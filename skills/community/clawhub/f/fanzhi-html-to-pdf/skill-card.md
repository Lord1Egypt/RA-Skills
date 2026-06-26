## Description: <br>
Html To Pdf converts local HTML files into image-based PDFs by rendering them with a locally installed Chrome or Chromium browser through Puppeteer, expanding hidden content, waiting for charts, and validating the resulting page count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ronie-shi](https://clawhub.ai/user/ronie-shi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert local dashboards, reports, web pages, Chinese-language HTML, and chart-heavy HTML into PDF files. It is best suited for one-page, rendered-page PDF capture rather than searchable text PDFs or print-layout pagination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local HTML is rendered through Chromium, so untrusted HTML or remote resources referenced by that HTML can introduce browser-side security and privacy risk. <br>
Mitigation: Use trusted local HTML, review external resource references before conversion, and run the skill in an environment appropriate for browser execution. <br>
Risk: The script launches Chromium with --no-sandbox, which is not appropriate for shared or multi-tenant environments. <br>
Mitigation: Avoid --no-sandbox in shared deployments and restrict use to trusted single-user environments unless the Chromium sandbox configuration is reviewed and changed. <br>
Risk: The skill depends on local npm packages, a local Chrome or Chromium installation, and local fonts for correct rendering. <br>
Mitigation: Install dependencies from trusted registries, set CHROME_PATH when needed, and install required Chinese and emoji fonts before relying on generated PDFs. <br>
Risk: Generated PDFs are image-based captures, so text selection, searchability, and formal print pagination may not meet document workflow requirements. <br>
Mitigation: Use the skill for rendered-page capture workflows and choose a text-native or print-layout PDF tool when searchable text or A4-style pagination is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ronie-shi/fanzhi-html-to-pdf) <br>
- [Chromium and Chrome platform paths](references/platforms.md) <br>
- [Sources and license references](references/sources.md) <br>
- [HTML to PDF technical details](references/tech-details.md) <br>
- [Puppeteer](https://github.com/puppeteer/puppeteer) <br>
- [pdf-lib](https://github.com/Hopding/pdf-lib) <br>
- [Noto Sans CJK font](https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf) <br>
- [Noto Emoji font](https://github.com/googlefonts/noto-emoji/raw/main/fonts/NotoEmoji-Regular.ttf) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and generated PDF file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces image-based PDF output from local .html or .htm input; PDF text is not expected to be selectable or searchable.] <br>

## Skill Version(s): <br>
1.0.4 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
