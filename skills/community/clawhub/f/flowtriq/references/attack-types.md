# Flowtriq Attack Types Reference

All 8 attack families Flowtriq classifies, with context on what they are,
what the traffic looks like, and recommended responses.

---

## UDP Flood (`udp_flood`)

**What it is:** High-volume UDP packets sent to random or specific ports to
saturate bandwidth or exhaust server resources.

**Traffic signature:** Sudden spike in UDP traffic, often targeting UDP/53
(DNS), UDP/123 (NTP), or random high ports. High BPS relative to PPS.

**IOC matches to watch for:** Generic UDP flood patterns, Mirai variants.

**Recommended response:**
- FlowSpec rate-limit on UDP if BGP is configured
- iptables drop rule on targeted port if specific port attack
- Check geo breakdown — UDP floods often originate from reflection sources

---

## SYN Flood (`syn_flood`)

**What it is:** Massive volume of TCP SYN packets to exhaust connection
state tables on the target server.

**Traffic signature:** Very high PPS, TCP flag breakdown shows SYN dominant
(80%+), low ACK count. `tcp_flag_breakdown.SYN` will be high.

**IOC matches to watch for:** SYN flood patterns, spoofed source IPs.

**Recommended response:**
- Enable SYN cookies on the server (`sysctl net.ipv4.tcp_syncookies=1`)
- FlowSpec rate-limit on TCP SYN flags
- Check `spoofing_detected` — SYN floods are commonly spoofed

---

## HTTP Flood (`http_flood`)

**What it is:** High volume of HTTP/HTTPS requests to overwhelm the web
application layer. Hard to distinguish from legitimate traffic at the
network layer.

**Traffic signature:** High request rate (req/s), TCP traffic, port 80/443
dominant in `top_dst_ports`. PPS may not be extreme but requests per second
will be high.

**Recommended response:**
- Rate limiting at load balancer or CDN level
- Cloudflare WAF rules if scrubbing is configured
- Review top source IPs for botnet patterns

---

## ICMP Flood (`icmp_flood`)

**What it is:** High-volume ICMP echo requests (ping flood) to consume
bandwidth.

**Traffic signature:** ICMP dominant in protocol breakdown. Often simple
and unsophisticated.

**Recommended response:**
- iptables drop ICMP at the node level
- FlowSpec ICMP rate-limit

---

## DNS Amplification (`dns_flood`)

**What it is:** Reflection/amplification attack using misconfigured open
DNS resolvers to bounce large UDP responses at the target.

**Traffic signature:** Very high BPS relative to PPS (amplification ratio
can be 50x+). Inbound traffic appears to come from legitimate DNS server
IPs. UDP/53 dominant.

**IOC matches to watch for:** DNS amplification patterns, known open
resolver IP ranges.

**Recommended response:**
- FlowSpec rate-limit on UDP/53
- Verify you don't have an open DNS resolver yourself
  (`flowtriq.com/tools/dns-resolver-checker`)
- Source IPs will be legitimate resolvers — blocking them is a last resort

---

## Multi-Vector (`multi_vector`)

**What it is:** Simultaneous attack combining two or more attack types.
Designed to overwhelm defences that are tuned for single-vector attacks.

**Traffic signature:** Mixed protocol breakdown, multiple attack families
detected at once. Flowtriq will show combined confidence scores.

**Recommended response:**
- Escalate to cloud scrubbing if BGP mitigation alone is insufficient
- Review each vector in the protocol breakdown separately
- Check if mitigation rules are addressing all vectors

---

## NTP Amplification (detected as `udp_flood` subtype)

**What it is:** UDP amplification using NTP monlist responses. Similar to
DNS amplification but via UDP/123.

**Traffic signature:** High BPS, UDP/123 dominant in destination ports.

**Recommended response:**
- FlowSpec rate-limit UDP/123
- Check NTP amplification exposure: `flowtriq.com/tools/ntp-amplification-checker`

---

## Unknown (`unknown`)

**What it is:** Traffic anomaly detected above threshold but doesn't match
any known attack signature.

**Recommended response:**
- Download the PCAP from the dashboard and inspect manually
- Use the Wireshark filter cheatsheet: `flowtriq.com/tools/wireshark-filters`
- Check IOC pattern list is up to date

---

## Severity Levels

| Severity | PPS Multiplier | Meaning |
|---|---|---|
| `low` | < 2x baseline | Probably noise or a probe. Monitor. |
| `medium` | 2-5x baseline | Real traffic anomaly. Watch for escalation. |
| `high` | 5-20x baseline | Active attack. Mitigation should be deploying. |
| `critical` | 20x+ baseline | Major attack. Check mitigation is active. Consider escalating to cloud scrubbing. |
