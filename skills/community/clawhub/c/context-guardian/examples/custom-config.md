# Custom Configuration Example

Create a `config/user.json` file to override default settings:

```json
{
  "enabled": true,
  "thresholds": {
    "warning": 50,
    "danger": 65,
    "critical": 80
  },
  "alertStyle": "detailed",
  "suggestions": {
    "autoSuggest": true,
    "suggestCompression": true,
    "suggestRestart": true
  }
}
```

## Configuration Options

### thresholds

Customize when alerts are triggered:

- `warning`: First alert level (default: 60)
- `danger`: Second alert level (default: 70)
- `critical`: Final alert level (default: 85)

### alertStyle

Choose how alerts are formatted:

- `emoji`: Emoji + concise text (default)
- `text`: Plain text only
- `detailed`: Full explanation with examples

### suggestions

Control what suggestions are included in alerts:

- `autoSuggest`: Include general suggestions (default: true)
- `suggestCompression`: Suggest using context-optimizer (default: true)
- `suggestRestart`: Suggest starting new session (default: true)

## Example Configurations

### Conservative (Alert Early)

```json
{
  "thresholds": {
    "warning": 40,
    "danger": 55,
    "critical": 70
  }
}
```

### Aggressive (Alert Late)

```json
{
  "thresholds": {
    "warning": 70,
    "danger": 80,
    "critical": 90
  }
}
```

### Minimal Alerts

```json
{
  "thresholds": {
    "warning": 999,
    "danger": 999,
    "critical": 85
  }
}
```

This configuration only alerts at critical level (85%).
