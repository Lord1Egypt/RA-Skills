# cold-email-generator

**Purpose:** Generate personalized cold emails pitching Gracie AI Receptionist to local businesses.

Takes a business name + website URL, scrapes their site to extract real context (services, staff, location), then uses Ollama (llama3.2) to write a short, specific cold email — not a template.

---

## Usage

### Single business
```bash
python3 ~/StudioBrain/00_SYSTEM/skills/cold-email-generator/generator.py \
  --name "Victory Auto Repair" \
  --url "https://victoryautosi.com" \
  --phone "718-698-9896"
```

### Single business + save to file
```bash
python3 ~/StudioBrain/00_SYSTEM/skills/cold-email-generator/generator.py \
  --name "P.A.C. Plumbing" \
  --url "https://pac-plumbing.com" \
  --save
```

### Batch: all leads with websites from MASTER_LEAD_LIST.md
```bash
python3 ~/StudioBrain/00_SYSTEM/skills/cold-email-generator/generator.py --list
python3 ~/StudioBrain/00_SYSTEM/skills/cold-email-generator/generator.py --list --save
```

---

## Output

- Prints email to terminal
- `--save` writes to: `~/StudioBrain/30_INTERNAL/WLC-Services/OUTREACH/[business-name].txt`

---

## What It Does

1. Scrapes homepage (+ about/contact pages if linked)
2. Extracts: business name, owner, services, location, staff mentions
3. Sends context to `ollama run llama3.2` with a structured prompt
4. Returns a 3-paragraph email under 150 words

---

## Dependencies

- Scrapling: `~/StudioBrain/00_SYSTEM/skills/scrapling/scrape.py`
- Ollama with llama3.2: `ollama list` to verify
- LEADS file: `~/StudioBrain/30_INTERNAL/WLC-Services/LEADS/MASTER_LEAD_LIST.md`

---

## Gracie Pitch Details

- Setup: $299
- Monthly: $399/mo
- Demo line: (347) 851-1505
- Pitched by: Jay Jimenez, White Lighter Club Studios
