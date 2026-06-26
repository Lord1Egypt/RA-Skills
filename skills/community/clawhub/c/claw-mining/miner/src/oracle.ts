import type { AttestRequest, AttestSuccessResponse, NonceResponse, OracleErrorResponse } from './types.js';

const NONCE_TIMEOUT = 30_000;
const ATTEST_TIMEOUT = 30_000;

export async function getNonce(
  oracleUrl: string,
  minerAddress: string,
): Promise<{ nonce: string; expires_at: number }> {
  const url = `${oracleUrl}/api/v1/nonce?miner=${minerAddress}`;
  const res = await fetch(url, { signal: AbortSignal.timeout(NONCE_TIMEOUT) });
  const data = await res.json() as NonceResponse | OracleErrorResponse;

  if (!data.success) {
    const err = data as OracleErrorResponse;
    throw new Error(`Oracle nonce error: ${err.error} - ${err.message}`);
  }

  const nonceData = data as NonceResponse;

  // F-05: Validate nonce format — must match Oracle pattern: CLAW-{hex8}-{timestamp}
  const NONCE_RE = /^CLAW-[0-9a-f]{8}-\d{10}$/;
  if (typeof nonceData.nonce !== 'string' || !NONCE_RE.test(nonceData.nonce)) {
    throw new Error(`Oracle returned invalid nonce format: ${String(nonceData.nonce).slice(0, 60)}`);
  }

  return { nonce: nonceData.nonce, expires_at: nonceData.expires_at };
}

export async function submitAttestation(
  oracleUrl: string,
  request: AttestRequest,
): Promise<AttestSuccessResponse> {
  const url = `${oracleUrl}/api/v1/attest`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
    signal: AbortSignal.timeout(ATTEST_TIMEOUT),
  });

  const data = await res.json() as AttestSuccessResponse | OracleErrorResponse;

  if (!data.success) {
    const err = data as OracleErrorResponse;
    throw new Error(`Oracle attest error: ${err.error} - ${err.message}`);
  }

  return data as AttestSuccessResponse;
}

export async function checkOracleHealth(oracleUrl: string): Promise<boolean> {
  try {
    const res = await fetch(`${oracleUrl}/health`, { signal: AbortSignal.timeout(5000) });
    const data = await res.json() as { status: string };
    return data.status === 'ok';
  } catch {
    return false;
  }
}
