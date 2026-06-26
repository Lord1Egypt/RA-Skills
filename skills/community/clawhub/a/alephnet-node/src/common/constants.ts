/**
 * Application Constants
 * 
 * Centralized constants for the AlephNet application.
 * These are shared across all modules.
 */

// ═══════════════════════════════════════════════════════════════════════════
// NETWORK CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Default network configuration
 */
export const NETWORK = {
  /** Default bootstrap URL */
  DEFAULT_BOOTSTRAP_URL: 'https://bootstrap.alephnet.com',
  
  /** Default Gun.js relay peers */
  DEFAULT_GUN_PEERS: [
    'https://gun-relay1.alephnet.com/gun',
    'https://gun-relay2.alephnet.com/gun'
  ],
  
  /** Heartbeat interval in milliseconds */
  HEARTBEAT_INTERVAL_MS: 30000,
  
  /** Node timeout (considered offline after this) */
  NODE_TIMEOUT_MS: 90000,
  
  /** Default request timeout */
  REQUEST_TIMEOUT_MS: 30000,
  
  /** Maximum number of peers to connect to */
  MAX_PEERS: 50,
  
  /** Minimum peers for mesh quorum */
  MIN_PEERS_QUORUM: 3
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// CONSENSUS CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

export const CONSENSUS = {
  /** Minimum coherence score for proposal acceptance */
  MIN_COHERENCE_THRESHOLD: 0.7,
  
  /** Required support ratio for consensus (2/3 majority) */
  CONSENSUS_THRESHOLD: 0.66,
  
  /** Minimum stake for voting */
  MIN_VOTE_STAKE: 10,
  
  /** Proposal timeout in milliseconds */
  PROPOSAL_TIMEOUT_MS: 60000,
  
  /** Vote collection window */
  VOTE_WINDOW_MS: 30000
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// SRIA CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

export const SRIA = {
  /** Initial free energy */
  INITIAL_FREE_ENERGY: 1.0,
  
  /** Free energy threshold for consolidation */
  CONSOLIDATION_THRESHOLD: 0.1,
  
  /** Maximum iterations per cycle */
  MAX_ITERATIONS: 100,
  
  /** Learning rate for belief updates */
  LEARNING_RATE: 0.1,
  
  /** Entropy decay factor */
  ENTROPY_DECAY: 0.95,
  
  /** Attention focus decay */
  ATTENTION_DECAY: 0.9
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// EMBEDDING CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

export const EMBEDDING = {
  /** OpenAI embedding model */
  OPENAI_MODEL: 'text-embedding-3-small',
  
  /** Native embedding dimensions (OpenAI) */
  NATIVE_DIMENSIONS: 1536,
  
  /** SMF target dimensions */
  SMF_DIMENSIONS: 16,
  
  /** Maximum text length for embedding */
  MAX_TEXT_LENGTH: 8192,
  
  /** Cache TTL in milliseconds (7 days) */
  CACHE_TTL_MS: 7 * 24 * 60 * 60 * 1000,
  
  /** Batch size for batch embedding */
  BATCH_SIZE: 100
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// TASK CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

export const TASK = {
  /** Default maximum concurrent tasks */
  DEFAULT_MAX_CONCURRENT: 5,
  
  /** Default retry attempts */
  DEFAULT_RETRY_ATTEMPTS: 3,
  
  /** Default retry backoff base */
  DEFAULT_BACKOFF_MS: 1000,
  
  /** Default retry backoff multiplier */
  DEFAULT_BACKOFF_MULTIPLIER: 2,
  
  /** Scheduler poll interval */
  SCHEDULER_INTERVAL_MS: 60000,
  
  /** Task timeout */
  TASK_TIMEOUT_MS: 300000
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// SERVICE CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

export const SERVICE = {
  /** Default rate limit per minute */
  DEFAULT_RATE_LIMIT_PER_MINUTE: 60,
  
  /** Default rate limit per hour */
  DEFAULT_RATE_LIMIT_PER_HOUR: 1000,
  
  /** Default rate limit per day */
  DEFAULT_RATE_LIMIT_PER_DAY: 10000,
  
  /** Health check interval */
  HEALTH_CHECK_INTERVAL_MS: 30000,
  
  /** SLA uptime guarantee default */
  DEFAULT_UPTIME_GUARANTEE: 0.99,
  
  /** Default max response time */
  DEFAULT_MAX_RESPONSE_MS: 5000,
  
  /** Registration fee (in base units) */
  REGISTRATION_FEE: 10
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// WALLET CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

export const WALLET = {
  /** Token decimals */
  TOKEN_DECIMALS: 18,
  
  /** One token in base units */
  ONE_TOKEN: 10n ** 18n,
  
  /** Minimum transfer amount */
  MIN_TRANSFER: 1n,
  
  /** Payment authorization expiry (1 minute) */
  PAYMENT_AUTH_EXPIRY_MS: 60000,
  
  /** Unstake lock periods in days */
  UNSTAKE_LOCK_DAYS: {
    IMMEDIATE: 7,
    STANDARD: 14,
    EXTENDED: 30
  },
  
  /** Revenue distribution percentages */
  REVENUE_DISTRIBUTION: {
    PROVIDER: 70,
    NETWORK: 20,
    STAKERS: 10
  }
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// ERROR CODES
// ═══════════════════════════════════════════════════════════════════════════

export const ERROR_CODES = {
  // Network errors (1xxx)
  E_NETWORK_TIMEOUT: 'E1001',
  E_NETWORK_UNREACHABLE: 'E1002',
  E_NETWORK_PEER_DISCONNECT: 'E1003',
  
  // Consensus errors (2xxx)
  E_CONSENSUS_TIMEOUT: 'E2001',
  E_CONSENSUS_NO_QUORUM: 'E2002',
  E_CONSENSUS_INVALID_PROOF: 'E2003',
  
  // SRIA errors (3xxx)
  E_SRIA_TIMEOUT: 'E3001',
  E_SRIA_SESSION_NOT_FOUND: 'E3002',
  E_SRIA_INVALID_STATE: 'E3003',
  
  // Service errors (4xxx)
  E_SERVICE_UNAVAILABLE: 'E4001',
  E_SERVICE_NOT_FOUND: 'E4002',
  E_SERVICE_RATE_LIMIT: 'E4003',
  E_SERVICE_PAYMENT_FAILED: 'E4004',
  
  // Storage errors (5xxx)
  E_STORAGE_NOT_FOUND: 'E5001',
  E_STORAGE_WRITE_FAILED: 'E5002',
  E_STORAGE_INTEGRITY: 'E5003',
  
  // Auth errors (6xxx)
  E_AUTH_INVALID_KEY: 'E6001',
  E_AUTH_PERMISSION_DENIED: 'E6002',
  E_AUTH_SIGNATURE_INVALID: 'E6003',
  E_AUTH_TIER_REQUIRED: 'E6004',
  
  // Validation errors (7xxx)
  E_VALIDATION_SCHEMA: 'E7001',
  E_VALIDATION_SMF: 'E7002',
  E_VALIDATION_INPUT: 'E7003',
  
  // Resource errors (8xxx)
  E_RESOURCE_EXHAUSTED: 'E8001',
  E_RESOURCE_NOT_AVAILABLE: 'E8002',
  
  // Internal errors (9xxx)
  E_INTERNAL_UNKNOWN: 'E9001',
  E_INTERNAL_CONFIG: 'E9002'
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// EVENT TYPES
// ═══════════════════════════════════════════════════════════════════════════

export const EVENT_TYPES = {
  // Agent events
  AGENT_TRIGGER: 'agent.trigger',
  AGENT_RESPONSE: 'agent.response',
  AGENT_ERROR: 'agent.error',
  
  // SRIA events
  SRIA_SUMMON: 'sria.summon',
  SRIA_DISMISS: 'sria.dismiss',
  SRIA_STEP: 'sria.step',
  SRIA_CONSOLIDATE: 'sria.consolidate',
  
  // Task events
  TASK_SCHEDULED: 'task.scheduled',
  TASK_STARTED: 'task.started',
  TASK_COMPLETED: 'task.completed',
  TASK_FAILED: 'task.failed',
  
  // Service events
  SERVICE_REGISTERED: 'service.registered',
  SERVICE_CALLED: 'service.called',
  SERVICE_HEALTH: 'service.health',
  
  // Consensus events
  CONSENSUS_PROPOSAL: 'consensus.proposal',
  CONSENSUS_VOTE: 'consensus.vote',
  CONSENSUS_RESULT: 'consensus.result',
  
  // GMF events
  GMF_INSERT: 'gmf.insert',
  GMF_UPDATE: 'gmf.update',
  GMF_SNAPSHOT: 'gmf.snapshot',
  
  // System events
  SYSTEM_STARTUP: 'system.startup',
  SYSTEM_SHUTDOWN: 'system.shutdown',
  SYSTEM_ERROR: 'system.error'
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// TIER MULTIPLIERS
// ═══════════════════════════════════════════════════════════════════════════

export const TIER_MULTIPLIERS = {
  /** Vote weight multipliers by tier */
  VOTE_WEIGHT: {
    Neophyte: 1,
    Adept: 2,
    Magus: 5,
    Archon: 10
  },
  
  /** Reward multipliers by tier */
  REWARD: {
    Neophyte: 1,
    Adept: 1.5,
    Magus: 2.5,
    Archon: 4
  },
  
  /** Rate limit multipliers by tier */
  RATE_LIMIT: {
    Neophyte: 1,
    Adept: 2,
    Magus: 5,
    Archon: 10
  }
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// LOGGING LEVELS
// ═══════════════════════════════════════════════════════════════════════════

export const LOG_LEVELS = {
  TRACE: 0,
  DEBUG: 1,
  INFO: 2,
  WARN: 3,
  ERROR: 4,
  FATAL: 5
} as const;

export type LogLevel = keyof typeof LOG_LEVELS;
