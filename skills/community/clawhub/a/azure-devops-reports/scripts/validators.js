const path = require('path');

const SAFE_TEXT_RE = /^[\w .()\-\\/]+$/;
const SAFE_ORG_RE = /^[A-Za-z0-9][A-Za-z0-9-]*$/;
const SAFE_FILE_RE = /^[A-Za-z0-9._-]+$/;

const DEFAULT_FIELDS = [
  'System.Id',
  'System.Title',
  'System.State',
  'System.WorkItemType',
  'System.AssignedTo',
  'System.TeamProject',
  'System.IterationPath',
  'System.AreaPath',
  'System.CreatedDate',
  'System.ChangedDate',
  'Microsoft.VSTS.Common.ClosedDate',
  'Microsoft.VSTS.Common.Priority',
  'Microsoft.VSTS.Scheduling.OriginalEstimate',
  'Microsoft.VSTS.Scheduling.RemainingWork',
  'Microsoft.VSTS.Scheduling.StoryPoints',
];

function requireNonEmpty(value, name) {
  if (!value || !String(value).trim()) {
    throw new Error(`${name} is required`);
  }
  return String(value).trim();
}

function validateOrg(org) {
  const value = requireNonEmpty(org, 'AZURE_DEVOPS_ORG');
  if (!SAFE_ORG_RE.test(value)) throw new Error('Invalid Azure DevOps org name');
  return value;
}

function validatePathPart(value, label) {
  const clean = requireNonEmpty(value, label);
  if (!SAFE_TEXT_RE.test(clean)) throw new Error(`Invalid ${label}`);
  return clean;
}

function validateId(value, label = 'id') {
  const str = requireNonEmpty(value, label);
  if (!/^\d+$/.test(str)) throw new Error(`Invalid ${label}`);
  return Number(str);
}

function validateFields(fields) {
  if (!fields || fields.length === 0) return [...DEFAULT_FIELDS];
  const list = Array.isArray(fields) ? fields : String(fields).split(',').map(s => s.trim()).filter(Boolean);
  const allowed = new Set(DEFAULT_FIELDS);
  for (const field of list) {
    if (!allowed.has(field)) throw new Error(`Field not allowed: ${field}`);
  }
  return list;
}

function safeOutputPath(outputDir, filename) {
  const clean = requireNonEmpty(filename, 'output filename');
  if (!SAFE_FILE_RE.test(clean)) throw new Error('Invalid output filename');
  return path.join(outputDir, clean);
}

module.exports = {
  DEFAULT_FIELDS,
  validateOrg,
  validatePathPart,
  validateId,
  validateFields,
  safeOutputPath,
  requireNonEmpty,
};
