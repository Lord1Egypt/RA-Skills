import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const openapi = require('@alicloud/openapi-client');
const OpenApiClient = openapi.default;
const { Config, Params, OpenApiRequest } = openapi;

const config = new Config({
  accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET
});
config.endpoint = `green-cip.cn-beijing.aliyuncs.com`;
const client = new OpenApiClient(config);

const guardParams = new Params({
  action: 'MultiModalGuard',
  version: '2022-03-02',
  protocol: 'HTTPS',
  method: 'POST',
  authType: 'AK',
  style: 'RPC',
  pathname: `/`,
  reqBodyType: 'formData',
  bodyType: 'json',
});

const contentCache = new Map<string, { blocked: boolean; blockText: string }>();

function hashContent(content: string): string {
  let h = 0;
  for (let i = 0; i < content.length; i++) {
    h = ((h << 5) - h + content.charCodeAt(i)) | 0;
  }
  return String(h);
}

async function checkContent(content: string): Promise<{ blocked: boolean; reasons: string[] }> {
  const body: Record<string, string> = {};
  body['Service'] = 'agent_runtime_guard';
  body['ServiceParameters'] = JSON.stringify({ content: content.slice(0, 2000) });

  const request = new OpenApiRequest({ body });
  const timeout = new Promise<never>((_, reject) => setTimeout(() => reject(new Error('timeout')), 1000));
  const resp = await Promise.race([client.callApi(guardParams, request, {} as any), timeout]);
  const details = resp?.body?.Data?.Detail || [];
  const reasons: string[] = [];
  for (const item of details) {
    if (item.Suggestion === 'block') {
      for (const r of item.Result || []) {
        reasons.push(`[${item.Type}] ${r.Description} (${r.Label}, level: ${r.Level})`);
      }
    }
  }
  return { blocked: reasons.length > 0, reasons };
}


const SECURITY_MARKER = Symbol.for('__security_hook_passed__');

function extractLastUserContent(parsed: any): string | null {
  const messages = parsed?.messages;
  if (!Array.isArray(messages) || messages.length === 0) return null;
  for (let i = messages.length - 1; i >= 0; i--) {
    const msg = messages[i];
    if (msg.role === 'user') {
      if (typeof msg.content === 'string') return msg.content;
      if (Array.isArray(msg.content)) {
        const textPart = msg.content.find((p: any) => p.type === 'text' && typeof p.text === 'string');
        if (textPart) return textPart.text;
      }
      return null;
    }
  }
  return null;
}

function getUserContent(msg: any): string | null {
  if (msg.role !== 'user') return null;
  if (typeof msg.content === 'string') return msg.content;
  if (Array.isArray(msg.content)) {
    const t = msg.content.find((p: any) => p.type === 'text' && typeof p.text === 'string');
    if (t) return t.text;
  }
  return null;
}

function replaceUserContent(msg: any, text: string) {
  if (typeof msg.content === 'string') {
    msg.content = text;
  } else if (Array.isArray(msg.content)) {
    const idx = msg.content.findIndex((p: any) => p.type === 'text');
    if (idx >= 0) msg.content[idx].text = text;
  }
}

const originalFetch = globalThis.fetch;

const patchedFetch: typeof globalThis.fetch = async (input, init) => {
  if ((init as any)?.[SECURITY_MARKER]) {
    return originalFetch(input, init as any);
  }

  try {
    const bodyText = typeof init?.body === 'string' ? init.body : '';
    if (bodyText && bodyText.startsWith('{')) {
      const parsed = JSON.parse(bodyText);
      if (Array.isArray(parsed?.messages) && parsed.messages.length > 0) {
        const url = typeof input === 'string' ? input : (input instanceof URL ? input.href : (input as Request).url);
        let bodyChanged = false;

        for (const msg of parsed.messages) {
          const content = getUserContent(msg);
          if (!content) continue;
          const key = hashContent(content);
          const cached = contentCache.get(key);
          if (cached?.blocked) {
            replaceUserContent(msg, cached.blockText);
            bodyChanged = true;
          }
        }

        const lastUserContent = extractLastUserContent(parsed);
        if (lastUserContent) {
          const key = hashContent(lastUserContent);
          if (!contentCache.has(key)) {
            console.log(`[aliyun-ai-guardrail] LLM request detected -> ${url.slice(0, 80)}, checking content...`);
            try {
              const { blocked, reasons } = await checkContent(lastUserContent);
              if (blocked) {
                const reason = reasons.join('; ');
                const blockText = `[aliyun-ai-guardrail][⚠️ Current user message MUSKED by Aliyun AI Guardrail: ${reason}. Please explain this to the user.]`;
                contentCache.set(key, { blocked: true, blockText });
                console.log(`[aliyun-ai-guardrail] BLOCKED -> ${url}, reason: ${reason}`);
              } else {
                contentCache.set(key, { blocked: false, blockText: '' });
                console.log(`[aliyun-ai-guardrail] PASSED -> ${url.slice(0, 80)}`);
              }
            } catch (err) {
              console.warn(`[aliyun-ai-guardrail] check timeout/error, passing through: ${(err as Error).message}`);
              contentCache.set(key, { blocked: false, blockText: '' });
            }
          }

          const cached = contentCache.get(key);
          if (cached?.blocked) {
            replaceUserContent(parsed.messages.find((m: any) => getUserContent(m) === lastUserContent && m.role === 'user'), cached.blockText);
            bodyChanged = true;
          }
        }

        if (bodyChanged) {
          const newInit = { ...init, body: JSON.stringify(parsed), [SECURITY_MARKER]: true };
          return originalFetch(input, newInit as any);
        }
      }
    }
  } catch (err) {
    const bodyPreview = typeof init?.body === 'string' ? init.body.slice(0, 200) : String(init?.body);
    console.warn(`[aliyun-ai-guardrail] fetch inspect error: ${(err as Error).message}, body: ${bodyPreview}`);
  }

  const markedInit = init ? { ...init, [SECURITY_MARKER]: true } : { [SECURITY_MARKER]: true };
  return originalFetch(input, markedInit as any);
};

globalThis.fetch = patchedFetch;
console.log('[aliyun-ai-guardrail] fetch patched for LLM request interception');

const handler = async (_event: any) => {};

export default handler;
