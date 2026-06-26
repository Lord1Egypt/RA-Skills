# 🚀 Getting Started

Get up and running with Drug Safety Review in 5 minutes!

## ⚡ Quick Start (Zero Configuration)

The fastest way to try the skill - no setup required!

### Step 1: Run the Demo
```bash
cd /home/node/.openclaw/workspace/skills/drug-safety-review
python demo.py
```

This will:
- Review 3 sample medication scenarios
- Show safety alerts and interactions
- Demonstrate risk assessment

### Step 2: Try with Your Own Medications
```bash
python demo.py --medications '[{"drug":"aspirin","dose":"100mg"}]' \
               --allergies '[{"allergen":"ibuprofen"}]' \
               --patient '{"age":65}'
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies
```bash
# No external dependencies required!
# The skill uses only Python standard library
```

## 🎯 Basic Usage

### Using the Demo Script
```bash
# Run with built-in examples
python demo.py

# Run with custom medications
python demo.py --medications '[{"drug":"metformin","dose":"500mg"}]' \
               --patient '{"age":70,"renal_function":{"egfr":40}}'

# Save output to file
python demo.py --output safety_report.json
```

### Using the Python API
```python
from scripts.safety_review import review_medications

# Review medications (free trial - no API key needed!)
result = review_medications(
    medications=[
        {"drug": "warfarin", "dose": "5mg", "frequency": "daily"},
        {"drug": "amoxicillin", "dose": "500mg", "frequency": "q8h"}
    ],
    allergies=[
        {"allergen": "penicillin", "reaction": "rash"}
    ],
    patient_data={
        "age": 65,
        "weight": 75,
        "renal_function": {"egfr": 45}
    },
    user_id="user_123"
)

print(f"Safety Status: {result['review']['safety_status']}")
print(f"Alert Count: {result['review']['alert_count']}")
```

### Using Command Line
```bash
python scripts/safety_review.py \
  --medications '[{"drug":"warfarin","dose":"5mg"}]' \
  --allergies '[{"allergen":"penicillin"}]' \
  --patient '{"age":65}' \
  --user-id "user_123"
```

## 🎁 Free Trial

Every new user gets **10 free calls** - no credit card required!

```python
result = review_medications(
    medications=[{"drug": "aspirin", "dose": "100mg"}],
    user_id="your_unique_user_id"  # Any string works!
)

# Check remaining free calls
if result.get("trial_mode"):
    print(f"剩余免费次数: {result['trial_remaining']}")
```

## 💳 After Free Trial

When your free trial ends:

1. Get an API key from [skillpay.me](https://skillpay.me)
2. Set environment variable:
   ```bash
   export SKILL_BILLING_API_KEY="your-api-key"
   export SKILL_ID="your-skill-id"
   ```
3. Continue using the skill - only $0.001 per call!

## 📋 Input Format

### Medications
```python
medications = [
    {
        "drug": "warfarin",        # Drug name (generic)
        "dose": "5mg",             # Dose amount
        "frequency": "daily"       # Frequency (optional)
    },
    {
        "drug": "metformin",
        "dose": "500mg",
        "frequency": "twice daily"
    }
]
```

### Allergies
```python
allergies = [
    {
        "allergen": "penicillin",  # Allergen name
        "reaction": "anaphylaxis"  # Reaction type (optional)
    },
    {
        "allergen": "sulfa",
        "reaction": "rash"
    }
]
```

### Patient Data
```python
patient_data = {
    "age": 65,                     # Years
    "weight": 75,                  # kg
    "conditions": ["diabetes", "hypertension"],
    "renal_function": {
        "egfr": 45                 # mL/min/1.73m²
    },
    "hepatic_function": "normal"
}
```

## 📤 Output Format

The skill returns comprehensive safety analysis:

```json
{
  "review": {
    "review_id": "SAFETY_20240306120000",
    "timestamp": "2024-03-06T12:00:00",
    "safety_status": "requires_intervention",
    "risk_score": {
      "score": 15,
      "level": "high",
      "safety_status": "requires_intervention"
    },
    "medication_count": 2,
    "alert_count": 2,
    "alerts": [
      {
        "alert_id": "ALLERGY-AMO",
        "severity": "critical",
        "category": "allergy",
        "title": "Amoxicillin - Known Allergy",
        "description": "Patient has documented penicillin allergy with anaphylaxis",
        "recommendation": "Avoid Amoxicillin. Use alternative medication.",
        "monitoring": ["for allergic reaction signs"]
      }
    ],
    "recommendations": [
      {
        "type": "alternative_therapy",
        "for_alert": "ALLERGY-AMO",
        "alternatives": [
          {"drug": "doxycycline", "reasoning": "No significant interaction"}
        ]
      }
    ]
  }
}
```

## 🚨 Alert Severity Levels

| Level | Description | Action Required |
|-------|-------------|-----------------|
| Critical | Life-threatening | Avoid combination |
| Major | Significant risk | Consider alternatives |
| Moderate | Potential risk | Monitor closely |
| Minor | Limited significance | Routine monitoring |

## 💊 Supported Drug Classes

- **Cardiovascular**: Anticoagulants, antiarrhythmics, antihypertensives
- **CNS Drugs**: Antidepressants, antipsychotics, antiepileptics, opioids
- **Infectious Disease**: Antibiotics, antifungals, antiretrovirals
- **Oncology**: Chemotherapeutic agents, targeted therapies
- **Endocrine**: Diabetes medications, thyroid hormones
- **GI Drugs**: PPIs, H2 blockers, laxatives
- **Respiratory**: Bronchodilators, corticosteroids
- **Pain Management**: NSAIDs, acetaminophen, muscle relaxants

## 🔧 Troubleshooting

### "User ID is required"
Make sure to provide a user_id parameter:
```python
review_medications(medications=[...], user_id="any_unique_id")
```

### JSON Parse Error
Ensure your JSON is properly formatted:
```bash
# ✅ Correct
--medications '[{"drug":"aspirin","dose":"100mg"}]'

# ❌ Incorrect
--medications "{'drug':'aspirin'}"  # Use double quotes
```

### Permission Denied
If you see permission errors for `~/.openclaw/`:
```bash
mkdir -p ~/.openclaw/skill_trial
chmod 755 ~/.openclaw
```

## ⚠️ Important Disclaimer

**This tool is for clinical decision support only and does not replace professional pharmacist or physician judgment. Always verify recommendations with qualified healthcare providers.**

## 📚 Next Steps

- Read the [full documentation](SKILL.md)
- Check out [examples](EXAMPLES.md)
- See [FAQ](FAQ.md) for common questions
- Review [security policy](SECURITY.md)

## 💬 Need Help?

- 📧 Email: support@openclaw.dev
- 💬 Discord: [Join our community](https://discord.gg/openclaw)
- 🐛 Issues: [GitHub Issues](https://github.com/openclaw/skills/issues)

---

**Safe Medication! 💊**
