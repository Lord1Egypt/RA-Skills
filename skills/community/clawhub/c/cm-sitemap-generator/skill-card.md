## Description: <br>
Generates XML sitemaps by crawling a website or scanning local files, with optional robots.txt generation and XML, text, or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site maintainers use this skill to create sitemap.xml content from a live site or a local web directory, and to optionally generate a robots.txt file that references the sitemap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crawler disables HTTPS certificate and hostname verification while fetching pages. <br>
Mitigation: Use only on sites the user controls or is authorized to crawl, avoid sensitive or internal HTTPS targets until TLS verification is fixed, and review generated sitemap.xml and robots.txt outputs before publishing. <br>
Risk: The skill can write sitemap.xml and robots.txt files to paths provided at runtime. <br>
Mitigation: Check output paths before execution and review generated files before deploying them to a website. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/cm-sitemap-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [XML sitemap, optional robots.txt, text summary, or JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write sitemap.xml and robots.txt to caller-specified output paths; crawl limit defaults to 500 pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and script __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
