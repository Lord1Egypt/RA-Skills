# Converly agent skill

Teach your AI agent to set up conversion tracking. This skill walks Claude Code, OpenClaw, Codex and other agents through the full Converly setup: install the tracking snippet, connect an ad platform, build and publish a conversion flow, verify it with a real test event, and read conversion results afterwards.

[Converly](https://converly.io) tracks form submissions on your website and fires conversions to Google Ads, Meta, GA4, LinkedIn, TikTok and more, including server side delivery (Google Enhanced Conversions, Meta CAPI).

## Install

OpenClaw:

```bash
clawhub install converly
```

Claude Code / Codex and other skill compatible agents:

```bash
npx skills add converlyio/converly-agent
```

Then ask your agent something like: "Set up conversion tracking so my Google Ads account knows when someone submits the demo form."

## What the agent can and cannot do

The agent does almost everything: account login happens in your browser (`converly login`, free trial starts automatically), the agent installs the snippet if it has access to your site's code, builds the flow, publishes it, and proves it works with a test conversion delivered to the ad platform.

One step is always yours: authorizing the ad platform. The agent hands you a link, you approve the connection in your browser. Your ad platform credentials never pass through the agent.

## Under the hood

The skill drives the [`converly` CLI](https://www.npmjs.com/package/@converly/cli) (`npm install -g @converly/cli`), which wraps Converly's [public REST API](https://developers.converly.io). Also available: the Converly MCP server at `https://app.converly.io/mcp` for Claude and ChatGPT connector users.

## License

MIT-0
