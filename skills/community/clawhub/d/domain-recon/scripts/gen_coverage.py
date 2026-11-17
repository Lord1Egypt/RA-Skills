#!/usr/bin/env python3
"""Regenerate docs/tld-rdap-coverage.md — the per-TLD RDAP coverage map.

Maintenance / research tool (NOT part of the passive runtime): it makes a couple
of live requests to authoritative IANA endpoints to classify every delegated TLD
by which RDAP source covers it. Stdlib-only, like recon.py.

    python3 scripts/gen_coverage.py [--out docs/tld-rdap-coverage.md]

Classification per TLD:
  * bootstrap  — present in IANA's RDAP bootstrap (data.iana.org/rdap/dns.json)
  * supplement — absent from the bootstrap but covered by recon._RDAP_SUPPLEMENT
  * none       — no public RDAP server found -> recon `rdap` degrades gracefully

Only `rdap` is TLD-variable; dns/certs/ip/asn/wayback are TLD-agnostic (documented
once in the output, not re-checked per TLD).
"""
import argparse
import json
import os
import sys
import urllib.request
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recon  # noqa: E402  (local import after sys.path tweak)

TLD_LIST_URL = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
BOOTSTRAP_URL = recon._RDAP_BOOTSTRAP_URL
UA = "domain-recon-coverage/1.0 (+https://github.com/maggiedev-bot/domain-recon)"

# Registry display names for supplement rows.
REG = {
    "io": "Identity Digital", "sh": "Identity Digital", "ac": "Identity Digital",
    "us": "GoDaddy Registry (nic.us)", "de": "DENIC", "ch": "SWITCH",
    "af": "nic.af", "aw": "nic.aw", "ci": "nic.ci", "ga": "nic.ga", "kn": "nic.kn",
    "kz": "nic.kz", "mr": "nic.mr", "mz": "nic.mz", "sb": "nic.sb", "so": "nic.so",
    "td": "nic.td", "tl": "nic.tl",
}

# Notes for notable `none` TLDs, from the 2026-07-27 live investigation. These are
# observations, not hardcoded behaviour: the code always falls through to a live
# check and reports "unsupported" only when the TLD is truly absent everywhere.
NONE_NOTE = {
    "eu": "EURid; no public RDAP reachable from probe — WHOIS-only for our purposes",
    "ru": "TCI RDAP host exists but 404'd a known-registered domain — unverified, not added",
    "su": "same operator as .ru — unverified",
    "jp": "JPRS RDAP is gTLD-only; .jp is WHOIS-only",
    "co": "registry-level RDAP not exposed (per-registrar only)",
    "es": "Red.es — WHOIS-only",
    "it": "Registro.it exposes only a *pubtest* RDAP endpoint; no verified production server",
    "dk": "Punktum dk — WHOIS/web only",
    "arpa": "infrastructure TLD (reverse DNS); domain-RDAP N/A — use RIR RDAP for in-addr/ip6",
    "edu": "EDUCAUSE — WHOIS-only",
    "mil": "US DoD — not publicly queryable",
}


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def load_tlds():
    version = ""
    tlds = []
    for line in _get(TLD_LIST_URL).splitlines():
        s = line.strip()
        if s.startswith("#"):
            if "Version" in s:
                version = s.lstrip("# ").strip()
            continue
        if s:
            tlds.append(s.lower())
    return version, tlds


def classify(tld, boot, supp):
    if tld in boot:
        return "bootstrap", "IANA RDAP bootstrap"
    if tld in supp:
        return "supplement", "{} — {}".format(supp[tld], REG.get(tld, "verified live"))
    if tld in NONE_NOTE:
        return "none", NONE_NOTE[tld]
    if tld.startswith("xn--"):
        return "none", "IDN ccTLD — no public RDAP in bootstrap/supplement"
    if len(tld) == 2:
        return "none", "ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only)"
    return "none", "no public RDAP in bootstrap/supplement"


def build(version, tlds, boot, supp, generated):
    rows = [(t,) + classify(t, boot, supp) for t in tlds]
    tally = Counter(r[1] for r in rows)
    nb, ns, nn = tally["bootstrap"], tally["supplement"], tally["none"]
    active_supp = sorted(t for t in supp if t not in boot)

    o = []
    w = o.append
    w("# domain-recon — per-TLD RDAP coverage map\n")
    w("_Generated {} from authoritative IANA data. Regenerate with `python3 scripts/gen_coverage.py`._\n".format(generated))
    w("- **TLD source:** `{}` — IANA `tlds-alpha-by-domain.txt` ({} delegated TLDs)".format(version, len(tlds)))
    w("- **RDAP bootstrap:** IANA `data.iana.org/rdap/dns.json`")
    w("- **Supplement:** `_RDAP_SUPPLEMENT` in `scripts/recon.py` — each entry verified live "
      "(HTTP 200 + real RDAP data, plus a clean 404 for a bogus name in the same TLD)\n")
    w("## Why only RDAP is mapped per-TLD\n")
    w("`rdap` is the **only** TLD-variable query. Every other subcommand is TLD-agnostic and works "
      "for any registrable name / IP / ASN, so it is **not** re-checked per TLD:\n")
    w("| subcommand | source | TLD-dependent? |")
    w("|---|---|---|")
    w("| `dns`     | DNS-over-HTTPS (Google / Cloudflare) | no — universal |")
    w("| `certs`   | crt.sh → certSpotter CT fallback     | no — universal |")
    w("| `ip`      | ip-api.com                           | no — operates on IPs |")
    w("| `asn`     | RIPEstat                             | no — operates on IPs / ASNs |")
    w("| `wayback` | archive.org                          | no — universal |")
    w("| `rdap`    | IANA bootstrap → supplement → rdap.org | **yes** — see table below |\n")
    w("## Summary\n")
    w("| rdap_source | TLDs | meaning |")
    w("|---|---:|---|")
    w("| `bootstrap`  | {} | authoritative RDAP server published in IANA's bootstrap; resolved automatically |".format(nb))
    w("| `supplement` | {} | registry runs a public RDAP server IANA omits; added to `_RDAP_SUPPLEMENT` (verified live) |".format(ns))
    w("| `none`       | {} | no public RDAP server → `rdap` returns a first-class `unsupported` result (graceful degradation) |".format(nn))
    w("| **total**    | **{}** | |\n".format(len(tlds)))
    w("For a `none` TLD, `recon.py rdap <domain>` returns "
      "`{\"supported\": false, \"rdap_source\": \"none\", \"reason\": \"...\"}` at **exit 0**, so a calling "
      "agent skips the field instead of treating a 404 as a tool failure. `dns` / `certs` / `ip` / `asn` / "
      "`wayback` still work for domains in these TLDs.\n")
    w("## Supplement entries ({} — verified live {})\n".format(ns, generated))
    w("| TLD | rdap server | registry |")
    w("|---|---|---|")
    for t in active_supp:
        w("| `.{}` | `{}` | {} |".format(t, supp[t], REG.get(t, "—")))
    w("")
    w("## Full coverage table ({} TLDs)\n".format(len(tlds)))
    w("| TLD | rdap_source | notes |")
    w("|---|---|---|")
    for t, src, note in rows:
        w("| `.{}` | {} | {} |".format(t, src, note))
    w("")
    return "\n".join(o), (nb, ns, nn)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), os.pardir, "docs", "tld-rdap-coverage.md"))
    ap.add_argument("--date", default="", help="stamp for the 'Generated' line (default: today, UTC)")
    args = ap.parse_args(argv)

    version, tlds = load_tlds()
    boot = recon.parse_rdap_bootstrap(json.loads(_get(BOOTSTRAP_URL)))
    supp = recon._RDAP_SUPPLEMENT
    generated = args.date or __import__("datetime").datetime.utcnow().strftime("%Y-%m-%d")

    text, (nb, ns, nn) = build(version, tlds, boot, supp, generated)
    out = os.path.abspath(args.out)
    with open(out, "w") as f:
        f.write(text)
    print("wrote {}".format(out))
    print("bootstrap={} supplement={} none={} total={}".format(nb, ns, nn, len(tlds)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
