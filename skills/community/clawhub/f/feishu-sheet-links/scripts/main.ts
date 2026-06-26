/**
 * feishu-sheet-links — standalone skill
 *
 * Extracts all hyperlinks from a public Feishu spreadsheet (all sheet tabs).
 *
 * Usage:
 *   npx -y bun main.ts <spreadsheet-url> [-o output.json]
 *
 * Env vars:
 *   FEISHU_CHROME_PATH    Custom Chrome executable path
 *   FEISHU_CHROME_PROFILE Custom Chrome profile directory
 */

import { writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

import {
  CdpSession,
  evaluate,
  findExistingChrome,
  getFreePort,
  killChrome,
  launchChrome,
  waitForDebugPort,
} from "./cdp.js";

function sleep(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms));
}

// ── JS injected into the page ────────────────────────────────────────────────

const GET_SHEET_IDS_JS = `
(function() {
  var spread = window.spreadApp &&
    window.spreadApp.collaborativeSpread &&
    window.spreadApp.collaborativeSpread._spread;
  if (!spread) return null;
  var idMap = spread.sheetIdToIndexMap;
  if (!(idMap instanceof Map)) return null;
  var entries = [];
  idMap.forEach(function(idx, id) { entries.push([id, idx]); });
  var names = {};
  for (var i = 0; i < spread.sheets.length; i++) {
    var s = spread.sheets[i];
    if (s) names[i] = s._name || String(i);
  }
  return JSON.stringify({ entries: entries, names: names });
})()
`;

// Try multiple APIs to programmatically activate a sheet so its data model loads
function makeActivateSheetJs(sheetIndex: number): string {
  return `(function() {
  var spread = window.spreadApp &&
    window.spreadApp.collaborativeSpread &&
    window.spreadApp.collaborativeSpread._spread;
  if (!spread) return false;
  try {
    if (typeof spread.setActiveSheetIndex === 'function') {
      spread.setActiveSheetIndex(${sheetIndex}); return true;
    }
    if (typeof spread.setActiveSheet === 'function') {
      var s = spread.sheets[${sheetIndex}];
      if (s) { spread.setActiveSheet(s); return true; }
    }
    if (spread.activeSheetIndex !== undefined) {
      spread.activeSheetIndex = ${sheetIndex}; return true;
    }
  } catch(e) {}
  return false;
})()`;
}

// Returns true once the target sheet's content model is populated
function makeWaitForSheetJs(sheetIndex: number): string {
  return `(function() {
  var spread = window.spreadApp &&
    window.spreadApp.collaborativeSpread &&
    window.spreadApp.collaborativeSpread._spread;
  if (!spread) return false;
  var sheet = spread.sheets[${sheetIndex}];
  if (!sheet) return false;
  return !!(sheet._dataModel && sheet._dataModel.contentModel);
})()`;
}

// Returns JSON array of links for one specific sheet, or null if not loaded yet.
// Returns "[]" (empty array JSON) when sheet is loaded but has no links.
function makeExtractSheetLinksJs(sheetIndex: number): string {
  return `(function() {
  var spread = window.spreadApp &&
    window.spreadApp.collaborativeSpread &&
    window.spreadApp.collaborativeSpread._spread;
  if (!spread) return null;
  var sheet = spread.sheets[${sheetIndex}];
  if (!sheet) return null;
  var cm = sheet._dataModel && sheet._dataModel.contentModel;
  if (!cm) return null;
  var links = [];
  var seen = new Set();

  // url-type: whole-cell hyperlinks
  var linkMap = cm.link && cm.link.idToRef && cm.link.idToRef._map;
  if (linkMap instanceof Map) {
    linkMap.forEach(function(val) {
      if (val && val.link && !seen.has(val.link)) {
        seen.add(val.link);
        links.push({ text: val.text || val.link, url: val.link });
      }
    });
  }

  // mention-type: inline rich-text hyperlinks
  var table = cm.segmentModel && cm.segmentModel.table;
  if (Array.isArray(table)) {
    for (var ri = 0; ri < table.length; ri++) {
      var row = table[ri];
      if (!row || !row.data) continue;
      for (var ci = 0; ci < row.data.length; ci++) {
        var cell = row.data[ci];
        if (!Array.isArray(cell)) continue;
        for (var seg of cell) {
          if (seg && seg.type === 'mention' && seg.link && !seen.has(seg.link)) {
            seen.add(seg.link);
            links.push({ text: seg.text || seg.link, url: seg.link });
          }
        }
      }
    }
  }

  return JSON.stringify(links);
})()`;
}

// ── Types ────────────────────────────────────────────────────────────────────

interface Link { text: string; url: string; }
interface SheetLinks { [sheetName: string]: Link[]; }
interface SheetInfo { id: string; index: number; name: string; }

// ── Helpers ──────────────────────────────────────────────────────────────────

async function waitForSpread(
  cdp: CdpSession,
  sid: string,
  timeoutMs = 25_000
): Promise<boolean> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    await sleep(1_000);
    const val = await evaluate<string>(cdp, sid, GET_SHEET_IDS_JS, 5_000);
    if (val) return true;
  }
  return false;
}

async function getSheetIds(cdp: CdpSession, sid: string): Promise<SheetInfo[]> {
  const raw = await evaluate<string>(cdp, sid, GET_SHEET_IDS_JS, 10_000);
  if (!raw) return [];
  const data = JSON.parse(raw) as {
    entries: Array<[string, number]>;
    names: Record<number, string>;
  };
  return data.entries.map(([id, index]) => ({
    id,
    index,
    name: data.names[index] ?? String(index),
  }));
}

// Wait specifically for target sheet's data model to be populated.
async function waitForSheetData(
  cdp: CdpSession,
  sid: string,
  sheetIndex: number,
  timeoutMs = 25_000
): Promise<boolean> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    await sleep(1_000);
    const val = await evaluate<boolean>(cdp, sid, makeWaitForSheetJs(sheetIndex), 5_000);
    if (val) return true;
  }
  return false;
}

// Extract links for one sheet. Returns empty array if loaded but has no links.
// Retries only while contentModel is null (not yet loaded).
async function extractSheetLinks(
  cdp: CdpSession,
  sid: string,
  sheetIndex: number,
  timeoutMs = 15_000
): Promise<Link[]> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    await sleep(500);
    const raw = await evaluate<string>(cdp, sid, makeExtractSheetLinksJs(sheetIndex), 5_000);
    if (raw !== null && raw !== undefined) {
      return JSON.parse(raw) as Link[];
    }
  }
  return [];
}

async function openTabForSheet(
  cdp: CdpSession,
  url: string,
  sheet: SheetInfo
): Promise<Link[]> {
  console.log(`  [${sheet.name}] Opening tab (index=${sheet.index})...`);
  const { targetId } = await cdp.send<{ targetId: string }>(
    "Target.createTarget",
    { url }
  );
  const { sessionId: sid } = await cdp.send<{ sessionId: string }>(
    "Target.attachToTarget",
    { targetId, flatten: true }
  );
  await cdp.send("Page.enable", {}, { sessionId: sid });

  const spreadReady = await waitForSpread(cdp, sid, 30_000);
  if (!spreadReady) {
    console.warn(`  [${sheet.name}] Warning: spread not ready`);
    try { await cdp.send("Target.closeTarget", { targetId }); } catch {}
    return [];
  }

  // Programmatically activate the target sheet to trigger its lazy data load
  await evaluate(cdp, sid, makeActivateSheetJs(sheet.index), 5_000);

  const dataReady = await waitForSheetData(cdp, sid, sheet.index, 25_000);
  if (!dataReady) {
    console.warn(`  [${sheet.name}] Warning: sheet data not ready after 25s`);
  }

  const links = await extractSheetLinks(cdp, sid, sheet.index, 15_000);

  try { await cdp.send("Target.closeTarget", { targetId }); } catch {}
  return links;
}

function stripSheetParam(url: string): string {
  const u = new URL(url);
  u.searchParams.delete("sheet");
  return u.toString();
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function run(spreadsheetUrl: string, outputPath: string): Promise<void> {
  const existingWs = await findExistingChrome();
  let cdp: CdpSession;
  let ownedProcess: Awaited<ReturnType<typeof launchChrome>> | null = null;

  if (existingWs) {
    cdp = await CdpSession.connect(existingWs);
  } else {
    const port = await getFreePort();
    console.log(`Launching Chrome on port ${port}...`);
    ownedProcess = await launchChrome(spreadsheetUrl, port);
    const wsUrl = await waitForDebugPort(port, 30_000);
    cdp = await CdpSession.connect(wsUrl);
  }

  try {
    // Open the spreadsheet once to discover all sheet IDs
    console.log("Discovering sheets...");
    const { targetId: rootTarget } = await cdp.send<{ targetId: string }>(
      "Target.createTarget",
      { url: spreadsheetUrl }
    );
    const { sessionId: rootSid } = await cdp.send<{ sessionId: string }>(
      "Target.attachToTarget",
      { targetId: rootTarget, flatten: true }
    );
    await cdp.send("Page.enable", {}, { sessionId: rootSid });

    const ready = await waitForSpread(cdp, rootSid, 30_000);
    if (!ready) throw new Error("Spreadsheet JS model did not initialize within timeout");

    const sheets = await getSheetIds(cdp, rootSid);
    console.log(`Found ${sheets.length} sheets: ${sheets.map((s) => s.name).join(", ")}`);

    try { await cdp.send("Target.closeTarget", { targetId: rootTarget }); } catch {}

    const allLinks: SheetLinks = {};
    const baseUrl = stripSheetParam(spreadsheetUrl);

    // Open a dedicated tab per sheet — each tab loads only its own data model
    for (const sheet of sheets) {
      const links = await openTabForSheet(
        cdp,
        `${baseUrl}?sheet=${sheet.id}`,
        sheet
      );
      allLinks[sheet.name] = links;
      console.log(`  ${sheet.name}: ${links.length} links`);
    }

    // Output
    await mkdir(path.dirname(outputPath), { recursive: true });
    await writeFile(outputPath, JSON.stringify(allLinks, null, 2), "utf-8");

    const total = Object.values(allLinks).reduce((s, v) => s + v.length, 0);
    console.log(`\nDone. ${total} links across ${Object.keys(allLinks).length} sheets.`);
    console.log(`Saved: ${outputPath}`);

    console.log("\n--- Links ---");
    for (const [month, links] of Object.entries(allLinks)) {
      console.log(`\n## ${month} (${links.length})`);
      for (const l of links) console.log(`- [${l.text}](${l.url})`);
    }
  } finally {
    cdp.close();
    if (ownedProcess) killChrome(ownedProcess);
  }
}

// ── CLI ──────────────────────────────────────────────────────────────────────

const argv = process.argv.slice(2);
const url = argv.find((a) => !a.startsWith("-"));
const oIdx = argv.indexOf("-o");
const output = oIdx >= 0 ? argv[oIdx + 1] : path.join(process.cwd(), "feishu-sheet-links.json");

if (!url) {
  console.error("Usage: bun main.ts <spreadsheet-url> [-o output.json]");
  process.exit(1);
}

run(url, output).catch((err) => {
  console.error("Error:", err instanceof Error ? err.message : String(err));
  process.exit(1);
});
