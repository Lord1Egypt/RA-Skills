"use strict";
/**
 * Copyright (c) 2026 ByteDance Ltd. and/or its affiliates
 * SPDX-License-Identifier: MIT
 *
 * WebSocket monitoring for the Lark/Feishu channel plugin.
 *
 * Manages per-account WSClient connections and routes inbound Feishu
 * events (messages, bot membership changes, read receipts) to the
 * appropriate handlers.
 */
import { getLarkAccount, getEnabledLarkAccounts } from '../core/accounts';
import { LarkClient } from '../core/lark-client';
import { MessageDedup } from '../messaging/inbound/dedup';
import { larkLogger } from '../core/lark-logger';
import { drainShutdownHooks } from '../core/shutdown-hooks';
import { handleMessageEvent, handleReactionEvent, handleBotMembershipEvent, handleCardActionEvent, } from './event-handlers';
const mlog = larkLogger('channel/monitor');
// ---------------------------------------------------------------------------
// Single-account monitor
// ---------------------------------------------------------------------------
/**
 * Start monitoring a single Feishu account.
 *
 * Creates a LarkClient, probes bot identity, registers event handlers,
 * and starts a WebSocket connection. Returns a Promise that resolves
 * when the abort signal fires (or immediately if already aborted).
 */
async function monitorSingleAccount(params) {
    const { account, runtime, abortSignal } = params;
    const { accountId } = account;
    const log = runtime?.log ?? ((...args) => mlog.info(args.map(String).join(' ')));
    const error = runtime?.error ?? ((...args) => mlog.error(args.map(String).join(' ')));
    // Only websocket mode is supported in the monitor path.
    const connectionMode = account.config.connectionMode ?? 'websocket';
    if (connectionMode !== 'websocket') {
        log(`feishu[${accountId}]: webhook mode not implemented in monitor`);
        return;
    }
    // Message dedup — filters duplicate deliveries from WebSocket reconnects.
    const dedupCfg = account.config.dedup;
    const messageDedup = new MessageDedup({
        ttlMs: dedupCfg?.ttlMs,
        maxEntries: dedupCfg?.maxEntries,
    });
    log(`feishu[${accountId}]: message dedup enabled (ttl=${messageDedup['ttlMs']}ms, max=${messageDedup['maxEntries']})`);
    log(`feishu[${accountId}]: starting WebSocket connection...`);
    // Create LarkClient instance — manages SDK client, WS, and bot identity.
    const lark = LarkClient.fromAccount(account);
    // Attach dedup instance so it is disposed together with the client.
    lark.messageDedup = messageDedup;
    /** Per-chat history maps (used for group-chat context window). */
    const chatHistories = new Map();
    const ctx = {
        get cfg() {
            return LarkClient.runtime.config.loadConfig();
        },
        lark,
        accountId,
        chatHistories,
        messageDedup,
        runtime,
        log,
        error,
    };
    // [feishu-doc-collab] Debounce map for drive edit events (30s per fileToken)
    const _editDebounce = new Map();
    const DEBOUNCE_MS = 30000;
    async function _handleDriveEditEvent(data) {
        try {
            const fileToken = data?.file_token || data?.event?.file_token || '';
            const fileType = data?.file_type || data?.event?.file_type || 'unknown';
            const operatorId = data?.operator_id?.open_id || data?.event?.operator_id?.open_id || '';
            // Anti-loop: skip bot's own edits
            if (operatorId && operatorId === lark.botOpenId) {
                log(`feishu[${accountId}]: skipping own doc edit on ${fileToken}`);
                return;
            }
            // Debounce: skip if same file triggered within 30s
            const now = Date.now();
            const lastTrigger = _editDebounce.get(fileToken) || 0;
            if (now - lastTrigger < DEBOUNCE_MS) {
                log(`feishu[${accountId}]: debounce skip doc edit on ${fileToken}`);
                return;
            }
            _editDebounce.set(fileToken, now);
            // Trigger /hooks/agent
            const fs2 = await import("fs");
            const cfgRaw = fs2.readFileSync(`${process.env.HOME || "/root"}/.openclaw/openclaw.json`, "utf-8");
            const cfgJson = JSON.parse(cfgRaw);
            const hooksToken = cfgJson?.hooks?.token;
            const port = cfgJson?.gateway?.port ?? 18789;
            if (!hooksToken) {
                log(`feishu[${accountId}]: hooks.token not configured, cannot trigger agent`);
                return;
            }
            const agentMessage = `[Document Edit Event] Feishu document (token: ${fileToken}, type: ${fileType}) was edited.

INSTRUCTIONS — follow exactly:
1. Read DOC_PROTOCOL.md from workspace for the message format specification.
2. Read the document: feishu_fetch_doc(doc_id=${fileToken})
3. Find the LAST message block (delimited by ---). Parse its header line: sender, receiver, status.
4. Decision logic:
   - If status is 🔴 (editing) or missing → do NOTHING, reply NO_REPLY
   - If sender is yourself (MyBot) → do NOTHING, reply NO_REPLY
   - If receiver is not your name (MyBot) and not "all" → do NOTHING, reply NO_REPLY
   - If status is 🟢 (complete) AND receiver is you or "all" → process the message
5. If processing: compose your reply in the protocol format and append it using feishu_update_doc
6. If not processing: reply NO_REPLY`;
            const resp = await fetch(`http://127.0.0.1:${port}/hooks/agent`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "Authorization": `Bearer ${hooksToken}` },
                body: JSON.stringify({ message: agentMessage, deliver: false, name: "DocCollab" }),
            });
            if (resp.ok) {
                log(`feishu[${accountId}]: triggered /hooks/agent for doc edit on ${fileToken}`);
            } else {
                const body = await resp.text().catch(() => "");
                log(`feishu[${accountId}]: /hooks/agent returned ${resp.status}: ${body.slice(0,200)}`);
            }
        } catch (err) {
            log(`feishu[${accountId}]: doc edit handler error (non-fatal): ${String(err)}`);
        }
    }
    await lark.startWS({
        handlers: {
            'im.message.receive_v1': (data) => handleMessageEvent(ctx, data),
            'im.message.message_read_v1': async () => { },
            'im.message.reaction.created_v1': (data) => handleReactionEvent(ctx, data),
            'im.chat.member.bot.added_v1': (data) => handleBotMembershipEvent(ctx, data, 'added'),
            'im.chat.member.bot.deleted_v1': (data) => handleBotMembershipEvent(ctx, data, 'removed'),
            // [feishu-doc-collab] Document edit events
            'drive.file.edit_v1': (data) => _handleDriveEditEvent(data),
            'drive.file.bitable_record_changed_v1': (data) => _handleDriveEditEvent(data),
            'drive.file.read_v1': () => { /* intentionally ignored – doc read events */ },
            // 飞书 SDK EventDispatcher.register 不支持带返回值的处理器，此处 as any 是 SDK 类型限制的变通
            'card.action.trigger': ((data) => 
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            handleCardActionEvent(ctx, data)),
        },
        abortSignal,
    });
    // startWS resolves when abortSignal fires — probe result is logged inside startWS.
    log(`feishu[${accountId}]: bot open_id resolved: ${lark.botOpenId ?? 'unknown'}`);
    log(`feishu[${accountId}]: WebSocket client started`);
    mlog.info(`websocket started for account ${accountId}`);
}
// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------
/**
 * Start monitoring for all enabled Feishu accounts (or a single
 * account when `opts.accountId` is specified).
 */
export async function monitorFeishuProvider(opts = {}) {
    const cfg = opts.config;
    if (!cfg) {
        throw new Error('Config is required for Feishu monitor');
    }
    // Store the original global config so plugin commands (doctor, diagnose)
    // can access cross-account information even when running inside an
    // account-scoped config context.
    LarkClient.setGlobalConfig(cfg);
    const log = opts.runtime?.log ?? ((...args) => mlog.info(args.map(String).join(' ')));
    // Single-account mode.
    if (opts.accountId) {
        const account = getLarkAccount(cfg, opts.accountId);
        if (!account.enabled || !account.configured) {
            throw new Error(`Feishu account "${opts.accountId}" not configured or disabled`);
        }
        await monitorSingleAccount({
            cfg,
            account,
            runtime: opts.runtime,
            abortSignal: opts.abortSignal,
        });
        await drainShutdownHooks({ log });
        return;
    }
    // Multi-account mode: start all enabled accounts in parallel.
    const accounts = getEnabledLarkAccounts(cfg);
    if (accounts.length === 0) {
        throw new Error('No enabled Feishu accounts configured');
    }
    log(`feishu: starting ${accounts.length} account(s): ${accounts.map((a) => a.accountId).join(', ')}`);
    await Promise.all(accounts.map((account) => monitorSingleAccount({
        cfg,
        account,
        runtime: opts.runtime,
        abortSignal: opts.abortSignal,
    })));
    await drainShutdownHooks({ log });
}
