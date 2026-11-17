import { createServer } from "node:http";
import { extname, join, normalize } from "node:path";
import { readFile } from "node:fs/promises";

const root = process.cwd();
const port = Number(process.env.PORT || 4177);

const types = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml; charset=utf-8",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png"
};

createServer(async (request, response) => {
  try {
    const url = new URL(request.url || "/", `http://${request.headers.host || "localhost"}`);
    const pathname = normalize(decodeURIComponent(url.pathname === "/" ? "/index.html" : url.pathname)).replace(/^\.\.(\/|$)/, "");
    const filePath = join(root, pathname);
    const body = await readFile(filePath);
    response.writeHead(200, { "Content-Type": types[extname(filePath)] || "text/plain; charset=utf-8" });
    response.end(body);
  } catch {
    response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    response.end("Not found");
  }
}).listen(port, () => {
  console.log(`Yan Zhi Report skill preview: http://localhost:${port}`);
});
