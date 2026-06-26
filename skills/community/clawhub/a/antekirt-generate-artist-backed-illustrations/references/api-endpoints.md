# Antekirt API Endpoints (Working Notes)

Base URL: `https://antekirt.com`

## Auth
- Header: `x-api-key: <API_KEY>`

## Artists
- `GET /api/v1/artists`
- Useful query params: `page`, `limit`, `search`, `order`, `direction`

## Generations
- `POST /api/v1/generations/image`
  - Body: `{ artistId, prompt }`
  - Async: returns accepted/processing with generation id
- `GET /api/v1/generations/:id`
  - Poll until `status=completed`

## Status values
- `processing`
- `processing_svg`
- `processing_video`
- `completed`
- `failed`

## Credit costs
- image: 3
- svg: 5
- video: 25
