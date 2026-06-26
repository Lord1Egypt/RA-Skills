## Description: <br>
通过命令行下载任意网站 favicon，支持多种尺寸与格式，无依赖。Using favicondl.com API to download favicon for any domain via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sweesama](https://clawhub.ai/user/sweesama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to fetch favicon image files for websites from the command line. It supports icon collection for bookmarks, directories, design references, SEO assets, and scripted workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested website domains are sent to favicondl.com and downloads may follow redirects to favicon hosts. <br>
Mitigation: Use the tool only for domains that are acceptable to disclose to the favicon service and expected redirect targets. <br>
Risk: The script writes to the requested output path and removes that file when a download fails. <br>
Mitigation: Choose a non-critical output path and avoid pointing the command at existing files that should be preserved. <br>
Risk: Downloaded favicon files originate from external network services. <br>
Mitigation: Review the script before installation and scan downloaded files before using them in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sweesama/favicondl) <br>
- [FaviconDL website](https://favicondl.com) <br>
- [Favicon API endpoint](https://favicondl.com/api/favicon?domain={domain}&size={size}&format=redirect) <br>
- [NPM package](https://www.npmjs.com/package/favicondl) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and local favicon image file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads are requested through favicondl.com and saved to the specified local output path.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
