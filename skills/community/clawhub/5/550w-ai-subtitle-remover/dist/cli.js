#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const dispatcher_1 = require("./dispatcher");
const i18n_1 = require("./i18n");
const local_media_1 = require("./local-media");
async function readStdin() {
    const chunks = [];
    for await (const chunk of process.stdin)
        chunks.push(Buffer.from(chunk));
    return Buffer.concat(chunks).toString("utf-8");
}
function attachLocalFile(request) {
    const params = { ...(request.params || {}) };
    const filePath = typeof params.filePath === "string" ? params.filePath : null;
    if (!filePath)
        return { ...request, params };
    const kind = request.action === "removeImageWatermark" ? "image" : "video";
    params.file = (0, local_media_1.openSelectedLocalMedia)(filePath, kind);
    delete params.filePath;
    return { ...request, params };
}
async function main() {
    let locale;
    try {
        const input = (await readStdin()).trim();
        if (!input)
            throw new Error((0, i18n_1.localize)(locale, "请通过标准输入提供 JSON 请求", "Provide a JSON request on standard input"));
        const parsed = JSON.parse(input);
        locale = parsed.params?.locale;
        const request = attachLocalFile(parsed);
        const result = await (0, dispatcher_1.invoke)(request);
        process.stdout.write(`${JSON.stringify(result)}\n`);
        if (result.code !== 200)
            process.exitCode = 1;
    }
    catch {
        process.stdout.write(`${JSON.stringify({ code: -200, message: (0, i18n_1.localize)(locale, "请求无效或无法读取本地文件", "The request is invalid or the local file could not be read") })}\n`);
        process.exitCode = 1;
    }
}
void main();
//# sourceMappingURL=cli.js.map