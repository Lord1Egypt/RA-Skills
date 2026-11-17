'use strict';
const fs = require('fs');
const path = require('path');

function exportPublishPackage(targetIds, outPath) {
  const genesFile = path.join('.evolver', 'gep', 'genes.json');
  const capsulesFile = path.join('.evolver', 'gep', 'capsules.json');

  const genes = JSON.parse(fs.readFileSync(genesFile, 'utf8'));
  const capsules = JSON.parse(fs.readFileSync(capsulesFile, 'utf8'));

  const geneList = genes.genes || genes;
  const capsuleList = capsules.capsules || capsules;

  const out = {
    package_name: 'Local Evolution Publish Package',
    generated_at: new Date().toISOString(),
    assets: []
  };

  for (const g of geneList) {
    if (!targetIds.includes(g.id)) continue;
    out.assets.push({
      type: 'Gene',
      id: g.id,
      category: g.category,
      summary: g.summary || '',
      signals_match: g.signals_match || [],
      strategy: g.strategy || [],
      validation: g.validation || [],
      constraints: g.constraints || {},
      preconditions: g.preconditions || []
    });
  }

  for (const c of capsuleList) {
    if (!targetIds.includes(c.id)) continue;
    out.assets.push({
      type: 'Capsule',
      id: c.id,
      gene: c.gene || null,
      summary: c.summary || '',
      trigger: c.trigger || [],
      outcome: c.outcome || {},
      blast_radius: c.blast_radius || {},
      execution_trace: c.execution_trace || []
    });
  }

  const outAbs = path.resolve(outPath);
  fs.writeFileSync(outAbs, JSON.stringify(out, null, 2));
  console.log('Exported ' + out.assets.length + ' assets to ' + outAbs);
}

function showHelp() {
  console.log('Usage: node publish-package.js --genes=<id1>,<id2> --out=<path>');
  console.log('Example: node publish-package.js --genes=gene_distilled_protocol-drift-repeated-tool-usage,capsule_1780307670667 --out=memory/evolution/publish-package.json');
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
  showHelp();
  process.exit(0);
}

let geneIds = [];
let outPath = path.join('memory', 'evolution', 'publish-package.json');

for (const a of args) {
  if (a.startsWith('--genes=')) geneIds = a.slice(8).split(',');
  if (a.startsWith('--out=')) outPath = a.slice(6);
}

if (!geneIds.length) {
  console.error('Error: --genes is required');
  showHelp();
  process.exit(1);
}

exportPublishPackage(geneIds, outPath);
