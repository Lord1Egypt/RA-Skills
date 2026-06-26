## Description: <br>
Edits images to beautify faces or portraits using BitSoul beauty parameters and a downloaded native image-processing tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhi43](https://clawhub.ai/user/wangzhi43) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to configure face-beauty presets, prepare JSON parameters, and run the BitSoul image beautification binary on local photos. It requires a BITSOUL_TOKEN for permission verification before downloading and running the native tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs a native binary that is not accompanied by verifiable hashes or signatures in the evidence. <br>
Mitigation: Install only if the publisher is trusted, and verify the downloaded binary out of band before running it on valuable data. <br>
Risk: The security summary reports token transmission over plain HTTP. <br>
Mitigation: Avoid using sensitive photos or valuable tokens until remote calls use HTTPS and token handling is clearly documented. <br>
Risk: The skill processes personal photos and requires a BITSOUL_TOKEN for permission verification. <br>
Mitigation: Use test or low-sensitivity images first, keep the token in an external environment variable or env file, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangzhi43/bitsoul-face-beauty-pro) <br>
- [BitSoul token registration](https://www.aicodingyard.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with JSON parameter snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary JSON parameter files and output directories for edited images.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
