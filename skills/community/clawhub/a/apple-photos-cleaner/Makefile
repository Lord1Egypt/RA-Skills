# Makefile for apple-photos-cleaner skill
#
# All targets run inside a local virtualenv at ./.venv, created on demand.
# Homebrew and system Pythons are "externally managed" (PEP 668) and refuse
# `pip install`, so installing into a venv is the only thing that works out of
# the box on macOS.

PYTHON ?= python3
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python
PYTEST := $(VENV_PYTHON) -m pytest
STAMP := $(VENV)/.install-stamp

.PHONY: help test coverage lint format check typecheck clean distclean install venv

help:
	@echo "Apple Photos Cleaner - Makefile targets:"
	@echo "  make install    - Create ./.venv and install dev/test dependencies"
	@echo "  make test       - Run tests"
	@echo "  make coverage   - Run tests with coverage report"
	@echo "  make lint       - Lint with ruff"
	@echo "  make format     - Auto-format with ruff"
	@echo "  make typecheck  - Type check with mypy"
	@echo "  make check      - Lint + format check + tests"
	@echo "  make clean      - Remove test artifacts"
	@echo "  make distclean  - Remove test artifacts and ./.venv"

$(VENV_PYTHON):
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --quiet --upgrade pip

# Reinstall whenever the dependency declaration changes.
$(STAMP): pyproject.toml | $(VENV_PYTHON)
	$(VENV_PYTHON) -m pip install -e ".[dev]"
	@touch $(STAMP)

venv: $(VENV_PYTHON)

install: $(STAMP)

test: $(STAMP)
	$(PYTEST) tests/ -v

coverage: $(STAMP)
	$(PYTEST) tests/ -v --cov=scripts --cov-report=term-missing --cov-report=html

lint: $(STAMP)
	$(VENV_PYTHON) -m ruff check .

format: $(STAMP)
	$(VENV_PYTHON) -m ruff format .

typecheck: $(STAMP)
	$(VENV_PYTHON) -m mypy

check: lint
	$(VENV_PYTHON) -m ruff format --check .
	$(PYTEST) tests/ -v

clean:
	rm -rf __pycache__ tests/__pycache__ scripts/__pycache__
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

distclean: clean
	rm -rf $(VENV)

.DEFAULT_GOAL := help
