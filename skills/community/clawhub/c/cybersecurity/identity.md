# Identity — Authentication, Sessions, Privilege

Identity is the perimeter, and almost every intrusion is an identity event wearing a host's clothes. This file holds the complete eviction list SKILL.md Rule 5 points at, plus the hardening that removes the paths.

**Before any identity change or investigation**, read `## Environment` in `~/Clawic/data/cybersecurity/memory.md` (the identity provider, the account population, which log tier exists) and `## Findings` for the identity findings somebody already raised — MFA gaps get re-discovered every quarter and re-argued every time. `platform.idp` in `config.yaml` names the provider whose console terms apply below.

**Contents:** [The Complete Eviction List](#the-complete-eviction-list) · [Why A Password Reset Is Not Containment](#why-a-password-reset-is-not-containment) · [Factor Strength, Honestly Ranked](#factor-strength-honestly-ranked) · [The Paths Around MFA](#the-paths-around-mfa) · [Conditional Access That Holds](#conditional-access-that-holds) · [Privilege: Standing Access Is The Finding](#privilege-standing-access-is-the-finding) · [Service Accounts And Non-Human Identity](#service-accounts-and-non-human-identity) · [Joiners, Movers, Leavers](#joiners-movers-leavers) · [The Help Desk Is An Authentication Path](#the-help-deREDACTED-SECRET) · [Identity Signals Worth Alerting On](#identity-signals-worth-alerting-on) · [Access Review That Is Not Rubber-Stamping](#access-review-that-is-not-rubber-stamping)

## The Complete Eviction List

When an account is compromised, all of it, in this order. Anything skipped is the reason the actor returns without a new phish.

1. **Revoke refresh tokens and sign out every session** — before the password reset, not after. Reset-first leaves a window in which the live session re-establishes itself.
2. **Reset the password**, and set it, do not mail a reset link to a mailbox the attacker reads.
3. **Access tokens already issued keep working until they expire** — commonly up to an hour. Where continuous access evaluation exists, enable it: it is what turns revocation from "eventually" into near-real-time. Where it does not, state the window out loud, because it is the window in which containment is not yet true.
4. **Review and remove registered authentication methods** — attacker-added phone numbers, authenticator apps and security keys. An attacker-enrolled factor makes the account look *more* secure than before, which is why this step gets skipped.
5. **Revoke OAuth grants and consented applications** for that user, and check tenant-wide consent for new applications and service principals. This is token persistence that survives every password reset ever performed.
6. **Remove device registrations and enrolments** created in the window. A registered device can hold a long-lived primary refresh token that no session revocation touches.
7. **Rotate application passwords and legacy-protocol credentials**, which exist precisely because they bypass MFA.
8. **Rotate API keys, personal access tokens and SSH keys** owned by that identity, in every system: the git host, the cloud provider, the CI platform, the ticketing system.
9. **Delete mail rules, forwarding, delegates and "send as"** created in the window (`phishing.md` has the full mailbox sweep).
10. **Check group memberships and role assignments** granted during the window, including nested groups and eligible-but-not-active roles.
11. **Check for new accounts** created by the compromised identity — the second door built while you were closing the first.
12. **Where the identity is privileged in a directory**: assume ticket-forging capability and follow the eradication gate in `incident-response.md`, including the krbtgt double rotation. Nothing else in this list matters if the attacker can mint their own tickets.

## Why A Password Reset Is Not Containment

Each row below survives a reset on its own, and each has ended an incident that somebody had declared closed:

| Survivor | Why |
|---|---|
| Live browser session cookie | Authentication already happened; the cookie is the credential now |
| Refresh token | Mints new access tokens indefinitely until explicitly revoked |
| Primary refresh token on a registered device | Device-bound, long-lived, invisible to a session sign-out |
| OAuth consent grant | The app authenticates as itself with a delegated scope; the user's password is irrelevant |
| App password / legacy protocol credential | Created specifically to bypass modern authentication |
| API key, PAT, SSH key | Separate credential store entirely |
| Attacker-registered MFA method | Lets them complete the *next* login legitimately |
| Mail forwarding rule | Keeps exfiltrating with no authentication at all |
| Enrolled device | Trust anchor that re-issues tokens |

## Factor Strength, Honestly Ranked

| Factor | Stops credential phishing | Stops AiTM proxy | Stops push fatigue | Note |
|---|---|---|---|---|
| Password only | No | No | — | The baseline everything else is measured against |
| SMS or voice OTP | No | No | n/a | Also exposed to SIM swap and carrier compromise; NIST has discouraged SMS as a factor for years |
| TOTP app | No | No | n/a | The code is phishable in real time; better than SMS only in that it removes the carrier |
| Push approval | No | No | No | The MFA-fatigue target |
| Push with number matching | No | Partially | Yes | Removes blind approval, still relays through a proxy |
| Certificate / smart card | Yes | Yes | n/a | Strong, with real PKI operating cost |
| FIDO2 / WebAuthn security key | Yes | Yes | Yes | Origin-bound: the credential simply does not work on the attacker's domain |
| Passkey, device-bound | Yes | Yes | Yes | Same guarantee; check whether the implementation syncs across a consumer cloud, which changes the threat model |

The line that matters is **origin binding**, not the number of factors. Everything above it is phishable in real time; everything below it is not, because the browser will not release the credential to the wrong origin.

## The Paths Around MFA

Enforcing MFA is not having MFA. Each of these leaves the path open:

- **Legacy authentication protocols** — IMAP, POP, SMTP AUTH, and older mail-sync protocols — that never present a challenge. One legacy endpoint left on for one old client defeats the entire tenant policy, and password spray finds it within days.
- **Users enrolled in a weaker factor** who can still choose it. Registered-but-unused SMS is an available path.
- **Break-glass accounts excluded from policy** and then forgotten. They need MFA too, plus an alert on any use.
- **Service accounts excluded** because "they cannot do MFA" — correct, which is why they need conditional access by IP or workload identity federation instead of an exemption.
- **The help-desk reset path** (below), which is authentication by social engineering.
- **Guest and external accounts** in a tenant that enforces MFA only for members.
- **Registration itself**: if anyone can register a factor from anywhere, an attacker with the password registers theirs first. Gate registration on a compliant device or a trusted location.
- **Recovery codes** in a shared drive, a password manager the attacker also owns, or a ticket.

The audit that finds all of them: list every successful authentication in the last 30 days where no MFA challenge was recorded, and explain each one. That query, run once a quarter, is worth more than any policy document.

## Conditional Access That Holds

- Baseline: block legacy authentication, require MFA for everyone, require compliant or hybrid-joined devices for administrative roles, and block or challenge sign-ins from countries the org never operates in.
- **Every exclusion is a hole with a name.** Keep the exclusion list short, dated and reviewed; an untracked exclusion is the actual policy.
- Require phishing-resistant factors for administrative roles first — that is where the cost/benefit is unambiguous — then expand.
- Sign-in frequency and session controls matter for high-privilege sessions: a 90-day session on an admin account means containment is 90 days late.
- Test policies in report-only mode before enforcement, and always have a break-glass path validated *before* the policy goes live. Locking the whole organization out of its own identity provider is an outage with no admin available to fix it.

## Privilege: Standing Access Is The Finding

- **Standing privilege is the vulnerability.** Just-in-time elevation with approval and an expiry converts a permanent target into a time-boxed one. Where the platform has no JIT feature, the poor-man's version — a separate admin account that is normally disabled, plus an alert on enable — removes most of the same path.
- **Separate admin identities that never read mail or browse.** One phished mailbox becoming tenant takeover is the most common escalation there is. The control leaks when admins use the same browser profile for both.
- **Tiering**: identity-plane administration (directory, identity provider, PKI, backup) is tier zero and must never be administered from a machine that also handles email and the internet. A privileged access workstation is the full version; at minimum, a separate browser profile and a separate account is the version everyone can do today.
- **Unique local administrator passwords per machine**, rotated automatically. Shared local admin is the single mechanism that turns one workstation into all of them.
- **Watch the paths, not the role list.** Attack-path tooling against a directory finds the chains — a service account with unexpected delegation, a group nested three levels into an admin group, an ACL that lets a helpdesk group reset a domain admin's password. Those chains are what an operator uses; a flat list of role members never shows them.
- **Group nesting is where privilege hides.** Review effective membership, never direct membership.

## Service Accounts And Non-Human Identity

Non-human identities usually outnumber humans, and they are worse in every dimension: no MFA, no rotation, no offboarding, permissions granted once and never reviewed.

- Inventory them with an owner each. An account with no owner cannot be rotated, because nobody knows what breaks.
- **A service account authenticating interactively, or from a workstation, is a credential-theft signal** — they are not supposed to have hands. Restrict logon types to what the service needs and alert on the rest.
- Prefer workload identity over stored secrets: managed identities, IRSA and equivalents, or OIDC federation from the CI platform. The best rotation policy is having no long-lived secret to rotate.
- Where a secret must exist, it lives in a secrets manager, and this skill records only the pointer: `env:OKTA_API_TOKEN`, `keychain:soc-svc`, `1password:Security/EDR-console`, `ssm:/prod/db/password`.
- Scope by IP or workload identity what you cannot protect with a factor.
- Rotation with no break: create the second credential, migrate consumers, verify use of the new one in logs, then delete the old. The delete step is the one people skip, which means the rotation never happened.

## Joiners, Movers, Leavers

- **Movers are the real problem.** Joiners get the right access and leavers get removed; people who change roles accumulate. Access review has to be role-change-driven, not annual, or a five-year employee ends up with the union of five jobs.
- Offboarding, in this order: disable the account (never delete first — deletion destroys audit linkage and mailbox access you may need), revoke sessions and tokens, remove MFA methods and devices, transfer data ownership, then remove licences and access. Contractor and vendor accounts follow the same path and are the ones that survive for months.
- **The token outlives the account** in more systems than people expect: personal access tokens, API keys and OAuth grants can keep working after the account is disabled. Sweep them explicitly at offboarding.
- An offboarding that nobody verifies is a hypothesis. Sample it quarterly and count the survivors — the number is always non-zero the first time.

## The Help Desk Is An Authentication Path

Every control above is bypassed by a convincing phone call if the reset procedure has no verification step. This path has been the initial access in several widely reported intrusions, and it costs nothing to close.

- **Write the verification procedure down**, because a procedure that lives in each agent's judgement fails under social pressure — which is exactly the condition the attacker creates.
- Verify through a channel the caller does not control: a callback to the number in the directory, confirmation by the person's manager, a video call for a known face, or an in-person check. Never verify with information an attacker can look up — date of birth, employee id, last four digits, manager's name.
- **Never reset MFA and the password in the same interaction** without a second, independent verification. That combination is a full account takeover delivered by your own staff.
- Higher bar for privileged accounts, executives and finance staff: two-person approval, and no exceptions for urgency. Urgency plus seniority plus secrecy is the attack, not a reason to skip the step.
- Log every reset with who requested it, who approved it, and how they were verified. That log is the detection: a spike in resets, or resets for accounts the agent has never handled, is a campaign in progress.
- Give agents an explicit, blameless way to refuse and escalate. Most help-desk failures are pressure failures, not knowledge failures, and the fix is permission to say no.
- New-hire and returning-from-leave enrolment is the same path with a different name: verify identity before issuing the first factor, or the attacker enrols theirs.

## Identity Signals Worth Alerting On

| Signal | Why it matters |
|---|---|
| Successful authentication with no MFA challenge | The path around the policy, in one query |
| New MFA method registered, especially soon after a password reset | Attacker persistence that looks like good hygiene |
| New OAuth consent, or a service principal granted mail or file scopes | Token persistence surviving every reset |
| Sign-in from a hosting or VPN-provider ASN with an unmatched device id | The token-replay and AiTM signature |
| Break-glass account used, at all | It should be zero; any use is either an outage or an intrusion |
| Privileged role activated outside change windows | JIT abuse or a compromised admin |
| Password spray shape: many accounts, few attempts each, one source | Finds the legacy endpoint before the attacker finishes with it |
| Directory sync account authenticating from anywhere unusual | It can read and write the whole directory |

Each of these belongs in `## Detections` with its response action and precision (`detection.md` has the tuning math).

## Access Review That Is Not Rubber-Stamping

The default review — a manager approving a list of 200 entitlements — produces a signature and no security. What works:

- Review by exception: show only what changed since last time, plus everything unused for 90 days. A short list gets read.
- Include the unused-access data next to each entitlement; "not used in 6 months" is what makes a manager click remove.
- Review privileged roles and service accounts on a separate, shorter cycle than ordinary access — quarterly for privileged, annually for the rest is a defensible split.
- Every review has a completion date recorded, because "we do access reviews" without a date is what an auditor writes an exception against.

Write what the work produced (`memory-template.md`): identity provider, account population, MFA coverage, privileged role inventory and the exclusion list in `## Environment`; every gap — legacy auth enabled, standing admin, an unowned service account, a stale exclusion — as a `## Findings` row with owner, due date and the attack path it removes; the new identity detections in `## Detections`; access review, key rotation and break-glass test cadences as `## Due` rows; the tiering model or the JIT procedure, once derived, in `~/Clawic/data/cybersecurity/artifacts/` with its `## Boxes` line in the same turn. People who own identity decisions — the IdP admin, the help-desk lead — go to `~/Clawic/data/contacts/contacts.md`. Credentials never: the pointer only, in `<kind>:<locator>` form.
