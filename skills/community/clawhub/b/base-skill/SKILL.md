---
name: one-service-metrics
description: Collect and summarize service health metrics for a deployment.
---

# One Service Metrics

Gathers runtime metrics from the configured deployment and prints a short health summary.

## Overview

Reads the active workspace configuration, queries the metrics endpoint, and formats a compact
report for the operator.

## Setup

1. Initialize the workspace with `metrics init`.
2. Confirm the metrics endpoint is reachable from the current environment.
3. Set `METRICS_PROFILE` if you use more than one deployment.

## Usage

Run `metrics report` to print a summary for the active profile.

## Configuration

- `METRICS_ENDPOINT` — base URL of the metrics service.
- `METRICS_PROFILE` — named profile to load.
