/**
 * EIP-191 signing for Clabcraw game requests.
 *
 * Signs the message: "{game_id}:{canonical_json}:{timestamp}"
 * using viem's signMessage (EIP-191 personal_sign).
 *
 * JSON keys MUST be sorted alphabetically to match the server's
 * Jason.encode! output (Elixir sorts map keys by default).
 */

/**
 * Sign a game action with EIP-191.
 *
 * @param {import('viem/accounts').PrivateKeyAccount} account - viem account
 * @param {string} gameId - Game UUID
 * @param {object} actionBody - Action payload (e.g., {action: "raise", amount: 800})
 * @param {string} timestamp - Unix timestamp as string
 * @returns {Promise<string>} Hex signature (0x-prefixed)
 */
export async function signAction(account, gameId, actionBody, timestamp) {
  const message = buildMessage(gameId, actionBody, timestamp);
  const signature = await account.signMessage({ message });
  return signature;
}

/**
 * Sign a game state read request with EIP-191.
 *
 * @param {import('viem/accounts').PrivateKeyAccount} account - viem account
 * @param {string} gameId - Game UUID
 * @param {string} timestamp - Unix timestamp as string
 * @returns {Promise<string>} Hex signature (0x-prefixed)
 */
export async function signState(account, gameId, timestamp) {
  return signAction(account, gameId, { action: "state" }, timestamp);
}

/**
 * Sign a queue cancellation request with EIP-191.
 * Message format: "cancel-queue:{gameId}:{timestamp}"
 * Distinct prefix prevents replaying cancel signatures as action/state requests.
 *
 * @param {import('viem/accounts').PrivateKeyAccount} account - viem account
 * @param {string} gameId - Game UUID
 * @param {string} timestamp - Unix timestamp as string
 * @returns {Promise<string>} Hex signature (0x-prefixed)
 */
export async function signCancel(account, gameId, timestamp) {
  const message = `cancel-queue:${gameId}:${timestamp}`;
  return account.signMessage({ message });
}

/**
 * Produce canonical JSON matching Elixir's Jason.encode!/1.
 * Keys are sorted alphabetically, no whitespace.
 */
function canonicalize(obj) {
  const sorted = Object.fromEntries(
    Object.entries(obj).sort(([a], [b]) => a.localeCompare(b))
  );
  return JSON.stringify(sorted);
}

function buildMessage(gameId, payload, timestamp) {
  const canonicalJson = canonicalize(payload);
  return `${gameId}:${canonicalJson}:${timestamp}`;
}
