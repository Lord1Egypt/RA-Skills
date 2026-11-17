# domain-recon — per-TLD RDAP coverage map

_Generated 2026-07-27 from authoritative IANA data. Regenerate with `python3 scripts/gen_coverage.py`._

- **TLD source:** `Version 2026072600, Last Updated Sun Jul 26 07:07:02 2026 UTC` — IANA `tlds-alpha-by-domain.txt` (1438 delegated TLDs)
- **RDAP bootstrap:** IANA `data.iana.org/rdap/dns.json`
- **Supplement:** `_RDAP_SUPPLEMENT` in `scripts/recon.py` — each entry verified live (HTTP 200 + real RDAP data, plus a clean 404 for a bogus name in the same TLD)

## Why only RDAP is mapped per-TLD

`rdap` is the **only** TLD-variable query. Every other subcommand is TLD-agnostic and works for any registrable name / IP / ASN, so it is **not** re-checked per TLD:

| subcommand | source | TLD-dependent? |
|---|---|---|
| `dns`     | DNS-over-HTTPS (Google / Cloudflare) | no — universal |
| `certs`   | crt.sh → certSpotter CT fallback     | no — universal |
| `ip`      | ip-api.com                           | no — operates on IPs |
| `asn`     | RIPEstat                             | no — operates on IPs / ASNs |
| `wayback` | archive.org                          | no — universal |
| `rdap`    | IANA bootstrap → supplement → rdap.org | **yes** — see table below |

## Summary

| rdap_source | TLDs | meaning |
|---|---:|---|
| `bootstrap`  | 1200 | authoritative RDAP server published in IANA's bootstrap; resolved automatically |
| `supplement` | 18 | registry runs a public RDAP server IANA omits; added to `_RDAP_SUPPLEMENT` (verified live) |
| `none`       | 220 | no public RDAP server → `rdap` returns a first-class `unsupported` result (graceful degradation) |
| **total**    | **1438** | |

For a `none` TLD, `recon.py rdap <domain>` returns `{"supported": false, "rdap_source": "none", "reason": "..."}` at **exit 0**, so a calling agent skips the field instead of treating a 404 as a tool failure. `dns` / `certs` / `ip` / `asn` / `wayback` still work for domains in these TLDs.

## Supplement entries (18 — verified live 2026-07-27)

| TLD | rdap server | registry |
|---|---|---|
| `.ac` | `https://rdap.identitydigital.services/rdap` | Identity Digital |
| `.af` | `https://rdap.nic.af` | nic.af |
| `.aw` | `https://rdap.nic.aw` | nic.aw |
| `.ch` | `https://rdap.nic.ch` | SWITCH |
| `.ci` | `https://rdap.nic.ci` | nic.ci |
| `.de` | `https://rdap.denic.de` | DENIC |
| `.ga` | `https://rdap.nic.ga` | nic.ga |
| `.io` | `https://rdap.identitydigital.services/rdap` | Identity Digital |
| `.kn` | `https://rdap.nic.kn` | nic.kn |
| `.kz` | `https://rdap.nic.kz` | nic.kz |
| `.mr` | `https://rdap.nic.mr` | nic.mr |
| `.mz` | `https://rdap.nic.mz` | nic.mz |
| `.sb` | `https://rdap.nic.sb` | nic.sb |
| `.sh` | `https://rdap.identitydigital.services/rdap` | Identity Digital |
| `.so` | `https://rdap.nic.so` | nic.so |
| `.td` | `https://rdap.nic.td` | nic.td |
| `.tl` | `https://rdap.nic.tl` | nic.tl |
| `.us` | `https://rdap.nic.us` | GoDaddy Registry (nic.us) |

## Full coverage table (1438 TLDs)

| TLD | rdap_source | notes |
|---|---|---|
| `.aaa` | bootstrap | IANA RDAP bootstrap |
| `.aarp` | bootstrap | IANA RDAP bootstrap |
| `.abb` | bootstrap | IANA RDAP bootstrap |
| `.abbott` | bootstrap | IANA RDAP bootstrap |
| `.abbvie` | bootstrap | IANA RDAP bootstrap |
| `.abc` | bootstrap | IANA RDAP bootstrap |
| `.able` | bootstrap | IANA RDAP bootstrap |
| `.abogado` | bootstrap | IANA RDAP bootstrap |
| `.abudhabi` | bootstrap | IANA RDAP bootstrap |
| `.ac` | supplement | https://rdap.identitydigital.services/rdap — Identity Digital |
| `.academy` | bootstrap | IANA RDAP bootstrap |
| `.accenture` | bootstrap | IANA RDAP bootstrap |
| `.accountant` | bootstrap | IANA RDAP bootstrap |
| `.accountants` | bootstrap | IANA RDAP bootstrap |
| `.aco` | bootstrap | IANA RDAP bootstrap |
| `.actor` | bootstrap | IANA RDAP bootstrap |
| `.ad` | bootstrap | IANA RDAP bootstrap |
| `.ads` | bootstrap | IANA RDAP bootstrap |
| `.adult` | bootstrap | IANA RDAP bootstrap |
| `.ae` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.aeg` | bootstrap | IANA RDAP bootstrap |
| `.aero` | bootstrap | IANA RDAP bootstrap |
| `.aetna` | bootstrap | IANA RDAP bootstrap |
| `.af` | supplement | https://rdap.nic.af — nic.af |
| `.afl` | bootstrap | IANA RDAP bootstrap |
| `.africa` | bootstrap | IANA RDAP bootstrap |
| `.ag` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.agakhan` | bootstrap | IANA RDAP bootstrap |
| `.agency` | bootstrap | IANA RDAP bootstrap |
| `.ai` | bootstrap | IANA RDAP bootstrap |
| `.aig` | bootstrap | IANA RDAP bootstrap |
| `.airbus` | bootstrap | IANA RDAP bootstrap |
| `.airforce` | bootstrap | IANA RDAP bootstrap |
| `.airtel` | bootstrap | IANA RDAP bootstrap |
| `.akdn` | bootstrap | IANA RDAP bootstrap |
| `.al` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.alibaba` | bootstrap | IANA RDAP bootstrap |
| `.alipay` | bootstrap | IANA RDAP bootstrap |
| `.allfinanz` | bootstrap | IANA RDAP bootstrap |
| `.allstate` | bootstrap | IANA RDAP bootstrap |
| `.ally` | bootstrap | IANA RDAP bootstrap |
| `.alsace` | bootstrap | IANA RDAP bootstrap |
| `.alstom` | bootstrap | IANA RDAP bootstrap |
| `.am` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.amazon` | bootstrap | IANA RDAP bootstrap |
| `.americanexpress` | bootstrap | IANA RDAP bootstrap |
| `.americanfamily` | bootstrap | IANA RDAP bootstrap |
| `.amex` | bootstrap | IANA RDAP bootstrap |
| `.amfam` | bootstrap | IANA RDAP bootstrap |
| `.amica` | bootstrap | IANA RDAP bootstrap |
| `.amsterdam` | bootstrap | IANA RDAP bootstrap |
| `.analytics` | bootstrap | IANA RDAP bootstrap |
| `.android` | bootstrap | IANA RDAP bootstrap |
| `.anquan` | bootstrap | IANA RDAP bootstrap |
| `.anz` | bootstrap | IANA RDAP bootstrap |
| `.ao` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.aol` | bootstrap | IANA RDAP bootstrap |
| `.apartments` | bootstrap | IANA RDAP bootstrap |
| `.app` | bootstrap | IANA RDAP bootstrap |
| `.apple` | bootstrap | IANA RDAP bootstrap |
| `.aq` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.aquarelle` | bootstrap | IANA RDAP bootstrap |
| `.ar` | bootstrap | IANA RDAP bootstrap |
| `.arab` | bootstrap | IANA RDAP bootstrap |
| `.aramco` | bootstrap | IANA RDAP bootstrap |
| `.archi` | bootstrap | IANA RDAP bootstrap |
| `.army` | bootstrap | IANA RDAP bootstrap |
| `.arpa` | none | infrastructure TLD (reverse DNS); domain-RDAP N/A — use RIR RDAP for in-addr/ip6 |
| `.art` | bootstrap | IANA RDAP bootstrap |
| `.arte` | bootstrap | IANA RDAP bootstrap |
| `.as` | bootstrap | IANA RDAP bootstrap |
| `.asda` | bootstrap | IANA RDAP bootstrap |
| `.asia` | bootstrap | IANA RDAP bootstrap |
| `.associates` | bootstrap | IANA RDAP bootstrap |
| `.at` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.athleta` | bootstrap | IANA RDAP bootstrap |
| `.attorney` | bootstrap | IANA RDAP bootstrap |
| `.au` | bootstrap | IANA RDAP bootstrap |
| `.auction` | bootstrap | IANA RDAP bootstrap |
| `.audi` | bootstrap | IANA RDAP bootstrap |
| `.audible` | bootstrap | IANA RDAP bootstrap |
| `.audio` | bootstrap | IANA RDAP bootstrap |
| `.auspost` | bootstrap | IANA RDAP bootstrap |
| `.author` | bootstrap | IANA RDAP bootstrap |
| `.auto` | bootstrap | IANA RDAP bootstrap |
| `.autos` | bootstrap | IANA RDAP bootstrap |
| `.aw` | supplement | https://rdap.nic.aw — nic.aw |
| `.aws` | bootstrap | IANA RDAP bootstrap |
| `.ax` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.axa` | bootstrap | IANA RDAP bootstrap |
| `.az` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.azure` | bootstrap | IANA RDAP bootstrap |
| `.ba` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.baby` | bootstrap | IANA RDAP bootstrap |
| `.baidu` | bootstrap | IANA RDAP bootstrap |
| `.banamex` | bootstrap | IANA RDAP bootstrap |
| `.band` | bootstrap | IANA RDAP bootstrap |
| `.bank` | bootstrap | IANA RDAP bootstrap |
| `.bar` | bootstrap | IANA RDAP bootstrap |
| `.barcelona` | bootstrap | IANA RDAP bootstrap |
| `.barclaycard` | bootstrap | IANA RDAP bootstrap |
| `.barclays` | bootstrap | IANA RDAP bootstrap |
| `.barefoot` | bootstrap | IANA RDAP bootstrap |
| `.bargains` | bootstrap | IANA RDAP bootstrap |
| `.baseball` | bootstrap | IANA RDAP bootstrap |
| `.basketball` | bootstrap | IANA RDAP bootstrap |
| `.bauhaus` | bootstrap | IANA RDAP bootstrap |
| `.bayern` | bootstrap | IANA RDAP bootstrap |
| `.bb` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.bbc` | bootstrap | IANA RDAP bootstrap |
| `.bbt` | bootstrap | IANA RDAP bootstrap |
| `.bbva` | bootstrap | IANA RDAP bootstrap |
| `.bcg` | bootstrap | IANA RDAP bootstrap |
| `.bcn` | bootstrap | IANA RDAP bootstrap |
| `.bd` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.be` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.beats` | bootstrap | IANA RDAP bootstrap |
| `.beauty` | bootstrap | IANA RDAP bootstrap |
| `.beer` | bootstrap | IANA RDAP bootstrap |
| `.berlin` | bootstrap | IANA RDAP bootstrap |
| `.best` | bootstrap | IANA RDAP bootstrap |
| `.bestbuy` | bootstrap | IANA RDAP bootstrap |
| `.bet` | bootstrap | IANA RDAP bootstrap |
| `.bf` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.bg` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.bh` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.bharti` | bootstrap | IANA RDAP bootstrap |
| `.bi` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.bible` | bootstrap | IANA RDAP bootstrap |
| `.bid` | bootstrap | IANA RDAP bootstrap |
| `.bike` | bootstrap | IANA RDAP bootstrap |
| `.bing` | bootstrap | IANA RDAP bootstrap |
| `.bingo` | bootstrap | IANA RDAP bootstrap |
| `.bio` | bootstrap | IANA RDAP bootstrap |
| `.biz` | bootstrap | IANA RDAP bootstrap |
| `.bj` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.black` | bootstrap | IANA RDAP bootstrap |
| `.blackfriday` | bootstrap | IANA RDAP bootstrap |
| `.blockbuster` | bootstrap | IANA RDAP bootstrap |
| `.blog` | bootstrap | IANA RDAP bootstrap |
| `.bloomberg` | bootstrap | IANA RDAP bootstrap |
| `.blue` | bootstrap | IANA RDAP bootstrap |
| `.bm` | bootstrap | IANA RDAP bootstrap |
| `.bms` | bootstrap | IANA RDAP bootstrap |
| `.bmw` | bootstrap | IANA RDAP bootstrap |
| `.bn` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.bnpparibas` | bootstrap | IANA RDAP bootstrap |
| `.bo` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.boats` | bootstrap | IANA RDAP bootstrap |
| `.boehringer` | bootstrap | IANA RDAP bootstrap |
| `.bofa` | bootstrap | IANA RDAP bootstrap |
| `.bom` | bootstrap | IANA RDAP bootstrap |
| `.bond` | bootstrap | IANA RDAP bootstrap |
| `.boo` | bootstrap | IANA RDAP bootstrap |
| `.book` | bootstrap | IANA RDAP bootstrap |
| `.booking` | bootstrap | IANA RDAP bootstrap |
| `.bosch` | bootstrap | IANA RDAP bootstrap |
| `.bostik` | bootstrap | IANA RDAP bootstrap |
| `.boston` | bootstrap | IANA RDAP bootstrap |
| `.bot` | bootstrap | IANA RDAP bootstrap |
| `.boutique` | bootstrap | IANA RDAP bootstrap |
| `.box` | bootstrap | IANA RDAP bootstrap |
| `.br` | bootstrap | IANA RDAP bootstrap |
| `.bradesco` | bootstrap | IANA RDAP bootstrap |
| `.bridgestone` | bootstrap | IANA RDAP bootstrap |
| `.broadway` | bootstrap | IANA RDAP bootstrap |
| `.broker` | bootstrap | IANA RDAP bootstrap |
| `.brother` | bootstrap | IANA RDAP bootstrap |
| `.brussels` | bootstrap | IANA RDAP bootstrap |
| `.bs` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.bt` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.build` | bootstrap | IANA RDAP bootstrap |
| `.builders` | bootstrap | IANA RDAP bootstrap |
| `.business` | bootstrap | IANA RDAP bootstrap |
| `.buy` | bootstrap | IANA RDAP bootstrap |
| `.buzz` | bootstrap | IANA RDAP bootstrap |
| `.bv` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.bw` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.by` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.bz` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.bzh` | bootstrap | IANA RDAP bootstrap |
| `.ca` | bootstrap | IANA RDAP bootstrap |
| `.cab` | bootstrap | IANA RDAP bootstrap |
| `.cafe` | bootstrap | IANA RDAP bootstrap |
| `.cal` | bootstrap | IANA RDAP bootstrap |
| `.call` | bootstrap | IANA RDAP bootstrap |
| `.calvinklein` | bootstrap | IANA RDAP bootstrap |
| `.cam` | bootstrap | IANA RDAP bootstrap |
| `.camera` | bootstrap | IANA RDAP bootstrap |
| `.camp` | bootstrap | IANA RDAP bootstrap |
| `.canon` | bootstrap | IANA RDAP bootstrap |
| `.capetown` | bootstrap | IANA RDAP bootstrap |
| `.capital` | bootstrap | IANA RDAP bootstrap |
| `.capitalone` | bootstrap | IANA RDAP bootstrap |
| `.car` | bootstrap | IANA RDAP bootstrap |
| `.caravan` | bootstrap | IANA RDAP bootstrap |
| `.cards` | bootstrap | IANA RDAP bootstrap |
| `.care` | bootstrap | IANA RDAP bootstrap |
| `.career` | bootstrap | IANA RDAP bootstrap |
| `.careers` | bootstrap | IANA RDAP bootstrap |
| `.cars` | bootstrap | IANA RDAP bootstrap |
| `.casa` | bootstrap | IANA RDAP bootstrap |
| `.case` | bootstrap | IANA RDAP bootstrap |
| `.cash` | bootstrap | IANA RDAP bootstrap |
| `.casino` | bootstrap | IANA RDAP bootstrap |
| `.cat` | bootstrap | IANA RDAP bootstrap |
| `.catering` | bootstrap | IANA RDAP bootstrap |
| `.catholic` | bootstrap | IANA RDAP bootstrap |
| `.cba` | bootstrap | IANA RDAP bootstrap |
| `.cbn` | bootstrap | IANA RDAP bootstrap |
| `.cbre` | bootstrap | IANA RDAP bootstrap |
| `.cc` | bootstrap | IANA RDAP bootstrap |
| `.cd` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.center` | bootstrap | IANA RDAP bootstrap |
| `.ceo` | bootstrap | IANA RDAP bootstrap |
| `.cern` | bootstrap | IANA RDAP bootstrap |
| `.cf` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.cfa` | bootstrap | IANA RDAP bootstrap |
| `.cfd` | bootstrap | IANA RDAP bootstrap |
| `.cg` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ch` | supplement | https://rdap.nic.ch — SWITCH |
| `.chanel` | bootstrap | IANA RDAP bootstrap |
| `.channel` | bootstrap | IANA RDAP bootstrap |
| `.charity` | bootstrap | IANA RDAP bootstrap |
| `.chase` | bootstrap | IANA RDAP bootstrap |
| `.chat` | bootstrap | IANA RDAP bootstrap |
| `.cheap` | bootstrap | IANA RDAP bootstrap |
| `.chintai` | bootstrap | IANA RDAP bootstrap |
| `.christmas` | bootstrap | IANA RDAP bootstrap |
| `.chrome` | bootstrap | IANA RDAP bootstrap |
| `.church` | bootstrap | IANA RDAP bootstrap |
| `.ci` | supplement | https://rdap.nic.ci — nic.ci |
| `.cipriani` | bootstrap | IANA RDAP bootstrap |
| `.circle` | bootstrap | IANA RDAP bootstrap |
| `.cisco` | bootstrap | IANA RDAP bootstrap |
| `.citadel` | bootstrap | IANA RDAP bootstrap |
| `.citi` | bootstrap | IANA RDAP bootstrap |
| `.citic` | bootstrap | IANA RDAP bootstrap |
| `.city` | bootstrap | IANA RDAP bootstrap |
| `.ck` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.cl` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.claims` | bootstrap | IANA RDAP bootstrap |
| `.cleaning` | bootstrap | IANA RDAP bootstrap |
| `.click` | bootstrap | IANA RDAP bootstrap |
| `.clinic` | bootstrap | IANA RDAP bootstrap |
| `.clinique` | bootstrap | IANA RDAP bootstrap |
| `.clothing` | bootstrap | IANA RDAP bootstrap |
| `.cloud` | bootstrap | IANA RDAP bootstrap |
| `.club` | bootstrap | IANA RDAP bootstrap |
| `.clubmed` | bootstrap | IANA RDAP bootstrap |
| `.cm` | bootstrap | IANA RDAP bootstrap |
| `.cn` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.co` | none | registry-level RDAP not exposed (per-registrar only) |
| `.coach` | bootstrap | IANA RDAP bootstrap |
| `.codes` | bootstrap | IANA RDAP bootstrap |
| `.coffee` | bootstrap | IANA RDAP bootstrap |
| `.college` | bootstrap | IANA RDAP bootstrap |
| `.cologne` | bootstrap | IANA RDAP bootstrap |
| `.com` | bootstrap | IANA RDAP bootstrap |
| `.commbank` | bootstrap | IANA RDAP bootstrap |
| `.community` | bootstrap | IANA RDAP bootstrap |
| `.company` | bootstrap | IANA RDAP bootstrap |
| `.compare` | bootstrap | IANA RDAP bootstrap |
| `.computer` | bootstrap | IANA RDAP bootstrap |
| `.comsec` | bootstrap | IANA RDAP bootstrap |
| `.condos` | bootstrap | IANA RDAP bootstrap |
| `.construction` | bootstrap | IANA RDAP bootstrap |
| `.consulting` | bootstrap | IANA RDAP bootstrap |
| `.contact` | bootstrap | IANA RDAP bootstrap |
| `.contractors` | bootstrap | IANA RDAP bootstrap |
| `.cooking` | bootstrap | IANA RDAP bootstrap |
| `.cool` | bootstrap | IANA RDAP bootstrap |
| `.coop` | bootstrap | IANA RDAP bootstrap |
| `.corsica` | bootstrap | IANA RDAP bootstrap |
| `.country` | bootstrap | IANA RDAP bootstrap |
| `.coupon` | bootstrap | IANA RDAP bootstrap |
| `.coupons` | bootstrap | IANA RDAP bootstrap |
| `.courses` | bootstrap | IANA RDAP bootstrap |
| `.cpa` | bootstrap | IANA RDAP bootstrap |
| `.cr` | bootstrap | IANA RDAP bootstrap |
| `.credit` | bootstrap | IANA RDAP bootstrap |
| `.creditcard` | bootstrap | IANA RDAP bootstrap |
| `.creditunion` | bootstrap | IANA RDAP bootstrap |
| `.cricket` | bootstrap | IANA RDAP bootstrap |
| `.crown` | bootstrap | IANA RDAP bootstrap |
| `.crs` | bootstrap | IANA RDAP bootstrap |
| `.cruise` | bootstrap | IANA RDAP bootstrap |
| `.cruises` | bootstrap | IANA RDAP bootstrap |
| `.cu` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.cuisinella` | bootstrap | IANA RDAP bootstrap |
| `.cv` | bootstrap | IANA RDAP bootstrap |
| `.cw` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.cx` | bootstrap | IANA RDAP bootstrap |
| `.cy` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.cymru` | bootstrap | IANA RDAP bootstrap |
| `.cyou` | bootstrap | IANA RDAP bootstrap |
| `.cz` | bootstrap | IANA RDAP bootstrap |
| `.dad` | bootstrap | IANA RDAP bootstrap |
| `.dance` | bootstrap | IANA RDAP bootstrap |
| `.data` | bootstrap | IANA RDAP bootstrap |
| `.date` | bootstrap | IANA RDAP bootstrap |
| `.dating` | bootstrap | IANA RDAP bootstrap |
| `.datsun` | bootstrap | IANA RDAP bootstrap |
| `.day` | bootstrap | IANA RDAP bootstrap |
| `.dclk` | bootstrap | IANA RDAP bootstrap |
| `.dds` | bootstrap | IANA RDAP bootstrap |
| `.de` | supplement | https://rdap.denic.de — DENIC |
| `.deal` | bootstrap | IANA RDAP bootstrap |
| `.dealer` | bootstrap | IANA RDAP bootstrap |
| `.deals` | bootstrap | IANA RDAP bootstrap |
| `.degree` | bootstrap | IANA RDAP bootstrap |
| `.delivery` | bootstrap | IANA RDAP bootstrap |
| `.dell` | bootstrap | IANA RDAP bootstrap |
| `.deloitte` | bootstrap | IANA RDAP bootstrap |
| `.delta` | bootstrap | IANA RDAP bootstrap |
| `.democrat` | bootstrap | IANA RDAP bootstrap |
| `.dental` | bootstrap | IANA RDAP bootstrap |
| `.dentist` | bootstrap | IANA RDAP bootstrap |
| `.desi` | bootstrap | IANA RDAP bootstrap |
| `.design` | bootstrap | IANA RDAP bootstrap |
| `.dev` | bootstrap | IANA RDAP bootstrap |
| `.dhl` | bootstrap | IANA RDAP bootstrap |
| `.diamonds` | bootstrap | IANA RDAP bootstrap |
| `.diet` | bootstrap | IANA RDAP bootstrap |
| `.digital` | bootstrap | IANA RDAP bootstrap |
| `.direct` | bootstrap | IANA RDAP bootstrap |
| `.directory` | bootstrap | IANA RDAP bootstrap |
| `.discount` | bootstrap | IANA RDAP bootstrap |
| `.discover` | bootstrap | IANA RDAP bootstrap |
| `.dish` | bootstrap | IANA RDAP bootstrap |
| `.diy` | bootstrap | IANA RDAP bootstrap |
| `.dj` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.dk` | none | Punktum dk — WHOIS/web only |
| `.dm` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.dnp` | bootstrap | IANA RDAP bootstrap |
| `.do` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.docs` | bootstrap | IANA RDAP bootstrap |
| `.doctor` | bootstrap | IANA RDAP bootstrap |
| `.dog` | bootstrap | IANA RDAP bootstrap |
| `.domains` | bootstrap | IANA RDAP bootstrap |
| `.dot` | bootstrap | IANA RDAP bootstrap |
| `.download` | bootstrap | IANA RDAP bootstrap |
| `.drive` | bootstrap | IANA RDAP bootstrap |
| `.dtv` | bootstrap | IANA RDAP bootstrap |
| `.dubai` | bootstrap | IANA RDAP bootstrap |
| `.dupont` | bootstrap | IANA RDAP bootstrap |
| `.durban` | bootstrap | IANA RDAP bootstrap |
| `.dvag` | bootstrap | IANA RDAP bootstrap |
| `.dvr` | bootstrap | IANA RDAP bootstrap |
| `.dz` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.earth` | bootstrap | IANA RDAP bootstrap |
| `.eat` | bootstrap | IANA RDAP bootstrap |
| `.ec` | bootstrap | IANA RDAP bootstrap |
| `.eco` | bootstrap | IANA RDAP bootstrap |
| `.edeka` | bootstrap | IANA RDAP bootstrap |
| `.edu` | none | EDUCAUSE — WHOIS-only |
| `.education` | bootstrap | IANA RDAP bootstrap |
| `.ee` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.eg` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.email` | bootstrap | IANA RDAP bootstrap |
| `.emerck` | bootstrap | IANA RDAP bootstrap |
| `.energy` | bootstrap | IANA RDAP bootstrap |
| `.engineer` | bootstrap | IANA RDAP bootstrap |
| `.engineering` | bootstrap | IANA RDAP bootstrap |
| `.enterprises` | bootstrap | IANA RDAP bootstrap |
| `.epson` | bootstrap | IANA RDAP bootstrap |
| `.equipment` | bootstrap | IANA RDAP bootstrap |
| `.er` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ericsson` | bootstrap | IANA RDAP bootstrap |
| `.erni` | bootstrap | IANA RDAP bootstrap |
| `.es` | none | Red.es — WHOIS-only |
| `.esq` | bootstrap | IANA RDAP bootstrap |
| `.estate` | bootstrap | IANA RDAP bootstrap |
| `.et` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.eu` | none | EURid; no public RDAP reachable from probe — WHOIS-only for our purposes |
| `.eurovision` | bootstrap | IANA RDAP bootstrap |
| `.eus` | bootstrap | IANA RDAP bootstrap |
| `.events` | bootstrap | IANA RDAP bootstrap |
| `.exchange` | bootstrap | IANA RDAP bootstrap |
| `.expert` | bootstrap | IANA RDAP bootstrap |
| `.exposed` | bootstrap | IANA RDAP bootstrap |
| `.express` | bootstrap | IANA RDAP bootstrap |
| `.extraspace` | bootstrap | IANA RDAP bootstrap |
| `.fage` | bootstrap | IANA RDAP bootstrap |
| `.fail` | bootstrap | IANA RDAP bootstrap |
| `.fairwinds` | bootstrap | IANA RDAP bootstrap |
| `.faith` | bootstrap | IANA RDAP bootstrap |
| `.family` | bootstrap | IANA RDAP bootstrap |
| `.fan` | bootstrap | IANA RDAP bootstrap |
| `.fans` | bootstrap | IANA RDAP bootstrap |
| `.farm` | bootstrap | IANA RDAP bootstrap |
| `.farmers` | bootstrap | IANA RDAP bootstrap |
| `.fashion` | bootstrap | IANA RDAP bootstrap |
| `.fast` | bootstrap | IANA RDAP bootstrap |
| `.fedex` | bootstrap | IANA RDAP bootstrap |
| `.feedback` | bootstrap | IANA RDAP bootstrap |
| `.ferrari` | bootstrap | IANA RDAP bootstrap |
| `.ferrero` | bootstrap | IANA RDAP bootstrap |
| `.fi` | bootstrap | IANA RDAP bootstrap |
| `.fidelity` | bootstrap | IANA RDAP bootstrap |
| `.fido` | bootstrap | IANA RDAP bootstrap |
| `.film` | bootstrap | IANA RDAP bootstrap |
| `.final` | bootstrap | IANA RDAP bootstrap |
| `.finance` | bootstrap | IANA RDAP bootstrap |
| `.financial` | bootstrap | IANA RDAP bootstrap |
| `.fire` | bootstrap | IANA RDAP bootstrap |
| `.firestone` | bootstrap | IANA RDAP bootstrap |
| `.firmdale` | bootstrap | IANA RDAP bootstrap |
| `.fish` | bootstrap | IANA RDAP bootstrap |
| `.fishing` | bootstrap | IANA RDAP bootstrap |
| `.fit` | bootstrap | IANA RDAP bootstrap |
| `.fitness` | bootstrap | IANA RDAP bootstrap |
| `.fj` | bootstrap | IANA RDAP bootstrap |
| `.fk` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.flickr` | bootstrap | IANA RDAP bootstrap |
| `.flights` | bootstrap | IANA RDAP bootstrap |
| `.flir` | bootstrap | IANA RDAP bootstrap |
| `.florist` | bootstrap | IANA RDAP bootstrap |
| `.flowers` | bootstrap | IANA RDAP bootstrap |
| `.fly` | bootstrap | IANA RDAP bootstrap |
| `.fm` | bootstrap | IANA RDAP bootstrap |
| `.fo` | bootstrap | IANA RDAP bootstrap |
| `.foo` | bootstrap | IANA RDAP bootstrap |
| `.food` | bootstrap | IANA RDAP bootstrap |
| `.football` | bootstrap | IANA RDAP bootstrap |
| `.ford` | bootstrap | IANA RDAP bootstrap |
| `.forex` | bootstrap | IANA RDAP bootstrap |
| `.forsale` | bootstrap | IANA RDAP bootstrap |
| `.forum` | bootstrap | IANA RDAP bootstrap |
| `.foundation` | bootstrap | IANA RDAP bootstrap |
| `.fox` | bootstrap | IANA RDAP bootstrap |
| `.fr` | bootstrap | IANA RDAP bootstrap |
| `.free` | bootstrap | IANA RDAP bootstrap |
| `.fresenius` | bootstrap | IANA RDAP bootstrap |
| `.frl` | bootstrap | IANA RDAP bootstrap |
| `.frogans` | bootstrap | IANA RDAP bootstrap |
| `.frontier` | bootstrap | IANA RDAP bootstrap |
| `.ftr` | bootstrap | IANA RDAP bootstrap |
| `.fujitsu` | bootstrap | IANA RDAP bootstrap |
| `.fun` | bootstrap | IANA RDAP bootstrap |
| `.fund` | bootstrap | IANA RDAP bootstrap |
| `.furniture` | bootstrap | IANA RDAP bootstrap |
| `.futbol` | bootstrap | IANA RDAP bootstrap |
| `.fyi` | bootstrap | IANA RDAP bootstrap |
| `.ga` | supplement | https://rdap.nic.ga — nic.ga |
| `.gal` | bootstrap | IANA RDAP bootstrap |
| `.gallery` | bootstrap | IANA RDAP bootstrap |
| `.gallo` | bootstrap | IANA RDAP bootstrap |
| `.gallup` | bootstrap | IANA RDAP bootstrap |
| `.game` | bootstrap | IANA RDAP bootstrap |
| `.games` | bootstrap | IANA RDAP bootstrap |
| `.gap` | bootstrap | IANA RDAP bootstrap |
| `.garden` | bootstrap | IANA RDAP bootstrap |
| `.gay` | bootstrap | IANA RDAP bootstrap |
| `.gb` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.gbiz` | bootstrap | IANA RDAP bootstrap |
| `.gd` | bootstrap | IANA RDAP bootstrap |
| `.gdn` | bootstrap | IANA RDAP bootstrap |
| `.ge` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.gea` | bootstrap | IANA RDAP bootstrap |
| `.gent` | bootstrap | IANA RDAP bootstrap |
| `.genting` | bootstrap | IANA RDAP bootstrap |
| `.george` | bootstrap | IANA RDAP bootstrap |
| `.gf` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.gg` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ggee` | bootstrap | IANA RDAP bootstrap |
| `.gh` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.gi` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.gift` | bootstrap | IANA RDAP bootstrap |
| `.gifts` | bootstrap | IANA RDAP bootstrap |
| `.gives` | bootstrap | IANA RDAP bootstrap |
| `.giving` | bootstrap | IANA RDAP bootstrap |
| `.gl` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.glass` | bootstrap | IANA RDAP bootstrap |
| `.gle` | bootstrap | IANA RDAP bootstrap |
| `.global` | bootstrap | IANA RDAP bootstrap |
| `.globo` | bootstrap | IANA RDAP bootstrap |
| `.gm` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.gmail` | bootstrap | IANA RDAP bootstrap |
| `.gmbh` | bootstrap | IANA RDAP bootstrap |
| `.gmo` | bootstrap | IANA RDAP bootstrap |
| `.gmx` | bootstrap | IANA RDAP bootstrap |
| `.gn` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.godaddy` | bootstrap | IANA RDAP bootstrap |
| `.gold` | bootstrap | IANA RDAP bootstrap |
| `.goldpoint` | bootstrap | IANA RDAP bootstrap |
| `.golf` | bootstrap | IANA RDAP bootstrap |
| `.goodyear` | bootstrap | IANA RDAP bootstrap |
| `.goog` | bootstrap | IANA RDAP bootstrap |
| `.google` | bootstrap | IANA RDAP bootstrap |
| `.gop` | bootstrap | IANA RDAP bootstrap |
| `.got` | bootstrap | IANA RDAP bootstrap |
| `.gov` | bootstrap | IANA RDAP bootstrap |
| `.gp` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.gq` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.gr` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.grainger` | bootstrap | IANA RDAP bootstrap |
| `.graphics` | bootstrap | IANA RDAP bootstrap |
| `.gratis` | bootstrap | IANA RDAP bootstrap |
| `.green` | bootstrap | IANA RDAP bootstrap |
| `.gripe` | bootstrap | IANA RDAP bootstrap |
| `.grocery` | bootstrap | IANA RDAP bootstrap |
| `.group` | bootstrap | IANA RDAP bootstrap |
| `.gs` | bootstrap | IANA RDAP bootstrap |
| `.gt` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.gu` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.gucci` | bootstrap | IANA RDAP bootstrap |
| `.guge` | bootstrap | IANA RDAP bootstrap |
| `.guide` | bootstrap | IANA RDAP bootstrap |
| `.guitars` | bootstrap | IANA RDAP bootstrap |
| `.guru` | bootstrap | IANA RDAP bootstrap |
| `.gw` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.gy` | bootstrap | IANA RDAP bootstrap |
| `.hair` | bootstrap | IANA RDAP bootstrap |
| `.hamburg` | bootstrap | IANA RDAP bootstrap |
| `.hangout` | bootstrap | IANA RDAP bootstrap |
| `.haus` | bootstrap | IANA RDAP bootstrap |
| `.hbo` | bootstrap | IANA RDAP bootstrap |
| `.hdfc` | bootstrap | IANA RDAP bootstrap |
| `.hdfcbank` | bootstrap | IANA RDAP bootstrap |
| `.health` | bootstrap | IANA RDAP bootstrap |
| `.healthcare` | bootstrap | IANA RDAP bootstrap |
| `.help` | bootstrap | IANA RDAP bootstrap |
| `.helsinki` | bootstrap | IANA RDAP bootstrap |
| `.here` | bootstrap | IANA RDAP bootstrap |
| `.hermes` | bootstrap | IANA RDAP bootstrap |
| `.hiphop` | bootstrap | IANA RDAP bootstrap |
| `.hisamitsu` | bootstrap | IANA RDAP bootstrap |
| `.hitachi` | bootstrap | IANA RDAP bootstrap |
| `.hiv` | bootstrap | IANA RDAP bootstrap |
| `.hk` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.hkt` | bootstrap | IANA RDAP bootstrap |
| `.hm` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.hn` | bootstrap | IANA RDAP bootstrap |
| `.hockey` | bootstrap | IANA RDAP bootstrap |
| `.holdings` | bootstrap | IANA RDAP bootstrap |
| `.holiday` | bootstrap | IANA RDAP bootstrap |
| `.homedepot` | bootstrap | IANA RDAP bootstrap |
| `.homegoods` | bootstrap | IANA RDAP bootstrap |
| `.homes` | bootstrap | IANA RDAP bootstrap |
| `.homesense` | bootstrap | IANA RDAP bootstrap |
| `.honda` | bootstrap | IANA RDAP bootstrap |
| `.horse` | bootstrap | IANA RDAP bootstrap |
| `.hospital` | bootstrap | IANA RDAP bootstrap |
| `.host` | bootstrap | IANA RDAP bootstrap |
| `.hosting` | bootstrap | IANA RDAP bootstrap |
| `.hot` | bootstrap | IANA RDAP bootstrap |
| `.hotels` | bootstrap | IANA RDAP bootstrap |
| `.hotmail` | bootstrap | IANA RDAP bootstrap |
| `.house` | bootstrap | IANA RDAP bootstrap |
| `.how` | bootstrap | IANA RDAP bootstrap |
| `.hr` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.hsbc` | bootstrap | IANA RDAP bootstrap |
| `.ht` | bootstrap | IANA RDAP bootstrap |
| `.hu` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.hughes` | bootstrap | IANA RDAP bootstrap |
| `.hyatt` | bootstrap | IANA RDAP bootstrap |
| `.hyundai` | bootstrap | IANA RDAP bootstrap |
| `.ibm` | bootstrap | IANA RDAP bootstrap |
| `.icbc` | bootstrap | IANA RDAP bootstrap |
| `.ice` | bootstrap | IANA RDAP bootstrap |
| `.icu` | bootstrap | IANA RDAP bootstrap |
| `.id` | bootstrap | IANA RDAP bootstrap |
| `.ie` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ieee` | bootstrap | IANA RDAP bootstrap |
| `.ifm` | bootstrap | IANA RDAP bootstrap |
| `.ikano` | bootstrap | IANA RDAP bootstrap |
| `.il` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.im` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.imamat` | bootstrap | IANA RDAP bootstrap |
| `.imdb` | bootstrap | IANA RDAP bootstrap |
| `.immo` | bootstrap | IANA RDAP bootstrap |
| `.immobilien` | bootstrap | IANA RDAP bootstrap |
| `.in` | bootstrap | IANA RDAP bootstrap |
| `.inc` | bootstrap | IANA RDAP bootstrap |
| `.industries` | bootstrap | IANA RDAP bootstrap |
| `.infiniti` | bootstrap | IANA RDAP bootstrap |
| `.info` | bootstrap | IANA RDAP bootstrap |
| `.ing` | bootstrap | IANA RDAP bootstrap |
| `.ink` | bootstrap | IANA RDAP bootstrap |
| `.institute` | bootstrap | IANA RDAP bootstrap |
| `.insurance` | bootstrap | IANA RDAP bootstrap |
| `.insure` | bootstrap | IANA RDAP bootstrap |
| `.int` | bootstrap | IANA RDAP bootstrap |
| `.international` | bootstrap | IANA RDAP bootstrap |
| `.intuit` | bootstrap | IANA RDAP bootstrap |
| `.investments` | bootstrap | IANA RDAP bootstrap |
| `.io` | supplement | https://rdap.identitydigital.services/rdap — Identity Digital |
| `.ipiranga` | bootstrap | IANA RDAP bootstrap |
| `.iq` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ir` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.irish` | bootstrap | IANA RDAP bootstrap |
| `.is` | bootstrap | IANA RDAP bootstrap |
| `.ismaili` | bootstrap | IANA RDAP bootstrap |
| `.ist` | bootstrap | IANA RDAP bootstrap |
| `.istanbul` | bootstrap | IANA RDAP bootstrap |
| `.it` | none | Registro.it exposes only a *pubtest* RDAP endpoint; no verified production server |
| `.itau` | bootstrap | IANA RDAP bootstrap |
| `.itv` | bootstrap | IANA RDAP bootstrap |
| `.jaguar` | bootstrap | IANA RDAP bootstrap |
| `.java` | bootstrap | IANA RDAP bootstrap |
| `.jcb` | bootstrap | IANA RDAP bootstrap |
| `.je` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.jeep` | bootstrap | IANA RDAP bootstrap |
| `.jetzt` | bootstrap | IANA RDAP bootstrap |
| `.jewelry` | bootstrap | IANA RDAP bootstrap |
| `.jio` | bootstrap | IANA RDAP bootstrap |
| `.jll` | bootstrap | IANA RDAP bootstrap |
| `.jm` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.jmp` | bootstrap | IANA RDAP bootstrap |
| `.jnj` | bootstrap | IANA RDAP bootstrap |
| `.jo` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.jobs` | bootstrap | IANA RDAP bootstrap |
| `.joburg` | bootstrap | IANA RDAP bootstrap |
| `.jot` | bootstrap | IANA RDAP bootstrap |
| `.joy` | bootstrap | IANA RDAP bootstrap |
| `.jp` | none | JPRS RDAP is gTLD-only; .jp is WHOIS-only |
| `.jpmorgan` | bootstrap | IANA RDAP bootstrap |
| `.jprs` | bootstrap | IANA RDAP bootstrap |
| `.juegos` | bootstrap | IANA RDAP bootstrap |
| `.juniper` | bootstrap | IANA RDAP bootstrap |
| `.kaufen` | bootstrap | IANA RDAP bootstrap |
| `.kddi` | bootstrap | IANA RDAP bootstrap |
| `.ke` | bootstrap | IANA RDAP bootstrap |
| `.kerryhotels` | bootstrap | IANA RDAP bootstrap |
| `.kerryproperties` | bootstrap | IANA RDAP bootstrap |
| `.kfh` | bootstrap | IANA RDAP bootstrap |
| `.kg` | bootstrap | IANA RDAP bootstrap |
| `.kh` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ki` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.kia` | bootstrap | IANA RDAP bootstrap |
| `.kids` | bootstrap | IANA RDAP bootstrap |
| `.kim` | bootstrap | IANA RDAP bootstrap |
| `.kindle` | bootstrap | IANA RDAP bootstrap |
| `.kitchen` | bootstrap | IANA RDAP bootstrap |
| `.kiwi` | bootstrap | IANA RDAP bootstrap |
| `.km` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.kn` | supplement | https://rdap.nic.kn — nic.kn |
| `.koeln` | bootstrap | IANA RDAP bootstrap |
| `.komatsu` | bootstrap | IANA RDAP bootstrap |
| `.kosher` | bootstrap | IANA RDAP bootstrap |
| `.kp` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.kpmg` | bootstrap | IANA RDAP bootstrap |
| `.kpn` | bootstrap | IANA RDAP bootstrap |
| `.kr` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.krd` | bootstrap | IANA RDAP bootstrap |
| `.kred` | bootstrap | IANA RDAP bootstrap |
| `.kuokgroup` | bootstrap | IANA RDAP bootstrap |
| `.kw` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ky` | bootstrap | IANA RDAP bootstrap |
| `.kyoto` | bootstrap | IANA RDAP bootstrap |
| `.kz` | supplement | https://rdap.nic.kz — nic.kz |
| `.la` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.lacaixa` | bootstrap | IANA RDAP bootstrap |
| `.lamborghini` | bootstrap | IANA RDAP bootstrap |
| `.lamer` | bootstrap | IANA RDAP bootstrap |
| `.land` | bootstrap | IANA RDAP bootstrap |
| `.landrover` | bootstrap | IANA RDAP bootstrap |
| `.lanxess` | bootstrap | IANA RDAP bootstrap |
| `.lasalle` | bootstrap | IANA RDAP bootstrap |
| `.lat` | bootstrap | IANA RDAP bootstrap |
| `.latino` | bootstrap | IANA RDAP bootstrap |
| `.latrobe` | bootstrap | IANA RDAP bootstrap |
| `.law` | bootstrap | IANA RDAP bootstrap |
| `.lawyer` | bootstrap | IANA RDAP bootstrap |
| `.lb` | bootstrap | IANA RDAP bootstrap |
| `.lc` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.lds` | bootstrap | IANA RDAP bootstrap |
| `.lease` | bootstrap | IANA RDAP bootstrap |
| `.leclerc` | bootstrap | IANA RDAP bootstrap |
| `.lefrak` | bootstrap | IANA RDAP bootstrap |
| `.legal` | bootstrap | IANA RDAP bootstrap |
| `.lego` | bootstrap | IANA RDAP bootstrap |
| `.lexus` | bootstrap | IANA RDAP bootstrap |
| `.lgbt` | bootstrap | IANA RDAP bootstrap |
| `.li` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.lidl` | bootstrap | IANA RDAP bootstrap |
| `.life` | bootstrap | IANA RDAP bootstrap |
| `.lifeinsurance` | bootstrap | IANA RDAP bootstrap |
| `.lifestyle` | bootstrap | IANA RDAP bootstrap |
| `.lighting` | bootstrap | IANA RDAP bootstrap |
| `.like` | bootstrap | IANA RDAP bootstrap |
| `.lilly` | bootstrap | IANA RDAP bootstrap |
| `.limited` | bootstrap | IANA RDAP bootstrap |
| `.limo` | bootstrap | IANA RDAP bootstrap |
| `.lincoln` | bootstrap | IANA RDAP bootstrap |
| `.link` | bootstrap | IANA RDAP bootstrap |
| `.live` | bootstrap | IANA RDAP bootstrap |
| `.living` | bootstrap | IANA RDAP bootstrap |
| `.lk` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.llc` | bootstrap | IANA RDAP bootstrap |
| `.llp` | bootstrap | IANA RDAP bootstrap |
| `.loan` | bootstrap | IANA RDAP bootstrap |
| `.loans` | bootstrap | IANA RDAP bootstrap |
| `.locker` | bootstrap | IANA RDAP bootstrap |
| `.locus` | bootstrap | IANA RDAP bootstrap |
| `.lol` | bootstrap | IANA RDAP bootstrap |
| `.london` | bootstrap | IANA RDAP bootstrap |
| `.lotte` | bootstrap | IANA RDAP bootstrap |
| `.lotto` | bootstrap | IANA RDAP bootstrap |
| `.love` | bootstrap | IANA RDAP bootstrap |
| `.lpl` | bootstrap | IANA RDAP bootstrap |
| `.lplfinancial` | bootstrap | IANA RDAP bootstrap |
| `.lr` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ls` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.lt` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ltd` | bootstrap | IANA RDAP bootstrap |
| `.ltda` | bootstrap | IANA RDAP bootstrap |
| `.lu` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.lundbeck` | bootstrap | IANA RDAP bootstrap |
| `.luxe` | bootstrap | IANA RDAP bootstrap |
| `.luxury` | bootstrap | IANA RDAP bootstrap |
| `.lv` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ly` | bootstrap | IANA RDAP bootstrap |
| `.ma` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.madrid` | bootstrap | IANA RDAP bootstrap |
| `.maif` | bootstrap | IANA RDAP bootstrap |
| `.maison` | bootstrap | IANA RDAP bootstrap |
| `.makeup` | bootstrap | IANA RDAP bootstrap |
| `.man` | bootstrap | IANA RDAP bootstrap |
| `.management` | bootstrap | IANA RDAP bootstrap |
| `.mango` | bootstrap | IANA RDAP bootstrap |
| `.map` | bootstrap | IANA RDAP bootstrap |
| `.market` | bootstrap | IANA RDAP bootstrap |
| `.marketing` | bootstrap | IANA RDAP bootstrap |
| `.markets` | bootstrap | IANA RDAP bootstrap |
| `.marriott` | bootstrap | IANA RDAP bootstrap |
| `.marshalls` | bootstrap | IANA RDAP bootstrap |
| `.mattel` | bootstrap | IANA RDAP bootstrap |
| `.mba` | bootstrap | IANA RDAP bootstrap |
| `.mc` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.mckinsey` | bootstrap | IANA RDAP bootstrap |
| `.md` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.me` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.med` | bootstrap | IANA RDAP bootstrap |
| `.media` | bootstrap | IANA RDAP bootstrap |
| `.meet` | bootstrap | IANA RDAP bootstrap |
| `.melbourne` | bootstrap | IANA RDAP bootstrap |
| `.meme` | bootstrap | IANA RDAP bootstrap |
| `.memorial` | bootstrap | IANA RDAP bootstrap |
| `.men` | bootstrap | IANA RDAP bootstrap |
| `.menu` | bootstrap | IANA RDAP bootstrap |
| `.merck` | bootstrap | IANA RDAP bootstrap |
| `.merckmsd` | bootstrap | IANA RDAP bootstrap |
| `.mg` | bootstrap | IANA RDAP bootstrap |
| `.mh` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.miami` | bootstrap | IANA RDAP bootstrap |
| `.microsoft` | bootstrap | IANA RDAP bootstrap |
| `.mil` | none | US DoD — not publicly queryable |
| `.mini` | bootstrap | IANA RDAP bootstrap |
| `.mint` | bootstrap | IANA RDAP bootstrap |
| `.mit` | bootstrap | IANA RDAP bootstrap |
| `.mitsubishi` | bootstrap | IANA RDAP bootstrap |
| `.mk` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ml` | bootstrap | IANA RDAP bootstrap |
| `.mlb` | bootstrap | IANA RDAP bootstrap |
| `.mls` | bootstrap | IANA RDAP bootstrap |
| `.mm` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.mma` | bootstrap | IANA RDAP bootstrap |
| `.mn` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.mo` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.mobi` | bootstrap | IANA RDAP bootstrap |
| `.mobile` | bootstrap | IANA RDAP bootstrap |
| `.moda` | bootstrap | IANA RDAP bootstrap |
| `.moe` | bootstrap | IANA RDAP bootstrap |
| `.moi` | bootstrap | IANA RDAP bootstrap |
| `.mom` | bootstrap | IANA RDAP bootstrap |
| `.monash` | bootstrap | IANA RDAP bootstrap |
| `.money` | bootstrap | IANA RDAP bootstrap |
| `.monster` | bootstrap | IANA RDAP bootstrap |
| `.mormon` | bootstrap | IANA RDAP bootstrap |
| `.mortgage` | bootstrap | IANA RDAP bootstrap |
| `.moscow` | bootstrap | IANA RDAP bootstrap |
| `.moto` | bootstrap | IANA RDAP bootstrap |
| `.motorcycles` | bootstrap | IANA RDAP bootstrap |
| `.mov` | bootstrap | IANA RDAP bootstrap |
| `.movie` | bootstrap | IANA RDAP bootstrap |
| `.mp` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.mq` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.mr` | supplement | https://rdap.nic.mr — nic.mr |
| `.ms` | bootstrap | IANA RDAP bootstrap |
| `.msd` | bootstrap | IANA RDAP bootstrap |
| `.mt` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.mtn` | bootstrap | IANA RDAP bootstrap |
| `.mtr` | bootstrap | IANA RDAP bootstrap |
| `.mu` | bootstrap | IANA RDAP bootstrap |
| `.museum` | bootstrap | IANA RDAP bootstrap |
| `.music` | bootstrap | IANA RDAP bootstrap |
| `.mv` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.mw` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.mx` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.my` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.mz` | supplement | https://rdap.nic.mz — nic.mz |
| `.na` | bootstrap | IANA RDAP bootstrap |
| `.nab` | bootstrap | IANA RDAP bootstrap |
| `.nagoya` | bootstrap | IANA RDAP bootstrap |
| `.name` | bootstrap | IANA RDAP bootstrap |
| `.navy` | bootstrap | IANA RDAP bootstrap |
| `.nba` | bootstrap | IANA RDAP bootstrap |
| `.nc` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ne` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.nec` | bootstrap | IANA RDAP bootstrap |
| `.net` | bootstrap | IANA RDAP bootstrap |
| `.netbank` | bootstrap | IANA RDAP bootstrap |
| `.netflix` | bootstrap | IANA RDAP bootstrap |
| `.network` | bootstrap | IANA RDAP bootstrap |
| `.neustar` | bootstrap | IANA RDAP bootstrap |
| `.new` | bootstrap | IANA RDAP bootstrap |
| `.news` | bootstrap | IANA RDAP bootstrap |
| `.next` | bootstrap | IANA RDAP bootstrap |
| `.nextdirect` | bootstrap | IANA RDAP bootstrap |
| `.nexus` | bootstrap | IANA RDAP bootstrap |
| `.nf` | bootstrap | IANA RDAP bootstrap |
| `.nfl` | bootstrap | IANA RDAP bootstrap |
| `.ng` | bootstrap | IANA RDAP bootstrap |
| `.ngo` | bootstrap | IANA RDAP bootstrap |
| `.nhk` | bootstrap | IANA RDAP bootstrap |
| `.ni` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.nico` | bootstrap | IANA RDAP bootstrap |
| `.nike` | bootstrap | IANA RDAP bootstrap |
| `.nikon` | bootstrap | IANA RDAP bootstrap |
| `.ninja` | bootstrap | IANA RDAP bootstrap |
| `.nissan` | bootstrap | IANA RDAP bootstrap |
| `.nissay` | bootstrap | IANA RDAP bootstrap |
| `.nl` | bootstrap | IANA RDAP bootstrap |
| `.no` | bootstrap | IANA RDAP bootstrap |
| `.nokia` | bootstrap | IANA RDAP bootstrap |
| `.norton` | bootstrap | IANA RDAP bootstrap |
| `.now` | bootstrap | IANA RDAP bootstrap |
| `.nowruz` | bootstrap | IANA RDAP bootstrap |
| `.nowtv` | bootstrap | IANA RDAP bootstrap |
| `.np` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.nr` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.nra` | bootstrap | IANA RDAP bootstrap |
| `.nrw` | bootstrap | IANA RDAP bootstrap |
| `.ntt` | bootstrap | IANA RDAP bootstrap |
| `.nu` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.nyc` | bootstrap | IANA RDAP bootstrap |
| `.nz` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.obi` | bootstrap | IANA RDAP bootstrap |
| `.observer` | bootstrap | IANA RDAP bootstrap |
| `.office` | bootstrap | IANA RDAP bootstrap |
| `.okinawa` | bootstrap | IANA RDAP bootstrap |
| `.olayan` | bootstrap | IANA RDAP bootstrap |
| `.olayangroup` | bootstrap | IANA RDAP bootstrap |
| `.ollo` | bootstrap | IANA RDAP bootstrap |
| `.om` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.omega` | bootstrap | IANA RDAP bootstrap |
| `.one` | bootstrap | IANA RDAP bootstrap |
| `.ong` | bootstrap | IANA RDAP bootstrap |
| `.onl` | bootstrap | IANA RDAP bootstrap |
| `.online` | bootstrap | IANA RDAP bootstrap |
| `.ooo` | bootstrap | IANA RDAP bootstrap |
| `.open` | bootstrap | IANA RDAP bootstrap |
| `.oracle` | bootstrap | IANA RDAP bootstrap |
| `.orange` | bootstrap | IANA RDAP bootstrap |
| `.org` | bootstrap | IANA RDAP bootstrap |
| `.organic` | bootstrap | IANA RDAP bootstrap |
| `.origins` | bootstrap | IANA RDAP bootstrap |
| `.osaka` | bootstrap | IANA RDAP bootstrap |
| `.otsuka` | bootstrap | IANA RDAP bootstrap |
| `.ott` | bootstrap | IANA RDAP bootstrap |
| `.ovh` | bootstrap | IANA RDAP bootstrap |
| `.pa` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.page` | bootstrap | IANA RDAP bootstrap |
| `.panasonic` | bootstrap | IANA RDAP bootstrap |
| `.paris` | bootstrap | IANA RDAP bootstrap |
| `.pars` | bootstrap | IANA RDAP bootstrap |
| `.partners` | bootstrap | IANA RDAP bootstrap |
| `.parts` | bootstrap | IANA RDAP bootstrap |
| `.party` | bootstrap | IANA RDAP bootstrap |
| `.pay` | bootstrap | IANA RDAP bootstrap |
| `.pccw` | bootstrap | IANA RDAP bootstrap |
| `.pe` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.pet` | bootstrap | IANA RDAP bootstrap |
| `.pf` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.pfizer` | bootstrap | IANA RDAP bootstrap |
| `.pg` | bootstrap | IANA RDAP bootstrap |
| `.ph` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.pharmacy` | bootstrap | IANA RDAP bootstrap |
| `.phd` | bootstrap | IANA RDAP bootstrap |
| `.philips` | bootstrap | IANA RDAP bootstrap |
| `.phone` | bootstrap | IANA RDAP bootstrap |
| `.photo` | bootstrap | IANA RDAP bootstrap |
| `.photography` | bootstrap | IANA RDAP bootstrap |
| `.photos` | bootstrap | IANA RDAP bootstrap |
| `.physio` | bootstrap | IANA RDAP bootstrap |
| `.pics` | bootstrap | IANA RDAP bootstrap |
| `.pictet` | bootstrap | IANA RDAP bootstrap |
| `.pictures` | bootstrap | IANA RDAP bootstrap |
| `.pid` | bootstrap | IANA RDAP bootstrap |
| `.pin` | bootstrap | IANA RDAP bootstrap |
| `.ping` | bootstrap | IANA RDAP bootstrap |
| `.pink` | bootstrap | IANA RDAP bootstrap |
| `.pioneer` | bootstrap | IANA RDAP bootstrap |
| `.pizza` | bootstrap | IANA RDAP bootstrap |
| `.pk` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.pl` | bootstrap | IANA RDAP bootstrap |
| `.place` | bootstrap | IANA RDAP bootstrap |
| `.play` | bootstrap | IANA RDAP bootstrap |
| `.playstation` | bootstrap | IANA RDAP bootstrap |
| `.plumbing` | bootstrap | IANA RDAP bootstrap |
| `.plus` | bootstrap | IANA RDAP bootstrap |
| `.pm` | bootstrap | IANA RDAP bootstrap |
| `.pn` | bootstrap | IANA RDAP bootstrap |
| `.pnc` | bootstrap | IANA RDAP bootstrap |
| `.pohl` | bootstrap | IANA RDAP bootstrap |
| `.poker` | bootstrap | IANA RDAP bootstrap |
| `.politie` | bootstrap | IANA RDAP bootstrap |
| `.porn` | bootstrap | IANA RDAP bootstrap |
| `.post` | bootstrap | IANA RDAP bootstrap |
| `.pr` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.praxi` | bootstrap | IANA RDAP bootstrap |
| `.press` | bootstrap | IANA RDAP bootstrap |
| `.prime` | bootstrap | IANA RDAP bootstrap |
| `.pro` | bootstrap | IANA RDAP bootstrap |
| `.prod` | bootstrap | IANA RDAP bootstrap |
| `.productions` | bootstrap | IANA RDAP bootstrap |
| `.prof` | bootstrap | IANA RDAP bootstrap |
| `.progressive` | bootstrap | IANA RDAP bootstrap |
| `.promo` | bootstrap | IANA RDAP bootstrap |
| `.properties` | bootstrap | IANA RDAP bootstrap |
| `.property` | bootstrap | IANA RDAP bootstrap |
| `.protection` | bootstrap | IANA RDAP bootstrap |
| `.pru` | bootstrap | IANA RDAP bootstrap |
| `.prudential` | bootstrap | IANA RDAP bootstrap |
| `.ps` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.pt` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.pub` | bootstrap | IANA RDAP bootstrap |
| `.pw` | bootstrap | IANA RDAP bootstrap |
| `.pwc` | bootstrap | IANA RDAP bootstrap |
| `.py` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.qa` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.qpon` | bootstrap | IANA RDAP bootstrap |
| `.quebec` | bootstrap | IANA RDAP bootstrap |
| `.quest` | bootstrap | IANA RDAP bootstrap |
| `.racing` | bootstrap | IANA RDAP bootstrap |
| `.radio` | bootstrap | IANA RDAP bootstrap |
| `.re` | bootstrap | IANA RDAP bootstrap |
| `.read` | bootstrap | IANA RDAP bootstrap |
| `.realestate` | bootstrap | IANA RDAP bootstrap |
| `.realtor` | bootstrap | IANA RDAP bootstrap |
| `.realty` | bootstrap | IANA RDAP bootstrap |
| `.recipes` | bootstrap | IANA RDAP bootstrap |
| `.red` | bootstrap | IANA RDAP bootstrap |
| `.redumbrella` | bootstrap | IANA RDAP bootstrap |
| `.rehab` | bootstrap | IANA RDAP bootstrap |
| `.reise` | bootstrap | IANA RDAP bootstrap |
| `.reisen` | bootstrap | IANA RDAP bootstrap |
| `.reit` | bootstrap | IANA RDAP bootstrap |
| `.reliance` | bootstrap | IANA RDAP bootstrap |
| `.ren` | bootstrap | IANA RDAP bootstrap |
| `.rent` | bootstrap | IANA RDAP bootstrap |
| `.rentals` | bootstrap | IANA RDAP bootstrap |
| `.repair` | bootstrap | IANA RDAP bootstrap |
| `.report` | bootstrap | IANA RDAP bootstrap |
| `.republican` | bootstrap | IANA RDAP bootstrap |
| `.rest` | bootstrap | IANA RDAP bootstrap |
| `.restaurant` | bootstrap | IANA RDAP bootstrap |
| `.review` | bootstrap | IANA RDAP bootstrap |
| `.reviews` | bootstrap | IANA RDAP bootstrap |
| `.rexroth` | bootstrap | IANA RDAP bootstrap |
| `.rich` | bootstrap | IANA RDAP bootstrap |
| `.richardli` | bootstrap | IANA RDAP bootstrap |
| `.ricoh` | bootstrap | IANA RDAP bootstrap |
| `.ril` | bootstrap | IANA RDAP bootstrap |
| `.rio` | bootstrap | IANA RDAP bootstrap |
| `.rip` | bootstrap | IANA RDAP bootstrap |
| `.ro` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.rocks` | bootstrap | IANA RDAP bootstrap |
| `.rodeo` | bootstrap | IANA RDAP bootstrap |
| `.rogers` | bootstrap | IANA RDAP bootstrap |
| `.room` | bootstrap | IANA RDAP bootstrap |
| `.rs` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.rsvp` | bootstrap | IANA RDAP bootstrap |
| `.ru` | none | TCI RDAP host exists but 404'd a known-registered domain — unverified, not added |
| `.rugby` | bootstrap | IANA RDAP bootstrap |
| `.ruhr` | bootstrap | IANA RDAP bootstrap |
| `.run` | bootstrap | IANA RDAP bootstrap |
| `.rw` | bootstrap | IANA RDAP bootstrap |
| `.rwe` | bootstrap | IANA RDAP bootstrap |
| `.ryukyu` | bootstrap | IANA RDAP bootstrap |
| `.sa` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.saarland` | bootstrap | IANA RDAP bootstrap |
| `.safe` | bootstrap | IANA RDAP bootstrap |
| `.safety` | bootstrap | IANA RDAP bootstrap |
| `.sakura` | bootstrap | IANA RDAP bootstrap |
| `.sale` | bootstrap | IANA RDAP bootstrap |
| `.salon` | bootstrap | IANA RDAP bootstrap |
| `.samsclub` | bootstrap | IANA RDAP bootstrap |
| `.samsung` | bootstrap | IANA RDAP bootstrap |
| `.sandvik` | bootstrap | IANA RDAP bootstrap |
| `.sandvikcoromant` | bootstrap | IANA RDAP bootstrap |
| `.sanofi` | bootstrap | IANA RDAP bootstrap |
| `.sap` | bootstrap | IANA RDAP bootstrap |
| `.sarl` | bootstrap | IANA RDAP bootstrap |
| `.sas` | bootstrap | IANA RDAP bootstrap |
| `.save` | bootstrap | IANA RDAP bootstrap |
| `.saxo` | bootstrap | IANA RDAP bootstrap |
| `.sb` | supplement | https://rdap.nic.sb — nic.sb |
| `.sbi` | bootstrap | IANA RDAP bootstrap |
| `.sbs` | bootstrap | IANA RDAP bootstrap |
| `.sc` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.scb` | bootstrap | IANA RDAP bootstrap |
| `.schaeffler` | bootstrap | IANA RDAP bootstrap |
| `.schmidt` | bootstrap | IANA RDAP bootstrap |
| `.scholarships` | bootstrap | IANA RDAP bootstrap |
| `.school` | bootstrap | IANA RDAP bootstrap |
| `.schule` | bootstrap | IANA RDAP bootstrap |
| `.schwarz` | bootstrap | IANA RDAP bootstrap |
| `.science` | bootstrap | IANA RDAP bootstrap |
| `.scot` | bootstrap | IANA RDAP bootstrap |
| `.sd` | bootstrap | IANA RDAP bootstrap |
| `.se` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.search` | bootstrap | IANA RDAP bootstrap |
| `.seat` | bootstrap | IANA RDAP bootstrap |
| `.secure` | bootstrap | IANA RDAP bootstrap |
| `.security` | bootstrap | IANA RDAP bootstrap |
| `.seek` | bootstrap | IANA RDAP bootstrap |
| `.select` | bootstrap | IANA RDAP bootstrap |
| `.sener` | bootstrap | IANA RDAP bootstrap |
| `.services` | bootstrap | IANA RDAP bootstrap |
| `.seven` | bootstrap | IANA RDAP bootstrap |
| `.sew` | bootstrap | IANA RDAP bootstrap |
| `.sex` | bootstrap | IANA RDAP bootstrap |
| `.sexy` | bootstrap | IANA RDAP bootstrap |
| `.sfr` | bootstrap | IANA RDAP bootstrap |
| `.sg` | bootstrap | IANA RDAP bootstrap |
| `.sh` | supplement | https://rdap.identitydigital.services/rdap — Identity Digital |
| `.shangrila` | bootstrap | IANA RDAP bootstrap |
| `.sharp` | bootstrap | IANA RDAP bootstrap |
| `.shell` | bootstrap | IANA RDAP bootstrap |
| `.shia` | bootstrap | IANA RDAP bootstrap |
| `.shiksha` | bootstrap | IANA RDAP bootstrap |
| `.shoes` | bootstrap | IANA RDAP bootstrap |
| `.shop` | bootstrap | IANA RDAP bootstrap |
| `.shopping` | bootstrap | IANA RDAP bootstrap |
| `.shouji` | bootstrap | IANA RDAP bootstrap |
| `.show` | bootstrap | IANA RDAP bootstrap |
| `.si` | bootstrap | IANA RDAP bootstrap |
| `.silk` | bootstrap | IANA RDAP bootstrap |
| `.sina` | bootstrap | IANA RDAP bootstrap |
| `.singles` | bootstrap | IANA RDAP bootstrap |
| `.site` | bootstrap | IANA RDAP bootstrap |
| `.sj` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.sk` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ski` | bootstrap | IANA RDAP bootstrap |
| `.skin` | bootstrap | IANA RDAP bootstrap |
| `.sky` | bootstrap | IANA RDAP bootstrap |
| `.skype` | bootstrap | IANA RDAP bootstrap |
| `.sl` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.sling` | bootstrap | IANA RDAP bootstrap |
| `.sm` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.smart` | bootstrap | IANA RDAP bootstrap |
| `.smile` | bootstrap | IANA RDAP bootstrap |
| `.sn` | bootstrap | IANA RDAP bootstrap |
| `.sncf` | bootstrap | IANA RDAP bootstrap |
| `.so` | supplement | https://rdap.nic.so — nic.so |
| `.soccer` | bootstrap | IANA RDAP bootstrap |
| `.social` | bootstrap | IANA RDAP bootstrap |
| `.softbank` | bootstrap | IANA RDAP bootstrap |
| `.software` | bootstrap | IANA RDAP bootstrap |
| `.sohu` | bootstrap | IANA RDAP bootstrap |
| `.solar` | bootstrap | IANA RDAP bootstrap |
| `.solutions` | bootstrap | IANA RDAP bootstrap |
| `.song` | bootstrap | IANA RDAP bootstrap |
| `.sony` | bootstrap | IANA RDAP bootstrap |
| `.soy` | bootstrap | IANA RDAP bootstrap |
| `.spa` | bootstrap | IANA RDAP bootstrap |
| `.space` | bootstrap | IANA RDAP bootstrap |
| `.sport` | bootstrap | IANA RDAP bootstrap |
| `.spot` | bootstrap | IANA RDAP bootstrap |
| `.sr` | bootstrap | IANA RDAP bootstrap |
| `.srl` | bootstrap | IANA RDAP bootstrap |
| `.ss` | bootstrap | IANA RDAP bootstrap |
| `.st` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.stada` | bootstrap | IANA RDAP bootstrap |
| `.staples` | bootstrap | IANA RDAP bootstrap |
| `.star` | bootstrap | IANA RDAP bootstrap |
| `.statebank` | bootstrap | IANA RDAP bootstrap |
| `.statefarm` | bootstrap | IANA RDAP bootstrap |
| `.stc` | bootstrap | IANA RDAP bootstrap |
| `.stcgroup` | bootstrap | IANA RDAP bootstrap |
| `.stockholm` | bootstrap | IANA RDAP bootstrap |
| `.storage` | bootstrap | IANA RDAP bootstrap |
| `.store` | bootstrap | IANA RDAP bootstrap |
| `.stream` | bootstrap | IANA RDAP bootstrap |
| `.studio` | bootstrap | IANA RDAP bootstrap |
| `.study` | bootstrap | IANA RDAP bootstrap |
| `.style` | bootstrap | IANA RDAP bootstrap |
| `.su` | none | same operator as .ru — unverified |
| `.sucks` | bootstrap | IANA RDAP bootstrap |
| `.supplies` | bootstrap | IANA RDAP bootstrap |
| `.supply` | bootstrap | IANA RDAP bootstrap |
| `.support` | bootstrap | IANA RDAP bootstrap |
| `.surf` | bootstrap | IANA RDAP bootstrap |
| `.surgery` | bootstrap | IANA RDAP bootstrap |
| `.suzuki` | bootstrap | IANA RDAP bootstrap |
| `.sv` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.swatch` | bootstrap | IANA RDAP bootstrap |
| `.swiss` | bootstrap | IANA RDAP bootstrap |
| `.sx` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.sy` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.sydney` | bootstrap | IANA RDAP bootstrap |
| `.systems` | bootstrap | IANA RDAP bootstrap |
| `.sz` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.tab` | bootstrap | IANA RDAP bootstrap |
| `.taipei` | bootstrap | IANA RDAP bootstrap |
| `.talk` | bootstrap | IANA RDAP bootstrap |
| `.taobao` | bootstrap | IANA RDAP bootstrap |
| `.target` | bootstrap | IANA RDAP bootstrap |
| `.tatamotors` | bootstrap | IANA RDAP bootstrap |
| `.tatar` | bootstrap | IANA RDAP bootstrap |
| `.tattoo` | bootstrap | IANA RDAP bootstrap |
| `.tax` | bootstrap | IANA RDAP bootstrap |
| `.taxi` | bootstrap | IANA RDAP bootstrap |
| `.tc` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.tci` | bootstrap | IANA RDAP bootstrap |
| `.td` | supplement | https://rdap.nic.td — nic.td |
| `.tdk` | bootstrap | IANA RDAP bootstrap |
| `.team` | bootstrap | IANA RDAP bootstrap |
| `.tech` | bootstrap | IANA RDAP bootstrap |
| `.technology` | bootstrap | IANA RDAP bootstrap |
| `.tel` | bootstrap | IANA RDAP bootstrap |
| `.temasek` | bootstrap | IANA RDAP bootstrap |
| `.tennis` | bootstrap | IANA RDAP bootstrap |
| `.teva` | bootstrap | IANA RDAP bootstrap |
| `.tf` | bootstrap | IANA RDAP bootstrap |
| `.tg` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.th` | bootstrap | IANA RDAP bootstrap |
| `.thd` | bootstrap | IANA RDAP bootstrap |
| `.theater` | bootstrap | IANA RDAP bootstrap |
| `.theatre` | bootstrap | IANA RDAP bootstrap |
| `.tiaa` | bootstrap | IANA RDAP bootstrap |
| `.tickets` | bootstrap | IANA RDAP bootstrap |
| `.tienda` | bootstrap | IANA RDAP bootstrap |
| `.tips` | bootstrap | IANA RDAP bootstrap |
| `.tires` | bootstrap | IANA RDAP bootstrap |
| `.tirol` | bootstrap | IANA RDAP bootstrap |
| `.tj` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.tjmaxx` | bootstrap | IANA RDAP bootstrap |
| `.tjx` | bootstrap | IANA RDAP bootstrap |
| `.tk` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.tkmaxx` | bootstrap | IANA RDAP bootstrap |
| `.tl` | supplement | https://rdap.nic.tl — nic.tl |
| `.tm` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.tmall` | bootstrap | IANA RDAP bootstrap |
| `.tn` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.to` | bootstrap | IANA RDAP bootstrap |
| `.today` | bootstrap | IANA RDAP bootstrap |
| `.tokyo` | bootstrap | IANA RDAP bootstrap |
| `.tools` | bootstrap | IANA RDAP bootstrap |
| `.top` | bootstrap | IANA RDAP bootstrap |
| `.toray` | bootstrap | IANA RDAP bootstrap |
| `.toshiba` | bootstrap | IANA RDAP bootstrap |
| `.total` | bootstrap | IANA RDAP bootstrap |
| `.tours` | bootstrap | IANA RDAP bootstrap |
| `.town` | bootstrap | IANA RDAP bootstrap |
| `.toyota` | bootstrap | IANA RDAP bootstrap |
| `.toys` | bootstrap | IANA RDAP bootstrap |
| `.tr` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.trade` | bootstrap | IANA RDAP bootstrap |
| `.trading` | bootstrap | IANA RDAP bootstrap |
| `.training` | bootstrap | IANA RDAP bootstrap |
| `.travel` | bootstrap | IANA RDAP bootstrap |
| `.travelers` | bootstrap | IANA RDAP bootstrap |
| `.travelersinsurance` | bootstrap | IANA RDAP bootstrap |
| `.trust` | bootstrap | IANA RDAP bootstrap |
| `.trv` | bootstrap | IANA RDAP bootstrap |
| `.tt` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.tube` | bootstrap | IANA RDAP bootstrap |
| `.tui` | bootstrap | IANA RDAP bootstrap |
| `.tunes` | bootstrap | IANA RDAP bootstrap |
| `.tushu` | bootstrap | IANA RDAP bootstrap |
| `.tv` | bootstrap | IANA RDAP bootstrap |
| `.tvs` | bootstrap | IANA RDAP bootstrap |
| `.tw` | bootstrap | IANA RDAP bootstrap |
| `.tz` | bootstrap | IANA RDAP bootstrap |
| `.ua` | bootstrap | IANA RDAP bootstrap |
| `.ubank` | bootstrap | IANA RDAP bootstrap |
| `.ubs` | bootstrap | IANA RDAP bootstrap |
| `.ug` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.uk` | bootstrap | IANA RDAP bootstrap |
| `.unicom` | bootstrap | IANA RDAP bootstrap |
| `.university` | bootstrap | IANA RDAP bootstrap |
| `.uno` | bootstrap | IANA RDAP bootstrap |
| `.uol` | bootstrap | IANA RDAP bootstrap |
| `.ups` | bootstrap | IANA RDAP bootstrap |
| `.us` | supplement | https://rdap.nic.us — GoDaddy Registry (nic.us) |
| `.uy` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.uz` | bootstrap | IANA RDAP bootstrap |
| `.va` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.vacations` | bootstrap | IANA RDAP bootstrap |
| `.vana` | bootstrap | IANA RDAP bootstrap |
| `.vanguard` | bootstrap | IANA RDAP bootstrap |
| `.vc` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.ve` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.vegas` | bootstrap | IANA RDAP bootstrap |
| `.ventures` | bootstrap | IANA RDAP bootstrap |
| `.verisign` | bootstrap | IANA RDAP bootstrap |
| `.versicherung` | bootstrap | IANA RDAP bootstrap |
| `.vet` | bootstrap | IANA RDAP bootstrap |
| `.vg` | bootstrap | IANA RDAP bootstrap |
| `.vi` | bootstrap | IANA RDAP bootstrap |
| `.viajes` | bootstrap | IANA RDAP bootstrap |
| `.video` | bootstrap | IANA RDAP bootstrap |
| `.vig` | bootstrap | IANA RDAP bootstrap |
| `.viking` | bootstrap | IANA RDAP bootstrap |
| `.villas` | bootstrap | IANA RDAP bootstrap |
| `.vin` | bootstrap | IANA RDAP bootstrap |
| `.vip` | bootstrap | IANA RDAP bootstrap |
| `.virgin` | bootstrap | IANA RDAP bootstrap |
| `.visa` | bootstrap | IANA RDAP bootstrap |
| `.vision` | bootstrap | IANA RDAP bootstrap |
| `.viva` | bootstrap | IANA RDAP bootstrap |
| `.vivo` | bootstrap | IANA RDAP bootstrap |
| `.vlaanderen` | bootstrap | IANA RDAP bootstrap |
| `.vn` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.vodka` | bootstrap | IANA RDAP bootstrap |
| `.volvo` | bootstrap | IANA RDAP bootstrap |
| `.vote` | bootstrap | IANA RDAP bootstrap |
| `.voting` | bootstrap | IANA RDAP bootstrap |
| `.voto` | bootstrap | IANA RDAP bootstrap |
| `.voyage` | bootstrap | IANA RDAP bootstrap |
| `.vu` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.wales` | bootstrap | IANA RDAP bootstrap |
| `.walmart` | bootstrap | IANA RDAP bootstrap |
| `.walter` | bootstrap | IANA RDAP bootstrap |
| `.wang` | bootstrap | IANA RDAP bootstrap |
| `.wanggou` | bootstrap | IANA RDAP bootstrap |
| `.watch` | bootstrap | IANA RDAP bootstrap |
| `.watches` | bootstrap | IANA RDAP bootstrap |
| `.weather` | bootstrap | IANA RDAP bootstrap |
| `.weatherchannel` | bootstrap | IANA RDAP bootstrap |
| `.web` | bootstrap | IANA RDAP bootstrap |
| `.webcam` | bootstrap | IANA RDAP bootstrap |
| `.weber` | bootstrap | IANA RDAP bootstrap |
| `.website` | bootstrap | IANA RDAP bootstrap |
| `.wed` | bootstrap | IANA RDAP bootstrap |
| `.wedding` | bootstrap | IANA RDAP bootstrap |
| `.weibo` | bootstrap | IANA RDAP bootstrap |
| `.weir` | bootstrap | IANA RDAP bootstrap |
| `.wf` | bootstrap | IANA RDAP bootstrap |
| `.whoswho` | bootstrap | IANA RDAP bootstrap |
| `.wien` | bootstrap | IANA RDAP bootstrap |
| `.wiki` | bootstrap | IANA RDAP bootstrap |
| `.williamhill` | bootstrap | IANA RDAP bootstrap |
| `.win` | bootstrap | IANA RDAP bootstrap |
| `.windows` | bootstrap | IANA RDAP bootstrap |
| `.wine` | bootstrap | IANA RDAP bootstrap |
| `.winners` | bootstrap | IANA RDAP bootstrap |
| `.wme` | bootstrap | IANA RDAP bootstrap |
| `.woodside` | bootstrap | IANA RDAP bootstrap |
| `.work` | bootstrap | IANA RDAP bootstrap |
| `.works` | bootstrap | IANA RDAP bootstrap |
| `.world` | bootstrap | IANA RDAP bootstrap |
| `.wow` | bootstrap | IANA RDAP bootstrap |
| `.ws` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.wtc` | bootstrap | IANA RDAP bootstrap |
| `.wtf` | bootstrap | IANA RDAP bootstrap |
| `.xbox` | bootstrap | IANA RDAP bootstrap |
| `.xerox` | bootstrap | IANA RDAP bootstrap |
| `.xihuan` | bootstrap | IANA RDAP bootstrap |
| `.xin` | bootstrap | IANA RDAP bootstrap |
| `.xn--11b4c3d` | bootstrap | IANA RDAP bootstrap |
| `.xn--1ck2e1b` | bootstrap | IANA RDAP bootstrap |
| `.xn--1qqw23a` | bootstrap | IANA RDAP bootstrap |
| `.xn--2scrj9c` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--30rr7y` | bootstrap | IANA RDAP bootstrap |
| `.xn--3bst00m` | bootstrap | IANA RDAP bootstrap |
| `.xn--3ds443g` | bootstrap | IANA RDAP bootstrap |
| `.xn--3e0b707e` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--3hcrj9c` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--3pxu8k` | bootstrap | IANA RDAP bootstrap |
| `.xn--42c2d9a` | bootstrap | IANA RDAP bootstrap |
| `.xn--45br5cyl` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--45brj9c` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--45q11c` | bootstrap | IANA RDAP bootstrap |
| `.xn--4dbrk0ce` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--4gbrim` | bootstrap | IANA RDAP bootstrap |
| `.xn--54b7fta0cc` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--55qw42g` | bootstrap | IANA RDAP bootstrap |
| `.xn--55qx5d` | bootstrap | IANA RDAP bootstrap |
| `.xn--5su34j936bgsg` | bootstrap | IANA RDAP bootstrap |
| `.xn--5tzm5g` | bootstrap | IANA RDAP bootstrap |
| `.xn--6frz82g` | bootstrap | IANA RDAP bootstrap |
| `.xn--6qq986b3xl` | bootstrap | IANA RDAP bootstrap |
| `.xn--80adxhks` | bootstrap | IANA RDAP bootstrap |
| `.xn--80ao21a` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--80aqecdr1a` | bootstrap | IANA RDAP bootstrap |
| `.xn--80asehdb` | bootstrap | IANA RDAP bootstrap |
| `.xn--80aswg` | bootstrap | IANA RDAP bootstrap |
| `.xn--8y0a063a` | bootstrap | IANA RDAP bootstrap |
| `.xn--90a3ac` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--90ae` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--90ais` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--9dbq2a` | bootstrap | IANA RDAP bootstrap |
| `.xn--9et52u` | bootstrap | IANA RDAP bootstrap |
| `.xn--9krt00a` | bootstrap | IANA RDAP bootstrap |
| `.xn--b4w605ferd` | bootstrap | IANA RDAP bootstrap |
| `.xn--bck1b9a5dre4c` | bootstrap | IANA RDAP bootstrap |
| `.xn--c1avg` | bootstrap | IANA RDAP bootstrap |
| `.xn--c2br7g` | bootstrap | IANA RDAP bootstrap |
| `.xn--cck2b3b` | bootstrap | IANA RDAP bootstrap |
| `.xn--cckwcxetd` | bootstrap | IANA RDAP bootstrap |
| `.xn--cg4bki` | bootstrap | IANA RDAP bootstrap |
| `.xn--clchc0ea0b2g2a9gcd` | bootstrap | IANA RDAP bootstrap |
| `.xn--czr694b` | bootstrap | IANA RDAP bootstrap |
| `.xn--czrs0t` | bootstrap | IANA RDAP bootstrap |
| `.xn--czru2d` | bootstrap | IANA RDAP bootstrap |
| `.xn--d1acj3b` | bootstrap | IANA RDAP bootstrap |
| `.xn--d1alf` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--e1a4c` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--eckvdtc9d` | bootstrap | IANA RDAP bootstrap |
| `.xn--efvy88h` | bootstrap | IANA RDAP bootstrap |
| `.xn--fct429k` | bootstrap | IANA RDAP bootstrap |
| `.xn--fhbei` | bootstrap | IANA RDAP bootstrap |
| `.xn--fiq228c5hs` | bootstrap | IANA RDAP bootstrap |
| `.xn--fiq64b` | bootstrap | IANA RDAP bootstrap |
| `.xn--fiqs8s` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--fiqz9s` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--fjq720a` | bootstrap | IANA RDAP bootstrap |
| `.xn--flw351e` | bootstrap | IANA RDAP bootstrap |
| `.xn--fpcrj9c3d` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--fzc2c9e2c` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--fzys8d69uvgm` | bootstrap | IANA RDAP bootstrap |
| `.xn--g2xx48c` | bootstrap | IANA RDAP bootstrap |
| `.xn--gckr3f0f` | bootstrap | IANA RDAP bootstrap |
| `.xn--gecrj9c` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--gk3at1e` | bootstrap | IANA RDAP bootstrap |
| `.xn--h2breg3eve` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--h2brj9c` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--h2brj9c8c` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--hxt814e` | bootstrap | IANA RDAP bootstrap |
| `.xn--i1b6b1a6a2e` | bootstrap | IANA RDAP bootstrap |
| `.xn--imr513n` | bootstrap | IANA RDAP bootstrap |
| `.xn--io0a7i` | bootstrap | IANA RDAP bootstrap |
| `.xn--j1aef` | bootstrap | IANA RDAP bootstrap |
| `.xn--j1amh` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--j6w193g` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--jlq480n2rg` | bootstrap | IANA RDAP bootstrap |
| `.xn--jvr189m` | bootstrap | IANA RDAP bootstrap |
| `.xn--kcrx77d1x4a` | bootstrap | IANA RDAP bootstrap |
| `.xn--kprw13d` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--kpry57d` | bootstrap | IANA RDAP bootstrap |
| `.xn--kput3i` | bootstrap | IANA RDAP bootstrap |
| `.xn--l1acc` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--lgbbat1ad8j` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgb9awbf` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgba3a3ejt` | bootstrap | IANA RDAP bootstrap |
| `.xn--mgba3a4f16a` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgba7c0bbn0a` | bootstrap | IANA RDAP bootstrap |
| `.xn--mgbaam7a8h` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgbab2bd` | bootstrap | IANA RDAP bootstrap |
| `.xn--mgbah1a3hjkrd` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgbai9azgqp6j` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgbayh7gpa` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgbbh1a` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgbbh1a71e` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgbc0a9azcg` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgbca7dzdo` | bootstrap | IANA RDAP bootstrap |
| `.xn--mgbcpq6gpa1a` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgberp4a5d4ar` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgbgu82a` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgbi4ecexp` | bootstrap | IANA RDAP bootstrap |
| `.xn--mgbpl2fh` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgbt3dhd` | bootstrap | IANA RDAP bootstrap |
| `.xn--mgbtx2b` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mgbx4cd0ab` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mix891f` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--mk1bu44c` | bootstrap | IANA RDAP bootstrap |
| `.xn--mxtq1m` | bootstrap | IANA RDAP bootstrap |
| `.xn--ngbc5azd` | bootstrap | IANA RDAP bootstrap |
| `.xn--ngbe9e0a` | bootstrap | IANA RDAP bootstrap |
| `.xn--ngbrx` | bootstrap | IANA RDAP bootstrap |
| `.xn--node` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--nqv7f` | bootstrap | IANA RDAP bootstrap |
| `.xn--nqv7fs00ema` | bootstrap | IANA RDAP bootstrap |
| `.xn--nyqy26a` | bootstrap | IANA RDAP bootstrap |
| `.xn--o3cw4h` | bootstrap | IANA RDAP bootstrap |
| `.xn--ogbpf8fl` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--otu796d` | bootstrap | IANA RDAP bootstrap |
| `.xn--p1acf` | bootstrap | IANA RDAP bootstrap |
| `.xn--p1ai` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--pgbs0dh` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--pssy2u` | bootstrap | IANA RDAP bootstrap |
| `.xn--q7ce6a` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--q9jyb4c` | bootstrap | IANA RDAP bootstrap |
| `.xn--qcka1pmc` | bootstrap | IANA RDAP bootstrap |
| `.xn--qxa6a` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--qxam` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--rhqv96g` | bootstrap | IANA RDAP bootstrap |
| `.xn--rovu88b` | bootstrap | IANA RDAP bootstrap |
| `.xn--rvc1e0am3e` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--s9brj9c` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--ses554g` | bootstrap | IANA RDAP bootstrap |
| `.xn--t60b56a` | bootstrap | IANA RDAP bootstrap |
| `.xn--tckwe` | bootstrap | IANA RDAP bootstrap |
| `.xn--tiq49xqyj` | bootstrap | IANA RDAP bootstrap |
| `.xn--unup4y` | bootstrap | IANA RDAP bootstrap |
| `.xn--vermgensberater-ctb` | bootstrap | IANA RDAP bootstrap |
| `.xn--vermgensberatung-pwb` | bootstrap | IANA RDAP bootstrap |
| `.xn--vhquv` | bootstrap | IANA RDAP bootstrap |
| `.xn--vuq861b` | bootstrap | IANA RDAP bootstrap |
| `.xn--w4r85el8fhu5dnra` | bootstrap | IANA RDAP bootstrap |
| `.xn--w4rs40l` | bootstrap | IANA RDAP bootstrap |
| `.xn--wgbh1c` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--wgbl6a` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--xhq521b` | bootstrap | IANA RDAP bootstrap |
| `.xn--xkc2al3hye2a` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--xkc2dl3a5ee0h` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--y9a3aq` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--yfro4i67o` | bootstrap | IANA RDAP bootstrap |
| `.xn--ygbi2ammx` | none | IDN ccTLD — no public RDAP in bootstrap/supplement |
| `.xn--zfr164b` | bootstrap | IANA RDAP bootstrap |
| `.xxx` | bootstrap | IANA RDAP bootstrap |
| `.xyz` | bootstrap | IANA RDAP bootstrap |
| `.yachts` | bootstrap | IANA RDAP bootstrap |
| `.yahoo` | bootstrap | IANA RDAP bootstrap |
| `.yamaxun` | bootstrap | IANA RDAP bootstrap |
| `.yandex` | bootstrap | IANA RDAP bootstrap |
| `.ye` | bootstrap | IANA RDAP bootstrap |
| `.yodobashi` | bootstrap | IANA RDAP bootstrap |
| `.yoga` | bootstrap | IANA RDAP bootstrap |
| `.yokohama` | bootstrap | IANA RDAP bootstrap |
| `.you` | bootstrap | IANA RDAP bootstrap |
| `.youtube` | bootstrap | IANA RDAP bootstrap |
| `.yt` | bootstrap | IANA RDAP bootstrap |
| `.yun` | bootstrap | IANA RDAP bootstrap |
| `.za` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
| `.zappos` | bootstrap | IANA RDAP bootstrap |
| `.zara` | bootstrap | IANA RDAP bootstrap |
| `.zero` | bootstrap | IANA RDAP bootstrap |
| `.zip` | bootstrap | IANA RDAP bootstrap |
| `.zm` | bootstrap | IANA RDAP bootstrap |
| `.zone` | bootstrap | IANA RDAP bootstrap |
| `.zuerich` | bootstrap | IANA RDAP bootstrap |
| `.zw` | none | ccTLD — no public RDAP in bootstrap/supplement (likely WHOIS-only) |
