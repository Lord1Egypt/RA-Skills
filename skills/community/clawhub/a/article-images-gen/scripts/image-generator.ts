import { exec } from "node:child_process";
import { promisify } from "node:util";
import path from "node:path";
import process from "node:process";

const execAsync = promisify(exec);

const DEFAULT_AR = "16:9";
const DEFAULT_OUTPUT_DIR = "/tmp/imageGen/opencli";

/** Map aspect ratio string to opencli --rt format */
function toOpencliRatio(ar: string): string {
  const map: Record<string, string> = {
    "1:1": "1:1",
    "16:9": "16:9",
    "9:16": "9:16",
    "4:3": "4:3",
    "3:4": "3:4",
    "2:3": "2:3",
    "3:2": "3:2",
  };
  return map[ar] || "16:9";
}

/**
 * Generate image via opencli gemini image, falling back to opencli grok image.
 * Returns the path to the saved image file.
 */
export async function generateImage(
  prompt: string,
  options?: {
    aspectRatio?: string | null;
    outputDir?: string;
  }
): Promise<{ imagePath: string }> {
  const ar = toOpencliRatio(options?.aspectRatio || DEFAULT_AR);
  const outDir = options?.outputDir || DEFAULT_OUTPUT_DIR;

  // Style prefix for the prompt
  const stylePrompt = `Hand-drawn minimalist illustration: ${prompt}. Simple, clean, lots of white space, balanced composition, unified color tone, no text, no words, no letters.`;

  // Try Gemini first
  try {
    console.log(`  → Generating with opencli gemini image (ratio: ${ar})...`);
    const result = await runGeminiImage(stylePrompt, ar, outDir);
    if (result) return result;
  } catch (error) {
    console.log(`  ✗ Gemini failed: ${error instanceof Error ? error.message : String(error)}`);
    console.log(`  → Falling back to opencli grok image...`);
  }

  // Fallback to Grok
  const grokResult = await runGrokImage(stylePrompt, outDir);
  if (grokResult) return grokResult;

  throw new Error("Both Gemini and Grok image generation failed");
}

async function runGeminiImage(
  prompt: string,
  ar: string,
  outDir: string
): Promise<{ imagePath: string } | null> {
  const cmd = `opencli gemini image "${escapeShell(prompt)}" --rt ${ar} --op "${escapeShell(outDir)}" -f json --timeout 300`;

  const { stdout } = await execAsync(cmd, { timeout: 310_000 });

  let parsed: any;
  try {
    parsed = JSON.parse(stdout);
  } catch {
    // Try to find JSON in output (opencli may emit logs before JSON)
    const jsonMatch = stdout.match(/\[[\s\S]*\]|\{[\s\S]*\}/);
    if (!jsonMatch) throw new Error(`Gemini: could not parse JSON output: ${stdout.slice(0, 500)}`);
    parsed = JSON.parse(jsonMatch[0]);
  }

  // opencli gemini image output columns: status, file, link
  const items = Array.isArray(parsed) ? parsed : parsed.results || parsed.images || [parsed];
  const success = items.find((item: any) => item.status === "success" || item.file);

  if (!success?.file) {
    throw new Error(`Gemini: no successful image in output. Status: ${JSON.stringify(items.slice(0, 2))}`);
  }

  const imagePath = success.file as string;
  console.log(`  ✓ Gemini image saved: ${imagePath}`);
  return { imagePath };
}

async function runGrokImage(
  prompt: string,
  outDir: string
): Promise<{ imagePath: string }> {
  const cmd = `opencli grok image "${escapeShell(prompt)}" --out "${escapeShell(outDir)}" -f json --timeout 300 --count 1`;

  const { stdout } = await execAsync(cmd, { timeout: 310_000 });

  let parsed: any;
  try {
    parsed = JSON.parse(stdout);
  } catch {
    const jsonMatch = stdout.match(/\[[\s\S]*\]|\{[\s\S]*\}/);
    if (!jsonMatch) throw new Error(`Grok: could not parse JSON output: ${stdout.slice(0, 500)}`);
    parsed = JSON.parse(jsonMatch[0]);
  }

  // opencli grok image output columns: url, width, height, path
  const items = Array.isArray(parsed) ? parsed : parsed.results || parsed.images || [parsed];
  const success = items.find((item: any) => item.path || item.url);

  if (!success) {
    throw new Error(`Grok: no image in output. Got: ${JSON.stringify(items.slice(0, 2))}`);
  }

  const imagePath = (success.path || success.url) as string;
  console.log(`  ✓ Grok image saved: ${imagePath}`);
  return { imagePath };
}

function escapeShell(str: string): string {
  return str.replace(/"/g, '\\"').replace(/\$/g, '\\$').replace(/`/g, '\\`');
}

/** Download image from URL and return local file path */
export async function downloadImage(url: string, outputPath: string): Promise<string> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to download image from ${url}: ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  const { writeFile, mkdir } = await import("node:fs/promises");
  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, buf);
  return outputPath;
}
