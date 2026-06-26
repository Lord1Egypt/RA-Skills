# domani.run - Transfer Reference

Detailed transfer workflows. See the main [SKILL.md](https://domani.run/SKILL.md) for transfer eligibility check and initiation.

## Check inbound transfer status

```bash
curl -s "https://domani.run/api/domains/mysite.com/transfer-status" \
  -H "Authorization: Bearer $DOMANI_API_KEY"
# Returns: {"domain": "mysite.com", "status": "pending_owner", "hint": "Transfer is awaiting approval..."}
```

Statuses: `pending_owner` (check email for approval link), `pending_admin` (awaiting registrar), `pending_registry` (approved, processing at registry, usually 1-7 days), `completed`, `cancelled`, `unknown`. Rate limit: 30/min.

## Before transferring: unlock & get auth code

Most registrars lock domains by default. Before initiating a transfer, the user must:
1. **Unlock the domain** at their current registrar (disable "Transfer Lock" / "Domain Lock")
2. **Get the EPP/authorization code** (also called "auth code", "transfer key", or "EPP key")
3. **Disable WHOIS privacy** temporarily (some registrars require this for transfers)

### Registrar-specific instructions

| Registrar | How to unlock & get EPP code |
|-----------|-----|
| **GoDaddy** | My Products → Domain → Domain Settings → turn off "Domain Lock" → tap "Transfer domain away from GoDaddy" → Get authorization code → code is emailed or shown |
| **Namecheap** | Domain List → Manage → Sharing & Transfer → scroll to "Transfer Out" section → click UNLOCK next to "Domain Lock" → click AUTH CODE button → code is emailed to registrant email |
| **Cloudflare** | Dash → domain → Configuration → disable "Domain Lock" → copy Authorization Code (shown in-page) |
| **Squarespace Domains** (ex-Google Domains) | Domains → domain → Settings → scroll to "Transfer away" → Unlock domain → Get auth code → code is emailed |
| **Hover** | Control Panel → domain → Transfer tab → Remove lock → "Get Auth Code" → code is emailed |
| **Name.com** | My Domains → domain → Details → unlock domain → Authorization Code → copy or email |
| **IONOS (1&1)** | Domain Center → domain gear icon → Transfer → Unlock domain → Get auth code → code is emailed |
| **OVH** | Web Cloud → Domains → domain → General Information → Unlock → Request auth code → code is emailed |
| **Gandi** | Domain → domain → Transfer tab → Unlock → click "Get authinfo code" → code is emailed |
| **Porkbun** | Domain Management → domain → Authorization Code → copy the code. Domain is unlocked by default |
| **Dynadot** | Manage Domains → domain → Unlock → Get Auth Code (shown in-page) |

### General tips

- The EPP code is usually 6-16 characters. If it looks like a URL or has spaces, they may have copied the wrong thing
- Codes are often emailed to the registrant email - make sure the user has access to that inbox
- Some registrars (GoDaddy, Squarespace) may impose a 60-day lock after purchase or contact changes
- WHOIS privacy should usually be disabled before transfer (re-enabled automatically after transfer completes at domani.run)
- If the domain was registered less than 60 days ago, ICANN rules prevent transfer
- **If the domain is not yet eligible**: we save the request and will automatically email the user when it becomes eligible. They'll need to get a fresh EPP code at that time and retry. No payment is charged until the transfer actually goes through

## DNS auto-migration

We automatically snapshot all existing DNS records before initiating the transfer (discovered via CT logs, SPF, MX/DKIM inference, and a common wordlist). When the transfer completes, records are restored at the new registrar - no manual DNS re-creation needed. Pass `extra_subdomains` in the request body to include any custom subdomains we might not auto-discover.
