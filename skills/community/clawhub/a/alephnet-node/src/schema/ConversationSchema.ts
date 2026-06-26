import { 
    ConversationNode, 
    ChatMessage, 
    DurableAgentState, 
    ToolResult, 
    SRIASessionState 
} from '../core/types';
import {
    Validator,
    validateObject,
    validateArray,
    isString,
    isNumber,
    isBoolean,
    isObject,
    validateEnum,
    validateSMFVector
} from './ValidationUtils';

// --- Sub-Schemas ---

const ResonanceKeySchema: Validator<any> = (data) => validateObject(data, {
    primes: (v) => validateArray(v, (p) => ({ valid: isNumber(p) })),
    hash: (v) => ({ valid: isString(v) }),
    timestamp: (v) => ({ valid: isNumber(v) })
});

const CoherenceProofSchema: Validator<any> = (data) => validateObject(data, {
    tickNumber: (v) => ({ valid: isNumber(v) }),
    coherence: (v) => ({ valid: isNumber(v) }),
    smfHash: (v) => ({ valid: isString(v) })
});

const ChatMessageSchema: Validator<ChatMessage> = (data) => validateObject(data, {
    id: (v) => ({ valid: isString(v) }),
    role: validateEnum(['system', 'user', 'assistant', 'tool']),
    content: (v) => ({ valid: isString(v) }),
    timestamp: (v) => ({ valid: isNumber(v) }),
    runId: (v) => ({ valid: isString(v) }),
    
    smf: validateSMFVector,
    resonanceKey: ResonanceKeySchema,
    coherenceProof: CoherenceProofSchema
}, ['runId', 'smf', 'resonanceKey', 'coherenceProof']);

const SRIASessionStateSchema: Validator<SRIASessionState> = (data) => validateObject(data, {
    sessionId: (v) => ({ valid: isString(v) }),
    lifecycleState: validateEnum(['DORMANT', 'PERCEIVING', 'DECIDING', 'ACTING', 'LEARNING', 'CONSOLIDATING', 'SLEEPING']),
    bodyHash: (v) => ({ valid: isString(v) }),
    quaternionState: (v) => validateObject(v, {
        w: (n) => ({ valid: isNumber(n) }),
        x: (n) => ({ valid: isNumber(n) }),
        y: (n) => ({ valid: isNumber(n) }),
        z: (n) => ({ valid: isNumber(n) })
    }),
    currentEpoch: (v) => ({ valid: isNumber(v) }),
    freeEnergy: (v) => ({ valid: isNumber(v) }),
    entropyTrajectory: (v) => validateArray(v, (n) => ({ valid: isNumber(n) })),
    currentBeliefs: (v) => validateArray(v, (b: any) => validateObject(b, {
        id: (s) => ({ valid: isString(s) }),
        content: (s) => ({ valid: isString(s) }),
        probability: (n) => ({ valid: isNumber(n) }),
        entropy: (n) => ({ valid: isNumber(n) }),
        primeFactors: (arr) => validateArray(arr, (n) => ({ valid: isNumber(n) }))
    })),
    attention: (v) => validateObject(v, {
        focusLayer: (s) => ({ valid: isString(s) }),
        layerWeights: (o) => ({ valid: isObject(o) }), // Simplified
        primeAlignments: (a) => validateArray(a, (n) => ({ valid: isNumber(n) }))
    })
});

const ToolResultSchema: Validator<ToolResult> = (data) => validateObject(data, {
    callId: (v) => ({ valid: isString(v) }),
    output: (v) => ({ valid: true }), // Any
    isError: (v) => ({ valid: isBoolean(v) }),
    timestamp: (v) => ({ valid: isNumber(v) }),
    executorId: (v) => ({ valid: isString(v) }),
    smfSignature: validateSMFVector,
    coherenceProof: CoherenceProofSchema
}, ['coherenceProof']);

const DurableAgentStateSchema: Validator<DurableAgentState> = (data) => validateObject(data, {
    conversationId: (v) => ({ valid: isString(v) }),
    activeRunId: (v) => ({ valid: v === null || isString(v) }),
    status: validateEnum(['IDLE', 'PROCESSING', 'AWAITING_CLIENT', 'AWAITING_SERVER_TOOL']),
    assignedServerId: (v) => ({ valid: isString(v) }),
    targetModelAlias: (v) => ({ valid: isString(v) }),
    preferredDomain: validateEnum(['perceptual', 'cognitive', 'temporal', 'meta']),
    thoughtBuffer: (v) => validateArray(v, (s) => ({ valid: isString(s) })),
    pendingTools: (v) => ({ valid: isObject(v) }), // Detailed validation of map omitted for brevity
    iterationCount: (v) => ({ valid: isNumber(v) }),
    maxIterations: (v) => ({ valid: isNumber(v) }),
    
    sria: SRIASessionStateSchema,
    conversationSmf: validateSMFVector,
    gmfContributions: (v) => validateArray(v, (s) => ({ valid: isString(s) }))
}, ['sria']);

// --- Main Schema ---

export const ConversationNodeSchema: Validator<ConversationNode> = (data) => validateObject(data, {
    metadata: (v) => validateObject(v, {
        ownerPub: (s) => ({ valid: isString(s) }),
        // ownerKeyTriplet check omitted to avoid circular dep or just simplify
        title: (s) => ({ valid: isString(s) }),
        createdAt: (n) => ({ valid: isNumber(n) }),
        semanticDomain: validateEnum(['perceptual', 'cognitive', 'temporal', 'meta']),
        smfSignature: validateSMFVector
    }, ['ownerKeyTriplet']), // Marked optional here just for simplicity of this validator
    
    messages: (v) => ({ valid: isObject(v) }), // Should validate values as ChatMessage
    state: DurableAgentStateSchema,
    toolResults: (v) => ({ valid: isObject(v) }),
    sria: SRIASessionStateSchema
}, ['sria']);
