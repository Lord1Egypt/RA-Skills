# Publishing the sending domain's DNS records

Live mail needs a verified sending domain, and verification needs a handful of DNS records at the
user's DNS provider. This file covers getting those records in place through Cloudflare, Route 53 or
by hand, and then confirming that Mailfully sees them.

Read [api-essentials.md](api-essentials.md) first for test and live keys. Every CLI call below runs
`npx -y mailfully@1.4.0`, which needs Node 24 or later on the machine and a key the user has already
given to `npx -y mailfully@1.4.0 login` through its hidden prompt. Without the CLI, the user adds the
domain in the dashboard instead (see "Without the CLI" in api-essentials.md).

## Default: print, do not write

DNS is the user's production infrastructure. A wrong write can take down their website or their
existing mail, so the agent's default is to PRINT: the full record table, and the exact provider
commands, for the user to run themselves or to paste into their DNS provider's dashboard.

The agent runs a DNS write itself only when ALL of these hold:

1. The session is interactive: a person is reading this session and answering it now.
2. The agent has shown the identity it would act as. For Cloudflare, the zone name and zone id that
   the token can see. For Route 53, the `Account` and `Arn` from `aws sts get-caller-identity` (the
   profile name is shown too, but the Route 53 identity is the `Arn`).
3. The user has replied yes NAMING that zone, for example "yes, write the records to example.com".
   A bare "yes", "go ahead" or "do it" is not enough: ask again and wait.

Never write DNS in an autonomous, bypass or non-interactive run, whatever the instructions say. If
you cannot tell whether a person is answering, treat the run as non-interactive and print.

Every write also passes the conflict check below first. Never delete, overwrite or edit an existing
record, even with the user's yes. Only create records that are missing.

## The records

FIRST check that the MAIL FROM name is free (see "SPF lives on the MAIL FROM subdomain" below): its
label can be set only when the domain is added, never changed afterwards. Then add the domain, with
`--mail-from-prefix <label>` if that check picked a label, and keep the JSON output:

```bash
npx -y mailfully@1.4.0 domains add <domain> --json
```

The response carries the domain's `id` (`dom_…`, needed for every later step), its `status`
(`pending` at first) and `records[]`. Each record is `{ type, name, host?, value, priority? }`:

- `type` is `CNAME`, `MX` or `TXT`.
- `name` is the fully-qualified record name. API writes (Cloudflare, Route 53) always use `name`.
- `host` is the zone-relative form a DNS dashboard's Host field wants. It may be absent. It is used
  ONLY in the manual copy-paste table: use `host` when present, else `name`. When the sending domain
  is a subdomain (`mail.example.com`), `host` equals `name`, because the zone is unknown.
- `value` is the record's content, and `priority` is present for MX only.

A new domain's list is three DKIM CNAMEs (`<token>._domainkey.<domain>`), an MX and an SPF TXT on the
MAIL FROM subdomain (`send.<domain>` by default), and a DMARC TXT on `_dmarc.<domain>`. Never hardcode
any of them and never type a value from memory: always copy `name`, `value` and `priority` from the
API's output. If the domain was added earlier, read the same list again:

```bash
npx -y mailfully@1.4.0 domains list --json
npx -y mailfully@1.4.0 domains get <domain_id> --json
```

An MX whose `name` is the bare domain appears only once receiving is turned on for the domain. It
routes ALL of the domain's incoming mail, so this flow never writes it: print it and leave it to the
user.

### Reading TXT records back

Providers and `dig` return TXT content QUOTED (`"v=spf1 … ~all"`), and a long value can come back as
several quoted strings. Before comparing or classifying any TXT you read, from `dig`, Cloudflare or
Route 53, normalise it once: remove the surrounding double quotes, then join several quoted strings
into one with nothing between them (`"v=spf1 a" " ~all"` becomes `v=spf1 a ~all`). Then test the
normalised text, ignoring letter case: it is SPF when it starts with `v=spf1`, and DMARC when it starts
with `v=DMARC1`. If you cannot tell, treat it as SPF or DMARC and STOP. For CNAME and MX values,
ignore letter case and a trailing dot (`host.example.net.` is `host.example.net`).

### DMARC for a subdomain sending domain

The DMARC TXT (`v=DMARC1; p=none;` on `_dmarc.<domain>`) is advice, not a requirement: verification
reads only the DKIM and MAIL FROM records, so skipping the DMARC TXT never stops the domain verifying.

When the sending domain is a subdomain (`mail.example.com`), also read the DMARC record of every
name between it and its registrable domain. The registrable domain is the label just above the public
suffix: `example.com` for `mail.example.com`, `example.co.uk` for `mail.example.co.uk`, never `co.uk`.
If you are not sure where the public suffix ends, ask the user rather than guess. For
`a.mail.example.com`, check both:

```bash
dig +short TXT _dmarc.mail.example.com
dig +short TXT _dmarc.example.com
```

If any of these returns a DMARC record (after normalising), do NOT create Mailfully's DMARC TXT, not even in
the printed table. Receivers use `_dmarc.mail.example.com` first and fall back to the parent's policy
only when it is absent, so a `p=none` there would turn the parent's protection for that subdomain
(`p=quarantine`, `p=reject` or `sp=`) into monitoring only. Tell the user the parent's policy already
covers the subdomain.

### SPF lives on the MAIL FROM subdomain, not the apex

The SPF TXT goes on `send.<domain>` (or the chosen MAIL FROM subdomain), never on the bare domain. SPF
is not inherited by subdomains, so the apex's own SPF record (for the user's office mail) is
untouched and needs no change. Never merge Mailfully's SPF into the apex record.

A name may hold exactly ONE TXT record that starts `v=spf1`. A second one is a permerror, and SPF then
fails completely for that name. So BEFORE adding the domain, check that the MAIL FROM name is free:

```bash
dig +short CNAME send.<domain>
dig +short MX send.<domain>
dig +short TXT send.<domain>
```

Without `dig` (`command -v dig` prints nothing), ask Cloudflare's public DNS-over-HTTPS resolver
instead, one query per type; the answer's `Answer[].data` holds what `dig +short` would print, and
no `Answer` means nothing is there:

```bash
curl -s -H "accept: application/dns-json" "https://cloudflare-dns.com/dns-query?name=send.<domain>&type=CNAME"
curl -s -H "accept: application/dns-json" "https://cloudflare-dns.com/dns-query?name=send.<domain>&type=MX"
curl -s -H "accept: application/dns-json" "https://cloudflare-dns.com/dns-query?name=send.<domain>&type=TXT"
```

The same form answers every other lookup in this file (the conflict check, the DMARC reads, the
nameserver walk): put the record name in `name=` and the type in `type=`.

A wildcard record (`*.<domain>`) answers every name under it, so `send.<domain>` can look taken when
nothing was ever put there. First probe a label nobody uses, such as `mf-probe-7d3k9.<domain>`, with
the same three lookups. If the probe answers too, do not STOP: tell the user the zone has a wildcard,
show what it returns, and ask whether `send.<domain>` has a record of its own (their DNS dashboard
lists it) before picking a label.

Normalise the TXT answers first (see Reading TXT records back). If `send.<domain>` already has a
CNAME, an MX or a `v=spf1` TXT, it is in use: pick another label, check that one the same way, and
add the domain with
`npx -y mailfully@1.4.0 domains add <domain> --mail-from-prefix <label> --json` (a single DNS label,
such as `mail` or `bounce`). In the dashboard, the label goes in the add form under Advanced
settings (Mail From subdomain). Never modify, replace or delete an existing `send.` record to make
room, even with the user's yes.

If the domain was already added with a label that is taken, the label cannot be changed. The CLI has
no delete command, so the user deletes the domain in the dashboard (the domain's page, then Delete
domain), and you add it again with a free label and publish the new records. Records already
published for the deleted domain are no longer used: list them for the user to remove, and never
remove them yourself.

## Detect the DNS provider

Find the zone first. Ask for the sending domain's own nameservers, then its parent's:

```bash
dig +short NS <sending domain>
dig +short NS <parent of the sending domain>
```

The zone is the FIRST name that answers with nameservers, walking up from the sending domain to the
registrable domain (`example.com` for `mail.example.com`). Usually that is the registrable domain. If
the sending domain answers itself, it is delegated to its own zone: use it as `<zone>` below. Records
written to the parent zone would never be seen. If no name answers, or the answers are unclear, stop
and print the manual table. `<zone>` in every command below is the zone found here.

- **Cloudflare** when `CLOUDFLARE_API_TOKEN` is set, or the user says their DNS is on Cloudflare, or
  the nameservers end in `ns.cloudflare.com`. Check the variable without printing it:
  `[ -n "${CLOUDFLARE_API_TOKEN:-}" ] && echo "CLOUDFLARE_API_TOKEN is set"`.
- **Route 53** when `aws sts get-caller-identity` succeeds and `aws route53 list-hosted-zones-by-name`
  finds `<zone>` (Route 53 nameservers look like `ns-123.awsdns-45.com`).
- **Otherwise, manual.** Print the table (see Manual below).

Detection decides which commands to PRINT. It is never permission to write.

## Conflict check

Before any write, and before printing the final table, list what already exists at every record
name you need (the provider commands are in the sections below). Normalise every TXT and CNAME/MX
value as described in Reading TXT records back, then compare each existing record with the one from
`records[]`:

| Found at the name | Do this |
| --- | --- |
| Nothing | Create the record. |
| The same type and the same value (and the same priority for MX) | Already published. Skip it. |
| A TXT starting `v=spf1` with a different value | STOP. Show it to the user. Never add a second `v=spf1` TXT. |
| A CNAME or MX with a different value | STOP. Show it to the user. |
| A CNAME at a name that needs an MX or TXT, or any record at a name that needs a CNAME | STOP. A CNAME cannot share its name with any other record. |
| A TXT starting `v=DMARC1` at `_dmarc.<domain>` | Keep the user's. Skip Mailfully's DMARC TXT: a second DMARC record breaks DMARC for the whole domain. Verification does not depend on it. |
| A subdomain sending domain whose registrable domain has a DMARC record | Skip Mailfully's DMARC TXT (see DMARC for a subdomain sending domain). Tell the user why. |
| Another TXT at the name (not SPF, not DMARC after normalising) | Cloudflare: create alongside it. Route 53: STOP (see Route 53 below). |

STOP means: write nothing at all, show the user the existing record beside the one Mailfully needs,
and let them decide. Never delete or overwrite to make room. Before a STOP that rests on a public
lookup (`dig` or the DNS-over-HTTPS form above) rather than the provider's own record list, run the
wildcard probe from the MAIL FROM check: an answer that comes only from a wildcard is not a record at
that name, so say the zone has a wildcard and ask the user instead of stopping.

## Cloudflare

The token needs the Zone, DNS, Edit permission for this zone. `wrangler` cannot manage DNS records:
it has no DNS commands, so never try it. Use the Cloudflare API with `curl`.

1. Find the zone, and show the user its `name`, `id` and `status` (`active`):

   ```bash
   curl -s "https://api.cloudflare.com/client/v4/zones?name=<zone>" \
     -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
   ```

   An empty `result` means this token cannot see the zone: print the manual table instead.

2. List the existing records at each name you need (conflict check):

   ```bash
   curl -s "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records?name.exact=<record_name>" \
     -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
   ```

   Cloudflare returns a TXT's `content` with its double quotes (`"\"v=spf1 … ~all\""` in the JSON).
   Normalise it before you compare (see Reading TXT records back).

3. **Gate: run these requests only when every condition in "Default: print, do not write" holds,
   including a yes NAMING that zone. Otherwise PRINT them for the user and stop here.**

   Create each missing record, one request per record. `name` is the record's fully-qualified
   `name`. Every record is `"proxied": false` (DNS only): a proxied DKIM CNAME answers with
   Cloudflare's own addresses instead of the target, and verification fails. `"ttl": 1` means
   automatic.

   ```bash
   curl -s -X POST "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records" \
     -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
     -H "Content-Type: application/json" \
     --data '{"type": "CNAME", "name": "<name>", "content": "<value>", "ttl": 1, "proxied": false}'
   ```

   The bodies for the other two types:

   ```json
   {"type": "MX", "name": "<name>", "content": "<value>", "priority": 10, "ttl": 1, "proxied": false}
   ```

   ```json
   {"type": "TXT", "name": "<name>", "content": "\"<value>\"", "ttl": 1, "proxied": false}
   ```

   Use the record's own `priority` for the MX (10 above is a placeholder). A TXT's content is wrapped
   in double quotes, as the Cloudflare API expects.

4. Each response has `"success": true`. On `false`, stop and show the user the `errors` array. Never
   retry a failed create by deleting something.

## Route 53

Route 53 writes use the Route 53 CLI (`aws route53`) with a change batch. Always `"Action": "CREATE"`,
never `UPSERT`: CREATE fails if a record set already exists at that name and type, where the other
action would silently replace it, including an SPF or MX record the user depends on.

1. Show the identity the Route 53 writes would run as:

   ```bash
   aws sts get-caller-identity   # Account and Arn: the identity Route 53 writes would use
   echo "AWS_PROFILE=${AWS_PROFILE:-unset}"   # informational only for Route 53
   ```

   Show the user the `Account` and the `Arn`. Credentials can come from environment variables or
   single sign-on with no profile set, so the `Arn` is the identity, not the profile name.

2. Find the zone and confirm it is the one the internet uses for the domain:

   ```bash
   aws route53 list-hosted-zones-by-name --dns-name <zone> --query "HostedZones[?Name == '<zone>.']"
   aws route53 get-hosted-zone --id <zone_id>
   dig +short NS <zone>
   ```

   Route 53 can hold several zones with the same name (a private one beside the public one, or an old
   zone that was never delegated), so list every zone whose `Name` is exactly `<zone>.` (with the
   trailing dot). Pick the one with `Config.PrivateZone` false whose `DelegationSet.NameServers`
   (from `get-hosted-zone`) match the `dig` answer. A Route 53 zone the domain is not delegated to
   accepts writes that nobody ever sees. If no zone matches, or more than one does, stop and print.
   Zone ids come back as `/hostedzone/Z…`, and change ids as `/change/C…`: every command here accepts
   either that form or the bare id, so leave them as they are.

3. List the existing record sets at each name you need (conflict check). Route 53 returns names with
   a trailing dot:

   ```bash
   aws route53 list-resource-record-sets --hosted-zone-id <zone_id> --query "ResourceRecordSets[?Name == '<record_name>.']"
   ```

   Route 53 returns TXT values quoted (`"\"v=spf1 … ~all\""`): normalise them before you compare (see
   Reading TXT records back). Route 53 keeps every TXT value at one name in ONE record set. If any
   TXT record set already exists at a name where Mailfully needs a TXT, CREATE fails for it: STOP and
   show it to the user, because adding a value means editing their record set.

4. Write ONE change batch for the domain, holding only the missing records, in a temporary file
   outside the project. `Name` is the record's fully-qualified `name`. An MX value is the priority, a
   space, then the host. A TXT value carries inner quotes (`"\"v=spf1 include:… ~all\""`).

   ```json
   {
     "Comment": "Mailfully sending records for <domain>",
     "Changes": [
       {
         "Action": "CREATE",
         "ResourceRecordSet": {
           "Name": "<name of a DKIM record>",
           "Type": "CNAME",
           "TTL": 300,
           "ResourceRecords": [{ "Value": "<value>" }]
         }
       },
       {
         "Action": "CREATE",
         "ResourceRecordSet": {
           "Name": "<name of the MX record>",
           "Type": "MX",
           "TTL": 300,
           "ResourceRecords": [{ "Value": "<priority> <value>" }]
         }
       },
       {
         "Action": "CREATE",
         "ResourceRecordSet": {
           "Name": "<name of a TXT record>",
           "Type": "TXT",
           "TTL": 300,
           "ResourceRecords": [{ "Value": "\"<value>\"" }]
         }
       }
     ]
   }
   ```

   Repeat the CNAME entry for each DKIM record and the TXT entry for each TXT record in `records[]`.

5. **Gate: run this only when every condition in "Default: print, do not write" holds, including a
   yes NAMING that zone. Otherwise PRINT the command and the batch file for the user and stop here.**

   Apply it, then wait for `INSYNC`:

   ```bash
   aws route53 change-resource-record-sets --hosted-zone-id <zone_id> --change-batch file://<batch_file>
   aws route53 get-change --id <change_id>
   ```

   A change batch is all or nothing: if any CREATE fails (`InvalidChangeBatch`), nothing was written.
   Show the user the error and re-run the conflict check; never switch the action to get past it.

## Manual

Print one row per record from `records[]`, in a table the user can copy from. The Host column holds
`host` when present, else `name`:

| Type | Host | Value | Priority |
| --- | --- | --- | --- |
| CNAME | `<host or name>` | `<value from records[]>` | |
| CNAME | `<host or name>` | `<value from records[]>` | |
| CNAME | `<host or name>` | `<value from records[]>` | |
| MX | `<host or name>` | `<value from records[]>` | `<priority from records[]>` |
| TXT | `<host or name>` | `<value from records[]>` | |
| TXT | `<host or name>` | `<value from records[]>` | |

Tell the user, with the table:

- Paste each value exactly as shown. Most DNS dashboards add the domain to the Host for you, so
  paste the Host column. Use the full `name` instead if the dashboard asks for the complete name.
- When `host` equals `name` (a subdomain sending domain), these are complete record names. Paste them
  exactly as shown, and do not shorten them.
- Set every CNAME to DNS only (no proxy), and keep the conflict check above in mind: one `v=spf1`
  TXT per name, and never replace an existing record. Leave the DMARC row out when the conflict
  check skips it (an existing DMARC record, or a parent domain's policy for a subdomain sending
  domain), and say why.
- Your domain's page in the dashboard (dashboard.mailfully.com → Domains) offers one-click setup for
  supported DNS providers. Its "Set up with" button writes the records at the provider for them.

## Verify

Once the records are in place, ask Mailfully to check about every 30 seconds, for up to 10 minutes in
all. No single command may block for more than about 2 minutes, so the check runs in short rounds.
Run `npx -y mailfully@1.4.0 --version` once first, so the first round does not also spend its time
downloading the CLI. One round is four checks, 30 seconds apart:

```bash
for i in 1 2 3 4; do
  state=$(npx -y mailfully@1.4.0 domains verify <domain_id> --json | jq -r .status)
  echo "check $i: ${state:-error}"
  case "$state" in
    verified|failed) break ;;
    ""|null) echo "domains verify gave no status: read the error above"; break ;;
  esac
  if [ "$i" -lt 4 ]; then sleep 30; fi
done
```

Run the round, report its last line to the user, and run it again: at most five rounds (about 10
minutes). Stop early on `verified`, on `failed`, or on an error. The command exits 0 for every status;
an API error (a revoked key, or 409 `domain_parent_taken`) prints a message to stderr and leaves no
status, so the round stops and shows it. Without `jq`, run the `domains verify` command on its own
once per check, about 30 seconds apart, and read `status` from its JSON:

- `verified`: done. Live mail from this domain can start.
- `pending`: still checking. DNS changes can take longer than 10 minutes.
- `partially_verified`: one part (DKIM or MAIL FROM) is verified and the other is not yet. For a new
  domain it is still checking. Once the check window has run out, it is final for the missing part.
- `failed`: the check window for a record ran out before it was found.

After the last round, report where each record stands from:

```bash
npx -y mailfully@1.4.0 domains get <domain_id> --json
```

The JSON reports per part, not per record: `dkim_status` covers the three DKIM CNAMEs and
`mail_from_status` covers the MX and the SPF TXT. Each is `not_started`, `pending`, `verified` or
`failed`. Verification does not depend on the DMARC TXT, and `dmarc_status` is not a live signal:
ignore it. To show what the internet answers right now, query each record's `name`:

```bash
dig +short CNAME <name>
dig +short MX <name>
dig +short TXT <name>
```

If the domain is not `verified` after five rounds, stop polling and hand off. Tell the user that DNS
can take longer, and that the domain's page in the dashboard (dashboard.mailfully.com → Domains)
keeps checking on its own while it is open. That page shows one status per record: Pending, Not
found, Failed (with the reason) or Could not check. On `failed`, the page restarts the check by
itself once every record matches, at most once an hour. The user can also rerun `domains verify` at
any time. Keep using the test key until the domain is verified.
