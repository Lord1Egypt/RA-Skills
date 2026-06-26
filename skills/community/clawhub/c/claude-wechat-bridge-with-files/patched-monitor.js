import path from "node:path";
import { getUpdates } from "./weixin/api.js";
import { SESSION_EXPIRED_ERRCODE, pauseSession, getRemainingPauseMs } from "./weixin/session-guard.js";
import { bodyFromItemList, setContextToken } from "./weixin/inbound.js";
import { loadSyncBuf, saveSyncBuf } from "./weixin/auth.js";
import { logger } from "./logger.js";
import { MessageType, MessageItemType } from "./weixin/types.js";
import { downloadMediaFromItem } from "./weixin/media/media-download.js";
const DEFAULT_LONG_POLL_TIMEOUT_MS = 35_000;
const MAX_CONSECUTIVE_FAILURES = 3;
const BACKOFF_DELAY_MS = 30_000;
const RETRY_DELAY_MS = 2_000;
export async function startMonitor(opts) {
    const { config, token, accountId, mcp, abortSignal } = opts;
    const baseUrl = config.weixinBaseUrl;
    const cdnBaseUrl = config.weixinCdnBaseUrl;
    const mediaTmpDir = path.join(config.dataDir, "media");
    logger.info(`monitor started: baseUrl=${baseUrl} accountId=${accountId} (media patch active, tmpDir=${mediaTmpDir})`);
    let getUpdatesBuf = loadSyncBuf();
    if (getUpdatesBuf) {
        logger.info(`resuming from previous sync buf (${getUpdatesBuf.length} bytes)`);
    }
    else {
        logger.info(`no previous sync buf, starting fresh`);
    }
    let nextTimeoutMs = DEFAULT_LONG_POLL_TIMEOUT_MS;
    let consecutiveFailures = 0;
    while (!abortSignal?.aborted) {
        try {
            const resp = await getUpdates({
                baseUrl,
                token,
                get_updates_buf: getUpdatesBuf,
                timeoutMs: nextTimeoutMs,
            });
            if (resp.longpolling_timeout_ms != null && resp.longpolling_timeout_ms > 0) {
                nextTimeoutMs = resp.longpolling_timeout_ms;
            }
            const isApiError = (resp.ret !== undefined && resp.ret !== 0) ||
                (resp.errcode !== undefined && resp.errcode !== 0);
            if (isApiError) {
                const isSessionExpired = resp.errcode === SESSION_EXPIRED_ERRCODE || resp.ret === SESSION_EXPIRED_ERRCODE;
                if (isSessionExpired) {
                    pauseSession(accountId);
                    const pauseMs = getRemainingPauseMs(accountId);
                    logger.error(`getUpdates: session expired (errcode=${resp.errcode}), pausing for ${Math.ceil(pauseMs / 60_000)} min`);
                    consecutiveFailures = 0;
                    await sleep(pauseMs, abortSignal);
                    continue;
                }
                consecutiveFailures += 1;
                logger.error(`getUpdates failed: ret=${resp.ret} errcode=${resp.errcode} errmsg=${resp.errmsg ?? ""} (${consecutiveFailures}/${MAX_CONSECUTIVE_FAILURES})`);
                if (consecutiveFailures >= MAX_CONSECUTIVE_FAILURES) {
                    logger.error(`${MAX_CONSECUTIVE_FAILURES} consecutive failures, backing off 30s`);
                    consecutiveFailures = 0;
                    await sleep(BACKOFF_DELAY_MS, abortSignal);
                }
                else {
                    await sleep(RETRY_DELAY_MS, abortSignal);
                }
                continue;
            }
            consecutiveFailures = 0;
            if (resp.get_updates_buf != null && resp.get_updates_buf !== "") {
                saveSyncBuf(resp.get_updates_buf);
                getUpdatesBuf = resp.get_updates_buf;
            }
            const msgs = resp.msgs ?? [];
            for (const msg of msgs) {
                // Skip bot's own messages
                if (msg.message_type === MessageType.BOT)
                    continue;
                const fromUserId = msg.from_user_id ?? "";
                if (!fromUserId)
                    continue;
                // Cache context token
                if (msg.context_token) {
                    setContextToken(fromUserId, msg.context_token);
                }
                // Extract text (voice with transcript counts as text)
                let text = bodyFromItemList(msg.item_list);
                // [media patch] Download attached image/file/video/voice and append path markers.
                // Skip voice if bodyFromItemList already extracted a transcript.
                const itemList = msg.item_list ?? [];
                const hasVoiceTranscript = itemList.some(it => it.type === MessageItemType.VOICE && it.voice_item?.text);
                const markers = [];
                for (const item of itemList) {
                    const t = item.type;
                    if (t !== MessageItemType.IMAGE && t !== MessageItemType.FILE && t !== MessageItemType.VIDEO && t !== MessageItemType.VOICE) {
                        continue;
                    }
                    if (t === MessageItemType.VOICE && hasVoiceTranscript) {
                        continue;
                    }
                    try {
                        const r = await downloadMediaFromItem(item, {
                            cdnBaseUrl,
                            tmpDir: mediaTmpDir,
                            label: `inbound-${fromUserId}`,
                        });
                        if (r.decryptedPicPath) markers.push(`[图片: ${r.decryptedPicPath}]`);
                        if (r.decryptedFilePath) markers.push(`[文件: ${r.decryptedFilePath}]`);
                        if (r.decryptedVoicePath) markers.push(`[语音文件: ${r.decryptedVoicePath}]`);
                        if (r.decryptedVideoPath) markers.push(`[视频: ${r.decryptedVideoPath}]`);
                    }
                    catch (err) {
                        logger.error(`media download failed for ${fromUserId}: ${String(err)}`);
                    }
                }
                if (markers.length > 0) {
                    text = text ? `${text}\n${markers.join("\n")}` : markers.join("\n");
                }
                if (!text) {
                    logger.debug(`skipping empty message from ${fromUserId}`);
                    continue;
                }
                logger.info(`inbound: from=${fromUserId} text="${text.substring(0, 100)}"`);
                // Push notification to Claude Code via MCP channel
                try {
                    await mcp.notification({
                        method: "notifications/claude/channel",
                        params: {
                            content: text,
                            meta: { sender: fromUserId, user_id: fromUserId },
                        },
                    });
                    logger.info(`notification pushed for ${fromUserId}`);
                }
                catch (err) {
                    logger.error(`failed to push notification for ${fromUserId}: ${String(err)}`);
                }
            }
        }
        catch (err) {
            if (abortSignal?.aborted) {
                logger.info("monitor stopped (aborted)");
                return;
            }
            consecutiveFailures += 1;
            logger.error(`getUpdates error (${consecutiveFailures}/${MAX_CONSECUTIVE_FAILURES}): ${String(err)}`);
            if (consecutiveFailures >= MAX_CONSECUTIVE_FAILURES) {
                logger.error(`${MAX_CONSECUTIVE_FAILURES} consecutive failures, backing off 30s`);
                consecutiveFailures = 0;
                await sleep(BACKOFF_DELAY_MS, abortSignal);
            }
            else {
                await sleep(RETRY_DELAY_MS, abortSignal);
            }
        }
    }
    logger.info("monitor ended");
}
function sleep(ms, signal) {
    return new Promise((resolve, reject) => {
        const t = setTimeout(resolve, ms);
        signal?.addEventListener("abort", () => {
            clearTimeout(t);
            reject(new Error("aborted"));
        }, { once: true });
    });
}
