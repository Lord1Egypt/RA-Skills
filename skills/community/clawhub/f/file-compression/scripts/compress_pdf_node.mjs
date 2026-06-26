#!/usr/bin/env node

import path from "node:path";
import process from "node:process";
import { promises as fs } from "node:fs";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

// Hardcoded binary path — not user-controllable
const GS_BIN = "/usr/bin/gs";

const PRESETS = {
  screen: "/screen",
  ebook: "/ebook",
  printer: "/printer",
  prepress: "/prepress",
};

// Validate and resolve a .pdf path; reject null bytes to prevent path traversal
function validatePdfPath(filePath, label) {
  const resolved = path.resolve(filePath);
  if (path.extname(resolved).toLowerCase() !== ".pdf") {
    throw new Error(`${label} must be a .pdf file`);
  }
  if (resolved.includes("\0")) {
    throw new Error(`${label} contains invalid characters`);
  }
  return resolved;
}

function parseArgs(argv) {
  if (argv.length < 2) {
    throw new Error(
      "Usage: compress_pdf_node.mjs <input.pdf> <output.pdf> [--preset screen|ebook|printer|prepress]"
    );
  }
  const args = { input: argv[0], output: argv[1], preset: "ebook" };

  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i];
    const val = argv[i + 1];
    if (key === "--preset" && val) {
      if (!Object.keys(PRESETS).includes(val)) {
        throw new Error(`Invalid preset: ${val}`);
      }
      args.preset = val;
      i += 1;
    } else {
      throw new Error(`Unknown or invalid argument: ${key}`);
    }
  }
  return args;
}

function bytesToHuman(value) {
  const units = ["B", "KB", "MB", "GB"];
  let size = Number(value);
  let unit = units[0];
  for (const next of units) {
    unit = next;
    if (size < 1024 || next === units[units.length - 1]) break;
    size /= 1024;
  }
  return `${size.toFixed(2)} ${unit}`;
}

async function run() {
  const { input, output, preset } = parseArgs(process.argv.slice(2));

  const resolvedInput = validatePdfPath(input, "Input");
  const resolvedOutput = validatePdfPath(output, "Output");

  if (resolvedInput === resolvedOutput) {
    throw new Error("Input and output paths must be different");
  }

  const before = await fs.stat(resolvedInput);
  await fs.mkdir(path.dirname(resolvedOutput), { recursive: true });

  // All args are literals or whitelist-validated values — no user-controlled interpolation
  const gsArgs = [
    "-sDEVICE=pdfwrite",
    "-dCompatibilityLevel=1.6",
    `-dPDFSETTINGS=${PRESETS[preset]}`,
    "-dNOPAUSE",
    "-dBATCH",
    "-dQUIET",
    "-dDetectDuplicateImages=true",
    "-dCompressFonts=true",
    "-dSubsetFonts=true",
    `-sOutputFile=${resolvedOutput}`,
    resolvedInput,
  ];

  // execFile with shell:false — no shell interpolation, binary is a hardcoded constant
  await execFileAsync(GS_BIN, gsArgs, { shell: false });

  const after = await fs.stat(resolvedOutput);
  const saved = before.size - after.size;
  const ratio = before.size === 0 ? 0 : (saved / before.size) * 100;

  console.log("Backend: node-ghostscript");
  console.log(`Output path: ${resolvedOutput}`);
  console.log(`Input size:  ${bytesToHuman(before.size)}`);
  console.log(`Output size: ${bytesToHuman(after.size)}`);
  console.log(`Saved:       ${bytesToHuman(saved)} (${ratio.toFixed(2)}%)`);
  console.log(`From/To:     from ${bytesToHuman(before.size)} to ${bytesToHuman(after.size)}`);
  if (after.size >= before.size) {
    console.error("Warning: output is not smaller than input. Try another preset/backend.");
  }
}

run().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});