# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.1] - 2026-11-02

### Fixed

- Ensure that the logo shows up

## [1.5.0] - 2026-11-01

### Added

- Say what transcription sends to Speech is Cheap
- Install and API-key setup for OpenClaw and Hermes Agent

### Changed

- Publish the skill under the `speechischeap` publisher on ClawHub
- Lead the description with what the skill does, as Hermes Agent shows only its start

### Fixed

- Run the helper with `bash` from the skill's folder, since installs drop its executable bit

## [1.4.0] - 2026-10-26

### Changed

- License the skill under MIT-0, which ClawHub requires; the copyright notice stays
- Link the reorganized x402 docs for errors, refunds and webhooks

### Fixed

- Publish to ClawHub with the CLI login and a changelog without the tag signature

## [1.3.0] - 2026-10-25

### Added

- Support for x402 wallet payments.

### Changed

- Summarize the skill's speed, quality and price on ClawHub

## [1.2.0] - 2026-02-01

### Added

- Add `publish.sh` script for publishing the skill to ClawHub

### Fixed

- Ensure the script is executable by publishing it with OpenClaw

## [1.1.0] - 2026-02-01

### Changed

- Update `SKILL.md` based on feedback from an OpenClaw agent

### Fixed

- Make `asr.sh` executable

## [1.0.0] - 2026-02-01

### Added

- Main functionality for the Speech is Cheap ASR skill
