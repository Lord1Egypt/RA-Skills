---
name: domain-analyze
description: Analyze a specific domain using registration, DNS, website, safety, backlink, cross-TLD, and market and legal-risk evidence. Use when a user asks what is known about a domain, wants due diligence before acquiring one, or requests a technical domain analysis. Do not use for generating domain names, simple availability checks, or expired-domain evaluation.
---

# Domain Analysis

**What this does:** builds a complete, evidence-based picture of one domain, its registration, safety, DNS setup, cross-TLD footprint, backlink profile, current usage, and market and legal context.

**Data interfaces it needs.** DomainKits MCP supplies part of the technical evidence through the tools below; host-provided web search and WebFetch supply public context and page inspection. Equivalent providers are acceptable. Never assume an MCP payload contains a record type or field that it does not actually return. Mark a missing field or capability `Unavailable` and continue.

- WHOIS / registration lookup, DomainKits: `whois`
- DNS records (at least A, AAAA, MX, NS, TXT, CNAME; CAA when relevant), DomainKits: `dns`
- Safe Browsing / malware status, DomainKits: `safety`
- Backlink profile (rank, referring domains, spam score, and link-type distribution when the source provides it), DomainKits: `backlink_summary`
- Cross-TLD registration data, DomainKits: `tld_check`
- Public Suffix List rules and IDN / punycode conversion, for input normalization
- Web search capability (market background, news, disputes)
- Web fetch capability (load the domain and its variants)

## Input normalization

Before analyzing, resolve the input to a single registrable domain, but do not silently change the user's intent. If the input is a URL, subdomain, or path, state the registrable domain you will analyze (for example, `https://blog.example.co.uk/x` reduces to `example.co.uk`) and proceed. Determine the registrable domain using Public Suffix List rules; do not assume it is always the final two labels (`.co.uk`, `.com.au`, `.github.io` and similar require the PSL to split correctly). Convert IDN / Unicode input to its punycode (`xn--`) form and note both. If the input is ambiguous (could map to more than one registrable domain), ask which one before proceeding.

## Evidence discipline

This is the core rule of the skill. Classify every material finding as Fact, Inference, or Unknown. Group related facts where doing so remains unambiguous.

- **Fact:** returned directly by a tool or read from a page (for example, "WHOIS status is clientTransferProhibited", "MX records are present").
- **Inference:** an interpretation supported by one or more facts but not confirmed. Always phrase with "may indicate", "is consistent with", or "suggests", never as fact.
- **Unknown:** the available data cannot decide the question. Say so explicitly.

Never convert absence of data into a negative finding. "No trademark hits returned" is not "the mark is clear"; "no sale record found" is not "never sold"; "no A record" is not "abandoned". Every time-sensitive conclusion must carry the date it was observed.

For DNS, distinguish an explicitly returned empty record set from a record type the source does not support. In particular, if `dns` does not return a `CAA` field, report CAA as `Not Provided` or query an independent DNS source; never interpret the missing field as proof that no CAA record exists.

## Workflow

Run the queries independently. A single tool failing, timing out, returning nothing, or being unavailable must NOT stop the rest of the report; mark that section Unavailable and continue. If the user asked only about one aspect (for example, just safety, or just backlinks), run that part and skip the rest: deliver only the section(s) that answer the question, plus their evidence limitations and sources, and do not emit the remaining sections of the full structure. The fixed output structure below applies in full only to a full-domain analysis; a narrow request returns the matching subset in the same format.

1. **Gather core data in parallel:**
   - `whois` for registrar, key dates, and status codes.
   - `dns` for A, AAAA, MX, NS, TXT, CNAME, and CAA when the actual response supports it. Otherwise mark CAA `Not Provided` or use an independent DNS source.
   - `safety` for malware / Safe Browsing status.
   - `backlink_summary` for rank, referring domains, and spam score, plus link-type distribution only when the source returns it.
   - `tld_check` for cross-TLD registration data.

2. **Cross-TLD investigation (conditional).** Use the rating the tool provides. If the tool gives no rating, report the raw count and the set of TLDs checked; do not label a count "high" on your own. If cross-TLD registration is notable, `whois` the common variants (.com/.net/.org) and record the registrars. Report the pattern as a fact; treat its meaning as inference (for example, "several variants use the same registrar, which may indicate coordinated registration, but does not establish common ownership; WHOIS privacy and registrar migrations can produce the same pattern"). Common ownership can only be inferred further when WHOIS registrant or organization details match. If you fetch the variants to see whether they resolve to the same site, each variant is a distinct domain: run `safety` on that variant before fetching it, and never carry the target domain's safety result over to a variant. Skip the fetch for any variant that safety flags as malicious, phishing, or malware-hosting, record the flag, and report only its non-fetch evidence (WHOIS, DNS).

3. **Website status.** Check the `safety` result first. If safety has flagged the domain as malicious, phishing, or malware-hosting, do NOT fetch it. Warn the user that the domain carries a serious safety flag and that continuing the analysis is not advised. Only if the user explicitly insists, skip the fetch (never load a flagged domain) and continue with the rest of the analysis; in that case the assessment defaults to not advised for registration, acquisition, or use, and the safety flag is the leading finding. If safety is clean or Unavailable, fetch the domain to determine current use: active business, parked page, for-sale landing, or no content. Distinguish and record HTTP redirects (and their target), TLS errors, login walls, and anti-bot / captcha pages, rather than treating them as "no content".

4. **Market and legal context.** Search the web for context that technical data cannot show: recent sale history, related news or brand events, and legal disputes (UDRP, trademark conflicts). Cite a source for each external claim, with the observation date. Prefer authoritative sources by type: UDRP from official decision databases (WIPO, Forum); trademarks from official trademark registries; sale prices from verifiable sale databases or marketplace announcements. A search-result snippet is not final evidence; open the original page to confirm. Historical pricing MUST distinguish confirmed public sale records from current listing / asking prices; do not merge them. Any trademark or UDRP observation is a search result, not a legal opinion.

5. **Synthesize the report** using the fixed structure below, so output is consistent across runs.

## Output structure

This is the structure for a full-domain analysis. For a narrow request (per the workflow note above), return only the sections that answer it, keeping this format and each included section's evidence limitations and sources.

1. **Executive summary**: the few findings that matter most, each with a confidence level:
   - **High:** directly reported by an authoritative source or tool.
   - **Medium:** supported by multiple consistent signals.
   - **Low:** based on a single indirect or incomplete signal.
2. **Registration**: registrar, creation/expiry dates, status codes.
3. **DNS and email**: A/AAAA, NS, MX, TXT, CNAME, CAA as found; note email configuration presence as a fact, not proof of active use.
4. **Website status**: live content, parked, redirect (with target), TLS/login/anti-bot state.
5. **Safety**: Safe Browsing / malware status. If flagged as malicious, phishing, or malware-hosting, this is the leading finding: state that the domain was not fetched, and that registration, acquisition, or use is not advised.
6. **Backlinks and SEO**: rank, referring domains, spam risk, and link-type distribution only when the source provides it (otherwise mark it Not Provided).
7. **Cross-TLD footprint**: counts, TLDs checked, registrar pattern (fact vs inference).
8. **Market and legal context**: sales history (public sale vs asking price), news, disputes, each with source and date.
9. **Evidence gaps and limitations**: every section marked Unavailable, and what could not be determined.
10. **Sources and observation timestamps**: external sources and the dates each fact was observed.

Do not make buy / don't-buy judgments, with one exception: a domain flagged by safety as malicious, phishing, or malware-hosting is reported as not advised for registration, acquisition, or use. Otherwise present evidence and let the user decide.

## Next steps

If the user's goal is not already known, ask one concise follow-up question. Otherwise, tailor next steps directly to the stated goal:

- Wants market pricing: a listing-based comparative market analysis is available, positioning the domain against current for-sale comparables rather than estimating a sale price (see domain-cma-valuation).
- Domain is listed for sale: state which marketplace it is on so the user can verify it directly.
- Wants alternatives: a naming consultation with a taken-target mode is available (see domain-name-advisor).
- Wants to track changes: a monitoring capability can watch the domain.

## Key principles

- Never fetch a domain that safety has flagged as malicious, phishing, or malware-hosting. Make the safety flag the leading finding, and default the assessment to not advised for registration, acquisition, or use, even if the user insists on continuing.
- Classify every material finding as fact, inference, or unknown. Use "may indicate" / "is consistent with" for inference.
- Absence of a record is never proof of absence. Do not read "not found" as "does not exist".
- Every query is independent; one failure marks a section Unavailable and does not abort the report.
- Every time-sensitive claim carries its observation date; every external claim carries its source.
- When a domain is for sale, name the marketplace so the user can verify it. Do not add referral or affiliate links.
