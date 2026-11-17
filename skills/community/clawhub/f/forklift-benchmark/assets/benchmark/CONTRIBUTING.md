# Contributing to FK-Bench v2

Thank you for your interest in improving the **Forklift Embodied Intelligence
Benchmark v2** (FK-Bench v2). This document explains how to set up a
development environment, how to propose changes, and what we expect from
contributions in terms of style, testing, and licensing.

## 1. Code of Conduct

By participating in this project you agree to abide by the
[Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
Please be respectful, assume good faith, and focus on technical merit.

## 2. Ways to contribute

There are many ways to help, in roughly increasing order of effort:

- **Report a bug.** Open an issue with a minimal reproduction script, the
  command you ran, and the observed vs. expected behaviour.
- **Suggest a new evaluation module.** Open an issue describing the
  industrial scenario, the expected action vocabulary, and the red-line
  conditions. The maintainers will triage.
- **Improve documentation.** Typos, missing examples, broken links, and
  clearer diagrams are all welcome.
- **Add a fixture or unit test.** Even a single regression test for a
  bug you found is valuable.
- **Submit a code change.** A bug fix, a new validator, a new scorer
  heuristic, a new attachment, or a new scene.

## 3. Development environment

The project targets Python 3.9 through 3.12. To set up a working
environment:

```bash
git clone https://github.com/forklift-benchmark/forklift-benchmark-v2.git
cd forklift-benchmark-v2
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e ".[dev]"
```

The dev extras install `pytest`, `pytest-cov`, and `ruff`.

## 4. Running the tests

```bash
pytest -v
```

A green CI run is required for any pull request to be merged. New
behaviour must be accompanied by tests; behaviour changes must update
existing tests.

## 5. Code style

- We follow PEP 8 with a 100-character line limit (`ruff` is configured
  in `pyproject.toml`).
- Prefer explicit, typed signatures (`from __future__ import annotations`
  is encouraged in new modules).
- Use `pydantic` v2 models for all structured data crossing module
  boundaries; do not pass raw `dict` objects between the DSL, generator,
  validator, and scorer.
- Avoid hidden global state inside the scoring engine. The `scorer` and
  `validator` subpackages must be deterministic given the same input and
  the same RNG seed.

## 6. Pull-request workflow

1. Fork the repository and create a topic branch, e.g.
   `git checkout -b feat/vna-derated-load-fixture`.
2. Make focused commits with descriptive messages. Squash cosmetic fix-ups.
3. Make sure `pytest -v` and `ruff check .` are both green locally.
4. Update `CHANGELOG.md` under the "Unreleased" section.
5. Open a pull request that:
   - References the issue it closes (`Closes #123`).
   - Includes a short rationale and a before/after note.
   - Adds or updates tests demonstrating the change.
6. A maintainer will review and either request changes or merge. Please
   respond to review comments within two weeks; otherwise the PR may be
   closed to keep the queue manageable.

## 7. Dataset contributions

We **do** accept well-justified additions to the 500-item dataset, but
they go through a stricter review:

- New items must conform to the Pydantic schema in `dsl/schema.py`.
- The module × difficulty distribution must remain balanced. Coordinate
  with the maintainers before adding more than 5 items.
- New items must include a gold action plan written by a domain expert.
- The label file must reference any standard (GB/T 43756, ISO 3691-1,
  ISO 23308, TSG 11) the item depends on, with a one-line quote.

## 8. Licensing

By contributing, you agree that your contributions will be licensed
under the Apache License 2.0, the same license that covers the
repository. If you bring in third-party code, it must be compatible
with Apache-2.0 and clearly attributed in the commit message and in
the source files.

## 9. Security

If you discover a vulnerability — for example, a way to make the
validator accept a clearly unsafe plan — please **do not** open a public
issue. Email the maintainers privately (see `CITATION.cff` for the
contact address) and we will coordinate a fix and an advisory.

## 10. Recognition

Contributors are listed in `CITATION.cff` and in the release notes.
Significant contributions to the dataset, validator, or scoring engine
are noted as co-authors of the corresponding release.

Thank you for helping make industrial embodied AI safer and more
rigorously evaluated.
