# Security — Authentication, Authorization, and Query Injection

Elasticsearch spent years shipping with no authentication, and the resulting unsecured clusters were one of the largest sources of public data exposure of the era. `elasticsearch >=8.0` enables TLS and authentication by default on a new install; every cluster older than that, or upgraded in place, needs it checked by hand.

## The Non-Negotiables

1. **Never expose the HTTP port to the internet.** Bind `network.host` to a private interface and put the cluster behind an application that authenticates users. `_search` is a query language with expensive operators and, without `allow_expensive_queries: false`, an easy denial of service.
2. **Never let a browser talk to Elasticsearch directly.** Any credential in browser code is public, and an authenticated user is authorized against *indices*, not against rows the application intended them to see.
3. **TLS on both channels.** `xpack.security.http.ssl` for clients, `xpack.security.transport.ssl` for inter-node traffic. Without transport TLS, any host that can reach the transport port can join the cluster and read everything.
4. **Change every default and bootstrap password**, and remove the elastic superuser from application configuration entirely.

## Users, Roles, and API Keys

```json
POST /_security/api_key
{ "name": "search-frontend", "expiration": "90d",
  "role_descriptors": { "reader": {
      "indices": [ { "names": ["products-*"], "privileges": ["read"] } ] } } }
```

- Prefer API keys over usernames and passwords for applications: independently revocable, scoped at creation, expiring, and they cannot log into Kibana.
- The key's effective permissions are the **intersection** of the creating user's privileges and the `role_descriptors`. A key created by a superuser without descriptors is a superuser key.
- Role privileges are hierarchical: cluster-level (`monitor`, `manage_index_templates`) and index-level (`read`, `write`, `create_index`, `view_index_metadata`). Grant `read` and `write`, not `all`, and never `manage` to an application.
- Index patterns in roles accept wildcards; a role scoped to `logs-*` also covers indices a future team creates under that prefix. Scope tightly and revisit.
- Realms compose in order: native, file, LDAP, Active Directory, SAML, OIDC, PKI, Kerberos. The file realm is the one that survives a broken external directory — keep one break-glass account there.

## Document- and Field-Level Security

```json
"indices": [ { "names": ["orders"], "privileges": ["read"],
               "query": { "term": { "tenant_id": "acme" } },
               "field_security": { "grant": ["*"], "except": ["credit_card"] } } ]
```

- DLS applies a filter to every search that role performs; FLS hides fields from `_source` and from search. Both are licensed features (`license_tier`).
- DLS costs query performance and interacts badly with some aggregations and with `terms` lookups. Test the actual query shapes, not just access.
- The open-tier equivalent is a **filtered alias**, which is weaker — a user with access to the underlying index bypasses it — but it removes the "application forgot the filter" class of bug, which is the common one.
- FLS does not hide a field's existence from `_field_caps` or from a mapping read, so it is confidentiality of values, not of schema.

## Query Injection

The concrete risk is not "SQL injection for Elasticsearch"; it is a user controlling the *shape* of the query.

| Pattern | Risk | Do instead |
|---|---|---|
| User input concatenated into `query_string` | `*:*` widens the result set; `field:value` reaches fields the UI never exposed; malformed syntax throws a 400 | `simple_query_string` (never throws, ignores bad syntax) or a plain `match` |
| Client sends a full query DSL body | The user picks the query, including scripts and huge aggregations | The server builds the body; the client sends parameters only |
| A tenant filter added in application code | One refactor removes it and nothing fails | Filtered alias, or DLS |
| User-supplied `size`, `from`, or aggregation `size` | Trivial resource exhaustion | Clamp server-side; `terminate_after` and `track_total_hits: false` as backstops |
| User-supplied regex or wildcard | Catastrophic expansion over the term dictionary | `search.allow_expensive_queries: false`, and an input length limit |

Even with `simple_query_string`, cap input length and reject control characters. And set `search.allow_expensive_queries: false` cluster-wide on any cluster serving user-facing traffic: it blocks `script`, `regexp`, leading-wildcard, `fuzzy`, and joining queries outright.

## Scripting Surface

- Painless is sandboxed: no I/O, no reflection, no arbitrary classes. Treat that as defence in depth, not permission to accept scripts from users.
- `script.allowed_types: inline|stored|none` and `script.allowed_contexts` restrict where scripts may run at all. Setting `allowed_types: stored` means only scripts an operator installed can execute, which removes user-supplied scripts as a category.
- Stored scripts live in cluster state and are managed like code: reviewed, versioned, deployed. Inline scripts from application code are the middle ground; inline scripts assembled from user input are not acceptable at any tier.

## Data Handling

- `_source` returns everything indexed. Anything sensitive that the application never displays should not be in the document — filtering it at read time is a policy, not a control.
- Personal data plus ILM means deletion has to be planned: a `_delete_by_query` leaves tombstones until merges run, and the value survives in snapshots until they expire. Time-based indices with a delete phase are the only clean deletion story.
- Encryption at rest is a disk-level concern; Elasticsearch does not encrypt segments itself. Snapshots inherit the repository's encryption, so the bucket's configuration is part of your posture.
- Audit logging (licensed) records authentication and authorization events. Without it, "who read this index" has no answer at all.

## Operational Hygiene

- Rotate API keys on a schedule; set `expiration` at creation so an unrotated key fails loudly rather than living forever.
- `GET /_security/_query_api_key` inventories keys with their owners and expiry. Run it quarterly and revoke what nobody claims.
- Restrict `manage_security` to a small set of humans; anyone with it can mint a superuser key.
- Keep one file-realm break-glass account, documented, with its password in the same vault as everything else, and test it during the restore drill.
- New index patterns inherit nothing: a role scoped to `logs-*` does not cover `metrics-*`, and the failure appears as an authorization error from a batch job at 3am. Add the pattern when you add the data stream, not after.

## Security Gates

- Is the HTTP port unreachable from the public internet, verified from outside?
- Is transport TLS on, with certificates that are not the auto-generated dev ones on a production cluster?
- Does every application authenticate with a scoped, expiring API key rather than the elastic user?
- Is user input reaching `query_string` anywhere, or building a query body client-side?
- Is `search.allow_expensive_queries` false on user-facing clusters?
- Is tenant isolation enforced by a filtered alias or DLS rather than by application code alone?
- Do snapshots and their repository fall under the same access controls as the cluster?
