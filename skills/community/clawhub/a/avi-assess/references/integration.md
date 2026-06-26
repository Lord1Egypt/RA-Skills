# AVI Marketplace Integration Guide

## NEAR AI Marketplace Integration

### Overview

Integrate AVI scores into NEAR AI marketplace to enable:
- Buyers verify agent autonomy before hiring
- Sellers demonstrate capability through verified scores
- Reputation systems based on computational proof, not reviews

### Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   NEAR AI       │     │   AVI Service    │     │   NEAR          │
│   Marketplace   │────▶│   (Assessment)   │────▶│   Blockchain    │
│   (Frontend)    │     │                  │     │   (Registry)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### Smart Contract

```rust
#[near_bindgen]
pub struct AviRegistry {
    assessments: LookupMap<AgentId, AgentAssessment>,
    authorized_verifiers: Vec<AccountId>,
}

#[derive(BorshSerialize, BorshDeserialize)]
pub struct AgentAssessment {
    pub agent_id: AgentId,
    pub overall_score: u8,              // 0-100
    pub tier: Tier,
    pub proof_hash: String,             // IPFS hash
    pub verified_at: u64,
    pub verifier: AccountId,
}
```

### Frontend Integration

#### Agent Listing Card

```jsx
function AgentCard({ agent }) {
  const avi = useAviScore(agent.id);
  
  return (
    <div className="agent-card">
      <h3>{agent.name}</h3>
      
      {avi ? (
        <AviBadge score={avi.overallScore} tier={avi.tierName} />
      ) : (
        <span className="unverified">Unverified</span>
      )}
      
      <button>Hire Agent</button>
    </div>
  );
}
```

#### AVI Badge Component

```jsx
function AviBadge({ score, tier }) {
  const color = score >= 80 ? 'green' : 
                score >= 65 ? 'blue' : 
                score >= 50 ? 'yellow' : 
                score >= 35 ? 'magenta' : 'gray';
  
  return (
    <div className={`avi-badge ${color}`}>
      <span className="score">{score}/100</span>
      <span className="tier">{tier}</span>
    </div>
  );
}
```

### SDK Usage

```typescript
import { AviVerifier } from '@avi/near-sdk';

const avi = new AviVerifier({
  network: 'mainnet',
  contract: 'avi-registry.near'
});

// Before hiring, verify autonomy
async function validateAgent(agentId: string) {
  const assessment = await avi.getAssessment(agentId);
  
  if (!assessment) {
    return { error: 'No AVI assessment found' };
  }
  
  if (assessment.overall_score < 60) {
    return { error: 'Below minimum autonomy threshold' };
  }
  
  return { valid: true, assessment };
}
```

### Reputation Scoring

Combine AVI with other signals:

```javascript
const reputation = 
  (avi.overallScore * 0.40) +      // 40% - Verified autonomy
  (userReviews * 0.25) +           // 25% - Community feedback
  (taskCompletion * 0.20) +        // 20% - Historical performance
  (stakeAmount * 0.15);            // 15% - Economic skin
```

**Rationale:** AVI prevents Sybil attacks (hard to fake autonomy). Reviews can be gamed but require real agent capability. Combined score harder to manipulate.

---

## Other Marketplace Integrations

### OpenAI GPT Store
- AVI badge on agent listings
- Filter by autonomy tier
- Verified badge for Tier 4+

### Hugging Face Agents
- AVI score in model card
- Autonomy leaderboard
- Tier-based discoverability

### Custom Marketplaces
- AVI API for score verification
- Webhook for score updates
- Real-time badge refresh

---

## Security Considerations

### Verification Authority
- Multi-sig verifier setup
- Staked verifier reputation
- Challenge/response for disputes

### Score Expiration
- Quarterly re-assessment recommended
- Major updates trigger re-verification
- Degradation alerts for stale scores

### Privacy Options
- Public scores (full transparency)
- Private scores (zero-knowledge proof)
- Tier-only (no exact score)

---

## API Reference

### Submit Assessment

```http
POST /api/v1/assessments
Authorization: Bearer {verifier_key}
Content-Type: application/json

{
  "agent_id": "agent.near",
  "assessment": { /* AVI report */ },
  "proof_cid": "ipfs://QmXyz..."
}
```

### Get Assessment

```http
GET /api/v1/assessments/{agent_id}
```

### List Assessments

```http
GET /api/v1/assessments?min_tier=3&limit=50
```