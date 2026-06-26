---
version: 1.0.0
name: beta-client-onboarding
description: Manages client onboarding workflows — welcome sequences, document collection, intake forms, kickoff scheduling, and progress tracking. Supports multiple tracks (e.g., SMB vs Enterprise). Generates onboarding checklists and reminds about stalled accounts.
metadata:
  openclaw:
    emoji: "🤝"
    requires:
      bins: [python3]
    always: false
---

# Client Onboarding Skill

## Overview

Handles the complete client onboarding process for Beta AI Agent.

## Features

- Welcome email sequences
- Document collection tracking
- Intake form management
- Kickoff scheduling
- Progress tracking for multiple tracks
- Stalled account reminders

## Usage

Activated automatically when a new client engagement begins.

## Requirements

- Python 3
- Email integration
- Calendar access
