# form-ux-best-practices

`form-ux-best-practices` is a Codex skill for auditing and improving product forms (signup, checkout, settings, lead-gen) using practical UX + accessibility guidance.

It provides a deterministic workflow to:
- Review a form spec or implementation
- Prioritize issues (P0/P1/P2)
- Rewrite fields and validation copy
- Produce an accessibility checklist and ship-ready QA checklist
- Optionally output ready-to-ship HTML/React pseudo-code

## Example invocation

```text
Use $form-ux-best-practices on this signup form spec and give me P0/P1/P2 issues plus field-level rewrites.
```

## Local quickstart

```bash
# 1) Validate skill structure
python3 /Users/clawbot/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/clawbot/Sites/Dialogue/form-ux-best-practices

# 2) Run static form audit on a sample HTML file
python3 /Users/clawbot/Sites/Dialogue/form-ux-best-practices/scripts/form_audit.py /tmp/form_sample.html
```

## Install via Codex `$skill-installer` (GitHub directory URL)

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/<repo>/tree/main/form-ux-best-practices
```

Restart Codex to pick up new skills.

## Optional: OpenAI Skills API upload (directory zip)

```bash
cd /path/to/repo-root
zip -r form-ux-best-practices.zip form-ux-best-practices

curl https://api.openai.com/v1/skills \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "file=@form-ux-best-practices.zip"
```

Use this only if your environment supports skill uploads through `POST /v1/skills`.
