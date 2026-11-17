# CarsXE Skill for OpenClaw

Access the full suite of [CarsXE](https://api.carsxe.com) vehicle data APIs from [OpenClaw](https://openclaw.ai) — decode VINs, look up license plates, get market values, check history, recalls (VIN, YMM, or batch), YMM options, ownership, liens, OBD codes, and more.

Published on ClawHub as [@carsxe/carsxe](https://clawhub.ai/carsxe/carsxe).

## Features

| Intent | Endpoint |
| --- | --- |
| Decode a VIN / specs | `GET /specs` |
| License plate lookup | `GET /v2/platedecoder` |
| Market value | `GET /v2/marketvalue` |
| Vehicle history | `GET /history` |
| Vehicle images | `GET /images` |
| Safety recalls (VIN) | `GET /v1/recalls` |
| Safety recalls (year/make/model) | `GET /v1/recalls-ymm` |
| Safety recalls (batch) | `POST/GET /v1/recalls-batch/*` |
| Lien & theft | `GET /v1/lien-theft` |
| International VIN | `GET /v1/international-vin-decoder` |
| Year/Make/Model specs | `GET /v1/ymm` |
| YMM options (dropdowns) | `GET /v1/ymm-options` |
| Ownership (Enterprise) | `GET /v1/ownership/vin\|person\|address\|zip` |
| OBD-II decoder | `GET /obdcodesdecoder` |
| VIN OCR | `POST /v1/vinocr` |
| Plate OCR | `POST /platerecognition` |

The skill is auto-invoked from natural language. Agents call `https://api.carsxe.com` with `key=$CARSXE_KEY` and `source=openclaw` on every request.

## Installation

```bash
openclaw skills install carsxe
```

Or from ClawHub:

```bash
openclaw skills install @carsxe/carsxe
```

## Setup

Get an API key from the [CarsXE developer dashboard](https://api.carsxe.com/dashboard/developer), then:

```bash
openclaw config set skills.entries.carsxe.env.CARSXE_KEY "cxe_live_YOUR_KEY"
```

Restart the OpenClaw gateway after setting the key.

## Usage examples

Just describe what you need — OpenClaw selects the endpoint and chains calls when required.

- *"What are the specs for VIN WBAFR7C57CC811956?"* → `/specs`
- *"Decode California plate 7XER187"* → `/v2/platedecoder`
- *"What's this car worth?"* → `/v2/marketvalue`
- *"Does this VIN have any recalls?"* → `/v1/recalls`
- *"Any recalls on a 2023 Toyota Camry?"* → `/v1/recalls-ymm`
- *"Check recalls for this list of VINs"* → `/v1/recalls-batch/*`
- *"What Toyota models were sold in 2023?"* → `/v1/ymm-options`
- *"Who is the registered owner of this VIN?"* → `/v1/ownership/vin`
- *"Check liens and theft for this VIN"* → `/v1/lien-theft`
- *"My check engine light shows P0300"* → `/obdcodesdecoder`

## Skill layout

```
SKILL.md                      # Agent instructions + API map
references/api-reference.md   # Full endpoint table
references/recalls-ymm.md
references/recalls-batch.md
references/ymm-options.md
references/ownership.md
```

## Docs

- Skill listing: [clawhub.ai/carsxe/carsxe](https://clawhub.ai/carsxe/carsxe)
- API docs: [api.carsxe.com/docs](https://api.carsxe.com/docs)
- OpenClaw install guide: [api.carsxe.com/docs/integrations/openclaw-quickstart](https://api.carsxe.com/docs/integrations/openclaw-quickstart)

## License

MIT © CarsXE
