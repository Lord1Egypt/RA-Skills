/**
 * OpenClaw Plugin Entry Point for Crypto Price Prediction
 * Calls the Python prediction script and returns unified JSON
 */

const { spawn } = require('child_process');
const path = require('path');

const SCRIPT_PATH = path.join(__dirname, 'scripts', 'predict.py');
const PYTHON_CMD = process.env.PYTHON_CMD || 'python3';

const COIN_MAP = {
  'BTCUSDT': 'BTC',
  'ETHUSDT': 'ETH',
};

/**
 * Predict crypto price using the Python script
 * @param {Object} params - { symbol: string, hours: number, timezone: string }
 * @returns {Promise<Object>} Unified prediction result
 */
async function predictPrice(params) {
  const symbol = (params?.symbol || 'BTCUSDT').toUpperCase();
  const hours = Number(params?.hours ?? 1.0);
  const timezone = params?.timezone; // optional, will prompt if not provided

  // Validate
  if (!COIN_MAP[symbol]) {
    throw new Error(`Unsupported symbol: ${symbol}. Supported: ${Object.keys(COIN_MAP).join(', ')}`);
  }
  if (hours <= 0 || hours > 24) {
    throw new Error('Hours must be between 0.1 and 24');
  }

  // This API only provides next-hour prediction
  if (hours !== 1) {
    console.warn(`Note: API only provides 1-hour prediction, ignoring hours=${hours}`);
  }

  const coin = COIN_MAP[symbol];

  return new Promise((resolve, reject) => {
    const args = [SCRIPT_PATH, '--coin', coin];
    if (timezone) {
      args.push('--timezone', timezone);
    }
    const proc = spawn(PYTHON_CMD, args, { stdio: ['ignore', 'pipe', 'pipe'] });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (data) => { stdout += data.toString(); });
    proc.stderr.on('data', (data) => { stderr += data.toString(); });

    proc.on('close', (code) => {
      if (code === 0) {
        try {
          // Parse JSON from stdout (first line should be JSON)
          const lines = stdout.trim().split('\n');
          const jsonLine = lines[0];
          const result = JSON.parse(jsonLine);
          
          // Ensure symbol format matches input
          result.symbol = symbol;
          resolve(result);
        } catch (e) {
          reject(new Error(`Failed to parse JSON output: ${stdout.trim()}`));
        }
      } else {
        reject(new Error(`Prediction failed (exit ${code}): ${stderr.trim() || stdout.trim()}`));
      }
    });

    proc.on('error', (err) => {
      reject(new Error(`Failed to spawn prediction script: ${err.message}`));
    });
  });
}

module.exports = {
  tools: {
    predictPrice,
  },
};