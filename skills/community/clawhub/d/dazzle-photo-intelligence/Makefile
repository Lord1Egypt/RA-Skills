install:
	uv sync --extra dev

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check dazzle_photo_intelligence tests
	uv run ruff format --check dazzle_photo_intelligence tests

format:
	uv run ruff check --fix dazzle_photo_intelligence tests
	uv run ruff format dazzle_photo_intelligence tests

run:
	uv run dazzle

.PHONY: install test lint format run
