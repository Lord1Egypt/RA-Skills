/** Chat message for OpenAI-compatible API */
export interface ChatMessage {
  role: string;
  content: string;
}

/** OpenAI-compatible chat completion response */
export interface AiApiResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    message: { role: string; content: string };
    finish_reason: string;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

/** Oracle attest request body (matches Oracle server's AttestRequest) */
export interface AttestRequest {
  miner_address: string;
  nonce: string;
  api_response: AiApiResponse;
  api_request: {
    model: string;
    messages: ChatMessage[];
  };
  seed_epoch: number;
  seed: string;
  claim_index: number;
}

/** Attestation data from Oracle */
export interface Attestation {
  miner_address: string;
  model_hash: string;
  total_tokens: number;
  seed_epoch: number;
  seed: string;
  claim_index: number;
  deadline: number;
  signature: string;
}

/** Oracle attest success response */
export interface AttestSuccessResponse {
  success: true;
  attestation: Attestation;
  estimated_reward: string;
}

/** Oracle error response */
export interface OracleErrorResponse {
  success: false;
  error: string;
  message: string;
}

/** Oracle nonce response */
export interface NonceResponse {
  success: true;
  nonce: string;
  expires_at: number;
  message: string;
}

/** On-chain state snapshot */
export interface ChainState {
  currentEra: bigint;
  currentGlobalEpoch: bigint;
  currentSeed: bigint;
  seedEpoch: bigint;
  eraModelHash: string;
  currentBlock: number;
}

/** Miner-specific on-chain state */
export interface MinerChainState {
  cooldownRemaining: bigint;
  epochClaimCount: bigint;
  maxClaimsPerEpoch: bigint;
  ethBalance: bigint;
}

/** Parameters for a single mine operation */
export interface MineParams {
  chainState: ChainState;
  minerState: MinerChainState;
  nonce: string;
  claimIndex: number;
  seedHex: string;
}
