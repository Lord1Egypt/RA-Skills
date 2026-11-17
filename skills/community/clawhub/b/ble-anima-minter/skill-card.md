## Description:

Scans nearby BLE MAC addresses, hashes them with a salt, and stores local proof nodes for soulbound $ANIMA token minting logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[penguinx01](https://clawhub.ai/user/penguinx01)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to run a local BLE scanning workflow that turns observed nearby Bluetooth identifiers into salted hashes and stores them as local DAG proof records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans nearby Bluetooth device identifiers and may collect observations without clear consent controls.

Mitigation: Run only where BLE scanning is authorized and appropriate, preferably in an isolated environment.

Risk: Raw Bluetooth MAC addresses can appear in terminal logs and deterministic hashes are saved locally.

Mitigation: Delete anima_dag.gpickle and related logs when no longer needed, and treat the hashes as sensitive device-observation data.

Risk: Future gossip-sync behavior could share nearby-device observations beyond the local machine.

Mitigation: Require explicit opt-in, scope limits, and review before enabling or extending any sharing behavior.

Risk: Dependencies are unpinned in requirements.txt.

Mitigation: Pin and review dependencies before installation.

## Reference(s):

- [ClawHub skill release: BLE → $ANIMA Minter](https://clawhub.ai/penguinx01/skills/ble-anima-minter)
- [ClawHub publisher profile: penguinx01](https://clawhub.ai/user/penguinx01)

## Skill Output:

**Output Type(s):** [guidance, shell commands, files]

**Output Format:** [Markdown guidance with inline bash commands; runtime output may include terminal logs and a local anima_dag.gpickle file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime script scans for 10 seconds, prints detected BLE MAC addresses and hashes, and writes hashed nodes to local DAG storage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
