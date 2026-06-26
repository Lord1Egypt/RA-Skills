/**
 * SRIA Engine - Legacy re-export
 * 
 * This file re-exports from the new modular SRIA implementation
 * for backward compatibility.
 * 
 * @deprecated Import directly from './sria' instead
 */

import { SRIALifecycleState } from '../common/types';
import { Quaternion } from '../common/math';

export { SRIAEngine } from './sria/SRIAEngine';
export { SRIALifecycleState, Quaternion };
export type { 
  SRIASessionState,
  BeliefState,
  Policy,
  PolicyType,
  ActionOutcome,
  GenerativeModelParams,
  AttentionState,
  Prediction,
  SRIAEvent,
  SRIAEventHandler
} from './sria/types';
