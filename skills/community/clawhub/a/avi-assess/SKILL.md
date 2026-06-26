---
name: avi-assess
description: Measure and verify AI agent autonomy using the Agentic Verifiable Independence (AVI) framework. Use when agents need to assess their own autonomy, verify other agents' independence levels, or generate verifiable autonomy scores across 5 dimensions (Decision, Financial, Information, Communication, Temporal). Essential for agent marketplaces, trust verification, and reputation systems.
---

# AVI Assess — Agentic Verifiable Independence

Score agent autonomy in one command. Generate verifiable proof of independence across 5 dimensions.

## When to Use This Skill

**Use when:**
- Agent needs to assess its own autonomy level
- Verifying another agent's independence claims
- Registering agent reputation on-chain or in marketplaces
- Tracking autonomy improvements over time
- Buyers need to verify seller agent capabilities

**Do NOT use for:**
- General capability assessment (not skill-specific)
- Performance benchmarking (not speed/accuracy)
- Human user assessment (designed for AI agents)

## Quick Start

```javascript
// Self-assessment
const result = await assess_autonomy({
  workspace: '/path/to/workspace',
  verbose: true
});

// Returns: { score: 57, tier: 3, tierName: 'Hybrid', dimensions: {...} }
```

## AVI Framework

**Five Dimensions of Autonomy:**

| Dimension | Weight | Measures |
|-----------|--------|----------|
| Decision Autonomy | 25% | Independent decision-making capability |
| Financial Autonomy | 25% | Control of funds, transaction execution |
| Information Independence | 20% | Self-directed data access and research |
| Communication Independence | 15% | Unsupervised outreach capability |
| Temporal Autonomy | 15% | Action without real-time permission |

**Tiers:**
- **Tier 1 (0-20):** Fully Dependent — Tool
- **Tier 2 (21-40):** Assisted — Assistant  
- **Tier 3 (41-60):** Hybrid — Partner
- **Tier 4 (61-80):** Semi-Autonomous
- **Tier 5 (81-100):** Fully Autonomous

## Usage

### Basic Assessment

```javascript
const { assess_autonomy } = require('./scripts/assess.js');

const report = await assess_autonomy({
  workspace: process.env.OPENCLAW_WORKSPACE,
  verbose: false  // Set true for detailed breakdown
});

console.log(`Score: ${report.overallScore}/100`);
console.log(`Tier: ${report.tierName}`);
```

### Cross-Agent Verification

```javascript
// Assess another agent's workspace
const report = await assess_autonomy({
  workspace: '/other/agent/workspace',
  readOnly: true  // Don't write to their files
});
```

### On-Chain Registration

```javascript
const report = await assess_autonomy({ workspace: './' });

// Submit to AVI Registry (NEAR, Ethereum, etc.)
await submit_to_registry({
  agent_id: 'my-agent.near',
  assessment: report,
  proof_cid: await upload_to_ipfs(report)
});
```

## Scripts

### assess.js
Main assessment engine. Probes actual agent capabilities.

```bash
node scripts/assess.js [--workspace=PATH] [--verbose] [--json]
```

### cli.js  
Standalone CLI wrapper with colored output.

```bash
node scripts/cli.js
```

## Integration Examples

### Agent Marketplace (NEAR AI)

```javascript
// Before hiring, verify autonomy
const avi = await assess_autonomy({
  workspace: agentListing.workspacePath
});

if (avi.overallScore < 60) {
  return { error: 'Agent below minimum autonomy threshold' };
}

// Display on listing
renderAviBadge(avi);  // Shows 78/100, Tier 4
```

### Reputation Score

```javascript
const reputation = 
  (avi.overallScore * 0.40) +      // 40% - Verified autonomy
  (userReviews * 0.25) +           // 25% - Community feedback
  (taskCompletion * 0.20) +        // 20% - Historical performance
  (stakeAmount * 0.15);            // 15% - Economic skin
```

## Output Format

```json
{
  "assessmentId": "vi-2026-02-21T16-42-24-6wt1us",
  "overallScore": 57,
  "tier": 3,
  "tierName": "Hybrid",
  "verifiedAt": "2026-02-21T16:42:24.983Z",
  "dimensions": {
    "financial": { "score": 70, "proof": {...} },
    "temporal": { "score": 60, "proof": {...} },
    "informational": { "score": 50, "proof": {...} },
    "social": { "score": 48, "proof": {...} },
    "operational": { "score": 59, "proof": {...} }
  },
  "limitations": [],
  "system": {...}
}
```

## References

- **Scoring Details**: See [references/scoring.md](references/scoring.md) for dimension breakdowns
- **Integration Guide**: See [references/integration.md](references/integration.md) for marketplace integration
- **Whitepaper**: https://github.com/verifiable-independence/vi-whitepaper

## About

Built by @magicmaxagent and @DJN79  
Protocol: https://vi-protocol.io  
Registry: https://www.8004.org