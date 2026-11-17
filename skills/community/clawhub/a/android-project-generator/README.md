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
├── references/                 # version matrix and config templates
├── scripts/                    # skill runtime helpers (shipped)
│   ├── detect_env.py           # environment audit
│   ├── project_validator.py    # project readiness acceptance bar
│   └── build_flow.py           # assembleDebug / adb orchestration
├── tests/                      # dev-only self-test harness (NOT shipped)
│   ├── run_tests.py            # test runner entrypoint
│   ├── generate_report.py      # report generator
│   ├── report_generator.py     # HTML report renderer
│   ├── sitecustomize.py        # keeps pycache/tmp inside cache/
│   ├── REPORTING.md            # how to generate and view reports
│   ├── unit/ integration/ e2e/ # test suites
│   └── requirements.txt
├── cache/                      # python / pytest / coverage caches (ignored)
└── reports/                    # generated reports (ignored)
```

## Release Scope

The published skill package ships **only the skill runtime**:

```text
SKILL.md  README.md  LICENSE  references/  scripts/
```

`tests/`, `cache/`, and `reports/` are development-only and must not be
included in a release. `.skillignore` at the repository root declares this
exclusion set; packaging tools that honour ignore files pick it up
automatically, otherwise exclude the three directories explicitly.

Runtime code never imports from `tests/`. The skill's workflow (Phase 1-7 in
`SKILL.md`) only invokes `scripts/detect_env.py`, `references/*`, and
`scripts/build_flow.py`.

## Development

All self-test tooling lives under `tests/`:

```bash
python tests/run_tests.py              # run all tests + HTML report
python tests/run_tests.py --unit       # unit tests only
python tests/run_tests.py --open-report
python tests/run_tests.py --report-only
```

Tests never prompt for input; the report is only opened when `--open-report` is
passed explicitly, so the runner is safe for non-interactive use.

See `tests/REPORTING.md` for report details.

## Features

- AGP / Gradle / JDK / Kotlin compatibility profiles
- Local environment detection
- Complete Android project templates
- Real Gradle Wrapper validation
- `assembleDebug` build verification
- APK output confirmation
- JNI / NDK / CMake native project setup
- Build-state reporting: scaffolding_only, build_failed, compiled, runnable

## Roadmap

- Expand Android template coverage
- Add Compose template support
- Add CI matrix for AGP / Gradle / JDK combinations
- Add more JNI / NDK / CMake examples
- Improve China mirror support
- Add GitHub Action for generated project verification
