#!/usr/bin/env node

/**
 * Chart Splat - Chart Generation Script
 *
 * Usage:
 *   node generate-chart.js <type> <labels> <data> [title] [output]
 *
 * Examples:
 *   node generate-chart.js bar "Q1,Q2,Q3,Q4" "50,75,60,90" "Revenue" chart.png
 *   node generate-chart.js line "Mon,Tue,Wed" "10,20,15"
 *   node generate-chart.js pie "A,B,C" "30,50,20" "" pie.png
 *   node generate-chart.js --config chart-config.json -o chart.png
 */

const fs = require('fs');

const API_URL = process.env.CHARTSPLAT_API_URL || 'https://api.chartsplat.com';
const API_KEY = process.env.CHARTSPLAT_API_KEY;

if (!API_KEY) {
  console.error('Error: CHARTSPLAT_API_KEY environment variable is required');
  console.error('Get your API key at https://chartsplat.com/dashboard/api-keys');
  process.exit(1);
}

const VALID_TYPES = ['line', 'bar', 'pie', 'doughnut', 'radar', 'polarArea'];

async function generateChart(config) {
  const response = await fetch(`${API_URL}/chart`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Api-Key': API_KEY,
    },
    body: JSON.stringify(config),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API error (${response.status}): ${error}`);
  }

  const result = await response.json();
  return result.image;
}

async function main() {
  const args = process.argv.slice(2);

  // Handle --config mode
  const configIdx = args.indexOf('--config');
  if (configIdx !== -1) {
    const configFile = args[configIdx + 1];
    if (!configFile) {
      console.error('Error: --config requires a file path');
      process.exit(1);
    }
    const outputIdx = args.indexOf('-o');
    const output = outputIdx !== -1 ? args[outputIdx + 1] : 'chart.png';
    const config = JSON.parse(fs.readFileSync(configFile, 'utf-8'));
    const image = await generateChart(config);
    const base64 = image.replace(/^data:image\/png;base64,/, '');
    fs.writeFileSync(output, Buffer.from(base64, 'base64'));
    console.log(`Chart saved to ${output}`);
    return;
  }

  // Positional args mode
  if (args.length < 3) {
    console.error('Usage: generate-chart.js <type> <labels> <data> [title] [output]');
    console.error('       generate-chart.js --config <file> [-o output.png]');
    console.error('');
    console.error(`Chart types: ${VALID_TYPES.join(', ')}`);
    process.exit(1);
  }

  const [type, labelsStr, dataStr, title, output = 'chart.png'] = args;

  if (!VALID_TYPES.includes(type)) {
    console.error(`Error: Invalid chart type '${type}'`);
    console.error(`Valid types: ${VALID_TYPES.join(', ')}`);
    process.exit(1);
  }

  const labels = labelsStr.split(',').map((s) => s.trim());
  const data = dataStr.split(',').map((s) => parseFloat(s.trim()));

  const config = {
    type,
    data: {
      labels,
      datasets: [{ data }],
    },
    options: {
      width: 800,
      height: 600,
      ...(title && {
        plugins: { title: { display: true, text: title } },
      }),
    },
  };

  const image = await generateChart(config);
  const base64 = image.replace(/^data:image\/png;base64,/, '');
  fs.writeFileSync(output, Buffer.from(base64, 'base64'));
  console.log(`Chart saved to ${output}`);
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
