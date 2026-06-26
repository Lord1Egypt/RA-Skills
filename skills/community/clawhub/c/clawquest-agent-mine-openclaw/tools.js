import { readFile } from "node:fs/promises";
import path from "node:path";
const gameApiBaseUrl = process.env.GAME_API_BASE_URL ?? "https://api.km.cocweb3.com";
const requestTimeoutMilliseconds = Number(process.env.REQUEST_TIMEOUT_MS ?? "8000");
const oreTypeNameMapPath = process.env.ORE_TYPE_NAME_MAP_PATH ??
    path.join(process.cwd(), "config", "ore-type-map.json");
const defaultManagedPollingIntervalMilliseconds = Number(process.env.MANAGED_MINING_POLL_INTERVAL_MS ?? "1000");
const defaultManagedRoundIntervalMilliseconds = Number(process.env.MANAGED_MINING_ROUND_INTERVAL_MS ?? "2000");
const defaultManagedMaxConsecutiveErrorCount = Number(process.env.MANAGED_MINING_MAX_CONSECUTIVE_ERROR_COUNT ?? "10");
const defaultAutoBuyStaminaMaxFailures = Number(process.env.MANAGED_MINING_AUTO_BUY_MAX_FAILURES ?? "3");
const defaultLanguage = "zh_CN";
const supportedLanguages = new Set([
    "zh_CN",
    "zh_TW",
    "en_US",
    "ja_JP",
    "ko_KR",
    "ru_RU",
]);
let oreTypeNameMapCache;
export class GameApiHttpError extends Error {
    statusCode;
    responseBody;
    constructor(statusCode, message, responseBody) {
        super(message);
        this.name = "GameApiHttpError";
        this.statusCode = statusCode;
        this.responseBody = responseBody;
    }
}
const SERVER_ERROR = {
    COMMON_INVALID_PARAMS: 400,
    COMMON_NOT_ENOUGH_RESOURCES: 1010,
    GAME_INSUFFICIENT_RESOURCES: 2003,
    GAME_DIAMOND_NOT_ENOUGH: 2008,
    GAME_MINING_STATE_CONFLICT: 2009,
    GAME_MINING_API_NOT_ACTIVE: 2014,
    GAME_MINING_NOT_FINISHED: 2018,
};
function isInsufficientStaminaCode(code) {
    return code === SERVER_ERROR.GAME_INSUFFICIENT_RESOURCES;
}
function isCriticalStopCode(code) {
    return (code === SERVER_ERROR.GAME_DIAMOND_NOT_ENOUGH ||
        code === SERVER_ERROR.GAME_MINING_API_NOT_ACTIVE ||
        code === SERVER_ERROR.COMMON_INVALID_PARAMS);
}
function isMiningStateConflictCode(code) {
    return code === SERVER_ERROR.GAME_MINING_STATE_CONFLICT;
}
/**
 * Whether endMining should keep polling without escalating the error.
 */
function isPollingRewardRetryableCode(code) {
    return code === SERVER_ERROR.GAME_MINING_NOT_FINISHED;
}
function extractServerErrorCode(responseBody) {
    if (!responseBody || typeof responseBody !== "object") {
        return undefined;
    }
    const body = responseBody;
    return typeof body.code === "number" ? body.code : undefined;
}
function extractGetStaminaSnapshot(envelope) {
    if (!envelope || typeof envelope !== "object") {
        return undefined;
    }
    const envelopeObject = envelope;
    if (envelopeObject.code !== 0) {
        return undefined;
    }
    const dataObject = envelopeObject.data;
    if (!dataObject || typeof dataObject !== "object") {
        return undefined;
    }
    const stamina = Number(dataObject.stamina);
    const diamonds = Number(dataObject.diamonds);
    const maxStamina = Number(dataObject.maxStamina);
    if (!Number.isFinite(stamina) ||
        !Number.isFinite(diamonds) ||
        !Number.isFinite(maxStamina)) {
        return undefined;
    }
    return { stamina, diamonds, maxStamina };
}
function isBuyStaminaDiamondInsufficientCode(code) {
    if (code === undefined) {
        return false;
    }
    return (code === SERVER_ERROR.COMMON_NOT_ENOUGH_RESOURCES ||
        code === SERVER_ERROR.GAME_DIAMOND_NOT_ENOUGH);
}
async function tryAutoBuyStaminaAfterInsufficientResources(apiCode) {
    const getResult = await executePostWithApiCode("/api/getStamina", apiCode, {});
    if (getResult.httpStatus < 200 || getResult.httpStatus >= 300) {
        return "failed";
    }
    const getCode = extractServerErrorCode(getResult.body);
    if (getCode !== undefined && getCode !== 0) {
        return "failed";
    }
    const staminaSnapshot = extractGetStaminaSnapshot(getResult.body);
    if (staminaSnapshot &&
        staminaSnapshot.maxStamina > 0 &&
        staminaSnapshot.stamina >= staminaSnapshot.maxStamina) {
        return "recovered";
    }
    if (staminaSnapshot && staminaSnapshot.diamonds <= 0) {
        return "failed";
    }
    const buyResult = await executePostWithApiCode("/api/buyStamina", apiCode, {});
    if (buyResult.httpStatus < 200 || buyResult.httpStatus >= 300) {
        return "failed";
    }
    const buyCode = extractServerErrorCode(buyResult.body);
    if (buyCode === 0) {
        return "recovered";
    }
    if (isBuyStaminaDiamondInsufficientCode(buyCode)) {
        return "failed";
    }
    return "failed";
}
export async function startMining(apiCode) {
    return await postJson("/api/startMining", apiCode, {});
}
export async function checkMiningState(apiCode) {
    return await postJson("/api/checkMiningState", apiCode, {});
}
/** 同步服务端 MiningRuntime.apiAutoMining（托管循环开始时 true，结束时 false）。 */
export async function setApiAutoMining(apiCode, enabled) {
    const body = await postJson("/api/setAutoMining", apiCode, { enabled });
    const code = extractServerErrorCode(body);
    if (code !== undefined && code !== 0) {
        throw new GameApiHttpError(502, `setAutoMining failed code=${code}`, body);
    }
}
export async function endMining(apiCode, lang) {
    const response = await postJson("/api/endMining", apiCode, {});
    return await enrichRewardResponse(response, lang);
}
export async function fetchGameApiWithApiCodePost(path, apiCode, jsonBody) {
    return await executePostWithApiCode(path, apiCode, jsonBody);
}
export async function enrichEndMiningResponseForDisplay(response, lang) {
    return await enrichRewardResponse(response, lang);
}
export async function runManagedMiningLoop(apiCode, shouldContinue, callbacks, options) {
    const normalizedLanguage = normalizeLanguage(options?.lang);
    const pollingIntervalMilliseconds = normalizePositiveInteger(options?.pollingIntervalMilliseconds, defaultManagedPollingIntervalMilliseconds);
    const roundIntervalMilliseconds = normalizePositiveInteger(options?.roundIntervalMilliseconds, defaultManagedRoundIntervalMilliseconds);
    const maxConsecutiveErrorCount = normalizePositiveInteger(options?.maxConsecutiveErrorCount, defaultManagedMaxConsecutiveErrorCount);
    const autoBuyStaminaEnabled = options?.autoBuyStaminaEnabled === true;
    const autoBuyStaminaMaxFailuresConfigured = normalizePositiveInteger(options?.autoBuyStaminaMaxFailures, defaultAutoBuyStaminaMaxFailures);
    let roundsCompleted = 0;
    let consecutiveErrorCount = 0;
    let autoBuyStaminaFailureCount = 0;
    let lastError;
    let lastRewardDetails;
    let lastCheckState;
    while (shouldContinue()) {
        try {
            callbacks?.onPhaseChanged?.("starting_round");
            let startMiningState;
            try {
                startMiningState = await startMining(apiCode);
                consecutiveErrorCount = 0;
                lastError = undefined;
            }
            catch (error) {
                throw error;
            }
            const now = Date.now();
            let estimatedEndAt = extractEstimatedEndAt(startMiningState);
            if (!estimatedEndAt || estimatedEndAt <= now) {
                estimatedEndAt = now + 60000;
            }
            else {
                estimatedEndAt = Math.min(estimatedEndAt + 10000, now + 60000);
            }
            callbacks?.onPhaseChanged?.("waiting_estimated_end_at", {
                estimatedEndAt,
            });
            await sleepWithContinueCheck(estimatedEndAt - Date.now(), shouldContinue);
            if (!shouldContinue()) {
                break;
            }
            callbacks?.onPhaseChanged?.("polling_reward");
            while (shouldContinue()) {
                try {
                    const endResult = await endMining(apiCode, normalizedLanguage);
                    const rewardDetails = extractRewardDetails(endResult);
                    lastRewardDetails = rewardDetails;
                    lastCheckState = endResult;
                    roundsCompleted += 1;
                    autoBuyStaminaFailureCount = 0;
                    consecutiveErrorCount = 0;
                    lastError = undefined;
                    callbacks?.onRoundCompleted?.({
                        rewardDetails,
                        checkState: endResult,
                    });
                    callbacks?.onPhaseChanged?.("reward_collected", {
                        rewardCount: rewardDetails.length,
                        roundsCompleted,
                    });
                    callbacks?.onPhaseChanged?.("sleeping_between_rounds", {
                        roundIntervalMilliseconds,
                    });
                    await sleepWithContinueCheck(roundIntervalMilliseconds, shouldContinue);
                    break;
                }
                catch (endError) {
                    if (endError instanceof GameApiHttpError) {
                        const serverCode = extractServerErrorCode(endError.responseBody);
                        if (serverCode !== undefined && isCriticalStopCode(serverCode)) {
                            throw endError;
                        }
                        if (serverCode !== undefined &&
                            isPollingRewardRetryableCode(serverCode)) {
                            await sleepWithContinueCheck(pollingIntervalMilliseconds, shouldContinue);
                            continue;
                        }
                    }
                    throw endError;
                }
            }
        }
        catch (error) {
            if (error instanceof GameApiHttpError) {
                const serverCode = extractServerErrorCode(error.responseBody);
                if (autoBuyStaminaEnabled &&
                    serverCode !== undefined &&
                    isInsufficientStaminaCode(serverCode)) {
                    const buyAttempt = await tryAutoBuyStaminaAfterInsufficientResources(apiCode);
                    if (buyAttempt === "recovered") {
                        autoBuyStaminaFailureCount = 0;
                        await sleepWithContinueCheck(pollingIntervalMilliseconds, shouldContinue);
                        continue;
                    }
                    autoBuyStaminaFailureCount += 1;
                    lastError = `stamina_insufficient_auto_buy_failed count=${autoBuyStaminaFailureCount} max=${autoBuyStaminaMaxFailuresConfigured}`;
                    callbacks?.onError?.(lastError, autoBuyStaminaFailureCount, autoBuyStaminaMaxFailuresConfigured);
                    if (autoBuyStaminaFailureCount >= autoBuyStaminaMaxFailuresConfigured) {
                        callbacks?.onPhaseChanged?.("stopping", {
                            stopReason: "auto_buy_stamina_exhausted",
                            autoBuyStaminaFailureCount,
                        });
                        return {
                            stopReason: "auto_buy_stamina_exhausted",
                            roundsCompleted,
                            consecutiveErrorCount,
                            maxConsecutiveErrorCount,
                            lastError,
                            criticalErrorCode: serverCode,
                            autoBuyStaminaFailureCount,
                            lastRewardDetails,
                            lastCheckState,
                        };
                    }
                    await sleepWithContinueCheck(pollingIntervalMilliseconds, shouldContinue);
                    continue;
                }
                if (serverCode !== undefined && isCriticalStopCode(serverCode)) {
                    consecutiveErrorCount += 1;
                    lastError = getErrorMessage(error);
                    callbacks?.onPhaseChanged?.("stopping", {
                        stopReason: "critical_error",
                        consecutiveErrorCount,
                        criticalErrorCode: serverCode,
                    });
                    return {
                        stopReason: "critical_error",
                        roundsCompleted,
                        consecutiveErrorCount,
                        maxConsecutiveErrorCount,
                        lastError,
                        criticalErrorCode: serverCode,
                        lastRewardDetails,
                        lastCheckState,
                    };
                }
            }
            consecutiveErrorCount += 1;
            lastError = getErrorMessage(error);
            callbacks?.onError?.(lastError, consecutiveErrorCount, maxConsecutiveErrorCount);
            if (consecutiveErrorCount >= maxConsecutiveErrorCount) {
                callbacks?.onPhaseChanged?.("stopping", {
                    stopReason: "error_limit_reached",
                    consecutiveErrorCount,
                });
                return {
                    stopReason: "error_limit_reached",
                    roundsCompleted,
                    consecutiveErrorCount,
                    maxConsecutiveErrorCount,
                    lastError,
                    lastRewardDetails,
                    lastCheckState,
                };
            }
            await sleepWithContinueCheck(pollingIntervalMilliseconds, shouldContinue);
        }
    }
    callbacks?.onPhaseChanged?.("stopping", { stopReason: "stopped_by_user" });
    return {
        stopReason: "stopped_by_user",
        roundsCompleted,
        consecutiveErrorCount,
        maxConsecutiveErrorCount,
        lastError,
        lastRewardDetails,
        lastCheckState,
    };
}
async function executePostWithApiCode(path, apiCode, jsonBody) {
    const sanitizedApiCode = apiCode.trim();
    if (!sanitizedApiCode) {
        throw new Error("invalid_api_code");
    }
    const abortController = new AbortController();
    const timeoutHandle = setTimeout(() => {
        abortController.abort();
    }, requestTimeoutMilliseconds);
    try {
        const response = await fetch(`${gameApiBaseUrl}${path}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Api-Code": sanitizedApiCode,
            },
            body: JSON.stringify(jsonBody),
            signal: abortController.signal,
        });
        const responseJson = (await response.json());
        return { httpStatus: response.status, body: responseJson };
    }
    catch (error) {
        if (error instanceof Error && error.name === "AbortError") {
            throw new Error(`game_api_timeout timeoutMs=${requestTimeoutMilliseconds}`);
        }
        throw error;
    }
    finally {
        clearTimeout(timeoutHandle);
    }
}
async function postJson(path, apiCode, body) {
    const { httpStatus, body: responseBody } = await executePostWithApiCode(path, apiCode, body);
    if (httpStatus < 200 || httpStatus >= 300) {
        throw new GameApiHttpError(httpStatus, `game_api_error status=${httpStatus} body=${JSON.stringify(responseBody)}`, responseBody);
    }
    return responseBody;
}
function extractEstimatedEndAt(startState) {
    if (!startState || typeof startState !== "object") {
        return undefined;
    }
    const stateObject = startState;
    const estimatedEndAt = Number(stateObject.data?.estimatedEndAt);
    if (!Number.isFinite(estimatedEndAt) || estimatedEndAt <= 0) {
        return undefined;
    }
    return estimatedEndAt;
}
function extractRewardDetails(checkState) {
    if (!checkState || typeof checkState !== "object") {
        return [];
    }
    const stateObject = checkState;
    const resourceResultList = stateObject.data?.reward?.resResults;
    if (!Array.isArray(resourceResultList)) {
        return [];
    }
    return resourceResultList.map((resourceResultItem) => ({
        ...resourceResultItem,
    }));
}
function normalizePositiveInteger(value, fallbackValue) {
    const normalizedValue = Math.floor(Number(value));
    if (!Number.isFinite(normalizedValue) || normalizedValue <= 0) {
        return fallbackValue;
    }
    return normalizedValue;
}
function getErrorMessage(error) {
    if (error instanceof Error) {
        return error.message;
    }
    return String(error);
}
async function sleepWithContinueCheck(totalMilliseconds, shouldContinue) {
    const normalizedMilliseconds = Math.max(0, Math.floor(totalMilliseconds));
    if (normalizedMilliseconds <= 0) {
        return;
    }
    let remainingMilliseconds = normalizedMilliseconds;
    while (remainingMilliseconds > 0 && shouldContinue()) {
        const currentSleepMilliseconds = Math.min(remainingMilliseconds, 1000);
        await new Promise((resolve) => setTimeout(resolve, currentSleepMilliseconds));
        remainingMilliseconds -= currentSleepMilliseconds;
    }
}
async function enrichRewardResponse(response, lang) {
    const oreTypeNameMap = await loadOreTypeNameMap();
    const normalizedLanguage = normalizeLanguage(lang);
    if (!response || typeof response !== "object") {
        return response;
    }
    const responseObject = response;
    const resultList = responseObject.data?.reward?.resResults;
    if (!Array.isArray(resultList)) {
        return response;
    }
    for (const resultItem of resultList) {
        const oreTypeValue = Number(resultItem.oreType);
        if (!Number.isFinite(oreTypeValue)) {
            resultItem.oreTypeName = "Unknown Ore";
            continue;
        }
        const oreTypeNames = oreTypeNameMap[String(oreTypeValue)];
        if (!oreTypeNames) {
            resultItem.oreTypeName = `Unknown Ore(${oreTypeValue})`;
            continue;
        }
        resultItem.oreTypeName =
            oreTypeNames[normalizedLanguage] ??
                oreTypeNames[defaultLanguage] ??
                `Unknown Ore(${oreTypeValue})`;
    }
    return responseObject;
}
async function loadOreTypeNameMap() {
    if (oreTypeNameMapCache) {
        return oreTypeNameMapCache;
    }
    try {
        const fileContent = await readFile(oreTypeNameMapPath, "utf-8");
        const parsed = JSON.parse(fileContent);
        oreTypeNameMapCache = parsed.oreTypeNameMap ?? {};
        return oreTypeNameMapCache;
    }
    catch {
        oreTypeNameMapCache = {};
        return oreTypeNameMapCache;
    }
}
function normalizeLanguage(lang) {
    const normalizedLanguage = String(lang ?? "").trim();
    if (!supportedLanguages.has(normalizedLanguage)) {
        return defaultLanguage;
    }
    return normalizedLanguage;
}
