#!/usr/bin/env bash
# get-credential.sh — Centralized credential resolver for agent-memes scripts.
# Reads from env vars first, falls back to ~/.openclaw/openclaw.json.
#
# Usage: get-credential.sh <platform> [field...]
#   discord              → prints bot token
#   feishu               → prints "appId appSecret"
#   telegram             → prints bot token
#   slack                → prints bot token
#   whatsapp             → prints "token phoneId"
#   wechat               → prints "corpId corpSecret agentId"
#   qq                   → prints "token appId"
#   line                 → prints channel access token
#
# Security: only reads the specific fields needed, never dumps full config.
set -euo pipefail

PLATFORM="${1:?Usage: get-credential.sh <platform>}"
CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"

# Helper: read a specific field path from openclaw.json via Node
_read_config() {
  node -e "
const fs = require('fs');
try {
  const c = JSON.parse(fs.readFileSync('$CONFIG', 'utf8'));
  const val = $1;
  if (!val) { process.exit(1); }
  process.stdout.write(String(val));
} catch { process.exit(1); }
" 2>/dev/null
}

case "$PLATFORM" in
  discord)
    if [[ -n "${DISCORD_BOT_TOKEN:-}" ]]; then
      echo "$DISCORD_BOT_TOKEN"
    else
      ACCT="${DISCORD_ACCOUNT:-}"
      _read_config "(() => {
        const accts = c.channels?.discord?.accounts || {};
        const name = '$ACCT' || Object.keys(accts)[0] || '';
        return accts[name]?.token || '';
      })()" || { echo "Error: Set DISCORD_BOT_TOKEN or configure openclaw.json" >&2; exit 1; }
    fi
    ;;
  feishu)
    if [[ -n "${FEISHU_APP_ID:-}" && -n "${FEISHU_APP_SECRET:-}" ]]; then
      echo "$FEISHU_APP_ID $FEISHU_APP_SECRET"
    else
      ACCT="${FEISHU_ACCOUNT:-}"
      _read_config "(() => {
        const accts = c.channels?.feishu?.accounts ?? {};
        const name = '$ACCT' || Object.keys(accts)[0];
        const a = accts[name];
        if (!a?.appId || !a?.appSecret) return '';
        return a.appId + ' ' + a.appSecret;
      })()" || { echo "Error: Set FEISHU_APP_ID+FEISHU_APP_SECRET or configure openclaw.json" >&2; exit 1; }
    fi
    ;;
  telegram)
    if [[ -n "${TELEGRAM_BOT_TOKEN:-}" ]]; then
      echo "$TELEGRAM_BOT_TOKEN"
    else
      _read_config "(() => {
        const t = c.channels?.telegram;
        return t?.botToken || t?.token || (() => {
          const accts = t?.accounts || {};
          const name = Object.keys(accts)[0] || '';
          return accts[name]?.token || '';
        })();
      })()" || { echo "Error: Set TELEGRAM_BOT_TOKEN or configure openclaw.json" >&2; exit 1; }
    fi
    ;;
  slack)
    if [[ -n "${SLACK_BOT_TOKEN:-}" ]]; then
      echo "$SLACK_BOT_TOKEN"
    else
      _read_config "(() => {
        const accts = c.channels?.slack?.accounts || {};
        const name = Object.keys(accts)[0] || '';
        return accts[name]?.token || '';
      })()" || { echo "Error: Set SLACK_BOT_TOKEN or configure openclaw.json" >&2; exit 1; }
    fi
    ;;
  whatsapp)
    if [[ -n "${WHATSAPP_TOKEN:-}" && -n "${WHATSAPP_PHONE_ID:-}" ]]; then
      echo "$WHATSAPP_TOKEN $WHATSAPP_PHONE_ID"
    else
      _read_config "(() => {
        const w = c.channels?.whatsapp || {};
        const t = w.token || ''; const p = w.phoneId || w.phone_id || '';
        if (!t || !p) return '';
        return t + ' ' + p;
      })()" || { echo "Error: Set WHATSAPP_TOKEN+WHATSAPP_PHONE_ID or configure openclaw.json" >&2; exit 1; }
    fi
    ;;
  wechat)
    if [[ -n "${WECHAT_CORP_ID:-}" && -n "${WECHAT_CORP_SECRET:-}" ]]; then
      echo "$WECHAT_CORP_ID $WECHAT_CORP_SECRET ${WECHAT_AGENT_ID:-}"
    else
      _read_config "(() => {
        const w = c.channels?.wechat || c.channels?.wecom || {};
        const id = w.corpId || w.corp_id || '';
        const s = w.corpSecret || w.corp_secret || '';
        const a = w.agentId || w.agent_id || '';
        if (!id || !s) return '';
        return id + ' ' + s + ' ' + a;
      })()" || { echo "Error: Set WECHAT_CORP_ID+WECHAT_CORP_SECRET or configure openclaw.json" >&2; exit 1; }
    fi
    ;;
  qq)
    if [[ -n "${QQ_BOT_TOKEN:-}" && -n "${QQ_BOT_APPID:-}" ]]; then
      echo "$QQ_BOT_TOKEN $QQ_BOT_APPID"
    else
      _read_config "(() => {
        const q = c.channels?.qqbot || c.channels?.qq || {};
        const t = q.token || ''; const a = q.appId || q.app_id || '';
        if (!t || !a) return '';
        return t + ' ' + a;
      })()" || { echo "Error: Set QQ_BOT_TOKEN+QQ_BOT_APPID or configure openclaw.json" >&2; exit 1; }
    fi
    ;;
  line)
    if [[ -n "${LINE_CHANNEL_ACCESS_TOKEN:-}" ]]; then
      echo "$LINE_CHANNEL_ACCESS_TOKEN"
    else
      ACCT="${LINE_ACCOUNT:-}"
      _read_config "(() => {
        const accts = c.channels?.line?.accounts || {};
        const name = '$ACCT' || Object.keys(accts)[0] || '';
        return accts[name]?.channelAccessToken || accts[name]?.token || '';
      })()" || { echo "Error: Set LINE_CHANNEL_ACCESS_TOKEN or configure openclaw.json" >&2; exit 1; }
    fi
    ;;
  *)
    echo "Error: Unknown platform '$PLATFORM'" >&2
    exit 1
    ;;
esac
