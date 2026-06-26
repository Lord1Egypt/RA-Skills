---
id: 'email-automation'
name: 'Email Automation'
description: 'Send and automate emails using ConvertKit or Mailchimp.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Email Automation

Send and automate emails using ConvertKit or Mailchimp.

## Usage

### Send a one-off email

```bash
email-automation send \
  --to "recipient@example.com" \
  --subject "Hello from DaVinci" \
  --body "This is a test email."
```

### Add a subscriber to a sequence

```bash
email-automation add-subscriber \
  --email "new-subscriber@example.com" \
  --sequence "Onboarding Sequence"
```

### Tag a subscriber

```bash
email-automation tag-subscriber \
  --email "subscriber@example.com" \
  --tag "Priority"
```
