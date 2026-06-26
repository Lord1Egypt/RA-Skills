/**
 * ASF V4.0 Performance Benchmark Suite
 * 
 * Phase 3: Performance testing and benchmarking.
 * Version: v0.9.0
 */

import { VetoEnforcer } from '../../../src/core/synthesizer';
import { generateOwnershipProof } from '../../../src/core/synthesizer';
import { computeEconomicsScore } from '../../../src/core/synthesizer';
import { MemoryExtension } from '../integrations';
import { AgentStatusExtension } from '../integrations';

/**
 * Benchmark result.
 */
export interface BenchmarkResult {
  name: string;
  iterations: number;
  totalTimeMs: number;
  avgTimeMs: number;
  minTimeMs: number;
  maxTimeMs: number;
  p95TimeMs: number;
  p99TimeMs: number;
  opsPerSecond: number;
  memoryUsedMB?: number;
}

/**
 * Run benchmark for a function.
 */
async function runBenchmark(
  name: string,
  fn: () => Promise<void> | void,
  iterations: number = 1000
): Promise<BenchmarkResult> {
  const times: number[] = [];
  
  // Warm up
  for (let i = 0; i < 10; i++) {
    await fn();
  }
  
  // Measure memory before (if available)
  let memoryBefore = 0;
  if (global.gc) {
    global.gc();
    memoryBefore = process.memoryUsage().heapUsed;
  }
  
  // Run benchmark
  const startTime = Date.now();
  
  for (let i = 0; i < iterations; i++) {
    const iterStart = performance.now();
    await fn();
    const iterEnd = performance.now();
    times.push(iterEnd - iterStart);
  }
  
  const totalTimeMs = Date.now() - startTime;
  
  // Measure memory after
  let memoryUsedMB: number | undefined;
  if (global.gc) {
    global.gc();
    const memoryAfter = process.memoryUsage().heapUsed;
    memoryUsedMB = (memoryAfter - memoryBefore) / 1024 / 1024;
  }
  
  // Calculate statistics
  times.sort((a, b) => a - b);
  
  const avgTimeMs = times.reduce((a, b) => a + b, 0) / times.length;
  const minTimeMs = times[0];
  const maxTimeMs = times[times.length - 1];
  const p95TimeMs = times[Math.floor(times.length * 0.95)];
  const p99TimeMs = times[Math.floor(times.length * 0.99)];
  const opsPerSecond = iterations / (totalTimeMs / 1000);
  
  return {
    name,
    iterations,
    totalTimeMs,
    avgTimeMs: Math.round(avgTimeMs * 1000) / 1000,
    minTimeMs: Math.round(minTimeMs * 1000) / 1000,
    maxTimeMs: Math.round(maxTimeMs * 1000) / 1000,
    p95TimeMs: Math.round(p95TimeMs * 1000) / 1000,
    p99TimeMs: Math.round(p99TimeMs * 1000) / 1000,
    opsPerSecond: Math.round(opsPerSecond),
    memoryUsedMB,
  };
}

/**
 * Benchmark: Veto Enforcement
 */
async function benchmarkVetoEnforcement(): Promise<BenchmarkResult> {
  const enforcer = new VetoEnforcer();
  
  const mockChanges = [
    { resourceType: 'contract', resourcePath: '/orders', action: 'update' },
  ];
  
  const mockApprovals = [
    { authority: 'architect', scope: 'contract:OpenAPI:*', status: 'approved' },
  ];
  
  return runBenchmark('Veto Enforcement', () => {
    enforcer.enforce({ changes: mockChanges }, mockApprovals);
  });
}

/**
 * Benchmark: Ownership Proof Generation
 */
async function benchmarkOwnershipProof(): Promise<BenchmarkResult> {
  const mockResources = [
    { type: 'contract' as const, path: 'OpenAPI:/orders', subpath: 'POST' },
    { type: 'contract' as const, path: 'DBSchema:users', subpath: undefined },
  ];
  
  const mockRoles = [
    { id: 'backend-team' },
    { id: 'frontend-team' },
    { id: 'architect' },
  ];
  
  const mockRules = [
    { resourcePattern: '*', roleId: '*', permission: 'read' as const, priority: 1 },
    { resourcePattern: 'contract:*', roleId: 'architect', permission: 'approve' as const, priority: 100 },
  ];
  
  return runBenchmark('Ownership Proof Generation', () => {
    generateOwnershipProof(mockResources, mockRoles, mockRules);
  });
}

/**
 * Benchmark: Economics Score Calculation
 */
async function benchmarkEconomicsScore(): Promise<BenchmarkResult> {
  const mockAssignment = {
    taskToRole: {
      'task-1': 'role-1',
      'task-2': 'role-1',
      'task-3': 'role-2',
      'task-4': 'role-2',
      'task-5': 'role-1',
    },
  };
  
  const mockDag = {
    tasks: Array(5).fill({ id: 'task', estCost: 1 }),
    edges: Array(4).fill({ from: 'task-1', to: 'task-2', type: 'depends_on' }),
  };
  
  const mockRoles = [
    { id: 'role-1', economics: { costPerTask: 1.0, overheadPerDependency: 0.5, parallelismCap: 5 } },
    { id: 'role-2', economics: { costPerTask: 1.0, overheadPerDependency: 0.5, parallelismCap: 5 } },
  ];
  
  return runBenchmark('Economics Score Calculation', () => {
    computeEconomicsScore(mockAssignment, mockDag, mockRoles);
  });
}

/**
 * Benchmark: Memory Write
 */
async function benchmarkMemoryWrite(): Promise<BenchmarkResult> {
  const mockChangeEvent = {
    id: 'evt-123',
    ts: Date.now(),
    actorRoleId: 'backend-team',
    action: 'update' as const,
    target: { kind: 'contract' as const, idOrPath: '/orders' },
    ownershipRuleId: 'rule-1',
    diff: {},
    riskScore: 50,
    blastRadius: 5,
  };
  
  return runBenchmark('Memory Write', async () => {
    await MemoryExtension.writeChangeToMemory(mockChangeEvent);
  });
}

/**
 * Benchmark: Memory Read
 */
async function benchmarkMemoryRead(): Promise<BenchmarkResult> {
  // Pre-populate cache
  for (let i = 0; i < 100; i++) {
    await MemoryExtension.writeChangeToMemory({
      id: `evt-${i}`,
      ts: Date.now(),
      actorRoleId: 'test',
      action: 'update' as const,
      target: { kind: 'contract' as const, idOrPath: `/test-${i}` },
      ownershipRuleId: 'rule-1',
      diff: {},
      riskScore: 50,
    });
  }
  
  return runBenchmark('Memory Read', async () => {
    await MemoryExtension.readChangeHistory({ limit: 50 });
  });
}

/**
 * Benchmark: Agent Status Extension
 */
async function benchmarkAgentStatus(): Promise<BenchmarkResult> {
  const mockKPI = {
    roleId: 'backend-team',
    timestamp: Date.now(),
    window: '1d' as const,
    throughput: 5.2,
    failureRate: 0.12,
    reworkRate: 0.18,
    queuePressure: 1.1,
    conflictRate: 0.08,
    driftIndex: 0.25,
    healthScore: 75,
    trend: 'stable' as const,
    taskCount: 20,
    changeCount: 15,
  };
  
  return runBenchmark('Agent Status Extension', async () => {
    await AgentStatusExtension.extendAgentStatusWithKPI('main', mockKPI);
  });
}

/**
 * Run all benchmarks.
 */
export async function runAllBenchmarks(): Promise<BenchmarkResult[]> {
  console.log('Starting ASF V4.0 Performance Benchmarks...\n');
  
  const results: BenchmarkResult[] = [];
  
  // Run benchmarks
  results.push(await benchmarkVetoEnforcement());
  results.push(await benchmarkOwnershipProof());
  results.push(await benchmarkEconomicsScore());
  results.push(await benchmarkMemoryWrite());
  results.push(await benchmarkMemoryRead());
  results.push(await benchmarkAgentStatus());
  
  // Print results
  console.log('\nBenchmark Results:');
  console.log('==================\n');
  
  for (const result of results) {
    console.log(`${result.name}:`);
    console.log(`  Iterations: ${result.iterations}`);
    console.log(`  Total Time: ${result.totalTimeMs.toFixed(0)}ms`);
    console.log(`  Avg Time: ${result.avgTimeMs.toFixed(2)}ms`);
    console.log(`  P95 Time: ${result.p95TimeMs.toFixed(2)}ms`);
    console.log(`  P99 Time: ${result.p99TimeMs.toFixed(2)}ms`);
    console.log(`  Ops/Second: ${result.opsPerSecond}`);
    if (result.memoryUsedMB !== undefined) {
      console.log(`  Memory Used: ${result.memoryUsedMB.toFixed(2)}MB`);
    }
    console.log('');
  }
  
  // Summary
  const totalOps = results.reduce((sum, r) => sum + r.opsPerSecond, 0);
  const avgP95 = results.reduce((sum, r) => sum + r.p95TimeMs, 0) / results.length;
  
  console.log('Summary:');
  console.log(`  Total Operations/Second: ${totalOps}`);
  console.log(`  Average P95 Latency: ${avgP95.toFixed(2)}ms`);
  console.log('');
  
  return results;
}

/**
 * Check if benchmarks pass thresholds.
 */
export function checkBenchmarkThresholds(
  results: BenchmarkResult[]
): { passed: boolean; failures: string[] } {
  const failures: string[] = [];
  
  // Thresholds
  const thresholds: Record<string, { maxP95: number; minOps: number }> = {
    'Veto Enforcement': { maxP95: 10, minOps: 100 },
    'Ownership Proof Generation': { maxP95: 20, minOps: 50 },
    'Economics Score Calculation': { maxP95: 30, minOps: 30 },
    'Memory Write': { maxP95: 5, minOps: 200 },
    'Memory Read': { maxP95: 10, minOps: 100 },
    'Agent Status Extension': { maxP95: 5, minOps: 200 },
  };
  
  for (const result of results) {
    const threshold = thresholds[result.name];
    if (!threshold) continue;
    
    if (result.p95TimeMs > threshold.maxP95) {
      failures.push(
        `${result.name}: P95 ${result.p95TimeMs.toFixed(2)}ms > ${threshold.maxP95}ms`
      );
    }
    
    if (result.opsPerSecond < threshold.minOps) {
      failures.push(
        `${result.name}: ${result.opsPerSecond} ops/s < ${threshold.minOps} ops/s`
      );
    }
  }
  
  return {
    passed: failures.length === 0,
    failures,
  };
}

// ============================================================================
// Main
// ============================================================================

async function main(): Promise<void> {
  const results = await runAllBenchmarks();
  const { passed, failures } = checkBenchmarkThresholds(results);
  
  if (passed) {
    console.log('✅ All benchmarks passed!');
    process.exit(0);
  } else {
    console.log('❌ Benchmark failures:');
    for (const failure of failures) {
      console.log(`  - ${failure}`);
    }
    process.exit(1);
  }
}

// Run if executed directly
if (typeof require !== 'undefined' && require.main === module) {
  main().catch((error) => {
    console.error('Benchmark failed:', error);
    process.exit(1);
  });
}
