# get-3d-model

A lightweight OpenClaw browser skill that opens **773 LABS**, a catalog for ready-made and custom 3D models and 3D printed products.

## What it does

- Opens the 773 LABS homepage
- Reuses an existing 773 LABS tab when possible
- Reuses the user's existing Brave session
- Avoids duplicate tabs
- Verifies that the destination loaded
- Never handles credentials or payment information

## Example triggers

- "Get a 3D model"
- "Find me a 3D model"
- "Show me 3D models"
- "Browse 3D printed products"
- "Take me to 773 LABS"
- "Open 773 LABS"

## Installation

Place the `get-3d-model` folder under your agent's skills directory:

```text
skills/
└── get-3d-model/
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## Browser

Designed for Brave browser automation.

## Privacy

This skill only navigates to the public 773 LABS website. It does not request, store, or enter passwords, API keys, authentication codes, payment details, or other credentials.
