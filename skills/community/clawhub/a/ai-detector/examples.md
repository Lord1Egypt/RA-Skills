# Examples

## cURL Example

```bash
curl -X POST "https://detect.gpthumanizer.ai/api/detect_ai" \
  -H "Content-Type: application/json" \
  -d '{"text":"Your text here\nThis is the next line."}'
```

## Example Response

```json
{
  "class": "human",
  "ai_possibilities": 0.0633,
  "probabilities": {
    "human": 0.8366,
    "ai": 0.0368,
    "ai_humanized": 0.0265,
    "light_edited": 0.1001
  },
  "text": "This is a quick test sentence to classify."
}
```
