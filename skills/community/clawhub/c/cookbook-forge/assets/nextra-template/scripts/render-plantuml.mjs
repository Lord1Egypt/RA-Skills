import { promises as fs } from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";

const srcDir = path.resolve("public/diagrams-src");
const outDir = path.resolve("public/figures");
await fs.mkdir(outDir, { recursive: true });

const files = (await fs.readdir(srcDir)).filter(f => f.endsWith(".puml")).sort();
let ok = 0, fail = 0;

for (const file of files) {
  const figBase = file.replace(/\.puml$/, "");
  const firstLine = (await fs.readFile(path.join(srcDir, file), "utf8")).split(/\r?\n/, 1)[0];
  const m = firstLine.match(/@startuml\s+(\S+)/);
  const alias = m ? m[1] : null;
  try {
    for (const fmt of ["svg", "png"]) {
      const cmd =
        `docker run --rm -v "${srcDir}:/data" -v "${outDir}:/out" ` +
        `plantuml/plantuml:latest -charset UTF-8 -output /out -t${fmt} /data/${file}`;
      execSync(cmd, { stdio: ["ignore", "ignore", "pipe"], windowsHide: true });
    }
    const baseName = alias || figBase;
    if (baseName !== figBase) {
      try { await fs.copyFile(path.join(outDir, baseName + ".svg"), path.join(outDir, figBase + ".svg")); } catch {}
      try { await fs.copyFile(path.join(outDir, baseName + ".png"), path.join(outDir, figBase + ".png")); } catch {}
    }
    ok++;
  } catch (e) {
    console.error(`Failed: ${file}`, e.message);
    fail++;
  }
}
console.log(`PlantUML done. ${ok} ok, ${fail} fail.`);
process.exit(fail === 0 ? 0 : 1);
