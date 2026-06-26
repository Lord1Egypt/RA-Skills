import type { DingTalkConfig } from "./index.js";
import { resolveDingTalkCredentials } from "./index.js";

export interface ProbeResult {
  ok: boolean;
  error?: string;
  botName?: string;
  botUserId?: string;
}

export async function probeDingTalk(cfg: DingTalkConfig): Promise<ProbeResult> {
  const creds = resolveDingTalkCredentials(cfg);
  if (!creds) {
    return { ok: false, error: "Credentials not configured" };
  }

  try {
    const response = await fetch(
      `https://oapi.dingtalk.com/gettoken?appkey=${encodeURIComponent(creds.clientId)}&appsecret=${encodeURIComponent(creds.clientSecret)}`,
      { method: "GET" }
    );

    if (!response.ok) {
      return { ok: false, error: `HTTP ${response.status}` };
    }

    const data = await response.json();
    if (data.errcode !== 0) {
      return { ok: false, error: data.errmsg || `Error ${data.errcode}` };
    }

    const accessToken = data.access_token;

    // Try to get bot/app info
    try {
      const appInfoResponse = await fetch(
        `https://oapi.dingtalk.com/topapi/microapp/list?access_token=${accessToken}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({}),
        }
      );

      const appInfo = await appInfoResponse.json();
      if (appInfo.errcode === 0 && appInfo.appList && appInfo.appList.length > 0) {
        const app = appInfo.appList[0];
        return {
          ok: true,
          botName: app.name,
          botUserId: app.agentId,
        };
      }
    } catch {
      // Ignore app info errors
    }

    return { ok: true };
  } catch (error) {
    return { ok: false, error: String(error) };
  }
}
