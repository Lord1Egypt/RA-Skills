# Android REPL Smoke Flow

Use this checklist when validating a fresh setup.

## Preconditions

- Android REPL app installed
- API service running
- controlling machine on the same LAN
- `agent-android` available on `PATH`

## Checklist

1. Save the device URL:

```text
set url http://<device-ip>:8080
```

2. Check service health:

```bash
curl http://<device-ip>:8080/health
```

3. List launcher apps:

```bash
agent-android --apps --url http://<device-ip>:8080
```

4. Launch the target app.
5. List the current UI tree.
6. Perform one tap.
7. Perform one text input if relevant.
8. Navigate back.

## Success Criteria

- the device responds
- launcher apps are visible
- launch succeeds
- the UI tree refreshes after actions
- the user can complete at least one inspect -> act -> inspect loop


