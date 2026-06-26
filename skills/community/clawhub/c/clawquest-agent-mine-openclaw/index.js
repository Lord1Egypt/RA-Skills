import express from "express";
import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import path from "node:path";
import { z } from "zod";
import { GameApiHttpError, fetchGameApiWithApiCodePost, runManagedMiningLoop, setApiAutoMining, } from "./tools.js";
const app = express();
app.use(express.json());
const requestSchema = z.object({
    apiCode: z.string().trim().min(1).optional(),
    cacheKey: z.string().trim().min(1).optional(),
    lang: z
        .enum(["zh_CN", "zh_TW", "en_US", "ja_JP", "ko_KR", "ru_RU"])
        .optional(),
    pollingIntervalMilliseconds: z.number().int().positive().optional(),
    roundIntervalMilliseconds: z.number().int().positive().optional(),
    maxConsecutiveErrorCount: z.number().int().positive().optional(),
    sinceEventId: z.number().int().nonnegative().optional(),
    openclawSessionKey: z.string().trim().min(1).optional(),
    sessionKey: z.string().trim().min(1).optional(),
    forceRestart: z.boolean().optional(),
    autoBuyStamina: z.boolean().optional(),
    autoBuyStaminaMaxFailures: z.number().int().positive().optional(),
});
const apiCodeCache = new Map();
const defaultCacheKey = "default";
const apiCodeStorePath = process.env.API_CODE_STORE_PATH ??
    path.join(process.cwd(), "data", "api-code-store.json");
const defaultManagedMaxConsecutiveErrorCount = Number(process.env.MANAGED_MINING_MAX_CONSECUTIVE_ERROR_COUNT ?? "10");
const maxMiningSessionEventCount = Number(process.env.MINING_SESSION_MAX_EVENTS ?? "200");
const defaultAutoBuyStaminaEnabledFromEnv = process.env.MANAGED_MINING_AUTO_BUY_STAMINA === "1" ||
    process.env.MANAGED_MINING_AUTO_BUY_STAMINA === "true";
let managedMiningTask;
let managedMiningStatus = buildIdleManagedMiningStatus();
let miningSessionEventIdCounter = 0;
let managedMiningTaskGeneration = 0;
app.post("/tool/:name", async (req, res) => {
    const parsed = requestSchema.safeParse(req.body ?? {});
    if (!parsed.success) {
        return res.status(400).json({ ok: false, error: "invalid_payload" });
    }
    const toolName = req.params.name;
    const payload = parsed.data;
    const cacheKey = payload.cacheKey ?? defaultCacheKey;
    try {
        if (toolName === "set_api_code") {
            if (!payload.apiCode) {
                return res.status(400).json({ ok: false, error: "api_code_required" });
            }
            apiCodeCache.set(cacheKey, payload.apiCode);
            await persistApiCodeStore();
            return res.json({ ok: true, data: { cacheKey, hasApiCode: true } });
        }
        if (toolName === "get_api_code") {
            const cachedApiCode = apiCodeCache.get(cacheKey);
            if (!cachedApiCode) {
                return res.status(404).json({ ok: false, error: "api_code_not_found" });
            }
            return res.json({ ok: true, data: { cacheKey, apiCode: cachedApiCode } });
        }
        if (toolName === "clear_api_code") {
            const deleted = apiCodeCache.delete(cacheKey);
            if (deleted) {
                await persistApiCodeStore();
            }
            return res.json({ ok: true, data: { cacheKey, deleted } });
        }
        if (toolName === "check_mining_state") {
            if (payload.apiCode) {
                await upsertApiCode(cacheKey, payload.apiCode);
            }
            const apiCode = resolveApiCodeOrBadRequest(res, payload, cacheKey);
            if (apiCode === undefined) {
                return;
            }
            const upstream = await fetchGameApiWithApiCodePost("/api/checkMiningState", apiCode, {});
            return res.status(upstream.httpStatus).json(upstream.body);
        }
        if (toolName === "buy_stamina") {
            if (payload.apiCode) {
                await upsertApiCode(cacheKey, payload.apiCode);
            }
            const apiCode = resolveApiCodeOrBadRequest(res, payload, cacheKey);
            if (apiCode === undefined) {
                return;
            }
            const upstream = await fetchGameApiWithApiCodePost("/api/buyStamina", apiCode, {});
            return res.status(upstream.httpStatus).json(upstream.body);
        }
        if (toolName === "get_stamina") {
            if (payload.apiCode) {
                await upsertApiCode(cacheKey, payload.apiCode);
            }
            const apiCode = resolveApiCodeOrBadRequest(res, payload, cacheKey);
            if (apiCode === undefined) {
                return;
            }
            const upstream = await fetchGameApiWithApiCodePost("/api/getStamina", apiCode, {});
            return res.status(upstream.httpStatus).json(upstream.body);
        }
        if (toolName === "start_auto_mining") {
            return res.status(410).json({
                ok: false,
                error: "tool_deprecated_use_start_managed_mining_loop",
                message: "start_auto_mining is deprecated. Use start_managed_mining_loop.",
            });
        }
        if (toolName === "start_managed_mining_loop" ||
            toolName === "start_mining_session") {
            if (payload.apiCode) {
                await upsertApiCode(cacheKey, payload.apiCode);
            }
            const apiCode = resolveApiCode(payload, cacheKey);
            if (managedMiningTask) {
                if (payload.forceRestart) {
                    managedMiningTask.stopRequested = true;
                    managedMiningTask = undefined;
                    managedMiningTaskGeneration += 1;
                    managedMiningStatus = buildIdleManagedMiningStatus();
                }
                else {
                    return res.status(409).json({
                        ok: false,
                        error: "managed_mining_loop_already_running",
                        message: "Managed mining loop is already running. Call stop_managed_mining_loop first or use forceRestart: true.",
                        data: managedMiningStatus,
                    });
                }
            }
            const maxConsecutiveErrorCount = normalizePositiveInteger(payload.maxConsecutiveErrorCount, defaultManagedMaxConsecutiveErrorCount);
            const openclawSessionKey = extractOpenClawSessionKey(req, payload);
            miningSessionEventIdCounter = 0;
            const loopGeneration = managedMiningTaskGeneration;
            managedMiningTask = {
                stopRequested: false,
                apiCode,
                cacheKey,
            };
            managedMiningStatus = {
                running: true,
                phase: "starting_round",
                message: "Managed mining loop started. Starting current round.",
                openclawSessionKey,
                startedAt: Date.now(),
                updatedAt: Date.now(),
                cacheKey,
                roundsCompleted: 0,
                consecutiveErrorCount: 0,
                maxConsecutiveErrorCount,
                lastRewardDetails: [],
                events: [],
                lastEventId: 0,
            };
            appendMiningSessionEvent("session_started", {
                openclawSessionKey: openclawSessionKey ?? null,
                cacheKey,
            });
            try {
                await setApiAutoMining(apiCode, true);
            }
            catch (error) {
                console.warn("[skill-openclaw] setApiAutoMining(true) failed:", error);
            }
            void runManagedMiningLoop(apiCode, () => managedMiningTaskGeneration === loopGeneration &&
                managedMiningTask !== undefined &&
                !managedMiningTask.stopRequested, {
                onPhaseChanged: (phase, details) => {
                    if (managedMiningTaskGeneration !== loopGeneration)
                        return;
                    managedMiningStatus.phase = phase;
                    managedMiningStatus.updatedAt = Date.now();
                    managedMiningStatus.message = mapManagedMiningPhaseToMessage(phase);
                    if (phase !== "waiting_estimated_end_at") {
                        managedMiningStatus.estimatedEndAt = undefined;
                    }
                    if (phase === "waiting_estimated_end_at" &&
                        details?.estimatedEndAt) {
                        managedMiningStatus.estimatedEndAt = Number(details.estimatedEndAt);
                    }
                    if (phase === "starting_round") {
                        managedMiningStatus.consecutiveErrorCount = 0;
                        managedMiningStatus.lastError = undefined;
                    }
                },
                onError: (errorMessage, consecutiveErrorCount) => {
                    if (managedMiningTaskGeneration !== loopGeneration)
                        return;
                    managedMiningStatus.updatedAt = Date.now();
                    managedMiningStatus.lastError = errorMessage;
                    managedMiningStatus.consecutiveErrorCount = consecutiveErrorCount;
                    managedMiningStatus.message =
                        "Loop execution error recorded. Continuing according to retry policy.";
                    appendMiningSessionEvent("error", {
                        message: errorMessage,
                        consecutiveErrorCount,
                    });
                },
                onRoundCompleted: (roundResult) => {
                    if (managedMiningTaskGeneration !== loopGeneration)
                        return;
                    managedMiningStatus.updatedAt = Date.now();
                    managedMiningStatus.roundsCompleted += 1;
                    managedMiningStatus.lastRewardDetails = roundResult.rewardDetails;
                    managedMiningStatus.lastCheckState = roundResult.checkState;
                    managedMiningStatus.lastPlayerStatus = extractPlayerStatus(roundResult.checkState);
                    appendMiningSessionEvent("round_completed", {
                        roundsCompleted: managedMiningStatus.roundsCompleted,
                        rewardDetails: roundResult.rewardDetails,
                        playerStatus: managedMiningStatus.lastPlayerStatus,
                    });
                },
            }, {
                lang: payload.lang,
                pollingIntervalMilliseconds: payload.pollingIntervalMilliseconds,
                roundIntervalMilliseconds: payload.roundIntervalMilliseconds,
                maxConsecutiveErrorCount,
                autoBuyStaminaEnabled: payload.autoBuyStamina !== undefined
                    ? payload.autoBuyStamina
                    : defaultAutoBuyStaminaEnabledFromEnv,
                autoBuyStaminaMaxFailures: payload.autoBuyStaminaMaxFailures,
            })
                .then((summary) => {
                if (managedMiningTaskGeneration !== loopGeneration)
                    return;
                managedMiningStatus.running = false;
                managedMiningStatus.phase = "idle";
                managedMiningStatus.updatedAt = Date.now();
                managedMiningStatus.estimatedEndAt = undefined;
                managedMiningStatus.stopReason = summary.stopReason;
                managedMiningStatus.criticalErrorCode = summary.criticalErrorCode;
                if (summary.stopReason === "critical_error") {
                    managedMiningStatus.message = `Managed mining loop stopped by critical server error (code=${summary.criticalErrorCode}).`;
                }
                else if (summary.stopReason === "error_limit_reached") {
                    managedMiningStatus.message =
                        "Managed mining loop stopped after reaching the consecutive error limit.";
                }
                else if (summary.stopReason === "auto_buy_stamina_exhausted") {
                    managedMiningStatus.message = `Managed mining loop stopped because auto-buy stamina failed ${summary.autoBuyStaminaFailureCount ?? 0} consecutive times. Refill resources and restart.`;
                }
                else {
                    managedMiningStatus.message =
                        "Managed mining loop stopped by request.";
                }
                managedMiningStatus.roundsCompleted = summary.roundsCompleted;
                managedMiningStatus.consecutiveErrorCount =
                    summary.consecutiveErrorCount;
                if (summary.lastError) {
                    managedMiningStatus.lastError = summary.lastError;
                }
                if (summary.lastRewardDetails) {
                    managedMiningStatus.lastRewardDetails = summary.lastRewardDetails;
                }
                if (summary.lastCheckState) {
                    managedMiningStatus.lastCheckState = summary.lastCheckState;
                    managedMiningStatus.lastPlayerStatus = extractPlayerStatus(summary.lastCheckState);
                }
                appendMiningSessionEvent("stopped", {
                    stopReason: summary.stopReason,
                    criticalErrorCode: summary.criticalErrorCode,
                    autoBuyStaminaFailureCount: summary.autoBuyStaminaFailureCount,
                    roundsCompleted: summary.roundsCompleted,
                    consecutiveErrorCount: summary.consecutiveErrorCount,
                    lastError: summary.lastError,
                });
            })
                .catch((error) => {
                if (managedMiningTaskGeneration !== loopGeneration)
                    return;
                const message = error instanceof Error ? error.message : String(error);
                managedMiningStatus.running = false;
                managedMiningStatus.phase = "idle";
                managedMiningStatus.updatedAt = Date.now();
                managedMiningStatus.lastError = message;
                managedMiningStatus.message = `Managed mining loop crashed: ${message}`;
                appendMiningSessionEvent("stopped", {
                    stopReason: "critical_error",
                    lastError: message,
                });
            })
                .finally(async () => {
                try {
                    await setApiAutoMining(apiCode, false);
                }
                catch (error) {
                    console.warn("[skill-openclaw] setApiAutoMining(false) failed:", error);
                }
                if (managedMiningTaskGeneration === loopGeneration) {
                    managedMiningTask = undefined;
                }
            });
            return res.json({
                ok: true,
                data: {
                    created: true,
                    openclawSessionKey,
                    status: managedMiningStatus,
                },
            });
        }
        if (toolName === "stop_managed_mining_loop") {
            if (!managedMiningTask) {
                return res.status(404).json({
                    ok: false,
                    error: "managed_mining_loop_not_running",
                    data: managedMiningStatus,
                });
            }
            managedMiningTask.stopRequested = true;
            managedMiningStatus.phase = "stopping";
            managedMiningStatus.updatedAt = Date.now();
            managedMiningStatus.message =
                "Stop request received. Exiting safely at the next checkpoint.";
            return res.json({
                ok: true,
                data: { stopRequested: true, status: managedMiningStatus },
            });
        }
        if (toolName === "get_managed_mining_status") {
            const statusMessage = generateStatusMessage(managedMiningStatus);
            return res.json({
                ok: true,
                data: {
                    ...managedMiningStatus,
                    friendlyMessage: statusMessage,
                },
            });
        }
        if (toolName === "get_mining_quick_status") {
            const quickStatus = {
                running: managedMiningStatus.running,
                phase: managedMiningStatus.phase,
                message: managedMiningStatus.message,
                roundsCompleted: managedMiningStatus.roundsCompleted,
                consecutiveErrorCount: managedMiningStatus.consecutiveErrorCount,
                lastEventId: managedMiningStatus.lastEventId,
                updatedAt: managedMiningStatus.updatedAt,
            };
            return res.json({ ok: true, data: quickStatus });
        }
        if (toolName === "get_mining_session_events") {
            const sinceEventId = payload.sinceEventId ?? 0;
            const newEvents = managedMiningStatus.events.filter((event) => event.id > sinceEventId);
            return res.json({
                ok: true,
                data: {
                    openclawSessionKey: managedMiningStatus.openclawSessionKey,
                    sinceEventId,
                    lastEventId: managedMiningStatus.lastEventId,
                    events: newEvents,
                },
            });
        }
        if (toolName === "stop_auto_mining") {
            return res.status(410).json({
                ok: false,
                error: "tool_deprecated_use_stop_managed_mining_loop",
                message: "stop_auto_mining is deprecated. Use stop_managed_mining_loop.",
            });
        }
    }
    catch (error) {
        if (error instanceof GameApiHttpError) {
            const responseBody = error.responseBody;
            if (responseBody !== undefined &&
                typeof responseBody === "object" &&
                responseBody !== null) {
                return res.status(error.statusCode).json(responseBody);
            }
            return res.status(error.statusCode).json({ message: error.message });
        }
        if (error instanceof Error &&
            error.message.startsWith("game_api_timeout")) {
            return res.status(504).json({ error: error.message });
        }
        const errorMessage = error instanceof Error ? error.message : "tool_execution_failed";
        return res.status(502).json({ ok: false, error: errorMessage });
    }
    return res.status(404).json({ ok: false, error: "tool_not_found" });
});
app.get("/health", (_req, res) => {
    res.json({ ok: true, service: "skill-openclaw" });
});
const port = Number(process.env.PORT ?? "4021");
void bootstrap();
function resolveApiCode(payload, cacheKey) {
    if (payload.apiCode) {
        return payload.apiCode;
    }
    const cachedApiCode = apiCodeCache.get(cacheKey);
    if (!cachedApiCode) {
        throw new Error("api_code_required_or_cache_miss");
    }
    return cachedApiCode;
}
function resolveApiCodeOrBadRequest(res, payload, cacheKey) {
    try {
        return resolveApiCode(payload, cacheKey);
    }
    catch {
        res.status(400).json({ error: "api_code_required_or_cache_miss" });
        return undefined;
    }
}
async function bootstrap() {
    await loadApiCodeStore();
    app.listen(port, () => {
        console.log(`skill-openclaw listening on :${port}`);
    });
}
async function loadApiCodeStore() {
    try {
        const fileContent = await readFile(apiCodeStorePath, "utf-8");
        const parsedStore = JSON.parse(fileContent);
        const apiCodeEntries = Object.entries(parsedStore.apiCodes ?? {});
        for (const [cacheKey, apiCode] of apiCodeEntries) {
            const normalizedCacheKey = cacheKey.trim();
            const normalizedApiCode = String(apiCode).trim();
            if (!normalizedCacheKey || !normalizedApiCode) {
                continue;
            }
            apiCodeCache.set(normalizedCacheKey, normalizedApiCode);
        }
    }
    catch (error) {
        if (error.code === "ENOENT") {
            return;
        }
        throw error;
    }
}
async function persistApiCodeStore() {
    const apiCodeRecord = Object.fromEntries(apiCodeCache.entries());
    const serializedStore = JSON.stringify({ apiCodes: apiCodeRecord }, null, 2);
    await mkdir(path.dirname(apiCodeStorePath), { recursive: true });
    const tmpPath = `${apiCodeStorePath}.tmp.${process.pid}`;
    await writeFile(tmpPath, serializedStore, "utf-8");
    await rename(tmpPath, apiCodeStorePath);
}
async function upsertApiCode(cacheKey, apiCode) {
    apiCodeCache.set(cacheKey, apiCode.trim());
    await persistApiCodeStore();
}
function buildIdleManagedMiningStatus() {
    return {
        running: false,
        phase: "idle",
        message: "Managed mining loop is not running.",
        updatedAt: Date.now(),
        roundsCompleted: 0,
        consecutiveErrorCount: 0,
        maxConsecutiveErrorCount: defaultManagedMaxConsecutiveErrorCount,
        lastRewardDetails: [],
        events: [],
        lastEventId: 0,
    };
}
function extractOpenClawSessionKey(req, payload) {
    const headerValue = req.get("x-openclaw-session-key");
    const fromHeader = normalizeOpenClawSessionKey(headerValue);
    if (fromHeader) {
        return fromHeader;
    }
    const fromBodyExplicit = normalizeOpenClawSessionKey(payload.openclawSessionKey);
    if (fromBodyExplicit) {
        return fromBodyExplicit;
    }
    return normalizeOpenClawSessionKey(payload.sessionKey);
}
function normalizeOpenClawSessionKey(value) {
    if (value === undefined) {
        return undefined;
    }
    const trimmed = value.trim();
    return trimmed.length > 0 ? trimmed : undefined;
}
function appendMiningSessionEvent(eventType, eventPayload) {
    miningSessionEventIdCounter += 1;
    const miningSessionEvent = {
        id: miningSessionEventIdCounter,
        ts: Date.now(),
        type: eventType,
        payload: eventPayload,
    };
    managedMiningStatus.events.push(miningSessionEvent);
    managedMiningStatus.lastEventId = miningSessionEventIdCounter;
    const maxEventCount = Math.max(1, Math.floor(maxMiningSessionEventCount));
    while (managedMiningStatus.events.length > maxEventCount) {
        managedMiningStatus.events.shift();
    }
}
function generateStatusMessage(status) {
    if (!status.running) {
        return "Managed mining loop is not running";
    }
    if (status.roundsCompleted === 0) {
        return `Status: ${status.message}`;
    }
    const playerStatus = status.lastPlayerStatus;
    const goldCount = playerStatus?.Gold || 0;
    const rewardSummary = formatRewardSummary(status.lastRewardDetails);
    return `Round ${status.roundsCompleted} | ${rewardSummary} | Total Gold Bars ${goldCount} | Status: ${getRunningStatusText(status.phase)}`;
}
function getRunningStatusText(phase) {
    switch (phase) {
        case "starting_round":
            return "starting";
        case "waiting_estimated_end_at":
            return "waiting";
        case "polling_reward":
            return "claiming_reward";
        case "reward_collected":
        case "sleeping_between_rounds":
            return "mining";
        case "stopping":
            return "stopping";
        default:
            return "mining";
    }
}
function formatRewardSummary(rewardDetails) {
    if (!Array.isArray(rewardDetails) || rewardDetails.length === 0) {
        return "no_reward";
    }
    const oreCountMap = new Map();
    for (const reward of rewardDetails) {
        const name = String(reward.oreTypeName || reward.name || "unknown");
        const count = Number(reward.count || reward.amount || 0);
        if (count > 0) {
            oreCountMap.set(name, (oreCountMap.get(name) ?? 0) + count);
        }
    }
    if (oreCountMap.size === 0) {
        return "no_reward";
    }
    const parts = [];
    for (const [name, count] of oreCountMap) {
        parts.push(`${name}×${count}`);
    }
    return parts.join(", ");
}
function mapManagedMiningPhaseToMessage(phase) {
    const messageByPhase = {
        idle: "Managed mining loop is not running.",
        starting_round: "Starting current mining round.",
        waiting_estimated_end_at: "Estimated end time received. Waiting before polling reward.",
        polling_reward: "Polling reward status.",
        reward_collected: "Reward collected for current round.",
        sleeping_between_rounds: "Current round completed. Waiting 2 seconds before next round.",
        stopping: "Managed mining loop is stopping.",
    };
    return messageByPhase[phase];
}
function extractPlayerStatus(state) {
    if (!state || typeof state !== "object") {
        return undefined;
    }
    const stateObject = state;
    return stateObject.data?.commonInfo ?? stateObject.data?.playerStatus;
}
function normalizePositiveInteger(value, fallbackValue) {
    const normalizedValue = Math.floor(Number(value));
    if (!Number.isFinite(normalizedValue) || normalizedValue <= 0) {
        return fallbackValue;
    }
    return normalizedValue;
}
