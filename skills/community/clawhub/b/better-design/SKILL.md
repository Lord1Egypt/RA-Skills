---
name: better-design
description: Design harness for coding agents. Connects OpenClaw to the Better Design MCP server so the apps, sites and screens it builds use a real design system, follow UI and UX principles, and pass review checks for accessibility, copy and spacing. Use when the user asks for an app, site, page, dashboard or component, or asks to choose, create, install or review a design system or interface.
version: 1.0.1
homepage: https://better-design.com
metadata:
  openclaw:
    emoji: "🎨"
    homepage: https://better-design.com
    envVars:
      - name: BETTER_DESIGN_API_KEY
        required: false
        description: Optional Better Design API key (bd_live_...) for a headless Gateway that cannot open a browser sign-in. Create one at https://better-design.com/mcp. OAuth sign-in needs no key.
---

# Better Design

Better Design is a remote MCP server at `https://better-design.com/api/mcp`. It gives the agent design systems, UI and UX principles, icons and review checks. This skill says how to connect it and the order to use its tools in.

## 1. Connect the server once

Check whether a `better-design` server is already configured:

```bash
openclaw mcp status --verbose
```

If it is missing, add it with OAuth sign-in. This is the default and needs no key:

```bash
openclaw mcp set better-design '{"url":"https://better-design.com/api/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login better-design
openclaw mcp doctor better-design --probe
```

`openclaw mcp login` prints a sign-in link. The user opens it, signs in to Better Design with email, Google or GitHub, and approves access. A free account works. You can also add the server in the Control UI under **Settings → MCP** with the same URL and the Streamable HTTP transport, then select **Sign in**.

On a headless Gateway that cannot open a browser, use an API key instead. The user creates it at https://better-design.com/mcp and stores it as `BETTER_DESIGN_API_KEY` through the Gateway's secret mechanism. Send it as the header `Authorization: Bearer <key>`. Never write the key into a config literal or into chat.

The probe must list tools such as `find-design-system` and `get-design-system-kit` before you continue.

## 2. Keep the design system the project already has

If `components/ui/` already holds a Better Design system, or `components/icons/.library.json` names an icon library, build with those. Change them only when the user asks.

## 3. Choose a design system with the user

1. Call `find-design-system` with a short description of the product and its audience.
2. Show the user the top matches, each with its name and preview link, and let the user pick one. Do not pick for them.
3. For a custom brand, call `create-design-system` with a description of the look. Pass the chosen match as `baseDesignSystemId`, or pass `brandCss` from `extract-from-url` or `extract-design-system` when the user has an existing site or stylesheet. Creating a custom system uses credits from the user's Better Design account.
4. Poll `get-design-system-status` until the system is ready, then share its preview link.

## 4. Install it

Call `get-design-system-kit` with the target that fits the project:

| Project | Target |
| --- | --- |
| React or Next.js with a terminal | `react`, then run the returned install command |
| An inline canvas or artifact with no build step | `html` |
| React Native or Expo (Pro plan) | `react-native` |
| An iOS app in SwiftUI (Pro plan) | `swiftui` |
| A Shopify theme (Pro plan) | `shopify` |

Build with the installed components instead of writing new ones.

## 5. Check the principles for the job

- Before styling, call `get-ui-principle` with the topic, such as `spacing`, `typography` or `color`.
- Before building a flow, call `get-ux-principle` with the topic, such as `forms`, `onboarding` or `errors`.
- For icons, call `find-icon-library`, then `find-icons`, then `install-icons`, and save the returned files.

## 6. Review before you present

1. Call `get-review-rules` for the categories that apply: `accessibility`, `visual-design`, `animation`, `content`, `comprehension` or `ai-features`. Check the code against each rule.
2. Call `check-comprehension` with the screen's headline, body and action labels. It flags insider words and actions that hide their result.
3. When a browser is available, call `inspect-spacing` with no states to get the capture script, run it in the rendered page at desktop and mobile widths, then call `inspect-spacing` again with the captured states.
4. For a dashboard, call `review-dashboard-structure` with the page source, its data fixture and the installed component sources. Then call `finalize-dashboard-review`, and present the dashboard only on a VALID receipt.

Fix every critical and serious finding, run the checks again, and tell the user what changed and what remains.

## Support

Docs: https://better-design.com/mcp/install · Privacy: https://better-design.com/privacy · Terms: https://better-design.com/terms · Support: info@better-design.com
