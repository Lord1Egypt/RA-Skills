# EchoMemory Mode Switching

Use this reference when the user wants to move between localhost-only usage and EchoMemory cloud sync.

## Cloud mode

Cloud mode requires:

- `localOnlyMode: false`
- a valid `apiKey`
- a gateway restart after the change

Recommended plugin config:

```json5
{
  "plugins": {
    "entries": {
      "echo-memory-cloud-openclaw-plugin": {
        "enabled": true,
        "config": {
          "apiKey": "ec_your_key_here",
          "localOnlyMode": false,
          "memoryDir": "C:\\Users\\your-user\\.openclaw\\workspace\\memory",
          "autoSync": true,
          "localUiAutoOpenOnGatewayStart": true,
          "localUiAutoInstall": true,
          "syncIntervalMinutes": 15,
          "batchSize": 10
        }
      }
    }
  }
}
```

Expected behavior after `openclaw gateway restart`:

- the local UI still starts on localhost
- the viewer should not say local-only mode
- `/echo-memory whoami` should succeed
- `/echo-memory sync` should be able to upload markdown memories
- the setup sidebar should still show version and update information for packaged installs

## Local mode

Local mode requires:

- `localOnlyMode: true`
- no API key requirement

Recommended plugin config:

```json5
{
  "plugins": {
    "entries": {
      "echo-memory-cloud-openclaw-plugin": {
        "enabled": true,
        "config": {
          "localOnlyMode": true,
          "memoryDir": "C:\\Users\\your-user\\.openclaw\\workspace\\memory",
          "localUiAutoOpenOnGatewayStart": true,
          "localUiAutoInstall": true
        }
      }
    }
  }
}
```

Expected behavior after `openclaw gateway restart`:

- the local UI still starts
- localhost browsing works
- cloud sync and cloud identity checks are unavailable by design
- the local UI can still show the version badge and update panel, but linked or local-checkout installs should not be treated as packaged-update targets

## Config precedence

The plugin resolves config in this order:

1. `plugins.entries.echo-memory-cloud-openclaw-plugin.config.*`
2. `~/.openclaw/.env`
3. process environment
4. plugin defaults

Relevant environment variables:

- `ECHOMEM_API_KEY`
- `ECHOMEM_MEMORY_DIR`
- `ECHOMEM_LOCAL_ONLY_MODE`
- `ECHOMEM_LOCAL_UI_AUTO_OPEN_ON_GATEWAY_START`
- `ECHOMEM_LOCAL_UI_AUTO_INSTALL`
- `ECHOMEM_AUTO_SYNC`

## Safe switching sequence

1. Update plugin config or `~/.openclaw/.env`.
2. Make sure the local-only flag and API key agree with the intended mode.
3. Restart the gateway.
4. Verify the gateway log shows the local workspace viewer URL.
5. In cloud mode, run `/echo-memory whoami` and `/echo-memory status`.

## Important pitfall

If the user removes the API key in the local UI sidebar, the plugin saves `ECHOMEM_LOCAL_ONLY_MODE=true` to the local env file. That local-only flag can keep winning on later restarts until it is changed back.
