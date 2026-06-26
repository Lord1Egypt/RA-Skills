import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { repoRoot } from "./repo-paths.mjs";

const execFileAsync = promisify(execFile);
const BASE_URL = process.env.BOOKMARK_BRIDGE_BASE_URL || "http://127.0.0.1:8787";
const MAX_ROUNDS = Number(process.env.BOOKMARK_BRIDGE_ENSURE_ROUNDS || 3);

async function main() {
  for (let round = 1; round <= MAX_ROUNDS; round += 1) {
    console.log(`[bridge-ensure-live] round ${round}/${MAX_ROUNDS}`);

    await runPreflight();
    const context = await requestContext();
    if (context.ok) {
      console.log(JSON.stringify({
        ok: true,
        bookmarkCount: context.data.bookmarks.length,
        folderCount: context.data.folders.length
      }, null, 2));
      return;
    }

    console.log(`[bridge-ensure-live] context failed after preflight: ${context.error}`);
  }

  console.error("[bridge-ensure-live] bridge/executor is not live after recovery attempts.");
  process.exitCode = 1;
}

async function runPreflight() {
  try {
    const result = await execFileAsync("npm", ["run", "bridge:preflight"], {
      cwd: repoRoot,
      maxBuffer: 1024 * 1024 * 8,
      env: {
        ...process.env,
        NO_PROXY: appendNoProxy(process.env.NO_PROXY || process.env.no_proxy || ""),
        no_proxy: appendNoProxy(process.env.NO_PROXY || process.env.no_proxy || "")
      }
    });

    printCommandOutput(result);
  } catch (error) {
    printCommandOutput(error);
    console.log(`[bridge-ensure-live] preflight failed: ${error.message}`);
  }
}

function printCommandOutput(result) {
  if (result.stdout?.trim()) {
    console.log(result.stdout.trim());
  }
  if (result.stderr?.trim()) {
    console.log(result.stderr.trim());
  }
}

async function requestContext() {
  try {
    const response = await fetch(`${BASE_URL}/context`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        scope: {
          type: "all",
          label: "All bookmarks"
        }
      })
    });
    const data = await response.json();
    if (!response.ok) {
      return {
        ok: false,
        error: data?.error?.message || `HTTP ${response.status}`
      };
    }
    return {
      ok: true,
      data
    };
  } catch (error) {
    return {
      ok: false,
      error: error?.message || String(error)
    };
  }
}

function appendNoProxy(existing) {
  const values = new Set(existing.split(",").map((value) => value.trim()).filter(Boolean));
  values.add("127.0.0.1");
  values.add("localhost");
  return [...values].join(",");
}

main().catch((error) => {
  console.error(`[bridge-ensure-live] ${error.message}`);
  process.exitCode = 1;
});
