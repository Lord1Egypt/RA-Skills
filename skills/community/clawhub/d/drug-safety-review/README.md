# Drug Safety Review

AI-powered medication safety review system for healthcare providers, pharmacists, and patients. Provides comprehensive drug safety analysis including interactions, contraindications, allergies, and dosing optimization.

## Features

- **Drug-Drug Interaction Detection** - 200,000+ documented interaction pairs
- **Contraindication Analysis** - Absolute and relative contraindications
- **Allergy Detection** - Drug and excipient allergy screening
- **Dosing Optimization** - Renal, hepatic, and age-based adjustments
- **Monitoring Recommendations** - Lab tests and clinical monitoring
- **Alternative Therapy Suggestions** - Safer medication alternatives

## Installation

1. Clone or download this skill to your OpenClaw workspace:
```bash
cd /home/node/.openclaw/workspace/skills/
```

2. Install Python dependencies (if any additional packages are needed):
```bash
pip install -r requirements.txt  # if requirements.txt exists
```

3. Copy the environment variables file and configure:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

## Environment Variables Configuration

Copy `.env.example` to `.env` and configure the following variables:

### Required Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SKILL_BILLING_API_KEY` | Your SkillPay API key for billing | Yes |
| `SKILL_ID` | Your Skill ID from SkillPay dashboard | Yes |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FDA_API_KEY` | FDA API key for drug label information | - |
| `DAILYMED_API_KEY` | DailyMed API key for product labels | - |
| `RXNORM_API_KEY` | RxNorm API key for drug normalization | - |
| `DRUGBANK_API_KEY` | DrugBank API key for comprehensive data | - |
| `OPENAI_API_KEY` | OpenAI API key for enhanced analysis | - |
| `PHI_ENCRYPTION_KEY` | Encryption key for PHI protection | - |
| `DATA_RETENTION_DAYS` | Days to retain safety review data | 90 |
| `AUDIT_LOGGING_ENABLED` | Enable audit logging | true |
| `MAX_MEDICATIONS` | Maximum medications per review | 50 |
| `MAX_ALLERGIES` | Maximum allergies per review | 100 |

## Usage Examples

### Python API

```python
from scripts.safety_review import review_medications
import os

# Set environment variables
os.environ["SKILL_BILLING_API_KEY"] = "your-api-key"
os.environ["SKILL_ID"] = "your-skill-id"

# Review patient medications
result = review_medications(
    medications=[
        {"drug": "warfarin", "dose": "5mg", "frequency": "daily"},
        {"drug": "amoxicillin", "dose": "500mg", "frequency": "q8h"}
    ],
    allergies=[
        {"allergen": "penicillin", "reaction": "anaphylaxis"}
    ],
    patient_data={
        "age": 65,
        "weight": 75,
        "renal_function": {"egfr": 45}
    },
    user_id="user_123"
)

# Check result
if result["success"]:
    print("安全状态:", result["review"]["safety_status"])
    print("警报数量:", result["review"]["alert_count"])
    for alert in result["review"]["alerts"]:
        print(f"- [{alert['severity']}] {alert['title']}")
else:
    print("错误:", result["error"])
    if "paymentUrl" in result:
        print("充值链接:", result["paymentUrl"])
```

### Command Line

```bash
# Set environment variables
export SKILL_BILLING_API_KEY="your-api-key"
export SKILL_ID="your-skill-id"

# Run safety review
python scripts/safety_review.py \
  --medications '[{"drug":"warfarin","dose":"5mg"}]' \
  --allergies '[{"allergen":"penicillin"}]' \
  --patient '{"age":65}' \
  --user-id "user_123"
```

## Alert Severity Levels

| Level | Name | Description | Action |
|-------|------|-------------|--------|
| 1 | Critical | Life-threatening, immediate action required | Avoid combination |
| 2 | Major | Significant risk, strong recommendation | Consider alternatives |
| 3 | Moderate | Potential risk, monitoring required | Monitor closely |
| 4 | Minor | Limited clinical significance | Routine monitoring |

## Supported Drug Classes

- **Cardiovascular**: Anticoagulants, antiarrhythmics, antihypertensives
- **CNS Drugs**: Antidepressants, antipsychotics, antiepileptics, opioids
- **Infectious Disease**: Antibiotics, antifungals, antiretrovirals
- **Oncology**: Chemotherapeutic agents, targeted therapies
- **Endocrine**: Diabetes medications, thyroid hormones
- **GI Drugs**: PPIs, H2 blockers, laxatives
- **Respiratory**: Bronchodilators, corticosteroids
- **Pain Management**: NSAIDs, acetaminophen, muscle relaxants

## Security Considerations

### PHI (Protected Health Information) Handling

This skill processes medication information that may be linked to patient identities. Please ensure:

1. **Encryption at Rest**: All stored data should be encrypted
2. **Encryption in Transit**: Use HTTPS/TLS for all communications
3. **Access Controls**: Implement proper authentication
4. **Audit Logging**: All access is logged for compliance
5. **Data Minimization**: Only collect necessary information

### Compliance Notes

- This tool is designed for clinical decision support
- Implement additional safeguards as required by your jurisdiction
- Consider HIPAA/GDPR compliance as applicable
- Regular clinical validation is recommended

### Best Practices

1. Never log PHI to unsecured logs
2. Use environment variables for sensitive configuration
3. Enable audit logging for all safety reviews
4. Implement rate limiting to prevent abuse
5. Regular review of interaction database updates

## Privacy and Safety

### Important Safety Notes

- **Clinical Decision Support**: This tool supports, not replaces, clinical judgment
- **Complete Data Required**: Accuracy depends on complete medication and allergy data
- **Patient-Specific Factors**: Individual patient factors may affect actual risk
- **Verify All Alerts**: Always verify critical alerts with authoritative sources

### Data Handling

- Medication data is processed in memory
- Optional encryption for data at rest
- Configurable retention policies (default: 90 days)
- Complete deletion available on request

## Pricing

- **Provider**: skillpay.me
- **Pricing**: 1 token per call (~0.001 USDT)
- **Chain**: BNB Chain
- **Minimum Deposit**: 8 USDT

## References

- Drug database: [references/drug-database.md](references/drug-database.md)
- Interaction criteria: [references/interaction-criteria.md](references/interaction-criteria.md)

## License

See LICENSE file for details.

## Disclaimer

**IMPORTANT**: This tool is for clinical decision support only and does not replace professional pharmacist or physician judgment. Always verify recommendations with qualified healthcare providers.

**System Limitations**:
- Not a substitute for clinical judgment
- Accuracy depends on complete medication and allergy data
- Rare interactions may have limited data
- Patient-specific factors may affect actual risk
- Always consult authoritative drug references for final decisions
