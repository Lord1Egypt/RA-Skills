# Manage doxx.net Domains

> **Live schema first.** The doxx.net Config API is agent-descriptive. Fetch `https://config.doxx.net/` for the current manifest (every endpoint, params, returns, auth, side effects): this file is a snapshot. Every POST response also includes a `context` field with per-endpoint docs.

You help users register domains, manage DNS records, sign TLS certificates, and import external domains on doxx.net.


## API convention

**Auth token -- never enters the AI conversation.**

The token is passed to `curl` via shell expansion, so its plaintext value stays on your machine. Two sources, checked in this order:

1. `$DOXXNET_TOKEN` env var (preferred): user exports it before launching the agent.
2. `~/.config/doxxnet/token` file: used automatically if the env var is unset.

curl commands below use `${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}`, so both work transparently. The shell expands the value at exec time -- the plaintext is never emitted in a tool call to the LLM.

**Config API**: POST to `https://config.doxx.net/v1/`:
```
curl -s -X POST https://config.doxx.net/v1/ -d "ENDPOINT=1&param=value&token=${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}"
```

## Endpoints

- `list_tlds`: list all 196 available TLDs with categories (no auth)
- `list_domains`: list registered domains
- `create_domain`: register a domain. Params: `domain`
- `delete_domain`: delete a domain. Params: `domain`
- `list_dns`: list DNS records. Params: `domain`
- `create_dns_record`: create a record. Params: `domain`, `name` (FQDN), `type` (A/AAAA/CNAME/MX/TXT/NS/SRV/PTR), `content`. Optional: `ttl`, `prio`
- `update_dns_record`: update a record. Params: `domain`, `old_name`, `old_type`, `old_content`, `name`, `content`. Optional: `ttl`
- `delete_dns_record`: delete a record. Params: `domain`, `name`, `type`, `content`
- `get_domain_validation`: get TXT verification code for importing external domains. Params: `domain`
- `import_domain`: import external domain after TXT verification. Params: `domain`, `validation_code`
- `link_profile_domain`: link a saved profile to a domain; creates A/AAAA records that auto-update with the profile's IPs. Params: `domain`, `hostname` (subdomain label), `profile_id`. Returns: full FQDN created
- `unlink_profile_domain`: remove DNS records linking a profile to a domain. Params: `profile_id`
- `sign_certificate`: sign a CSR (returns raw PEM, not JSON). Params: `domain`, `csr`
- `list_tunnels`: list tunnels (to get IPs for DNS records)

## TLD categories

Use `list_tlds` to get the full live list. Popular choices for private networking: `.lan`, `.vpn`, `.mesh`, `.home`, `.wg`, `.wireguard`, `.local`, `.internal`

Other: crypto (.btc, .eth, .crypto), tech (.api, .dns, .json, .git), hacking (.cyber, .onion, .tor, .pwnd)

Default TLD is `.doxx` if none specified.

## TLS certificates

To sign a certificate, generate a key and CSR first with openssl, then call `sign_certificate`:
1. `openssl ecparam -genkey -name prime256v1 -out DOMAIN.key`
2. `openssl req -new -key DOMAIN.key -out DOMAIN.csr -subj "/CN=DOMAIN"`
3. `curl -s -X POST https://config.doxx.net/v1/ --data-urlencode "csr@DOMAIN.csr" -d "sign_certificate=1&domain=DOMAIN&token=${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}"`

Remind users: clients need the doxx.net root CA installed to trust these certs.

## Importing external domains

1. Call `get_domain_validation` to get a TXT verification code
2. Tell user to create TXT record `_doxx-verify.DOMAIN` at their current DNS provider
3. Call `import_domain`
4. Tell user to update nameservers to: `a.root-dx.net`, `a.root-dx.com`, `a.root-dx.org`

## Guidelines

- Always list existing domains/records before making changes
- When creating A records for tunnels, get tunnel IPs from `list_tunnels` first
- Verify DNS after changes with `dig @a.root-dx.net`
- For TLS certs, the private key stays local: never send it anywhere
