#!/usr/bin/env python3
"""
_analyze.py — Contact analysis layer for email-summarizer.

NOT a standalone script. Imported by build_report.py.

Provides:
  infer_owner(emails)              → str
  build_contacts(emails, owner)    → list[dict]
  MERGE_MAP                        → dict  (address normalization table)
"""

import re
from collections import defaultdict, Counter

from _core import parse_addr, get_domain, strip_html


# ── Address normalization ─────────────────────────────────────────────────────
# Maps known alias/subdomain addresses to a canonical (display_name, address).

MERGE_MAP: dict = {
    "service@mail8.lietou-edm.com":  ("Liepin",  "service@liepin.com"),
    "service@mail19.lietou-edm.com": ("Liepin",  "service@liepin.com"),
}


# ── Domain → company lookup ────────────────────────────────────────────────────

DOMAIN_COMPANY: dict = {
    "github.com":                  "GitHub",
    "linkedin.com":                "LinkedIn",
    "xing.com":                    "XING",
    "mail.xing.com":               "XING",
    "lietou-edm.com":              "Liepin",
    "liepin.com":                  "Liepin",
    "maimai.mobi":                 "Maimai",
    "patreon.com":                 "Patreon",
    "discord.com":                 "Discord",
    "mail.hsbc.com.hk":            "HSBC",
    "notification.hsbc.com.hk":    "HSBC",
    "hsbc.com.hk":                 "HSBC",
    "bank.za.group":               "ZA Bank",
    "hello.stackoverflow.email":   "Stack Overflow",
    "stackoverflow.email":         "Stack Overflow",
    "mail.coursera.org":           "Coursera / Stanford",
    "e.cathaypacific.com":         "Cathay Pacific",
    "conductor.build":             "Conductor",
    "email.webook.com":            "Webook",
    "nia.gov.cn":                  "China Immigration Bureau",
    "service.netease.com":         "NetEase (163 Mail)",
    "163.com":                     "163 Mail (NetEase)",
    "quora.com":                   "Quora",
    "tavily.com":                  "Tavily",
    "polyu.edu.hk":                "Hong Kong Polytechnic University",
}

_SYSTEM_KW = frozenset({
    "noreply", "no-reply", "mailrobot", "notification", "service",
    "donotreply", "do-not-reply", "support", "info", "admin", "alert",
    "newsletter", "mailer", "robot", "bot", "auto", "jobs", "digest",
    "news", "mkt", "help", "safe", "security",
})


# ── Inference helpers ─────────────────────────────────────────────────────────

def infer_company(domain: str, display_name: str, bodies: list) -> str:
    d = domain.lower()
    for k, v in DOMAIN_COMPANY.items():
        if d == k or d.endswith("." + k):
            return v
    combined = " ".join(bodies[:3])
    for pat in [
        r"\bat\s+([A-Z][A-Za-z0-9 &,.\-]{2,40})",
        r"Company[:\s]+([A-Za-z0-9 &,.\-]{2,40})",
    ]:
        m = re.search(pat, combined)
        if m:
            return m.group(1).strip().rstrip(".,")
    for part in d.split("."):
        if part not in ("www", "mail", "smtp", "imap", "com", "org", "net", "cn", "hk", "io"):
            return part.capitalize()
    return domain


def infer_preferred_name(display_name: str, addr: str, bodies: list) -> str:
    n = (display_name or "").strip()
    local = addr.split("@")[0].lower()
    if n and not any(k in n.lower() for k in _SYSTEM_KW) and len(n) <= 50:
        if re.search(r"[A-Za-z\u4e00-\u9fff]", n):
            return n
    combined = "\n".join(bodies[:3])
    for pat in [
        r"(?:Best|Regards|Thanks|Cheers|Sincerely|Warm regards)[,\s]+([A-Z][a-z]+(?: [A-Z][a-z]+)?)",
        r"--\s*\n([A-Z][a-z]+(?: [A-Z][a-z]+)?)",
    ]:
        m = re.search(pat, combined)
        if m:
            return m.group(1).strip()
    if any(k in local for k in _SYSTEM_KW):
        return display_name or local
    return re.sub(r"[\._\-\+\d]+", " ", local).strip().title() or display_name or local


def infer_position(display_name: str, domain: str, subjects: list, bodies: list) -> str:
    d = domain.lower()
    if "lietou" in d or "liepin" in d:         return "Headhunter / Recruiter"
    if "linkedin.com" in d:                    return "Platform Bot (LinkedIn)"
    if "xing.com" in d:
        return "Job Recommendation Bot" if "jobs" in (display_name or "").lower() else "Platform Bot (XING)"
    if "github.com" in d:                      return "Platform Bot (GitHub)"
    if "discord.com" in d:                     return "Platform Bot (Discord)"
    if "hsbc" in d:                            return "Banking Service"
    if "za.group" in d:                        return "Banking Service"
    if "stackoverflow" in d or "coursera" in d: return "Platform Bot (Education)"
    if "cathaypacific" in d or "cathay" in d:  return "Airline Service"
    if "nia.gov.cn" in d:                      return "Government Service"
    if "netease" in d or "163.com" in d:       return "Platform Bot (Mail Provider)"
    if "patreon.com" in d:                     return "Content Creator"
    if "polyu.edu.hk" in d:                    return "University Staff / Admin"

    body_text = " ".join(bodies[:5])
    for pat in [
        r"(?:Title|Position|Role)[:\s]+([A-Za-z &/\-]{3,50})",
        r"\n([A-Z][a-z]+(?: [A-Z][a-z]+)?\s*\|)",
    ]:
        m = re.search(pat, body_text)
        if m:
            c = m.group(1).strip(" |")
            if 3 < len(c) < 60:
                return c

    subj_text = " ".join(subjects).lower()
    if any(k in subj_text for k in ["recruit", "opportunity", "position", "job", "career", "hiring"]):
        return "Recruiter"
    if any(k in subj_text for k in ["invoice", "payment", "purchase", "order"]):
        return "Finance / Billing"
    if any(k in subj_text for k in ["security", "alert", "verify", "confirm", "login"]):
        return "Security Service"
    return "Unknown"


def summarise_subjects(subjects: list) -> str:
    if not subjects:
        return "—"
    unique = list(dict.fromkeys(s.strip() for s in subjects if s.strip()))
    if len(unique) == 1:
        return unique[0][:90]
    clean = []
    for s in unique:
        s = re.sub(r"^(?:Re|Fwd|FW|AW|回复|转发)[:\s]+", "", s, flags=re.IGNORECASE).strip()
        s = re.sub(r"^\[.*?\]\s*", "", s).strip()
        if s:
            clean.append(s)
    if not clean:
        return unique[0][:90]
    words = [set(re.findall(r"[a-zA-Z]{4,}", s.lower())) for s in clean]
    if len(words) >= 2:
        common = words[0].intersection(*words[1:])
        common -= {"your", "with", "this", "that", "from", "have", "will", "been", "about"}
        if common:
            return f"{max(common, key=len).title()}-related ({len(unique)} emails)"
    preview = " · ".join(clean[:3])
    if len(unique) > 3:
        preview += f" (+{len(unique)-3} more)"
    return preview[:120]


# ── Owner inference ───────────────────────────────────────────────────────────

def infer_owner(emails: list) -> str:
    """
    Infer the mailbox owner from email records.

    The owner is the address most frequently appearing as a recipient in
    received emails. Prefers 'to_addrs' (real SMTP addresses from PST
    recipient table) over the 'to' display-name string.

    Returns lowercase address, or '' if not determinable.
    """
    counter: Counter = Counter()
    for e in emails:
        if e.get("direction", "received") == "received":
            smtp_addrs = e.get("to_addrs", [])
            if smtp_addrs:
                for addr in smtp_addrs:
                    if addr:
                        counter[addr.lower()] += 1
            else:
                for part in e.get("to", "").split(","):
                    _, addr = parse_addr(part.strip())
                    if addr and "@" in addr:
                        counter[addr.lower()] += 1
    return counter.most_common(1)[0][0] if counter else ""


# ── Contact builder ───────────────────────────────────────────────────────────

def build_contacts(emails: list, owner: str) -> list:
    """
    Analyse email records and return a ranked contact list.

    Each contact dict contains:
      preferred_name, email, company, position, subject_summary,
      source, received, sent, total

    owner: lowercase email address of the mailbox owner — excluded from results.
    """
    raw: dict = defaultdict(lambda: {
        "display_name": "", "email": "", "domain": "",
        "received": 0, "sent": 0,
        "subjects": [], "bodies": [],
        "sources": set(),
    })

    for e in emails:
        direction = e.get("direction", "received")
        subj      = e.get("subject", "").strip()
        body_raw  = e.get("body", "")
        body      = (strip_html(body_raw) if "<" in body_raw else body_raw)[:500]

        if direction == "received":
            name, addr = parse_addr(e.get("from", ""))
            if not addr:
                continue
            raw_key = addr.lower()
            if raw_key in MERGE_MAP:
                name, addr = MERGE_MAP[raw_key]
            key = addr.lower()
            c = raw[key]
            if not c["email"]:
                c["display_name"] = name
                c["email"]        = addr
                c["domain"]       = get_domain(addr)
            c["received"] += 1
            c["subjects"].append(subj)
            c["bodies"].append(body)
            c["sources"].add("From")
            for part in e.get("cc", "").split(","):
                _, cc_addr = parse_addr(part.strip())
                if cc_addr and owner not in cc_addr.lower():
                    ck = cc_addr.lower()
                    raw[ck]["sources"].add("CC")
                    if not raw[ck]["email"]:
                        raw[ck]["email"]  = cc_addr
                        raw[ck]["domain"] = get_domain(cc_addr)
        else:
            for part in e.get("to", "").split(","):
                _, addr = parse_addr(part.strip())
                if not addr or owner in addr.lower():
                    continue
                key = addr.lower()
                raw[key]["sent"] += 1
                raw[key]["sources"].add("To")
                if not raw[key]["email"]:
                    raw[key]["email"]  = addr
                    raw[key]["domain"] = get_domain(addr)
            for part in e.get("cc", "").split(","):
                _, addr = parse_addr(part.strip())
                if not addr or owner in addr.lower():
                    continue
                key = addr.lower()
                raw[key]["sources"].add("CC")
                if not raw[key]["email"]:
                    raw[key]["email"]  = addr
                    raw[key]["domain"] = get_domain(addr)

    raw.pop(owner, None)

    src_order = {"From": 0, "To": 1, "CC": 2}
    result = []
    for c in raw.values():
        total = c["received"] + c["sent"]
        result.append({
            "preferred_name":  infer_preferred_name(c["display_name"], c["email"], c["bodies"]),
            "email":           c["email"],
            "company":         infer_company(c["domain"], c["display_name"], c["bodies"]),
            "position":        infer_position(c["display_name"], c["domain"], c["subjects"], c["bodies"]),
            "subject_summary": summarise_subjects(c["subjects"]),
            "source":          " / ".join(sorted(c["sources"], key=lambda x: src_order.get(x, 9))) or "—",
            "received":        c["received"],
            "sent":            c["sent"],
            "total":           total,
        })

    return sorted(result, key=lambda x: -x["total"])
