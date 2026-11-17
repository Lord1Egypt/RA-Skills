## Description: <br>
Card Image Builder helps agents generate branded card images, social media posters, X/Twitter-style thread images, batch image sets, and custom template outputs through local rendering workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams, developers, and agent users use this skill to produce reusable card-image assets for social media, brand communication, long-form post sharing, and batch visual content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to read files, run local Python or Chrome commands, and write generated outputs. <br>
Mitigation: Run it in a dedicated workspace and explicitly set input and output paths before execution. <br>
Risk: Batch and recursive processing can expose or overwrite unintended local files. <br>
Mitigation: Avoid recursive runs over private directories and review the output directory before starting batch jobs. <br>
Risk: The evidence notes inconsistent network and API-key guidance. <br>
Mitigation: Do not provide API keys unless the publisher documents which feature needs them and what data is sent externally. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated outputs are PNG files and JSON status records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local Python and Chrome rendering, batch generation, custom templates, text highlighting, and watermark options.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
