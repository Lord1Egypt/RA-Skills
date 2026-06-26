import { describe, it, expect, beforeEach } from 'vitest';
import { resolveModel, calculateCost, costFallback, clearResolveCache } from '../src/pricing.js';

describe('resolveModel', () => {
  beforeEach(() => clearResolveCache());

  it('returns plain model name unchanged with pricing', () => {
    const result = resolveModel('claude-sonnet-4-6');
    expect(result.friendlyName).toBe('claude-sonnet-4-6');
    expect(result.rawModel).toBe('claude-sonnet-4-6');
    expect(result.pricing).toBeDefined();
    expect(result.pricing!.inputPer1M).toBe(3.00);
  });

  it('returns unknown model name unchanged without pricing', () => {
    const result = resolveModel('some-custom-model');
    expect(result.friendlyName).toBe('some-custom-model');
    expect(result.pricing).toBeUndefined();
  });

  it('returns empty string for empty input', () => {
    const result = resolveModel('');
    expect(result.friendlyName).toBe('');
    expect(result.rawModel).toBe('');
  });

  it('resolves Bedrock ARN via model_map', () => {
    const modelMap = { 'ekadx6q1kayx': 'claude-sonnet-4-6' };
    const arn = 'arn:aws:bedrock:eu-west-1:482397833370:application-inference-profile/ekadx6q1kayx';
    const result = resolveModel(arn, modelMap);
    expect(result.friendlyName).toBe('claude-sonnet-4-6');
    expect(result.rawModel).toBe(arn);
    expect(result.region).toBe('eu-west-1');
    expect(result.pricing).toBeDefined();
    expect(result.pricing!.inputPer1M).toBe(3.00);
  });

  it('resolves ARN with known model name pattern (no model_map)', () => {
    const arn = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0';
    const result = resolveModel(arn);
    expect(result.friendlyName).toBe('claude-3-5-sonnet');
    expect(result.rawModel).toBe(arn);
    expect(result.region).toBe('us-east-1');
    expect(result.pricing).toBeDefined();
  });

  it('returns original ARN when no match and no model_map', () => {
    const arn = 'arn:aws:bedrock:eu-west-1:123456:application-inference-profile/unknown-profile';
    const result = resolveModel(arn);
    expect(result.friendlyName).toBe(arn);
    expect(result.rawModel).toBe(arn);
    expect(result.pricing).toBeUndefined();
  });

  it('uses region-specific pricing for eu-west-1 haiku', () => {
    const modelMap = { 'my-haiku-profile': 'claude-haiku-4-5' };
    const arn = 'arn:aws:bedrock:eu-west-1:123:application-inference-profile/my-haiku-profile';
    const result = resolveModel(arn, modelMap);
    expect(result.friendlyName).toBe('claude-haiku-4-5');
    expect(result.pricing!.inputPer1M).toBe(1.00); // EU pricing
    expect(result.pricing!.outputPer1M).toBe(5.00);
  });

  it('uses default pricing when no region-specific entry', () => {
    const modelMap = { 'my-haiku-profile': 'claude-haiku-4-5' };
    const arn = 'arn:aws:bedrock:us-east-1:123:application-inference-profile/my-haiku-profile';
    const result = resolveModel(arn, modelMap);
    expect(result.pricing!.inputPer1M).toBe(0.80); // Default pricing
    expect(result.pricing!.outputPer1M).toBe(4.00);
  });

  it('extracts region from ARN', () => {
    const arn = 'arn:aws:bedrock:ap-southeast-1:123:foundation-model/anthropic.claude-3-haiku-20240307-v1:0';
    const result = resolveModel(arn);
    expect(result.region).toBe('ap-southeast-1');
  });

  it('uses configPricing override over built-in pricing', () => {
    const configPricing = {
      'claude-sonnet-4-6': { input: 99.00, output: 199.00 },
    };
    const result = resolveModel('claude-sonnet-4-6', undefined, configPricing);
    expect(result.pricing).toBeDefined();
    expect(result.pricing!.inputPer1M).toBe(99.00);
    expect(result.pricing!.outputPer1M).toBe(199.00);
  });

  it('configPricing does not invent cache pricing when not provided', () => {
    const configPricing = {
      'llama3-3-70b': { input: 5.00, output: 5.00 },
    };
    const result = resolveModel('llama3-3-70b', undefined, configPricing);
    expect(result.pricing).toBeDefined();
    expect(result.pricing!.cacheReadPer1M).toBeUndefined();
    expect(result.pricing!.cacheWritePer1M).toBeUndefined();
  });

  it('configPricing preserves explicit cache pricing', () => {
    const configPricing = {
      'claude-sonnet-4-6': { input: 3.00, output: 15.00, cacheRead: 0.30, cacheWrite: 3.75 },
    };
    const result = resolveModel('claude-sonnet-4-6', undefined, configPricing);
    expect(result.pricing!.cacheReadPer1M).toBe(0.30);
    expect(result.pricing!.cacheWritePer1M).toBe(3.75);
  });

  it('uses region-specific configPricing when available', () => {
    const configPricing = {
      'claude-haiku-4-5:eu-west-1': { input: 2.00, output: 8.00 },
      'claude-haiku-4-5': { input: 0.80, output: 4.00 },
    };
    const modelMap = { 'my-haiku': 'claude-haiku-4-5' };
    const arn = 'arn:aws:bedrock:eu-west-1:123:application-inference-profile/my-haiku';
    const result = resolveModel(arn, modelMap, configPricing);
    expect(result.pricing!.inputPer1M).toBe(2.00); // region-specific override
    expect(result.pricing!.outputPer1M).toBe(8.00);
  });

  it('caches resolved models (same result for same rawModel)', () => {
    const arn = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-opus-20240229-v1:0';
    const result1 = resolveModel(arn);
    const result2 = resolveModel(arn);
    expect(result1).toBe(result2); // Same reference (cached)
  });

  it('model_map uses longest match when multiple keys match', () => {
    const modelMap = {
      'claude': 'claude-generic',       // short — matches broadly
      'ekadx6q1kayx': 'claude-sonnet-4-6', // long — specific profile ID
    };
    const arn = 'arn:aws:bedrock:eu-west-1:123:application-inference-profile/ekadx6q1kayx';
    const result = resolveModel(arn, modelMap);
    // Should match the longer, more specific key
    expect(result.friendlyName).toBe('claude-sonnet-4-6');
  });

  it('resolves nova-premier ARN with pricing', () => {
    const arn = 'arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-premier-v1:0';
    const result = resolveModel(arn);
    expect(result.friendlyName).toBe('nova-premier');
    expect(result.pricing).toBeDefined();
    expect(result.pricing!.inputPer1M).toBe(2.40);
  });
});

describe('calculateCost', () => {
  it('calculates basic input/output cost', () => {
    const pricing = { inputPer1M: 3.00, outputPer1M: 15.00 };
    const cost = calculateCost(1000, 500, pricing);
    // 1000/1M * 3.00 = 0.003, 500/1M * 15.00 = 0.0075
    expect(cost.input).toBe(0.003);
    expect(cost.output).toBe(0.0075);
    expect(cost.total).toBe(0.0105);
  });

  it('calculates cost with cache tokens', () => {
    const pricing = {
      inputPer1M: 3.00,
      outputPer1M: 15.00,
      cacheReadPer1M: 0.30,   // 0.1x input
      cacheWritePer1M: 3.75,  // 1.25x input
    };
    const cost = calculateCost(1000, 500, pricing, 2000, 1000);
    expect(cost.cacheRead).toBe(0.0006);   // 2000/1M * 0.30
    expect(cost.cacheWrite).toBe(0.00375); // 1000/1M * 3.75
    expect(cost.total).toBeCloseTo(0.003 + 0.0075 + 0.0006 + 0.00375, 6);
  });

  it('handles zero tokens', () => {
    const pricing = { inputPer1M: 3.00, outputPer1M: 15.00 };
    const cost = calculateCost(0, 0, pricing);
    expect(cost.total).toBe(0);
    expect(cost.input).toBe(0);
    expect(cost.output).toBe(0);
  });

  it('handles large token counts', () => {
    const pricing = { inputPer1M: 3.00, outputPer1M: 15.00 };
    const cost = calculateCost(50000, 1000, pricing);
    // 50000/1M * 3.00 = 0.15, 1000/1M * 15.00 = 0.015
    expect(cost.input).toBe(0.15);
    expect(cost.output).toBe(0.015);
    expect(cost.total).toBe(0.165);
  });

  it('omits cacheRead/cacheWrite when no cache tokens provided', () => {
    const pricing = { inputPer1M: 3.00, outputPer1M: 15.00, cacheReadPer1M: 0.30 };
    const cost = calculateCost(1000, 500, pricing);
    expect(cost.cacheRead).toBeUndefined();
    expect(cost.cacheWrite).toBeUndefined();
  });

  it('omits cache costs when model has no cache pricing (non-Anthropic)', () => {
    // Llama pricing — no cacheReadPer1M/cacheWritePer1M
    const pricing = { inputPer1M: 2.00, outputPer1M: 2.00 };
    const cost = calculateCost(1000, 500, pricing, 5000, 1000);
    // Cache tokens provided but model has no cache pricing — should not fabricate costs
    expect(cost.cacheRead).toBeUndefined();
    expect(cost.cacheWrite).toBeUndefined();
    expect(cost.total).toBe(0.003); // only input + output
  });
});

describe('costFallback', () => {
  it('returns reported cost when available and > 0', () => {
    const pricing = { inputPer1M: 3.00, outputPer1M: 15.00 };
    const result = costFallback(0.05, pricing, 1000, 500);
    expect(result.costTotal).toBe(0.05);
    expect(result.costBreakdown).toBeUndefined();
  });

  it('calculates from tokens when reported cost is 0', () => {
    const pricing = { inputPer1M: 3.00, outputPer1M: 15.00 };
    const result = costFallback(0, pricing, 1000, 500);
    expect(result.costTotal).toBe(0.0105);
    expect(result.costBreakdown).toBeDefined();
    expect(result.costBreakdown!.input).toBe(0.003);
    expect(result.costBreakdown!.output).toBe(0.0075);
  });

  it('calculates from tokens when reported cost is undefined', () => {
    const pricing = { inputPer1M: 3.00, outputPer1M: 15.00 };
    const result = costFallback(undefined, pricing, 1000, 500);
    expect(result.costTotal).toBe(0.0105);
    expect(result.costBreakdown).toBeDefined();
  });

  it('returns empty when no pricing and no reported cost', () => {
    const result = costFallback(undefined, undefined, 1000, 500);
    expect(result.costTotal).toBeUndefined();
    expect(result.costBreakdown).toBeUndefined();
  });

  it('returns empty when tokens are zero and no reported cost', () => {
    const pricing = { inputPer1M: 3.00, outputPer1M: 15.00 };
    const result = costFallback(undefined, pricing, 0, 0);
    expect(result.costTotal).toBeUndefined();
  });
});
