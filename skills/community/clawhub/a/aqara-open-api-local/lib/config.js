const fs = require('fs');
const os = require('os');
const path = require('path');

const { cliError } = require('./errors');

const packageRootPath = path.resolve(__dirname, '..');

function resolveDefaultCliConfigPath() {
  return path.join(os.homedir(), '.aqa', 'config.json');
}

function stripJsonc(sourceText) {
  let outputText = '';
  let inString = false;
  let escapeNext = false;
  let inLineComment = false;
  let inBlockComment = false;

  for (let index = 0; index < sourceText.length; index += 1) {
    const currentCharacter = sourceText[index];
    const nextCharacter = sourceText[index + 1] || '';

    if (inLineComment) {
      if (currentCharacter === '\n') {
        inLineComment = false;
        outputText += currentCharacter;
      }
      continue;
    }

    if (inBlockComment) {
      if (currentCharacter === '*' && nextCharacter === '/') {
        inBlockComment = false;
        index += 1;
      }
      continue;
    }

    if (inString) {
      outputText += currentCharacter;
      if (escapeNext) {
        escapeNext = false;
      } else if (currentCharacter === '\\') {
        escapeNext = true;
      } else if (currentCharacter === '"') {
        inString = false;
      }
      continue;
    }

    if (currentCharacter === '"') {
      inString = true;
      outputText += currentCharacter;
      continue;
    }

    if (currentCharacter === '/' && nextCharacter === '/') {
      inLineComment = true;
      index += 1;
      continue;
    }

    if (currentCharacter === '/' && nextCharacter === '*') {
      inBlockComment = true;
      index += 1;
      continue;
    }

    outputText += currentCharacter;
  }

  return outputText;
}

function readCliConfig() {
  const configPath = resolveDefaultCliConfigPath();
  if (!configPath || !fs.existsSync(configPath)) {
    return {
      configPath,
      config: {},
    };
  }

  let rawConfigText = '';
  try {
    rawConfigText = fs.readFileSync(configPath, 'utf8');
  } catch (error) {
    throw cliError('CONFIG_ERROR', `failed to read CLI config: ${configPath}`, {
      path: configPath,
      cause: error.message,
    });
  }

  let parsedConfig = {};
  try {
    parsedConfig = JSON.parse(stripJsonc(rawConfigText));
  } catch (error) {
    throw cliError('CONFIG_ERROR', `failed to parse CLI config: ${configPath}`, {
      path: configPath,
      cause: error.message,
    });
  }

  return {
    configPath,
    config: parsedConfig && typeof parsedConfig === 'object'
      ? parsedConfig
      : {},
  };
}

function ensureConfigDirectory(configPath) {
  const parentDirectoryPath = path.dirname(configPath);
  fs.mkdirSync(parentDirectoryPath, { recursive: true });
}

function writeCliConfig(nextConfig) {
  const configPath = resolveDefaultCliConfigPath();
  ensureConfigDirectory(configPath);
  fs.writeFileSync(configPath, `${JSON.stringify(nextConfig, null, 2)}\n`, 'utf8');
  return {
    configPath,
    config: nextConfig,
  };
}

function updateCliConfig(updater) {
  const { config } = readCliConfig();
  const nextConfig = updater({
    ...(config && typeof config === 'object' ? config : {}),
  });
  return writeCliConfig(nextConfig);
}

function maskToken(token) {
  const stringToken = String(token || '');
  if (!stringToken) {
    return '';
  }
  if (stringToken.length <= 8) {
    return '*'.repeat(stringToken.length);
  }
  return `${stringToken.slice(0, 4)}...${stringToken.slice(-4)}`;
}

function getRuntimeConfig(options = {}) {
  const { allowMissing = false } = options;
  const { configPath, config } = readCliConfig();

  const endpointUrl = process.env.AQARA_ENDPOINT_URL || config.endpointUrl || config.AQARA_ENDPOINT_URL || '';
  const token = process.env.AQARA_OPEN_API_TOKEN || config.token || config.AQARA_OPEN_API_TOKEN || '';
  const endpointSource = process.env.AQARA_ENDPOINT_URL ? 'env' : (endpointUrl ? 'config' : 'missing');
  const tokenSource = process.env.AQARA_OPEN_API_TOKEN ? 'env' : (token ? 'config' : 'missing');

  if (!allowMissing) {
    const missingKeys = [];
    if (!endpointUrl) {
      missingKeys.push('AQARA_ENDPOINT_URL');
    }
    if (!token) {
      missingKeys.push('AQARA_OPEN_API_TOKEN');
    }
    if (missingKeys.length > 0) {
      throw cliError('NO_TOKEN', 'missing Aqara Open API credentials', {
        missingKeys,
        configPath,
        help: 'Set AQARA_ENDPOINT_URL and AQARA_OPEN_API_TOKEN in the current environment, or run `aqara config set-endpoint <url>` and `aqara config set-token <token>`.',
      });
    }
  }

  return {
    endpointUrl,
    token,
    endpointSource,
    tokenSource,
    configPath,
    packageRootPath,
    cachePath: path.join(packageRootPath, 'data', 'devices.json'),
    traitCodesPath: path.join(packageRootPath, 'assets', 'trait-codes.md'),
  };
}

module.exports = {
  getRuntimeConfig,
  maskToken,
  packageRootPath,
  readCliConfig,
  resolveDefaultCliConfigPath,
  stripJsonc,
  updateCliConfig,
  writeCliConfig,
};
