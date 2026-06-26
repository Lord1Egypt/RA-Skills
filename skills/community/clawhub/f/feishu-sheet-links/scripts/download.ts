/**
 * feishu-sheet-links — batch download script
 *
 * Downloads all linked articles from a feishu-sheet-links JSON output file.
 * Supports resume: already-downloaded URLs are skipped.
 *
 * Usage:
 *   npx -y bun download.ts <links.json> [-o output-dir] [-c concurrency]
 *
 * Options:
 *   <links.json>     Output from main.ts ({"月": [{text, url}, ...], ...})
 *   -o <dir>         Output directory (default: ./feishu-articles)
 *   -c <n>           Concurrent downloads (default: 5)
 *   --max-wait <ms>  Max page wait in ms (default: 20000)
 */

import { writeFile, mkdir } from "node:fs/promises";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import process from "node:process";

import { CdpSession, findExistingChrome, getFreePort, launchChrome, waitForDebugPort } from "./cdp.js";

// ── Types ────────────────────────────────────────────────────────────────────

interface Link { text: string; url: string; }
interface LinksFile { [month: string]: Link[]; }
interface ProgressEntry { status: "ok" | "empty" | "error" | "timeout" | "skipped"; file?: string; chars?: number; error?: string; }
interface Progress { [url: string]: ProgressEntry; }

// ── Constants ────────────────────────────────────────────────────────────────

const SKIP_DOMAINS = new Set(["pan.xunlei.com", "internal-api-drive-stream.feishu.cn"]);
const MIN_CHARS = 80;

const EXTRACT_JS = `
(function() {
  var title = document.title
    .replace(/\\s*[-–|]\\s*(飞书|Feishu|lark).*$/i, '')
    .replace(/\\s*-\\s*飞书云文档\\s*$/, '').trim();
  var body = document.body.innerText
    .replace(/^[\\s\\S]*?登录\\/注册\\n/, '')
    .replace(/\\n评论（\\d+）[\\s\\S]*$/, '')
    .replace(/\\n帮助中心[\\s\\S]*$/, '')
    .trim();
  return JSON.stringify({ title, body, chars: body.length });
})()
`;

// ── Helpers ──────────────────────────────────────────────────────────────────

function slugify(text: string, maxLen = 60): string {
  return text
    .replace(/[^\w\s一-鿿㐀-䶿]/g, "")
    .replace(/\s+/g, "-")
    .trim()
    .slice(0, maxLen);
}

function sleep(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms));
}

async function getAnchorWs(ports = [64023, 9222, 9229]): Promise<string | null> {
  for (const port of ports) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json`, { signal: AbortSignal.timeout(2000) });
      if (!res.ok) continue;
      const pages = (await res.json()) as Array<{ webSocketDebuggerUrl?: string }>;
      const page = pages.find((p) => p.webSocketDebuggerUrl);
      if (page?.webSocketDebuggerUrl) return page.webSocketDebuggerUrl;
    } catch {}
  }
  return null;
}

// ── Download one URL ─────────────────────────────────────────────────────────

async function downloadOne(
  anchorWs: string,
  url: string,
  maxWaitMs: number
): Promise<{ title: string; body: string } | null> {
  const cdp = await CdpSession.connect(anchorWs);
  try {
    const { targetId } = await cdp.send<{ targetId: string }>("Target.createTarget", { url });
    const { sessionId: sid } = await cdp.send<{ sessionId: string }>(
      "Target.attachToTarget", { targetId, flatten: true }
    );
    await cdp.send("Page.enable", {}, { sessionId: sid });

    // Adaptive wait: poll every 600ms until content appears or timeout
    const deadline = Date.now() + maxWaitMs;
    let result: { title: string; body: string; chars: number } | null = null;
    while (Date.now() < deadline) {
      await sleep(600);
      const raw = await cdp.send<{ result: { value?: string } }>(
        "Runtime.evaluate",
        { expression: EXTRACT_JS, returnByValue: true, awaitPromise: false },
        { sessionId: sid, timeoutMs: 5000 }
      );
      const val = raw.result.value;
      if (val) {
        const parsed = JSON.parse(val) as { title: string; body: string; chars: number };
        if (parsed.chars >= MIN_CHARS) { result = parsed; break; }
      }
    }

    try { await cdp.send("Target.closeTarget", { targetId }); } catch {}
    return result;
  } finally {
    cdp.close();
  }
}

// ── Worker ───────────────────────────────────────────────────────────────────

async function processItem(
  sem: { acquire(): Promise<void>; release(): void },
  anchorWs: string,
  outDir: string,
  progress: Progress,
  progressPath: string,
  lock: { locked: boolean },
  i: number,
  total: number,
  month: string,
  text: string,
  url: string,
  maxWaitMs: number
): Promise<void> {
  const domain = new URL(url).hostname;
  if (SKIP_DOMAINS.has(domain)) {
    console.log(`[${i + 1}/${total}] SKIP  ${text.slice(0, 50)}`);
    progress[url] = { status: "skipped" };
    writeFileSync(progressPath, JSON.stringify(progress, null, 2));
    return;
  }

  console.log(`[${i + 1}/${total}] ${month} | ${text.slice(0, 55)}`);

  await sem.acquire();
  let data: { title: string; body: string } | null = null;
  try {
    // Try twice on empty result
    for (let attempt = 1; attempt <= 2; attempt++) {
      try {
        data = await Promise.race([
          downloadOne(anchorWs, url, maxWaitMs),
          new Promise<null>((_, reject) => setTimeout(() => reject(new Error("timeout")), 90_000)),
        ]);
      } catch (e) {
        const msg = e instanceof Error ? e.message : String(e);
        if (msg === "timeout") {
          console.log(`  ✗ [${i + 1}] Timeout`);
          progress[url] = { status: "timeout" };
        } else {
          console.log(`  ✗ [${i + 1}] Error: ${msg}`);
          progress[url] = { status: "error", error: msg.slice(0, 80) };
        }
        writeFileSync(progressPath, JSON.stringify(progress, null, 2));
        return;
      }
      if (data && data.body.length >= MIN_CHARS) break;
      if (attempt === 1) {
        console.log(`  ↺ [${i + 1}] Empty (${data?.body.length ?? 0} chars), retrying…`);
        await sleep(5000);
        data = null;
      }
    }
  } finally {
    sem.release();
  }

  if (!data || data.body.length < MIN_CHARS) {
    console.log(`  ✗ [${i + 1}] Empty after retry: ${text.slice(0, 40)}`);
    progress[url] = { status: "empty" };
    writeFileSync(progressPath, JSON.stringify(progress, null, 2));
    return;
  }

  // Prefer link text over extracted title: document.title on Feishu pages is often just "Docs"
  const GENERIC_TITLES = new Set(["docs", "doc", "飞书云文档", "feishu", "lark"]);
  const extractedTitle = data.title?.trim() ?? "";
  const title = (extractedTitle && !GENERIC_TITLES.has(extractedTitle.toLowerCase())) ? extractedTitle : text;
  const slug = slugify(title);
  let fname = `${month}-${slug}.md`;
  let fpath = path.join(outDir, fname);
  if (existsSync(fpath)) { fname = `${month}-${slug}-${i}.md`; fpath = path.join(outDir, fname); }

  const now = new Date().toISOString();
  const md = `---\nurl: ${url}\ntitle: "${title.replace(/"/g, "'")}"\nmonth: ${month}\ncaptured_at: "${now}"\n---\n\n# ${title}\n\n${data.body}\n`;
  await writeFile(fpath, md, "utf-8");

  console.log(`  ✓ [${i + 1}] ${data.body.length.toLocaleString()} chars → ${fname}`);
  progress[url] = { status: "ok", file: fname, chars: data.body.length };
  writeFileSync(progressPath, JSON.stringify(progress, null, 2));
}

// ── Semaphore ────────────────────────────────────────────────────────────────

function makeSemaphore(n: number) {
  let count = 0;
  const queue: Array<() => void> = [];
  return {
    acquire(): Promise<void> {
      return new Promise((resolve) => {
        if (count < n) { count++; resolve(); }
        else queue.push(resolve);
      });
    },
    release() {
      const next = queue.shift();
      if (next) next(); else count--;
    },
  };
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function run(
  linksPath: string,
  outDir: string,
  concurrency: number,
  maxWaitMs: number
): Promise<void> {
  await mkdir(outDir, { recursive: true });

  const allLinks = JSON.parse(readFileSync(linksPath, "utf-8")) as LinksFile;
  const items: Array<{ month: string; text: string; url: string }> = [];
  for (const [month, links] of Object.entries(allLinks)) {
    for (const l of links) items.push({ month, text: l.text, url: l.url });
  }

  const progressPath = path.join(outDir, ".download-progress.json");
  const progress: Progress = existsSync(progressPath)
    ? JSON.parse(readFileSync(progressPath, "utf-8"))
    : {};

  const pending = items.filter((it) => !(it.url in progress));
  console.log(`Total: ${items.length}  |  Done: ${items.length - pending.length}  |  Pending: ${pending.length}`);
  console.log(`Workers: ${concurrency}  |  Max wait: ${maxWaitMs / 1000}s/page\n`);

  if (pending.length === 0) { console.log("Nothing to do."); return; }

  // Get CDP anchor
  let anchorWs = await getAnchorWs();
  let ownedProcess: Awaited<ReturnType<typeof launchChrome>> | null = null;

  if (!anchorWs) {
    const port = await getFreePort();
    console.log(`Launching Chrome on port ${port}…`);
    ownedProcess = await launchChrome("about:blank", port);
    const wsUrl = await waitForDebugPort(port, 30_000);
    // Get a page anchor
    const res = await fetch(`http://127.0.0.1:${port}/json`);
    const pages = (await res.json()) as Array<{ webSocketDebuggerUrl?: string }>;
    anchorWs = pages.find((p) => p.webSocketDebuggerUrl)?.webSocketDebuggerUrl ?? wsUrl;
  }

  if (!anchorWs) throw new Error("Could not get CDP anchor WebSocket URL");
  console.log(`CDP anchor: ${anchorWs}\n`);

  const sem = makeSemaphore(concurrency);
  const lock = { locked: false };
  const tasks = pending.map((it, idx) =>
    processItem(sem, anchorWs!, outDir, progress, progressPath, lock, items.indexOf(it), items.length, it.month, it.text, it.url, maxWaitMs)
  );
  await Promise.all(tasks);

  const ok    = Object.values(progress).filter((v) => v.status === "ok").length;
  const empty = Object.values(progress).filter((v) => v.status === "empty").length;
  const err   = Object.values(progress).filter((v) => v.status === "error" || v.status === "timeout").length;
  const skip  = Object.values(progress).filter((v) => v.status === "skipped").length;
  console.log(`\n=== Done: ✓${ok} saved  ✗${empty} empty  ✗${err} failed  -${skip} skipped ===`);
  console.log(`Files: ${outDir}`);

  if (ownedProcess) {
    const { killChrome } = await import("./cdp.js");
    killChrome(ownedProcess);
  }
}

// ── CLI ──────────────────────────────────────────────────────────────────────

const argv = process.argv.slice(2);
const linksFile = argv.find((a) => !a.startsWith("-") && a.endsWith(".json"));
const oIdx = argv.indexOf("-o");
const cIdx = argv.indexOf("-c");
const wIdx = argv.indexOf("--max-wait");

if (!linksFile) {
  console.error("Usage: bun download.ts <links.json> [-o output-dir] [-c concurrency] [--max-wait ms]");
  process.exit(1);
}

const outDir     = oIdx >= 0 ? argv[oIdx + 1] : path.join(process.cwd(), "feishu-articles");
const conc       = cIdx >= 0 ? parseInt(argv[cIdx + 1], 10) : 5;
const maxWaitMs  = wIdx >= 0 ? parseInt(argv[wIdx + 1], 10) : 20_000;

run(linksFile, outDir, conc, maxWaitMs).catch((err) => {
  console.error("Error:", err instanceof Error ? err.message : String(err));
  process.exit(1);
});
