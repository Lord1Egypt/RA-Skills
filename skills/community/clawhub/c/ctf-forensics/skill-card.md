## Description:

Provides digital forensics and signal analysis techniques for CTF challenges involving disk images, memory dumps, event logs, network captures, steganography, hardware signals, and recovery workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli](https://clawhub.ai/user/gandli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security practitioners, and CTF participants use this skill as a quick reference for investigating challenge artifacts, recovering hidden data, and choosing appropriate forensic tools and workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes guidance for credential extraction, remote probing, credential-vault transfer, package installation, disk reconstruction, and other high-impact forensic actions.

Mitigation: Use only in isolated, disposable CTF or explicitly authorized forensics environments, and require human review before running credential recovery, cloud access, network probing, ptrace, package install, or disk reconstruction steps.

Risk: Forensic commands can alter local systems, expose sensitive data, or produce misleading results when applied outside the intended challenge context.

Mitigation: Run commands against copies of challenge artifacts where possible, avoid personal, production, third-party, or live systems, and validate findings before relying on recovered data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gandli/skills/ctf-forensics)
- [3D Printing Forensics](artifact/3d-printing.md)
- [Disk and Memory Forensics](artifact/disk-and-memory.md)
- [Advanced Disk and Memory Techniques](artifact/disk-advanced.md)
- [Disk Recovery and Extraction Patterns](artifact/disk-recovery.md)
- [Linux and Application Forensics](artifact/linux-forensics.md)
- [Network Forensics](artifact/network.md)
- [Advanced Network Forensics](artifact/network-advanced.md)
- [Signals and Hardware Forensics](artifact/signals-and-hardware.md)
- [Steganography](artifact/steganography.md)
- [Image Steganography](artifact/stego-image.md)
- [Advanced Steganography](artifact/stego-advanced.md)
- [Advanced Steganography Part 2](artifact/stego-advanced-2.md)
- [Windows Forensics](artifact/windows.md)
- [Mempool Transaction API](https://mempool.space/api/tx/<TXID>)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include investigative procedures, package installation commands, forensic tool invocations, parsing snippets, and pivot guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
