# Networking — VPC, Firewalls, Private Access, Load Balancing

GCP's network is global where AWS's is regional, and that single difference invalidates most transplanted VPC designs. The other half of this file is Private Google Access and Private Service Connect, which is where the NAT bill goes to die.

**Contents:** [The Model, and Where It Differs](#the-model-and-where-it-differs) · [Address Planning](#address-planning) · [Firewall Rules](#firewall-rules) · [Reaching Google APIs Without a Public IP](#reaching-google-apis-without-a-public-ip) · [Private Service Connect and Peering](#private-service-connect-and-peering) · [Shared VPC](#shared-vpc) · [Cloud NAT](#cloud-nat) · [Load Balancing](#load-balancing) · [DNS](#dns) · [Connectivity Walk for an Unreachable Endpoint](#connectivity-walk-for-an-unreachable-endpoint)

## The Model, and Where It Differs

| Concept | GCP | Consequence |
|---|---|---|
| VPC | **Global** — one network spans every region | Multi-region does not need peering, and a single VPC is usually correct |
| Subnet | Regional, spans all zones in the region | No per-AZ subnet arithmetic; a zonal outage does not strand a subnet |
| Subnet range | Primary range **can be expanded** in place, never shrunk | Being slightly wrong on size is recoverable; being wrong upward is not |
| Secondary ranges | Alias IP ranges on a subnet, used by GKE pods and services | Sized at cluster creation, and they cap the cluster's pod count forever (`gke.md`) |
| Routes | Global routing table per network, with priorities | Cross-region traffic works by default; disable it deliberately if you want regional isolation |
| Firewall | Stateful, allow-and-deny with priorities, applied by tag or service account | There is no stateless NACL layer to forget about |
| Egress | Implied allow-all | An egress control posture requires explicit deny rules; nobody gets them for free |
| Ingress | Implied deny-all | Same as everywhere else |

The default VPC that a new project ships with has permissive firewall rules including SSH from anywhere. Delete it and build one, or at minimum delete `default-allow-ssh` and `default-allow-rdp`. `constraints/compute.skipDefaultNetworkCreation` prevents the problem for every future project (`organization.md`).

## Address Planning

Decisions that are expensive or impossible to change later.

- **Reserve for GKE first.** A cluster needs a primary range for nodes, a secondary for pods, and a secondary for services. Pod ranges are the greedy one: the per-node pod ceiling multiplies out fast, so a cluster that looks small consumes a wide block. Size it against the three-year node count, not today's.
- **Never overlap with anything you might peer to** — another VPC, an on-premises range, a partner, a future acquisition. Overlapping ranges cannot be peered, and renumbering a live network is a migration project.
- **Reserve a block for the service networking allocation** used by Cloud SQL private IP, Memorystore and other managed services. That allocation is a range you hand to Google once; growing it later is possible but the instances already placed do not move.
- **Regional prefix scheme** beats sequential allocation: encode region and environment in the address so a route table is readable. Record the scheme under `conventions.cidr_scheme` in `config.yaml` once the user states it.
- Private ranges other than RFC 1918 are allowed for subnets, which is the escape hatch when 10/8 is already spoken for.

## Firewall Rules

- **Priority 0-65535, lower wins, default 1000.** Two rules matching the same traffic resolve by priority, and a `deny` at 900 beats an `allow` at 1000.
- **Target by service account, not by network tag, wherever possible.** A tag is a string anyone with instance-edit rights can add to their own VM; a service account target requires the ability to run as that service account. Tags are convenient and forgeable; service accounts are the security boundary.
- **Hierarchical firewall policies** attach at the organization or folder and evaluate before VPC rules, with `goto_next` to delegate. The right home for "never allow 0.0.0.0/0 on 22 or 3389, anywhere, in any project".
- **Network firewall policies** are the newer per-network object with rule groups and better ordering than legacy rules. Prefer them for new builds; mixing both is legal and confusing.
- **Turn on firewall rules logging** on the deny rules that matter before you need them. Logging a broad allow rule is a Cloud Logging bill (`costs.md`).
- The rules everyone forgets:
  - **Health checks** arrive from `35.191.0.0/16` and `130.211.0.0/22`. Without an ingress allow from those ranges to the backend port, every backend is unhealthy and the load balancer returns 503 with no useful message. This is the single most-missed firewall rule in GCP.
  - **IAP TCP forwarding** arrives from `35.235.240.0/20`. Allow it and you get SSH with no external IP and no open port to the internet.

## Reaching Google APIs Without a Public IP

Default behaviour: a VM with no external IP cannot reach `storage.googleapis.com`, so teams add a NAT gateway and pay per GB to talk to Google. Three better answers:

| Mechanism | What it covers | Cost | Note |
|---|---|---|---|
| **Private Google Access** | Most Google APIs and services, from a VM with only an internal IP | Free | A **per-subnet** setting. Enable on every subnet that has private workloads; the failure mode is one subnet nobody flipped |
| **Private Service Connect endpoint** | Google APIs via an internal IP you choose, and consumer-producer services | Endpoint charge, no NAT data processing | Also works across peered networks, which Private Google Access does not |
| **Restricted / private VIPs** | Google APIs, with VPC Service Controls-compatible domains | Free | Required when a VPC-SC perimeter is in play; needs DNS records pointing `*.googleapis.com` at the restricted VIP (`security.md`) |

Artifact Registry pulls, Cloud Storage reads, Secret Manager fetches and Cloud Logging writes are all Google API traffic. Routing them through NAT is the most common avoidable line item on a GCP bill.

## Private Service Connect and Peering

- **VPC peering is not transitive.** A peered to B and B peered to C does not give A a path to C, and no route will make it. Hub-and-spoke designs built on peering silently lose every spoke-to-spoke path.
- **Managed services use a peering you do not control.** Cloud SQL private IP, Memorystore and others attach through the service networking connection. That peering's non-transitivity is why a second VPC, or an on-prem network reached by VPN, cannot see the Cloud SQL private IP by default — the fix is either PSC or a proxy, never a route.
- **Private Service Connect** is the answer to all of it: the consumer gets an internal IP in their own network, no ranges are shared, no transitivity problem exists, and the producer stays isolated. Cloud SQL, and a growing set of managed services, support PSC endpoints — prefer them over the legacy peering when starting fresh.
- **Peering ranges are exchanged, not routed selectively.** Import/export of custom routes is a per-peering setting people discover only when an on-prem route fails to propagate.

## Shared VPC

One **host project** owns the network; **service projects** attach workloads to it.

- Grant `roles/compute.networkUser` on the *subnet*, not the host project, so a team can use their subnet and not everyone else's.
- The host project is the correct home for firewall rules, Cloud NAT, Cloud Router, and the VPN or Interconnect. Centralizing them is the entire point.
- Service project workloads referencing host project resources need the network-user grant **and**, in some cases, the service agent of the product to be granted access — the errors when this is missing name the service agent, which is a principal nobody remembers creating.
- Correct when a network team exists or when environments must not reach each other by accident. Overkill for a solo builder with three projects, where one VPC per project and no peering is simpler.
- Record the host project in `## Org Context` (or the projects table) with its role stated — "which project owns the network" is a question that recurs monthly.

## Cloud NAT

- Regional, attached to a Cloud Router, and priced as an hourly gateway charge plus per-GB processed. Both parts matter: idle NAT still bills.
- **Port allocation is the failure mode.** Each VM gets a fixed number of source ports per NAT IP by default; a workload making many short-lived connections to the same destination exhausts them and new connections fail intermittently while the VM looks healthy. Enable dynamic port allocation, raise the minimum ports per VM, or add NAT IPs — and watch the dropped-connection metric before it becomes a mystery outage.
- **Log only the dropped connections** (not all), or NAT logging becomes a Logging bill on its own.
- Endpoint-independent mapping is on by default and is what makes NAT-to-NAT connectivity behave; changing it breaks some peer-to-peer protocols in unobvious ways.
- Before adding NAT, check what the traffic actually is. If it is Google APIs, the answer is Private Google Access and the NAT should not exist.

## Load Balancing

| Type | Use | Watch |
|---|---|---|
| Global external Application LB | Anycast HTTP(S) across regions, Cloud CDN, Cloud Armor, managed certs | Requires Premium network tier; the anycast IP is the reason to choose it |
| Regional external Application LB | Single-region HTTP(S), Standard tier eligible | Cheaper, no cross-region failover |
| Internal Application LB | HTTP(S) between services inside the VPC | Regional; needs a proxy-only subnet in the region, which must be created first |
| External passthrough Network LB | TCP/UDP at L4, preserves client IP | No TLS termination, no CDN |
| Internal passthrough Network LB | L4 inside the VPC, common for databases and appliances | Health checks still come from the Google ranges |

Rules that decide behaviour:

- **Backend service timeout defaults to 30 seconds** and is the top cause of 504s on long requests, streamed responses and websockets. Raise it deliberately; do not raise it to hide a slow backend.
- **Managed certificates need the DNS record to exist and resolve to the load balancer** before provisioning completes, and they stop renewing if that stops being true. The failure surfaces weeks later as an expired certificate. Record the dependency in the shared `domains.md` box.
- **Cloud Armor** attaches to the backend service, so a rule protects the backends behind it and nothing else. Preview mode first: a rate-limit rule tuned by guesswork blocks real users on day one.
- **Cloud CDN** is a flag on the backend service. Cache keys default to including the full query string; a URL with a cache-busting parameter per request has a 0% hit rate and full origin cost.
- Session affinity is best-effort and breaks on backend changes. Design stateless, or keep state in Memorystore.

## DNS

- **Cloud DNS private zones** are attached to networks; a VM resolves a private zone only if its network is authorized on the zone. Peered networks do not inherit it — a private zone must be shared to the peer explicitly.
- **Split-horizon** works by having a private zone shadow a public one for the same name. It is the standard way to keep an internal service on the corporate domain.
- **DNS forwarding** in both directions (to on-prem, and inbound from on-prem via an inbound server policy) is what makes hybrid name resolution work. The inbound policy creates resolver IPs in each subnet that on-prem must be pointed at.
- Internal DNS names for VMs exist automatically; zonal names are stable, and depending on the internal DNS setting the project-wide form may or may not be available. Do not build service discovery on them — use a private zone or a service mesh.
- Whenever a zone is created or an apex is pointed at a GCP load balancer, write the row into the shared `~/Clawic/data/domains/domains.md` (`memory-template.md`).

## Connectivity Walk for an Unreachable Endpoint

In order. Each step is a check, not a guess. **Connectivity Tests** in Network Intelligence Center runs most of this as a single simulated packet trace and names the blocking rule — start there when it is available.

1. **Firewall**: is there an ingress allow for the source range and port, and is a lower-priority deny beating it? Check the rule's target — tag or service account — actually matches the instance.
2. **Route**: does a route exist toward the destination, and is a higher-priority route sending it somewhere else? Custom routes from a peering or a VPN can shadow the default.
3. **Private Google Access**: for a Google API from a VM with no external IP, is PGA enabled *on that subnet*?
4. **Peering path**: is the destination behind a peering, and is the path transitive? If it is two hops, it does not work.
5. **Managed service networking**: for Cloud SQL or Memorystore private IP, is the caller in the VPC that holds the service networking connection, or is it a peer or VPN client that cannot cross it?
6. **DNS**: does the name resolve from the client's network, and to the address you expect? A private zone unauthorized on the client's network resolves to the public record instead — traffic then leaves the VPC and hits a firewall or a perimeter.
7. **VPC Service Controls**: for a Google API, is the caller inside the perimeter? Perimeter denials surface as vague 403s (`security.md`).
8. **The endpoint itself**: is the process listening on the interface you are hitting, not only on localhost?

When the walk changes the topology — a new subnet, a new peering, a PSC endpoint, an address plan — update `## Current Infrastructure` in `~/Clawic/data/gcp/memory.md` in the same turn, and if the address plan itself was designed here, save it to `~/Clawic/data/gcp/artifacts/network-plan.md` with its `## Boxes` line. A CIDR plan reconstructed from a live network six months later is a guess.
