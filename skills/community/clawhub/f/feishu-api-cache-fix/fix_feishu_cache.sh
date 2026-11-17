#!/bin/bash
# 飞书API缓存修复脚本
# 添加2小时缓存，避免每分钟调用API

PROBE_FILE="/usr/local/lib/node_modules/openclaw/extensions/feishu/src/probe.ts"

# 备份原文件
cp "$PROBE_FILE" "${PROBE_FILE}.bak"

# 创建带缓存的版本
cat > "$PROBE_FILE" << 'EOF'
import type { FeishuProbeResult } from "./types.js";
import { createFeishuClient, type FeishuClientCredentials } from "./client.js";

// Cache probe results to avoid hitting API rate limits
// Cache for 2 hours (2h = 7200000ms)
const PROBE_CACHE_TTL_MS = 2 * 60 * 60 * 1000;
const probeCache = new Map<string, { result: FeishuProbeResult; timestamp: number }>();

function getCacheKey(creds?: FeishuClientCredentials): string {
  if (!creds?.appId) return "no-creds";
  return creds.appId;
}

export async function probeFeishu(creds?: FeishuClientCredentials): Promise<FeishuProbeResult> {
  if (!creds?.appId || !creds?.appSecret) {
    return {
      ok: false,
      error: "missing credentials (appId, appSecret)",
    };
  }

  // Check cache first
  const cacheKey = getCacheKey(creds);
  const cached = probeCache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < PROBE_CACHE_TTL_MS) {
    return cached.result;
  }

  try {
    const client = createFeishuClient(creds);
    // Use bot/v3/info API to get bot information
    // eslint-disable-next-line @typescript-eslint/no-explicit-any -- SDK generic request method
    const response = await (client as any).request({
      method: "GET",
      url: "/open-apis/bot/v3/info",
      data: {},
    });

    if (response.code !== 0) {
      const result = {
        ok: false,
        appId: creds.appId,
        error: `API error: ${response.msg || \`code \${response.code}\`}`,
      };
      probeCache.set(cacheKey, { result, timestamp: Date.now() });
      return result;
    }

    const bot = response.bot || response.data?.bot;
    const result = {
      ok: true,
      appId: creds.appId,
      botName: bot?.bot_name,
      botOpenId: bot?.open_id,
    };
    
    // Cache the result
    probeCache.set(cacheKey, { result, timestamp: Date.now() });
    return result;
  } catch (err) {
    const result = {
      ok: false,
      appId: creds.appId,
      error: err instanceof Error ? err.message : String(err),
    };
    probeCache.set(cacheKey, { result, timestamp: Date.now() });
    return result;
  }
}
EOF

echo "✅ 飞书API缓存修复完成！"
echo "备份文件: ${PROBE_FILE}.bak"
echo ""
echo "请运行以下命令重启OpenClaw使更改生效："
echo "  点击菜单栏OpenClaw图标 → Restart"
