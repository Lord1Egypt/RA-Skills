# Release Notes - 0.4.0

This release packages a publishable defensive skill scaffold for clawhub.ai and restores the executable helper scripts that make the scanner and adapter workflows usable end to end.

Highlights:
- Clear defensive posture and safety boundaries
- OpenClaw, Hermes, host, and skill-supply-chain adapters
- Explicit scan workflow with staged ClawHub installs
- Quarantine policy for already-installed skills only
- Executable helper scripts for scan, staged install, quarantine, and adapter health flows
- Publication copy suitable for repository and marketplace listing

Operational summary:
- Scan candidate skills before install when possible
- Block High/Critical findings
- Allow Medium/Low/Info with warnings
- Preserve evidence before remediation
- Prefer fresh sessions or containment over trying to recover a poisoned thread
