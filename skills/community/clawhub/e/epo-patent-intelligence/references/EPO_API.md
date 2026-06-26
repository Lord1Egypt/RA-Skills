# EPO OPS API Reference Documentation

## Overview

The European Patent Office (EPO) Open Patent Services (OPS) API provides access to patent data from the EPO and other national patent offices.

## Authentication

### OAuth2 Client Credentials Flow

**Endpoint:** `POST https://ops.epo.org/3.2/auth/accesstoken`

**Headers:**
```
Authorization: Basic <base64(consumer_key:secret_key)>
Content-Type: application/x-www-form-urlencoded
```

**Body:**
```
grant_type=client_credentials
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

## Search API

### Endpoint
`GET https://ops.epo.org/3.2/rest-services/published-data/search/biblio`

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `q` | Search query | `pa=IBM` (applicant), `ti=CNC` (title), `ab=robot` (abstract) |
| `Range` | Result range | `1-10` (first 10 results) |

### Query Syntax

**Applicant Search:**
- `pa=IBM` - Search by company name
- `pa=Trumpf` - Search for Trumpf patents

**Title Search:**
- `ti=CNC` - CNC in title
- `ti=additive manufacturing` - Additive manufacturing in title
- `ti=machine tool` - Machine tool in title

**Abstract Search:**
- `ab=automation` - Automation in abstract
- `ab=robot` - Robot in abstract

**Combined Queries:**
- `pa=IBM AND ti=CNC` - IBM patents with CNC in title
- `pa=Trumpf OR pa=Mazak` - Patents by either company

### Response Format

```json
{
  "ops:world-patent-data": {
    "ops:biblio-search": {
      "ops:search-result": {
        "exchange-documents": {
          "exchange-document": [
            {
              "bibliographic-data": {
                "publication-reference": {
                  "document-id": [
                    {
                      "doc-number": "US1234567B1",
                      "date": "20240315"
                    }
                  ]
                },
                "invention-title": [
                  {
                    "$": "Machine Tool System",
                    "@lang": "en"
                  }
                ],
                "parties": {
                  "applicants": {
                    "applicant": [
                      {
                        "addressbook": {
                          "name": "YAMAZAKI MAZAK CORP [JP]"
                        }
                      }
                    ]
                  }
                }
              },
              "abstract": [
                {
                  "$": "Abstract text here...",
                  "@lang": "en"
                }
              ]
            }
          ]
        }
      }
    }
  }
}
```

## Rate Limits

- **Anonymous:** 10 requests per minute
- **Registered:** 500 requests per hour (with OAuth)
- **Query limits:** Max 100 results per query

## Error Handling

### Common Errors

**401 Unauthorized:**
- Invalid or expired access token
- Missing authentication

**400 Bad Request:**
- Invalid query syntax
- Missing required parameters

**404 Not Found:**
- Patent not found
- Invalid document ID

**429 Rate Limited:**
- Too many requests
- Wait before retrying

## Best Practices

1. **Authenticate once, reuse token** - Tokens valid for 1 hour
2. **Batch queries** - Fetch multiple competitors in sequence
3. **Handle rate limits** - Add delays between batches
4. **Validate responses** - Check for empty or malformed data
5. **Log failures** - Track which queries fail for debugging

## Tips for Competitor Monitoring

**Effective Queries:**
- `pa=Trumpf` - Get all Trumpf patents (good)
- `pa=Trumpf AND ti=laser` - Trumpf laser patents (focused)
- `ti=CNC AND ab=automation` - CNC automation patents (broad)

**Query Optimization:**
- Start broad (`pa=IBM`) then narrow down
- Use title (`ti=`) for specific technology searches
- Use abstract (`ab=`) for concept searches
- Combine with AND/OR for complex queries

## API Documentation

Full documentation: https://developers.epo.org/

OPS API Reference: https://www.epo.org/searching-for-patents/technical/epo-ops.html

## Example Usage

### Python
```python
import requests
import base64

# Authenticate
auth_string = base64.b64encode(f"{consumer_key}:{secret_key}".encode()).decode()
response = requests.post(
    "https://ops.epo.org/3.2/auth/accesstoken",
    headers={'Authorization': f'Basic {auth_string}'},
    data={'grant_type': 'client_credentials'}
)
token = response.json()['access_token']

# Search patents
response = requests.get(
    "https://ops.epo.org/3.2/rest-services/published-data/search/biblio",
    headers={'Authorization': f'Bearer {token}'},
    params={'q': 'pa=IBM', 'Range': '1-5'}
)
patents = response.json()
```

### cURL
```bash
# Authenticate
curl -X POST https://ops.epo.org/3.2/auth/accesstoken \
  -H "Authorization: Basic $(echo -n 'consumer_key:secret_key' | base64)" \
  -d "grant_type=client_credentials"

# Search patents
curl "https://ops.epo.org/3.2/rest-services/published-data/search/biblio?q=pa=IBM&Range=1-5" \
  -H "Authorization: Bearer <access_token>"
```