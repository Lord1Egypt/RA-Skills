# benos-bootstrap

BenOS Bootstrap is a system-initialization skill for OpenClaw-based agent stacks.

## Purpose

This skill initializes a BenOS runtime environment inside OpenClaw. It performs startup validation, establishes baseline state, and ensures required system dependencies are reachable before other BenOS skills execute.

## What It Does

- Verifies workspace structure and sandbox integrity
- Confirms agent runtime configuration is valid
- Checks required environment variables
- Validates Node runtime compatibility
- Returns structured health status for orchestration logic

## Why It Exists

BenOS is designed as a deterministic, structured executive runtime overlay. The bootstrap layer ensures predictable startup behavior and prevents downstream skills from executing in an inconsistent environment.

This skill is intentionally lightweight but foundational. It is meant to run prior to advanced orchestration or automation layers.

## Usage

This skill is invoked during startup or manually when system validation is required.

Example:

Run benos-bootstrap to verify runtime health before deploying additional automation modules.

## Output

Returns structured JSON with:

- ok (boolean)
- message (string)
- environment metadata (future expansion)

## Roadmap

Future versions will:
- Add environment diff detection
- Integrate structured logging
- Support pre-flight dependency resolution
