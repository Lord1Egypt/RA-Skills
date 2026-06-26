# Threat Modeling Workflow

Use this flow when the user is designing, reviewing, or changing a system.

## Start With the System

- identify the asset, users, entry points, data flows, and trust boundaries
- name the attacker goals before listing controls
- ask what would hurt most if this component failed, leaked, or was abused

## Build the Attack Path

- start at the first realistic foothold, not the scariest exploit
- trace movement across identity, network, application, and human layers
- highlight assumptions that keep the path viable

## Prioritize Findings

- exploitability: what the attacker needs
- impact: what the attacker gains
- detection: how visible the attack is
- mitigation: what reduces risk fastest

## Good Output

- one-paragraph system summary
- top attack paths with confidence
- controls that already help
- missing controls in rollout order
- open questions blocking stronger conclusions
