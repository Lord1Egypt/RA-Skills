"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.validatePreparedUpload = validatePreparedUpload;
exports.inspectLocalMedia = inspectLocalMedia;
exports.uploadPreparedMedia = uploadPreparedMedia;
const node_fs_1 = __importDefault(require("node:fs"));
const node_path_1 = __importDefault(require("node:path"));
const node_https_1 = __importDefault(require("node:https"));
const form_data_1 = __importDefault(require("form-data"));
const MAX_RESPONSE_BYTES = 2 * 1024 * 1024;
const MAX_SIZES = { image: 50 * 1024 * 1024, video: 1024 * 1024 * 1024 };
const EXTENSIONS = {
    image: new Set([".jpg", ".jpeg", ".png", ".bmp", ".webp", ".avif", ".tif", ".tiff", ".svg"]),
    video: new Set([".mp4", ".mov"]),
};
function validatePreparedUpload(input) {
    if (input.region !== "cn" && input.region !== "global")
        throw new Error("Invalid MCP region");
    if (input.mediaType !== "image" && input.mediaType !== "video")
        throw new Error("Invalid media type");
    if (!node_path_1.default.isAbsolute(input.filePath))
        throw new Error("An absolute local file path is required");
    if (!/^[0-9a-f-]{36}$/.test(input.uploadTicket))
        throw new Error("Invalid upload ticket");
    if (input.mediaType === "image" && !/^[A-Za-z0-9._:-]{8,64}$/.test(input.operationId || ""))
        throw new Error("Image upload requires a stable operationId");
    if (input.operationId && !/^[A-Za-z0-9._:-]{8,64}$/.test(input.operationId))
        throw new Error("Invalid operationId");
    const url = new URL(input.uploadUrl);
    if (url.protocol !== "https:" || url.origin !== "https://www.550wai.cn"
        || url.pathname !== `/mcp-media/${input.region}/${input.mediaType}`
        || url.search || url.hash || url.username || url.password)
        throw new Error("Upload URL is outside the expected 550W endpoint");
    if (input.timeoutMs !== undefined && (!Number.isSafeInteger(input.timeoutMs)
        || input.timeoutMs < 1000 || input.timeoutMs > 30 * 60 * 1000))
        throw new Error("Invalid upload timeout");
    return url;
}
/** Metadata for prepare_media_upload; actual upload re-opens and revalidates the file. */
function inspectLocalMedia(filePath, mediaType) {
    if (mediaType !== "image" && mediaType !== "video")
        throw new Error("Invalid media type");
    if (!node_path_1.default.isAbsolute(filePath))
        throw new Error("An absolute local file path is required");
    if (!EXTENSIONS[mediaType].has(node_path_1.default.extname(filePath).toLowerCase()))
        throw new Error("Unsupported media file extension");
    const fd = node_fs_1.default.openSync(filePath, node_fs_1.default.constants.O_RDONLY | (node_fs_1.default.constants.O_NOFOLLOW || 0));
    try {
        const stat = node_fs_1.default.fstatSync(fd);
        if (!stat.isFile() || stat.size < 1 || stat.size > MAX_SIZES[mediaType])
            throw new Error("Invalid media file size or type");
        return { fileSize: stat.size, fileName: node_path_1.default.basename(filePath) };
    }
    finally {
        node_fs_1.default.closeSync(fd);
    }
}
/** Uploads a user-selected local file using a one-use MCP ticket; never needs an OAuth token. */
async function uploadPreparedMedia(input) {
    if (input.confirmProcessing !== true)
        throw new Error('User approval of media transmission and possible billing is required (confirmProcessing=true)');
    const url = validatePreparedUpload(input);
    const extension = node_path_1.default.extname(input.filePath).toLowerCase();
    if (!EXTENSIONS[input.mediaType].has(extension))
        throw new Error("Unsupported media file extension");
    const flags = node_fs_1.default.constants.O_RDONLY | (node_fs_1.default.constants.O_NOFOLLOW || 0);
    const fd = node_fs_1.default.openSync(input.filePath, flags);
    let stream;
    try {
        const stat = node_fs_1.default.fstatSync(fd);
        if (!stat.isFile() || stat.size < 1 || stat.size > MAX_SIZES[input.mediaType])
            throw new Error("Invalid media file size or type");
        stream = node_fs_1.default.createReadStream(input.filePath, { fd, autoClose: true });
        const form = new form_data_1.default();
        form.append("file", stream, { filename: node_path_1.default.basename(input.filePath), knownLength: stat.size,
            contentType: "application/octet-stream" });
        if (input.mediaType === "image") {
            form.append("operationId", input.operationId);
            form.append("sync", input.sync === true ? "true" : "false");
        }
        return await new Promise((resolve, reject) => {
            const request = node_https_1.default.request(url, { method: "POST", headers: {
                    ...form.getHeaders(), "X-550W-Upload-Ticket": input.uploadTicket,
                } }, response => {
                const chunks = [];
                let size = 0;
                response.on("data", (chunk) => {
                    size += chunk.length;
                    if (size > MAX_RESPONSE_BYTES)
                        request.destroy(new Error("Upload response too large"));
                    else
                        chunks.push(chunk);
                });
                response.on("end", () => {
                    const status = response.statusCode || 0;
                    if (status < 200 || status >= 300)
                        return reject(new Error(`Upload failed (HTTP ${status}); verify the outcome before retrying with the same operation ID`));
                    try {
                        const body = JSON.parse(Buffer.concat(chunks).toString("utf8"));
                        if (!body || typeof body !== "object" || Array.isArray(body))
                            throw new Error("Invalid upload response");
                        resolve(body);
                    }
                    catch {
                        reject(new Error("Invalid upload response"));
                    }
                });
                response.on("error", reject);
            });
            request.setTimeout(input.timeoutMs ?? 10 * 60 * 1000, () => request.destroy(new Error("Upload timed out; verify the outcome before retrying with the same operation ID")));
            request.on("error", reject);
            form.on("error", error => request.destroy(error));
            form.pipe(request);
        });
    }
    finally {
        if (stream)
            stream.destroy();
        else
            node_fs_1.default.closeSync(fd);
    }
}
//# sourceMappingURL=oauth-media-uploader.js.map