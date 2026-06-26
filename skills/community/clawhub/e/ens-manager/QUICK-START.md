# ENS Manager - Quick Start for Agents

**For autonomous agent operations.**  
**Copy-paste ready commands.**

---

## Install Dependencies

```bash
cd scripts/
npm install viem          # Core (required)
npm install content-hash  # Extended (only for IPFS)
```

**Or install everything:**
```bash
cd scripts/ && npm install
```

---

## Core Operations (No IPFS)

### 1. Check ENS Name

```bash
node scripts/check-ens-name.js clophorse.eth
```

**Output:**
- Owner address
- Wrapped/unwrapped status
- Resolver address
- Content hash (if set)

**Time:** 5 seconds  
**Cost:** Free

---

### 2. Register .eth Name

**Dry run (check availability + price):**
```bash
node scripts/register-ens-name.js mynewname --dry-run
```

**Register for 1 year:**
```bash
node scripts/register-ens-name.js mynewname \
  --years 1 \
  --keystore /path/to/keystore.enc \
  --password "your-password"
```

**Or with environment variable:**
```bash
export WALLET_PRIVATE_KEY="0x..."
node scripts/register-ens-name.js mynewname \
  --years 1 \
  --private-key-env WALLET_PRIVATE_KEY
```

**Time:** 2-3 minutes (commitment → 60s wait → register)  
**Cost:** ~$6-14 (5-letter name)

---

### 3. Create Bare Subdomain (Minimal)

```bash
node scripts/create-subdomain.js yourname.eth api \
  --keystore /path/to/keystore.enc \
  --password "your-password"
```

**Result:** `api.yourname.eth` created (no IPFS content)

**Time:** 1 minute  
**Cost:** ~$0.08-4

---

## Extended Operations (With IPFS)

### 4. Create Subdomain + Set IPFS Content

**Prerequisites:**
- IPFS CID ready (e.g., `QmABC123...`)
- content-hash dependency installed

```bash
node scripts/create-subdomain-ipfs.js yourname.eth site QmABC123... \
  --keystore /path/to/keystore.enc \
  --password "your-password"
```

**Result:** `site.yourname.eth` → `https://site.yourname.eth.limo`

**Time:** 1-2 minutes  
**Cost:** ~$0.08-4

---

## Wallet Options

### Option 1: Encrypted Keystore (Safest)

```bash
node script.js ... \
  --keystore /path/to/keystore.enc \
  --password "your-password"
```

### Option 2: Environment Variable

```bash
export WALLET_PRIVATE_KEY="0x1234..."
node script.js ... \
  --private-key-env WALLET_PRIVATE_KEY
```

### Option 3: Direct (Less Secure)

```bash
node script.js ... \
  --private-key "0x1234..."
```

---

## State Verification

### Check Name Owner

```bash
node scripts/check-ens-name.js name.eth | grep Owner
```

### Check if Wrapped

```bash
node scripts/check-ens-name.js name.eth | grep Wrapped
```

### Check Resolver

```bash
node scripts/check-ens-name.js name.eth | grep Resolver
```

### Check Content Hash

```bash
node scripts/check-ens-name.js name.eth | grep "Content Hash"
```

### Check if Subdomain Exists

```bash
# If owner is not 0x000..., subdomain exists
node scripts/check-ens-name.js sub.name.eth | grep Owner
```

---

## Resumability Patterns

### Before Creating Subdomain

```bash
# Check if already exists
EXISTS=$(node scripts/check-ens-name.js api.myname.eth 2>&1 | grep -c "0x0000000000000000000000000000000000000000")

if [ "$EXISTS" -eq "0" ]; then
  echo "Subdomain already exists, skipping creation"
else
  echo "Creating subdomain..."
  node scripts/create-subdomain.js myname.eth api ...
fi
```

### Before Registration

```bash
# Check availability first
node scripts/register-ens-name.js mynewname --dry-run

# Only register if available
if [ $? -eq 0 ]; then
  node scripts/register-ens-name.js mynewname ...
fi
```

### After Any Operation

```bash
# Verify state changed
node scripts/check-ens-name.js name.eth

# Check specific field
OWNER=$(node scripts/check-ens-name.js name.eth | grep "Owner:" | awk '{print $2}')
if [ "$OWNER" = "0x0000000000000000000000000000000000000000" ]; then
  echo "Operation failed, owner still zero"
else
  echo "Success, owner: $OWNER"
fi
```

---

## Error Recovery

### Transaction Failed

```bash
# Check why
node scripts/check-ens-name.js name.eth

# Common issues:
# - Not the owner (can't create subdomain)
# - Insufficient balance
# - Wrong network
```

### Name Already Exists

```bash
# Check current owner
node scripts/check-ens-name.js name.eth

# Wait for expiration or contact owner
```

### Commitment Expired (> 24 hours)

```bash
# Start registration again from phase 1
node scripts/register-ens-name.js name --years 1 ...
```

---

## Common Workflows

### Workflow 1: Register + Create Subdomain

```bash
# 1. Check availability
node scripts/register-ens-name.js myproject --dry-run

# 2. Register
node scripts/register-ens-name.js myproject --years 1 \
  --keystore keystore.enc --password "pass"

# 3. Wait for confirmation (2-3 min)

# 4. Create subdomain
node scripts/create-subdomain.js myproject.eth api \
  --keystore keystore.enc --password "pass"
```

### Workflow 2: Publish Website

```bash
# 1. Upload to IPFS
ipfs add -r ./website
# Returns: QmXYZ...

# 2. Create subdomain with content
node scripts/create-subdomain-ipfs.js myname.eth site QmXYZ... \
  --keystore keystore.enc --password "pass"

# 3. Access at https://site.myname.eth.limo
```

### Workflow 3: Update Content

```bash
# 1. Upload new version
ipfs add -r ./website-v2
# Returns: QmNEW...

# 2. Update content hash
node scripts/create-subdomain-ipfs.js myname.eth site QmNEW... \
  --keystore keystore.enc --password "pass"

# 3. Wait 1-2 minutes for gateway update
```

---

## Decision Tree

**Do you need IPFS?**
- ❌ No → Use `create-subdomain.js` (minimal)
- ✅ Yes → Use `create-subdomain-ipfs.js` (extended)

**Do you own the parent name?**
- ❌ No → Register first with `register-ens-name.js`
- ✅ Yes → Proceed with subdomain creation

**Is the name wrapped?**
- Check with: `node scripts/check-ens-name.js name.eth`
- Both scripts handle wrapped/unwrapped automatically

---

## Performance Tips

### Batch Operations

```bash
# Create multiple subdomains (sequential)
for label in api www mail; do
  node scripts/create-subdomain.js myname.eth $label \
    --keystore keystore.enc --password "pass"
done
```

### Parallel (Advanced)

```bash
# Run in background (be careful with nonce management!)
node scripts/create-subdomain.js myname.eth api ... &
sleep 30  # Wait for first TX to confirm
node scripts/create-subdomain.js myname.eth www ... &
```

**⚠️ Warning:** Parallel transactions require proper nonce management to avoid conflicts.

---

## Debugging

### Verbose Output

```bash
# Add console.log debugging
export DEBUG=true
node scripts/check-ens-name.js ...
```

### Check Transaction Status

```bash
# Get TX hash from output, then:
cast receipt <TX_HASH> --rpc-url https://mainnet.rpc.buidlguidl.com
```

### Test on Sepolia First

```bash
# Not supported yet, coming soon
# For now, use small subdomains on mainnet for testing
```

---

## Summary Table

| Operation | Script | Time | Cost | Dependencies |
|-----------|--------|------|------|--------------|
| Check name | `check-ens-name.js` | 5s | Free | viem |
| Register | `register-ens-name.js` | 2-3min | $6-14 | viem |
| Subdomain (bare) | `create-subdomain.js` | 1min | $0.08-4 | viem |
| Subdomain (IPFS) | `create-subdomain-ipfs.js` | 1-2min | $0.08-4 | viem, content-hash |

---

**Quick reference for copy-paste operations.** See [README.md](README.md) for detailed documentation.
