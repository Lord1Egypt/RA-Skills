# Discogs API Reference

This skill interacts with the Discogs API to search for vinyl releases and retrieve marketplace price suggestions.

## Authentication

All requests must be authenticated using a Discogs Personal Access Token.

- **Header**: `Authorization: Discogs token={YOUR_TOKEN}`
- **User-Agent**: A unique User-Agent string is required (e.g., `OpenclawSkill/1.0`).

To generate a token:
1. Go to [Discogs Developer Settings](https://www.discogs.com/settings/developers).
2. Click "Generate new token".

## Endpoints

### 1. Search for Releases

Search the Discogs database for a release.

- **URL**: `https://api.discogs.com/database/search`
- **Method**: `GET`
- **Parameters**:
  - `q`: The search query (e.g., "Artist - Album").
  - `type`: `release` (to filter for releases).
  - `format`: `Vinyl` (to filter for vinyl records).

#### Example Request

```bash
curl "https://api.discogs.com/database/search?q=Daft+Punk&type=release&format=Vinyl" \
  -H "User-Agent: OpenclawSkill/1.0" \
  -H "Authorization: Discogs token=YOUR_TOKEN"
```

#### Example Response (Excerpt)

```json
{
  "results": [
    {
      "id": 4570366,
      "title": "Daft Punk - Random Access Memories",
      "year": "2013",
      "format": ["Vinyl", "LP", "Album"],
      "resource_url": "https://api.discogs.com/releases/4570366"
    }
  ]
}
```

### 2. Price Suggestions

Retrieve price suggestions for a specific release based on its condition.

- **URL**: `https://api.discogs.com/marketplace/price_suggestions/{release_id}`
- **Method**: `GET`

#### Example Request

```bash
curl "https://api.discogs.com/marketplace/price_suggestions/4570366" \
  -H "User-Agent: OpenclawSkill/1.0" \
  -H "Authorization: Discogs token=YOUR_TOKEN"
```

#### Example Response

```json
{
  "Good (G)": {
    "currency": "USD",
    "value": 25.00
  },
  "Very Good Plus (VG+)": {
    "currency": "USD",
    "value": 35.00
  },
  "Mint (M)": {
    "currency": "USD",
    "value": 60.00
  }
}
```

### 3. Release Statistics

Retrieve marketplace statistics for a release.

- **URL**: `https://api.discogs.com/releases/{release_id}/stats`
- **Method**: `GET`

#### Example Request

```bash
curl "https://api.discogs.com/releases/4570366/stats" \
  -H "User-Agent: OpenclawSkill/1.0" \
  -H "Authorization: Discogs token=YOUR_TOKEN"
```

#### Example Response

```json
{
  "num_for_sale": 15,
  "lowest_price": {
    "value": 22.50,
    "currency": "USD"
  },
  "blocked_from_sale": false
}
```

## Rate Limiting

The Discogs API limits requests to **60 per minute** per IP address. The skill should respect this limit to avoid `429 Too Many Requests` errors.

## References

- [Discogs API Documentation](https://www.discogs.com/developers)
- [Authentication Guide](https://www.discogs.com/developers#page:authentication)
- [Search Endpoint](https://www.discogs.com/developers#page:database,header:database-search)
- [Price Suggestions Endpoint](https://www.discogs.com/developers#page:marketplace,header:marketplace-price-suggestions)

