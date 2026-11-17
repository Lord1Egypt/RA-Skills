# Garden Doctor

An agent skill that diagnoses plant health problems from symptoms and provides treatment plans and prevention tips.

## Features

- 🌿 **40+ common plant problems** in the knowledge base
- 🔍 **Symptom-based diagnosis** with confidence scoring
- 💊 **Step-by-step treatment plans** for each diagnosis
- 🛡️ **Prevention tips** to stop recurrence
- 🐛 **Pest identification** (aphids, spider mites, gnats, whiteflies, more)
- 🌱 **Plant-type awareness** — filters diagnoses relevant to specific plants

## Installation

```bash
cp -r garden-doctor /path/to/skills/
```

## Usage

```bash
# Diagnose a plant problem
python3 scripts/garden_doctor.py diagnose \
  --plant "tomato" \
  --symptoms "yellow leaves" "brown spots" "drooping"

# List all known problems
python3 scripts/garden_doctor.py list

# Show details of a specific problem by ID
python3 scripts/garden_doctor.py info --id spider_mites

# Search problems by symptom keyword
python3 scripts/garden_doctor.py search --symptom "yellow leaves"
```

## Output Format

Diagnosis results are JSON:

```json
{
  "plant": "tomato",
  "symptoms_reported": ["yellow leaves", "brown spots"],
  "diagnoses": [
    {
      "id": "early_blight",
      "name": "Early Blight",
      "confidence": 0.80,
      "matched_symptoms": 2,
      "cause": "Fungal infection (Alternaria solani)",
      "treatment": ["Remove affected leaves", "Apply copper fungicide", ...],
      "prevention": ["Rotate crops", "Water at soil level", ...]
    }
  ]
}
```

## Supported Plant Types

The knowledge base covers problems applicable to: tomatoes, peppers, roses, monstera, pothos, succulents, orchids, ferns, herbs (basil, mint), cucumbers, lettuce, citrus, fiddle leaf fig, snake plant, and general houseplants.

## Reference Documentation

- [Knowledge Base](references/knowledge-base.md) — full catalog of 40+ problems
- [Symptoms Guide](references/symptoms-guide.md) — symptom-to-cause quick reference

## Disclaimer

⚠️ For informational purposes only. For valuable, rare, or commercially important plants, consult a local horticulturist or agricultural extension service.

## License

MIT © Denis Voronin
