# Publish Checklist

## Skill format

- `SKILL.md` exists at the root of the skill folder.
- Frontmatter keys are single-line.
- `metadata` is a single-line JSON object.
- The skill name is `cde-monitor`.
- The skill folder should also be named `cde-monitor` before packaging or publishing.

## Bundle safety

- No passwords, API keys, cookies, or tokens are checked in.
- All included files are text-based.
- Ignore local caches and virtual environments through `.clawhubignore`.
- Clean `__pycache__`, `.pytest_cache`, `.pyc`, and `.pyo` artifacts before packaging.
- Do not include `.clawhubignore` in the runtime zip that will be uploaded to ClawHub.
- Do not include browser traces, screenshots, downloads, or temporary artifacts.

## Runtime clarity

- `scripts/requirements.txt` lists only the Python dependencies needed to run the skill.
- `references/setup.md` explains Windows and Linux setup.
- `references/queries.md` documents the supported command surface.

## Validation before publish

Run these checks locally:

```bash
python ./scripts/cde_query.py --help
python -m unittest discover -s tests -p "test_*.py"
```

For real release validation, also run at least one live query from each of the six supported query families.

## Build dist artifacts

Use the packaging script from the repository root:

```bash
python ./scripts/build_dist.py
```

This script:

- removes local Python cache artifacts from `scripts/` and `tests/`
- rebuilds `dist/package` and `dist/runtime-package`
- excludes `__pycache__`, `.pyc`, `.pyo`, and `.pytest_cache` from copied contents and zip files

## ClawHub notes

- ClawHub publishing requires MIT-0 acceptance for published skills.
- You can publish from the skill root with a semver version, for example:

```bash
clawhub skill publish . --slug cde-monitor --name "CDE Monitor" --version 1.0.0 --tags latest
```
