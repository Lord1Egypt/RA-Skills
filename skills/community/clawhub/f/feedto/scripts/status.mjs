#!/usr/bin/env node
import { getRuntimeSnapshot } from "./common.mjs";

const snapshot = await getRuntimeSnapshot();

console.log(`STATE: ${snapshot.state}`);
console.log(`MODE: ${snapshot.mode || "unknown"}`);
console.log(`API_URL: ${snapshot.apiUrl}`);
console.log(`STATE_DIR: ${snapshot.stateDir}`);
console.log(`PROCESS: ${snapshot.pid || "none"}${snapshot.pid ? snapshot.processAlive ? " (alive)" : " (stale)" : ""}`);
console.log(`HEARTBEAT: ${snapshot.heartbeatAt || "none"}${snapshot.heartbeatAge ? ` (${snapshot.heartbeatAge})` : ""}`);
console.log(`QUEUE_LENGTH: ${snapshot.queueLength}`);
console.log(`OLDEST_QUEUED_AT: ${snapshot.oldestQueuedAt || "none"}`);
console.log(`NEWEST_QUEUED_AT: ${snapshot.newestQueuedAt || "none"}`);
console.log(`LAST_FEED_AT: ${snapshot.lastFeedAt || "none"}${snapshot.lastFeedAge ? ` (${snapshot.lastFeedAge})` : ""}`);
console.log(`LAST_BACKFILL_COUNT: ${snapshot.lastBackfillCount ?? "none"}`);
console.log(`MESSAGE: ${snapshot.message || "none"}`);
console.log(`LAST_ERROR: ${snapshot.lastError || "none"}`);
console.log(`UPDATED_AT: ${snapshot.updatedAt || "none"}`);
