#!/usr/bin/env node
/**
 * Figma REST API：拉取节点树、简化 JSON、对比模式、SVG 导出。
 * 需要环境变量 FIGMA_TOKEN（或项目根目录 .env）。
 * 运行：Node.js 18+，无需 npm 依赖（仅需本目录 package.json 的 "type":"module"）。
 */
import { loadDotEnv } from "./load-env.js";

const FIGMA_API = "https://api.figma.com/v1";

export function parseFigmaUrl(url) {
  let u;
  try {
    u = new URL(url.trim());
  } catch {
    throw new Error(`INVALID_URL: ${url}`);
  }
  const path = u.pathname;
  const designMatch = path.match(/\/(?:design|file)\/([^/]+)/);
  if (!designMatch) throw new Error(`INVALID_URL: cannot find file key in ${url}`);
  const fileKey = designMatch[1];
  const nodeParam = u.searchParams.get("node-id") ?? u.searchParams.get("node_id");
  if (!nodeParam) throw new Error(`INVALID_URL: missing node-id in query string`);
  const nodeId = nodeParam.replace(/-/g, ":");
  return { fileKey, nodeId };
}

function getToken() {
  const t = process.env.FIGMA_TOKEN?.trim();
  if (!t) {
    console.error("FIGMA_TOKEN_NOT_SET");
    process.exit(2);
  }
  return t;
}

async function figmaGet(path, token) {
  const res = await fetch(`${FIGMA_API}${path}`, {
    headers: { "X-Figma-Token": token },
  });
  const text = await res.text();
  let body;
  try {
    body = JSON.parse(text);
  } catch {
    throw new Error(`Figma API non-JSON response (${res.status}): ${text.slice(0, 200)}`);
  }
  if (!res.ok) {
    const err = body;
    throw new Error(`Figma API ${res.status}: ${err.err ?? err.message ?? text.slice(0, 300)}`);
  }
  return body;
}

const MAX_CHILD_WARN = 200;

function pick(obj, keys) {
  const out = {};
  for (const k of keys) {
    if (obj[k] !== undefined) out[k] = obj[k];
  }
  return out;
}

function simplifyNode(node, depth, maxDepth) {
  if (node.visible === false) return {};

  const base = {
    id: node.id,
    name: node.name,
    type: node.type,
  };

  const t = node.type;
  const layoutKeys = [
    "layoutMode",
    "primaryAxisSizingMode",
    "counterAxisSizingMode",
    "primaryAxisAlignItems",
    "counterAxisAlignItems",
    "paddingLeft",
    "paddingRight",
    "paddingTop",
    "paddingBottom",
    "itemSpacing",
    "layoutAlign",
    "layoutGrow",
    "layoutSizingHorizontal",
    "layoutSizingVertical",
  ];
  const visualKeys = [
    "fills",
    "strokes",
    "strokeWeight",
    "strokeAlign",
    "effects",
    "opacity",
    "blendMode",
    "cornerRadius",
    "rectangleCornerRadii",
  ];

  if (t === "TEXT") {
    Object.assign(
      base,
      pick(node, [
        "characters",
        "style",
        "characterStyleOverrides",
        "styleOverrideTable",
      ])
    );
  } else {
    Object.assign(base, pick(node, [...layoutKeys, ...visualKeys]));
  }

  if (t === "INSTANCE") {
    Object.assign(
      base,
      pick(node, ["componentId", "variantProperties", "componentProperties"])
    );
  }

  const rawChildren = node.children;
  if (!rawChildren?.length) return base;

  if (depth >= maxDepth) {
    return {
      ...base,
      _truncated: true,
      _childCount: rawChildren.length,
    };
  }

  if (rawChildren.length > MAX_CHILD_WARN) {
    base._largeChildList = true;
    base._childCount = rawChildren.length;
  }

  const children = [];
  for (const ch of rawChildren) {
    const s = simplifyNode(ch, depth + 1, maxDepth);
    if (Object.keys(s).length > 0) children.push(s);
  }
  if (children.length) base.children = children;
  return base;
}

export function simplifyTree(root, maxDepth) {
  return simplifyNode(root, 0, maxDepth);
}

async function fetchNodes(fileKey, nodeIds, token) {
  const ids = nodeIds.map((id) => encodeURIComponent(id)).join(",");
  const data = await figmaGet(`/files/${fileKey}/nodes?ids=${ids}`, token);
  if (!data.nodes) throw new Error("Figma API: empty nodes in response");
  return { name: data.name, nodes: data.nodes };
}

async function exportSvg(fileKey, nodeIds, token) {
  const ids = nodeIds.map((id) => encodeURIComponent(id)).join(",");
  const data = await figmaGet(`/images/${fileKey}?ids=${ids}&format=svg`, token);
  return data.images ?? {};
}

function diffSummary(a, b, pathPrefix = "") {
  const lines = [];
  const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
  keys.delete("id");
  for (const k of keys) {
    const p = pathPrefix ? `${pathPrefix}.${k}` : k;
    const va = a[k];
    const vb = b[k];
    if (va === undefined && vb !== undefined) lines.push(`+ ${p}`);
    else if (va !== undefined && vb === undefined) lines.push(`- ${p}`);
    else if (typeof va === "object" && va !== null && typeof vb === "object" && vb !== null) {
      lines.push(...diffSummary(va, vb, p));
    } else if (JSON.stringify(va) !== JSON.stringify(vb)) {
      lines.push(`~ ${p}`);
    }
  }
  return lines;
}

function parseArgs(argv) {
  const args = [...argv];
  const flags = {
    compare: false,
    depth: 5,
    exportSvg: false,
    nodes: null,
    json: false,
  };
  const positional = [];
  while (args.length) {
    const x = args.shift();
    if (x === "--compare") flags.compare = true;
    else if (x === "--json") flags.json = true;
    else if (x === "--export-svg") flags.exportSvg = true;
    else if (x === "--depth") {
      const n = parseInt(args.shift() ?? "", 10);
      if (!Number.isFinite(n) || n < 1) throw new Error("--depth requires positive integer");
      flags.depth = n;
    } else if (x === "--nodes") {
      flags.nodes = args.shift() ?? "";
    } else if (!x.startsWith("-")) positional.push(x);
    else throw new Error(`Unknown flag: ${x}`);
  }
  return { flags, positional };
}

async function main() {
  loadDotEnv();
  const { flags, positional } = parseArgs(process.argv.slice(2));

  if (flags.exportSvg) {
    const token = getToken();
    const extraIds = flags.nodes
      ? flags.nodes.split(/[,\s]+/).map((s) => s.trim().replace(/-/g, ":")).filter(Boolean)
      : [];
    if (positional.length < 1) {
      console.error("Usage: node src/figma-fetch.js <figma-url> --export-svg [--nodes id1,id2]");
      process.exit(1);
    }
    const { fileKey, nodeId } = parseFigmaUrl(positional[0]);
    const ids = [nodeId, ...extraIds];
    const urls = await exportSvg(fileKey, ids, token);
    console.log(JSON.stringify({ fileKey, svgUrls: urls }, null, 2));
    return;
  }

  if (flags.compare) {
    if (positional.length < 2) {
      console.error("Usage: node src/figma-fetch.js --compare <url1> <url2> [--depth N]");
      process.exit(1);
    }
    const token = getToken();
    let maxDepth = flags.depth;
    const parsed = positional.map((u) => parseFigmaUrl(u));
    const trees = [];
    let autoDeepened = false;

    for (const p of parsed) {
      const { nodes } = await fetchNodes(p.fileKey, [p.nodeId], token);
      const doc = nodes[p.nodeId]?.document;
      if (!doc) throw new Error(`No document for node ${p.nodeId}`);
      let simplified = simplifyTree(doc, maxDepth);
      const sc = JSON.stringify(simplified);
      if (sc.includes('"_truncated":true') && maxDepth < 15) {
        maxDepth = 15;
        autoDeepened = true;
        simplified = simplifyTree(doc, maxDepth);
      }
      trees.push(simplified);
    }

    const d = diffSummary(trees[0], trees[1]);
    const out = {
      mode: "compare",
      depthUsed: maxDepth,
      autoDeepened,
      diffLines: d.slice(0, 200),
      diffTruncated: d.length > 200,
      trees,
    };
    console.log(JSON.stringify(out, null, flags.json ? 2 : 0));
    return;
  }

  if (positional.length < 1) {
    console.error(
      "Usage: node src/figma-fetch.js <figma-url> [--depth N]\n" +
        "       node src/figma-fetch.js --compare <url1> <url2> [--depth N]\n" +
        "       node src/figma-fetch.js <figma-url> --export-svg [--nodes id1,id2]\n" +
        "（在 scripts/ 目录下；亦可用 npm run figma-fetch -- <参数>）"
    );
    process.exit(1);
  }

  const token = getToken();
  const { fileKey, nodeId } = parseFigmaUrl(positional[0]);
  let maxDepth = flags.depth;
  const { name, nodes } = await fetchNodes(fileKey, [nodeId], token);
  const doc = nodes[nodeId]?.document;
  if (!doc) throw new Error(`No document for node ${nodeId}`);

  let simplified = simplifyTree(doc, maxDepth);
  if (JSON.stringify(simplified).includes('"_truncated":true') && maxDepth < 15) {
    maxDepth = 15;
    simplified = simplifyTree(doc, maxDepth);
    process.stderr.write(
      "[figma-fetch] 子树较深，已自动将 depth 提升到 " + maxDepth + "\n"
    );
  }

  const out = {
    fileKey,
    fileName: name,
    nodeId,
    depthUsed: maxDepth,
    simplified,
  };
  console.log(JSON.stringify(out, null, flags.json ? 2 : 0));
}

main().catch((e) => {
  console.error(e instanceof Error ? e.message : e);
  process.exit(1);
});
