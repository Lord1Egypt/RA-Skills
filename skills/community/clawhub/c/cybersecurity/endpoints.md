# Endpoints — Baselines, EDR, Patching, BYOD

Laptops, servers and phones: what to configure, what EDR does and does not see, and how to keep a fleet patched without an outage.

**Before hardening or investigating a device**, read `~/Clawic/data/devices/devices.md` (what is known about this machine: owner, OS, encryption, MDM enrolment, EDR presence) and `## Environment` in `~/Clawic/data/cybersecurity/memory.md` for the fleet composition and the EDR coverage gaps already recorded. `edr_platform` and `platform.os_mix` in `config.yaml` decide which of the baselines below apply.

**Contents:** [The Baseline That Removes The Most Path](#the-baseline-that-removes-the-most-path) · [Windows](#windows) · [macOS](#macos) · [Linux Servers](#linux-servers) · [Mobile](#mobile) · [What EDR Sees, And What It Does Not](#what-edr-sees-and-what-it-does-not) · [Deploying EDR Without Breaking Production](#deploying-edr-without-breaking-production) · [Patching A Fleet](#patching-a-fleet) · [Application Control, Realistically](#application-control-realistically) · [BYOD And Unmanaged Devices](#byod-and-unmanaged-devices) · [Removable Media](#removable-media) · [Device Loss And Disposal](#device-loss-and-disposal)

## The Baseline That Removes The Most Path

Ordered by path removed per unit of effort, and true on every platform:

1. **Full-disk encryption with escrowed recovery keys.** Removes the lost-laptop breach entirely, and it is the one control that converts a notifiable incident into a non-event.
2. **No local administrator for daily use**, plus **unique local administrator passwords per machine**, rotated automatically. Shared local admin is the mechanism that turns one workstation into the whole fleet.
3. **Automatic OS and browser updates**, with a deadline the user cannot postpone indefinitely. The browser is the internet-facing application on every endpoint.
4. **EDR in block mode with somebody who responds.** Detect-only is a 3am alert with nobody to act on it.
5. **Host firewall inbound-deny by default.** Workstations do not need to serve anything.
6. **Screen lock with a short timeout and a real credential.**
7. **Managed enrolment (MDM)** so the six above are enforced and verifiable rather than requested. A baseline you cannot measure is a suggestion.

Everything below adds to this. An organization that only ever achieves this list is in better shape than most.

## Windows

- **LAPS or equivalent** for unique local administrator passwords — the highest-value single Windows control.
- **Attack surface reduction rules** in block mode: Office spawning child processes, script-launched executables, credential access from LSASS, executable content from mail and webmail, and untrusted USB executables. These block real initial-access techniques and cost nothing but testing.
- **Credential protections**: LSA protection, Credential Guard where the hardware supports it, and no cached credentials on machines that never leave the network.
- **Command-line auditing (4688) and PowerShell script-block logging** on, forwarded off the host. Their absence is the most expensive investigative gap on Windows, and it cannot be filled retroactively.
- **Constrained language mode or application control** for PowerShell where feasible, plus AMSI enabled and not excluded.
- **Macros from the internet blocked** by policy; the Mark-of-the-Web must survive your file-transfer path, or the block silently does nothing.
- **SMB signing required, SMBv1 removed, LLMNR and NBT-NS disabled** — the last two remove the relay and poisoning attacks that need no vulnerability at all.
- Windows servers: no browsing or mail, RDP restricted to a jump path with MFA, and the print spooler disabled where it is not needed.

## macOS

- **FileVault on with keys escrowed to MDM.** Without escrow, encryption is a data-loss risk trading against a data-breach risk.
- **Gatekeeper and notarization enforced**; System Integrity Protection never disabled — an SIP-disabled machine is a finding by itself.
- **Configuration profiles via MDM** for the baseline, with the profile inventory reviewed: a profile is also how an attacker persists.
- **TCC permissions reviewed**: full disk access and accessibility are the two an attacker actually wants, and the applications holding them are a short list worth reading.
- **Persistence surfaces to monitor**: launch agents and daemons, login items, and configuration profiles. Most macOS malware lives in one of those three.
- Unified log retention is short — days on a busy machine. If macOS matters to your investigations, forward the relevant subsystems off the host now, not during the incident.
- Local admin rights are commonly granted to every developer. Where that is unavoidable, compensate with EDR, MDM enforcement of the baseline, and no shared local admin credential.

## Linux Servers

- **SSH keys only**, no password authentication, no direct root login, and a bastion or session-manager path rather than internet-exposed hosts.
- **auditd configured before you need it.** Without it there is essentially no execution evidence on Linux, and no amount of skill recovers it afterwards.
- Unattended security updates for the distribution, with a reboot policy — a patched kernel that never reboots is an unpatched kernel.
- Minimal package surface: no compilers, no unnecessary daemons, and a host firewall that permits only the service ports.
- **Immutable infrastructure beats patching where it is achievable**: rebuild from a new image rather than updating in place, and the drift problem disappears with it.
- SELinux or AppArmor in enforcing mode. Disabling it "temporarily" is permanent in every environment where it has ever happened.
- Containers: a compromised container's filesystem disappears on restart, so capture from the host during an incident (`forensics.md`), and treat the image as the durable artifact. Container escape is a real path — no `--privileged`, drop capabilities, non-root user, read-only root filesystem.

## Mobile

- Phones hold the second factor, the mail and the session cookies, which makes them an identity asset rather than a peripheral. Treat a lost unlocked phone as an identity incident, not an inventory event.
- Minimum on any device that receives corporate mail: passcode enforced, OS updates current, disk encryption (on by default with a passcode on both major platforms), and remote wipe or selective wipe available.
- Enforce through conditional access on device compliance. A mobile policy that is not an access condition is a document.
- **Jailbroken or rooted devices are out**, detected by the management platform and blocked at access. The device's own security guarantees are what everything else assumes.
- Sideloaded applications and enterprise-signed profiles are the mobile persistence surface; on managed devices, restrict installation sources and review installed configuration profiles.
- SMS as a second factor is worse on mobile than anywhere else, because compromising the phone compromises both factors at once (`identity.md` ranks the factors).
- Attacks needing no user interaction exist for messaging and image-parsing stacks; the defence is current OS versions and the platform's own lockdown mode for high-risk individuals — not an endpoint agent, since mobile platforms do not grant one the visibility EDR has elsewhere.

## What EDR Sees, And What It Does Not

Sets the honest expectation, and every row is a scope statement you should be able to give from memory:

| Sees well | Blind or partial |
|---|---|
| Process execution, ancestry, command lines | Anything on a device with no agent — the whole shadow fleet |
| File and registry modification | Firmware, BIOS/UEFI, and pre-boot |
| Network connections initiated by processes | Network devices, appliances, printers, cameras, OT |
| Credential-access behaviour on the endpoint | **Authentication that happens elsewhere** — SaaS, cloud console, identity provider |
| Known malware and many behaviours | Living-off-the-land use of legitimate admin tooling, when it looks like administration |
| Persistence mechanism creation | Activity inside a container, unless deployed to see it |
| Script execution where the platform is instrumented | Encrypted traffic contents, and much of what happens inside a browser |

**The load-bearing gap is the fourth row.** A modern intrusion authenticates to cloud and SaaS from an unmanaged machine, and EDR never sees any of it. That is why identity telemetry outranks endpoint telemetry in `detection.md`'s source ranking, and why "EDR shows nothing on the other hosts" is not a scope conclusion.

Tampering matters as much as coverage: alert on agent stop, uninstall, and any host that stops checking in. The console's last check-in timestamp is a high-confidence event in an incident timeline.

## Deploying EDR Without Breaking Production

- Detect-only first, everywhere, for two to four weeks. Learn the environment's normal before anything blocks.
- Roll block mode out in rings: IT, then a pilot department, then the fleet. Servers last and individually — a false positive on a database server is an outage.
- Performance-sensitive systems (build servers, databases, trading systems, CI runners) need tested exclusions. **Exclusions are the attacker's allowlist**: narrow, dated, owned, and reviewed quarterly as a `## Due` item.
- Verify coverage against an authoritative asset list rather than the EDR console's own list — the console cannot show you the machines it is not on. The delta between MDM enrolment, directory objects and EDR agents is the shadow fleet, and it is never zero.
- Tune before enabling paging. An EDR deployed straight to a pager produces an abandoned queue in a fortnight (`detection.md` has the precision math).

## Patching A Fleet

- **Ring deployment**: canary (IT, a handful of machines), early (5-10%), broad, then the exceptions. Each ring soaks for a defined period, and a defect stops the promotion.
- Emergency path for KEV and edge devices, with pre-approved change authority. Waiting for the weekly change board with a known-exploited internet-facing vulnerability is a decision with a foreseeable outcome (`vulnerabilities.md` holds the prioritization gate).
- **Measure compliance as a percentage of known assets patched within the SLA**, not as a count of patches deployed. The second number rises when the estate gets worse.
- The unpatchable tail — legacy applications, certified systems, one machine that runs the payroll software — gets isolation, monitoring and a dated risk acceptance, never silence.
- Reboots are part of patching. Track uptime as a patch metric: a 400-day uptime is a server carrying a year of unapplied kernel fixes.
- Third-party applications are the bigger surface than the OS on workstations: browsers, PDF readers, communication tools, developer runtimes. A software-deployment tool that only patches the OS covers the smaller half.

## Application Control, Realistically

Extremely effective and expensive to operate — the honest framing rather than the vendor's.

- Full allowlisting suits fixed-function machines: kiosks, point of sale, industrial controllers, servers with a stable workload. There, it is close to a complete answer.
- General-purpose workstations, especially developer machines, fight it constantly. The usual failure is an exception process so slow that somebody grants a blanket exception and the control becomes decorative.
- The affordable middle: block execution from user-writable locations (downloads, temp, profile directories) where nothing legitimate should run, and block the scripting hosts nobody uses.
- Publisher-based rules are more maintainable than hash-based, which need updating on every release.
- Audit mode first, for months, on real users. The exception list you discover is the deployment plan.

## BYOD And Unmanaged Devices

- **Decide the model explicitly**: full management, application-level management (a managed container for corporate data), or browser-only access with no local data. The third is underused and is the cleanest answer for contractors and personal devices.
- Conditional access on device compliance is the enforcement point. Without it, "BYOD policy" is a document the attacker has not read.
- On a personal device, a remote wipe of the whole device is a legal and human problem. Selective wipe of the managed container is the only sustainable answer, and the policy has to say which one applies before anybody needs it.
- Contractor and vendor devices: browser-only through an identity-aware proxy, or a corporate machine. A contractor's unmanaged laptop with a session cookie is an unmonitored endpoint inside your trust boundary.
- Every unmanaged device found on the corporate network is both a `## Findings` row and a row in `~/Clawic/data/devices/devices.md`. The inventory is what makes the next discovery a comparison rather than a surprise.

## Removable Media

- Block or read-only by default; allow by exception with encryption enforced. The exception list is short in every organization that has actually looked.
- Block executable content from removable media even where the media itself is allowed — this is one of the highest-value attack-surface reduction rules.
- The realistic threat is data walking out rather than malware walking in; the logging matters as much as the block.
- Where USB must be permitted for a business reason, restrict by device id and log every mount.

## Device Loss And Disposal

- Loss with full-disk encryption on and the device powered off is an inventory event, not a breach — and that distinction, documented, is what a notification decision rests on. Powered-on-and-unlocked is a different answer, which is why the screen-lock timeout is a breach control.
- Response: remote lock or wipe where enrolled, revoke the device's sessions and tokens in the identity provider (`identity.md`), and record it. Revoking the sessions is the step people forget, and it is the one that matters when the disk is encrypted.
- Disposal: cryptographic erase for self-encrypting drives, verified wipe otherwise, and physical destruction for anything that held regulated data and cannot be verified. Get a certificate from the disposal vendor; the vendor is also a third party holding your data (`supply-chain.md`).
- Delete the row from `~/Clawic/data/devices/devices.md` and note the date. An inventory that only grows stops being an inventory.

Write it (`memory-template.md`): every device discovered, hardened or retired as a row in `~/Clawic/data/devices/devices.md` with its owner, OS, encryption, MDM and EDR state — one row per device, matched on the device name and updated in place; servers in `~/Clawic/data/servers/servers.md`; fleet composition, EDR coverage percentage and the named blind spots in `## Environment`, because the blind spots decide what an incident can conclude; each gap — unencrypted machine, unmanaged device, missing agent, unpatchable host — as a `## Findings` row with owner, due date and the path it removes; the unpatchable tail in `## Risk Accepted` with expiry and a `## Due` row; agent-tampering and exclusion-review detections in `## Detections`; patch-compliance review and EDR exclusion review as `## Due` rows; the tested baseline and its exception list in `~/Clawic/data/cybersecurity/artifacts/` with its `## Boxes` line in the same turn — the exceptions took months to discover and nobody should rediscover them.
