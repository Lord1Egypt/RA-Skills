# Bland

## Before the call

Call the check from your own code before you send the call, and skip numbers that return `use_link` or
`do_not_call`:

```bash
curl "https://linepref.byronwebstudio.com.au/v1/check?number=%2B15125550100&website=example.com"
```

## During the call (webhook tool)

In the tool builder, create a webhook tool:

- **Name:** `record_opt_out`
- **Description:** "Use when the person asks to stop being called (scope caller), or asks to stop automated
  assistant calls from all callers (scope all)."
- **Method:** `POST`
- **URL:** `https://linepref.byronwebstudio.com.au/v1/optout`
- **Body:**

  ```json
  {
    "number": "{{called_number}}",
    "scope": "{{scope}}"
  }
  ```

- **Input variables:** add `scope` (text, required, instructions: "caller or all"). Pass `called_number` as a
  variable on the call when you send it, set to the number you are dialling, so the agent does not have to
  fill it.

Opening line for the task prompt:

> This is an automated assistant. To stop calls from us, say "stop calling" at any time. To stop automated
> assistant calls from all participating callers, say "stop all assistant calls".

This recipe uses a spoken opt-out because Bland's tool documentation does not describe key-press handling.
If your Bland setup does pass key presses to the agent, use the key-press wording from the main skill
(9 for this caller, 8 for all participating callers).

## After the call

From your webhook or post-call code:

```bash
curl -X POST https://linepref.byronwebstudio.com.au/v1/outcome -H 'content-type: application/json' \
  -d '{"number":"+15125550100","code":"connected_human"}'
```
