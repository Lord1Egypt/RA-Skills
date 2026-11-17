# Debugging GCP — Symptom to Cause

GCP failures are opaque for a specific reason: the platform returns a small set of status codes for a large set of unrelated causes, and the useful detail is in the audit log rather than the response. Work symptom-first; every step below is a check, not a guess.

**Contents:** [The Universal First Three](#the-universal-first-three) · [403 Is Five Different Problems](#403-is-five-different-problems) · [Quota, Capacity, and Rate](#quota-capacity-and-rate) · [Timeouts and Hangs](#timeouts-and-hangs) · [5xx From a Load Balancer](#5xx-from-a-load-balancer) · [Deploy Failures](#deploy-failures) · [Reading the Logs](#reading-the-logs) · [Works in the Console, Fails in Code](#works-in-the-console-fails-in-code) · [When You Are Truly Stuck](#when-you-are-truly-stuck)

## The Universal First Three

1. **Who am I, and in which project?** Print the active account, project and region from the same context that is failing. A local CLI runs as your user, a deployed service runs as its attached service account, and a client library runs as whatever Application Default Credentials resolved to — which can be a third identity nobody chose (`commands.md`).
2. **What did the API actually see?** Cloud Audit Logs record every admin action with the principal, the method, the request parameters and the exact error. Look the call up by method name before theorizing. Admin Activity logs are always on and free, so this evidence always exists.
3. **Is the API even enabled?** A disabled API returns 403 with a message about the API not being used in the project. It is not a permissions problem, it takes ten seconds to rule out, and it is the most common wrong diagnosis in GCP.

## 403 Is Five Different Problems

| Message contains | Cause | Fix |
|---|---|---|
| "has not been used in project … or it is disabled" | Service not enabled | Enable the API. Nothing about IAM is wrong |
| `PERMISSION_DENIED` naming a specific permission | Missing role binding, or bound at the wrong resource | Policy Troubleshooter with principal + resource + permission (`iam.md`) |
| `iam.serviceAccounts.actAs` | Caller may create the resource but not attach that service account | `roles/iam.serviceAccountUser` on the exact service account (`iam.md`) |
| "Request is prohibited by organization's policy" | An org policy constraint, not IAM | Find the constraint; it is usually external IP, public access prevention, or resource locations (`organization.md`) |
| Vague denial with a unique request identifier, or an explicit VPC-SC mention | VPC Service Controls perimeter | The perimeter and blocked service are named in the audit log, not in the response (`security.md`) |

A sixth case that is not really a 403: eventual consistency. A binding created seconds ago may not be visible yet. Retry once. Never grant a broader role during the propagation window — that grant outlives everyone's memory of why it exists.

## Quota, Capacity, and Rate

Three different failures that all sound like "we hit a limit".

- **Quota (allocation)** — how much of a resource you may hold at once: CPUs, IPs, GPUs, per project per region. Exceeding it fails resource creation with a quota message. Several defaults are **zero**, notably GPUs and TPUs, and an increase is a request with a human in the loop that takes days (SKILL.md Rule 8).
- **Quota (rate)** — requests per minute against an API. Surfaces as 429 `RESOURCE_EXHAUSTED`. Fix with exponential backoff plus jitter first; request an increase only after the client is well-behaved, because a badly-behaved client will exhaust the new limit too.
- **Capacity** — `ZONE_RESOURCE_POOL_EXHAUSTED` and its relatives mean Google has none of that machine type in that zone right now. Quota is irrelevant; raising it changes nothing. Move zone, change machine family, or hold a reservation. Scarce shapes (large GPU types, newest families) are where this bites.

Every quota you check, request, or get granted goes in `## Quotas` in `~/Clawic/data/gcp/memory.md` with the observed peak — the peak is what makes the next request credible (`memory-template.md`).

## Timeouts and Hangs

A bare timeout is almost always the network, not permissions. The distinction is diagnostic:

| Observation | Meaning |
|---|---|
| Connection times out | Path problem — firewall, route, peering, Private Google Access, or a perimeter |
| Connection refused | Path is fine, nothing is listening on that port |
| TLS handshake fails | Path and listener are fine; certificate, SNI or protocol mismatch |
| `password authentication failed`, `access denied` | Path is fine — this is credentials |
| Slow then fails at a round number (30s, 60s, 600s) | A configured timeout fired. Find which layer owns that number |

Round-number timeouts worth memorizing: load balancer backend service **30s** default; Cloud Run request ceiling up to **60 min** but often set far lower; Pub/Sub ack deadline **10s** default; Cloud Functions gen1 **9 min** hard cap. When the failure lands exactly on one of these, the timeout is the cause and everything upstream is a symptom.

Full connectivity walk: `networking.md`.

## 5xx From a Load Balancer

| Code | Most likely cause | First move |
|---|---|---|
| 502 | Backend closed the connection, returned an invalid response, or died mid-request | Backend logs first. If the backend looks healthy, raise its keep-alive above the load balancer's so the LB never reuses a connection the backend is about to close |
| 503 | No healthy backends | Health-check firewall from `35.191.0.0/16` and `130.211.0.0/22`, then the check's path/port/protocol, then whether the backend is actually serving that path (`networking.md`) |
| 504 | Backend slower than the backend service timeout (30s default) | 504 is time, 502 is a broken connection. Fix the slow path before raising the timeout |
| 429 from Cloud Armor | A rate-limit rule matched | Check the Cloud Armor logs for the matched rule; preview mode before enforcing |
| Intermittent 502/503 under load only | Backend saturation, or NAT port exhaustion on the outbound side | Backend utilization and NAT dropped-connection metrics together |

Load balancer request logs carry a `statusDetails` field that names the internal reason — `failed_to_pick_backend`, `backend_connection_closed_before_data_sent_to_client`, `client_disconnected_before_any_response`. Read it before guessing; it distinguishes "the backend broke" from "the client left".

## Deploy Failures

| Symptom | Cause |
|---|---|
| Cloud Run: "container failed to start and listen on the port" | The app is not listening on `$PORT` (8080 by default) on `0.0.0.0`, or startup is slower than the probe allows. Binding to `127.0.0.1` fails exactly this way (`run.md`) |
| Cloud Run / GKE: image pull denied | The runtime service account lacks `roles/artifactregistry.reader`, or the image is in another project's registry |
| GKE: pod `Unschedulable` | No node fits the request. On Autopilot, the request itself may violate a CPU:memory ratio rule (`gke.md`) |
| GKE: `ImagePullBackOff` in a private cluster | No path to Artifact Registry: missing Private Google Access, or no NAT and no PSC endpoint (`networking.md`) |
| Terraform: 403 on create | The Terraform service account, not your user, lacks the role. Check the identity Terraform authenticated as (`iac.md`) |
| Cloud Build: permission denied on first run | The Cloud Build service account has no roles for what the build deploys. Grant before the first run, not after (`iac.md`) |
| Anything: "resource already exists" after a failed apply | A partially-created resource that state does not know about. Import it rather than renaming around it (`iac.md`) |

## Reading the Logs

- **Log Explorer query language** is the tool. `resource.type`, `severity>=ERROR`, `protoPayload.methodName`, `protoPayload.authenticationInfo.principalEmail`, `httpRequest.status`. Filter by resource type first — it is indexed and it cuts the search space hardest.
- **Audit log categories**: Admin Activity (always on, free, every write operation), Data Access (off by default except BigQuery, billable, and this is the one that produces a Logging bill when enabled org-wide), System Event, Policy Denied (which is where org policy and VPC-SC denials appear).
- **Correlate by trace**: requests through a load balancer or Cloud Run carry a trace id. Filter by it to get every log line of one request across services — far faster than reading each service's logs in sequence.
- **Log-based metrics** turn a recurring error into a number you can alert on. Cheaper and faster than exporting logs to BigQuery for the same question (`production.md`).
- **Error Reporting** groups by stack trace, which means the same fault with a formatted message per occurrence appears as many distinct groups. Log the exception with a stable message and the variable data in structured fields.
- Structured logging (JSON to stdout) is what makes all of the above work on Cloud Run and GKE. A plain-text line is a single string field and every filter on it is a substring match.

## Works in the Console, Fails in Code

| Difference | Detail |
|---|---|
| Different principal | The console is your user; the code is a service account or ADC. Compare identities from both sides |
| Different project | The console remembers a project per tab; the client library reads it from the environment, the credentials file, or a constructor argument |
| Different network position | The console calls the public API from Google's frontend; your code may be inside a perimeter, behind a restricted VIP, or in a subnet without Private Google Access |
| Different API surface | Console actions sometimes call a different method than the SDK's convenient wrapper, with different required permissions. The audit log shows which method actually ran |
| Quota scope | Rate quota is per project; a busy service can exhaust it while your console click sails through |
| Enabled API | The console enables an API on demand with a prompt. Your code cannot |

## When You Are Truly Stuck

Cut the problem in half with a minimal reproduction from the same network position and the same identity: run the single failing call from a throwaway VM or a one-off Cloud Run job **in the same subnet, as the same service account**. If it works there, the difference is your application's configuration. If it fails there, the difference is IAM, org policy, or the network — and you have halved the search space with one test.

Two GCP-specific accelerators worth reaching for before a long session: **Connectivity Tests** simulates a packet and names the rule that drops it, and **Policy Troubleshooter** names the binding that grants or fails to grant a permission. Between them they answer most "why is this blocked" questions without a single retry.

When a diagnosis took real work — a multi-layer 403, a NAT port exhaustion, a perimeter that blocked one service — write the runbook to `~/Clawic/data/gcp/artifacts/runbook-<symptom>.md` with the symptom in the title, the walk that found it, and every secret replaced by its pointer. Add its `## Boxes` line with the read condition (`the moment <symptom> appears`) in the same turn (`memory-template.md`). The second occurrence of a hard bug should cost minutes.
