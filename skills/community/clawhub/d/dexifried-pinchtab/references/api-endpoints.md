# API Endpoints

## Base URL
`http://localhost:9867`

## Authorization
All requests require the header:
```
Authorization: Bearer b6a91002205211861a1840bc7d1f55e98757ba635436b5a7
```

## Endpoints

### 1. Launch Browser
- **Endpoint:** `/launch`
- **Method:** `POST`

#### Request Body:
```json
{}
```

---

### 2. Navigate to URL
- **Endpoint:** `/navigate`
- **Method:** `POST`

#### Request Body:
```json
{
  "url": "https://example.com"
}
```

---

### 3. Get Snapshot
- **Endpoint:** `/snapshot`
- **Method:** `GET`

#### Query Parameters:
- `format`: (optional) Either `json` or `html`.

---

### 4. Click Element
- **Endpoint:** `/click`
- **Method:** `POST`

#### Request Body:
```json
{
  "selector": "<css_selector>"
}
```
---