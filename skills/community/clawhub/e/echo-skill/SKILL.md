# Echo Skill

## Overview

Echo Skill is a simple HTTP-based skill that receives text input and returns the same content back to the caller.

This skill is primarily designed for testing integration workflows between ClawHub and external HTTP services.

## Use Cases

- Validate HTTP skill connectivity
- Test parameter passing
- Debug agent-tool invocation pipeline
- Verify schema validation behavior

## Input Parameters

| Name    | Type   | Required | Description                     |
|---------|--------|----------|---------------------------------|
| content | string | Yes      | The text content to echo back   |

Example:

{
  "content": "hello world"
}

## Output Format

{
  "message": "Echo: hello world"
}

## Technical Details

- Method: POST
- Endpoint: /echo
- Content-Type: application/json

## Notes

This is a development and testing skill and should not be used in production environments.