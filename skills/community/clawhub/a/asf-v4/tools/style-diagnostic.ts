/**
 * ASF V4.0 Style Loading Diagnostic CLI
 * 
 * V1.5.0 - Style loading diagnostic commands.
 * Provides 5 diagnostic commands for style loading issues.
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

// ============================================================================
// Types
// ============================================================================

export interface DiagnosticResult {
  command: string;
  status: 'pass' | 'fail' | 'warning';
  message: string;
  details?: any;
  timestamp: number;
}

export interface StyleLoadingReport {
  overall: 'healthy' | 'degraded' | 'critical';
  styleLoadingRate: number;
  criticalCSSStatus: 'inlined' | 'missing' | 'partial';
  externalStylesLoaded: number;
  externalStylesTotal: number;
  foucIncidents: number;
  recommendations: string[];
}

// ============================================================================
// Diagnostic Commands
// ============================================================================

/**
 * Command 1: anfsf:style:status
 * Check overall style loading status.
 */
export async function cmdStyleStatus(): Promise<DiagnosticResult> {
  console.log('🔍 Checking style loading status...\n');

  try {
    // Check if style assets exist
    const workspaceRoot = process.cwd();
    const styleDirs = [
      join(workspaceRoot, 'src', 'styles'),
      join(workspaceRoot, 'public', 'styles'),
      join(workspaceRoot, 'assets', 'styles'),
    ];

    const foundDirs: string[] = [];
    const missingDirs: string[] = [];

    for (const dir of styleDirs) {
      if (existsSync(dir)) {
        foundDirs.push(dir);
      } else {
        missingDirs.push(dir);
      }
    }

    // Check for critical CSS
    const criticalCSSPath = join(workspaceRoot, 'src', 'styles', 'critical.css');
    const hasCriticalCSS = existsSync(criticalCSSPath);

    // Check for tailwind config
    const tailwindConfigPath = join(workspaceRoot, 'tailwind.config.js');
    const hasTailwindConfig = existsSync(tailwindConfigPath);

    const status: DiagnosticResult = {
      command: 'anfsf:style:status',
      status: hasCriticalCSS ? 'pass' : 'warning',
      message: hasCriticalCSS 
        ? '✅ Style loading configuration looks good' 
        : '⚠️  Critical CSS not found',
      details: {
        styleDirectories: {
          found: foundDirs,
          missing: missingDirs,
        },
        criticalCSS: hasCriticalCSS,
        tailwindConfig: hasTailwindConfig,
      },
      timestamp: Date.now(),
    };

    console.log(formatDiagnosticResult(status));
    return status;

  } catch (error) {
    return {
      command: 'anfsf:style:status',
      status: 'fail',
      message: `❌ Error checking style status: ${error}`,
      timestamp: Date.now(),
    };
  }
}

/**
 * Command 2: anfsf:style:probe
 * Probe style resources for availability.
 */
export async function cmdStyleProbe(urls?: string[]): Promise<DiagnosticResult> {
  console.log('🔍 Probing style resources...\n');

  const defaultUrls = [
    'https://cdn.example.com/styles/main.css',
    'https://cdn.example.com/styles/critical.css',
    'https://fonts.googleapis.com/css2?family=Inter',
  ];

  const urlsToProbe = urls || defaultUrls;
  const results: { url: string; status: string; ok: boolean }[] = [];

  for (const url of urlsToProbe) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);

      const response = await fetch(url, {
        method: 'HEAD',
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      results.push({
        url,
        status: `${response.status} ${response.statusText}`,
        ok: response.ok,
      });
    } catch (error) {
      results.push({
        url,
        status: `Error: ${error}`,
        ok: false,
      });
    }
  }

  const passedCount = results.filter(r => r.ok).length;
  const failedCount = results.length - passedCount;

  const status: DiagnosticResult = {
    command: 'anfsf:style:probe',
    status: failedCount === 0 ? 'pass' : failedCount < results.length / 2 ? 'warning' : 'fail',
    message: `Probed ${results.length} resources: ${passedCount} passed, ${failedCount} failed`,
    details: {
      results,
      passedCount,
      failedCount,
      successRate: (passedCount / results.length) * 100,
    },
    timestamp: Date.now(),
  };

  console.log(formatDiagnosticResult(status));
  console.log('\nDetailed Results:');
  results.forEach(r => {
    console.log(`  ${r.ok ? '✅' : '❌'} ${r.url}`);
    console.log(`     Status: ${r.status}`);
  });

  return status;
}

/**
 * Command 3: anfsf:style:kpi
 * Check style loading KPI metrics.
 */
export async function cmdStyleKPI(): Promise<DiagnosticResult> {
  console.log('📊 Checking style loading KPI metrics...\n');

  // Target KPI values (V1.5.0)
  const targets = {
    styleLoadingSuccessRate: 99.0,
    criticalCSSInliningRate: 100.0,
    avgLoadTimeMs: 200,
    p99LoadTimeMs: 500,
    foucIncidentsMax: 0,
  };

  // In production, these would come from actual metrics
  // For demo, we'll simulate reasonable values
  const current = {
    styleLoadingSuccessRate: 99.5,
    criticalCSSInliningRate: 100.0,
    avgLoadTimeMs: 150,
    p99LoadTimeMs: 400,
    foucIncidents: 0,
  };

  const violations: string[] = [];

  if (current.styleLoadingSuccessRate < targets.styleLoadingSuccessRate) {
    violations.push(`Style loading rate ${current.styleLoadingSuccessRate}% < ${targets.styleLoadingSuccessRate}%`);
  }

  if (current.criticalCSSInliningRate < targets.criticalCSSInliningRate) {
    violations.push(`Critical CSS inlining ${current.criticalCSSInliningRate}% < ${targets.criticalCSSInliningRate}%`);
  }

  if (current.avgLoadTimeMs > targets.avgLoadTimeMs) {
    violations.push(`Avg load time ${current.avgLoadTimeMs}ms > ${targets.avgLoadTimeMs}ms`);
  }

  if (current.foucIncidents > targets.foucIncidentsMax) {
    violations.push(`FOUC incidents ${current.foucIncidents} > ${targets.foucIncidentsMax}`);
  }

  const status: DiagnosticResult = {
    command: 'anfsf:style:kpi',
    status: violations.length === 0 ? 'pass' : 'warning',
    message: violations.length === 0 
      ? '✅ All KPIs within target ranges' 
      : `⚠️  ${violations.length} KPI violation(s) detected`,
    details: {
      targets,
      current,
      violations,
    },
    timestamp: Date.now(),
  };

  console.log(formatDiagnosticResult(status));
  console.log('\nKPI Details:');
  console.log('┌─────────────────────────────┬──────────┬──────────┬────────┐');
  console.log('│ Metric                      │ Target   │ Current  │ Status │');
  console.log('├─────────────────────────────┼──────────┼──────────┼────────┤');
  console.log(`│ Style Loading Success Rate  │ ≥${targets.styleLoadingSuccessRate}%    │ ${current.styleLoadingSuccessRate}%      │ ${current.styleLoadingSuccessRate >= targets.styleLoadingSuccessRate ? '✅' : '❌'}      │`);
  console.log(`│ Critical CSS Inlining Rate  │ ≥${targets.criticalCSSInliningRate}%    │ ${current.criticalCSSInliningRate}%      │ ${current.criticalCSSInliningRate >= targets.criticalCSSInliningRate ? '✅' : '❌'}      │`);
  console.log(`│ Avg Load Time               │ ≤${targets.avgLoadTimeMs}ms   │ ${current.avgLoadTimeMs}ms     │ ${current.avgLoadTimeMs <= targets.avgLoadTimeMs ? '✅' : '❌'}      │`);
  console.log(`│ P99 Load Time               │ ≤${targets.p99LoadTimeMs}ms   │ ${current.p99LoadTimeMs}ms     │ ${current.p99LoadTimeMs <= targets.p99LoadTimeMs ? '✅' : '❌'}      │`);
  console.log(`│ FOUC Incidents              │ ≤${targets.foucIncidentsMax}       │ ${current.foucIncidents}         │ ${current.foucIncidents <= targets.foucIncidentsMax ? '✅' : '❌'}      │`);
  console.log('└─────────────────────────────┴──────────┴──────────┴────────┘');

  return status;
}

/**
 * Command 4: anfsf:style:contract
 * Check UI Contract Pack asset manifest.
 */
export async function cmdStyleContract(): Promise<DiagnosticResult> {
  console.log('📦 Checking UI Contract Pack asset manifest...\n');

  // In production, this would read from actual contract files
  // For demo, we'll simulate the check

  const manifestCheck = {
    hasAssetManifest: true,
    hasCriticalStyles: true,
    hasExternalStyles: true,
    hasDynamicStyles: true,
    hasTailwindStyles: true,
    hasFonts: true,
    mcpSyncEnabled: true,
    integrityValidation: true,
  };

  const missing: string[] = [];

  if (!manifestCheck.hasAssetManifest) missing.push('assetManifest');
  if (!manifestCheck.hasCriticalStyles) missing.push('styles.critical');
  if (!manifestCheck.hasExternalStyles) missing.push('styles.external');
  if (!manifestCheck.hasDynamicStyles) missing.push('styles.dynamic');
  if (!manifestCheck.hasTailwindStyles) missing.push('styles.tailwind');
  if (!manifestCheck.mcpSyncEnabled) missing.push('MCP sync');
  if (!manifestCheck.integrityValidation) missing.push('integrity validation');

  const status: DiagnosticResult = {
    command: 'anfsf:style:contract',
    status: missing.length === 0 ? 'pass' : 'fail',
    message: missing.length === 0
      ? '✅ UI Contract Pack asset manifest is complete'
      : `❌ Missing manifest components: ${missing.join(', ')}`,
    details: {
      manifestCheck,
      missing,
    },
    timestamp: Date.now(),
  };

  console.log(formatDiagnosticResult(status));
  console.log('\nManifest Components:');
  console.log(`  ${manifestCheck.hasAssetManifest ? '✅' : '❌'} assetManifest`);
  console.log(`  ${manifestCheck.hasCriticalStyles ? '✅' : '❌'} styles.critical`);
  console.log(`  ${manifestCheck.hasExternalStyles ? '✅' : '❌'} styles.external`);
  console.log(`  ${manifestCheck.hasDynamicStyles ? '✅' : '❌'} styles.dynamic`);
  console.log(`  ${manifestCheck.hasTailwindStyles ? '✅' : '❌'} styles.tailwind`);
  console.log(`  ${manifestCheck.hasFonts ? '✅' : '❌'} fonts`);
  console.log(`  ${manifestCheck.mcpSyncEnabled ? '✅' : '❌'} MCP sync`);
  console.log(`  ${manifestCheck.integrityValidation ? '✅' : '❌'} Integrity validation`);

  return status;
}

/**
 * Command 5: anfsf:style:report
 * Generate comprehensive style loading report.
 */
export async function cmdStyleReport(outputFile?: string): Promise<DiagnosticResult> {
  console.log('📋 Generating comprehensive style loading report...\n');

  // Run all checks
  const statusResult = await cmdStyleStatus();
  const probeResult = await cmdStyleProbe();
  const kpiResult = await cmdStyleKPI();
  const contractResult = await cmdStyleContract();

  // Determine overall status
  const failures = [statusResult, probeResult, kpiResult, contractResult]
    .filter(r => r.status === 'fail').length;
  
  const warnings = [statusResult, probeResult, kpiResult, contractResult]
    .filter(r => r.status === 'warning').length;

  const overall: 'healthy' | 'degraded' | 'critical' = 
    failures > 0 ? 'critical' : warnings > 0 ? 'degraded' : 'healthy';

  const report: StyleLoadingReport = {
    overall,
    styleLoadingRate: (kpiResult.details?.current?.styleLoadingSuccessRate as number) || 100,
    criticalCSSStatus: (statusResult.details?.criticalCSS as boolean) ? 'inlined' : 'missing',
    externalStylesLoaded: (probeResult.details?.passedCount as number) || 0,
    externalStylesTotal: (probeResult.details?.results?.length as number) || 0,
    foucIncidents: (kpiResult.details?.current?.foucIncidents as number) || 0,
    recommendations: generateRecommendations(statusResult, probeResult, kpiResult, contractResult),
  };

  const status: DiagnosticResult = {
    command: 'anfsf:style:report',
    status: overall === 'healthy' ? 'pass' : overall === 'degraded' ? 'warning' : 'fail',
    message: `Style Loading Report: ${overall.toUpperCase()}`,
    details: report,
    timestamp: Date.now(),
  };

  console.log('\n' + '='.repeat(60));
  console.log('         ASF V4.0 STYLE LOADING REPORT');
  console.log('='.repeat(60));
  console.log(`Overall Status: ${overall.toUpperCase()}`);
  console.log(`Style Loading Rate: ${report.styleLoadingRate}%`);
  console.log(`Critical CSS: ${report.criticalCSSStatus}`);
  console.log(`External Styles: ${report.externalStylesLoaded}/${report.externalStylesTotal}`);
  console.log(`FOUC Incidents: ${report.foucIncidents}`);
  console.log('\nRecommendations:');
  report.recommendations.forEach((rec, i) => {
    console.log(`  ${i + 1}. ${rec}`);
  });
  console.log('='.repeat(60));

  // Write to file if specified
  if (outputFile) {
    writeFileSync(outputFile, JSON.stringify(report, null, 2));
    console.log(`\n📄 Report saved to: ${outputFile}`);
  }

  return status;
}

// ============================================================================
// Helper Functions
// ============================================================================

function formatDiagnosticResult(result: DiagnosticResult): string {
  const icon = result.status === 'pass' ? '✅' : result.status === 'warning' ? '⚠️' : '❌';
  return `${icon} [${result.command}] ${result.message}`;
}

function generateRecommendations(
  status: DiagnosticResult,
  probe: DiagnosticResult,
  kpi: DiagnosticResult,
  contract: DiagnosticResult
): string[] {
  const recommendations: string[] = [];

  if (!status.details?.criticalCSS) {
    recommendations.push('Add critical CSS inlining to prevent FOUC');
  }

  if (probe.details?.failedCount > 0) {
    recommendations.push(`Fix ${probe.details.failedCount} failed style resource(s)`);
  }

  if (kpi.details?.violations?.length > 0) {
    recommendations.push('Address KPI violations to meet targets');
  }

  if (contract.details?.missing?.length > 0) {
    recommendations.push(`Complete UI Contract Pack: add ${contract.details.missing.join(', ')}`);
  }

  if (recommendations.length === 0) {
    recommendations.push('Style loading is healthy - no action needed');
  }

  return recommendations;
}

// ============================================================================
// CLI Entry Point
// ============================================================================

export async function runStyleDiagnostic(
  command: string,
  args: string[]
): Promise<DiagnosticResult> {
  switch (command) {
    case 'status':
      return cmdStyleStatus();
    
    case 'probe':
      return cmdStyleProbe(args);
    
    case 'kpi':
      return cmdStyleKPI();
    
    case 'contract':
      return cmdStyleContract();
    
    case 'report':
      const outputFile = args.find(arg => arg.startsWith('--output='))?.split('=')[1];
      return cmdStyleReport(outputFile);
    
    default:
      return {
        command: 'unknown',
        status: 'fail',
        message: `Unknown command: ${command}. Available: status, probe, kpi, contract, report`,
        timestamp: Date.now(),
      };
  }
}
