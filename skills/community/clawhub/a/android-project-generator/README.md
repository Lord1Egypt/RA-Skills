# android-project-generator
When generating an Android project from scratch, it can be compiled successfully in one go.

## Python Environment

- Python 3.10+ recommended
- Install test dependencies before running scripts that call pytest:

```bash
python -m pip install -r tests/requirements.txt
```

## Directory Layout

```text
android-project-generator/
├── SKILL.md                    # skill entrypoint
├── README.md
├── LICENSE
├── docs/                       # one human-facing guide: reporting
├── cache/                      # python / pytest / coverage caches
├── references/                 # version matrix and config templates
├── scripts/                    # executable helpers
│   ├── run_tests.py            # test runner entrypoint
│   └── generate_report.py      # report generator
├── tests/                      # unit / integration / e2e tests
└── reports/                    # generated reports (ignored)
```
