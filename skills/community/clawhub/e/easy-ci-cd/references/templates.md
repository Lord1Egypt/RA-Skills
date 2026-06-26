# Minimal CI/CD templates

Use these as patterns, not rigid copy-paste rules.

## Python + GitHub Actions

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip
      - run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - run: python -m compileall .
      - env:
          PYTHONPATH: .
        run: pytest -q
```

## Node + GitHub Actions

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
      - run: npm ci
      - run: npm test -- --runInBand
```

## Tiny source artifact on tags

```yaml
on:
  push:
    tags: ["v*"]

jobs:
  package:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          mkdir -p dist
          git archive --format=tar.gz --output=dist/source-${GITHUB_REF_NAME}.tar.gz HEAD
      - uses: actions/upload-artifact@v4
        with:
          name: source-${{ github.ref_name }}
          path: dist/*.tar.gz
```

## Minimal Python Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

## Minimal .dockerignore

```gitignore
.git/
__pycache__/
.pytest_cache/
.venv/
*.pyc
node_modules/
dist/
build/
```
