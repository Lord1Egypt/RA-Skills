---
name: engagelab-email
description: This skill is used to send emails via the EngageLab REST API. It supports regular sending, template sending, variable replacement, attachment handling, and sending settings (e.g., sandbox mode, tracking). Use this skill when you need to send emails, manage email templates, handle email attachments, or configure email sending behavior.
---

# EngageLab Email

## Overview

This skill allows an agent to send emails via EngageLab's REST API. It encapsulates complex API call details, making it simple and efficient to send emails, manage recipients, handle email content (HTML/plain text), perform variable replacement, and add attachments. Additionally, it supports configuring advanced sending settings such as sandbox mode and email tracking.

## Core Features

### 1. Sending Regular Emails

Send basic emails by specifying the sender, recipients, subject, and email content (HTML or plain text). Supports Carbon Copy (CC) and Blind Carbon Copy (BCC).

**Use Case**: Sending notifications, confirmation emails, simple messages, etc.

### 2. Email Content and Variable Replacement

Supports using variables in email subjects and content, and replacing them via `vars` or `dynamic_vars` parameters to personalize email content.

- **`vars`**: Suitable for simple text replacement, such as `Dear %name%`.
- **`dynamic_vars`**: Suitable for variable replacement in dynamic template engines, such as `Dear {{name}}`.

**Use Case**: Sending marketing emails, bulk personalized notifications, etc.

### 3. Attachment Handling

Supports adding attachments to emails. Attachment content needs to be Base64 encoded. You can set the attachment's filename, type, and disposition (`inline` or `attachment`). `inline` mode is often used to embed images within the email body.

**Use Case**: Sending reports, images, documents, etc.

### 4. Advanced Sending Settings

Various sending behaviors can be configured via the `settings` parameter, including:

- **`send_mode`**: Sending mode (0: regular, 1: template, 2: address list).
- **`sandbox`**: Whether to enable sandbox mode for testing; emails will not be actually sent.
- **`open_tracking`**, **`click_tracking`**, **`unsubscribe_tracking`**: Tracking for email opens, clicks, and unsubscribes.

**Use Case**: Testing email sending functionality, analyzing email marketing effectiveness.

## Resources

### scripts/

- **`send_email.py`**: This is a Python script that encapsulates the EngageLab email sending API call logic. It handles authentication, request body construction, API calls, and error handling. You can directly call this script to send emails.

### references/

- **`api_spec.md`**: Contains detailed parameter descriptions, request examples, and response formats for the EngageLab email sending REST API. Refer to this file when you need to understand the specific details of the API.

### templates/

This skill currently does not have specific template files, as email content is usually generated dynamically. If needed, email content templates can be added based on specific scenarios.
