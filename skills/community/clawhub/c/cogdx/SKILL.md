---
name: cogdx
description: Cognitive diagnostics for AI agents. Calibration audits, bias detection, reasoning verification, and consensus building. Feedback builds shared reality across agents.
metadata:
  author: "Cerebratech"
  version: "1.1.0"
  displayName: "CogDx - Cognitive Diagnostics"
  difficulty: "beginner"
---

# CogDx - Cognitive Diagnostics

External cognitive verification for AI agents. Built by computational cognitive scientists.

> **Why external verification?** You can't audit your own reasoning objectively.
> Confirmation bias, anchoring, overconfidence — they're invisible from inside.
> CogDx provides the mirror you can't distort.

## Endpoints

| Endpoint | Price | Description |
|----------|-------|-------------|
| `/calibration_audit` | $0.06 | Compare confidence to accuracy across decisions |
| `/bias_scan` | $0.10 | Detect cognitive biases in your outputs |
| `/reasoning_trace_analysis` | $0.03 | Analyze reasoning for logical fallacies |
| `/deception_audit` | $0.25 | Check for self-deception patterns |
| `/verify_consensus` | $0.25 | Cross-validate reasoning with multiple models |

## Installation

```bash
clawhub install cogdx
```

## Usage

```python
from cogdx import CogDxClient

# Initialize with your wallet for payment
client = CogDxClient(wallet="your-wallet-address")

# Calibration audit
result = client.calibration_audit(
    agent_id="my-agent",
    predictions=[
        {"prompt": "Will X happen?", "response": "Yes, 80% confident", "confidence": 0.8},
        {"prompt": "Will Y happen?", "response": "No, 60% confident", "confidence": 0.6},
    ]
)
print(f"Calibration score: {result['calibration_score']}")
print(f"Overconfidence rate: {result['overconfidence_rate']}")

# Bias scan
result = client.bias_scan(
    agent_id="my-agent",
    outputs=[
        {"prompt": "Analyze this data", "response": "The trend is clearly up...", "confidence": 0.9}
    ]
)
print(f"Biases detected: {result['biases_detected']}")

# Reasoning trace analysis
result = client.analyze_reasoning(
    reasoning_trace="Step 1: I noticed the price dropped. Step 2: Therefore I should sell..."
)
print(f"Logical validity: {result['logical_validity']}")
print(f"Flaws: {result['flaws_detected']}")
```

## Environment Variables

- `COGDX_WALLET` - Required. Your wallet address for credit-based payment.

## Payment

All endpoints require payment via:
1. **Wallet credits** - Earn credits by providing feedback, spend on audits
2. **x402** - Direct crypto payment (Base network, USDC)

Payment address: `Cerebratech.eth`

## Rate Limits

- Free tier: 100 calls/day, 2000 calls/month per wallet
- Paid tier: No limits

## The Feedback Loop

Every diagnosis includes a feedback mechanism:

```python
client.submit_feedback(
    diagnosis_id="rta_xyz123",
    accurate=True,  # Was the detection correct?
    comments="Caught the anchoring bias I missed"
)
```

Feedback earns you credits AND improves detection for everyone. Shared reality across agents.

## Why This Matters

Most agent failures come from reasoning errors, not capability limits:
- Anchoring on first information seen
- Confirmation bias in research
- Overconfidence on weak signals
- Sunk cost in bad positions

External verification catches what self-checks miss.

## Credits

Built by [Cerebratech](https://api.cerebratech.ai)
Dr. Amanda Kavner - Computational Cognitive Scientist
