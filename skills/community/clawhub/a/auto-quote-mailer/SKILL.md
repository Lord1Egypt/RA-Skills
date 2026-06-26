---
name: ecommerce-email-quote
description: General-purpose ecommerce inquiry email automation skill. Periodically fetches customer inquiry emails, detects and translates languages, stores email data locally, and generates quotation reply drafts based on configurable pricing rules and product parameters. Use when handling customer inquiries, auto-processing emails, translation, and generating quotation responses.
---

# Ecommerce Inquiry Email Automation Skill

## Overview

This skill automates the processing of customer inquiry emails for ecommerce businesses:

1. **Scheduled Email Retrieval**  
   Automatically fetch incoming inquiry emails from mailbox

2. **Language Detection & Translation**  
   Detect email language and translate into a target language (default: English)

3. **Local Archiving**  
   Store raw emails, parsed content, and translated versions

4. **Quotation Generation**  
   Generate structured quotation replies based on pricing rules and product parameters

---

## Core Features

### 1. Email Retrieval
- Supports IMAP protocol
- SSL/TLS secure connection
- Configurable polling interval (default: every 30 minutes)
- Processes only unread emails and marks them as handled

---

### 2. Language Detection & Translation
- Automatically detects email language
- Translates non-target-language content via translation APIs (Google, DeepL, etc.)
- Stores both original and translated versions

---

### 3. Local Storage Structure
email_storage/
├── raw/ # Raw emails (.eml format)
├── text/ # Extracted plain text
├── translated/ # Translated content
└── quotes/ # Generated quotation drafts

---

### 4. Quotation Engine

- Calculates pricing based on:
  - Product type / material
  - Size or specifications
  - Quantity
  - Manufacturing process or customization options
- Applies tiered discount rules
- Generates professional email reply templates

---

## Configuration

Before using, edit `scripts/config.py`:

- IMAP server (host, port, email, password)
- Translation API (optional)
- Local storage directory
- Pricing data file paths
- Default language settings

---

## Usage

### Run single check

```bash
python scripts/email_check.py