// kroki-render.mjs — Render PlantUML (.puml) to SVG/PNG via https://kroki.io
// Usage: node kroki-render.mjs <input.puml> <output.(svg|png)>
import { promises as fs } from "node:fs";
import path from "node:path";
import zlib from "node:zlib";
import https from "node:https";

const [,, inFile, outFile] = process.argv;
if (!inFile || !outFile) {
  console.error("Usage: node kroki-render.mjs <input.puml> <output.(svg|png)>");
  process.exit(1);
}

const fmt = path.extname(outFile).slice(1).toLowerCase();
const src = await fs.readFile(inFile, "utf8");

// Encode for kroki: deflate + base64url
const deflated = zlib.deflateSync(src, { level: 9 });
const b64 = deflated.toString("base64")
  .replace(/\+/g, "-")
  .replace(/\//g, "_")
  .replace(/=+$/, "");

const url = `https://kroki.io/plantuml/${fmt}/${b64}`;
console.log("POST →", url.slice(0, 100) + "...");

await new Promise((resolve, reject) => {
  const req = https.request(url, { method: "GET", headers: { "User-Agent": "cookbookgen" } }, (res) => {
    if (res.statusCode !== 200) {
      let body = "";
      res.on("data", c => body += c);
      res.on("end", () => reject(new Error(`HTTP ${res.statusCode}: ${body.slice(0, 500)}`)));
      return;
    }
    const chunks = [];
    res.on("data", c => chunks.push(c));
    res.on("end", async () => {
      await fs.writeFile(outFile, Buffer.concat(chunks));
      console.log(`Wrote ${outFile} (${chunks.reduce((a,c)=>a+c.length,0)} bytes)`);
      resolve();
    });
  });
  req.on("error", reject);
  req.end();
});
