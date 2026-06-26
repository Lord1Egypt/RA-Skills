## Description: <br>
Scans nearby BLE MAC addresses, hashes each identifier with a salt, and stores proof records for soulbound $ANIMA minting in a local DAG file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PenguinX01](https://clawhub.ai/user/PenguinX01) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill when they intentionally want an agent workflow to scan nearby Bluetooth Low Energy devices, hash observed MAC addresses, and create local $ANIMA proof records for later review or synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BLE scanning can expose or correlate nearby device identifiers through terminal output, logs, or the generated DAG file. <br>
Mitigation: Run only when BLE scanning is intended, treat terminal output and anima_dag.gpickle as sensitive, and delete generated data when it is no longer needed. <br>
Risk: Dependencies are unpinned, so future installs may resolve different package versions. <br>
Mitigation: Pin dependency versions before operational use and review resolved packages during installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PenguinX01/ble-anima-minter) <br>
- [Publisher profile](https://clawhub.ai/user/PenguinX01) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Terminal output and a local NetworkX gpickle DAG file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes anima_dag.gpickle locally and may print observed BLE MAC addresses and hashes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
