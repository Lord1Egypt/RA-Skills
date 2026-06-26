# Schema Format Reference

## Schema JSON Structure

```json
{
  "variables": {
    "VARIABLE_NAME": {
      "type": "string",
      "required": true,
      "description": "What this variable does",
      "pattern": "^regex$",
      "default": "default_value",
      "example": "example_value",
      "sensitive": false,
      "min": 0,
      "max": 65535
    }
  }
}
```

## Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | no | Expected type (see below) |
| `required` | boolean | no | Whether variable must exist |
| `description` | string | no | Human-readable description |
| `pattern` | string | no | Regex pattern for validation |
| `default` | string | no | Default value (informational) |
| `example` | string | no | Example value (informational) |
| `sensitive` | boolean | no | If true, mask in diff output |
| `min` | number | no | Minimum for numeric values |
| `max` | number | no | Maximum for numeric values |

## Supported Types

| Type | Validates | Examples |
|------|-----------|---------|
| `string` | Any value | `production`, `hello world` |
| `integer` | Digits only | `3000`, `10` |
| `float` | Decimal number | `0.5`, `3.14` |
| `boolean` | true/false/yes/no/1/0/on/off | `true`, `false` |
| `url` | Protocol prefix required | `https://api.example.com` |
| `email` | user@domain.tld format | `admin@example.com` |
| `ip` | IPv4 dotted notation | `192.168.1.1` |
| `port` | 1-65535 | `3000`, `8080` |
| `path` | Starts with / or ~ | `/var/log/app.log` |
| `connection_string` | postgres/mysql/redis/etc:// | `postgres://user:pass@host/db` |

## Auto-Generated Schema

Use `--generate-schema .env` to create a schema from an existing file. It infers:
- Variable types from key names and value patterns
- Required flag (all set to true)
- Sensitive flag for SECRET/PASSWORD/KEY/TOKEN variables
- Example values from current values
