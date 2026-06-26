# Email Authentication Setup Guide

This guide covers SPF, DKIM, DMARC, and BIMI configuration for ecommerce sending domains. Follow the protocols in order -- each builds on the previous.

---

## SPF (Sender Policy Framework)

SPF tells receiving servers which IP addresses and services are authorized to send email on behalf of your domain.

### How SPF Works

When a receiving server gets an email claiming to be from `yourstore.com`, it checks the DNS TXT record at `yourstore.com` for an SPF policy. If the sending server's IP is listed in that policy, SPF passes. If not, it fails.

### Setting Up SPF

**1. Identify all legitimate sending sources:**
- Your ESP (Klaviyo, Mailchimp, Omnisend, etc.)
- Transactional email service (Postmark, SendGrid, Amazon SES)
- Help desk (Zendesk, Freshdesk, Gorgias)
- Any other service sending as your domain

**2. Build the SPF record:**

```
v=spf1 include:_spf.google.com include:sendgrid.net include:klaviyo.com ~all
```

Structure:
- `v=spf1` -- version identifier (required, must be first)
- `include:[domain]` -- authorize a third-party service's IP ranges
- `ip4:[address]` -- authorize a specific IPv4 address or CIDR range
- `~all` -- soft fail for unauthorized senders (use during setup)
- `-all` -- hard fail for unauthorized senders (use once validated)

**3. Publish as a DNS TXT record** on the root domain (e.g., `yourstore.com`).

### SPF Constraints and Common Problems

- **10 DNS lookup limit:** Each `include`, `a`, `mx`, `ptr`, and `redirect` mechanism counts as one DNS lookup. Nested includes also count. Exceeding 10 causes a permanent error (`permerror`), which many receivers treat as a fail.
- **Counting lookups:** Use `mxtoolbox.com/spf.aspx` to see total lookup count.
- **Fixing excess lookups:**
  - Remove services you no longer use
  - Replace `include` with direct `ip4`/`ip6` entries for services with static IPs (but note these break if the service changes IPs)
  - Use an SPF flattening service (e.g., autospf.com, dmarcian SPF Surveyor) that auto-resolves includes to IP addresses and keeps the record updated
  - Split sending across subdomains (e.g., marketing sends from `mail.yourstore.com` with its own SPF record)
- **Only one SPF record per domain:** Multiple TXT records starting with `v=spf1` cause SPF to fail. Merge them into one.
- **No SPF on subdomains by default:** SPF records are not inherited. If you send from `mail.yourstore.com`, it needs its own SPF record.

### SPF Alignment

For DMARC to use SPF results, the domain in the envelope-from (Return-Path) must align with the domain in the header-from. Most ESPs provide a custom bounce/return-path domain setting to achieve this. Configure it.

---

## DKIM (DomainKeys Identified Mail)

DKIM cryptographically signs outgoing emails so receivers can verify the message was not altered in transit and was authorized by the domain owner.

### How DKIM Works

The sending server signs a hash of specified email headers and body content using a private key. The corresponding public key is published in DNS. The receiving server retrieves the public key and verifies the signature.

### Setting Up DKIM

**1. Generate a key pair through your ESP.**

Most ESPs handle key generation. You will receive a DNS record to publish. Example:

```
Host:  s1._domainkey.yourstore.com
Type:  CNAME (or TXT)
Value: s1.domainkey.klaviyo.com (CNAME) or "v=DKIM1; k=rsa; p=MIGfMA0G..." (TXT)
```

**2. Publish the DNS record.**

Add the CNAME or TXT record at the specified hostname. CNAME is preferred when the ESP offers it because key rotation is handled automatically.

**3. Enable signing in your ESP dashboard.**

Most ESPs have a domain authentication or sender authentication section. Complete the verification steps.

**4. Test by sending an email and inspecting headers.**

Look for:
```
dkim=pass header.d=yourstore.com header.s=s1
```

### DKIM Best Practices

- **Use 2048-bit keys.** 1024-bit is the minimum accepted length but is increasingly vulnerable. Some DNS providers have a 255-character TXT record limit; if so, split the key across multiple strings within one TXT record.
- **Rotate keys annually.** Publish the new key, update ESP configuration, then remove the old key after 48 hours.
- **Sign with your own domain, not the ESP's default.** Unsigned or third-party-signed emails fail DMARC alignment.
- **Sign each sending source separately.** Every service sending as your domain needs its own DKIM key published in your DNS.

### DKIM Alignment

For DMARC, the `d=` domain in the DKIM signature must match (or be a subdomain of) the header-from domain. If your From address is `hello@yourstore.com`, the DKIM signature must have `d=yourstore.com` (or `d=mail.yourstore.com` in relaxed alignment mode).

---

## DMARC (Domain-based Message Authentication, Reporting, and Conformance)

DMARC ties SPF and DKIM together with a policy that tells receivers what to do when authentication fails, and provides reporting so you can monitor abuse.

### How DMARC Works

The receiving server checks if the email passes SPF or DKIM with alignment to the From domain. Based on the DMARC policy, it then delivers, quarantines, or rejects the message. Aggregate reports are sent to the domain owner.

### Setting Up DMARC

**Phase 1: Monitor (weeks 1-4)**

Start with a monitoring-only policy to collect data without affecting delivery.

```
v=DMARC1; p=none; rua=mailto:dmarc-reports@yourstore.com; ruf=mailto:dmarc-forensic@yourstore.com; pct=100;
```

- `p=none` -- take no action on failures (monitor only)
- `rua` -- address for aggregate reports (daily XML summaries)
- `ruf` -- address for forensic/failure reports (individual message details; not all providers send these)
- `pct=100` -- apply policy to 100% of messages

Use a DMARC report analyzer (dmarcian, Postmark DMARC, EasyDMARC) instead of raw XML reports.

**Phase 2: Quarantine (weeks 5-8)**

After confirming all legitimate sources pass, move to quarantine.

```
v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@yourstore.com; pct=25;
```

Start with `pct=25` (apply quarantine to 25% of failing messages), then increase to 50%, 75%, 100% over several weeks while monitoring reports for false positives.

**Phase 3: Reject (week 9+)**

Once confident, enforce full rejection.

```
v=DMARC1; p=reject; rua=mailto:dmarc-reports@yourstore.com; pct=100;
```

### DMARC Record Placement

Publish as a TXT record at `_dmarc.yourstore.com`.

### DMARC Policy Considerations for Ecommerce

- **Third-party senders:** Review platforms, loyalty programs, and marketplace integrations that send email using your domain. Each must pass SPF or DKIM alignment before moving to quarantine/reject.
- **Subdomain policy:** Use `sp=none` if subdomains have different authentication needs while the main domain is at `p=reject`.
- **Forwarding:** Email forwarding breaks SPF (the forwarder's IP is not in your SPF). DKIM survives forwarding if the message is not modified. This is one reason DKIM alignment is more reliable than SPF alignment for DMARC.

---

## BIMI (Brand Indicators for Message Identification)

BIMI displays your brand logo next to emails in supporting clients (Gmail, Yahoo, Apple Mail). It requires DMARC at `p=quarantine` or `p=reject`.

### Requirements

1. DMARC policy at `p=quarantine` or `p=reject` with `pct=100`
2. A Verified Mark Certificate (VMC) from DigiCert or Entrust (required for Gmail; Yahoo shows logos without VMC)
3. Your trademarked logo in SVG Tiny PS format

### Setting Up BIMI

**1. Prepare your logo:**
- Must be SVG Tiny Portable/Secure format (not standard SVG)
- Square aspect ratio, centered logo on solid background
- Host at an HTTPS URL

**2. Obtain a VMC (for Gmail display):**
- Requires a registered trademark in a participating jurisdiction
- Apply through DigiCert or Entrust (annual cost: ~$1,000-1,500)

**3. Publish the BIMI record:**

```
Host:  default._bimi.yourstore.com
Type:  TXT
Value: v=BIMI1; l=https://yourstore.com/brand/logo.svg; a=https://yourstore.com/brand/vmc.pem;
```

- `l=` -- URL to your SVG logo
- `a=` -- URL to your VMC certificate (omit if no VMC)

### BIMI ROI for Ecommerce

BIMI improves brand recognition and trust in the inbox. Early data shows 10-20% improvement in open rates for BIMI-enabled senders, making the VMC investment worthwhile for brands sending >100K emails/month.

---

## Authentication Verification Checklist

After setup, verify all protocols:

- [ ] SPF record exists and is valid (`v=spf1` prefix, single record, <10 lookups)
- [ ] SPF includes all legitimate sending services
- [ ] SPF ends with `-all` or `~all`
- [ ] Custom return-path/bounce domain configured for SPF alignment
- [ ] DKIM key published for each sending service
- [ ] DKIM key length is 2048-bit
- [ ] DKIM signing enabled and verified via test email headers
- [ ] DKIM `d=` domain aligns with From domain
- [ ] DMARC record published at `_dmarc.[domain]`
- [ ] DMARC `rua` reporting configured and reports are being received
- [ ] DMARC policy is at minimum `p=quarantine` (target: `p=reject`)
- [ ] All third-party senders pass DMARC checks (review aggregate reports)
- [ ] BIMI record published (if DMARC is at quarantine/reject and trademark is registered)
- [ ] Test email scores 10/10 on mail-tester.com

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| SPF permerror | >10 DNS lookups | Flatten record or split across subdomains |
| SPF softfail/fail | Sending IP not in SPF | Add the service's include mechanism |
| DKIM fail | Key not published or wrong selector | Verify DNS record matches ESP configuration |
| DKIM body hash mismatch | Message modified in transit (forwarding, list software) | Check for intermediary modification; rely on DKIM alignment rather than SPF for DMARC |
| DMARC fail (both SPF and DKIM) | Neither protocol aligned with From domain | Configure custom domains for both SPF and DKIM alignment |
| DMARC reports show unknown senders | Spoofing or forgotten authorized service | Investigate source IPs; add legitimate services or tighten policy |
