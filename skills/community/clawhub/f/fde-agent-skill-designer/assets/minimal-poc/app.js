'use strict';

const input = document.querySelector('#task-input');
const status = document.querySelector('#status');
const evidence = document.querySelector('#evidence');
const decision = document.querySelector('#decision');
const humanAction = document.querySelector('#human-action');
const externalAction = document.querySelector('#external-action');
const result = document.querySelector('#result');

function render(value) {
  status.className = `status ${value.status}`;
  status.textContent = value.status === 'ready' ? 'Generated · Waiting for manual review' : 'Blocked · Need to re-certify or upgrade';
  evidence.textContent = value.evidence;
  decision.textContent = value.decision;
  humanAction.textContent = value.human_action;
  externalAction.textContent = value.external_action ? 'Triggered' : 'Not enabled';
  result.textContent = value.output;
}

document.querySelector('#run').addEventListener('click', () => render(window.PocLogic.run(input.value)));
document.querySelector('#clear').addEventListener('click', () => {
  input.value = '';
  status.className = 'status idle';
  status.textContent = 'waiting for input';
  evidence.textContent = decision.textContent = humanAction.textContent = '—';
  externalAction.textContent = 'Not enabled';
  result.textContent = 'Not running yet.';
});
document.querySelector('#load-example').addEventListener('click', () => {
  input.value = 'Example task: Based on confirmed customer materials, organize facts, items to be confirmed and recommend next actions. All results must be manually reviewed.';
});
