# Autoresearch Config for dialogflow-cx-to-ces-migration

## Target Skill
`skills/dialogflow-cx-to-ces-migration/SKILL.md`

## Test Inputs (5 scenarios)

1. **carconnect (full)** — `python migrate.py --project genaiguruyoutube --agent-id 3736c564-5b3b-4f93-bbb2-367e7f04e4e8 --output ./test_output_1`
2. **carconnect (dry-run)** — `python migrate.py --project genaiguruyoutube --agent-id 3736c564-5b3b-4f93-bbb2-367e7f04e4e8 --dry-run`
3. **Hair Saloon** — `python migrate.py --project genaiguruyoutube --agent-id 1505de89-6337-4d07-9537-719dabc5e9da --output ./test_output_3`
4. **dental-voice-receptionist** — `python migrate.py --project genaiguruyoutube --agent-id 2da0df19-893b-4c76-916e-968cb6c6884d --output ./test_output_4`
5. **halfwebhook** — `python migrate.py --project genaiguruyoutube --agent-id def1abb4-bd23-49b2-b263-fb508df325c4 --output ./test_output_5`

## Eval Criteria (6 binary checks)

Run `python evals.py --output-dir <output_dir>` after each test.

| # | Name | Pass Condition |
|---|------|---------------|
| 1 | EVAL_FLOWS | `ces_agent.json` contains ≥1 sub-agent entry |
| 2 | EVAL_TOOLS | All webhooks → tools with OpenAPI `textSchema` |
| 3 | EVAL_ENTITIES | `entity_types.json` non-empty with name+entities fields |
| 4 | EVAL_EVALS_CSV | `golden_evals.csv` has required headers + ≥1 eval row |
| 5 | EVAL_INSTRUCTIONS | Every sub-agent has non-empty `instruction` field |
| 6 | EVAL_REPORT | `migration_report.md` has Stats + Next Steps sections |

## Runs per Experiment
5

## Max Score
30 (6 evals × 5 runs)

## Stop Condition
90%+ (27/30) for 3 consecutive experiments
