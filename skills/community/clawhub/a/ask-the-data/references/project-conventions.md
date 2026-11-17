# Project Conventions

Recommended but optional layout:

```text
project/
├── data/
│   ├── source-a.xlsx
│   ├── source-b.csv
│   ├── dictionary.md
│   └── codes.xlsx
├── TASK.md
└── outputs/
```

## `data/`

Use for raw/authoritative structured inputs and data dictionaries. Do not require users to rename files purely to satisfy the skill.

## `TASK.md`

Useful for recurring analysis. It may contain questions, definitions, output requirements, and acceptance criteria. Treat it as task intent, not as data truth.

## Persistence

Persist a DuckDB database when:

- the dataset is expensive to reload;
- multiple questions will be asked;
- joins or normalized views should be reused;
- reproducibility benefits from a stable local analytical layer.

For a one-off tiny CSV question, persistence may be unnecessary.
