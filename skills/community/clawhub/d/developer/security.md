# The Security Pass on Your Own Diff

Not a security review of the system — that is `threat-modeling` and a specialist's job. This is the pass a developer runs on their own change, which catches the majority of what actually reaches production: input that is trusted, an authorization check that was never written, and a secret in a place secrets do not belong.

**Before this pass**, read `## Conventions` in `~/Clawic/data/developer/repos/<repo>.md` for how this codebase does validation, authorization and secret loading. Inventing a second pattern is itself the vulnerability, because the next reader will not know which one is authoritative.

## The Seven Questions

Run these against every diff that touches a request path, a query, a file, a template, or a permission:

1. **Where does untrusted input enter this change, and where is it validated?** Untrusted means anything from a user, another service, a webhook, a queue, a file, or a URL parameter. Validate at the boundary, by allow-list, into a typed shape. "It's an internal service" is a trust assumption, not a control.
2. **Is every new data access authorized for *this* user, not just authenticated?** The classic hole: `GET /orders/:id` returns any order to any logged-in caller. Authorization belongs in the same layer as the query, always scoped by the caller's identity — a check in the UI is not a check.
3. **Is any input concatenated into an interpreter?** SQL, shell, HTML, template, LDAP, regex, path. Parameterize; never build a query by string. Where the tool has no parameters — a shell — pass an argument array, never a formatted string.
4. **Can this path be made to fetch, read, or write somewhere unintended?** User-supplied URLs (SSRF), user-supplied paths (`../` traversal), user-supplied filenames on write, redirects to a user-supplied target.
5. **What does this log, and what does it return on error?** Stack traces, SQL, tokens, full request bodies and personal data all leak through logs and error responses. Log the identifier, not the payload.
6. **Does any secret appear in code, config, a test fixture, a log, or a URL?** Including in the commit history: a secret committed and then removed is a rotated secret, not a deleted one.
7. **What is the blast radius if this new code is wrong?** Whose data, how much, and can it be undone (`migrations.md`)?

## Input Validation

| Input | Rule |
|---|---|
| Anything from a client | Allow-list of shape, type, length and range at the boundary; reject rather than sanitize |
| Identifiers from a client | Never trust them to belong to the caller — scope the query by the caller (question 2) |
| Numbers | Bounds, and the sign; unbounded page sizes are a denial-of-service in one parameter |
| Uploads | Type by content, not by extension or client-declared MIME; size cap; store outside the web root; never execute |
| Redirect targets | Allow-list of hosts or relative paths only |
| Rich text or HTML from users | A maintained sanitizer library, on output, with a strict policy — never a regex |
| Data from another internal service | Same rules; internal only means the attacker had to arrive from somewhere else first |

Sanitizing input by removing characters is a losing game: escape or encode **at the point of use** — HTML-escape when rendering, parameterize when querying — because the correct escaping depends on the destination, which the input layer does not know.

## Authentication and Authorization in New Code

- **Deny by default.** A new endpoint or job with no explicit authorization must not be reachable; if the framework requires an opt-in to be public, the mistake becomes a 403 instead of a leak.
- **Check on every request**, server side. A token issued an hour ago says nothing about a permission revoked ten minutes ago for a sensitive action.
- **Object-level checks, not just role checks.** "Is an admin" and "may see this record" are different questions and the second is the one that leaks.
- **Multi-tenancy**: the tenant id comes from the session, never from the request body. Every query in a tenanted system carries it.
- **Never roll your own crypto, tokens, or password hashing.** Use the platform's password hash with its current defaults, the platform's random source for anything security-relevant, and constant-time comparison for secrets.

## Secrets Discipline

- Secrets come from the environment or a manager at runtime — never a literal, never a committed config file, never a default value in code, never a test fixture.
- `.env` files are gitignored and never pasted into a ticket, a chat message, or into anything under `~/Clawic/data/` (`memory-template.md`).
- A secret that reached a repo, a log, a screenshot or a CI output is compromised: rotate it, then clean it up. Rewriting history without rotating is theatre.
- Scan for secrets in a pre-commit hook or in CI — the cheapest control in this file, because it catches the mistake before it is permanent.
- Third-party tokens follow the same rule as your own, and a webhook URL with a token in the path is a secret in a URL.

## Dependencies and Data

- New dependency in this diff → the supply-chain checks in `dependencies.md`, including install scripts and typosquats.
- New personal data stored → know why it is needed, where it will be deleted, and whether it should be in logs at all (it should not).
- New external call → timeout, and a bound on the response you will parse. An unbounded read from a remote host is a memory exhaustion waiting for a bad day.
- New file write → path built from your own values, never from user input, and the permissions set deliberately.

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Validating in the client | Anyone can call the API directly; the client is a convenience, not a control | Validate server side; the client is UX only |
| Blocklisting bad input | The list is always incomplete, and encodings multiply | Allow-list the shape you accept |
| Escaping on input | The right escaping depends on the destination | Escape at the point of use |
| String-built SQL "because it's just an internal id" | Internal ids come from the client more often than anyone remembers | Parameterize, every time |
| Authorization checked in the UI | The endpoint stays open | Check where the data is fetched |
| Logging the request body to debug | Personal data and tokens land in a log that is retained for a year | Log identifiers and outcome |
| Committing a secret and removing it in the next commit | It is in the history and in every clone | Rotate first, then clean |
| "It's behind the VPN" | The VPN is one compromised laptop from being the internet | Authenticate and authorize anyway |
| Copying an auth pattern from another repo without its context | The check that mattered lived somewhere else | Follow this repo's convention; if there is none, that is the finding |

## Write Down What You Found

- **A security decision with a rejected alternative** — how tenancy is enforced, why a token lives where it does → `~/Clawic/data/developer/artifacts/adr-<topic>.md` with its `## Boxes` line (`memory-template.md`).
- **A vulnerability found and fixed** → a row in `## Pain Points` of `memory.md`, describing the class, not the exploit: "authorization missing on new endpoints — check added to the review checklist".
- **A recurring check worth institutionalizing** → `artifacts/review-checklist-<repo>.md` (`reviews.md`).
- **A finding you could not fix now** → `## Open Threads` with the risk in one line, and a ticket in `tracker` if there is one. Never leave it only in the chat.
- **Never** write the vulnerable payload, the token, or the affected customer's data into any file under `~/Clawic/data/`.
