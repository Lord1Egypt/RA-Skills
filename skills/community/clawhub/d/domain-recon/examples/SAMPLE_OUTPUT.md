# Sample output — domain-recon

Real output captured against generic public targets (`example.com`, `8.8.8.8`,
`AS15169`). JSON is the default; `--human` gives the compact form shown here.

## `dns example.com --type A,MX --human`
```
DNS (google) — example.com
  A     104.20.23.154, 172.66.147.243
  MX    0 .
```

## `ip 8.8.8.8 --human`
```
ip-api — 8.8.8.8
  country: United States
  region: Virginia
  city: Ashburn
  isp: Google LLC
  org: Google Public DNS
  as: AS15169 Google LLC
  timezone: America/New_York
  flags: hosting
```

## `asn 8.8.8.8 --human`   (IP → owning ASN + prefix)
```
RIPEstat IP — prefix 8.8.8.0/24
  ASNs: 15169
```

## `asn AS15169 --human`   (ASN → holder + announced prefixes, capped in human mode)
```
RIPEstat ASN 15169 — GOOGLE - Google LLC
  announced: True
  prefixes (1409): 152.65.214.0/23, 142.251.165.0/24, 34.0.234.0/24, ... (+1394 more)
```

## `rdap 8.8.8.8`   (JSON, default)
```json
{
  "endAddress": "8.8.8.255",
  "entities": [{"handle": "GOGL", "roles": ["registrant"]}],
  "events": {
    "last changed": "2023-12-28T17:24:56-05:00",
    "registration": "2023-12-28T17:24:33-05:00"
  },
  "handle": "NET-8-8-8-0-2",
  "ipVersion": "v4",
  "kind": "ip",
  "name": "GOGL",
  "rdap_source": "rdap.org",
  "source": "rdap",
  "startAddress": "8.8.8.0",
  "status": ["active"],
  "type": "DIRECT ALLOCATION"
}
```
> `rdap_source` records which tier answered: `iana-bootstrap`, `supplement`, or
> `rdap.org`. IP/ASN lookups always use `rdap.org`.

## `rdap github.io`   (ccTLD `.io` — resolved via the curated supplement)
```json
{
  "kind": "domain",
  "ldhName": "github.io",
  "nameservers": [
    "dns1.p05.nsone.net", "dns2.p05.nsone.net", "dns3.p05.nsone.net",
    "ns-1622.awsdns-10.co.uk", "ns-692.awsdns-22.net"
  ],
  "rdap_source": "supplement",
  "source": "rdap",
  "target": "github.io"
}
```
> `.io` is **absent from IANA's RDAP bootstrap** and rdap.org `404`s it, so the
> lookup would fail with bootstrap alone. The curated supplement routes `.io` to
> Identity Digital's RDAP server — `rdap_source: "supplement"` shows that path won.

## `certs example.com --human`   (crt.sh down → certSpotter fallback)
Captured live on 2026-07-26 while crt.sh was returning `HTTP 502` on every query:
```
certs — example.com (via certspotter)
  subdomains (3):
    *.example.com
    example.com
    www.example.com
  certificates: 5
  ! crtsh unavailable: HTTP 502 from https://crt.sh/?q=%25.example.com&output=json
```
The JSON form carries the same audit trail:
```json
{
  "source": "ct",
  "sources_used": ["certspotter"],
  "errors": [
    {"source": "crtsh", "error": "HTTP 502 from https://crt.sh/?q=%25.example.com&output=json"}
  ],
  "subdomain_count": 3,
  "subdomains": ["*.example.com", "example.com", "www.example.com"]
}
```
> `certs` tries crt.sh first and falls back to certSpotter on any failure, so a
> crt.sh outage no longer kills subdomain enumeration. `sources_used` shows which
> CT source answered; `errors[]` records what failed. A `200` with no certs is a
> real "no certs logged" answer and does **not** trigger the fallback. Use
> `--all-ct` to query both sources and merge for wider coverage.

## `wayback example.com --cdx-limit 3`   (availability fast-path + CDX history)
```json
{
  "archived": true,
  "snapshot_url": "http://web.archive.org/web/20260726083637/http://example.com/",
  "timestamp": "20260726083637",
  "status": "200",
  "cdx": {
    "first_capture": {
      "timestamp": "20020120142510",
      "original": "http://example.com:80/",
      "statuscode": "200",
      "snapshot_url": "http://web.archive.org/web/20020120142510/http://example.com:80/"
    },
    "last_capture": {
      "timestamp": "20260726083637",
      "original": "http://example.com/",
      "statuscode": "200",
      "snapshot_url": "http://web.archive.org/web/20260726083637/http://example.com/"
    },
    "recent": [ "... up to --cdx-limit most-recent captures ..." ]
  },
  "source": "wayback",
  "url": "example.com"
}
```
> The availability endpoint and the CDX index are independent; when availability
> is momentarily empty the CDX history still surfaces the capture record.

## `profile example.com --human`   (orchestrate every source into one report)
```
profile — example.com
  registration: 1995-08-14T04:00:00Z
  nameservers: elliott.ns.cloudflare.com, hera.ns.cloudflare.com
  dns:
    A     104.20.23.154, 172.66.147.243
    AAAA  2606:4700:10::ac42:93f3, 2606:4700:10::6814:179a
    MX    0 .
    NS    elliott.ns.cloudflare.com., hera.ns.cloudflare.com.
  subdomains: 0
  hosts:
    104.20.23.154 — AS13335 Cloudflare, Inc. [Canada / Toronto]
    172.66.147.243 — AS13335 Cloudflare, Inc. [Canada / Toronto]
  Wayback — example.com
    first capture: 20020120142510
    last capture:  20260726083637
  errors (1):
    certs: HTTP 404 from https://crt.sh/?q=%25.example.com&output=json
```
> Note the `errors` block: crt.sh was momentarily unavailable, but `profile`
> **isolates the failure** — it records the failed step and still returns every
> other source rather than aborting the whole report.
