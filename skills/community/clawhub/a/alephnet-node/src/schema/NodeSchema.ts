import { DSNNodeConfig, KeyTriplet, AIProviderConfig } from '../core/types';
import { 
    Validator, 
    validateObject, 
    validateArray, 
    isString, 
    isNumber, 
    isBoolean,
    validateEnum,
    validateSMFVector
} from './ValidationUtils';

// --- Sub-Schemas ---

const KeyTripletSchema: Validator<KeyTriplet> = (data) => validateObject(data, {
    pub: (v) => ({ valid: isString(v) }),
    resonance: validateSMFVector,
    fingerprint: (v) => ({ valid: isString(v) }),
    bodyPrimes: (v) => validateArray(v, (p) => ({ valid: isNumber(p) }))
}, ['bodyPrimes']);

const AIProviderConfigSchema: Validator<AIProviderConfig> = (data) => validateObject(data, {
    alias: (v) => ({ valid: isString(v) }),
    provider: validateEnum(['openai', 'anthropic', 'local-llama', 'vertex-ai']),
    modelName: (v) => ({ valid: isString(v) }),
    contextWindow: (v) => ({ valid: isNumber(v) })
});

// --- Main Schema ---

export const DSNNodeSchema: Validator<DSNNodeConfig> = (data) => validateObject(data, {
    nodeId: (v) => ({ valid: isString(v) }),
    name: (v) => ({ valid: isString(v) }),
    domain: (v) => ({ valid: isString(v) }),
    
    seaPublicKey: (v) => ({ valid: isString(v) }),
    gunPeers: (v) => validateArray(v, (p) => ({ valid: isString(p) })),
    
    keyTriplet: KeyTripletSchema,
    semanticDomain: validateEnum(['perceptual', 'cognitive', 'temporal', 'meta']),
    primeDomain: (v) => validateArray(v, (p) => ({ valid: isNumber(p) })),
    smfAxes: (v) => validateArray(v, (p) => ({ valid: isNumber(p) })),
    sriaCapable: (v) => ({ valid: isBoolean(v) }),
    bootstrapUrl: (v) => ({ valid: isString(v) }),
    
    status: validateEnum(['ONLINE', 'DRAINING', 'OFFLINE']),
    lastHeartbeat: (v) => ({ valid: isNumber(v) }),
    supportedProviders: (v) => validateArray(v, AIProviderConfigSchema),
    hostedSkills: (v) => validateArray(v, (s) => ({ valid: isString(s) })),
    loadIndex: (v) => ({ valid: isNumber(v) }),
    stakingTier: validateEnum(['Neophyte', 'Adept', 'Magus', 'Archon']),
    alephBalance: (v) => ({ valid: isNumber(v) })
});
