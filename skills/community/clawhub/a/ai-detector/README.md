# GPTHumanizer AI Detector Skill for OpenClaw

🌐 **Official Website:** [GPTHumanizer](https://www.gpthumanizer.ai/)

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-Publishable-brightgreen)](https://github.com/openclaw/clawhub)
[![API](https://img.shields.io/badge/API-GPTHumanizer-orange)](https://detect.gpthumanizer.ai/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](#license)

A professional OpenClaw skill for detecting whether text is likely **human-written**, **AI-generated**, **AI-humanized**, or **lightly edited** using the **GPTHumanizer Detection API**.

Designed for lightweight deployment, clean skill packaging, and straightforward publishing to ClawHub.

---

## Overview

This repository provides a production-ready OpenClaw skill package for AI text detection.

It is useful for:

- AI text review workflows
- moderation and quality screening
- pre-submission writing checks
- editorial and compliance analysis
- OpenClaw skill pipelines that need fast classification + probability scoring

The skill returns:

- a final classification label
- aggregated AI-likelihood
- per-class probability distribution
- original input text

---

## Why this repository

OpenClaw skills are distributed as simple folders centered around a `SKILL.md` file, optionally with supporting files. This repository follows that model and keeps the package minimal, readable, and easy to publish. It is well suited for users who want a clean, standalone skill instead of a large plugin or monolithic integration.

---

## Repository Structure

```text
.
├── SKILL.md
├── api.md
└── examples.md
