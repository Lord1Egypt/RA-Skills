#!/usr/bin/env -S deno run --allow-read --allow-write
/**
 * PPTX generator wrapper.
 *
 * Takes a .tsx slide file path and output .pptx path as arguments.
 * The .tsx file must export a `deck` variable (the JSX Presentation element).
 *
 * Usage:
 *   deno run --allow-read --allow-write generate.ts slides.tsx output.pptx [--json]
 */

import { generate } from "@pixel/pptx";
import { resolve } from "https://deno.land/std@0.224.0/path/mod.ts";

const args = Deno.args;
const jsonMode = args.includes("--json");
const filteredArgs = args.filter((a) => a !== "--json");

if (filteredArgs.length < 2) {
  const msg = "Usage: generate.ts <slides.tsx> <output.pptx> [--json]";
  if (jsonMode) {
    console.log(JSON.stringify({ ok: false, error: msg }));
  } else {
    console.error(msg);
  }
  Deno.exit(1);
}

const [inputFile, outputFile] = filteredArgs;
const inputPath = resolve(inputFile);
const outputPath = resolve(outputFile);

try {
  const mod = await import(`file://${inputPath}`);

  if (!mod.deck) {
    const msg = `Error: ${inputFile} must export a "deck" variable`;
    if (jsonMode) {
      console.log(JSON.stringify({ ok: false, error: msg }));
    } else {
      console.error(msg);
    }
    Deno.exit(1);
  }

  const pptxBytes = generate(mod.deck);
  Deno.writeFileSync(outputPath, pptxBytes);

  if (jsonMode) {
    console.log(JSON.stringify({
      ok: true,
      file: outputPath,
      size: pptxBytes.byteLength,
    }));
  } else {
    console.log(`Saved: ${outputPath}`);
    console.log(`MEDIA: ${outputPath}`);
    console.log(`Size: ${(pptxBytes.byteLength / 1024).toFixed(1)} KB`);
  }
} catch (e) {
  const msg = e instanceof Error ? e.message : String(e);
  if (jsonMode) {
    console.log(JSON.stringify({ ok: false, error: msg }));
  } else {
    console.error(`Error: ${msg}`);
  }
  Deno.exit(1);
}
