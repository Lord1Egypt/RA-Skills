# BanditDB API Reference

Base URL: `http://localhost:8080` (default)

## Campaigns

- **Create**: `POST /campaign` — body: `campaign_id`, `arms` (string array), `feature_dim` (int), optional `algorithm` ("lin_ucb" or "thompson_sampling", default: lin_ucb)
- **List**: `GET /campaigns`
- **Get**: `GET /campaign/{campaign_id}`
- **Delete**: `DELETE /campaign/{campaign_id}`

## Predictions

- **Predict**: `POST /predict` — body: `campaign_id`, `context` (float array, length = feature_dim). Returns `arm_id` and `interaction_id`.

## Rewards

- **Record**: `POST /reward` — body: `interaction_id`, `reward` (float, typically 0.0–1.0). Returns "OK".

## Export

- **Parquet**: `GET /export/{campaign_id}` — returns binary Parquet file with propensity-logged interactions. LinUCB only.

## MCP Tools

Register as MCP server for Claude, Cursor, or any MCP-compatible host:

Tools exposed: `create_campaign`, `get_intuition`, `record_outcome`, `campaign_diagnostics`.

## Installation

- **Binary**: available for Linux, macOS, Windows at github.com/dynamicpricing-ai/banditdb/releases
- **Docker**: image `simeonlukov/banditdb:latest` on port 8080
- **Python SDK**: `banditdb-python` on PyPI
