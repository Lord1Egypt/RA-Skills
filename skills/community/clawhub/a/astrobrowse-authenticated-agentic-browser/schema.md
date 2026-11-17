# AstroBrowse - Authenticated Agentic Browser Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `astrobrowse-authenticated-agentic-browser`

x402 availability: not enabled for this product.

## `close_browser`

Action slug: `close-browser`

Price: `5` credits

Release the session: it is wiped and destroyed. Always call this when finished.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |

Sample parameters:

```json
{
  "browser_session_id": null
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  }
}
```

## `download_file`

Action slug: `download-file`

Price: `5` credits

Persist a file the browser downloaded into the File Manager (size-capped, requires workflow budget context). Pass download_name from list_downloads, or omit it to save the most recent download.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |
| `download_name` | `string` | no | For download_file: the download filename to persist (from list_downloads). Omit to persist the most recent completed download. |

Sample parameters:

```json
{
  "browser_session_id": null,
  "download_name": null
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  },
  "download_name": {
    "default": null,
    "description": "For download_file: the download filename to persist (from list_downloads). Omit to persist the most recent completed download.",
    "required": false,
    "type": "string"
  }
}
```

## `extract_page`

Action slug: `extract-page`

Price: `5` credits

Extract visible text (or HTML) from the active page or a selector.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |
| `include_html` | `boolean` | no | Whether extract_page should include capped outer HTML. |
| `selector` | `string` | no | Optional selector for extract_page or upload_file. |

Sample parameters:

```json
{
  "browser_session_id": null,
  "include_html": false,
  "selector": null
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  },
  "include_html": {
    "default": false,
    "description": "Whether extract_page should include capped outer HTML.",
    "required": false,
    "type": "boolean"
  },
  "selector": {
    "default": null,
    "description": "Optional selector for extract_page or upload_file.",
    "required": false,
    "type": "string"
  }
}
```

## `get_policy`

Action slug: `get-policy`

Price: `5` credits

Read the user's browsing policy (saved-only vs general browsing). The policy is set only by the human from their dashboard; there is no agent action to change it.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `heartbeat`

Action slug: `heartbeat`

Price: `5` credits

Refresh the runtime session's 10-minute idle deadline before long non-browser work. It never extends the 30-minute hard cap.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |

Sample parameters:

```json
{
  "browser_session_id": null
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  }
}
```

## `initialize_browser`

Action slug: `initialize-browser`

Price: `5` credits

Start a fresh, single-use, isolated browser session. Pass a stable idempotency_key (required) so a retry never starts a second session. Provide account_id to resume a saved login, or omit account_id for a general-browsing session (allowed only when the user has enabled general browsing). Call list_accounts first.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `account_id` | `string` | no | Saved account id for an account-backed session. Omit it to start a general-browsing session (no saved login). |
| `idempotency_key` | `string` | yes | Caller-supplied idempotency key for initialize_browser (the agent/request id). |
| `initial_url` | `string` | no | Optional URL to navigate to after initialization. Must match the account's allowed origins. |
| `region` | `string` | no | Optional region override for a general-browsing session. |

Sample parameters:

```json
{
  "account_id": null,
  "idempotency_key": null,
  "initial_url": null,
  "region": null
}
```

Generated JSON parameter schema:

```json
{
  "account_id": {
    "default": null,
    "description": "Saved account id for an account-backed session. Omit it to start a general-browsing session (no saved login).",
    "required": false,
    "type": "string"
  },
  "idempotency_key": {
    "default": null,
    "description": "Caller-supplied idempotency key for initialize_browser (the agent/request id).",
    "required": true,
    "type": "string"
  },
  "initial_url": {
    "default": null,
    "description": "Optional URL to navigate to after initialization. Must match the account's allowed origins.",
    "required": false,
    "type": "string"
  },
  "region": {
    "default": null,
    "description": "Optional region override for a general-browsing session.",
    "required": false,
    "type": "string"
  }
}
```

## `list_accounts`

Action slug: `list-accounts`

Price: `5` credits

List the user's saved AstroBrowse logins (accounts). Call this first to find a saved site before initialize_browser.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `list_downloads`

Action slug: `list-downloads`

Price: `5` credits

List files the browser has downloaded in this session (name, size, type) so you can pick one to save with download_file.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |

Sample parameters:

```json
{
  "browser_session_id": null
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  }
}
```

## `request_user_takeover`

Action slug: `request-user-takeover`

Price: `5` credits

Ask the human to take over the live browser (e.g. CAPTCHA, MFA, unusual login UI). Holds the session open past the idle timeout. Use ONLY when the agent cannot proceed automatically.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |
| `reason` | `string` | yes | Reason to show the user when requesting browser takeover. |

Sample parameters:

```json
{
  "browser_session_id": null,
  "reason": null
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  },
  "reason": {
    "default": null,
    "description": "Reason to show the user when requesting browser takeover.",
    "required": true,
    "type": "string"
  }
}
```

## `run_steps`

Action slug: `run-steps`

Price: `5` credits

Run bounded browser steps in an initialized session, including navigation, role/name targeting, drag and drop, accessible-name search, screenshots, and tab listing or switching.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |
| `steps` | `array` | yes | One to 20 AstroBrowse steps, validated as a complete batch before execution. JavaScript is not supported. Target an element with a CSS selector, or with role (+ optional name) when class names are generated and unstable; run snapshot first to read the page's roles and names. Required fields by action: goto=url; click=(selector\|role); click_at=(selector\|role)+offset_x+offset_y; hover=(selector\|role); drag=(selector\|role); drag_by=(selector\|role)+dx+dy; fill=(selector\|role)+text; type_text=(selector\|role)+text; press=key (selector optional); select=(selector\|role)+value; wait_for_load_state=none; wait_for_selector=(selector\|role); wait_for_text=text; snapshot=none; find=text; extract_text=(selector\|role); extract_html=(selector\|role); screenshot=none (selector optional); list_tabs=none; switch_tab=tab_index. drag accepts target_selector, target_role (+ target_name), or target_x+target_y. Use name_exact=true for exact accessible-name matching. Empty fill.text and select.value values are valid. |

Sample parameters:

```json
{
  "browser_session_id": null,
  "steps": null
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  },
  "steps": {
    "default": null,
    "description": "One to 20 AstroBrowse steps, validated as a complete batch before execution. JavaScript is not supported. Target an element with a CSS selector, or with role (+ optional name) when class names are generated and unstable; run snapshot first to read the page's roles and names. Required fields by action: goto=url; click=(selector|role); click_at=(selector|role)+offset_x+offset_y; hover=(selector|role); drag=(selector|role); drag_by=(selector|role)+dx+dy; fill=(selector|role)+text; type_text=(selector|role)+text; press=key (selector optional); select=(selector|role)+value; wait_for_load_state=none; wait_for_selector=(selector|role); wait_for_text=text; snapshot=none; find=text; extract_text=(selector|role); extract_html=(selector|role); screenshot=none (selector optional); list_tabs=none; switch_tab=tab_index. drag accepts target_selector, target_role (+ target_name), or target_x+target_y. Use name_exact=true for exact accessible-name matching. Empty fill.text and select.value values are valid.",
    "items": {
      "description": "AstroBrowse step shape, validated before the worker receives a batch.",
      "properties": {
        "action": {
          "description": "",
          "enum": [
            "goto",
            "click",
            "click_at",
            "hover",
            "drag",
            "drag_by",
            "fill",
            "type_text",
            "press",
            "select",
            "wait_for_load_state",
            "wait_for_selector",
            "wait_for_text",
            "snapshot",
            "find",
            "extract_text",
            "extract_html",
            "screenshot",
            "list_tabs",
            "switch_tab"
          ],
          "required": true,
          "type": "string"
        },
        "blur": {
          "default": null,
          "description": "CSS selectors to frost (blur) on the live page before this step acts, so secrets never appear in a recording. Persists until navigation. Fails closed: every selector must blur at least one element on the current page (a typo'd selector matching nothing is unverifiable), otherwise the step aborts with BROWSER_AUTOMATION_BLUR_FAILED instead of recording the secret unblurred. If the target renders later, wait_for_selector first.",
          "items": {
            "description": "",
            "type": "string"
          },
          "required": false,
          "type": "array"
        },
        "button": {
          "default": null,
          "description": "Mouse button for click. Defaults to left.",
          "enum": [
            "left",
            "right",
            "middle"
          ],
          "required": false,
          "type": "string"
        },
        "click_count": {
          "default": null,
          "description": "Click repetitions. Use 2 for a double-click.",
          "maximum": 3,
          "minimum": 1,
          "required": false,
          "type": "integer"
        },
        "dx": {
          "default": null,
          "description": "Horizontal pixels to drag for drag_by. May be negative.",
          "maximum": 10000,
          "minimum": -10000,
          "required": false,
          "type": "integer"
        },
        "dy": {
          "default": null,
          "description": "Vertical pixels to drag for drag_by. May be negative.",
          "maximum": 10000,
          "minimum": -10000,
          "required": false,
          "type": "integer"
        },
        "key": {
          "default": null,
          "description": "",
          "required": false,
          "type": "string"
        },
        "marker": {
          "default": null,
          "description": "Visual marker drawn on the page right before a step acts.",
          "properties": {
            "margin": {
              "default": 16,
              "description": "",
              "maximum": 60,
              "minimum": 4,
              "required": false,
              "type": "integer"
            },
            "shape": {
              "default": "oval",
              "description": "",
              "enum": [
                "oval",
                "circle"
              ],
              "required": false,
              "type": "string"
            }
          },
          "required": false,
          "type": "object"
        },
        "modifiers": {
          "default": null,
          "description": "Modifier keys held during click, e.g. ['Shift'].",
          "items": {
            "description": "",
            "enum": [
              "Alt",
              "Control",
              "Meta",
              "Shift"
            ],
            "type": "string"
          },
          "required": false,
          "type": "array"
        },
        "name": {
          "default": null,
          "description": "Accessible name filter used with role (substring match).",
          "required": false,
          "type": "string"
        },
        "name_exact": {
          "default": false,
          "description": "Match the accessible name exactly when role and name are supplied.",
          "required": false,
          "type": "boolean"
        },
        "offset_x": {
          "default": null,
          "description": "X offset inside the target element for click_at.",
          "maximum": 10000,
          "minimum": 0,
          "required": false,
          "type": "integer"
        },
        "offset_y": {
          "default": null,
          "description": "Y offset inside the target element for click_at.",
          "maximum": 10000,
          "minimum": 0,
          "required": false,
          "type": "integer"
        },
        "role": {
          "default": null,
          "description": "Accessibility role to target instead of a CSS selector, e.g. 'button'. Pair with name and name_exact for an exact match. Survives generated class names; read available roles with a snapshot step.",
          "required": false,
          "type": "string"
        },
        "selector": {
          "default": null,
          "description": "",
          "required": false,
          "type": "string"
        },
        "tab_index": {
          "default": null,
          "description": "Tab index from list_tabs for switch_tab.",
          "maximum": 100,
          "minimum": 0,
          "required": false,
          "type": "integer"
        },
        "target_name": {
          "default": null,
          "description": "Accessible name of the drag drop target.",
          "required": false,
          "type": "string"
        },
        "target_name_exact": {
          "default": false,
          "description": "Match target_name exactly.",
          "required": false,
          "type": "boolean"
        },
        "target_role": {
          "default": null,
          "description": "Drop target accessibility role for drag.",
          "required": false,
          "type": "string"
        },
        "target_selector": {
          "default": null,
          "description": "Drop target for drag, as a CSS selector.",
          "required": false,
          "type": "string"
        },
        "target_x": {
          "default": null,
          "description": "Viewport X coordinate for drag drop.",
          "maximum": 10000,
          "minimum": 0,
          "required": false,
          "type": "integer"
        },
        "target_y": {
          "default": null,
          "description": "Viewport Y coordinate for drag drop.",
          "maximum": 10000,
          "minimum": 0,
          "required": false,
          "type": "integer"
        },
        "text": {
          "default": null,
          "description": "",
          "required": false,
          "type": "string"
        },
        "timeout_ms": {
          "default": 10000,
          "description": "",
          "maximum": 60000,
          "minimum": 500,
          "required": false,
          "type": "integer"
        },
        "url": {
          "default": null,
          "description": "",
          "required": false,
          "type": "string"
        },
        "value": {
          "default": null,
          "description": "",
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "maxItems": 20,
    "minItems": 1,
    "required": true,
    "type": "array"
  }
}
```

## `screenshot`

Action slug: `screenshot`

Price: `5` credits

Capture a PNG screenshot and save it to your File Manager (requires workflow budget context). The image is NOT returned inline; the response has artifact.file_id and a fresh artifact.signed_url for viewing or analysis.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |

Sample parameters:

```json
{
  "browser_session_id": null
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  }
}
```

## `start_recording`

Action slug: `start-recording`

Price: `5` credits

Start an MP4 screen recording of the session. show_cursor controls whether the cursor appears in the video.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |
| `show_cursor` | `boolean` | no | For start_recording: capture the real cursor in the video. Only human (takeover) interaction moves the real cursor; agent-driven motion uses the run_steps tutorial fake cursor instead. |

Sample parameters:

```json
{
  "browser_session_id": null,
  "show_cursor": true
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  },
  "show_cursor": {
    "default": true,
    "description": "For start_recording: capture the real cursor in the video. Only human (takeover) interaction moves the real cursor; agent-driven motion uses the run_steps tutorial fake cursor instead.",
    "required": false,
    "type": "boolean"
  }
}
```

## `status`

Action slug: `status`

Price: `5` credits

Return the session's sanitized live status (no cookies).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |

Sample parameters:

```json
{
  "browser_session_id": null
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  }
}
```

## `stop_recording`

Action slug: `stop-recording`

Price: `5` credits

Stop the recording and save the MP4 to your File Manager (requires workflow budget context). The video is NOT returned inline; the response has artifact.file_id — fetch it from the File Manager to view the recording. Call before close_browser.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |

Sample parameters:

```json
{
  "browser_session_id": null
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  }
}
```

## `upload_file`

Action slug: `upload-file`

Price: `5` credits

Attach File Manager files to one input[type=file] on the active tab. Hidden file inputs are supported; pass a selector and file_ids.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |
| `file_ids` | `array` | yes | File Manager file_id values for upload_file. |
| `selector` | `string` | yes | Optional selector for extract_page or upload_file. |

Sample parameters:

```json
{
  "browser_session_id": null,
  "file_ids": null,
  "selector": null
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  },
  "file_ids": {
    "default": null,
    "description": "File Manager file_id values for upload_file.",
    "items": {
      "description": "",
      "type": "string"
    },
    "required": true,
    "type": "array"
  },
  "selector": {
    "default": null,
    "description": "Optional selector for extract_page or upload_file.",
    "required": true,
    "type": "string"
  }
}
```

## `wait_for_takeover`

Action slug: `wait-for-takeover`

Price: `5` credits

Poll the session status after request_user_takeover.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser_session_id` | `string` | yes | Opaque browser runtime session id returned by initialize_browser. |

Sample parameters:

```json
{
  "browser_session_id": null
}
```

Generated JSON parameter schema:

```json
{
  "browser_session_id": {
    "default": null,
    "description": "Opaque browser runtime session id returned by initialize_browser.",
    "required": true,
    "type": "string"
  }
}
```
