## Description: <br>
Provides digital forensics and signal analysis techniques for CTF challenges, including disk images, memory dumps, event logs, network captures, steganography, Windows artifacts, Volatility, PCAPs, side-channel traces, audio spectrograms, and deleted file or credential recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gandli](https://clawhub.ai/user/gandli) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, security practitioners, and CTF competitors use this skill as a forensics quick reference for choosing tools, commands, and analysis paths when investigating challenge artifacts. It focuses on lab and competition evidence such as disk images, memory dumps, packet captures, logs, media files, and steganographic payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags under-scoped credential extraction guidance. <br>
Mitigation: Use the skill only on authorized CTF or lab artifacts, avoid personal or third-party browser profiles and password vaults, and review commands before running them. <br>
Risk: The security summary flags live probing and forged DNSSEC response guidance. <br>
Mitigation: Run network probing only with explicit authorization and avoid using the guidance against live third-party systems. <br>
Risk: The security summary flags evidence-modifying commands. <br>
Mitigation: Analyze copies of evidence, prefer read-only mounts where possible, and keep original disk images unchanged. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gandli/ctf-forensics) <br>
- [SKILL.md](SKILL.md) <br>
- [Disk and memory forensics](disk-and-memory.md) <br>
- [Advanced disk and memory techniques](disk-advanced.md) <br>
- [Disk recovery and extraction patterns](disk-recovery.md) <br>
- [Network forensics basics](network.md) <br>
- [Advanced network forensics](network-advanced.md) <br>
- [Steganography reference](steganography.md) <br>
- [Image steganography reference](stego-image.md) <br>
- [Advanced steganography part 1](stego-advanced.md) <br>
- [Advanced steganography part 2](stego-advanced-2.md) <br>
- [Linux and application forensics](linux-forensics.md) <br>
- [Windows forensics](windows.md) <br>
- [Signals and hardware forensics](signals-and-hardware.md) <br>
- [3D printing forensics](3d-printing.md) <br>
- [mempool.space transaction API](https://mempool.space/api/tx/<TXID) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, checklists, and reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended for CTF and lab artifacts and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
