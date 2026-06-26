# Apollo People Enrichment API

## Endpoint
POST https://api.apollo.io/api/v1/people/match

## Headers
Content-Type: application/json
Cache-Control: no-cache

## Parameters (JSON body)
{
  \"api_key\": \"[KEY]\",
  \"first_name\": \"[string]\",
  \"last_name\": \"[string]\",
  \"name\": \"[full name if no split]\",
  \"email\": \"[optional]\",
  \"organization_name\": \"[company]\",
  \"title\": \"[job title]\",
  \"reveal_personal_emails\": true,  // Set to true for personal emails
  \"reveal_phone_number\": true      // Set to true for phone
}

## Response Example
{
  \"person\": {
    \"id\": \"[apollo id]\",
    \"first_name\": \"John\",
    \"last_name\": \"Doe\",
    \"name\": \"John Doe\",
    \"title\": \"CEO\",
    \"organization\": { \"name\": \"Acme Corp\" },
    \"email\": \"john@acme.com\",
    \"phone\": \"+1-123-456-7890\"
  }
}

## Notes
- More params = better match
- Credits consumed per call
- Auto-syncs to HubSpot if integrated
- For bulk, use /bulk/people/match (up to 10)

Full docs: https://docs.apollo.io/reference/people-enrichment