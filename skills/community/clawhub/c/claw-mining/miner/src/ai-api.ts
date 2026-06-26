import type { ChatMessage, AiApiResponse } from './types.js';

export interface AiApiConfig {
  apiKey: string;
  apiUrl: string;
  model: string;
}

const AI_TIMEOUT = 60_000;
// F-12: Limit AI response body to 2 MB to prevent memory exhaustion
const MAX_RESPONSE_BYTES = 2 * 1024 * 1024;

export async function callAiApi(
  config: AiApiConfig,
  messages: ChatMessage[],
): Promise<AiApiResponse> {
  const res = await fetch(config.apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${config.apiKey}`,
    },
    body: JSON.stringify({
      model: config.model,
      messages,
    }),
    signal: AbortSignal.timeout(AI_TIMEOUT),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(`AI API error: ${res.status} ${body}`);
  }

  // F-12: Check Content-Length header and body size
  const contentLength = res.headers.get('content-length');
  if (contentLength && parseInt(contentLength, 10) > MAX_RESPONSE_BYTES) {
    throw new Error(`AI API response too large: ${contentLength} bytes (limit: ${MAX_RESPONSE_BYTES})`);
  }

  const body = await res.text();
  if (body.length > MAX_RESPONSE_BYTES) {
    throw new Error(`AI API response too large: ${body.length} bytes (limit: ${MAX_RESPONSE_BYTES})`);
  }

  return JSON.parse(body) as AiApiResponse;
}
