/**
 * Common Type Definitions
 * 
 * Shared types used across the AlephNet codebase.
 * These are foundational types that don't depend on domain-specific logic.
 */

// ═══════════════════════════════════════════════════════════════════════════
// SEMANTIC TYPES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * 16-dimensional Sedenion Memory Field vector.
 * Organized into 4 semantic domains of 4 dimensions each.
 */
export type SMFVector = [
  number, number, number, number,  // Perceptual (0-3): visual, auditory, spatial, motion
  number, number, number, number,  // Cognitive (4-7): logical, emotional, certainty, relevance
  number, number, number, number,  // Temporal (8-11): immediacy, duration, periodicity, causal
  number, number, number, number   // Meta (12-15): self-reference, abstraction, coherence, consensus
];

/**
 * Semantic domain classification
 */
export type SemanticDomain = 'perceptual' | 'cognitive' | 'temporal' | 'meta';

/**
 * SMF axis index (0-15)
 */
export type SMFAxisIndex = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15;

/**
 * Domain range mapping
 */
export const DOMAIN_RANGES: Record<SemanticDomain, [SMFAxisIndex, SMFAxisIndex]> = {
  perceptual: [0, 3],
  cognitive: [4, 7],
  temporal: [8, 11],
  meta: [12, 15]
};

/**
 * SMF axis metadata
 */
export interface SMFAxisInfo {
  name: string;
  domain: SemanticDomain;
  description: string;
}

/**
 * Complete SMF axis mapping
 */
export const SMF_AXES: Record<SMFAxisIndex, SMFAxisInfo> = {
  0: { name: 'visual_salience', domain: 'perceptual', description: 'Visual importance and attention' },
  1: { name: 'auditory_prominence', domain: 'perceptual', description: 'Auditory signal strength' },
  2: { name: 'spatial_orientation', domain: 'perceptual', description: 'Spatial relationship encoding' },
  3: { name: 'motion_change', domain: 'perceptual', description: 'Dynamic/motion components' },
  4: { name: 'logical_complexity', domain: 'cognitive', description: 'Reasoning complexity' },
  5: { name: 'emotional_valence', domain: 'cognitive', description: 'Emotional polarity' },
  6: { name: 'certainty', domain: 'cognitive', description: 'Confidence level' },
  7: { name: 'relevance', domain: 'cognitive', description: 'Contextual relevance' },
  8: { name: 'immediacy', domain: 'temporal', description: 'Urgency/recency' },
  9: { name: 'duration', domain: 'temporal', description: 'Time span' },
  10: { name: 'periodicity', domain: 'temporal', description: 'Cyclical patterns' },
  11: { name: 'causal_weight', domain: 'temporal', description: 'Cause-effect strength' },
  12: { name: 'self_reference', domain: 'meta', description: 'Self-referential degree' },
  13: { name: 'abstraction_level', domain: 'meta', description: 'Concrete to abstract' },
  14: { name: 'coherence', domain: 'meta', description: 'Internal consistency' },
  15: { name: 'network_consensus', domain: 'meta', description: 'Network agreement' }
};

// ═══════════════════════════════════════════════════════════════════════════
// STAKING & ECONOMICS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Staking tier based on token amount
 */
export type StakingTier = 'Neophyte' | 'Adept' | 'Magus' | 'Archon';

/**
 * Tier thresholds in base units (assuming 18 decimals)
 */
export const TIER_THRESHOLDS: Record<StakingTier, bigint> = {
  Neophyte: 0n,
  Adept: 100n * 10n ** 18n,      // 100 tokens
  Magus: 1000n * 10n ** 18n,     // 1,000 tokens
  Archon: 10000n * 10n ** 18n    // 10,000 tokens
};

/**
 * Tier order for comparison
 */
export const TIER_ORDER: StakingTier[] = ['Neophyte', 'Adept', 'Magus', 'Archon'];

/**
 * Lock period options
 */
export type LockPeriod = '7d' | '30d' | '90d' | '180d' | '365d';

/**
 * Lock period to milliseconds mapping
 */
export const LOCK_PERIOD_MS: Record<LockPeriod, number> = {
  '7d': 7 * 24 * 60 * 60 * 1000,
  '30d': 30 * 24 * 60 * 60 * 1000,
  '90d': 90 * 24 * 60 * 60 * 1000,
  '180d': 180 * 24 * 60 * 60 * 1000,
  '365d': 365 * 24 * 60 * 60 * 1000
};

// ═══════════════════════════════════════════════════════════════════════════
// LIFECYCLE & STATUS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Node operational status
 */
export type NodeStatus = 'ONLINE' | 'DRAINING' | 'OFFLINE';

/**
 * Agent processing status
 */
export type AgentStatus = 'IDLE' | 'PROCESSING' | 'AWAITING_CLIENT' | 'AWAITING_SERVER_TOOL';

/**
 * SRIA lifecycle states
 */
export type SRIALifecycleState = 
  'DORMANT' | 'PERCEIVING' | 'DECIDING' | 'ACTING' | 'LEARNING' | 
  'CONSOLIDATING' | 'SLEEPING';

/**
 * Service instance status
 */
export type ServiceStatus = 'STARTING' | 'RUNNING' | 'DRAINING' | 'STOPPED' | 'ERROR';

/**
 * Task execution status
 */
export type TaskStatus = 
  'PENDING' | 'VALIDATING' | 'RUNNING' | 'AWAITING_SERVICE' | 
  'COMPLETED' | 'FAILED' | 'CANCELLED' | 'TIMEOUT';

// ═══════════════════════════════════════════════════════════════════════════
// PRIME NUMBER UTILITIES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * First 16 primes used for semantic encoding
 */
export const PRIMES_16 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53] as const;

/**
 * Extended primes for various operations
 */
export const PRIMES_100 = [
  2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
  73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
  157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
  239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
  331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
  421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
  509, 521, 523, 541
] as const;

// ═══════════════════════════════════════════════════════════════════════════
// GENERIC UTILITY TYPES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Make specific properties required
 */
export type RequireFields<T, K extends keyof T> = T & Required<Pick<T, K>>;

/**
 * Make all properties optional except specified ones
 */
export type PartialExcept<T, K extends keyof T> = Partial<T> & Pick<T, K>;

/**
 * Deep readonly
 */
export type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

/**
 * Timestamp type alias for clarity
 */
export type Timestamp = number;

/**
 * UUID string type
 */
export type UUID = string;

/**
 * Base64 encoded string
 */
export type Base64 = string;

/**
 * Hex encoded string
 */
export type HexString = string;

/**
 * Callback function type
 */
export type Callback<T = void> = (error: Error | null, result?: T) => void;

/**
 * Async function that returns a value
 */
export type AsyncFn<T, R> = (input: T) => Promise<R>;

/**
 * Disposable resource pattern
 */
export interface Disposable {
  dispose(): void | Promise<void>;
}

/**
 * Initializable component pattern
 */
export interface Initializable {
  initialize(): Promise<void>;
  isInitialized(): boolean;
}

export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  lastCheck: number;
  details?: Record<string, any>;
}

/**
 * Health check pattern
 */
export interface HealthCheckable {
  healthCheck(): Promise<HealthStatus>;
}


// ═══════════════════════════════════════════════════════════════════════════
// DOMAIN SYSTEM
// ═══════════════════════════════════════════════════════════════════════════

export type DomainVisibility = 'public' | 'private' | 'secret';
export type DomainRole = 'owner' | 'admin' | 'member' | 'guest';
export type MembershipStatus = 'pending' | 'active' | 'suspended' | 'banned';

export interface DomainRules {
  minStakingTier: StakingTier;
  minReputation: number;
  requiresApproval: boolean;
  whitelist?: string[];
  blacklist?: string[];
  grantedCapabilities: string[];
}

export interface DomainDefinition {
  id: string;
  handle: string;
  name: string;
  description: string;
  ownerId: string;
  createdAt: number;
  visibility: DomainVisibility;
  rules: DomainRules;
  metadata: Record<string, unknown>;
}

export interface DomainMembership {
  domainId: string;
  userId: string;
  role: DomainRole;
  status: MembershipStatus;
  joinedAt: number;
  approvedBy?: string;
}
