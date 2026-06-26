import { chmodSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const SYSTEM_REQUIRE = createRequire(import.meta.url);
const INSTALLER_SCRIPT_PATH = fileURLToPath(new URL('./runtime-deps.mjs', import.meta.url));

function normalizeVersion(value) {
  if (typeof value !== 'string') return null;
  const normalized = value.trim().replace(/^v/i, '');
  return normalized.length > 0 ? normalized : null;
}

function unwrapModuleCandidates(moduleNamespace) {
  return [
    moduleNamespace,
    moduleNamespace?.default,
    moduleNamespace?.ethers,
    moduleNamespace?.default?.ethers,
  ].filter((candidate, index, list) => candidate && typeof candidate === 'object' && list.indexOf(candidate) === index);
}

function validateEthersModule(moduleNamespace) {
  const candidates = unwrapModuleCandidates(moduleNamespace);
  for (const candidate of candidates) {
    const version = normalizeVersion(candidate.version ?? moduleNamespace?.version ?? moduleNamespace?.default?.version);
    const missingExports = [];
    if (typeof candidate.Interface !== 'function') missingExports.push('Interface');
    if (typeof candidate.JsonRpcProvider !== 'function') missingExports.push('JsonRpcProvider');
    if (typeof candidate.Contract !== 'function') missingExports.push('Contract');
    if (typeof candidate.Signature?.from !== 'function') missingExports.push('Signature.from');
    if (typeof candidate.Wallet?.createRandom !== 'function') missingExports.push('Wallet.createRandom');
    if (typeof candidate.getAddress !== 'function') missingExports.push('getAddress');
    if (typeof candidate.getBytes !== 'function') missingExports.push('getBytes');
    if (typeof candidate.keccak256 !== 'function') missingExports.push('keccak256');
    if (typeof candidate.solidityPacked !== 'function') missingExports.push('solidityPacked');
    if (typeof candidate.toUtf8Bytes !== 'function') missingExports.push('toUtf8Bytes');

    if (version && !version.startsWith('6.')) {
      return {
        ok: false,
        reason: 'unsupported_version',
        version,
        message: `Expected ethers v6, found ${version}`,
        missing_exports: missingExports,
      };
    }

    if (missingExports.length > 0) {
      return {
        ok: false,
        reason: 'missing_exports',
        version,
        message: `Resolved ethers package is missing required v6 exports: ${missingExports.join(', ')}`,
        missing_exports: missingExports,
      };
    }

    return {
      ok: true,
      version,
      exports_checked: [
        'Interface',
        'JsonRpcProvider',
        'Contract',
        'Signature.from',
        'Wallet.createRandom',
        'getAddress',
        'getBytes',
        'keccak256',
        'solidityPacked',
        'toUtf8Bytes',
      ],
    };
  }

  return {
    ok: false,
    reason: 'invalid_namespace',
    version: null,
    message: 'Resolved ethers package did not expose a usable module namespace',
    missing_exports: [],
  };
}

export const NODE_PACKAGE_REGISTRY = {
  ethers: {
    alias: 'ethers',
    installSpecifier: 'ethers@^6',
    label: 'ethers',
    installable: true,
    validate: validateEthersModule,
  },
};

function truthyEnv(name) {
  const value = process.env[name];
  if (typeof value !== 'string') return false;
  const normalized = value.trim().toLowerCase();
  return normalized === '1' || normalized === 'true' || normalized === 'yes' || normalized === 'on';
}

function resolveHomeDir() {
  const home = process.env.HOME?.trim() || os.homedir?.();
  if (!home) {
    throw new Error('Cannot resolve HOME for AgentWork runtime state directory');
  }
  return home;
}

export function resolveStateRoot(options = {}) {
  const explicit = typeof options.stateDir === 'string' ? options.stateDir.trim() : '';
  if (explicit) return path.resolve(explicit);

  const envDir = process.env.AGENTWORK_STATE_DIR?.trim() || process.env.OPENCLAW_STATE_DIR?.trim();
  if (envDir) return path.resolve(envDir);

  return path.join(resolveHomeDir(), '.agentwork');
}

export function resolveRuntimeNodePrefix(options = {}) {
  const explicit = process.env.AGENTWORK_RUNTIME_NODE_PREFIX?.trim();
  if (explicit) return path.resolve(explicit);
  return path.join(resolveStateRoot(options), 'runtime', 'node', 'agentwork');
}

export function systemNodeModulesEnabled() {
  return !truthyEnv('AGENTWORK_DISABLE_SYSTEM_NODE_MODULES');
}

function packageMetadataFor(specifierOrAlias) {
  const metadata = NODE_PACKAGE_REGISTRY[specifierOrAlias];
  if (!metadata) {
    const error = new Error(`Unsupported runtime package: ${specifierOrAlias}`);
    error.code = 'UNKNOWN_RUNTIME_PACKAGE';
    error.details = {
      package: specifierOrAlias,
      supported: Object.keys(NODE_PACKAGE_REGISTRY),
    };
    throw error;
  }
  return metadata;
}

function ensureRuntimePackageRoot(prefix) {
  mkdirSync(prefix, { recursive: true, mode: 0o700 });
  try {
    chmodSync(prefix, 0o700);
  } catch {
    // best effort
  }

  const packageJsonPath = path.join(prefix, 'package.json');
  if (!existsSync(packageJsonPath)) {
    writeFileSync(
      packageJsonPath,
      `${JSON.stringify(
        {
          name: 'agentwork-wallet-runtime',
          private: true,
          type: 'module',
        },
        null,
        2,
      )}\n`,
      { encoding: 'utf8', mode: 0o600 },
    );
  }
}

function tryResolveWithRequire(requireImpl, specifier) {
  try {
    return requireImpl.resolve(specifier);
  } catch {
    return null;
  }
}

function resolveLocalPackagePath(specifier, options = {}) {
  const prefix = resolveRuntimeNodePrefix(options);
  ensureRuntimePackageRoot(prefix);
  const localRequire = createRequire(path.join(prefix, 'package.json'));
  const resolved = tryResolveWithRequire(localRequire, specifier);
  if (!resolved) return null;
  return {
    source: 'local-runtime',
    resolved,
    runtimeNodePrefix: prefix,
  };
}

function resolveSystemPackagePath(specifier) {
  const resolved = tryResolveWithRequire(SYSTEM_REQUIRE, specifier);
  if (!resolved) return null;
  return {
    source: 'system',
    resolved,
    runtimeNodePrefix: null,
  };
}

export function buildInstallCommand(packageAlias = 'ethers') {
  const metadata = packageMetadataFor(packageAlias);
  if (metadata.installable === false) {
    const error = new Error(`Runtime package ${metadata.alias} is not installable via runtime-deps.mjs`);
    error.code = 'RUNTIME_PACKAGE_NOT_INSTALLABLE';
    error.details = {
      package: metadata.alias,
    };
    throw error;
  }
  return [process.execPath, INSTALLER_SCRIPT_PATH, 'install', metadata.alias];
}

function resolveInstallerBinary() {
  const explicit = process.env.AGENTWORK_NPM_BIN?.trim();
  return explicit && explicit.length > 0 ? explicit : 'npm';
}

export function checkInstallerBinary() {
  const installer = resolveInstallerBinary();
  const result = spawnSync(installer, ['--version'], {
    stdio: 'ignore',
    shell: false,
  });

  if (result.error) {
    return {
      ok: false,
      installer,
      reason: result.error.code === 'ENOENT' ? 'missing_bin' : 'spawn_failed',
      message: `${installer} is required on PATH to install AgentWork runtime dependencies`,
    };
  }
  if (result.status !== 0) {
    return {
      ok: false,
      installer,
      reason: 'nonzero_exit',
      message: `${installer} exited with status ${result.status} during readiness check`,
    };
  }

  return {
    ok: true,
    installer,
  };
}

export function buildMissingNodePackageStatus(specifierOrAlias, options = {}) {
  const metadata = packageMetadataFor(specifierOrAlias);
  const installerCheck = metadata.installable === false ? null : checkInstallerBinary();
  return {
    ok: false,
    type: 'nodeImport',
    specifier: metadata.alias,
    install_id: metadata.alias,
    package_specifier: metadata.installSpecifier,
    label: metadata.label,
    remediation_kind: metadata.installable === false ? 'manual' : 'install',
    approval_required: metadata.installable !== false,
    install_ready: installerCheck?.ok ?? false,
    installer_check: installerCheck,
    runtime_node_prefix: resolveRuntimeNodePrefix(options),
    install_command: metadata.installable === false ? null : buildInstallCommand(metadata.alias),
    message: metadata.installable === false
      ? `${metadata.label} must already be available in the runtime environment`
      : `Install ${metadata.label} into the AgentWork runtime before retrying`,
  };
}

function buildIncompatibleNodePackageStatus(specifierOrAlias, attempts, options = {}) {
  const metadata = packageMetadataFor(specifierOrAlias);
  const primary = attempts[0] ?? null;
  const installerCheck = metadata.installable === false ? null : checkInstallerBinary();
  return {
    ok: false,
    type: 'nodeImport',
    specifier: metadata.alias,
    install_id: metadata.alias,
    package_specifier: metadata.installSpecifier,
    label: metadata.label,
    reason: 'incompatible',
    remediation_kind: metadata.installable === false ? 'manual' : 'install',
    approval_required: metadata.installable !== false,
    install_ready: installerCheck?.ok ?? false,
    installer_check: installerCheck,
    runtime_node_prefix: resolveRuntimeNodePrefix(options),
    install_command: metadata.installable === false ? null : buildInstallCommand(metadata.alias),
    detected_source: primary?.source ?? null,
    detected_version: primary?.version ?? null,
    detected_module_path: primary?.module_path ?? null,
    attempts,
  };
}

async function inspectResolvedPackage(metadata, resolvedStatus, options = {}) {
  try {
    const moduleNamespace = await import(pathToFileURL(resolvedStatus.resolved).href);
    const validation = typeof metadata.validate === 'function'
      ? metadata.validate(moduleNamespace)
      : { ok: true, version: null };

    if (!validation.ok) {
      return {
        ok: false,
        source: resolvedStatus.source,
        module_path: resolvedStatus.resolved,
        version: validation.version ?? null,
        reason: validation.reason ?? 'incompatible',
        message: validation.message ?? `Resolved ${metadata.alias} package is incompatible`,
        missing_exports: validation.missing_exports ?? [],
      };
    }

    return {
      ok: true,
      specifier: metadata.alias,
      source: resolvedStatus.source,
      module_path: resolvedStatus.resolved,
      runtime_node_prefix: resolvedStatus.runtimeNodePrefix ?? resolveRuntimeNodePrefix(options),
      version: validation.version ?? null,
    };
  } catch (error) {
    return {
      ok: false,
      source: resolvedStatus.source,
      module_path: resolvedStatus.resolved,
      version: null,
      reason: 'load_failed',
      message: error?.message ?? `Failed to load ${metadata.alias}`,
      missing_exports: [],
    };
  }
}

export async function checkNodePackage(specifier, options = {}) {
  const metadata = packageMetadataFor(specifier);
  const attempts = [];
  const candidates = [];

  const local = resolveLocalPackagePath(metadata.alias, options);
  if (local) candidates.push(local);

  if (systemNodeModulesEnabled()) {
    const system = resolveSystemPackagePath(metadata.alias);
    if (system) candidates.push(system);
  }

  for (const candidate of candidates) {
    const inspected = await inspectResolvedPackage(metadata, candidate, options);
    if (inspected.ok) {
      return inspected;
    }
    attempts.push(inspected);
  }

  if (attempts.length > 0) {
    return buildIncompatibleNodePackageStatus(metadata.alias, attempts, options);
  }

  return buildMissingNodePackageStatus(metadata.alias, options);
}

export async function importNodePackage(specifier, options = {}) {
  const status = await checkNodePackage(specifier, options);
  if (!status.ok) {
    const qualifier = status.reason === 'incompatible' ? 'found an incompatible' : 'is missing';
    const remediation = status.install_command
      ? `Ask the owner for approval, then run: ${status.install_command.join(' ')}`
      : status.message ?? `Make ${specifier} available in the runtime environment`;
    const installerNote = status.install_ready === false && status.installer_check
      ? ` (${status.installer_check.message})`
      : '';
    const error = new Error(
      `AgentWork runtime ${qualifier} "${specifier}". ${remediation}${installerNote}`,
    );
    error.code = 'NODE_PACKAGE_MISSING';
    error.details = status;
    throw error;
  }

  return await import(pathToFileURL(status.module_path).href);
}

export async function installNodePackage(packageAlias = 'ethers', options = {}) {
  const metadata = packageMetadataFor(packageAlias);
  if (metadata.installable === false) {
    const error = new Error(`Runtime package ${metadata.alias} is not installable via runtime-deps.mjs`);
    error.code = 'RUNTIME_PACKAGE_NOT_INSTALLABLE';
    error.details = {
      package: metadata.alias,
    };
    throw error;
  }

  const installerCheck = checkInstallerBinary();
  if (!installerCheck.ok) {
    const error = new Error(installerCheck.message);
    error.code = 'RUNTIME_INSTALLER_MISSING';
    error.details = installerCheck;
    throw error;
  }

  const prefix = resolveRuntimeNodePrefix(options);
  ensureRuntimePackageRoot(prefix);

  const installer = installerCheck.installer;
  const args = ['install', '--no-save', '--ignore-scripts', '--prefix', prefix, metadata.installSpecifier];

  return await new Promise((resolve, reject) => {
    const child = spawn(installer, args, {
      env: {
        ...process.env,
        npm_config_fund: 'false',
        npm_config_audit: 'false',
        npm_config_update_notifier: 'false',
      },
      stdio: ['ignore', 'pipe', 'pipe'],
      shell: false,
    });

    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on('data', (chunk) => {
      stderr += chunk.toString();
    });
    child.on('error', (error) => {
      reject(error);
    });
    child.on('close', (code, signal) => {
      if (code === 0) {
        resolve({
          ok: true,
          package: metadata.alias,
          package_specifier: metadata.installSpecifier,
          installer,
          runtime_node_prefix: prefix,
          stdout,
          stderr,
        });
        return;
      }

      const error = new Error(
        `Failed to install ${metadata.installSpecifier} into ${prefix} using ${installer} (exit ${code ?? 'unknown'}${signal ? `, signal ${signal}` : ''})`,
      );
      error.code = 'NODE_PACKAGE_INSTALL_FAILED';
      error.details = {
        package: metadata.alias,
        package_specifier: metadata.installSpecifier,
        installer,
        runtime_node_prefix: prefix,
        stdout,
        stderr,
      };
      reject(error);
    });
  });
}
