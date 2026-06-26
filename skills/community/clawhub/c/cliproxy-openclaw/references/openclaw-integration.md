# OpenClaw integration

Use this file when the user wants CLIProxy connected to OpenClaw.

## Objective

Take a working CLIProxy deployment and convert it into a usable OpenClaw provider configuration.

## Minimum values to gather

- base URL
- API key or token
- one known-good model name
- any extra headers only if the deployment truly requires them

## Integration approach

Prefer the most direct compatible provider path that OpenClaw already supports.

In practice, that means giving the user or the runtime the exact values needed for:
- provider endpoint or base URL
- bearer token or API key
- chosen model name

## Verification steps

1. Confirm OpenClaw can reach the base URL.
2. List models if supported.
3. Send a minimal request against one known-good model.
4. If the request fails, identify whether the break is in:
   - networking
   - auth
   - model naming
   - streaming compatibility
   - upstream provider state inside CLIProxy

## Success condition

The task is done only when OpenClaw or the chosen downstream client gets a real response from a model through CLIProxy.
