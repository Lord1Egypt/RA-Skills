# Frequently Asked Questions (FAQ)

## General Questions

### What is Drug Safety Review?
A comprehensive medication safety analysis tool that checks for drug-drug interactions, contraindications, allergy risks, and dosing optimization. It supports 20,000+ FDA-approved medications with 200,000+ documented interactions.

### Is it free to use?
Yes! Every new user gets **10 free calls** with no credit card required. After that, it's only $0.001 per call.

### Do I need an API key?
- **For the first 10 calls**: No API key needed!
- **After free trial**: Yes, you'll need a SkillPay API key

### Is this a replacement for a pharmacist?
**No!** This tool provides clinical decision support only. Always verify recommendations with qualified healthcare providers.

## Usage Questions

### How accurate is the interaction data?
The drug database includes:
- 20,000+ FDA-approved medications
- 200,000+ documented interactions
- Evidence-based recommendations

### What types of alerts does it generate?
1. **Drug-Drug Interactions** - Effects between multiple medications
2. **Contraindications** - Conditions where drugs shouldn't be used
3. **Allergy Screening** - Drug and cross-reactivity checks
4. **Renal Dosing** - Kidney function-based adjustments

### Can I check a single medication?
Yes, though the tool is most valuable with multiple medications:
```python
review_medications(
    medications=[{"drug": "metformin", "dose": "500mg"}],
    patient_data={"age": 65, "renal_function": {"egfr": 40}}
)
```

### How do I format medication input?
```python
medications = [
    {
        "drug": "warfarin",        # Generic name preferred
        "dose": "5mg",             # Include units
        "frequency": "daily"       # Optional
    }
]
```

## Technical Questions

### What data is stored?
Only **free trial usage counts** are stored locally:
- User ID (hashed)
- Number of calls used
- Timestamps

**No medication data is ever stored or transmitted.**

### Is my data secure?
Yes! See our [Security Policy](SECURITY.md) for details. Key points:
- All analysis happens locally
- No PHI is transmitted over the network
- Drug database is embedded locally
- All code is open source and auditable

### What are the system requirements?
- Python 3.8+
- No external dependencies
- Works completely offline

### Can I integrate this into my EHR system?
Yes, but please:
- Include appropriate disclaimers
- Ensure compliance with healthcare regulations
- Consider liability implications

## Alert Questions

### What do the severity levels mean?
| Level | Description | Action |
|-------|-------------|--------|
| Critical | Life-threatening | Avoid combination |
| Major | Significant risk | Consider alternatives |
| Moderate | Potential risk | Monitor closely |
| Minor | Limited significance | Routine monitoring |

### What if I get a critical alert?
1. Do not dispense/administer the medication
2. Contact the prescriber immediately
3. Document the alert and actions taken
4. Consider suggested alternatives

### Can I override an alert?
The tool provides recommendations, not mandates. However:
- Document the reason for override
- Ensure prescriber is aware
- Monitor patient appropriately

### Why didn't it detect a known interaction?
Possible reasons:
- Drug name variation (use generic names)
- Very rare interaction not in database
- New drug not yet added

Contact us to report missing interactions.

## Billing Questions

### How much does it cost?
- **First 10 calls**: Free
- **After trial**: $0.001 USDT per call

### What payment methods are accepted?
Payments are processed via SkillPay using BNB Chain USDT.

### How do I check my balance?
```python
result = review_medications(...)
print(f"Balance: {result.get('balance')}")
```

### What happens if I run out of balance?
You'll receive a payment URL to top up your account.

## Troubleshooting

### "User ID is required" error
You must provide a user_id parameter:
```python
review_medications(medications=[...], user_id="any_unique_string")
```

### JSON parse error
Ensure proper JSON formatting:
```bash
# ✅ Correct
--medications '[{"drug":"aspirin","dose":"100mg"}]'

# ❌ Incorrect
--medications "{'drug':'aspirin'}"
```

### Permission denied errors
Create the required directory:
```bash
mkdir -p ~/.openclaw/skill_trial
chmod 755 ~/.openclaw
```

### Drug not recognized
Try using the generic (non-brand) name:
```python
# ✅ Correct
{"drug": "atorvastatin"}

# ❌ May not work
{"drug": "Lipitor"}
```

## Clinical Questions

### Does it check pediatric dosing?
Basic age-based checks are included. For detailed pediatric dosing, consult pediatric references.

### Does it check pregnancy/lactation?
Basic contraindication checks are included. Always consult specialized references for pregnancy/lactation safety.

### How often is the database updated?
The drug database is updated quarterly with:
- New FDA approvals
- New interaction data
- Safety alerts and recalls

### Can I export the results?
Yes, save to JSON:
```bash
python scripts/safety_review.py ... --output report.json
```

## Compliance Questions

### Is this FDA approved?
This tool is for clinical decision support only. It is not a medical device and has not been submitted to the FDA.

### Can pharmacists use this?
Yes, as a decision support tool. However:
- Professional judgment should always prevail
- Pharmacists are responsible for final verification
- Document appropriately

### Is this HIPAA compliant?
The tool is designed with HIPAA safeguards:
- No persistent PHI storage
- Local processing
- No data transmission

**However**, you are responsible for ensuring your specific use case complies with HIPAA and other applicable regulations.

## Getting Help

### Where can I get support?
- 📧 Email: support@openclaw.dev
- 💬 Discord: [Join our community](https://discord.gg/openclaw)
- 🐛 GitHub Issues: [Report bugs](https://github.com/openclaw/skills/issues)

### How do I report a bug?
Please include:
1. Medication list (anonymized)
2. Expected vs actual alerts
3. Patient data provided (anonymized)

### Can I request features?
Yes! Please open a feature request on GitHub.

---

**Important**: This tool is for clinical decision support only and does not replace professional pharmacist or physician judgment. Always verify recommendations with qualified healthcare providers.
