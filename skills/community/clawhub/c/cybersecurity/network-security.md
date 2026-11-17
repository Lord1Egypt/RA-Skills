# Network Security — Exposure, Segmentation, Egress

Two jobs: know what you expose, and make sure one compromised host is one compromised host.

**Before touching a network**, read `## Scope & Authorization` in `~/Clawic/data/cybersecurity/memory.md` — active scanning of a segment you do not own, or of OT and medical devices, is the fastest way to turn an assessment into an outage you caused — plus `## Environment` for the trust boundaries already mapped and `~/Clawic/data/servers/servers.md` for what is supposed to be out there.

**Contents:** [Discover The Surface First](#discover-the-surface-first) · [Scanning Safely](#scanning-safely) · [The Exposure Checklist](#the-exposure-checklist) · [Edge Devices Are The Initial Access Story](#edge-devices-are-the-initial-access-story) · [Segmentation That Removes A Path](#segmentation-that-removes-a-path) · [Egress Is The Control Nobody Implements](#egress-is-the-control-nobody-implements) · [DNS](#dns) · [Remote Access](#remote-access) · [TLS And Certificates](#tls-and-certificates) · [Wireless And The Office](#wireless-and-the-office) · [OT, Medical And Legacy Segments](#ot-medical-and-legacy-segments)

## Discover The Surface First

You cannot defend an inventory you do not have, and the assets missing from the inventory are disproportionately the vulnerable ones — nobody patches what nobody remembers.

External surface, in the order that finds forgotten things:

1. **Domains and subdomains**: certificate transparency logs (every TLS certificate issued for your domains is public, which repeatedly surfaces staging hosts nobody meant to expose), DNS records, registrar inventory, and historical DNS.
2. **IP ranges**: your allocations, your cloud accounts' public addresses, and anything a provider assigned dynamically that a DNS record still points at.
3. **Services on those addresses**: internet-wide scan datasets (Shodan, Censys and equivalents) show what the world already sees, at zero risk of causing an outage, and often show things your own scanner's scope excludes.
4. **Cloud-native exposure**: public storage buckets, managed databases with public endpoints, load balancers, API gateways, and functions with public URLs. These bypass the network team entirely because they are created with an API call.
5. **The shadow surface**: marketing sites, campaign microsites, a developer's demo, an acquired company's estate, an expired domain still trusted by your systems.

**Dangling DNS is the highest-value cheap finding**: a CNAME pointing at a deprovisioned cloud resource lets anyone who claims that resource serve content on your hostname, receive its cookies, and pass domain-validated certificate issuance. Sweep for unresolvable or unclaimed targets on every DNS record, on a `## Due` cadence.

Internal surface: passive first — ARP tables, DHCP leases, switch MAC tables, existing flow logs, the identity provider's device list, the EDR console. Passive discovery finds most of the estate and cannot break anything.

## Scanning Safely

- Get the scan in writing, with windows, source addresses and exclusions, in `## Scope & Authorization`. Verbal permission for "the network" is not authorization for the segment you did not know was there.
- Start slow and non-intrusive; escalate rate only after the first pass shows nothing fragile.
- **Never aggressively scan OT, medical, building-management or legacy segments.** Some devices fail on a single unexpected packet, and a scan-induced outage of a production line or a clinical device is your incident, with your name on it.
- Cloud provider terms permit testing of your own resources within stated limits; managed services and other tenants are off limits. Read the current policy rather than a remembered one.
- Announce to the network and service teams. An unannounced scan consumes somebody's afternoon and burns the goodwill you need next quarter.
- Scanning from inside and outside gives two different answers, and the difference between them *is* the perimeter's actual shape.

## The Exposure Checklist

Anything on this list reachable from the internet is a finding until justified:

| Exposed | Why it is a finding |
|---|---|
| RDP (3389), SSH (22) with password authentication, VNC | Brute-forced and sprayed continuously; a favoured ransomware entry point |
| SMB (445), NetBIOS, RPC | No legitimate reason to be internet-facing, ever |
| Database ports: 3306, 5432, 1433, 27017, 6379, 9200 | Frequently with default or absent authentication; internet-wide scans find them in minutes |
| Management interfaces: hypervisor, iDRAC/iLO/IPMI, switch, firewall admin, printer | Full control of the platform, and the credentials are often the vendor default |
| Kubernetes API, container registries, etcd, Docker daemon (2375) | Cluster takeover in one request when unauthenticated |
| CI/CD consoles, artifact repositories, monitoring dashboards | Deploy access, secrets, and a map of the estate |
| Anything on a non-standard port that is "hidden" | Internet-wide scanning enumerates every port; obscurity is not a control |
| Staging, UAT and dev environments | Same data, weaker controls, no monitoring |

For each, the answer is one of: remove it, put it behind the VPN or an identity-aware proxy, restrict source addresses to a named list, or accept it formally with a compensating control and an expiry.

## Edge Devices Are The Initial Access Story

VPN concentrators, firewalls, gateways, file-transfer appliances and load balancers have been the most reliably mass-exploited class of recent years, and they share the properties that make that inevitable: internet-facing by design, complex code, opaque to EDR, and excluded from the scanner because "they are not servers".

- Patch them on the KEV clock, ahead of everything else. When a vendor advisory lands for an edge appliance, treat it as an emergency change, not a maintenance-window item.
- Management interfaces are never internet-facing. Not "restricted to our IPs" — off the internet.
- **Assume compromise on patch**: for the appliance classes with a history of mass exploitation, patching after public exploitation began is not enough. Rotate every credential and certificate on the device, check for configuration changes and added accounts, and follow the vendor's compromise-assessment guidance if one exists.
- Export their logs somewhere else, because the on-device log is the first thing an operator clears and the storage is tiny anyway.
- Inventory them as first-class assets in `~/Clawic/data/servers/servers.md` with an owner. The appliance nobody owns is the one nobody patches.

## Segmentation That Removes A Path

Segmentation is only real when it stops a specific movement. Name the movement first.

- **The highest-value segment boundary in most organizations is user-workstation to user-workstation.** Workstations rarely need to talk to each other; blocking SMB and RDP between them removes the lateral movement that turns one phish into the estate. It is one policy and it breaks almost nothing.
- **Second: the management plane.** Hypervisors, backup infrastructure, directory services and network device administration on a segment reachable only from a hardened jump path. This is what stops a workstation compromise becoming a hypervisor compromise.
- **Third: the crown jewel.** The database segment with no internet route and a short list of callers.
- Flat networks with a firewall only at the perimeter are the norm and are the reason lateral movement is trivial. Any internal boundary is a substantial improvement over none.
- Micro-segmentation and zero-trust network access are the mature versions; they are worth it once identity-aware proxying is in place and the inventory is accurate. Attempted before either, they produce an outage and a rollback.
- **Test the segmentation.** An untested rule set is a diagram. Try to reach the database segment from a workstation and record the result — that test is a `## Due` item, and the result belongs in `## Environment`.
- Every exception in the rule set carries an owner and an expiry, or the segmentation decays into a flat network with extra steps.

## Egress Is The Control Nobody Implements

**Allowing all outbound 443 allows command and control by definition.** Nearly every intrusion needs outbound connectivity; almost nobody constrains it.

- Servers are where this is achievable today: a server should reach a short, known list of destinations. Start there rather than with laptops, and you get most of the value for a fraction of the pain.
- Layers, from easiest to strongest: block direct outbound DNS except through your resolvers; block known-bad and newly registered domains at the resolver; force web traffic through a proxy that logs; then allowlist destinations for server segments.
- **Log what you cannot block.** Egress logging with no blocking still gives you the exfiltration answer during an incident, and it is the prerequisite for any future blocking.
- Beaconing detection lives here: regular intervals with low jitter, small consistent payload sizes, long-lived connections to a newly registered domain, and traffic to a cloud service the org does not use. Legitimate file-sharing and cloud-storage services are the modern exfiltration channel precisely because naive blocking of them breaks the business.
- Watch for the protocol mismatches: DNS with unusual query volume or long labels, ICMP with payloads, TLS on a non-standard port, and any protocol whose destination is an address rather than a name.

## DNS

- **Query logging is one of the cheapest high-value sources there is** (`detection.md` ranks it fifth overall and first per dollar). It sees C2 and exfiltration attempts even when the connection fails.
- Sinkholing is the quietest containment lever available: the operator sees a connection failure, not a block page.
- Your own DNS is an attack surface: registrar account compromise redirects your mail and issues certificates in your name. Registrar lock on, MFA on the registrar account, and the registrar account owned by somebody who still works there. Registrar, expiry and lock state live in `~/Clawic/data/domains/domains.md`.
- Watch for records nobody claims, wildcard records that hide new hosts, and zone transfers open to the world.
- DNS over HTTPS from endpoints bypasses your resolver and your logging entirely: decide the policy deliberately, and enforce it on managed devices.

## Remote Access

- Password-only VPN is a credential-stuffing target with a corporate network behind it. Phishing-resistant MFA, or replace it.
- **A VPN grants network access; an identity-aware proxy grants application access.** The second is strictly better where the application supports it, because a compromised endpoint reaches one app rather than a subnet.
- Split tunnelling is a trade: less backhaul, less visibility. If you split, keep DNS and security telemetry on the corporate path.
- Third-party and vendor access is the recurring incident: named accounts, time-boxed, scoped to one system, MFA, logged, and revoked on a date rather than on somebody's memory. A shared vendor account with permanent access is a finding by itself.
- SSH: keys only, no password authentication, no direct root login, a bastion or session-manager path rather than internet-exposed servers, and key inventory with owners. Recorded sessions where the platform offers them, because SSH is where the evidence usually is not.

## TLS And Certificates

- **Expiry is an outage with a date on it**, and it is the most predictable incident in existence. Every certificate gets a `## Due` row and, better, automated renewal with monitoring on the automation.
- Automate issuance; a manual annual renewal is a calendar invite that gets declined.
- Internal certificate authorities need the same care as public: a compromised internal CA lets an attacker impersonate any internal service and decrypt what they intercept.
- Certificate transparency monitoring for your domains catches both a mis-issued certificate and your own team standing up something unannounced.
- Modern configuration: TLS 1.2 minimum with 1.3 preferred, no legacy protocol versions, no expired or weak cipher suites, HSTS on public sites. Verify with an external scan rather than from the config file.

## Wireless And The Office

- Guest network genuinely isolated from corporate — verify by trying to reach a corporate host from it, do not assume the vendor's checkbox works.
- Corporate wireless on certificate-based authentication (EAP-TLS) rather than a shared passphrase that left with the last three employees.
- Rogue access points and unmanaged devices on the corporate segment: network access control is the full answer, and a periodic passive inventory against `~/Clawic/data/devices/devices.md` is the version everyone can afford.
- Physical ports in reachable areas are network access. Port security, or the meeting-room jack is an unauthenticated foothold.

## OT, Medical And Legacy Segments

Different rules, and the default assumptions are actively dangerous here:

- **Availability and safety outrank confidentiality.** A control that risks a process outage or a clinical device is usually the wrong control, whatever the vulnerability score.
- Passive discovery only. Protocol-aware passive monitoring exists for these environments; active scanning does not belong there.
- Patching follows the vendor's validated cycle, which may be annual or may not exist. The compensating control is isolation, not urgency.
- **Segmentation is the entire strategy**: a hard boundary with a small, enumerated set of allowed flows, and a jump path with its own authentication for engineering access. Assume the devices themselves cannot be secured.
- Remote vendor access into these segments is the recurring initial-access vector — time-boxed, brokered, supervised and logged, or not at all.
- Record the segment's exclusions in `## Scope & Authorization` explicitly, so nobody scans it during the next assessment because they did not know.

Write what the work produced (`memory-template.md`): the external attack surface — hostnames, exposed services, edge appliances and their owners — plus trust boundaries and the segmentation test result in `## Environment`; every host and appliance discovered in `~/Clawic/data/servers/servers.md` with its role, and every unmanaged device in `~/Clawic/data/devices/devices.md`; domains, registrar lock state, mail-authentication posture and certificate expiry in `~/Clawic/data/domains/domains.md`, with the expiries also as `## Due` rows because an inventory reminds nobody by itself; each exposure as a `## Findings` row with owner, due date and the path it removes; scan windows and OT exclusions in `## Scope & Authorization`; the egress allowlist and the firewall rule rationale, once derived, in `~/Clawic/data/cybersecurity/artifacts/` with its `## Boxes` line in the same turn — rebuilding it costs days and the reasons are what get lost first.
