#!/usr/bin/env node
// Executes reviewed candidate code. Node vm is NOT a security sandbox.
'use strict';
const fs = require('fs');
const vm = require('vm');
const crypto = require('crypto');
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const own = (o, k) => o != null && Object.hasOwn(o, k);
const controls = new Set(['code', 'codeType', 'system_addInputParam']);
function subset(actual, expected) {
  if (Array.isArray(expected)) return Array.isArray(actual) && actual.length === expected.length && expected.every((x, i) => subset(actual[i], x));
  if (expected && typeof expected === 'object') return actual && typeof actual === 'object' && Object.keys(expected).every(k => own(actual, k) && subset(actual[k], expected[k]));
  return Object.is(actual, expected);
}
function fail(message) { throw Error(message); }
function nodeById(workflow, id) {
  const node = workflow.nodes.find(n => n.nodeId === id);
  if (!node) fail('node_missing:' + id);
  return node;
}
function executeCode(node, input) {
  if (node.flowNodeType !== 'code') fail('code_node_required');
  const code = node.inputs.find(i => i.key === 'code')?.value;
  if (typeof code !== 'string') fail('code_source_missing');
  const context = vm.createContext({ input: JSON.parse(JSON.stringify(input)) });
  vm.runInContext(code, context, { timeout: 1000 });
  return JSON.parse(vm.runInContext('(() => { const result = main(input); if (result && typeof result.then === "function") throw Error("async_main_not_supported"); return JSON.stringify(result); })()', context, { timeout: 1000 }));
}
function declaredOutput(node, field) {
  return (node.outputs || []).find(o => o.id === field);
}
function resolveReference(workflow, state, variables, source, field) {
  if (source === 'VARIABLE_NODE_ID') {
    const config = (workflow.chatConfig?.variables || []).find(v => v.key === field);
    if (!config) fail('variable_not_declared:' + field);
    if (own(variables, field)) return variables[field];
    if (own(config, 'defaultValue')) return config.defaultValue;
    fail('variable_unresolved:' + field);
  }
  const node = nodeById(workflow, source);
  const output = declaredOutput(node, field);
  if (!output) fail('reference_not_declared:' + source + '.' + field);
  if (!own(state, source) || !own(state[source], output.key)) fail('reference_unresolved:' + source + '.' + field);
  return state[source][output.key];
}
function display(value) {
  if (value == null) return '';
  return typeof value === 'string' ? value : JSON.stringify(value);
}
function bindInputs(workflow, node, state, variables) {
  const input = {};
  for (const item of node.inputs || []) {
    if (controls.has(item.key)) continue;
    let value;
    if (own(item, 'value')) value = item.value;
    else if (own(item, 'defaultValue')) value = item.defaultValue;
    else if (item.required) fail('input_value_missing:' + node.nodeId + '.' + item.key);
    else continue;
    if ((item.renderTypeList || []).includes('reference') && Array.isArray(value)) {
      if (value.length !== 2 || value.some(v => typeof v !== 'string' || !v)) fail('reference_shape_invalid:' + item.key);
      value = resolveReference(workflow, state, variables, value[0], value[1]);
    } else if (typeof value === 'string') {
      value = value.replace(/\{\{\$([^{}]+?)\$\}\}/g, (_, body) => {
        const dot = body.indexOf('.');
        if (dot < 1) fail('template_reference_invalid');
        return display(resolveReference(workflow, state, variables, body.slice(0, dot), body.slice(dot + 1)));
      });
    }
    input[item.key] = value;
  }
  return input;
}
function inputReferences(node) {
  const refs = [];
  for (const item of node.inputs || []) {
    if ((item.renderTypeList || []).includes('reference') && Array.isArray(item.value) && item.value.length === 2) refs.push(item.value);
    if (typeof item.value === 'string') for (const m of item.value.matchAll(/\{\{\$([^{}]+?)\$\}\}/g)) {
      const dot = m[1].indexOf('.');
      if (dot > 0) refs.push([m[1].slice(0, dot), m[1].slice(dot + 1)]);
    }
  }
  return refs;
}
function boundCase(workflow, c) {
  if (own(c, 'input')) fail('bound_mode_disallows_manual_input');
  const steps = c.steps || [c.node_id];
  if (!Array.isArray(steps) || !steps.length || new Set(steps).size !== steps.length) fail('invalid_data_steps');
  const state = JSON.parse(JSON.stringify(c.seeds || {}));
  const variables = c.variables || {};
  for (const key of Object.keys(state)) {
    const node = nodeById(workflow, key);
    if (steps.includes(key)) fail('cannot_seed_executed_step:' + key);
    for (const field of Object.keys(state[key])) if (!(node.outputs || []).some(o => o.key === field)) fail('seed_output_not_declared:' + key + '.' + field);
  }
  for (const key of Object.keys(variables)) if (!(workflow.chatConfig?.variables || []).some(v => v.key === key)) fail('variable_override_not_declared:' + key);
  let actual;
  for (const id of steps) {
    const node = nodeById(workflow, id);
    for (const key of (c.required_inputs || {})[id] || []) {
      if (!(node.inputs || []).some(i => i.key === key && !controls.has(key))) fail('input_not_declared:' + id + '.' + key);
    }
    const args = bindInputs(workflow, node, state, variables);
    for (const key of (c.required_inputs || {})[id] || []) if (!own(args, key)) fail('input_value_missing:' + id + '.' + key);
    if (node.flowNodeType === 'code') actual = executeCode(node, args);
    else if (node.flowNodeType === 'answerNode') actual = { text: display(args.text) };
    else fail('unsupported_data_step:' + node.flowNodeType); // Never execute HTTP or condition nodes.
    state[id] = actual;
  }
  const last = nodeById(workflow, steps[steps.length - 1]);
  const refs = inputReferences(last);
  for (const required of c.required_references || []) {
    if (!Array.isArray(required) || required.length !== 2 || !refs.some(r => r[0] === required[0] && r[1] === required[1])) fail('required_reply_reference_missing');
  }
  return { actual, steps };
}
function run(workflow, contract) {
  if (!contract || !Array.isArray(contract.cases) || !contract.cases.length) fail('nonempty cases required');
  const results = contract.cases.map(c => {
    const mode = c.mode || 'direct';
    try {
      if (!c.name) fail('name_required');
      const hasExpected = c.expected && typeof c.expected === 'object' && Object.keys(c.expected).length > 0;
      const hasText = Array.isArray(c.contains_all) && c.contains_all.length > 0 && c.contains_all.every(t => typeof t === 'string' && t.length > 0);
      if (!hasExpected && !hasText) fail('nonempty expected or contains_all required');
      let actual, steps = [];
      if (mode === 'direct') {
        if (!c.node_id || !c.input || typeof c.input !== 'object') fail('node_id/input required');
        actual = executeCode(nodeById(workflow, c.node_id), c.input);
      } else if (mode === 'bound') ({ actual, steps } = boundCase(workflow, c));
      else fail('unknown_mode');
      if (hasExpected && !subset(actual, c.expected)) return { name: c.name, mode, passed: false, error: 'expected_mismatch', actual };
      if (c.forbidden && Object.keys(c.forbidden).some(k => subset(actual[k], c.forbidden[k]))) return { name: c.name, mode, passed: false, error: 'forbidden_value', actual };
      const text = actual[c.text_field || 'text'];
      if (hasText && (typeof text !== 'string' || !c.contains_all.every(s => text.includes(s)))) return { name: c.name, mode, passed: false, error: 'reply_text_incomplete', actual };
      if (Array.isArray(c.not_contains) && typeof text === 'string' && c.not_contains.some(s => text.includes(s))) return { name: c.name, mode, passed: false, error: 'reply_forbidden_text', actual };
      return { name: c.name, mode, passed: true, steps_executed: steps };
    } catch (e) { return { name: c.name, mode, passed: false, error: String(e.message) }; }
  });
  return { passed: results.every(r => r.passed), cases: results,
    scope: 'direct=manual code inputs; bound=JSON input references and explicit data steps with mocked seeds and local answer rendering; no condition evaluation, HTTP execution, platform import or loop runtime verification' };
}
if (require.main === module) {
  if (process.argv.includes('--help')) console.log('node run_code_contract.js workflow.json contract.json [report.json] — reviewed code only; modes direct/bound; vm is not a security sandbox');
  else try {
    const [workflowPath, contractPath, output] = process.argv.slice(2);
    const wb = fs.readFileSync(workflowPath), cb = fs.readFileSync(contractPath);
    const report = { ...run(JSON.parse(wb), JSON.parse(cb)), executed_at: new Date().toISOString(), workflow_sha256: hash(wb), contract_sha256: hash(cb) };
    const text = JSON.stringify(report, null, 2) + '\n';
    if (output) fs.writeFileSync(output, text);
    process.stdout.write(text);
    process.exitCode = report.passed ? 0 : 1;
  } catch (e) { console.error(String(e.message)); process.exitCode = 1; }
}
module.exports = { run, subset, bindInputs };
