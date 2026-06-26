# API Reference

This skill uses the GPTHumanizer detection API to evaluate whether a text is likely human-written, AI-generated, AI-humanized, or lightly edited.

## Endpoint

- Base URL: `https://detect.gpthumanizer.ai`
- Endpoint: `/api/detect_ai`
- Method: `POST`
- Full URL: `https://detect.gpthumanizer.ai/api/detect_ai`

## Authentication

- No authentication required

## Defaults

- `base_url`: `https://detect.gpthumanizer.ai`
- `endpoint`: `/api/detect_ai`
- `timeout`: `30s`

## Rate Limits

- `100/min` per IP
- `10k/day` per IP

## Request Fields

### Required

- `text`: text to evaluate

### Optional

- `base_url`: override the API base URL
- `endpoint`: override the endpoint path
- `timeout`: request timeout in seconds

## Response Fields

- `class`: final label  
  Possible values:
  - `human`
  - `ai`
  - `ai_humanized`
  - `light_edited`

- `ai_possibilities`: aggregated AI likelihood from `0` to `1`

- `probabilities`: probability distribution across classes
  - `human`
  - `ai`
  - `ai_humanized`
  - `light_edited`

- `text`: original input text

## Label Meanings

- `human`: likely human-authored
- `ai`: likely directly AI-generated
- `ai_humanized`: likely AI-generated and then paraphrased or humanized
- `light_edited`: likely partially modified or mixed-origin text

## Notes

- Detection output should be treated as a probabilistic signal, not proof.
- Very short text, heavily edited text, or mixed-source text may reduce reliability.
- If the API fails or times out, report that detection could not be completed.
