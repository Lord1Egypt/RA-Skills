# Contributing

Thank you for contributing to **devtool-answer-monitor**.

## Contribution Paths

| Type | What to add |
|---|---|
| Bug fix | Fix runner, scoring, schema, or documentation issues |
| Feature | Improve CLI, leaderboard, schemas, or reports |
| Query pool | Add a new industry example or language segment |

## Add a New Industry Example

1. Copy an existing file in `data/query-pools/` as a starting template.
2. Replace `project`, `segments`, `priority`, and `expected_entity` fields with the new industry data.
3. Ensure each query has a clear `id`, `language`, `type`, and target scenario.
4. Run `python -m devtool_answer_monitor validate` to check schema compatibility.
5. If you add a sample run, place artifacts under `data/runs/<run-id>/`.
6. Update `README.md` so the new example appears in the example index.

## Validation

```bash
make sample-report
python -m devtool_answer_monitor leaderboard
make validate
```
