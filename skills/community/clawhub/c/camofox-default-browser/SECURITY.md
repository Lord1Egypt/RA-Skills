# 🔒 Camoufox Default Browser — Security Guidelines

> **Last updated:** 2026-07-30  
> **Scope:** All operators, administrators, and developers using the Camoufox browser integration in OpenClaw.

---

## ⚠️ Critical Warning

**Cookies are bearer tokens.** Anyone who obtains a cookie file can impersonate you without needing your password, MFA, or any other credential. Treat cookies like your bank card — if it's stolen, someone else controls your account.

---

## 1. Cookie Security 🍪

### What Are Bearer Cookies?

A cookie is essentially an authentication token that says "trust whoever presents this." Sites don't check passwords again — they check the cookie. This means:

- **Cookie = Full Account Access** — possession is equivalent to the username, password, and often 2FA bypass.
- **No granular permissions** — there's no such thing as "read-only session" for most platforms. It's all-or-nothing.

### Proper Storage

```
✅ DO                                          ❌ DON'T
─────────────────────────────────    ─────────────────────────────────
Store .txt/.cookies files outside            Leave them in world-readable /tmp
public web root                              directories
                                             
Set file permissions 600 (owner only)        chmod 777 for convenience
                                          
Use dedicated files per account              Mix multiple accounts in one file
                                          
Encrypt at rest if possible                  Store unencrypted on shared drives
                                           
Delete after use                             Hoard old cookies "just in case"
```

**Permission requirement:** Cookie files MUST have permissions `600` (`rw-------`). This means only the file owner can read or write them. No group, no others.

```bash
chmod 600 /path/to/cookies.txt
```

### Account Takeover Risks — Real Scenarios

| Scenario | Impact | Prevention |
|----------|--------|------------|
| Cookie file copied by another user/process | Full account impersonation | Permissions 600 + dedicated files |
| Cookie exported to clipboard or chat log | Intercepted by malware/logging | Never paste cookies anywhere |
| Old cookie retained on decommissioned machine | Zombie access to active accounts | Delete immediately when done |
| Cookie sync via cloud backup service | Uploaded to third-party servers | Exclude from backup patterns |

### Best Practices

1. **Rotate regularly** — Replace cookies every time login credentials change or suspicious activity is detected.
2. **Scope minimally** — Import only what you need. Use `domainSuffix` filter instead of bulk imports.
3. **Segregate by purpose** — Separate work, personal, and testing cookies into different files.
4. **Never commit to version control** — Add `*.cookies`, `*cookies.txt`, `*.netrc` to `.gitignore` immediately.

---

## 2. Authorized Use Only ⚖️

### Legal Compliance

Unauthorized automated access to computer systems violates laws worldwide:

- **United States:** Computer Fraud and Abuse Act (CFAA), 18 U.S.C. § 1030
- **European Union:** Directive on security of network and information systems (NIS Directive)
- **Indonesia:** UU ITE (Undang-Undang Informasi dan Transaksi Elektronik) Pasal 30
- **Australia:** Cybercrime Act 2001
- **Other jurisdictions:** Most countries have similar anti-hacking legislation

### Terms of Service Considerations

Many platforms explicitly prohibit automated access:

- **Google, Meta, LinkedIn, X/Twitter** — ToS often forbid scraping and bot activity
- **E-commerce platforms** — Anti-bot measures are legally enforceable terms
- **Social media** — Automated interaction may violate community standards

**Rule:** Always review the target platform's Terms of Service before automating access. If the ToS prohibits automation, do not automate — even if technically possible.

### Permission Documentation

Maintain written authorization records:

- ✅ Document who approved the automation
- ✅ Record which accounts are authorized
- ✅ Note the scope (what actions are permitted)
- ✅ Include expiration dates for temporary access
- ✅ Keep records alongside cookie files as `.authorization.json`

```json
{
  "account": "user@example.com",
  "approved_by": "Akmal",
  "purpose": "Automated browsing for task management",
  "date_approved": "2026-07-30",
  "expires": "2026-08-30",
  "scope": "view_and_interact_only"
}
```

---

## 3. Data Protection 🛡️

### What Data IS Collected (Telemetry)

If telemetry is enabled by the operator, the following may be collected:

- **Browser fingerprint metadata** — User-Agent string, viewport size, timezone offset
- **Connection metadata** — Timestamps of sessions, duration estimates
- **Error reports** — Stack traces and error codes from failed operations

### What Data Is NOT Collected

Under normal operation, Camoufox does **NOT** collect:

- ❌ Page content or HTML responses
- ❌ Cookie values or authentication tokens
- ❌ Personal messages, emails, or private data
- ❌ IP addresses sent to external services
- ❌ Form inputs or typed text
- ❌ Screenshots unless explicitly captured

This design ensures privacy-by-default — the browser engine processes everything locally.

### Opt-Out Procedures

To disable telemetry (if available):

1. Check operator configuration in `openclaw.json` under relevant settings
2. Set explicit opt-out flags per documentation
3. Verify no background processes are transmitting data
4. Monitor network connections during test runs using `ss -tulnp`

### Data Retention Policies

- **Session logs:** Purge after task completion (automatic cleanup recommended)
- **Cookie files:** Delete when account access is no longer needed
- **Screenshots:** Remove after verification and delivery to user
- **Temporary files:** Clean `/tmp/` and workspace `tmp/` directories after use
- **Archive records:** Comply with organization-defined retention periods (default 90 days)

---

## 4. Access Control 🔐

### API Key Protection

- Never embed API keys directly in scripts or command history
- Use environment variables or secure config managers
- Rotate keys periodically (at minimum when team membership changes)
- Audit key usage patterns for anomalous consumption

```bash
# ✅ Correct: Environment variable
CAMOUFOX_API_KEY=$API_KEY camofox_navigate ...

# ❌ Wrong: Hardcoded in script
apikey="sk-abc123def456"  # EXPOSED IN VERSION CONTROL
```

### Server Binding

**Critical:** The Camoufox automation server must bind to `localhost` (127.0.0.1) only, unless multi-machine access is explicitly required and properly secured.

```
✅ Bind to: 127.0.0.1:port     — Localhost only (safe)
✅ Bind to: 127.0.0.1:port     — Explicit localhost (recommended)
⚠️ Bind to: 0.0.0.0:port       — All interfaces (requires firewall)
❌ Bind to: public IP:port      — Exposed to internet (never)
```

### Firewall Recommendations

Configure host firewall rules:

```bash
# Allow localhost access
iptables -A INPUT -p tcp --dport <camoufox-port> -s 127.0.0.1 -j ACCEPT

# Block external access
iptables -A INPUT -p tcp --dport <camoufox-port> -j DROP

# Or use ufw for simpler management
ufw deny <camoufox-port>/tcp  # deny by default
ufw allow from 127.0.0.1 to any port <camoufox-port>
```

### Multi-User Isolation

When multiple users share a system:

1. Each operator gets a dedicated cookie directory with restricted permissions
2. Browser profiles must be separated — never share state between users
3. Session IDs should not leak between concurrent operations
4. Process ownership must match file ownership for cookie access

---

## 5. Risk Mitigation 🎯

### Session Hijacking Prevention

- **Regenerate sessions** after any suspected compromise
- **Bind sessions** to specific browser fingerprints where the platform supports it
- **Detect anomalies** — sudden geographic jumps or device changes should trigger alerts
- **Use short-lived cookies** where the platform provides refresh token capabilities

### Credential Storage Best Practices

| Method | Security Level | Recommendation |
|--------|---------------|----------------|
| Environment variables | High | ✅ Preferred for runtime access |
| Encrypted files (gpg) | High | ✅ Good for persistent storage |
| OS keychain | Medium-High | ✅ Platform-dependent availability |
| Plain text files | Low | ⚠️ Acceptable only with 600 permissions |
| Hardcoded strings | None | ❌ Never — in code, configs, or git |
| URL parameters | None | ❌ Appears in server logs |

### Audit Logging Recommendations

Log the following events for operational security:

- Cookie import/export operations (timestamp, source, target account)
- Successful and failed navigation attempts to restricted sites
- Configuration changes to access rules
- Any deviation from expected browser behavior

Keep logs separate from cookie/data files. Example log format:

```
[2026-07-30T13:00:00+07:00] IMPORT cookies: linkedin.com domain_suffix
[2026-07-30T13:01:15+07:00] NAVIGATE @google_search query="example"
[2026-07-30T13:05:30+07:00] EXPORT cookies: example.com -> /dev/null (cleanup)
```

### Incident Response Procedures

**If a cookie is suspected compromised:**

1. **STOP** — Immediately close all tabs using that session
2. **ISOLATE** — Revoke the cookie at the target platform (log in manually and rotate session)
3. **ASSESS** — Determine what was exposed and how long the breach lasted
4. **DOCUMENT** — Record timeline, affected accounts, and potential damage
5. **ROTATE** — Generate fresh cookies and revoke the compromised ones
6. **REVIEW** — Update security practices to prevent recurrence

**Escalation path:** Inform Akmal immediately. For multi-account compromises, assess blast radius across all impacted platforms before resuming operations.

---

## 6. Compliance 📋

### GDPR Considerations (European Union)

When operating on EU data subjects:

- **Lawful basis** — Ensure processing has consent, contract necessity, or legitimate interest
- **Data minimization** — Collect only what is strictly necessary for the task
- **Purpose limitation** — Do not use scraped data for unrelated purposes
- **Right to erasure** — Be prepared to delete personal data upon request
- **Record keeping** — Maintain processing activity records per Article 30

Camoufox as a tool operator: The browser itself performs local processing. Cookie management acts as a data processor. Document the controller-processor relationship clearly.

### CCPA Awareness (California, USA)

- **Notice at collection** — Inform users whose data is being processed
- **Opt-out of sale** — Honor Global Privacy Control (GPC) signals where encountered
- **Right to know** — Maintain inventories of categories of personal information accessed
- **Service provider contracts** — Define limitations on data use when acting on behalf of data controllers

### Regional Law Variations

| Region | Key Requirements | Notes |
|--------|-----------------|-------|
| 🇮🇩 Indonesia | UU ITE Art. 30 | Unauthorized access punishable; consent required for electronic data handling |
| 🇪🇺 EU/EEA | GDPR + ePrivacy | Strict consent; cross-border transfer restrictions; DPIA for high-risk processing |
| 🇺🇸 California | CCPA/CPRA | GPC signals; right to delete; notice requirements |
| 🇺🇸 Other US states | Varying consumer privacy laws | Monitor state-level developments |
| 🇬🇧 UK | UK GDPR + DPA 2018 | Post-Brexit alignment with EU framework |
| 🇦🇺 Australia | Privacy Act 1988 | APPs govern collection, use, disclosure |

**Rule:** When operating in uncertain legal territory, consult qualified counsel rather than relying on generalized guidance. Regulations evolve frequently.

---

## Quick Reference Checklist

Before each automation session, confirm:

- [ ] Cookie files exist with `600` permissions and are not committed to git
- [ ] Authorization record exists and is within its validity period
- [ ] Target platform's Terms of Service reviewed for compliance
- [ ] Server binds to localhost or firewall rules are confirmed
- [ ] Logs are configured and accessible for audit trail
- [ ] Incident response contacts are known and reachable
- [ ] Telemetry is disabled unless explicitly enabled and documented
- [ ] Data retention schedule is understood and followed

---

*This document covers security guidelines for the Camoufox browser skill. Operators are responsible for staying current with applicable laws and platform policies. When in doubt, stop and ask.*
