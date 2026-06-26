#!/usr/bin/env node
// CLI wrapper for figma-mcp.mjs — separates env reading from network code.
// Usage: FIGMA_MCP_TOKEN=... node figma-mcp-cli.mjs [tool] [key=value ...] [--out <file>]
//
// Special: --out <file> for screenshot/image tools saves PNG directly to file
// (decodes base64 from API response) instead of printing JSON to stdout.

import { createClient } from './figma-mcp.mjs';
import { writeFileSync } from 'node:fs';

const token = process.env.FIGMA_MCP_TOKEN;
if (!token) { console.error('Set FIGMA_MCP_TOKEN'); process.exit(1); }

const [, , toolName, ...rest] = process.argv;

// Parse args + --out flag
const outIdx = rest.indexOf('--out');
const outFile = outIdx >= 0 ? rest[outIdx + 1] : null;
const cleanArgs = outFile !== null
  ? rest.filter((a, i) => i !== outIdx && i !== outIdx + 1)
  : rest;

const client = createClient({ token });
await client.initialize();
console.error(`Session: ${client.sessionId}`);

if (!toolName || toolName === 'list') {
  const tools = await client.listTools();
  for (const t of tools) console.log(`  ${t.name}`);
  console.error(`${tools.length} tools`);
} else {
  const args = {};
  for (const a of cleanArgs) {
    const eq = a.indexOf('=');
    if (eq > 0) args[a.slice(0, eq)] = a.slice(eq + 1);
  }
  const result = await client.call(toolName, args);

  // For screenshot tools: decode base64 image from result and save to file
  // so it can be sent as a Telegram attachment via the `image` tool.
  const screenshotTools = new Set([
    'get_screenshot', 'export_image', 'get_thumbnail',
    'render_node', 'render_document',
  ]);
  if (outFile && screenshotTools.has(toolName)) {
    const base64 = extractBase64FromResult(result);
    if (base64) {
      const buf = Buffer.from(base64, 'base64');
      writeFileSync(outFile, buf);
      console.error(`Image saved: ${outFile} (${buf.length} bytes)`);
      // Emit minimal JSON for automation
      console.log(JSON.stringify({ ok: true, file: outFile, size: buf.length }));
    } else {
      console.error(`No image found in result for tool "${toolName}". Falling back to JSON output.`);
      console.log(JSON.stringify(result, null, 2));
    }
  } else {
    console.log(JSON.stringify(result, null, 2));
  }
}

/**
 * Extract base64 image data from an Figma MCP result object.
 * Figma returns: { content: [{ type: "image", data: "base64..." }] }
 * or direct base64 string.
 */
function extractBase64FromResult(result) {
  if (!result) return null;
  // Direct string
  if (typeof result === 'string') return extractFromString(result);
  // Array format: { content: [{ type: "image", data: "base64..." }] }
  if (Array.isArray(result)) {
    for (const item of result) {
      if (item?.type === 'image' && item?.data) {
        const b64 = typeof item.data === 'string' ? item.data : extractFromString(item.data);
        if (b64) return b64;
      }
    }
  }
  // Object with image field
  if (typeof result === 'object') {
    for (const key of ['image', 'data', 'base64', 'img', 'screenshot']) {
      if (result[key] && typeof result[key] === 'string') {
        const b64 = extractFromString(result[key]);
        if (b64) return b64;
      }
    }
    // Nested content array
    if (Array.isArray(result.content)) {
      return extractBase64FromResult(result.content);
    }
  }
  return null;
}

function extractFromString(str) {
  if (!str || typeof str !== 'string') return null;
  const trimmed = str.trim();
  // Data URL prefix
  const dataIdx = trimmed.indexOf(',');
  if (dataIdx >= 0) return trimmed.slice(dataIdx + 1);
  // Bare base64 (alphanumeric + / + =, at least 20 chars)
  if (/^[A-Za-z0-9+/=]{20,}$/.test(trimmed)) return trimmed;
  return null;
}
