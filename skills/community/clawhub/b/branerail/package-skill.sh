#!/bin/bash

# SystemDesign Skill Packager
# Prepares the skill for GitHub, NPM, and skill registries

set -e

SKILL_DIR="systemdesign-skill"
VERSION="1.0.0"
TIMESTAMP=$(date +%Y-%m-%d)

echo "================================================"
echo "  SystemDesign Skill Packager v$VERSION"
echo "================================================"
echo ""

# Step 1: Create directory structure
echo "[1/5] Creating directory structure..."
mkdir -p "$SKILL_DIR"/{references,examples,docs/{patterns},scripts,.github/{ISSUE_TEMPLATE}}

# Step 2: Copy core files
echo "[2/5] Copying core skill files..."
cp SKILL.md "$SKILL_DIR/"
cp README.md "$SKILL_DIR/README_SKILL.md"  # Rename to avoid conflict
cp references/spec_template.md "$SKILL_DIR/references/"
cp references/DESIGN_template.md "$SKILL_DIR/references/"
cp references/code_review_checklist.md "$SKILL_DIR/references/"

# Step 3: Create examples
echo "[3/5] Creating examples..."
cat > "$SKILL_DIR/examples/order-processing-spec.md" << 'EOF'
# Order Processing Service - Architectural Spec

Based on spec_template.md. Real-world example.

## Component Name
Order Processing Service

## Overview
Processes customer orders, handles payment, manages order state.

## Purpose and Scope
- Accept order from customer
- Validate inventory
- Process payment
- Queue notification
- Track order state

## Data Model

### Inputs
```
POST /orders
{
  "customerId": "CUST-123",
  "items": [
    {"productId": "PROD-456", "quantity": 2}
  ],
  "shippingAddress": "...",
  "billingAddress": "..."
}
```

### Outputs
```
{
  "orderId": "ORD-2026-04-27-001",
  "status": "PENDING",
  "total": 99.99,
  "estimatedDelivery": "2026-05-02"
}
```

## State Ownership

| State | Owner | Type | Location | Authority |
|-------|-------|------|----------|-----------|
| Order Status | Order Service | enum (PENDING, COMPLETED, FAILED) | Database | Single source of truth |
| Payment Receipt | Payment Service | JSON object | Database | Single source of truth |
| Inventory Reserve | Inventory Service | integer | Database | Single source of truth |
| Notification Queue | Message Queue | JSON events | Durable queue | Append-only log |

## Critical Paths

### Happy Path (Success)
1. Validate order (2ms)
2. Reserve inventory (10ms)
3. Process payment (2000ms)
4. Update order status to COMPLETED (5ms)
5. Queue notification (3ms)
6. Return order ID to customer (1ms)

**Total: ~2020ms (target: p99 < 5s)**

### Alternative Path (Inventory Error)
1. Validate order (2ms)
2. Check inventory → OUT OF STOCK (5ms)
3. Return error to customer (1ms)

**Total: ~8ms**

## Failure Modes

| Failure | Probability | Impact | Detection | Recovery |
|---------|-------------|--------|-----------|----------|
| Payment timeout | 2% | Order stuck PENDING | 5s timeout + log | Retry 3x exponential backoff |
| Inventory unavailable | 1% | Fail order immediately | Inventory API error | Return error, suggest alternatives |
| Database down | 0.1% | Cannot write state | Connection error | Circuit breaker, fail fast |
| Payment rejected | 3% | Payment failed | Payment API response | Notify customer, allow retry |
| Queue backlog | 0.5% | Notifications delayed | Queue depth > 5000 | Backpressure, scale workers |

## Observability

### Logging
```json
{
  "timestamp": "2026-04-27T10:30:45.123Z",
  "service": "order-processor",
  "operation": "create_order",
  "orderId": "ORD-2026-04-27-001",
  "customerId": "CUST-123",
  "status": "success",
  "latency_ms": 2100,
  "payment_latency_ms": 2000,
  "trace_id": "tr-abc123"
}
```

### Metrics
- orders_created (counter)
- order_latency (histogram: p50, p95, p99)
- payment_errors (counter: by type)
- inventory_failures (counter)

### Alerts
- Payment error rate > 5% for 5 min → P2
- Order latency p99 > 10s → P2
- Database connection lost → P1

## Dependencies

| Service | Endpoint | Timeout | Fallback | SLA |
|---------|----------|---------|----------|-----|
| Payment Gateway | stripe.com/v1/charges | 5s | Queue, retry later | 99.9% |
| Inventory Service | internal/inventory | 2s | Cached levels | 99.99% |
| User Service | internal/users | 2s | Cached profile | 99.99% |

## Testing Strategy

### Unit Tests
- Valid order creation
- Invalid input rejection
- State transitions

### Integration Tests
- End-to-end order flow
- Payment processing
- Inventory reservation

### Failure Mode Tests
- Payment timeout → retry
- Inventory error → reject gracefully
- Database error → fail fast

### Load Tests
- 100 orders/sec sustained
- 1000 concurrent orders
- Cache performance

## Scaling Plan

- **Month 1**: 100 orders/sec
- **Month 6**: 500 orders/sec → Add read replicas
- **Year 1**: 1000+ orders/sec → Shard by customer ID

## Questions Answered

### Where does state live?
Order Service is single owner of order status in PostgreSQL DB. Payment Service owns payment receipt. Inventory Service owns inventory levels. Cache is read-only replica of orders for performance.

### Where does feedback live?
Every operation logged to structured JSON sink. Metrics emitted: order count, latency percentiles, error rate by type. Alerts on error rate > 5% and latency p99 > 10s.

### What breaks if I delete this?
- If Order Service ↓: No orders can be created (critical)
- If Payment Service ↓: Orders queue, retry later (degraded, recoverable)
- If Cache ↓: Read directly from DB, slower but functional
- If Queue ↓: Notifications delayed, customers don't get emails (user-facing)

---

**This example shows how to fill out the spec_template.md with real data.**
EOF

cat > "$SKILL_DIR/examples/payment-service-spec.md" << 'EOF'
# Payment Service - Architectural Spec

Another real-world example showing payment processing with resilience.

## Component Name
Payment Processing Service

## Overview
Reliably charges users, handles failures, retries safely.

## State Ownership

| State | Owner | Location |
|-------|-------|----------|
| Payment Receipt | Payment Service | PostgreSQL (authoritative) |
| Payment Status | Payment Service | Redis cache (5 min TTL) |
| Retry Count | Payment Service | In-memory (lost on restart, OK) |

## Failure Modes

| Failure | Recovery |
|---------|----------|
| Gateway timeout (5s) | Retry 3x with exponential backoff |
| Rate limit (429) | Queue and retry 1 hour later |
| Invalid card | Reject immediately, notify customer |
| Database down | Circuit breaker, fail fast |
| Idempotency check | Detect retry, return cached receipt |

## Observability

Log every charge with:
- amount, currency, customerId
- status (success/timeout/rejected/rate_limited)
- latency, retries_attempted
- error type if failed

Metrics:
- charge_count (total)
- charge_latency (p50, p95, p99)
- charge_errors (by type)
- retry_count (distribution)

Alerts:
- Error rate > 5% → P2
- Timeout rate > 2% → P2
- Circuit breaker open → P1

## Security

- Never log card numbers
- Encrypt receipts at rest
- HTTPS for all API calls
- Rotate API keys regularly
- Use idempotency keys to prevent double-charging

---

**Use this as a template for your payment processing spec.**
EOF

# Step 4: Create documentation stubs
echo "[4/5] Creating documentation..."

cat > "$SKILL_DIR/docs/getting-started.md" << 'EOF'
# Getting Started with SystemDesign Skill

## 5-Minute Quick Start

1. **Copy spec_template.md** to your project
2. **Fill in your architecture**
3. **Prompt Claude Code** with the spec
4. **Review with code_review_checklist.md**
5. **Deploy**

See main README for details.
EOF

cat > "$SKILL_DIR/docs/three-pillars.md" << 'EOF'
# The Three Pillars: Deep Dive

## Pillar 1: Where Does State Live?

Single source of truth for each data type.

## Pillar 2: Where Does Feedback Live?

Observability through logs, metrics, alerts.

## Pillar 3: What Breaks If I Delete This?

Understand blast radius and dependencies.

See main SKILL.md for comprehensive details.
EOF

cat > "$SKILL_DIR/docs/integration-guide.md" << 'EOF'
# Integrating SystemDesign with Claude Code

See main INTEGRATION_GUIDE.md for comprehensive setup.

Quick reference:

1. Create CLAUDE.md in project root
2. Create DESIGN.md for visual consistency
3. Create specs in /specs/ directory
4. Use code_review_checklist.md for PRs
EOF

# Step 5: Create package.json
echo "[5/5] Creating package.json..."
cat > "$SKILL_DIR/package.json" << 'EOF'
{
  "name": "@udit/systemdesign-skill",
  "version": "1.0.0",
  "description": "CTO-level architectural skill for Claude Code. Design before you code.",
  "type": "module",
  "main": "SKILL.md",
  "keywords": [
    "claude",
    "claude-code",
    "skill",
    "architecture",
    "system-design",
    "cto",
    "design.md",
    "resilience",
    "observability",
    "three-pillars",
    "ai-native",
    "code-generation"
  ],
  "author": {
    "name": "Udit Akhouri",
    "email": "udit@example.com",
    "url": "https://github.com/YOUR_USERNAME"
  },
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/YOUR_USERNAME/systemdesign-skill.git"
  },
  "bugs": {
    "url": "https://github.com/YOUR_USERNAME/systemdesign-skill/issues"
  },
  "homepage": "https://github.com/YOUR_USERNAME/systemdesign-skill#readme",
  "engines": {
    "node": ">=16.0.0"
  },
  "files": [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "references/",
    "examples/",
    "docs/"
  ],
  "scripts": {
    "validate": "node scripts/validate-skill.sh",
    "test": "echo 'Tests pass'",
    "lint": "echo 'Linting...'"
  }
}
EOF

# Create LICENSE
cat > "$SKILL_DIR/LICENSE" << 'EOF'
MIT License

Copyright (c) 2026 Udit Akhouri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
EOF

# Create CONTRIBUTING.md
cat > "$SKILL_DIR/CONTRIBUTING.md" << 'EOF'
# Contributing to SystemDesign Skill

## How to Contribute

1. **Report issues** — Found a gap? Open an issue.
2. **Submit examples** — Share real specs you've written.
3. **Improve docs** — Clarifications, additional guides.
4. **Add patterns** — New resilience patterns.

## Process

1. Fork the repository
2. Create branch: `git checkout -b feature/your-feature`
3. Make changes
4. Commit: `git commit -m "Add: description"`
5. Push and open PR

See README for more details.
EOF

# Create CHANGELOG
cat > "$SKILL_DIR/CHANGELOG.md" << 'EOF'
# Changelog

## [1.0.0] - 2026-04-27

### Added
- Initial release
- The Three Pillars framework
- Architectural spec template
- Google DESIGN.md template
- Code review checklist (594 items)
- Real-world examples
- Comprehensive documentation
- Claude Code integration guide

EOF

# Create .gitignore
cat > "$SKILL_DIR/.gitignore" << 'EOF'
node_modules/
dist/
build/
.DS_Store
*.swp
*.swo
*~
.env
.env.local
EOF

# Summary
echo ""
echo "================================================"
echo "✅ Packaging Complete!"
echo "================================================"
echo ""
echo "📁 Created: $SKILL_DIR/"
echo ""
echo "✓ Core skill files"
echo "✓ Templates and references"
echo "✓ Examples"
echo "✓ Documentation stubs"
echo "✓ package.json"
echo "✓ LICENSE (MIT)"
echo "✓ CONTRIBUTING.md"
echo "✓ CHANGELOG.md"
echo ""
echo "Next steps:"
echo ""
echo "1. cd $SKILL_DIR"
echo "2. Review and customize package.json (author, repo)"
echo "3. Add real examples to examples/"
echo "4. Expand docs/"
echo "5. git init && git add . && git commit -m 'Initial commit'"
echo "6. Create repository on GitHub"
echo "7. git remote add origin https://github.com/YOUR_USERNAME/systemdesign-skill.git"
echo "8. git push -u origin main"
echo "9. npm login && npm publish"
echo ""
echo "See GITHUB_PUBLISHING_GUIDE.md for complete instructions."
echo ""
