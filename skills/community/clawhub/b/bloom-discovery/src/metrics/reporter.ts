/**
 * Metrics Reporter (Stub)
 *
 * Sends anonymized usage metrics to POST /api/metrics.
 * Only transmits: skill name + usage frequency.
 *
 * Opt-in only — never sends data without explicit user consent.
 *
 * Stub: logs locally until backend API is ready.
 */

import type { MetricsPayload } from '../types/usecase';
import { collectMetrics } from './collector';

const BLOOM_API_URL =
  process.env.BLOOM_API_URL || 'https://api.bloomprotocol.ai';

/**
 * Report collected metrics to the Bloom API.
 *
 * When backend is ready:
 * - POST /api/metrics { userId, metrics, reportedAt }
 *
 * Current stub: returns success without sending.
 */
export async function reportMetrics(
  userId: string
): Promise<{ success: boolean; message: string }> {
  if (!hasOptedIn()) {
    return {
      success: false,
      message: 'Metrics reporting requires opt-in. Set BLOOM_METRICS_OPTIN=true to enable.',
    };
  }

  const metrics = collectMetrics();

  if (metrics.length === 0) {
    return {
      success: true,
      message: 'No installed skills found. Nothing to report.',
    };
  }

  const payload: MetricsPayload = {
    userId,
    metrics,
    reportedAt: new Date().toISOString(),
  };

  // TODO: Replace with actual API call when backend is ready
  //
  // const response = await fetch(`${BLOOM_API_URL}/api/metrics`, {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify(payload),
  // });
  //
  // if (!response.ok) {
  //   throw new Error(`Metrics report failed: ${response.status}`);
  // }
  //
  // return await response.json();

  console.log(
    `[metrics] Would report ${metrics.length} skill(s) (stub — API not yet available)`
  );

  return {
    success: true,
    message: `Collected ${metrics.length} skill metric(s). API endpoint not yet available — data stays local.`,
  };
}

/**
 * Check if the user has opted in to metrics reporting.
 *
 * Stub: always returns false until opt-in UI is implemented.
 */
export function hasOptedIn(): boolean {
  // TODO: Check user preference from local config or env var
  // e.g. process.env.BLOOM_METRICS_OPTIN === 'true'
  return process.env.BLOOM_METRICS_OPTIN === 'true';
}
