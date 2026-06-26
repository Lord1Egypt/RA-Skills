# Workflow Recipes

Step-by-step recipes for common affiliate management tasks. All commands use `--json` for machine-readable output.

## 1. Affiliate Onboarding

Review and approve pending affiliates, assign them to a group, and create a coupon.

```bash
# List pending affiliates
affonso affiliates list --json --status pending

# Review a specific affiliate
affonso affiliates get aff_abc123 --json

# Approve the affiliate
affonso affiliates update aff_abc123 --json --status approved

# Assign to a group
affonso affiliates update aff_abc123 --json --group-id grp_xyz789

# Create a coupon for the affiliate
affonso coupons create --json \
  --affiliate-id aff_abc123 \
  --code PARTNER20 \
  --discount-type percentage \
  --discount-value 20 \
  --duration forever
```

## 2. Commission Tracking

Monitor referrals and their resulting commissions.

```bash
# List recent referrals for an affiliate
affonso referrals list --json --affiliate-id aff_abc123 --order desc

# Get details on a specific referral
affonso referrals get ref_def456 --json --expand commissions

# List commissions for a referral
affonso commissions list --json --referral-id ref_def456

# Update commission status (e.g. approve a pending commission)
affonso commissions update com_ghi789 --json --status approved
```

**Pagination note:** Referrals use cursor-based pagination. To get the next page:
```bash
affonso referrals list --json --affiliate-id aff_abc123 --starting-after ref_lastId
```

## 3. Payout Processing

Review and process pending payouts.

```bash
# List pending payouts
affonso payouts list --json --status pending

# Review a specific payout
affonso payouts get pay_jkl012 --json

# Mark as processing
affonso payouts update pay_jkl012 --json --status processing

# Mark as completed with payment reference
affonso payouts update pay_jkl012 --json \
  --status completed \
  --payment-method bank_transfer \
  --payment-reference "TXN-2024-001234"
```

## 4. Program Setup

Configure your affiliate program from scratch.

```bash
# View current program settings
affonso program get --json

# Update basic program info
affonso program update --json \
  --name "My Affiliate Program" \
  --tagline "Earn commissions promoting our products" \
  --website-url "https://example.com" \
  --auto-approve

# Set commission structure
affonso program payment-terms update --json \
  --commission-type percentage \
  --commission-rate 25 \
  --commission-duration forever \
  --payment-threshold 50 \
  --cookie-lifetime 30

# Configure fraud protection
affonso program fraud-rules update --json \
  --self-referral block \
  --duplicate-ip detect \
  --vpn-proxy detect \
  --suspicious-conversion detect

# Customize the affiliate portal
affonso program portal update --json \
  --primary-color "#4F46E5" \
  --onboarding-enabled \
  --resources-enabled

# Set traffic restrictions
affonso program restrictions update --json \
  --websites \
  --social-marketing \
  --content-marketing \
  --no-incentivized-traffic \
  --no-trademark-bidding
```

## 5. Coupon Campaign

Create and manage coupons for affiliates.

```bash
# Create coupons for multiple affiliates
affonso coupons create --json \
  --affiliate-id aff_abc123 \
  --code SPRING25 \
  --discount-type percentage \
  --discount-value 25 \
  --duration once

affonso coupons create --json \
  --affiliate-id aff_def456 \
  --code SAVE10 \
  --discount-type fixed \
  --discount-value 10 \
  --duration forever \
  --currency USD

# List all coupons for a program
affonso coupons list --json --program-id prog_xyz

# List coupons for a specific affiliate
affonso coupons list --json --affiliate-id aff_abc123

# Delete an expired coupon (confirm with user first)
affonso coupons delete coup_mno345 --json
```

## 6. Marketplace Discovery

Browse and search the public affiliate marketplace. No authentication required.

```bash
# Browse all programs
affonso marketplace list --json

# Search for programs
affonso marketplace list --json --search "saas"

# Filter by category
affonso marketplace list --json --category software

# Get details on a specific program
affonso marketplace get prog_pqr678 --json
```
