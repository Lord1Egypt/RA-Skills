import { 
  SemanticDomain, 
  StakingTier, 
  SMFVector, 
  SRIALifecycleState 
} from '../common/types';
import { KeyTriplet } from '../common/crypto';

export { 
  SemanticDomain, 
  StakingTier, 
  SMFVector, 
  SRIALifecycleState, 
  KeyTriplet 
};

export type ExecutionContext = 'SERVER' | 'CLIENT';
export type MessageRole = 'system' | 'user' | 'assistant' | 'tool';

export interface SkillParameterSchema {
  type: 'object';
  properties: Record<string, any>;
  required?: string[];
}

/**
 * A portable definition of a tool with semantic metadata.
 */
export interface SkillDefinition {
  name: string;
  description: string;
  executionLocation: ExecutionContext;
  parameters: SkillParameterSchema;
  version: string;
  
  // AlephNet semantic metadata
  semanticDomain: SemanticDomain;
  primeDomain: number[];
  smfAxes: number[];
  requiredTier: 'Neophyte' | 'Adept' | 'Magus' | 'Archon';
  gasCost?: number;
}

/**
 * The specific instance of a tool call with semantic context.
 */
export interface ToolCallIntent {
  callId: string;
  skillName: string;
  arguments: Record<string, any>;
  timestamp: number;
  status: 'PENDING' | 'CLAIMED' | 'COMPLETED' | 'FAILED';
  target: ExecutionContext;
  
  // AlephNet context
  smfContext: number[];
  resonanceKey: {
    primes: number[];
    hash: string;
    timestamp: number;
  };
  preferredDomain?: SemanticDomain;
}

/**
 * The output of a tool with semantic proof.
 */
export interface ToolResult {
  callId: string;
  output: any;
  isError: boolean;
  timestamp: number;
  executorId: string;
  
  // AlephNet verification
  smfSignature: number[];
  coherenceProof?: {
    tickNumber: number;
    coherence: number;
    smfHash: string;
  };
}

export interface AIProviderConfig {
  alias: string;
  provider: 'openai' | 'anthropic' | 'local-llama' | 'vertex-ai';
  modelName: string;
  contextWindow: number;
}

// KeyTriplet imported from common/crypto

/**
 * DSNNode in the AlephNet-Gun mesh.
 */
export interface DSNNodeConfig {
  // Core identity
  nodeId: string;
  name: string;
  domain: string;
  
  // Gun.js layer
  seaPublicKey: string;
  gunPeers: string[];
  
  // AlephNet layer
  keyTriplet: KeyTriplet;
  semanticDomain: SemanticDomain;
  primeDomain: number[];
  smfAxes: number[];
  sriaCapable: boolean;
  bootstrapUrl: string;
  
  // Capabilities
  status: 'ONLINE' | 'DRAINING' | 'OFFLINE';
  lastHeartbeat: number;
  supportedProviders: AIProviderConfig[];
  hostedSkills: string[];
  loadIndex: number;
  stakingTier: 'Neophyte' | 'Adept' | 'Magus' | 'Archon';
  alephBalance: number;
}

/**
 * Semantic routing decision
 */
export interface RoutingDecision {
  targetNodeId: string;
  relevanceScore: number;
  semanticDomainMatch: boolean;
  primeDomainOverlap: number;
  loadFactor: number;
  fallbackNodes: string[];
}

/**
 * PRRC Channel configuration
 */
export interface PRRCChannelConfig {
  nodeId: string;
  channelId: string;
  primeSet: number[];
  phaseReference: number;
  useExpertiseRouting: boolean;
  relevanceThreshold: number;
}

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: number;
  runId?: string;
  
  // AlephNet semantic data
  smf?: number[];
  resonanceKey?: {
    primes: number[];
    hash: string;
    timestamp: number;
  };
  coherenceProof?: {
    tickNumber: number;
    coherence: number;
    smfHash: string;
  };
}

/**
 * SRIA Session State
 */
export interface SRIASessionState {
  sessionId: string;
  lifecycleState: SRIALifecycleState;
  bodyHash: string;
  quaternionState: { w: number; x: number; y: number; z: number; };
  currentEpoch: number;
  freeEnergy: number;
  entropyTrajectory: number[];
  currentBeliefs: Array<{
    id: string;
    content: string;
    probability: number;
    entropy: number;
    primeFactors: number[];
  }>;
  attention: {
    focusLayer: string;
    layerWeights: Record<string, number>;
    primeAlignments: number[];
  };
}

/**
 * Combined agent brain state
 */
export interface DurableAgentState {
  conversationId: string;
  activeRunId: string | null;
  status: 'IDLE' | 'PROCESSING' | 'AWAITING_CLIENT' | 'AWAITING_SERVER_TOOL';
  assignedServerId: string;
  targetModelAlias: string;
  preferredDomain: SemanticDomain;
  thoughtBuffer: string[];
  pendingTools: Record<string, ToolCallIntent>;
  iterationCount: number;
  maxIterations: number;
  
  // SRIA integration
  sria?: SRIASessionState;
  conversationSmf: number[];
  gmfContributions: string[];
}

export interface AlephMeshGraph {
  nodes: Record<string, DSNNodeConfig>;
  users: Record<string, AlephUserProfile>;
  skills: Record<string, SkillDefinition>;
  conversations: Record<string, ConversationNode>;
  gmf: {
    objects: Record<string, GMFObject>;
    snapshots: Record<string, GMFSnapshot>;
    deltas: GMFDelta[];
  };
  coherence: {
    claims: Record<string, CoherenceClaim>;
    stakes: Record<string, CoherenceStake>;
  };
}

export interface AlephUserProfile {
  alias: string;
  pub: string;
  settings: string;
  alephnet: {
    nodeId: string;
    keyTriplet: KeyTriplet;
    stakingTier: 'Neophyte' | 'Adept' | 'Magus' | 'Archon';
    alephBalance: number;
    reputation: number;
  };
}

export interface ConversationNode {
  metadata: {
    ownerPub: string;
    ownerKeyTriplet: KeyTriplet;
    title: string;
    createdAt: number;
    semanticDomain: SemanticDomain;
    smfSignature: number[];
  };
  messages: Record<string, ChatMessage>;
  state: DurableAgentState;
  toolResults: Record<string, ToolResult>;
  sria?: SRIASessionState;
}

export interface GMFObject {
  id: string;
  semanticObject: { term: any; normalForm: string; };
  weight: number;
  smf: number[];
  insertedAt: number;
  proposalId: string;
  redundancyScore: number;
  metadata: { nodeId: string; consensusAchieved: boolean; };
}

export interface GMFSnapshot {
  id: number;
  timestamp: number;
  objectCount: number;
  hash: string;
}

export interface GMFDelta {
  type: 'insert' | 'update_weight' | 'remove';
  id: string;
  timestamp: number;
  snapshotId: number;
  data?: any;
}

export interface CoherenceClaim {
  id: string;
  title: string;
  content: string;
  submitterId: string;
  smfSignature: number[];
  status: 'PENDING' | 'ACCEPTED' | 'REJECTED' | 'SYNTHESIZED';
  totalStake: number;
  supportStake: number;
  contestStake: number;
  createdAt: number;
}

export interface CoherenceStake {
  id: string;
  claimId: string;
  stakerId: string;
  amount: number;
  vote: 'SUPPORT' | 'CONTEST';
  timestamp: number;
}

export interface AgentTriggerEvent {
  action: 'NEW_MESSAGE' | 'RESUME_FROM_CLIENT_TOOL' | 'SRIA_SUMMON' | 'SRIA_DISMISS';
  conversationId: string;
  
  routing?: {
    targetServer?: string;
    modelAlias?: string;
    preferredDomain?: SemanticDomain;
    requiredSmfAxes?: number[];
    minRelevanceThreshold?: number;
  };
  
  payload?: {
    text?: string;
    toolResult?: any;
    smf?: number[];
    resonanceKey?: { primes: number[]; hash: string; timestamp: number; };
  };
  
  sriaOptions?: {
    summonWithContext?: string;
    dismissAndConsolidate?: boolean;
    contributeToGMF?: boolean;
  };
}

/**
 * Bridge interface
 */
export interface AlephGunBridge {
  initialize(gun: any, dsnNode: any, agentManager: any, embeddingService?: any): Promise<void>;
  authenticate(pair: any): Promise<void>;
  getGun(): any;
  subscribe(path: string, callback: (data: any) => void): () => void;
  put(path: string, data: any): Promise<void>;
  get(path: string): Promise<any>;
  projectToSMF(graphPath: string, data: any): Promise<number[]>;
  routeRequest(event: AgentTriggerEvent): Promise<RoutingDecision>;
  verifyCoherence(proposal: any): Promise<boolean>;
  syncGMFToGraph(): Promise<void>;
  handleSRIAEvent(event: 'summon' | 'dismiss' | 'step', data: any): Promise<any>;
}
