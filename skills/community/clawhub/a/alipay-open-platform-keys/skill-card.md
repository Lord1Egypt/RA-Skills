## Description: <br>
Helps agents guide developers through local Alipay Open Platform RSA2 key-pair generation, certificate-mode CSR creation, key-pair verification, and the required handoff to Alipay console and SDK configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangke091](https://clawhub.ai/user/zhangke091) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when generating or rotating Alipay Open Platform RSA2 application keys, creating certificate-mode CSRs, checking whether key files match, and aligning generated artifacts with console and SDK configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated private keys can be printed to the terminal or captured by an agent, shell history, logs, or CI output. <br>
Mitigation: Run key generation only in a trusted local directory, prefer --no-print for agent or CI use, and never paste generated private keys into chat. <br>
Risk: Payment credentials or generated PEM and CSR files could be committed or shared accidentally. <br>
Mitigation: Keep *.pem, *.csr, and alipay_keys_* outputs out of version control and review the scripts before using production payment credentials. <br>


## Reference(s): <br>
- [Skill reference guide](reference.md) <br>
- [ClawHub release page](https://clawhub.ai/zhangke091/alipay-open-platform-keys) <br>
- [Alipay Open Platform](https://open.alipay.com) <br>
- [Alipay key generation documentation](https://opendocs.alipay.com/common/02kipl) <br>
- [Alipay RSA2 key configuration support](https://opendocs.alipay.com/support/01raut) <br>
- [Alipay key tool documentation](https://opendocs.alipay.com/mini/02c7i5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and file path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local PEM and CSR files when the user runs the bundled shell scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
