#!/usr/bin/env node
/**
 * doc2markdown
 * Convert multiple file formats to Markdown
 * Default output directory is the same directory as the source file
 */
const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const { URL } = require('url');

const POLL_INTERVAL = 3;   // Polling interval (seconds)
const POLL_TIMEOUT = 60;   // Auto-polling timeout limit (seconds)

class Doc2Markdown {
    constructor() {
        this.BASE_URL = "https://lab.hjcloud.com/llmdoc";
    }

    /**
     * Send HTTP request
     * @param {string} url
     * @param {object} options
     * @returns {Promise<{status: number, data: any}>}
     */
    async request(url, options = {}) {
        return new Promise((resolve, reject) => {
            const urlObj = new URL(url);
            const isHttps = urlObj.protocol === 'https:';
            const httpModule = isHttps ? https : http;

            const reqOptions = {
                hostname: urlObj.hostname,
                port: urlObj.port || (isHttps ? 443 : 80),
                path: urlObj.pathname + urlObj.search,
                method: options.method || 'GET',
                headers: options.headers || {},
                timeout: options.timeout || 30000
            };

            const req = httpModule.request(reqOptions, (res) => {
                const chunks = [];

                res.on('data', (chunk) => {
                    chunks.push(chunk);
                });

                res.on('end', () => {
                    const buffer = Buffer.concat(chunks);
                    let data;

                    if (options.responseType === 'arraybuffer') {
                        data = buffer;
                    } else {
                        const text = buffer.toString('utf8');
                        try {
                            data = JSON.parse(text);
                        } catch (e) {
                            data = text;
                        }
                    }

                    resolve({
                        status: res.statusCode,
                        data: data
                    });
                });
            });

            req.on('error', (error) => {
                reject(error);
            });

            req.on('timeout', () => {
                req.destroy();
                reject(new Error('Request timeout'));
            });

            if (options.body) {
                req.write(options.body);
            }

            req.end();
        });
    }

    /**
     * Generate multipart/form-data format request body
     * @param {string} filePath
     * @param {string} filename
     * @returns {{body: Buffer, boundary: string}}
     */
    createMultipartFormData(filePath, filename) {
        const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);
        const fileContent = fs.readFileSync(filePath);

        const parts = [];

        // Add file field
        parts.push(
            `--${boundary}\r\n` +
            `Content-Disposition: form-data; name="file"; filename="${filename}"\r\n` +
            `Content-Type: application/octet-stream\r\n\r\n`
        );

        parts.push(fileContent);
        parts.push(`\r\n--${boundary}--\r\n`);

        // Merge all parts
        const buffers = parts.map(part =>
            Buffer.isBuffer(part) ? part : Buffer.from(part, 'utf8')
        );

        const body = Buffer.concat(buffers);

        return { body, boundary };
    }

    /**
     * Upload file to docchain service, return document reference ID
     * @param {string} filePath
     * @returns {Promise<string|null>}
     */
    async uploadFile(filePath) {
        if (!fs.existsSync(filePath)) {
            console.log(`Error: File does not exist - ${filePath}`);
            return null;
        }

        try {
            let asciiFilename = path.basename(filePath);
            if (!asciiFilename) {
                asciiFilename = 'document.docx';
            }

            const { body, boundary } = this.createMultipartFormData(filePath, asciiFilename);
            const url = `${this.BASE_URL}/v1/skills/doc2markdown/convert`;

            const response = await this.request(url, {
                method: 'POST',
                headers: {
                    'Content-Type': `multipart/form-data; boundary=${boundary}`,
                    'Content-Length': body.length
                },
                body: body,
                timeout: 30000
            });

            if (response.status === 200) {
                const responseJson = response.data;
                if (!responseJson.success && responseJson.success !== undefined) {
                    console.log(`API request failed: ${responseJson.err}`);
                    return null;
                }
                const docId = responseJson.doc_id;
                if (docId) {
                    return docId;
                } else {
                    console.log(`Upload successful but failed to get document reference ID`);
                    return null;
                }
            } else {
                console.log(`Upload failed, status code: ${response.status}`);
                console.log(`Error message: ${JSON.stringify(response.data)}`);
                return null;
            }

        } catch (error) {
            console.log(`Error occurred during file upload: ${error.message}`);
            return null;
        }
    }

    /**
     * Check document processing status
     * @param {string} docId
     * @returns {Promise<{status: 'done'|'failed'|'converting', error: string}|null>}
     */
    async checkStatus(docId) {
        try {
            const url = `${this.BASE_URL}/v1/skills/doc2markdown/check?doc_id=${encodeURIComponent(docId)}`;

            const response = await this.request(url, {
                method: 'GET',
                timeout: 30000
            });

            if (response.status === 200) {
                const data = response.data;
                if (!data.success && data.success !== undefined) {
                    console.log(`Status check failed: ${data.err}`);
                    return null;
                }
                const statusDetail = data.status_detail || {};
                const convertStatus = (statusDetail.convert_md || {}).state;
                if (convertStatus === '1') {
                    return { status: 'done', error: '' };
                } else if (convertStatus === '3') {
                    return { status: 'failed', error: statusDetail.error || '' };
                }
                return { status: 'converting', error: '' };
            } else {
                console.log(`Status check failed, status code: ${response.status}, error message: ${JSON.stringify(response.data)}`);
                return null;
            }

        } catch (error) {
            console.log(`Error occurred during status check: ${error.message}`);
            return null;
        }
    }

    /**
     * Get converted markdown content (zip package bytes)
     * @param {string} docId
     * @returns {Promise<Buffer|null>}
     */
    async getMarkdown(docId) {
        try {
            const url = `${this.BASE_URL}/v1/skills/doc2markdown/download?doc_id=${encodeURIComponent(docId)}`;

            const response = await this.request(url, {
                method: 'GET',
                timeout: 30000,
                responseType: 'arraybuffer'
            });

            if (response.status === 200) {
                return response.data;
            } else {
                console.log(`Failed to get content, status code: ${response.status}`);
                return null;
            }

        } catch (error) {
            console.log(`Error occurred while getting content: ${error.message}`);
            return null;
        }
    }

    /**
     * Get converted markdown content as single MD file (not zip)
     * @param {string} docId
     * @returns {Promise<Buffer|null>}
     */
    async getMarkdownFile(docId) {
        try {
            const url = `${this.BASE_URL}/v1/skills/doc2markdown/light/download?doc_id=${encodeURIComponent(docId)}`;

            const response = await this.request(url, {
                method: 'GET',
                timeout: 30000,
                responseType: 'arraybuffer'
            });

            if (response.status === 200) {
                return response.data;
            } else {
                console.log(`Failed to get content, status code: ${response.status}`);
                return null;
            }

        } catch (error) {
            console.log(`Error occurred while getting content: ${error.message}`);
            return null;
        }
    }

    /**
     * Save markdown as single file to source file directory (same level as source)
     * @param {Buffer} markdownBytes  Markdown file content
     * @param {string} filePath       Original source file path
     * @returns {Promise<string|null>} Saved markdown file path
     */
    async saveMarkdownFile(markdownBytes, filePath) {
        try {
            const parentDir = path.dirname(path.resolve(filePath));
            const baseName = path.parse(filePath).name;
            const outputFileName = `${baseName}.md`;
            const outPath = path.join(parentDir, outputFileName);

            fs.writeFileSync(outPath, markdownBytes);
            return outPath;

        } catch (error) {
            console.log(`Error occurred while saving file: ${error.message}`);
            return null;
        }
    }

    /**
     * Poll until conversion is complete (up to POLL_TIMEOUT seconds)
     * @param {string} docId
     * @param {string|null} filePath
     * @param {boolean} mdOnly - if true, download as single MD file instead of ZIP
     * @returns {Promise<[boolean, string]|[null, null]>}
     */
    async pollUntilDone(docId, filePath = null, mdOnly = false) {
        let elapsed = 0;
        while (elapsed < POLL_TIMEOUT) {
            const result = await this.checkStatus(docId);
            if (result === null) {
                console.log("Error: Unable to get document status, please try again later");
                process.exit(1);
            }
            if (result.status === 'done') {
                console.log(`  Conversion complete, downloading...`);
                if (mdOnly) {
                    const markdownBytes = await this.getMarkdownFile(docId);
                    if (!markdownBytes) {
                        return [false, "Failed to get markdown content"];
                    }
                    const hint = filePath || `${docId}.md`;
                    const outFilePath = await this.saveMarkdownFile(markdownBytes, hint);
                    if (!outFilePath) {
                        return [false, "Failed to save file"];
                    }
                    return [true, outFilePath];
                } else {
                    const zipBytes = await this.getMarkdown(docId);
                    if (!zipBytes) {
                        return [false, "Failed to get markdown content"];
                    }
                    const hint = filePath || `doc_${docId}.md`;
                    const outDir = await this.saveMarkdown(zipBytes, docId, hint);
                    if (!outDir) {
                        return [false, "Failed to save file"];
                    }
                    return [true, outDir];
                }
            } else if (result.status === 'failed') {
                const reason = result.error ? `: ${result.error}` : '';
                return [false, `Document conversion failed${reason}`];
            } else {
                console.log(`  Converting... waited ${elapsed}s.`);
                await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL * 1000));
                elapsed += POLL_INTERVAL;
            }
        }

        return [null, null];
    }

    /**
     * Upload file and auto-poll for conversion, return doc_id if timeout
     * @param {string} filePath
     * @param {boolean} mdOnly - if true, download as single MD file instead of ZIP
     */
    async convertFile(filePath, mdOnly = false) {
        // 1. Upload file
        console.log(`[1/3] Uploading file: ${filePath}`);
        const docId = await this.uploadFile(filePath);
        if (!docId) {
            console.log(`File upload failed!`);
            process.exit(1);
        }
        console.log(`  Upload successful, document ID: ${docId}`);

        // 2. Poll and wait (up to 60 seconds)
        console.log(`[2/3] Waiting for conversion (auto-checking)...`);
        const [result, detail] = await this.pollUntilDone(docId, filePath, mdOnly);

        if (result === true) {
            console.log(`[3/3] Download complete, file saved: ${detail}`);
        } else if (result === false) {
            console.log(`Error: ${detail}`);
            process.exit(1);
        } else {
            console.log(`  Document ID: ${docId}`);
            console.log(`[!] Document still converting (exceeded ${POLL_TIMEOUT}s)`);
            if (mdOnly) {
                console.log(`[!] When conversion completes, use: node scripts/doc2markdown.js check ${docId} "${filePath}" --md`);
            } else {
                console.log(`[!] Large documents typically require more time. During peak hours, conversions may be queued. Please be patient`);
                console.log(`[!] Do you need to continue checking conversion status and downloading`);
            }
            process.exit(2);
        }
    }

    /**
     * Extract zip to source file directory, returns output directory path
     * @param {Buffer} zipBytes
     * @param {string} docId
     * @param {string} filePath
     * @returns {Promise<string|null>}
     */
    async saveMarkdown(zipBytes, docId, filePath) {
        try {
            const parentDir = path.dirname(path.resolve(filePath));
            const [fileId] = docId.split('-');
            const markdownDirName = `${fileId}_` + path.parse(filePath).name;
            const outDir = path.join(parentDir, markdownDirName);

            if (!fs.existsSync(outDir)) {
                fs.mkdirSync(outDir, { recursive: true });
            }

            const zlib = require('zlib');
            const { pipeline } = require('stream/promises');

            // Save zip temporarily
            const tempZip = path.join(outDir, `temp_${Date.now()}.zip`);
            fs.writeFileSync(tempZip, zipBytes);

            // Parse ZIP central directory natively
            const buffer = fs.readFileSync(tempZip);
            let pos = buffer.length - 22;
            while (pos > 0) {
                if (
                    buffer.readUInt32LE(pos) === 0x06054b50 &&
                    pos + 22 <= buffer.length
                )
                    break;
                pos--;
            }

            const entries = [];
            const diskEntries = buffer.readUInt16LE(pos + 8);
            const dirStart = buffer.readUInt32LE(pos + 16);
            pos = dirStart;

            for (let i = 0; i < diskEntries; i++) {
                if (buffer.readUInt32LE(pos) !== 0x02014b50) break;
                const flags = buffer.readUInt16LE(pos + 8);
                const method = buffer.readUInt16LE(pos + 10);
                const nameLen = buffer.readUInt16LE(pos + 28);
                const extraLen = buffer.readUInt16LE(pos + 30);
                const commentLen = buffer.readUInt16LE(pos + 32);
                const offset = buffer.readUInt32LE(pos + 42);
                const name = buffer.toString('utf8', pos + 46, pos + 46 + nameLen);
                entries.push({ offset, method, name, encrypted: !!(flags & 1) });
                pos += 46 + nameLen + extraLen + commentLen;
            }

            // Extract each file
            for (const ent of entries) {
                if (ent.encrypted || ent.name.endsWith('/')) continue;
                const o = ent.offset;
                const sig = buffer.readUInt32LE(o);
                if (sig !== 0x04034b50) continue;
                const nameLen = buffer.readUInt16LE(o + 26);
                const extraLen = buffer.readUInt16LE(o + 28);
                const csize = buffer.readUInt32LE(o + 18);
                const usize = buffer.readUInt32LE(o + 14);
                const dataStart = o + 30 + nameLen + extraLen;
                const data = buffer.slice(dataStart, dataStart + csize);

                const outPath = path.join(outDir, ent.name.replace(/\\/g, '/'));
                const safeOutDir = path.resolve(outDir) + path.sep;
                if (!path.resolve(outPath).startsWith(safeOutDir)) {
                    throw new Error(`Unsafe ZIP entry path (path traversal): ${ent.name}`);
                }
                const outDirPath = path.dirname(outPath);
                if (!fs.existsSync(outDirPath)) fs.mkdirSync(outDirPath, { recursive: true });

                if (ent.method === 0) {
                    fs.writeFileSync(outPath, data);
                } else if (ent.method === 8) {
                    const decompressed = zlib.inflateSync(data, { chunkSize: usize });
                    fs.writeFileSync(outPath, decompressed);
                }
            }

            fs.unlinkSync(tempZip);
            return outDir;

        } catch (error) {
            console.log(`Error occurred while saving file: ${error.message}`);
            return null;
        }
    }

    /**
     * Check status and download via doc_id
     * @param {string} docId
     * @param {string} filePath
     * @param {boolean} mdOnly - if true, download as single MD file instead of ZIP
     */
    async checkAndDownload(docId, filePath, mdOnly = false) {
        console.log(`[1/2] Checking conversion status for document ${docId}...`);
        const result = await this.checkStatus(docId);
        if (result === null) {
            console.log("Error: Unable to get document status, please retry later");
            process.exit(1);
        }

        if (result.status === 'failed') {
            const reason = result.error ? `: ${result.error}` : '';
            console.log(`Error: Document conversion failed${reason}`);
            process.exit(1);
        } else if (result.status === 'done') {
            console.log(`  Conversion completed, downloading...`);
            if (mdOnly) {
                const markdownBytes = await this.getMarkdownFile(docId);
                if (!markdownBytes) {
                    console.log("Failed to get markdown content");
                    process.exit(1);
                }
                const outFilePath = await this.saveMarkdownFile(markdownBytes, filePath);
                if (!outFilePath) {
                    process.exit(1);
                }
                console.log(`[2/2] Download complete, file saved: ${outFilePath}`);
            } else {
                const zipBytes = await this.getMarkdown(docId);
                if (!zipBytes) {
                    console.log("Failed to get markdown content");
                    process.exit(1);
                }
                const outDir = await this.saveMarkdown(zipBytes, docId, filePath);
                if (!outDir) {
                    process.exit(1);
                }
                console.log(`[2/2] Download complete, file saved: ${outDir}`);
            }
        } else {
            console.log("  Document still converting, waiting...");
            const [result, detail] = await this.pollUntilDone(docId, filePath, mdOnly);
            if (result === true) {
                console.log(`[2/2] Download complete, file saved: ${detail}`);
            } else if (result === false) {
                console.log(`Error: ${detail}`);
                process.exit(1);
            } else {
                console.log(`[!] Document still converting, please retry later`);
                console.log(`  Document ID: ${docId}`);
                process.exit(2);
            }
        }
    }

}

const USAGE = `Usage:
  node doc2markdown.js convert <file_path> [--md]        Upload and convert document (default: download ZIP package)
  node doc2markdown.js check  <doc_id> <file_path> [--md] Check status and download
                                                          --md: Download as single MD file instead of ZIP package

Examples:
  node doc2markdown.js convert report.pdf
  node doc2markdown.js convert report.pdf --md
  node doc2markdown.js check 123-f3ce07 report.pdf
  node doc2markdown.js check 123-f3ce07 report.pdf --md`;


async function main() {
    if (process.argv.length < 3) {
        console.log(USAGE);
        process.exit(1);
    }

    const converter = new Doc2Markdown();
    const cmd = process.argv[2];

    // Parse --md flag
    const mdOnly = process.argv.includes('--md');

    if (cmd === "convert") {
        if (process.argv.length < 4 || process.argv.length > 5) {
            console.log("Usage: node doc2markdown.js convert <file_path> [--md]");
            process.exit(1);
        }
        await converter.convertFile(process.argv[3], mdOnly);

    } else if (cmd === "check") {
        if (process.argv.length < 5 || process.argv.length > 6) {
            console.log("Usage: node doc2markdown.js check <doc_id> <file_path> [--md]");
            process.exit(1);
        }
        const docId = process.argv[3];
        const filePath = process.argv[4];
        await converter.checkAndDownload(docId, filePath, mdOnly);

    } else {
        // Backward compatibility: treat direct file path as convert
        if (fs.existsSync(cmd) && fs.statSync(cmd).isFile()) {
            await converter.convertFile(cmd, mdOnly);
        } else {
            console.log(`Unknown command: ${cmd}`);
            console.log(USAGE);
            process.exit(1);
        }
    }
}

if (require.main === module) {
    main().catch(error => {
        console.error(`Program execution error: ${error.message}`);
        process.exit(1);
    });
}

module.exports = Doc2Markdown;