import { 
    GMFObject, 
    GMFSnapshot, 
    GMFDelta, 
    CoherenceClaim, 
    CoherenceStake 
} from '../core/types';
import { 
    Validator, 
    validateObject, 
    validateArray, 
    isString, 
    isNumber, 
    validateEnum,
    validateSMFVector
} from './ValidationUtils';

export const GMFObjectSchema: Validator<GMFObject> = (data) => validateObject(data, {
    id: (v) => ({ valid: isString(v) }),
    semanticObject: (v) => validateObject(v, {
        term: (t) => ({ valid: true }), // Any
        normalForm: (s) => ({ valid: isString(s) })
    }),
    weight: (v) => ({ valid: isNumber(v) }),
    smf: validateSMFVector,
    insertedAt: (v) => ({ valid: isNumber(v) }),
    proposalId: (v) => ({ valid: isString(v) }),
    redundancyScore: (v) => ({ valid: isNumber(v) }),
    metadata: (v) => validateObject(v, {
        nodeId: (s) => ({ valid: isString(s) }),
        consensusAchieved: (b) => ({ valid: typeof b === 'boolean' })
    })
});

export const GMFSnapshotSchema: Validator<GMFSnapshot> = (data) => validateObject(data, {
    id: (v) => ({ valid: isNumber(v) }),
    timestamp: (v) => ({ valid: isNumber(v) }),
    objectCount: (v) => ({ valid: isNumber(v) }),
    hash: (v) => ({ valid: isString(v) })
});

export const GMFDeltaSchema: Validator<GMFDelta> = (data) => validateObject(data, {
    type: validateEnum(['insert', 'update_weight', 'remove']),
    id: (v) => ({ valid: isString(v) }),
    timestamp: (v) => ({ valid: isNumber(v) }),
    snapshotId: (v) => ({ valid: isNumber(v) }),
    data: (v) => ({ valid: true }) // Optional/Any
}, ['data']);

export const CoherenceClaimSchema: Validator<CoherenceClaim> = (data) => validateObject(data, {
    id: (v) => ({ valid: isString(v) }),
    title: (v) => ({ valid: isString(v) }),
    content: (v) => ({ valid: isString(v) }),
    submitterId: (v) => ({ valid: isString(v) }),
    smfSignature: validateSMFVector,
    status: validateEnum(['PENDING', 'ACCEPTED', 'REJECTED', 'SYNTHESIZED']),
    totalStake: (v) => ({ valid: isNumber(v) }),
    supportStake: (v) => ({ valid: isNumber(v) }),
    contestStake: (v) => ({ valid: isNumber(v) }),
    createdAt: (v) => ({ valid: isNumber(v) })
});

export const CoherenceStakeSchema: Validator<CoherenceStake> = (data) => validateObject(data, {
    id: (v) => ({ valid: isString(v) }),
    claimId: (v) => ({ valid: isString(v) }),
    stakerId: (v) => ({ valid: isString(v) }),
    amount: (v) => ({ valid: isNumber(v) }),
    vote: validateEnum(['SUPPORT', 'CONTEST']),
    timestamp: (v) => ({ valid: isNumber(v) })
});
