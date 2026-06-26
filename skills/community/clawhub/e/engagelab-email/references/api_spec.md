# EngageLab Email REST API Detailed Specification

## POST /v1/mail/send

### Overview
This API is used to send emails through the EngageLab platform. It supports various sending methods, including single emails, bulk emails, template emails, and emails with attachments.

### Request URL
- **Singapore Data Center**: `https://email.api.engagelab.cc/v1/mail/send`
- **Turkey Data Center**: `https://emailapi-tr.engagelab.com/v1/mail/send`

### Request Method
`POST`

### Request Headers
| Header        | Type   | Required | Description                                       |
| ------------- | ------ | -------- | ------------------------------------------------- |
| Content-Type  | String | Yes      | `application/json;charset=utf-8`                  |
| Authorization | String | Yes      | `Basic base64(api_user:api_key)`, for authentication |

### Request Body
The request body is a JSON object containing the following top-level fields:

| Parameter        | Type           | Required | Description                                       |
| ---------------- | -------------- | -------- | ------------------------------------------------- |
| `from`           | String         | Yes      | Sender email address. Format: `"Sender Name<sender@example.com>"` or `"sender@example.com"`. |
| `to`             | Array of String| Yes      | Recipient email addresses. Max 100 recipients per call. Format: `["recipient1@example.com", "Recipient2 Name<recipient2@example.com>"]`. |
| `cc`             | Array of String| No       | Carbon Copy recipient email addresses.            |
| `bcc`            | Array of String| No       | Blind Carbon Copy recipient email addresses.      |
| `reply_to`       | Array of String| No       | Reply-To email addresses.                         |
| `subject`        | String         | Yes      | Email subject.                                    |
| `content`        | Object         | Yes      | Email content, can include `html`, `text`, `preview_text`. |
| `vars`           | Object         | No       | Variables for content replacement (e.g., `{"name": ["John Doe"]}`). |
| `dynamic_vars`   | Array of Object| No       | Dynamic variables for template engines.           |
| `label_id`       | Integer        | No       | Label ID for email classification.                |
| `label_name`     | String         | No       | Label name for email classification.              |
| `headers`        | Object         | No       | Custom email headers.                             |
| `attachments`    | Array of Object| No       | Email attachments. Each object contains `content` (Base64 encoded), `filename`, `type`, `disposition`. |
| `settings`       | Object         | No       | Advanced sending settings (e.g., `sandbox`, `open_tracking`). |
| `custom_args`    | Object         | No       | Custom arguments for tracking.                    |
| `request_id`     | String         | No       | Unique request ID for idempotency.                |

### `content` Object Fields

| Parameter        | Type   | Required | Description                                       |
| ---------------- | ------ | -------- | ------------------------------------------------- |
| `html`           | String | No       | HTML content of the email.                        |
| `text`           | String | No       | Plain text content of the email.                  |
| `preview_text`   | String | No       | Preview text for the email.                       |

### `attachments` Object Fields

| Parameter        | Type   | Required | Description                                       |
| ---------------- | ------ | -------- | ------------------------------------------------- |
| `content`        | String | Yes      | Base64 encoded content of the attachment.         |
| `filename`       | String | Yes      | Filename of the attachment.                       |
| `type`           | String | Yes      | MIME type of the attachment (e.g., `image/png`, `application/pdf`). |
| `disposition`    | String | Yes      | `inline` or `attachment`. `inline` for embedding images. |

### `settings` Object Fields

| Parameter        | Type    | Required | Description                                       |
| ---------------- | ------- | -------- | ------------------------------------------------- |
| `send_mode`      | Integer | No       | Sending mode (0: regular, 1: template, 2: address list). |
| `sandbox`        | Boolean | No       | Enable sandbox mode for testing. Emails will not be actually sent. |
| `open_tracking`  | Boolean | No       | Enable open tracking.                             |
| `click_tracking` | Boolean | No       | Enable click tracking.                            |
| `unsubscribe_tracking` | Boolean | No | Enable unsubscribe tracking.                      |

### Example Request Body

```json
{
    "from": "Sender Name<sender@example.com>",
    "to": ["recipient1@example.com", "Recipient2 Name<recipient2@example.com>"],
    "subject": "Your Subject Here",
    "content": {
        "html": "<p>Hello <strong>World</strong>!</p>",
        "text": "Hello World!",
        "preview_text": "This is a preview of the email."
    },
    "attachments": [
        {
            "content": "BASE64_ENCODED_CONTENT",
            "filename": "document.pdf",
            "type": "application/pdf",
            "disposition": "attachment"
        }
    ],
    "settings": {
        "sandbox": true
    }
}
```

### Example Response

```json
{
    "code": 0,
    "message": "success",
    "result": {
        "email_id": "some_unique_email_id"
    }
}
```

### Error Codes

| Code  | Message                                           | Description                                       |
| ----- | ------------------------------------------------- | ------------------------------------------------- |
| 30862 | The headers cannot include these headers: ...     | Indicates that certain headers are not allowed in the `headers` field of the `mail_body`. These are usually standard email headers that the API handles automatically. |
| ...   | ...                                               | ...                                               |
