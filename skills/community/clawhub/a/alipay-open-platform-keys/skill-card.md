## Description:

Helps agents guide developers through local generation, rotation, and verification of Alipay Open Platform RSA2 key pairs and certificate-mode CSRs with OpenSSL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangke091](https://clawhub.ai/user/zhangke091)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate or rotate Alipay RSA2 application keys, create certificate-mode CSRs, align console configuration with SDK environment settings, and troubleshoot key or signature mismatches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default key generator command can print newly generated private signing keys to the terminal, where logs or agent transcripts may capture them.

Mitigation: Run the generator only on a trusted local machine, prefer --no-print, avoid shared or world-writable output directories, and rotate any private key that has appeared in logs or transcripts.

Risk: Generated private keys and CSRs may be mishandled after creation.

Mitigation: Keep private keys out of version control and chats, store generated files in trusted local directories, and follow the skill guidance to configure Alipay console and SDK settings from local files.

## Reference(s):

- [Skill reference guide](artifact/reference.md)
- [ClawHub skill page](https://clawhub.ai/zhangke091/skills/alipay-open-platform-keys)
- [Alipay Open Platform](https://open.alipay.com)
- [Alipay key generation documentation](https://opendocs.alipay.com/common/02kipl)
- [Alipay RSA2 key configuration support](https://opendocs.alipay.com/support/01raut)
- [Alipay key tool documentation](https://opendocs.alipay.com/mini/02c7i5)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local PEM key files, public key files, and certificate signing requests when the bundled shell scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
