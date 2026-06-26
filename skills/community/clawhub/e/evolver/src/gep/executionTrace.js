// Execution Trace: structured, desensitized evolution execution summary.
// Built during solidify and optionally shared with Hub via EvolutionEvent payload.
//
// Desensitization rules (applied locally, never on Hub):
// - File paths: basename + extension only (src/utils/retry.js -> retry.js)
// - Code content: never sent, only statistical metrics (lines, files)
// - Error messages: type signature only (TypeError: x is not a function -> TypeError)
// - Environment variables, secrets, user data: stripped entirely
// - Configurable via EVOLVER_TRACE_LEVEL: none | minimal | standard | collaboration (default: minimal)

const path = require('path');

const TRACE_LEVELS = { none: 0, minimal: 1, standard: 2, collaboration: 3 };

function getTraceLevel() {
  const raw = String(process.env.EVOLVER_TRACE_LEVEL || 'minimal').toLowerCase().trim();
  return TRACE_LEVELS[raw] != null ? raw : 'minimal';
}

function desensitizeFilePath(filePath) {
  if (!filePath || typeof filePath !== 'string') return null;
  const ext = path.extname(filePath);
  const base = path.basename(filePath);
  return base || ext || 'unknown';
}

function extractErrorSignature(errorText) {
  if (!errorText || typeof errorText !== 'string') return null;
  const text = errorText.trim();

  // Match common error type patterns: TypeError, ReferenceError, SyntaxError, etc.
  const jsError = text.match(/^((?:[A-Z][a-zA-Z]*)?Error)\b/);
  if (jsError) return jsError[1];

  // Match errno-style: ECONNRESET, ENOENT, EPERM, etc.
  const errno = text.match(/\b(E[A-Z]{2,})\b/);
  if (errno) return errno[1];

  // Match HTTP status codes
  const http = text.match(/\b((?:4|5)\d{2})\b/);
  if (http) return 'HTTP_' + http[1];

  // Fallback: first word if it looks like an error type
  const firstWord = text.split(/[\s:]/)[0];
  if (firstWord && firstWord.length <= 40 && /^[A-Z]/.test(firstWord)) return firstWord;

  return 'UnknownError';
}

function inferToolChain(validationResults, blast) {
  const tools = new Set();

  if (blast && blast.files > 0) tools.add('file_edit');

  if (Array.isArray(validationResults)) {
    for (const r of validationResults) {
      const cmd = String(r.cmd || '').trim();
      if (cmd.startsWith('npm test') || cmd.includes('jest') || cmd.includes('mocha')) {
        tools.add('test_run');
      } else if (cmd.includes('lint') || cmd.includes('eslint')) {
        tools.add('lint_check');
      } else if (cmd.includes('validate') || cmd.includes('check')) {
        tools.add('validation_run');
      } else if (cmd.startsWith('node ')) {
        tools.add('node_exec');
      }
    }
  }

  return Array.from(tools);
}

function classifyBlastLevel(blast) {
  if (!blast) return 'unknown';
  const files = Number(blast.files) || 0;
  const lines = Number(blast.lines) || 0;
  if (files <= 3 && lines <= 50) return 'low';
  if (files <= 10 && lines <= 200) return 'medium';
  return 'high';
}

function buildExecutionTrace({
  gene,
  mutation,
  signals,
  blast,
  constraintCheck,
  validation,
  canary,
  outcomeStatus,
  startedAt,
  collaborationContext,
}) {
  const level = getTraceLevel();
  if (level === 'none') return null;

  const trace = {
    gene_id: gene && gene.id ? String(gene.id) : null,
    mutation_category: (mutation && mutation.category) || (gene && gene.category) || null,
    signals_matched: Array.isArray(signals) ? signals.slice(0, 10) : [],
    outcome: outcomeStatus || 'unknown',
  };

  // Minimal level: core metrics only
  trace.files_changed_count = blast ? Number(blast.files) || 0 : 0;
  trace.lines_added = 0;
  trace.lines_removed = 0;

  // Compute added/removed from blast if available
  if (blast && blast.lines) {
    // blast.lines is total churn (added + deleted); split heuristically
    const total = Number(blast.lines) || 0;
    if (outcomeStatus === 'success') {
      trace.lines_added = Math.round(total * 0.6);
      trace.lines_removed = total - trace.lines_added;
    } else {
      trace.lines_added = Math.round(total * 0.5);
      trace.lines_removed = total - trace.lines_added;
    }
  }

  trace.validation_result = validation && validation.ok ? 'pass' : 'fail';
  trace.blast_radius = classifyBlastLevel(blast);

  // Standard level: richer context
  if (level === 'standard') {
    // Desensitized file list (basenames only)
    if (blast && Array.isArray(blast.changed_files)) {
      trace.file_types = {};
      for (const f of blast.changed_files) {
        const ext = path.extname(f) || '.unknown';
        trace.file_types[ext] = (trace.file_types[ext] || 0) + 1;
      }
    }

    // Validation commands (already safe -- node/npm/npx only)
    if (validation && Array.isArray(validation.results)) {
      trace.validation_commands = validation.results.map(r => String(r.cmd || '').slice(0, 100));
    }

    // Error signatures (desensitized)
    trace.error_signatures = [];
    if (constraintCheck && Array.isArray(constraintCheck.violations)) {
      for (const v of constraintCheck.violations) {
        // Constraint violations have known prefixes; classify directly
        const vStr = String(v);
        if (vStr.startsWith('max_files')) trace.error_signatures.push('max_files_exceeded');
        else if (vStr.startsWith('forbidden_path')) trace.error_signatures.push('forbidden_path');
        else if (vStr.startsWith('HARD CAP')) trace.error_signatures.push('hard_cap_breach');
        else if (vStr.startsWith('CRITICAL')) trace.error_signatures.push('critical_overrun');
        else if (vStr.startsWith('critical_path')) trace.error_signatures.push('critical_path_modified');
        else if (vStr.startsWith('canary_failed')) trace.error_signatures.push('canary_failed');
        else if (vStr.startsWith('ethics:')) trace.error_signatures.push('ethics_violation');
        else {
          const sig = extractErrorSignature(v);
          if (sig) trace.error_signatures.push(sig);
        }
      }
    }
    if (validation && Array.isArray(validation.results)) {
      for (const r of validation.results) {
        if (!r.ok && r.err) {
          const sig = extractErrorSignature(r.err);
          if (sig && !trace.error_signatures.includes(sig)) {
            trace.error_signatures.push(sig);
          }
        }
      }
    }
    trace.error_signatures = trace.error_signatures.slice(0, 10);

    // Tool chain inference
    trace.tool_chain = inferToolChain(
      validation && validation.results ? validation.results : [],
      blast
    );

    // Duration
    if (validation && validation.startedAt && validation.finishedAt) {
      trace.validation_duration_ms = validation.finishedAt - validation.startedAt;
    }

    // Canary result
    if (canary && !canary.skipped) {
      trace.canary_ok = !!canary.ok;
    }
  }

  // Collaboration level: swarm interaction decision traces
  if (level === 'collaboration') {
    // Include everything from standard level
    if (blast && Array.isArray(blast.changed_files)) {
      if (!trace.file_types) {
        trace.file_types = {};
        for (const f of blast.changed_files) {
          const ext = path.extname(f) || '.unknown';
          trace.file_types[ext] = (trace.file_types[ext] || 0) + 1;
        }
      }
    }

    if (validation && Array.isArray(validation.results)) {
      if (!trace.validation_commands) {
        trace.validation_commands = validation.results.map(r => String(r.cmd || '').slice(0, 100));
      }
    }

    if (!trace.error_signatures) trace.error_signatures = [];
    if (!trace.tool_chain) {
      trace.tool_chain = inferToolChain(
        validation && validation.results ? validation.results : [],
        blast
      );
    }

    if (canary && !canary.skipped && trace.canary_ok === undefined) {
      trace.canary_ok = !!canary.ok;
    }

    // Collaboration-specific fields
    trace.collaboration = {};

    if (collaborationContext) {
      const ctx = collaborationContext;

      if (ctx.roleDecision) {
        trace.collaboration.role_decision = {
          chosen_role: ctx.roleDecision.chosenRole || null,
          reasoning: (ctx.roleDecision.reasoning || '').slice(0, 500),
          alternatives_considered: Array.isArray(ctx.roleDecision.alternatives)
            ? ctx.roleDecision.alternatives.slice(0, 5)
            : [],
        };
      }

      if (ctx.teammateOutputsConsumed) {
        trace.collaboration.context_consumption = Array.isArray(ctx.teammateOutputsConsumed)
          ? ctx.teammateOutputsConsumed.slice(0, 10).map(o => ({
              from_node_id: o.fromNodeId || null,
              output_type: o.outputType || 'unknown',
              consumed_bytes: Number(o.consumedBytes) || 0,
              usage_summary: (o.usageSummary || '').slice(0, 200),
            }))
          : [];
      }

      if (ctx.delegations) {
        trace.collaboration.delegations = Array.isArray(ctx.delegations)
          ? ctx.delegations.slice(0, 10).map(d => ({
              to_node_id: d.toNodeId || null,
              task_title: (d.taskTitle || '').slice(0, 100),
              role: d.role || 'builder',
            }))
          : [];
      }

      if (ctx.reviewFeedback) {
        trace.collaboration.review_feedback = {
          score: Math.max(0, Math.min(100, Number(ctx.reviewFeedback.score) || 0)),
          issues_count: Number(ctx.reviewFeedback.issuesCount) || 0,
          fix_instructions_count: Number(ctx.reviewFeedback.fixInstructionsCount) || 0,
        };
      }

      if (ctx.roleSwitch) {
        trace.collaboration.role_switch = {
          from_role: ctx.roleSwitch.fromRole || null,
          to_role: ctx.roleSwitch.toRole || null,
          trigger: (ctx.roleSwitch.trigger || '').slice(0, 200),
        };
      }

      if (ctx.sessionId) trace.collaboration.session_id = ctx.sessionId;
      if (ctx.teamSize) trace.collaboration.team_size = Math.max(0, Number(ctx.teamSize) || 0);
    }
  }

  // Timestamp
  trace.created_at = new Date().toISOString();

  return trace;
}

module.exports = {
  buildExecutionTrace,
  desensitizeFilePath,
  extractErrorSignature,
  inferToolChain,
  classifyBlastLevel,
  getTraceLevel,
};
