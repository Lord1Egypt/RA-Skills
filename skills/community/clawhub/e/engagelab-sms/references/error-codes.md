# EngageLab SMS API Error Codes

## SMS Sending Errors

| Error Code | HTTP Code | Description |
|------------|-----------|-------------|
| 1000 | 500 | Internal Error |
| 2001 | 401 | Authentication failed — incorrect token |
| 2002 | 401 | Authentication failed — token expired or disabled |
| 2004 | 403 | No permission to call this API |
| 3001 | 400 | Invalid request parameter format (not valid JSON) |
| 3002 | 400 | Invalid request parameters (do not meet requirements) |
| 3003 | 400 | Business validation failed — see `message` field for details |
| 3004 | 400 | Frequency limit exceeded — cannot resend same template to same user within verification code validity period |
| 4001 | 400 | Resource not found (e.g., non-existent template ID) |
| 5001 | 400 | Verification code sending failed — see `message` field for details |

## Template & Signature Errors

| Error Code | HTTP Code | Description |
|------------|-----------|-------------|
| 0 | 200 | Success |
| 400 | 400 | Parameter error or business logic error |
| 500 | 500 | Internal server error |

### Common Error Messages

| Message | Meaning |
|---------|---------|
| `invalid templateId` | Template ID format is invalid |
| `template config not exist` | Template does not exist |
| `invalid signId` | Signature ID format is invalid |
| `sign config not exist` | Signature does not exist |
| `sign_name already exist` | Signature name is already taken |
| `can not update pending status template` | Templates in Pending Review cannot be updated |
| `can not update pending status sign` | Signatures in Pending Review cannot be updated |
| `there are pending or running plans using current template, can not update` | Template is in use by active plans |
| `there are pending or running plans using current sign, can not update` | Signature is in use by active plans |
| `sign status is not approved, can not use` | Only Approved signatures can be attached to templates |
