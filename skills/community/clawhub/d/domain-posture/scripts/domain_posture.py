#!/usr/bin/env python3
"""Domain posture audit: passive DNS checks for email auth, transport, DNS
integrity and exposure signals. Read-only; no scanning, no brute force.

Usage: domain_posture.py domain [domain...] [--json] [--no-subdomains]
       [--wordlist PATH]
"""
import argparse
import json
import sys

try:
    import dns.resolver
    import dns.flags
    import dns.rdatatype
    HAVE_DNSPYTHON = True
except ImportError:
    HAVE_DNSPYTHON = False

COMMON_DKIM_SELECTORS = ["google", "selector1", "selector2", "default",
                         "mail", "s1", "s2", "dkim", "k1", "amazonses",
                         "sig1", "zoho", "protonmail", "mandrill"]
SENSITIVE_SUBDOMAINS = ["staging", "dev", "test", "uat", "qa", "vpn",
                        "admin", "adminpanel", "panel", "portal",
                        "gitlab", "jenkins", "ci", "grafana", "kibana",
                        "db", "database", "mysql", "postgres", "mongo",
                        "backup", "backups", "old", "legacy", "api-docs",
                        "swagger", "status", "mail", "webmail", "cpanel"]
DANGLING_MARKERS = ["s3.amazonaws.com", "s3-website", "cloudapp.net",
                    "azurewebsites.net", "blob.core.windows.net",
                    "herokudns.com", "herokuapp.com", "github.io",
                    "fastly", " Akamai".strip().lower()]
KNOWN_MX_PROVIDERS = {"google": ["google.com", "googlemail.com"],
                      "microsoft": ["outlook.com", "protection.outlook.com"],
                      "proton": ["protonmail.ch", "protonmail.com"],
                      "zoho": ["zoho.com"]}


def get_records(domain, rtype):
    if HAVE_DNSPYTHON:
        try:
            ans = dns.resolver.resolve(domain, rtype, lifetime=6)
            return [r.to_text().strip('"').replace('" "',
                     "") if rtype in ("TXT",) else r.to_text() for r in ans]
        except Exception:
            return []
    return []


def txt_flat(domain):
    """Join multi-string TXT records."""
    out = []
    try:
        ans = dns.resolver.resolve(domain, "TXT", lifetime=6)
        for r in ans:
            out.append("".join(s.decode() if isinstance(s, bytes) else s
                               for s in r.strings))
    except Exception:
        pass
    return out


def check_spf(domain, findings, pillar):
    txts = [t for t in txt_flat(domain) if t.startswith("v=spf1")]
    if not txts:
        findings.append(("critical",
                         f"No SPF record on {domain} — anyone can spoof "
                         f"email from this domain"))
        pillar["score"] -= 25
        return
    spf = txts[0]
    issues = []
    if "+all" in spf or " +all" in spf:
        issues.append("SPF has +all (allows everyone) — worse than nothing")
    if "~all" not in spf and "-all" not in spf and "?all" not in spf:
        issues.append("SPF has no all mechanism (~all or -all recommended)")
    lookups = spf.count("include:") + spf.count("redirect=")
    if lookups > 10:
        issues.append(f"SPF exceeds 10 DNS lookups ({lookups}) — permanent "
                      f"SPF failure for receivers")
    for i in issues:
        sev = "critical" if "+all" in i else "warning"
        findings.append((sev, f"SPF: {i}"))
        pillar["score"] -= 15 if sev == "critical" else 8


def check_dmarc(domain, findings, pillar):
    txts = [t for t in txt_flat(f"_dmarc.{domain}")
            if t.startswith("v=DMARC1")]
    if not txts:
        findings.append(("critical",
                         f"No DMARC record (_dmarc.{domain}) — domain is "
                         f"spoofable regardless of SPF"))
        pillar["score"] -= 35
        return
    dmarc = txts[0]
    if "p=none" in dmarc:
        findings.append(("warning",
                         "DMARC p=none — monitoring only, no enforcement. "
                         "Move to p=quarantine then p=reject"))
        pillar["score"] -= 12
    elif "p=quarantine" in dmarc:
        findings.append(("info",
                         "DMARC p=quarantine — consider p=reject"))
    if "rua=" not in dmarc:
        findings.append(("info", "DMARC has no rua (aggregate reports)"))
    if "p=reject" in dmarc and "sp=" not in dmarc:
        findings.append(("info",
                         "No sp= tag — subdomains fall back to p="))


def check_dkim(domain, findings, pillar):
    found = []
    for sel in COMMON_DKIM_SELECTORS:
        recs = txt_flat(f"{sel}._domainkey.{domain}")
        for r in recs:
            if "v=DKIM1" not in r and "p=" not in r:
                continue
            # 'p=' with empty key = neutralizer record, not a signing key
            pval = None
            for part in r.split(";"):
                part = part.strip()
                if part.startswith("p="):
                    pval = part[2:].strip()
            if pval:
                found.append(sel)
                break
    if found:
        findings.append(("info",
                         f"DKIM present (selectors: {', '.join(found)})"))
    else:
        findings.append(("warning",
                         "No DKIM found on common selectors — if this domain "
                         "sends mail, publish a DKIM record"))


def check_mx(domain, findings, pillar):
    try:
        ans = dns.resolver.resolve(domain, "MX", lifetime=6)
        mx = sorted((r.preference, r.exchange.to_text()) for r in ans)
    except Exception:
        findings.append(("info", "No MX — domain does not receive email"))
        return
    providers = set()
    for _, exch in mx:
        host = exch.rstrip(".").lower()
        for prov, markers in KNOWN_MX_PROVIDERS.items():
            if any(m in host for m in markers):
                providers.add(prov)
    findings.append(("info",
                     f"MX: {', '.join(e for _, e in mx)}"
                     + (f" (provider: {', '.join(sorted(providers))})"
                        if providers else " (custom/self-hosted)")))
    for _, exch in mx:
        host = exch.rstrip(".")
        if host != domain and not host.endswith("." + domain):
            continue
        # MX pointing at a hostname that doesn't resolve = dangling
        try:
            dns.resolver.resolve(host, "A", lifetime=4)
        except Exception:
            try:
                dns.resolver.resolve(host, "AAAA", lifetime=4)
            except Exception:
                findings.append(("critical",
                                 f"Dangling MX: {host} has no A/AAAA "
                                 f"record — mail to this domain can be "
                                 f"hijacked via the expired hostname"))
                pillar["score"] -= 25


def check_transport(domain, findings, pillar):
    mta_sts_txt = txt_flat(f"_mta-sts.{domain}")
    if not any("v=STSv1" in t for t in mta_sts_txt):
        findings.append(("warning",
                         "No MTA-STS (_mta-sts TXT + policy) — TLS "
                         "enforcement for inbound SMTP not declared"))
        pillar["score"] -= 10
    else:
        findings.append(("info", "MTA-STS declared"))
    if not txt_flat(f"_smtp._tls.{domain}"):
        findings.append(("info",
                         "No TLS-RPT (_smtp._tls) — no visibility into "
                         "TLS failures on inbound mail"))


def check_dnssec(domain, findings, pillar):
    try:
        ans = dns.resolver.resolve(domain, "DS", lifetime=6)
        has_ds = len(ans) > 0
    except Exception:
        has_ds = False
    if not has_ds:
        findings.append(("warning",
                         "No DS record — DNSSEC not enabled (zone is not "
                         "authenticated; lookalike/signed-subdomain attacks "
                         "possible)"))
        pillar["score"] -= 12


def check_caa(domain, findings, pillar):
    try:
        ans = dns.resolver.resolve(domain, "CAA", lifetime=6)
        caa = [r.to_text() for r in ans]
    except Exception:
        caa = []
    if not caa:
        findings.append(("warning",
                         "No CAA record — any CA can issue certificates "
                         "for this domain"))
        pillar["score"] -= 10
    else:
        issuers = [c for c in caa if "issue" in c]
        findings.append(("info",
                         f"CAA: {len(issuers)} issue tag(s) declared"))


def check_ns(domain, findings):
    try:
        ans = dns.resolver.resolve(domain, "NS", lifetime=6)
        ns = sorted({r.to_text().rstrip('.').lower() for r in ans})
        if len(ns) < 2:
            findings.append(("warning",
                             f"Only {len(ns)} NS server(s) — single point "
                             f"of failure for resolution"))
        findings.append(("info", f"NS: {', '.join(ns)}"))
    except Exception:
        pass


def check_exposure(domain, findings, pillar, wordlist, do_subs):
    # wildcard detection
    probe = f"definitely-not-real-{id(domain)%9973}.{domain}"
    if get_records(probe, "A") or get_records(probe, "CNAME"):
        findings.append(("info",
                         "Wildcard DNS detected — subdomain enumeration "
                         "results unreliable"))
        pillar["score"] -= 5
        return
    if not do_subs:
        return
    exposed = []
    dangling = []
    for sub in wordlist:
        fqdn = f"{sub}.{domain}"
        cnames = get_records(fqdn, "CNAME")
        for c in cnames:
            c = c.rstrip(".").lower()
            if any(m in c for m in DANGLING_MARKERS):
                dangling.append(f"{fqdn} -> {c}")
        if get_records(fqdn, "A") or get_records(fqdn, "AAAA") or cnames:
            exposed.append(fqdn)
    if dangling:
        findings.append(("critical",
                         f"Possible dangling CNAMEs (takeover candidates): "
                         f"{', '.join(dangling)}"))
        pillar["score"] -= 20
    if exposed:
        findings.append(("warning",
                         f"{len(exposed)} sensitive-looking hostnames "
                         f"resolvable: {', '.join(exposed[:8])}"
                         f"{'...' if len(exposed) > 8 else ''}"))
        pillar["score"] -= min(10, len(exposed) * 2)


def audit(domain, do_subs=True, wordlist=None):
    if wordlist is None:
        wordlist = SENSITIVE_SUBDOMAINS
    pillars = {k: {"score": 100} for k in
               ("Email Auth", "Transport", "DNS Integrity", "Exposure")}
    findings = []
    check_spf(domain, findings, pillars["Email Auth"])
    check_dmarc(domain, findings, pillars["Email Auth"])
    check_dkim(domain, findings, pillars["Email Auth"])
    check_mx(domain, findings, pillars["Email Auth"])
    check_transport(domain, findings, pillars["Transport"])
    check_dnssec(domain, findings, pillars["DNS Integrity"])
    check_caa(domain, findings, pillars["DNS Integrity"])
    check_ns(domain, findings)
    check_exposure(domain, findings, pillars["Exposure"],
                   wordlist, do_subs)
    for p in pillars.values():
        p["score"] = max(0, p["score"])
    overall = round(sum(p["score"] for p in pillars.values())
                    / len(pillars))
    sev_order = {"critical": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda f: sev_order[f[0]])
    return {"domain": domain, "score": overall, "pillars":
            {k: v["score"] for k, v in pillars.items()},
            "findings": [{"severity": s, "detail": d}
                         for s, d in findings]}


def render(report):
    bar = lambda s: "█" * (s // 10) + "░" * (10 - s // 10)
    out = [f"\n=== {report['domain']} — posture {report['score']}/100 ==="]
    for name, score in report["pillars"].items():
        out.append(f"  {name:<15} {bar(score)} {score}")
    out.append("")
    fixes = []
    for f in report["findings"]:
        icon = {"critical": "✗", "warning": "!", "info": "·"}[f["severity"]]
        out.append(f"  [{icon}] ({f['severity']}) {f['detail']}")
        if f["severity"] in ("critical", "warning"):
            fixes.append(f["detail"])
    if fixes:
        out.append("\n  Fix first:")
        out.extend(f"    {i+1}. {x}" for i, x in enumerate(fixes[:5]))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("domains", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-subdomains", action="store_true")
    ap.add_argument("--wordlist")
    a = ap.parse_args()
    if not HAVE_DNSPYTHON:
        sys.exit("dnspython required: pip install dnspython")
    wordlist = None
    if a.wordlist:
        wordlist = [l.strip() for l in open(a.wordlist)
                    if l.strip() and not l.startswith("#")]
    reports = [audit(d, do_subs=not a.no_subdomains,
                     wordlist=wordlist) for d in a.domains]
    if a.json:
        print(json.dumps(reports, indent=2))
    else:
        for r in reports:
            print(render(r))


if __name__ == "__main__":
    main()
