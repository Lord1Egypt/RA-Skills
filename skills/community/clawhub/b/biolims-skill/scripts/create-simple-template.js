#!/usr/bin/env node
/**
 * create-simple-template.js - Helper script to create simplified experiment templates
 *
 * Usage:
 *   node create-simple-template.js <template name> <experiment type ID> <experiment group ID> [approver ID] [approver name]
 *
 * Example:
 *   node create-simple-template.js "First Dosing" SYLX2026000002 GLY admin Administrator
 *
 * Output:
 *   Generates a JSON file to /home/biolims/.openclaw/workspace/temp/create-et-<timestamp>.json
 *   and returns the file path, which can be used directly with the biolims.mjs et-create command
 */

const fs = require('fs');
const path = require('path');

const [,, templateName, experimentType, experimentGroup, auditor = 'admin', auditorName = 'Administrator'] = process.argv;

if (!templateName || !experimentType || !experimentGroup) {
  console.log('Missing required parameters');
  console.log('');
  console.log('Usage:');
  console.log('  node create-simple-template.js <template name> <experiment type ID> <experiment group ID> [approver ID] [approver name]');
  console.log('');
  console.log('Example:');
  console.log('  node create-simple-template.js "First Dosing" SYLX2026000002 GLY admin Administrator');
  console.log('');
  console.log('Parameters:');
  console.log('  Template name      - Name of the template (required)');
  console.log('  Experiment type ID - Obtained from experiment-type-config-list (required)');
  console.log('  Experiment group ID - Usually GLY (admin personnel group) (required)');
  console.log('  Approver ID        - Approver username (optional, default: admin)');
  console.log('  Approver name      - Approver display name (optional, default: Administrator)');
  process.exit(1);
}

// Get experiment type name (inferred from ID)
const expTypeNames = {
  'SYLX2026000001': 'Protein Detection',
  'SYLX2026000002': 'Dosing and Observation',
  'SYLX2026000003': 'Animal Modeling',
  'SYLX2026000004': 'Cell Phenotype',
  'SYLX2026000005': 'Molecular Detection',
  'SYLX2026000006': 'Drug Treatment',
  'SYLX2026000007': 'Cell Culture',
  'SYLX2026000008': 'Cell Operation'
};

const experimentTypeName = expTypeNames[experimentType] || 'Unknown type';

// Get experiment group name
const groupNames = {
  'GLY': 'Admin Personnel Group'
};

const experimentGroupName = groupNames[experimentGroup] || experimentGroup;

// Build simplified template structure (one step + detail table + result table)
const templateData = {
  id: null,
  name: null,
  createTime: null,
  state: null,
  templateName: templateName,
  experimentType: experimentType,
  experimentGroup: experimentGroup,
  experimentGroupName: experimentGroupName,
  stateOptions: '0',
  stepDetails: [
    {
      jsonDatas: [
        {
          exclusiveShow: 0,
          label: 'Detail Table',
          draggLabel: 'Detail Table',
          type: 'detailTable',
          size: '24',
          value: '[]',
          propList: JSON.stringify([
            {label: 'Original Sample Code', prop: 'originalSampleCode', disabled: true, headerType: 'fixed'},
            {label: 'Sample Code', prop: 'sampleCode', disabled: true, headerType: 'fixed'},
            {label: 'Sample Type', prop: 'sampleType', disabled: true, headerType: 'fixed'},
            {label: '', prop: 'sampleTypeId', disabled: true, show: true},
            {label: 'Test Item', prop: 'testProjectName', disabled: true, headerType: 'fixed'},
            {label: 'Product Type', prop: 'productType', disabled: true, headerType: 'fixed'},
            {label: 'Product Qty', prop: 'productNum', disabled: true, headerType: 'fixed'},
            {label: 'Mix Sample', prop: 'mixNumber', disabled: true, show: true, headerType: 'fixed'},
            {label: 'index', prop: 'indexCode', disabled: true, show: true, headerType: 'fixed'},
            {label: 'Remaining Qty', prop: 'sumTotal', type: 'number', disabled: false, show: true, headerType: 'fixed'},
            {label: 'Unit', prop: 'sampleUnit', disabled: true, show: true, headerType: 'fixed'},
            {label: 'Storage Status', prop: 'storageState', disabled: true, show: true, headerType: 'fixed'},
            {label: 'Detection Gene', prop: 'detectionGene', disabled: true, headerType: 'fixed'},
            {label: 'Is Split', prop: 'isSplit', disabled: true, show: true, headerType: 'fixed'},
            {label: 'Split Quantity', prop: 'splitQuantity', disabled: true, show: true, headerType: 'fixed'},
            {label: 'Split Product', prop: 'splitProportion', disabled: true, show: true, headerType: 'fixed'}
          ]),
          menuList: '[]',
          productList: '[]',
          plate: '',
          formula: JSON.stringify({formX: [], formY: []}),
          keyId: 0
        },
        {
          exclusiveShow: 0,
          label: 'Result Table',
          draggLabel: 'Result Table',
          type: 'resultTable',
          size: '24',
          value: '[]',
          propList: JSON.stringify([
            {label: 'Original Sample Code', prop: 'originalSampleCode', disabled: true, headerType: 'fixed'},
            {label: 'Sample Code', prop: 'sampleCode', disabled: true, headerType: 'fixed'},
            {label: 'Sample Type', prop: 'sampleType', disabled: true, headerType: 'fixed'},
            {label: 'Test Item', prop: 'testProjectName', disabled: true, headerType: 'fixed'},
            {label: 'Volume', prop: 'volume', type: 'number', headerType: 'fixed'},
            {label: 'Total', prop: 'total', type: 'number', headerType: 'fixed'},
            {label: 'Unit', prop: 'sampleUnit', disabled: true, headerType: 'fixed'},
            {label: 'Next Flow', prop: 'nextFlow', disabled: true, headerType: 'fixed', required: true},
            {label: 'Result', prop: 'result', disabled: true, required: 1, headerType: 'fixed'},
            {label: 'Submit QC', prop: 'tjzk', disabled: true, headerType: 'fixed'},
            {label: 'Detection Gene', prop: 'detectionGene', disabled: true, headerType: 'fixed'}
          ]),
          menuList: '[]',
          productList: '[]',
          plate: '',
          formula: JSON.stringify({formX: [], formY: []}),
          itemIndex: 1,
          keyId: 1
        }
      ],
      name: null,
      keyId: 0
    }
  ],
  auditor: auditor,
  auditorName: auditorName,
  experimentalType: experimentType,
  experimentTypeName: experimentTypeName,
  logArrays: [
    {
      id: null,
      type: 'main',
      flag: '',
      logs: `Experiment Template:<br>'Template Name' :from' Empty 'changed to' ${templateName} '<br>'Experiment Type' :from' Empty 'changed to' ${experimentTypeName} '<br>'Experiment Group' :from' Empty 'changed to' ${experimentGroupName} '<br>'Approver' :from' Empty 'changed to' ${auditorName} '`
    },
    {type: 'step', flag: '1', logs: '1'},
    {
      type: 'detailTable',
      flag: '1',
      logs: `Detail:<br>'Component Name' :from' Empty 'changed to' Detail Table '<br>'Header' :from' Empty 'changed to' Original Sample Code，Sample Code，Sample Type，,Test Item，Product Type，Product Qty，Mix Sample，index，Remaining Qty，Unit，Storage Status，Detection Gene，Is Split，Split Quantity，Split Product '`
    },
    {type: 'detailTable', flag: '1', logs: []},
    {
      type: 'resultTable',
      flag: '1',
      logs: `Result:<br>'Component Name' :from' Empty 'changed to' Result Table '<br>'Header' :from' Empty 'changed to' Original Sample Code，Sample Code，Sample Type，Test Item，Volume，Total，Unit，Next Flow，Result，Submit QC，Detection Gene '`
    },
    {type: 'resultTable', flag: '1', logs: []}
  ]
};

// Generate output file path
const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
const outputDir = '/home/biolims/.openclaw/workspace/temp';
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}
const outputPath = path.join(outputDir, `create-et-${timestamp}.json`);

// Write file
fs.writeFileSync(outputPath, JSON.stringify(templateData, null, 2), 'utf8');

console.log('Template JSON file generated');
console.log('');
console.log('File path:', outputPath);
console.log('');
console.log('Template info:');
console.log('   Name:', templateName);
console.log('   Type:', experimentTypeName, '(' + experimentType + ')');
console.log('   Group:', experimentGroupName, '(' + experimentGroup + ')');
console.log('   Approver:', auditorName, '(' + auditor + ')');
console.log('');
console.log('Next step:');
console.log('   node biolims.mjs et-create @' + outputPath);
console.log('');

// Output file path (for script invocation)
console.log('FILE:' + outputPath);
