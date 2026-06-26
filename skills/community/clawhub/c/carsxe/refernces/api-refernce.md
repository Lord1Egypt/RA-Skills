# CarsXE API Reference

Base URL: `https://api.carsxe.com`
Auth: append `?key=YOUR_API_KEY` to every request.
Always append `&source=openclaw` to every request.
Docs: https://api.carsxe.com/docs

---

## 1. Vehicle Specs (VIN Decode)

**Endpoint:** `GET /specs`

**Parameters:**

| Param                   | Required | Description                                  |
| ----------------------- | -------- | -------------------------------------------- |
| `key`                   | Yes      | Your CarsXE API key                          |
| `vin`                   | Yes      | 17-character VIN                             |
| `deepdata`              | No       | `true` to get extended data                  |
| `disableIntVINDecoding` | No       | `true` to disable international VIN fallback |

**Response fields (key ones):**

- `input.vin` — validated VIN
- `attributes.year`, `attributes.make`, `attributes.model`, `attributes.trim`
- `attributes.engine` — displacement, cylinders, fuel type, horsepower, torque
- `attributes.transmission` — type, speeds
- `attributes.drivetrain` — AWD/FWD/RWD/4WD
- `attributes.doors`, `attributes.body_type`
- `attributes.dimensions` — wheelbase, length, width, height, weight
- `attributes.fuel` — tank capacity, city/hwy MPG
- `attributes.colors` — interior/exterior options
- `attributes.equipment` — standard and optional features list

**Example:**

```
GET /specs?key=KEY&vin=WBAFR7C57CC811956&source=openclaw
```

---

## 2. License Plate Decoder

**Endpoint:** `GET /v2/platedecoder`

**Parameters:**

| Param      | Required | Description                                                                      |
| ---------- | -------- | -------------------------------------------------------------------------------- |
| `key`      | Yes      | Your CarsXE API key                                                              |
| `plate`    | Yes      | License plate number                                                             |
| `country`  | Yes      | Country code (e.g., `US`, `CA`, `GB`)                                            |
| `state`    | No       | State/province abbreviation (e.g., `CA`, `NY`) — improves accuracy for US plates |
| `district` | No       | District or region within the country                                            |

**Response fields:**

- `vin` — resolved VIN
- `make`, `model`, `year`
- `state`, `country`
- Basic vehicle attributes

**Tip:** After decoding a plate, chain to `/specs`, `/history`, or `/v1/recalls` using the returned VIN.

**Example:**

```
GET /v2/platedecoder?key=KEY&plate=7XER187&country=US&state=CA&source=openclaw
```

---

## 3. Market Value

**Endpoint:** `GET /v2/marketvalue`

**Parameters:**

| Param       | Required | Description                                                       |
| ----------- | -------- | ----------------------------------------------------------------- |
| `key`       | Yes      | Your CarsXE API key                                               |
| `vin`       | Yes      | 17-character VIN                                                  |
| `state`     | No       | US state abbreviation (affects regional pricing, e.g. `CA`, `TX`) |
| `mileage`   | No       | Current mileage of the vehicle                                    |
| `condition` | No       | `excellent`, `clean`, `average`, or `rough`                       |

**Response fields:**

- `retail` — estimated retail price
- `trade_in` — trade-in value
- `msrp` — original MSRP
- `mileage_adjustment` — adjustment based on recorded mileage
- `condition` — assumed condition
- `currency` — USD by default

**Example:**

```
GET /v2/marketvalue?key=KEY&vin=WBAFR7C57CC811956&source=openclaw
GET /v2/marketvalue?key=KEY&vin=WBAFR7C57CC811956&state=CA&mileage=45000&condition=clean&source=openclaw
```

---

## 4. Vehicle History

**Endpoint:** `GET /history`

**Parameters:**

| Param | Required | Description         |
| ----- | -------- | ------------------- |
| `key` | Yes      | Your CarsXE API key |
| `vin` | Yes      | 17-character VIN    |

**Response fields:**

- `junk` — junk/salvage title records
- `insurance` — insurance loss records
- `brands` — title brands (rebuilt, flood, fire, etc.)
- `titles` — title history by state
- `odometer` — odometer readings over time
- `theft` — theft/recovery records
- `accidents` — accident/damage records (where available)
- `exports` — export records

**Example:**

```
GET /history?key=KEY&vin=WBAFR7C57CC811956&source=openclaw
```

---

## 5. Vehicle Images

**Endpoint:** `GET /images`

**Parameters:**

| Param         | Required | Description                                                               |
| ------------- | -------- | ------------------------------------------------------------------------- |
| `key`         | Yes      | Your CarsXE API key                                                       |
| `make`        | Yes      | Vehicle make (e.g., `BMW`)                                                |
| `model`       | Yes      | Vehicle model (e.g., `X5`)                                                |
| `year`        | No       | Year (e.g., `2019`)                                                       |
| `trim`        | No       | Trim level                                                                |
| `color`       | No       | Color name (e.g., `blue`, `white`)                                        |
| `transparent` | No       | `true` for transparent background                                         |
| `angle`       | No       | `front`, `rear`, `side`, `interior`                                       |
| `photoType`   | No       | `interior`, `exterior`, or `engine`                                       |
| `size`        | No       | `Small`, `Medium`, `Large`, `Wallpaper`, or `All`                         |
| `license`     | No       | `Public`, `Share`, `ShareCommercially`, `Modify`, or `ModifyCommercially` |

**Response fields:**

- Array of image objects with `url`, `width`, `height`, `color`, `angle`, `year`

**Example:**

```
GET /images?key=KEY&make=BMW&model=X5&year=2019&source=openclaw
```

---

## 6. Safety Recalls

**Endpoint:** `GET /v1/recalls`

**Parameters:**

| Param | Required | Description         |
| ----- | -------- | ------------------- |
| `key` | Yes      | Your CarsXE API key |
| `vin` | Yes      | 17-character VIN    |

**Response fields:**

- `total` — number of recalls found
- `recalls[]` — array of recall objects:
  - `date` — recall date
  - `description` — what's being recalled
  - `risk` — safety risk description
  - `remedy` — fix/remedy description
  - `status` — open/closed
  - `nhtsa_id` — NHTSA campaign number

**Important:** Always highlight open recalls prominently for the user.

**Example:**

```
GET /v1/recalls?key=KEY&vin=1C4JJXR64PW696340&source=openclaw
```

---

## 7. Lien & Theft

**Endpoint:** `GET /v1/lien-theft`

**Parameters:**

| Param | Required | Description         |
| ----- | -------- | ------------------- |
| `key` | Yes      | Your CarsXE API key |
| `vin` | Yes      | 17-character VIN    |

**Response fields:**

- `lien` — lien records (active loans/encumbrances)
- `theft` — theft/stolen vehicle records
- `recovery` — recovery records if stolen

**Important:** Flag any active liens or unresolved theft records prominently — critical for buyers.

**Example:**

```
GET /v1/lien-theft?key=KEY&vin=WBAFR7C57CC811956&source=openclaw
```

---

## 8. International VIN Decoder

**Endpoint:** `GET /v1/international-vin-decoder`

**Parameters:**

| Param | Required | Description                        |
| ----- | -------- | ---------------------------------- |
| `key` | Yes      | Your CarsXE API key                |
| `vin` | Yes      | 17-character VIN (non-US vehicles) |

**Response fields:** Similar to `/specs` but includes international-specific fields:

- `manufacturer_country`
- `emissions_standard` — Euro NCAP ratings where applicable
- `regional_specs`

Use for VINs that don't start with 1, 2, 3, 4, or 5 (those are North American).

**Example:**

```
GET /v1/international-vin-decoder?key=KEY&vin=WF0MXXGBWM8R43240&source=openclaw
```

---

## 9. Year/Make/Model (YMM)

**Endpoint:** `GET /v1/ymm`

**Parameters:**

| Param   | Required | Description                    |
| ------- | -------- | ------------------------------ |
| `key`   | Yes      | Your CarsXE API key            |
| `year`  | Yes      | Model year (e.g., `2020`)      |
| `make`  | Yes      | Make (e.g., `Toyota`)          |
| `model` | Yes      | Model (e.g., `Camry`)          |
| `trim`  | No       | Trim level (e.g., `LE`, `XSE`) |

**Response fields:**

- Vehicle specs similar to `/specs`
- `colors` — available colors for that year/trim
- `features` — standard features list
- `options` — available option packages
- `configurations` — all available trims if no trim specified

Use when the user doesn't have a VIN but knows the year, make, and model.

**Example:**

```
GET /v1/ymm?key=KEY&year=2020&make=Toyota&model=Camry&trim=LE&source=openclaw
```

---

## 10. OBD Code Decoder

**Endpoint:** `GET /obdcodesdecoder`

**Parameters:**

| Param  | Required | Description                                            |
| ------ | -------- | ------------------------------------------------------ |
| `key`  | Yes      | Your CarsXE API key                                    |
| `code` | Yes      | OBD-II code (e.g., `P0300`, `C0035`, `B1234`, `U0100`) |

**Code prefixes:**

- `P` — Powertrain (engine, transmission)
- `C` — Chassis (brakes, suspension)
- `B` — Body (airbags, comfort systems)
- `U` — Network/Communication

**Response fields:**

- `code` — the code
- `description` — plain-language description of the fault
- `diagnosis` — likely causes
- `date` — when the code was last updated in the database

**Example:**

```
GET /obdcodesdecoder?key=KEY&code=P0300&source=openclaw
```

---

## 11. VIN OCR

**Endpoint:** `POST /v1/vinocr`

**Method:** POST
**Content-Type:** `application/json`
**Query params:** `?key=YOUR_API_KEY&source=openclaw`

**Request body:**

```json
{
  "image": "https://example.com/vin-sticker.jpg"
}
```

**Response fields:**

- `vin` — detected VIN string
- `confidence` — confidence score (0–1)
- `bounding_box` — pixel coordinates of VIN in image
- `candidates` — alternative VIN readings if confidence is low

**Example:**

```
POST /v1/vinocr?key=KEY&source=openclaw
Body: {"image":"https://example.com/vin-sticker.jpg"}
```

---

## 12. Plate Image Recognition

**Endpoint:** `POST /platerecognition`

**Method:** POST
**Content-Type:** `application/json`
**Query params:** `?key=YOUR_API_KEY&source=openclaw`

**Request body:**

```json
{
  "image": "https://example.com/car-photo.jpg"
}
```

**Response fields:**

- `plates[]` — array of detected plates:
  - `plate` — plate text
  - `confidence` — confidence score
  - `bounding_box` — pixel coordinates in image
  - `vehicle_type` — car, truck, motorcycle, etc.
  - `country` / `state` — inferred location (where detectable)

**Example:**

```
POST /platerecognition?key=KEY&source=openclaw
Body: {"image":"https://example.com/car-photo.jpg"}
```

---

## 13. Auth Validate

**Endpoint:** `GET /v1/auth/validate`

**Parameters:**

| Param | Required | Description                    |
| ----- | -------- | ------------------------------ |
| `key` | Yes      | The CarsXE API key to validate |

**Response fields:**

- `valid` — `true` if the key is active
- Error message if invalid

**Example:**

```
GET /v1/auth/validate?key=YOUR_API_KEY&source=openclaw
```
