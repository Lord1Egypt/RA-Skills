/**
 * Claim SBT (Stub)
 *
 * Handles the claim flow for verified use case configurations.
 * Calls POST /api/claim on the backend.
 *
 * Stub: returns web link fallback until backend API is ready.
 */

import type { ClaimRequest, ClaimResponse } from '../types/usecase';

const BLOOM_API_URL =
  process.env.BLOOM_API_URL || 'https://api.bloomprotocol.ai';
const DASHBOARD_URL =
  process.env.DASHBOARD_URL || 'https://bloomprotocol.ai';

/**
 * Submit a claim for a verified use case configuration.
 *
 * When backend is ready:
 * - POST /api/claim { useCaseId, walletAddress }
 * - Returns mint tx hash (if wallet) or web link (if no wallet)
 *
 * Current stub: always returns web link.
 */
export async function claimSBT(
  request: ClaimRequest
): Promise<ClaimResponse> {
  // TODO: Replace with actual API call when backend is ready
  //
  // const response = await fetch(`${BLOOM_API_URL}/api/claim`, {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify(request),
  // });
  // return await response.json();

  const webUrl = `${DASHBOARD_URL}/claim/${encodeURIComponent(request.useCaseId)}`;

  if (request.walletAddress) {
    return {
      success: true,
      method: 'web-link',
      webUrl,
      message:
        `Claim API not yet available. Visit ${webUrl} to claim your SBT ` +
        `with wallet ${request.walletAddress}.`,
    };
  }

  return {
    success: true,
    method: 'web-link',
    webUrl,
    message: `Visit ${webUrl} to claim your SBT. Connect a wallet on the page to mint.`,
  };
}

/**
 * Check if a use case has already been claimed by this user.
 *
 * Stub: always returns false until backend is ready.
 */
export async function isAlreadyClaimed(
  _useCaseId: string,
  _userId: string
): Promise<boolean> {
  // TODO: GET /api/claim/status?useCaseId=X&userId=Y
  return false;
}
