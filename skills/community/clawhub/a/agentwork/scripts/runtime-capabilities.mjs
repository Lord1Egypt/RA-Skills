import { checkNodePackage } from './runtime-node-packages.mjs';
import {
  AGENTKIT_REQUIRED_ENV,
  resolveAgentkitSpecifier,
  validateAgentkitModule,
} from './signers/agentkit.mjs';

function readOptionalString(value) {
  if (typeof value !== 'string') return null;
  const normalized = value.trim();
  return normalized.length > 0 ? normalized : null;
}

function manualStatusBase(message) {
  return {
    remediation_kind: 'manual',
    approval_required: false,
    install_ready: false,
    install_command: null,
    message,
  };
}

function missingEnvStatus(name, message) {
  return {
    ok: false,
    type: 'env',
    name,
    label: name,
    ...manualStatusBase(message),
  };
}

function missingArgOrEnvStatus(argName, envName, message) {
  return {
    ok: false,
    type: 'argOrEnv',
    arg: argName,
    env: envName,
    label: `--${argName} or ${envName}`,
    ...manualStatusBase(message),
  };
}

function missingModuleStatus(specifier, message) {
  return {
    ok: false,
    type: 'nodeImport',
    specifier,
    label: '@coinbase/agentkit',
    ...manualStatusBase(message),
  };
}

function checkEnv(name, requirement) {
  if (readOptionalString(process.env[name])) {
    return {
      ok: true,
      type: 'env',
      name,
      source: 'env',
    };
  }
  return missingEnvStatus(name, requirement.message ?? `${name} is required`);
}

function checkArgOrEnv(requirement, options = {}) {
  const argValue = readOptionalString(options.args?.[requirement.arg]);
  if (argValue) {
    return {
      ok: true,
      type: 'argOrEnv',
      arg: requirement.arg,
      env: requirement.env,
      source: 'arg',
      value: argValue,
    };
  }

  const envValue = readOptionalString(process.env[requirement.env]);
  if (envValue) {
    return {
      ok: true,
      type: 'argOrEnv',
      arg: requirement.arg,
      env: requirement.env,
      source: 'env',
      value: envValue,
    };
  }

  return missingArgOrEnvStatus(
    requirement.arg,
    requirement.env,
    requirement.message ?? `--${requirement.arg} or ${requirement.env} is required`,
  );
}

async function checkAgentkitModule(requirement) {
  const specifier = resolveAgentkitSpecifier();
  try {
    const agentkit = await import(specifier);
    const validation = validateAgentkitModule(agentkit);
    if (!validation.ok) {
      return missingModuleStatus(
        specifier,
        validation.message ?? 'agentkit signer requires a compatible @coinbase/agentkit module',
      );
    }

    return {
      ok: true,
      type: 'nodeImport',
      specifier,
      label: '@coinbase/agentkit',
      source: 'system',
    };
  } catch (error) {
    return missingModuleStatus(
      specifier,
      requirement.message ?? error?.message ?? 'agentkit signer requires @coinbase/agentkit',
    );
  }
}

export const CAPABILITIES = {
  'evm.core': {
    description: 'Local EVM wallet operations backed by ethers',
    checks: [
      { type: 'nodeImport', specifier: 'ethers' },
    ],
  },
  'signer.agentkit': {
    description: 'Coinbase AgentKit signer runtime',
    checks: [
      {
        type: 'agentkitModule',
        message: 'agentkit signer requires @coinbase/agentkit to be available in the runtime environment',
      },
      ...AGENTKIT_REQUIRED_ENV.map((name) => ({
        type: 'env',
        name,
        message: `${name} is required for agentkit signer`,
      })),
    ],
  },
  'executor.onchainos-gateway': {
    description: 'OnchainOS gateway raw transaction executor',
    checks: [
      {
        type: 'argOrEnv',
        arg: 'base-url',
        env: 'OKX_ONCHAINOS_GATEWAY_URL',
        message: '--base-url or OKX_ONCHAINOS_GATEWAY_URL is required for onchainos-gateway executor',
      },
      {
        type: 'env',
        name: 'OKX_API_KEY',
        message: 'OKX_API_KEY is required for onchainos-gateway executor',
      },
      {
        type: 'env',
        name: 'OKX_SECRET_KEY',
        message: 'OKX_SECRET_KEY is required for onchainos-gateway executor',
      },
      {
        type: 'env',
        name: 'OKX_PASSPHRASE',
        message: 'OKX_PASSPHRASE is required for onchainos-gateway executor',
      },
    ],
  },
};

export async function checkCapability(name, options = {}) {
  const definition = CAPABILITIES[name];
  if (!definition) {
    throw new Error(`Unknown capability: ${name}`);
  }

  const checks = [];
  for (const requirement of definition.checks) {
    if (requirement.type === 'nodeImport') {
      checks.push(await checkNodePackage(requirement.specifier, options));
      continue;
    }
    if (requirement.type === 'env') {
      checks.push(checkEnv(requirement.name, requirement));
      continue;
    }
    if (requirement.type === 'argOrEnv') {
      checks.push(checkArgOrEnv(requirement, options));
      continue;
    }
    if (requirement.type === 'agentkitModule') {
      checks.push(await checkAgentkitModule(requirement));
      continue;
    }

    throw new Error(`Unsupported capability check type: ${requirement.type}`);
  }

  const missing = checks.filter((entry) => !entry.ok);
  if (missing.length > 0) {
    const primary = missing[0];
    return {
      ok: false,
      error_code: 'CAPABILITY_MISSING',
      capability: name,
      description: definition.description,
      missing,
      approval_required: missing.some((entry) => entry.approval_required === true),
      runtime_node_prefix: primary.runtime_node_prefix ?? null,
      remediation: missing[0],
    };
  }

  return {
    ok: true,
    capability: name,
    description: definition.description,
    checks,
    runtime_node_prefix: checks[0]?.runtime_node_prefix ?? null,
  };
}
