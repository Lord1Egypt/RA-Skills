const fs = require('fs');
const os = require('os');
const path = require('path');

function parseOpenClawConfig(configPath) {
    const raw = fs.readFileSync(configPath, 'utf8');

    try {
        return JSON.parse(raw);
    } catch (jsonErr) {
        let json5;
        try {
            json5 = require('json5');
        } catch (requireErr) {
            throw new Error(
                `Failed to parse ${configPath} as JSON. The file may be JSON5, but dependency "json5" is not installed.`
            );
        }

        try {
            return json5.parse(raw);
        } catch (json5Err) {
            throw new Error(`Failed to parse ${configPath} as JSON/JSON5: ${json5Err.message}`);
        }
    }
}

function loadCredentials() {
    // Intentional credential loading — reads only the two named Feishu app vars,
    // not a full environment dump. Falls back to openclaw.json if env vars absent.
    const envAppId = process.env.FEISHU_APP_ID;
    const envAppSecret = process.env.FEISHU_APP_SECRET;

    if (envAppId && envAppSecret) {
        return { appId: envAppId, appSecret: envAppSecret, source: 'env' };
    }

    const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
    let config;

    try {
        config = parseOpenClawConfig(configPath);
    } catch (err) {
        if (envAppId || envAppSecret) {
            throw new Error(
                `Incomplete Feishu env credentials (need both FEISHU_APP_ID and FEISHU_APP_SECRET), and failed to load fallback from ${configPath}: ${err.message}`
            );
        }
        throw new Error(`Failed to load Feishu credentials from ${configPath}: ${err.message}`);
    }

    const cfgAppId = config?.channels?.feishu?.appId;
    const cfgAppSecret = config?.channels?.feishu?.appSecret;

    const appId = envAppId || cfgAppId;
    const appSecret = envAppSecret || cfgAppSecret;

    if (!appId || !appSecret) {
        throw new Error(
            'Missing Feishu credentials. Provide FEISHU_APP_ID and FEISHU_APP_SECRET, or set channels.feishu.appId/appSecret in ~/.openclaw/openclaw.json'
        );
    }

    return {
        appId,
        appSecret,
        source: envAppId && envAppSecret ? 'env' : 'openclaw.json',
    };
}

function toErrorPayload(error, code, msg) {
    return {
        error,
        code,
        msg,
    };
}

function contentTypeToExt(contentType) {
    const ct = (contentType || '').toLowerCase();
    if (ct.includes('image/svg+xml')) return '.svg';
    if (ct.includes('image/png')) return '.png';
    if (ct.includes('image/jpeg') || ct.includes('image/jpg')) return '.jpg';
    if (ct.includes('image/gif')) return '.gif';
    return '.bin';
}

function normalizeOutputPath(outPath, ext) {
    if (!outPath) return null;
    const parsed = path.parse(outPath);
    if (parsed.ext.toLowerCase() === ext) return outPath;
    return path.join(parsed.dir, `${parsed.name}${ext}`);
}

async function getTenantAccessToken(appId, appSecret) {
    const res = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({ app_id: appId, app_secret: appSecret }),
    });

    let data;
    try {
        data = await res.json();
    } catch (e) {
        throw new Error('Failed to parse tenant_access_token response as JSON');
    }

    if (!res.ok || data.code !== 0 || !data.tenant_access_token) {
        const code = typeof data?.code === 'number' ? data.code : res.status;
        const msg = data?.msg || `HTTP ${res.status}`;
        const err = new Error(`Failed to get tenant_access_token: ${msg}`);
        err.code = code;
        err.apiMsg = msg;
        throw err;
    }

    return data.tenant_access_token;
}

async function main() {
    const args = process.argv.slice(2);
    const whiteboardId = args[0];
    const outPathArg = args[1];

    if (!whiteboardId) {
        console.error(JSON.stringify(toErrorPayload('Usage', 400, 'Usage: node export_board_svg.js <whiteboard_id> <out_path_optional>')));
        process.exit(1);
    }

    let credentials;
    try {
        credentials = loadCredentials();
    } catch (err) {
        console.error(JSON.stringify(toErrorPayload('CredentialsError', 400, err.message)));
        process.exit(1);
    }

    try {
        const tenantAccessToken = await getTenantAccessToken(credentials.appId, credentials.appSecret);

        const url = `https://open.feishu.cn/open-apis/board/v1/whiteboards/${encodeURIComponent(whiteboardId)}/download_as_image`;

        const doDownload = (accept) =>
            fetch(url, {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${tenantAccessToken}`,
                    Accept: accept,
                },
            });

        // 先强制请求 SVG；若不支持再回退到图片格式协商。
        let res = await doDownload('image/svg+xml');
        let contentType = res.headers.get('content-type') || '';

        if (res.ok && !contentType.toLowerCase().includes('image/svg+xml')) {
            res = await doDownload('image/svg+xml,image/png;q=0.8,image/jpeg;q=0.6');
            contentType = res.headers.get('content-type') || '';
        }

        if (!res.ok) {
            let remoteMsg = '';
            try {
                const maybeJson = await res.json();
                remoteMsg = maybeJson?.msg || '';
            } catch (_) {
                try {
                    remoteMsg = (await res.text()).slice(0, 200);
                } catch (__) {
                    remoteMsg = '';
                }
            }

            if (res.status === 403 || res.status === 404) {
                console.error(
                    JSON.stringify(
                        toErrorPayload(
                            'AccessDenied',
                            res.status,
                            `${remoteMsg || 'Access denied or whiteboard not found.'} 请确认白板已分享给 bot/app 且应用具备白板访问权限。`
                        )
                    )
                );
                process.exit(1);
            }

            console.error(
                JSON.stringify(
                    toErrorPayload(
                        'ApiError',
                        res.status,
                        remoteMsg || `Failed to export whiteboard image: HTTP ${res.status}`
                    )
                )
            );
            process.exit(1);
        }

        const ext = contentTypeToExt(contentType);
        const bodyArrayBuffer = await res.arrayBuffer();
        const bodyBuffer = Buffer.from(bodyArrayBuffer);

        const finalOutputPath = normalizeOutputPath(outPathArg, ext);

        if (finalOutputPath) {
            fs.mkdirSync(path.dirname(finalOutputPath), { recursive: true });
            fs.writeFileSync(finalOutputPath, bodyBuffer);
            process.stdout.write(
                `${JSON.stringify({
                    whiteboard_id: whiteboardId,
                    content_type: contentType,
                    output: finalOutputPath,
                    bytes: bodyBuffer.length,
                })}\n`
            );
            return;
        }

        if (ext === '.svg') {
            process.stdout.write(bodyBuffer.toString('utf8'));
        } else {
            process.stdout.write(bodyBuffer);
        }
    } catch (err) {
        const code = typeof err?.code === 'number' ? err.code : 500;
        const msg = err?.message || 'Unknown error';
        console.error(JSON.stringify(toErrorPayload('ExportFailed', code, msg)));
        process.exit(1);
    }
}

main();
