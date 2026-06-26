# domani.run - Recipes Reference

Step-by-step workflows for common tasks. Follow these exactly.

## Recipe: Set up Google Workspace Email

```
1. connect_domain({ domain: "example.com", provider: "google-workspace" })
   → Sets MX (5 records), SPF, DMARC automatically
   → Relay next_steps to user

2. Tell user: "Verify your domain in Google Admin Console"
   → https://admin.google.com/ac/domains
   → Google auto-checks MX records (may take up to 48h)

3. Tell user: "Generate DKIM record in Google Admin"
   → https://admin.google.com/ac/apps/gmail/authenticateemail
   → Select domain → Generate new record → Copy the TXT value

4. User provides DKIM value → you add it:
   set_dns({ domain: "example.com", records: [
     ...existing_records,
     { type: "TXT", name: "google._domainkey", value: "v=DKIM1; k=rsa; p=..." }
   ] })

5. Verify: domain_status({ domain: "example.com" })
   → Check MX, SPF, DMARC, DKIM all green
```

## Recipe: Set up Fastmail Email

```
1. connect_domain({ domain: "example.com", provider: "fastmail" })
   → Sets MX (2 records), SPF, DMARC, DKIM (3 CNAME records) automatically
   → DKIM is fully automated via CNAME - no manual step needed

2. Tell user: "Add domain in Fastmail settings"
   → https://app.fastmail.com/settings/domains
   → Fastmail verifies MX and DKIM automatically

3. Verify: domain_status({ domain: "example.com" })
```

## Recipe: Set up Proton Mail Email

```
1. connect_domain({ domain: "example.com", provider: "proton" })
   → Sets MX (2 records), SPF, DMARC automatically
   → DKIM is managed by Proton after verification

2. Tell user: "Verify domain in Proton account"
   → https://account.proton.me/u/0/mail/domain-names
   → Click "Add domain" → Proton checks DNS automatically

3. Verify: domain_status({ domain: "example.com" })
```

## Recipe: Deploy to Vercel

```
1. connect_domain({ domain: "example.com", target: "my-app.vercel.app" })
   → Sets A record (76.76.21.21) + CNAME www → cname.vercel-dns.com

2. Tell user: "Add domain to your Vercel project"
   → Run: npx vercel domains add example.com
   → Or: Project Settings > Domains on vercel.com

3. verify_connection({ domain: "example.com", target: "my-app.vercel.app" })
   → Confirms DNS propagation and SSL
```

## Recipe: Deploy to Netlify

```
1. connect_domain({ domain: "example.com", target: "my-site.netlify.app" })
   → Sets A record (75.2.60.5) + CNAME www → apex-loadbalancer.netlify.com

2. Tell user: "Add domain in Netlify"
   → Site configuration > Domain management > Add a domain
   → Or: ntl domains:create example.com

3. verify_connection({ domain: "example.com", target: "my-site.netlify.app" })
```

## Recipe: Deploy to GitHub Pages

```
1. connect_domain({ domain: "example.com", target: "username.github.io" })
   → Sets 4 A records + CNAME www → username.github.io

2. Tell user: "Set custom domain in repo settings"
   → Settings > Pages > Custom domain → enter example.com
   → Or create a CNAME file in the repo root

3. verify_connection({ domain: "example.com", target: "username.github.io" })
```

## Recipe: Deploy to Cloudflare Pages

```
1. connect_domain({ domain: "example.com", target: "my-project.pages.dev" })
   → Sets CNAME apex + www → my-project.pages.dev

2. Tell user: "Add custom domain in Cloudflare dashboard"
   → Pages project > Custom domains > Set up a custom domain

3. verify_connection({ domain: "example.com", target: "my-project.pages.dev" })
```

## Recipe: Transfer Domain from Another Registrar

```
1. check_transfer_eligibility({ domain: "example.com" })
   → Shows price (includes 1 year renewal) and eligibility

2. Confirm price with user → get auth/EPP code from current registrar

3. transfer_domain({ domain: "example.com", auth_code: "..." })
   → DNS auto-snapshotted from CT logs + SPF + DKIM inference
   → Transfer takes 1-5 days

4. Poll: check_transfer_status({ domain: "example.com" })
   → Or use watch_transfer() for real-time updates

5. On completion: DNS records auto-restored at new registrar
```

## Recipe: Buy Domain + Full Setup

```
1. dns_check({ name: "myapp", tlds: ["com","dev","ai","io"] })
   → Filter available TLDs

2. search({ domains: ["myapp.dev","myapp.ai"] })
   → Get pricing → confirm with user

3. buy_domain({ domain: "myapp.dev" })
   → Domain registered

4. Post-purchase:
   - Verify WHOIS privacy is on (auto-enabled)
   - Verify auto-renew is on (auto-enabled)
   - Ask: "Connect to hosting? Email?"

5. If hosting: connect_domain({ domain: "myapp.dev", target: "..." })
6. If email: connect_domain({ domain: "myapp.dev", provider: "google-workspace" })
```
