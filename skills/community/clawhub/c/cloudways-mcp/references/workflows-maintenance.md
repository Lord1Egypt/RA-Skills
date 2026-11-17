# Workflows — Maintenance (write operations)

Maintenance scenarios requiring write operations. **Every operation here requires explicit confirmation from the user before execution**, per the pattern in `SKILL.md`.

> **Basic rule:** Read before Write. Always read the current state before you change it. Both to verify the operation is needed, and so you have a baseline to roll back to.

---

## Standard confirmation pattern

Before **every** call to a W tool, display a block like this to the user and wait for an explicit "yes":

```
🔒 Confirm execution?
   tool: <tool_name>
   target: <server name + ID or app name + URL>
   parameters: <key params>
   expected impact: <what happens>
   risks: <what could go wrong>
   Continue? (yes / no / pause)
```

If the user wrote "yes" — execute. If anything else — ask for clarification.

For especially dangerous operations (W!): add a **second step**: "Type the server/application name to confirm". This ensures they are reading and not approving automatically.

---

> **Confirming a target: the narrowest fetch that gives you name + URL, and often no fetch at
> all.** Every sequence below starts by making sure the right application is in hand, and the
> confirmation block above requires its name + URL — **an id alone is never a confirmation**: a
> mistyped id that happens to belong to another application is still a valid id, so a write
> confirmed against nothing but a number can land on the wrong site (`app_restore` is the one
> that cannot be undone). Resolve in this order, and stop at the first rung you can use:
>
> 1. **The roster you already hold** from this conversation — zero calls. This is the usual case.
> 2. **You know the server and the app id, hold no roster** — read the name + URL **outside the
>    conversation** (the application's page in the Cloudways UI, or a direct API call through a
>    field filter): zero secrets in the transcript. If it has to be the API from here, **one
>    `app_get` for that one app** is the narrowest call there is — it returns that app's
>    database credentials, and nothing else's. Do **not** reach for `app_list` to confirm one
>    known id: rule 7 describes its payload, and it covers **every** application on the server,
>    so it exposes strictly more than the `app_get` it would be standing in for.
> 3. **You know the server and only a name or URL.** If it is the application's **primary**
>    domain (or its label), `app_list` on that server is the one API route — a single call;
>    take the one row you came for and paste none of it — or the same external filtered roster
>    as rung 2. If it is a **secondary** domain — an alias — `app_list` cannot resolve it: the
>    payload carries the primary `domain` only, and aliases have no read tool at all (see
>    `workflows-onboarding.md`, the domains note). An alias lookup through `app_list` would pay
>    the roster's cost and find nothing. Resolve an alias in the UI (the application's Domain
>    Management page) or through a filtered direct API call, which gives you the primary — and
>    only then, if you still need the id, is there something for `app_list` to match.
> 4. **You do not know the server** — stop and ask which server, or for the name/URL. There is
>    no lookup from an app id to its server: `app_list` and `app_get` both take a `server_id`,
>    and the only API route from a bare id is reading every server's roster, which is the sweep
>    this skill refuses.
>
> What `app_get` is never for is **habit**: reaching for it as the opening step of every job,
> for a label a held roster already gives you, was the finding this section exists to close.
>
> **Certificate state is read from the outside, and the verdict and the dates are two different
> commands.** The verdict is `env -u CURL_CA_BUNDLE -u SSL_CERT_FILE -u SSL_CERT_DIR curl -q --cacert "$HOME/.config/cloudways-mcp/cacert.pem" -sS -o /dev/null --max-time 15 --noproxy '*' https://<domain>/`: exit **0** means the chain, the hostname and the validity
> period all passed the OS trust store — what a browser checks — and exit **60** means one of
> them did not. Two guards on that command are not optional. `-q`, which must come **first**,
> stops curl reading `~/.curlrc`: a machine whose curlrc says `insecure` would otherwise pass
> an expired, self-signed or wrong-host certificate with exit 0 — measured against
> `expired.badssl.com` with such a file, exit 0 without `-q`, exit 60 with it. And the
> `env -u CURL_CA_BUNDLE -u SSL_CERT_FILE -u SSL_CERT_DIR` prefix clears curl's environment
> equivalents of `--cacert`/`--capath`, which `-q` does not touch: measured against
> `self-signed.badssl.com` with `CURL_CA_BUNDLE` pointed at its own certificate, exit 0 — the
> gate passes a certificate no browser trusts — and exit 60 again under `env -u`. And the
> third guard is the `--cacert` pointing at a **pinned copy of Mozilla's public roots**, because
> the system trust store is not the public one: a corporate or user-installed CA sits in it
> exactly where `env -u` cannot reach, and an origin certificate signed only by that CA exits 0
> on this machine while every ordinary visitor rejects it. The verdict has to come from the
> roots browsers ship with. One-time setup, beside `headers.txt` — and the digest it is checked
> against is **this one, recorded here**, not one fetched beside the file:
>
> ```
> sha256  f66dff1bdf8f96060b8177976f8b7d9254bc89bc4db933d769f7384d28480bc9
>         Mozilla certificate data as of Thu Aug 13 03:12:01 2026 GMT, 188 900 bytes
> ```
>
> ```bash
> umask 077; mkdir -p ~/.config/cloudways-mcp && cd ~/.config/cloudways-mcp
> curl -q -sS -o cacert.pem.new https://curl.se/ca/cacert-2026-08-13.pem
> [ "$(shasum -a 256 cacert.pem.new | cut -d' ' -f1)" = f66dff1bdf8f96060b8177976f8b7d9254bc89bc4db933d769f7384d28480bc9 ] && mv -f cacert.pem.new cacert.pem && echo OK || { echo 'digest MISMATCH against the value recorded in the skill - not installed'; rm -f cacert.pem.new; }
> ```
>
> The URL is the **dated** artifact, not `cacert.pem`: curl.se serves every Mozilla revision at
> `cacert-YYYY-MM-DD.pem` and moves the undated name to the newest, so an undated fetch would
> stop matching the recorded digest the day Mozilla revises — every new setup failing, for no
> reason anyone changed. And the download lands in a temporary name and is moved into place
> only after it verifies, so a mismatch leaves a working installation's existing bundle exactly
> where it was. Bumping is one commit that changes the date in the URL and the digest beside
> it, together.
>
> Why the digest lives here and not in `cacert.pem.sha256` next to the download: that file
> comes from the same origin over the same trust path as the bundle, so whatever can replace
> one can replace the other in the same breath — a TLS-inspecting proxy or a compromised
> system CA, which is exactly the situation this bundle exists to defend against. A same-origin
> checksum proves a transfer was not corrupted and nothing more. A digest recorded here moves
> the trust from the download path to the commit that recorded it (the same arrangement as
> `mcp-remote`'s tarball digest in `installation.md`): bumping the bundle means recording the
> new digest in the same commit. On a machine whose network or trust store you do not trust at
> all, obtain the bundle through an independent channel — a machine you do trust, or your OS
> vendor's `ca-certificates` package — and compare against the recorded digest there. Measured
> on this curl build: with that bundle a good host exits 0 and `self-signed.badssl.com` exits 60;
> with an **empty** bundle the good host exits 77 — proof that the file, not the OS store, is
> what the verdict trusts. Mozilla revises the bundle a few times a year; a newer one is
> adopted by updating this record, never by fetching the undated name.
>
> **And there may be two certificates.** Through public DNS that command validates whatever
> answers for the name — behind Cloudflare or any reverse proxy, that is the **edge**
> certificate, not the one installed on the Cloudways application. The **origin** is checked
> by pinning the name to the server's IP (from the `server_list` row you already hold, the
> server's page in the UI, or one `server_get` for that server — never a fresh `server_list`
> to read one address):
> `env -u CURL_CA_BUNDLE -u SSL_CERT_FILE -u SSL_CERT_DIR curl -q --cacert "$HOME/.config/cloudways-mcp/cacert.pem" -sS -o /dev/null --max-time 15 --noproxy '*' --resolve <domain>:443:<server-ip> https://<domain>/` — `--resolve` keeps the hostname for SNI and verification and only changes where the
> connection goes. `--noproxy '*'` is part of the command: with `HTTPS_PROXY` / `https_proxy` /
> `ALL_PROXY` set in the environment, curl hands the request to that proxy, which resolves
> `<domain>` through its own DNS and reaches the CDN edge — so the "origin" check would be
> validating the edge certificate after all (measured: with a proxy variable set, the
> `--resolve` form connects to the proxy address, not the server, until `--noproxy '*'` is
> added). **Whether something is in front is a DNS question, not a certificate one**:
> `R4=$(dig @1.1.1.1 +noall +comments +answer <domain> A) && R6=$(dig @1.1.1.1 +noall +comments +answer <domain> AAAA) && printf '%s\n%s\n' "$R4" "$R6" | grep -c 'status: NOERROR' | grep -qx 2 && A=$(printf '%s\n%s\n' "$R4" "$R6" | awk '$4=="A"||$4=="AAAA"{print $5}') && [ -n "$A" ] && printf '%s\n' "$A" || { echo 'DNS gate FAILED: lookup error, non-NOERROR rcode, or no address' >&2; false; }` against the server's addresses (same source as the IP above) — **every** routable answer, both
> record types, must be the server. `@1.1.1.1` (or any public resolver) is not decoration: on
> a VPN or an office network with **split-horizon DNS**, the local resolver can answer with the
> Cloudways origin while the public one answers with a Flexible-mode CDN — every check then
> exercises the origin, "no proxy" is concluded, and the redirect loops for every visitor
> outside that network. The gate has to believe what a visitor's resolver says. The same
> applies to the redirect-chain checks, which cannot pin hops to other hostnames: on a network
> whose resolver disagrees with the public one, run them from **outside** it, or with
> `--resolve <hostname>:443:<answer>` for **each** public answer in turn. Each, not one: a
> request with no pin exercises **one** address — curl races the answers and keeps the first
> connection to succeed (measured: three plain requests to a dual-stack hostname all connected
> to the same IPv6 address; its IPv4 answer was never touched) — so a hostname with an A and
> an AAAA record is two checks, and a family whose edge serves an expired certificate hides
> behind the family that works. An IPv6 answer goes into `--resolve` as it is (measured:
> accepted with and without brackets).
> The `awk`s keep only addresses: for a CNAME — an ordinary
> `www` alias — `dig +short` prints the canonical name on its own line before the address
> (`github.com.` then `20.217.135.5`, measured), and comparing that line against a server IP
> would call every alias a proxy. `awk` rather than `grep` because a name with no AAAA record
> is normal, and `grep` with nothing to select exits 1 — under `set -e`, or a runner that
> surfaces non-zero commands, that would fail the check on a perfectly valid setup; `awk`
> prints the same lines and exits 0 with nothing to print (measured on an IPv4-only name).
> Which is why the guard around it exists: an empty **family** is fine, an empty **answer** is
> not. With the public resolver blocked, filtered or erroring, `dig` exits 9 but the pipeline
> prints nothing and exits 0 (measured), and "every answer matches the origin" is then true of
> no answers — the proxy-mode check would be skipped on the very networks where it matters.
> Each `dig` is therefore checked on **its own exit status** before anything is filtered — a
> failed lookup for one family, hidden behind the other family's good answer, would otherwise
> pass an aggregate check while being the very family that resolves publicly to a proxy
> (measured: A good, AAAA against an unreachable resolver — an aggregate non-empty guard passed,
> the per-lookup guard failed). And the exit status is not enough either: `dig +short` prints
> nothing and exits **0** on a `SERVFAIL` (measured against `dnssec-failed.org` at 1.1.1.1), so
> a family whose lookup the resolver *refused* looked exactly like a family with no records.
> Each family's **RCODE** is therefore read from `+comments` and must be `NOERROR` — only then
> is an empty family a real no-data answer — and the addresses are taken from the answer
> section by record type. Three cases, stated: `NOERROR` with no records for either family
> passes; anything other than `NOERROR` for either family fails (a `SERVFAIL`, and an
> `NXDOMAIN` — a hostname the app supposedly serves that does not resolve is not a served
> hostname); and no addresses at all fails. No output, and no successful pair of lookups, is
> an unanswered gate — which is a failed gate, never a passed one. Any other address is a CDN or proxy, whatever certificate
> it shows; and a proxy reachable only over IPv6 (an A record at the origin, an AAAA at the
> edge) is still a proxy for every IPv6 client, so an A-only check is not a check. Comparing
> issuers proves nothing,
> because the edge and the origin can both hold Let's Encrypt certificates and still be two
> different machines with a Flexible-mode HTTP hop between them. And the origin check is for a
> site visitors reach **directly**: behind a proxy in Full or Full (strict) mode the origin may
> hold a certificate only the proxy trusts (Cloudflare Origin CA is the ordinary case), the
> local trust store calls it invalid, and the certificate that has to pass is the edge's — for
> the visitors who reach the edge. Proxying is a property of each DNS **answer**, not of the
> hostname: an origin A record beside a proxied AAAA record means IPv4 visitors get the origin's
> certificate and IPv6 visitors get the edge's, and both have to pass — see §9 step 1 for the
> branching. Let's Encrypt renewals happen
> at the origin, so a renewal is verified there; and enforcing HTTPS at the origin behind a
> proxy in **Flexible** mode (proxy speaks HTTPS to the browser, HTTP to the origin) makes the
> origin redirect every proxied request back to HTTPS — a loop. Both checks are measured below
> where they matter. The dates for a report come from `openssl s_client -servername <domain> -connect <domain>:443 </dev/null 2>/dev/null | openssl x509 -noout -issuer -dates`, and that line is **informational
> only**: measured against `expired.badssl.com`, `self-signed.badssl.com` and
> `wrong.host.badssl.com`, it prints issuer and dates and exits 0 for all three, while `curl`
> exits 60 for each. Nothing below decides anything on the openssl line.

## 1. Cache clear — basic

**When:** "The site isn't updating after a change" / "Admin screen shows an old version"

**Sequence:**

1. Confirm the target — name + URL, from the first rung of the ladder at the top you can use (held roster → external lookup or one `app_get` for a known id → `app_list` for a name → ask); an id alone is not a confirmation
2. `app_varnish_settings_get` — see if Varnish is active
3. **CONFIRM:** `app_purge_cache` (W)
4. If Varnish is active: **CONFIRM:** `varnish_app_manage` with action=purge (W)
5. Check the site in a browser (curl or manually)

**If the problem persists:**
- Check plugin caches (W3 Total Cache, WP Rocket, LiteSpeed) — these are not in Cloudways, they must be cleared from WP-Admin
- Check Cloudflare cache if in use — `purge everything` in the Cloudflare UI
- CDN caches

---

## 2. SSL — Let's Encrypt renewal

**When:** SSL is approaching expiry and there is no auto-renewal / auto-renewal failed

> **Covered by the MCP as of v1.2** via the security toolset: `security_lets_encrypt_install` (W), `security_lets_encrypt_renew` (W), `security_lets_encrypt_auto_renewal` (W), `security_lets_encrypt_revoke` (W!). For wildcard certs: `security_create_dns` + `security_verify_dns` handle the DNS-01 challenge.

**Sequence:**

1. Domain from the roster you hold, server IP from the `server_list` row you hold (or the UI, or
   one `server_get` for that server — see the note at the top). The certificate being renewed
   lives on the **origin**, so check that one: `env -u CURL_CA_BUNDLE -u SSL_CERT_FILE -u SSL_CERT_DIR curl -q --cacert "$HOME/.config/cloudways-mcp/cacert.pem" -sS -o /dev/null --max-time 15 --noproxy '*' --resolve <domain>:443:<server-ip> https://<domain>/` for the verdict (exit 0 / 60), and
   `openssl s_client -servername <domain> -connect <server-ip>:443 </dev/null 2>/dev/null | openssl x509 -noout -issuer -dates`
   for the issuer and `notAfter` on record. If `R4=$(dig @1.1.1.1 +noall +comments +answer <domain> A) && R6=$(dig @1.1.1.1 +noall +comments +answer <domain> AAAA) && printf '%s\n%s\n' "$R4" "$R6" | grep -c 'status: NOERROR' | grep -qx 2 && A=$(printf '%s\n%s\n' "$R4" "$R6" | awk '$4=="A"||$4=="AAAA"{print $5}') && [ -n "$A" ] && printf '%s\n' "$A" || { echo 'DNS gate FAILED: lookup error, non-NOERROR rcode, or no address' >&2; false; }` answers with anything that is not one
   of the server's own addresses, a proxy is in front — the renewal still happens here, at the origin, and
   the browser will keep showing you the proxy's certificate afterwards.
   Nothing in this step needs the database credentials `app_get` would add.
2. Check that the DNS still points to the server (critical for LE validation)
3. **CONFIRM:** `security_lets_encrypt_renew` (W) — or `security_lets_encrypt_install` (W) if no cert was issued yet. For a wildcard domain: **CONFIRM** `security_create_dns` (W), publish the returned TXT record at the DNS host, then **CONFIRM** `security_verify_dns` (W).
4. **CONFIRM:** `security_lets_encrypt_auto_renewal` (W) — turn auto-renewal on if it wasn't active.
5. Verify at the origin — the `--resolve` form of the check must exit **0** now, and the
   openssl line against `<server-ip>:443` should show the new `notAfter` — then load the site
   in a browser (which, behind a proxy, shows you the edge certificate, not this one). A re-read of `app_get` would confirm
   nothing the verified handshake does not, at the price of a second credential payload.

**If renewal fails:**
- Most common problem: DNS doesn't point correctly, or wildcard domains aren't configured
- Second: Let's Encrypt rate limit (5 attempts per week per domain)
- Third: HTTP-01 validation fails because the site is behind a Cloudflare proxy → resolve with DNS-01 or disable the proxy temporarily

---

## 3. SSL — installing a custom cert

**When:** The client purchased a cert from another CA (DigiCert, Sectigo, etc.), not Let's Encrypt

> **Barely covered by the MCP** (live-verified 2026-07-20): the only custom-SSL tool is `security_remove_own_ssl` (W!), which *removes* an installed cert. There is **no install tool and no CSR tool** — the article's `security_csr_create` / `security_csr_get` do not exist on the live server, and the `security` toolset description claiming a custom-cert install is wrong. Generate the CSR on the CA's side (or via `openssl`), then paste cert + key in the **Cloudways Platform UI** (Application → SSL Certificate → Custom SSL) or use the [direct API](https://developers.cloudways.com/).

**Sequence:**

1. Collect from the client: certificate, private key, ca bundle. If the CA still needs a CSR, generate it outside Cloudways (the MCP exposes no CSR tool) — and **name the key explicitly**, because the cert is only installable with the exact key that signed the CSR:

   ```bash
   # Signing with the key you already have:
   openssl req -new -key privkey.pem -out request.csr

   # Or generating a new key + CSR together (-nodes leaves the key
   # unencrypted, which the Cloudways UI requires):
   openssl req -new -newkey rsa:2048 -nodes -keyout privkey.pem -out request.csr
   ```

   Keep `privkey.pem` — a bare `openssl req -new` writes an encrypted key to whatever path the local OpenSSL config picks, and losing it makes the issued certificate unusable.
2. Confirm the target — name + URL, by the ladder at the top (held roster first; an id alone is not a confirmation)
3. **Install the custom cert in the Cloudways UI** (paste cert + key) — manual by necessity; no MCP tool covers this step.
4. Check SSL from the browser (SSL Labs grade A+ preferred)
5. If Let's Encrypt was active — decide: keep as backup or revoke (`security_lets_encrypt_revoke`, W! — double-confirm)

> Warning: Installing a custom cert **cancels** the Let's Encrypt cert if one was active. Make sure you have the custom cert in hand **before** you start.

---

## 4. Backup before a change

**When:** Before a migration, restore, significant plugin update, or any "I'm not sure what this will do"

**Sequence:**

1. Confirm the target — name + URL, by the ladder at the top (held roster first; an id alone is not a confirmation)
2. `monitoring_app_summary` — before: snapshot of state
3. **CONFIRM:** `app_backup` (W)
4. Check that the backup is progressing (`app_backup_status_get` for in-progress state, or via the UI). Note: there is no general "list backups" tool — the available restore points are visible in the Cloudways UI.
5. Record the backup timestamp — you'll need it for restore if something goes wrong

**Server-level backup:**
- `server_backup` (W) — slower, includes everything, more expensive
- Useful before a server-wide change (PHP upgrade, OS upgrade, package change)

---

## 5. Restore after an error

**When:** Something went wrong (bad deployment, hack, accidental delete)

**Sequence — critical to follow in order:**

1. **STOP** — don't do anything until you understand the scope of the problem.
2. The app's identity — name + URL — by the ladder at the top (a bare id is not an identity,
   and step 5 below has to be checked against something), then `monitoring_app_summary` for
   what it is doing right now — the current state a restore decision needs
3. Check the list of available backups (via the Cloudways UI — there is no MCP "list backups" tool; `app_backup_status_get` only reports in-progress backup status)
4. **CONFIRM step 1:** "Is the backup from date X the point you want to roll back to?"
5. **CONFIRM step 2:** Type the app name to confirm restore
6. **CONFIRM:** `app_restore` (W!) — full overwrite of the current state
7. Check that the site works
8. If the restore itself made things worse: **CONFIRM (W!):** `app_restore_rollback` — returns the app to its pre-restore files + database. This is available only within the limited rollback window (see below); after that, fall back to restoring an earlier backup or the Cloudways UI.

> **Limited rollback window.** `app_restore_rollback` only works for a short time after the restore (a few hours / a day) — after that the pre-restore local snapshot is gone and rollback is no longer possible. Make sure the site works **on the same day** as the restore. (Note: `app_local_backup_delete` deletes that pre-restore snapshot immediately, which also forecloses the rollback.)

---

## 6. Restart server / service

**When:** memory leak, services stuck, or troubleshooting

**Priority order — try the quietest one first:**

1. `app_purge_cache` (W) per app — sometimes that's all it takes
2. `service_restart` (W) on a single service (e.g. restart MySQL only)
3. If that doesn't help: `server_restart` (W) — 1-5 minutes downtime for all the apps

**Before server_restart:**

1. **Mandatory:** `app_list` → the applications about to go offline (`server_get` returns the same roster plus the server's master credentials; the roster is all this preflight needs)
2. **Mandatory:** count active users (if relevant — a store site with open carts?)
3. **Double CONFIRM:** "The server hosts X applications — Y, Z, W. Each of them will be offline for X minutes. Continue?"
4. Execute
5. **VERIFY:** `service_status` after the restart

---

## 7. IP whitelist — SSH/MySQL

**When:** Adding a key for a team member, or removing access for an old IP

> **Covered by the MCP as of v1.2** via the security toolset: `security_get_whitelisted_ips` (R, SSH/SFTP), `security_get_whitelisted_ips_mysql` (R), and `security_update_whitelisted_ips` (W! — **replaces** the whole list, not an append). Web-SSH / Adminer access: `security_whitelist_ip_siab` / `security_whitelist_ip_adminer` (W).

**Sequence:**

1. `security_get_whitelisted_ips` (or `_mysql`) — read what's there **now**
2. Plan the new list — **including your own IP** (the update **replaces** the list; anything you omit is removed)
3. **CONFIRM:** Show the user: "The new list is: [...]. Does your IP X.X.X.X stay on the list? yes/no"
4. If the user is missing from the list — **stop and clarify**
5. **Double CONFIRM (W!):** `security_update_whitelisted_ips` with the complete new list
6. **VERIFY:** re-read the list, then try SSH immediately (if it doesn't work — Cloudways support to restore)

> **Nightmare scenario to avoid:** updating the whitelist + removing your own IP + no alternative SSH. The only way out — the Cloudways UI (panic) or a support ticket (time). Be careful.

---

## 8. Disk cleanup

**When:** disk usage > 80%

**Priority order:**

1. `server_disk_usage_fetch` (init) then `monitoring_server_summary` (read) — where's the space?
2. **CONFIRM:** `app_purge_cache` (W) for all the suspect apps
3. If not enough: **CONFIRM:** `server_disk_cleanup_*` (W) — Cloudways magic cleanup
4. If not enough: upgrade size (UI only) or manual SSH to clean logs
5. **VERIFY:** `server_disk_usage_fetch` + `monitoring_server_summary` again

> `server_disk_cleanup_*` may delete logs. If the client must keep logs (compliance, debugging), export them manually first.

---

## 9. Enforce HTTPS

**When:** An old site still running on HTTP / client wants an SEO/security boost

**Sequence:**

0. **List every hostname the application serves, because the write covers all of them.**
   `app_enforce_https_update` turns on the redirect for the application, not for one domain —
   and steps 1 and 2 below are per **hostname**. The primary domain is in the roster you hold;
   the aliases are not: `app_list` carries the primary `domain` only, and the alias tools
   (`app_cname_update`, `app_aliases_update`) are writes with no read counterpart. Read them
   from the application's Domain Management page in the Cloudways UI, or a filtered direct API
   call. Then run steps 1 and 2 **once per hostname**. An alias with no matching origin
   certificate, or one behind a Flexible-mode proxy while the primary is not, passes nothing
   and breaks — certificate errors, or the loop — the moment the redirect goes on. The write in
   step 4 waits until every hostname has passed both.
1. **Is anything in front, and does the certificate visitors will meet pass?** The handshake
   only — what the application answers *after* it is step 2's job — and both must pass, **for
   every hostname from step 0** (`<hostname>` below is each of them in turn), before step 4.
   The DNS gate comes **first**, because it decides which certificate matters:
   `R4=$(dig @1.1.1.1 +noall +comments +answer <hostname> A) && R6=$(dig @1.1.1.1 +noall +comments +answer <hostname> AAAA) && printf '%s\n%s\n' "$R4" "$R6" | grep -c 'status: NOERROR' | grep -qx 2 && A=$(printf '%s\n%s\n' "$R4" "$R6" | awk '$4=="A"||$4=="AAAA"{print $5}') && [ -n "$A" ] && printf '%s\n' "$A" || { echo 'DNS gate FAILED: lookup error, non-NOERROR rcode, or no address' >&2; false; }`
   — compare **every** answer, A and AAAA both, against the server's own addresses (from the
   `server_list` row you hold), and classify **per answer**, not per hostname: an answer that
   is the server means clients on that family reach the origin directly; an answer that is
   anything else means clients on that family go through a CDN or reverse proxy, regardless of
   what certificate it presents and even if its issuer matches the origin's. A hostname whose
   A record is the origin and whose AAAA record is a proxy is **both**, and both branches
   below apply to it — every IPv4 client reaches the origin, every IPv6 client reaches the
   edge, and each path has to be right on its own.
   - **Any answer is the server — some or all visitors reach the origin directly.** Then the
     origin's certificate is one that browsers will be handed, and it must pass the pinned
     public roots: `env -u CURL_CA_BUNDLE -u SSL_CERT_FILE -u SSL_CERT_DIR curl -q --cacert "$HOME/.config/cloudways-mcp/cacert.pem" -sS -o /dev/null --max-time 15 --noproxy '*' --resolve <hostname>:443:<server-ip> https://<hostname>/` must exit
     **0** — chain + hostname + dates, at the Cloudways server itself. Exit 60 means there is
     no certificate browsers accept here **yet**, and which of two things that is decides where
     you go: if none was ever issued (a fresh app answers with Cloudways' self-signed default),
     go to step 3 and **install one**, then come back and re-run; if one is installed and
     failing (expired, wrong host), fix or reissue it first (sections 2 and 3) and re-run. What
     exit 60 never permits is step 4 — enforcing HTTPS now would redirect production traffic
     onto a certificate browsers reject.
   - **Any answer is not the server — some or all visitors go through a proxy.** Its origin
     mode has to be **Full (strict)**, or at least Full,
     confirmed in that proxy's own settings before this write; in Flexible mode the proxy
     reaches the origin over HTTP, the origin's new redirect sends it back to HTTPS, and the
     site loops. The origin's certificate is then judged by **the proxy's origin policy, not by
     this machine's trust store**: in Full it may be anything the proxy accepts, an
     origin-CA certificate included; in Full (strict) it must be publicly trusted **or** issued
     by that proxy's own origin CA — a Cloudflare Origin CA certificate is the normal, correct
     case here, and the origin command above would call it invalid (exit 60) while the proxy
     trusts it and visitors on that path never see it. Do not run the origin check against a
     site whose **every** answer is a proxy and read exit 60 as "replace the certificate" —
     but if the hostname also has a direct answer (the mixed case above), that allowance is
     gone: the origin certificate *is* handed to the direct family's browsers, and the direct
     branch's browser-trust check applies to it as well. The certificate visitors **will** be handed
     is the edge's, so that is what must pass the trust store — at **every** answer, pinned one
     at a time, since a request with no pin tests one address only (curl keeps the first
     connection to succeed; measured, three plain requests to a dual-stack hostname all landed
     on the same IPv6 address and never touched the IPv4 answer, so an edge family with an
     expired certificate hides behind a healthy one). With `$A` from this hostname's gate:
     `printf '%s\n' "$A" | while read -r ip; do env -u CURL_CA_BUNDLE -u SSL_CERT_FILE -u SSL_CERT_DIR curl -q --cacert "$HOME/.config/cloudways-mcp/cacert.pem" -sS -o /dev/null --max-time 15 --noproxy '*' --resolve "<hostname>:443:$ip" -w "$ip %{http_code}\n" https://<hostname>/ || echo "$ip FAILED (curl exit $?)"; done`
     — every line must carry a status that is **not 5xx** and no line may say `FAILED`
     (a failed handshake prints `<ip> 000` and then `<ip> FAILED (curl exit 60)`, measured).
     An answer that is the server gets the direct branch's check again here, same command,
     same verdict. 525/526 is the edge admitting it cannot complete TLS to the origin, which is the origin-policy failure the paragraph above is about, arriving as an HTTP status.
   Do not read any of this off `openssl x509 -dates`, which prints dates for a broken
   certificate just as happily.
2. **The HTTPS answer must not send anyone back to HTTP — at any hop.** Step 1 validated the
   handshake and nothing after it: a valid certificate in front of an application that answers
   `https://` with `301 Location: http://…` still exits 0, and so does one whose first hop is a
   harmless `https://www.` canonical redirect while the **second** hop goes back to `http://`.
   So follow the whole chain, the way a browser will, **before** the write — and refuse
   **any** hop to HTTP, not just an HTTP ending, because `%{url_effective}` reports only the
   final URL and a chain that dips to `http://` and climbs back to `https://` would otherwise
   pass:
   `printf '%s\n' "$A" | while read -r ip; do env -u CURL_CA_BUNDLE -u SSL_CERT_FILE -u SSL_CERT_DIR curl -q --cacert "$HOME/.config/cloudways-mcp/cacert.pem" -sS -o /dev/null --max-time 15 --noproxy '*' --resolve "<hostname>:443:$ip" -L --max-redirs 5 --proto-redir '=https' -w "$ip %{http_code} %{url_effective} %{num_redirects}\n" https://<hostname>/ || echo "$ip FAILED (curl exit $?)"; done`
   — one run per public answer (`$A` from this hostname's gate in step 1), for the reason
   step 1 gives: a request with no pin follows the chain at **one** address, and the
   application behind the other family may answer differently.
   (Quote `'=https'` — in zsh, macOS's default shell, a bare `=https` is expanded as a
   command lookup and the line fails with `https not found`. `--noproxy '*'` is here for the
   same reason as on the origin check: with `HTTPS_PROXY` set, an intercepting proxy's block
   or login page would pass this check — any status, small hop count — without the
   application's redirects ever being seen. It stops curl using a configured proxy and nothing
   else: DNS still resolves publicly, so the check still reaches the site's CDN as a visitor
   would.) Pass is, on **every** line: no `FAILED`, an
   `https://` effective URL, a small hop count — and a terminal status that is **not 5xx**. A
   `401` from Basic Auth on the root, a `403` from a WAF, a `204`/`404` from an API root are
   all fine answers over HTTPS: this check is about the path, not the application's opinion of
   the request. But a **5xx** over HTTPS is a broken HTTPS path, and behind a proxy the
   specific codes matter: Cloudflare's **525** (SSL handshake to the origin failed) and **526**
   (origin certificate invalid) — and the 52x family generally — are the *edge* reporting that
   it could not reach the origin over TLS, behind a perfectly valid edge certificate. `-sS`
   without `--fail` leaves curl's exit code to the transport, so these arrive as `exit 0` with
   the status in the `-w` output (measured: 525, 526 and 502 all exit 0) — read the status.
   Redirecting a working HTTP path onto any of them is the outage this step exists to prevent. `curl: (1) Protocol "http" disabled (in redirect)`
   (measured: exit 1, before curl ever connects to the HTTP target — the line reads
   `<ip> FAILED (curl exit 1)`) or an effective URL
   beginning `http://` means the app itself is pushing HTTPS visitors back to HTTP somewhere
   in its chain; on WordPress that is `WP_HOME` / `WP_SITEURL` still set to `http://`, the
   usual cause on a site that has never had HTTPS enforced. Enforcing now produces the loop
   the audit warned about: the server redirects `http→https`, the app redirects `https→http`,
   and every browser bounces between them until it gives up.
   `curl: (47) Maximum (5) redirects followed` is a **different** failure and must not be sent
   to the same repair: with `--proto-redir '=https'` an HTTP hop is never followed, so `47` can
   only be an **HTTPS-only** loop or a finite chain longer than five hops — `www`/apex
   ping-pong, an authentication redirect that never settles, a plugin's canonical rule
   fighting a server rule. Changing `home`/`siteurl` for that changes the scheme of a site
   whose problem is not the scheme. Diagnose it hop by hop instead — `--max-redirs 0 -w
   '%{http_code} %{redirect_url}\n'` on the start URL, then on the URL it named, and so on
   until the pair that bounces is in front of you — and fix that rule where it lives. Either
   way, step 4 waits until this step passes.
   **For the downgrade case, fix the application first**, then re-run this step until it
   passes — and that repair is a write of its own, on the site's database, with its own
   confirmation:
   - Read before writing: `wp option get home; wp option get siteurl`. The hostname in those
     values is the site's canonical host and **stays**; only the scheme changes. Never write
     `https://<hostname>` from this step's placeholder — when `<hostname>` is an alias, that
     would promote the alias to canonical and change every generated URL on the site.
   - Back up first (§4, `app_backup`, confirmed) — a wrong `siteurl` locks `wp-admin` out
     immediately.
   - **CONFIRM:** with the standard block (`tool: wp option update`, `target`: the app and its
     current `home`/`siteurl`, `expected impact`: scheme `http://` → `https://`, hostname
     unchanged), then:
     `wp option update home "$(wp option get home | sed 's#^http://#https://#')" && wp option update siteurl "$(wp option get siteurl | sed 's#^http://#https://#')"`
     (or edit the two constants in `wp-config.php` the same way). This confirmation is for this
     write; step 4 has its own. The pin covers `<hostname>` only, on purpose: a hop to another
   hostname (`www.`) resolves publicly, and that is right — that hostname is in step 0's list
   and gets its own gate and its own per-answer pass; the origin itself was already checked in
   step 1.
3. If there's no SSL: install one first — `security_lets_encrypt_install` (W, see sections 2 and 3). Enforcing HTTPS without a valid cert will break the site.
4. **CONFIRM:** `app_enforce_https_update` (W) — toggles the HTTP→HTTPS redirect (this is separate from installing the cert)
5. Verify the **whole chain** the way a browser walks it, not the first hop — **for every
   hostname from step 0**, since an alias can loop for host-specific CDN or origin reasons
   while the primary passes:
   `printf '%s\n' "$A" | while read -r ip; do env -u CURL_CA_BUNDLE -u SSL_CERT_FILE -u SSL_CERT_DIR curl -q --cacert "$HOME/.config/cloudways-mcp/cacert.pem" -sS -o /dev/null --max-time 15 --noproxy '*' --resolve "<hostname>:80:$ip" --resolve "<hostname>:443:$ip" -L --max-redirs 6 --proto-redir '=https' -w "$ip %{http_code} %{url_effective} %{num_redirects}\n" http://<hostname>/ || echo "$ip FAILED (curl exit $?)"; done`
   — per public answer, `$A` from this hostname's gate (re-run the gate line if the shell has
   moved on), and **both** ports pinned: `--resolve` is per host:port, so pinning `:443` alone
   leaves the `http://` hop — the one this write changed — free to land on whichever address
   curl reaches first (measured). The limit is **6**, not step 2's 5, on purpose: step 2
   passed a chain of up to five hops starting at `https://`, and this check starts one hop
   earlier — the `http→https` hop the write just added — so a chain that was exactly five
   hops and healthy would be six here, and `--max-redirs 5` would call it a loop (measured:
   a six-hop chain exits 47 at `--max-redirs 5` and 0 at 6). One more than the preflight
   allowed, and no more.
   The start is `http://` on purpose — that is what the new redirect acts on — and
   `--proto-redir` governs only the hops after it, so every one of those must be HTTPS. Expect, on
   **every** line: no `FAILED`, an `https://` effective URL, and a hop count of at least 1 — the
   `http→https` hop you just enabled — or a little more if the app adds a `www` or
   trailing-slash hop. The status may be whatever the application answers (`200`, a `401` behind
   Basic Auth, a `403` from a WAF) — but **not 5xx**: a 525/526 here means the proxy cannot
   reach the origin over TLS and every visitor is now redirected onto that failure; treat it
   exactly like the loop below.
   `curl: (47) Maximum (6) redirects followed` **is the loop** — the chain step 2 passed plus
   the one hop this write adds fits inside six, so exceeding it means the chain no longer
   settles, or grew by more than that hop — and `curl: (1) Protocol "http"
   disabled (in redirect)` is a downgrade somewhere past the first hop. Either way the fix is
   to take the server redirect back off and return to step 2 — and that is a **second
   production write**: **CONFIRM:** `app_enforce_https_update` (W) with the standard block, the
   `target` and `expected impact` now describing the rollback. The confirmation given in step 4
   authorised enabling the redirect; safety rule 2 does not let it carry to disabling it, and a
   transient failure that looks like a loop must not roll production back to HTTP on nobody's
   say-so. Per answer on purpose: each visitor takes one address, proxy included, and each address
   has to redirect correctly on its own. The application is healthy when every answer of every
   hostname from step 0 has passed this step, not when one has.

> **WordPress, after:** with `home`/`siteurl` already on `https://` (step 2), what can remain is
> mixed content from hard-coded `http://` URLs inside posts and options — a search-replace job
> (`wp search-replace 'http://<domain>' 'https://<domain>' --dry-run` first), not a Cloudways
> setting.

---

## 10. Git pull deployment

**When:** Deploying a branch to an application

**Sequence:**

1. `git_branches_get` — verify the branch exists
2. `git_history_get` — what the current state is
3. **CONFIRM:** `app_backup` (W) — always backup before a deploy
4. **CONFIRM:** `git_pull` (W) with branch + commit hash if relevant
5. **VERIFY:** Check the site
6. If something broke: `app_restore` (W!) to the backup from section 3

> Cloudways Git deploy doesn't run build steps. If the site requires `npm run build` / `composer install` — you'll need to do that manually over SSH after the pull, or keep build artifacts in the repo.

---

## 11. Varnish — configure/purge

**When:** Setting a cache strategy / performance tuning

**Sequence:**

1. `app_varnish_settings_get` — current config
2. Understand the policy: cache TTL, exceptions, purge rules
3. **CONFIRM:** `varnish_app_manage` (W) with a specific action (enable/disable/purge/configure). For changing Varnish settings, `app_varnish_settings_update` (W) is also available.
4. If purge: check that the cache is clean (`curl -I` to the URL → should be `X-Cache: MISS` on the first request)

> Varnish isn't compatible with every application. For WooCommerce or applications with session-heavy data, precise exclusion rules are needed. Always check after a change.

---

## Cleanup after a session

Before ending a conversation that included write operations:

1. Summarize what was done
2. Mention if backups were created and when they expire
3. Mention if there are operations that still require later verification (SSL renewal, cache propagation)
4. If something wasn't finished — document what remains open
