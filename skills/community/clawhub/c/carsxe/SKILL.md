---
name: carsxe
description: >
  Access the full suite of CarsXE vehicle data APIs — VIN decoding, license plate lookup,
  market value, vehicle history, safety recalls, lien/theft checks, OBD-II diagnostic code
  decoding, vehicle images, international VIN decoding, Year/Make/Model lookups, and plate/VIN
  OCR from images. Use this skill any time the user asks about a vehicle by VIN, plate, make/model,
  or OBD code. Also triggers for: "what's this car worth", "check for recalls", "vehicle history
  report", "decode this plate", "what does check engine code X mean", or any automotive data query.
  Always use this skill when working with CarsXE APIs — do not guess API behavior without it.
---

# CarsXE Skill

CarsXE provides a REST API for comprehensive vehicle data at `https://api.carsxe.com`.

## API Key

The API key is injected as the `CARSXE_KEY` environment variable. Read it before
making any request:

- Use `process.env.CARSXE_KEY` in Node.js
- Use `$env:CARSXE_KEY` in PowerShell
- Use `$CARSXE_KEY` in bash/zsh

If `CARSXE_KEY` is empty or missing, tell the user to run:

```
openclaw config set skills.entries.carsxe.env.CARSXE_KEY "cxe_live_YOUR_KEY"
```

Then restart the gateway.

Always append `&source=openclaw` to every request.

---

## Quick API Map

| User intent              | Endpoint                            | Method | Key Parameters                                                                                             |
| ------------------------ | ----------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------- |
| Decode a VIN / get specs | `GET /specs`                        | GET    | `vin`, optional: `deepdata`, `disableIntVINDecoding`                                                       |
| Decode a license plate   | `GET /v2/platedecoder`              | GET    | `plate`, `country` (required), `state`, `district` (optional)                                              |
| Market value             | `GET /v2/marketvalue`               | GET    | `vin`, optional: `state`, `mileage`, `condition`                                                           |
| Vehicle history report   | `GET /history`                      | GET    | `vin`                                                                                                      |
| Vehicle images           | `GET /images`                       | GET    | `make`, `model`, optional: `year`, `trim`, `color`, `angle`, `photoType`, `size`, `license`, `transparent` |
| Safety recalls           | `GET /v1/recalls`                   | GET    | `vin`                                                                                                      |
| Lien & theft check       | `GET /v1/lien-theft`                | GET    | `vin`                                                                                                      |
| International VIN        | `GET /v1/international-vin-decoder` | GET    | `vin`                                                                                                      |
| Year/Make/Model lookup   | `GET /v1/ymm`                       | GET    | `year`, `make`, `model`, optional: `trim`                                                                  |
| OBD code diagnosis       | `GET /obdcodesdecoder`              | GET    | `code`                                                                                                     |
| VIN OCR from image       | `POST /v1/vinocr`                   | POST   | JSON body: `{"image": "<URL>"}`                                                                            |
| Plate OCR from image     | `POST /platerecognition`            | POST   | JSON body: `{"image": "<URL>"}`                                                                            |
| Validate API key         | `GET /v1/auth/validate`             | GET    | `key`                                                                                                      |

---

## Workflow

### 1. Build the request URL

Replace `$CARSXE_KEY` with the actual value of the `CARSXE_KEY` environment variable.

### 2. Choose the right endpoint

- VIN provided → `/specs` first, chain to other endpoints as needed
- Plate provided → `/v2/platedecoder` to resolve VIN, then chain if needed
- Make/Model/Year only → `/v1/ymm` or `/images`
- OBD code (P/C/B/U + digits) → `/obdcodesdecoder`
- Image URL for VIN → `POST /v1/vinocr` with `{"image": "<URL>"}`
- Image URL for plate → `POST /platerecognition` with `{"image": "<URL>"}`

### 3. Chain requests when helpful

Example: *"Is this plate stolen and does it have open recalls?"*

1. `GET /v2/platedecoder` → extract VIN
2. In parallel: `GET /v1/lien-theft` + `GET /v1/recalls`

### 4. Present results

Format output clearly. Highlight important findings (open recalls, theft records, salvage titles) prominently.

---

## Error Handling

| HTTP Status         | Meaning                | Action                                                                              |
| ------------------- | ---------------------- | ----------------------------------------------------------------------------------- |
| 401 / `invalid key` | Bad or missing API key | Tell user to set key via `openclaw config set skills.entries.carsxe.env.CARSXE_KEY` |
| 404 / `no results`  | VIN/plate not found    | Inform user, suggest double-checking                                                |
| 429                 | Rate limit exceeded    | Wait and retry                                                                      |
| 5xx                 | Server error           | Retry once, then report error                                                       |

Always check the `error` field in JSON responses — CarsXE sometimes returns HTTP 200 with an error body.

---

## Examples (replace $CARSXE_KEY with actual env var value)

**"What are the specs for VIN WBAFR7C57CC811956?"**
→ `GET https://api.carsxe.com/specs?key=$CARSXE_KEY&vin=WBAFR7C57CC811956&source=openclaw`

**"Decode California plate 7XER187"**
→ `GET https://api.carsxe.com/v2/platedecoder?key=$CARSXE_KEY&plate=7XER187&country=US&state=CA&source=openclaw`

**"What's my car worth? VIN WBAFR7C57CC811956, 45k miles, clean condition, California"**
→ `GET https://api.carsxe.com/v2/marketvalue?key=$CARSXE_KEY&vin=WBAFR7C57CC811956&state=CA&mileage=45000&condition=clean&source=openclaw`

**"Does this car have any recalls? 1C4JJXR64PW696340"**
→ `GET https://api.carsxe.com/v1/recalls?key=$CARSXE_KEY&vin=1C4JJXR64PW696340&source=openclaw`

**"Check liens and theft for WBAFR7C57CC811956"**
→ `GET https://api.carsxe.com/v1/lien-theft?key=$CARSXE_KEY&vin=WBAFR7C57CC811956&source=openclaw`

**"Decode this international VIN: WF0MXXGBWM8R43240"**
→ `GET https://api.carsxe.com/v1/international-vin-decoder?key=$CARSXE_KEY&vin=WF0MXXGBWM8R43240&source=openclaw`

**"Look up 2020 Toyota Camry LE"**
→ `GET https://api.carsxe.com/v1/ymm?key=$CARSXE_KEY&year=2020&make=Toyota&model=Camry&trim=LE&source=openclaw`

**"My check engine light shows P0300"**
→ `GET https://api.carsxe.com/obdcodesdecoder?key=$CARSXE_KEY&code=P0300&source=openclaw`

**"Extract the VIN from this photo: https://user-images.githubusercontent.com/5663423/30922082-64edb4fa-a3a8-11e7-873e-3fbcdce8ea3a.png"**
→ `POST https://api.carsxe.com/v1/vinocr?key=$CARSXE_KEY&source=openclaw`
→ Body: `{"image": "https://user-images.githubusercontent.com/5663423/30922082-64edb4fa-a3a8-11e7-873e-3fbcdce8ea3a.png"}`

**"Extract the plate from this photo: https://imagedelivery.net/moyiiSImjJPI_EZVxNMBBw/f49aed53-d736-4370-f3f4-97418841c800/public"**
→ `POST https://api.carsxe.com/platerecognition?key=$CARSXE_KEY&source=openclaw`
→ Body: `{"image": "https://imagedelivery.net/moyiiSImjJPI_EZVxNMBBw/f49aed53-d736-4370-f3f4-97418841c800/public"}`

**"Get vehicle images for BMW X5 2019"**
→ `GET https://api.carsxe.com/images?key=$CARSXE_KEY&make=BMW&model=X5&year=2019&source=openclaw`
