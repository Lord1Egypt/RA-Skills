# ENS Manager Dependencies

**Last updated:** 2026-03-13

---

## Required Software

### 1. Node.js 18+

**Check version:**
```bash
node --version
# Should show: v18.x.x or higher
```

**Install if needed:**
- macOS: `brew install node`
- Ubuntu: `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt-get install -y nodejs`
- Windows: Download from https://nodejs.org

---

## NPM Package Dependencies

### Core Dependencies (Required for ALL scripts)

```bash
cd scripts/
npm install viem
```

**What it does:**
- `viem` - Ethereum client library for all blockchain interactions
- Used by: ALL scripts (check-ens-name.js, register-ens-name.js, create-subdomain.js, create-subdomain-ipfs.js)

**Size:** ~5MB  
**Install time:** 10-30 seconds

---

### Extended Dependencies (Only for IPFS features)

```bash
cd scripts/
npm install content-hash
```

**What it does:**
- `content-hash` - Encode/decode IPFS CIDs for ENS content hash records

**Used by:**
- ✅ `create-subdomain-ipfs.js` (REQUIRED)
- ❌ `create-subdomain.js` (NOT needed)
- ❌ `register-ens-name.js` (NOT needed)
- ❌ `check-ens-name.js` (NOT needed)

**Size:** ~500KB  
**Install time:** 5-10 seconds

---

## Quick Install (All Dependencies)

```bash
cd scripts/
npm install
```

This installs everything listed in `package.json`:
- viem
- content-hash

**Total size:** ~6MB  
**Total time:** 15-40 seconds

---

## Dependency Matrix

| Script | viem | content-hash | Notes |
|--------|------|--------------|-------|
| `check-ens-name.js` | ✅ Required | ⚠️ Optional | content-hash only for IPFS decode |
| `register-ens-name.js` | ✅ Required | ❌ Not used | Registration only |
| `create-subdomain.js` | ✅ Required | ❌ Not used | Minimal subdomain |
| `create-subdomain-ipfs.js` | ✅ Required | ✅ Required | IPFS content needed |

---

## Wallet Requirements

### Option 1: Encrypted Keystore (Recommended)

**Format:** AES-256-CBC encrypted JSON
```json
{
  "salt": "hex-string",
  "iv": "hex-string",
  "data": "hex-encrypted-private-key"
}
```

**Usage:**
```bash
node script.js ... --keystore /path/to/keystore.enc --password "your-password"
```

**No additional dependencies**

---

### Option 2: Private Key Environment Variable

**Setup:**
```bash
export WALLET_PRIVATE_KEY="0x1234..."
```

**Usage:**
```bash
node script.js ... --private-key-env WALLET_PRIVATE_KEY
```

**No additional dependencies**

---

### Option 3: Direct Private Key (Less Secure)

**Usage:**
```bash
node script.js ... --private-key "0x1234..."
```

**⚠️ Warning:** Exposes key in shell history. Use with caution.

---

## RPC Provider

### Default (Free)
- URL: `https://mainnet.rpc.buidlguidl.com`
- No API key needed
- Suitable for most use cases

### Custom Provider
```bash
export RPC_URL="https://your-provider.com"
node script.js ...
```

### Providers with Better Rate Limits
- **Infura:** https://infura.io (free tier: 100k requests/day)
- **Alchemy:** https://alchemy.com (free tier: 300M compute units/month)
- **QuickNode:** https://quicknode.com (various tiers)

---

## Testing Dependencies

```bash
# Install dev dependencies (optional)
cd scripts/
npm install --save-dev
```

No test framework included yet. Use `node -c script.js` to verify syntax.

---

## Troubleshooting

### "Cannot find module 'viem'"

```bash
cd scripts/
npm install viem
```

### "Cannot find module 'content-hash'"

You're using `create-subdomain-ipfs.js`:
```bash
cd scripts/
npm install content-hash
```

**Or use the minimal script instead:**
```bash
node create-subdomain.js ...  # No IPFS, no content-hash needed
```

### "EACCES: permission denied"

```bash
# Fix npm permissions
sudo chown -R $USER ~/.npm
npm install
```

### "gyp ERR!" (Build errors)

Usually safe to ignore. If scripts don't work:
```bash
npm rebuild
```

---

## Minimal Setup (Core Only)

If you only need basic ENS operations (no IPFS):

```bash
cd scripts/
npm install viem
```

**What you can do:**
- ✅ Check ENS names
- ✅ Register .eth names
- ✅ Create subdomains
- ❌ Set IPFS content (need content-hash)

---

## Full Setup (All Features)

For complete ENS + IPFS workflow:

```bash
cd scripts/
npm install viem content-hash
```

**What you can do:**
- ✅ Everything in core
- ✅ Set IPFS content hashes
- ✅ Publish decentralized websites

---

## Verification

Check all dependencies are installed:

```bash
cd scripts/
npm list --depth=0
```

Should show:
```
scripts@1.1.0
├── viem@1.20.0
└── content-hash@2.5.2
```

---

## Updates

Keep dependencies updated for bug fixes and features:

```bash
cd scripts/
npm update
```

Check for major version updates:
```bash
npm outdated
```

---

## Summary

**Minimum to start:**
```bash
cd scripts/ && npm install viem
```

**Full features:**
```bash
cd scripts/ && npm install
```

**Storage:** ~6MB total  
**Install time:** <1 minute

That's it! All dependencies are npm packages, no system libraries needed.
