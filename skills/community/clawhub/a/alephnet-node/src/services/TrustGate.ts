import type {
  Capability,
  CapabilityCheckResult,
  CapabilityDecision,
  ITrustEvaluator,
  ITrustGate,
  SignedEnvelope,
  TrustAssessment,
  TrustLevel,
} from '../common/trust-types';

type RiskLevel = 'low' | 'medium' | 'high' | 'critical';

interface MatrixRule {
  decision: CapabilityDecision;
  risk?: RiskLevel;
}

const DEFAULT_RULES: Record<TrustLevel, MatrixRule> = {
  SELF: { decision: 'ALLOW' },
  VOUCHED: { decision: 'CONFIRM', risk: 'medium' },
  COMMUNITY: { decision: 'CONFIRM', risk: 'high' },
  UNKNOWN: { decision: 'DENY' },
  REVOKED: { decision: 'DENY' },
};

const CAPABILITY_MATRIX: Partial<Record<Capability, Partial<Record<TrustLevel, MatrixRule>>>> = {
  'ui:notification': {
    // SELF: ALLOW (default)
    // VOUCHED: ALLOW (override default confirm)
    VOUCHED: { decision: 'ALLOW' },
    // COMMUNITY: ALLOW (override default confirm)
    COMMUNITY: { decision: 'ALLOW' },
    UNKNOWN: { decision: 'CONFIRM', risk: 'low' },
    // REVOKED: DENY (default)
  },
  'ui:overlay': {
    VOUCHED: { decision: 'ALLOW' },
    COMMUNITY: { decision: 'ALLOW' },
    UNKNOWN: { decision: 'CONFIRM', risk: 'low' },
  },
  'network:http': {
    // SELF: ALLOW (default)
    VOUCHED: { decision: 'ALLOW' },
    COMMUNITY: { decision: 'CONFIRM', risk: 'medium' },
    UNKNOWN: { decision: 'CONFIRM', risk: 'high' },
  },
  'fs:read': {
    VOUCHED: { decision: 'ALLOW' },
    COMMUNITY: { decision: 'CONFIRM', risk: 'medium' },
    UNKNOWN: { decision: 'CONFIRM', risk: 'high' },
  },
  'fs:write': {
    // SELF: ALLOW (default)
    VOUCHED: { decision: 'CONFIRM', risk: 'medium' }, // Matches default
    COMMUNITY: { decision: 'CONFIRM', risk: 'high' }, // Matches default
    UNKNOWN: { decision: 'DENY' }, // Matches default
  },
  'dsn:register-tool': {
    VOUCHED: { decision: 'ALLOW' },
    COMMUNITY: { decision: 'CONFIRM', risk: 'medium' },
    UNKNOWN: { decision: 'DENY' },
  },
  'dsn:register-service': {
    VOUCHED: { decision: 'ALLOW' },
    COMMUNITY: { decision: 'CONFIRM', risk: 'medium' },
    UNKNOWN: { decision: 'DENY' },
  },
  'dsn:publish-observation': {
    VOUCHED: { decision: 'ALLOW' },
    COMMUNITY: { decision: 'CONFIRM', risk: 'medium' },
    UNKNOWN: { decision: 'DENY' },
  },
  'dsn:identity': {
    // SELF: ALLOW (default)
    VOUCHED: { decision: 'CONFIRM', risk: 'high' },
    COMMUNITY: { decision: 'DENY' },
    UNKNOWN: { decision: 'DENY' },
  },
  'dsn:gmf-write': {
    // SELF: ALLOW (default)
    VOUCHED: { decision: 'CONFIRM', risk: 'medium' },
    COMMUNITY: { decision: 'CONFIRM', risk: 'high' },
    UNKNOWN: { decision: 'DENY' },
  },
  'crypto:sign': {
    // SELF: ALLOW (default)
    VOUCHED: { decision: 'CONFIRM', risk: 'medium' },
    COMMUNITY: { decision: 'DENY' },
    UNKNOWN: { decision: 'DENY' },
  },
  'crypto:encrypt': {
    // SELF: ALLOW (default)
    VOUCHED: { decision: 'CONFIRM', risk: 'medium' },
    COMMUNITY: { decision: 'DENY' },
    UNKNOWN: { decision: 'DENY' },
  },
  'wallet:read': {
    VOUCHED: { decision: 'ALLOW' },
    COMMUNITY: { decision: 'CONFIRM', risk: 'medium' },
    UNKNOWN: { decision: 'DENY' },
  },
  'wallet:transfer': {
    SELF: { decision: 'CONFIRM', risk: 'high' },
    VOUCHED: { decision: 'CONFIRM', risk: 'critical' },
    COMMUNITY: { decision: 'DENY' },
    UNKNOWN: { decision: 'DENY' },
  },
  'system:shell': {
    SELF: { decision: 'CONFIRM', risk: 'medium' },
    VOUCHED: { decision: 'DENY' },
    COMMUNITY: { decision: 'DENY' },
    UNKNOWN: { decision: 'DENY' },
  },
};

export class TrustGate implements ITrustGate {
  constructor(private readonly evaluator: ITrustEvaluator) {}

  /**
   * Evaluate the trust level of a signed envelope.
   * Delegates to the TrustEvaluator.
   */
  async evaluate<T>(envelope: SignedEnvelope<T>): Promise<TrustAssessment> {
    return this.evaluator.evaluate(envelope);
  }

  /**
   * Check if a requested capability is allowed for a given envelope.
   * Evaluates trust first, then checks the capability matrix.
   */
  async checkCapability<T>(
    envelope: SignedEnvelope<T>,
    capability: Capability
  ): Promise<CapabilityCheckResult> {
    const assessment = await this.evaluate(envelope);
    return this.check(capability, assessment);
  }

  /**
   * Check whether a capability is allowed for a given trust assessment.
   * Implements the Capability Matrix logic.
   */
  check(capability: Capability, trust: TrustAssessment): CapabilityCheckResult {
    if (trust.level === 'REVOKED') {
      return { decision: 'DENY', reason: 'Trust revoked' };
    }

    const levelRules = CAPABILITY_MATRIX[capability];
    const rule = levelRules?.[trust.level] ?? DEFAULT_RULES[trust.level];

    return {
      decision: rule.decision,
      reason: rule.risk ? `${rule.risk} risk capability` : undefined,
    };
  }

  /**
   * Check all requested capabilities for an envelope.
   */
  checkAll(
    envelope: SignedEnvelope<unknown>,
    trust: TrustAssessment
  ): Map<Capability, CapabilityCheckResult> {
    const results = new Map<Capability, CapabilityCheckResult>();
    for (const cap of envelope.requestedCapabilities) {
      results.set(cap, this.check(cap, trust));
    }
    return results;
  }
}
