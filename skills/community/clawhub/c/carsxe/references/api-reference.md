# CarsXE API reference (OpenClaw)

**Base URL:** `https://api.carsxe.com`

Append `key=$CARSXE_KEY` and `source=openclaw` on **every** request.

Do **not** call `usPlateDecoder` or `/v1/ownership/phone`.

| Intent | Endpoint | Method | Parameters |
| --- | --- | --- | --- |
| VIN specs | `/specs` | GET | `vin`; optional `deepdata`, `disableIntVINDecoding` |
| Plate decoder | `/v2/platedecoder` | GET | `plate`, `country` (required); optional `state`, `district` |
| Market value | `/v2/marketvalue` | GET | `vin`; optional `state`, `mileage`, `condition` |
| History | `/history` | GET | `vin` |
| Images | `/images` | GET | `make`, `model`; optional `year`, `trim`, `color`, `angle`, `photoType`, `size`, `license`, `transparent` |
| Recalls (VIN) | `/v1/recalls` | GET | `vin` |
| Recalls (YMM) | `/v1/recalls-ymm` | GET | `year`, `make`, `model` |
| Recalls batch submit | `/v1/recalls-batch/submit` | POST | JSON `vins` and/or `csv` / `csvUrl`; optional `webhookUrl` |
| Recalls batch status | `/v1/recalls-batch/status` | GET | `batchId` |
| Recalls batch results | `/v1/recalls-batch/results` | GET | `batchId` |
| Recalls batch download | `/v1/recalls-batch/download` | GET | `batchId` (returns `text/csv`) |
| Lien & theft | `/v1/lien-theft` | GET | `vin` |
| International VIN | `/v1/international-vin-decoder` | GET | `vin` |
| YMM specs | `/v1/ymm` | GET | `year`, `make`, `model`; optional `trim` |
| YMM options | `/v1/ymm-options` | GET | optional `dimension`, `year`, `make`, `model`, `trim` |
| Ownership by VIN | `/v1/ownership/vin` | GET | `vin`; optional `include` |
| Ownership by person | `/v1/ownership/person` | GET | `first_name`, `last_name`, `address`, `zip`; optional `include` |
| Ownership by address | `/v1/ownership/address` | GET | `address`, `zip`; optional `include`, `variant` |
| Ownership by ZIP | `/v1/ownership/zip` | GET | `zip`; optional `gender`, `min_age`, `max_age`, `income`, `page`, `limit`, `include`, `variant` |
| OBD decoder | `/obdcodesdecoder` | GET | `code` |
| VIN OCR | `/v1/vinocr` | POST | JSON `{"image": "<URL>"}` |
| Plate OCR | `/platerecognition` | POST | JSON `{"image": "<URL>"}` |
| Auth validate | `/v1/auth/validate` | GET | `key` |

## Routing

- Recalls: VIN → `/v1/recalls`; year/make/model → `/v1/recalls-ymm`; many VINs → `/v1/recalls-batch/*`
- YMM: dropdowns / "what years was X sold" → `/v1/ymm-options`; full specs → `/v1/ymm`
- Ownership is Enterprise-only and billed per returned record. Street `address` is street only (no city/state).

## Details

- [Recalls by YMM](recalls-ymm.md)
- [Recalls Batch](recalls-batch.md)
- [YMM Options](ymm-options.md)
- [Ownership](ownership.md)
