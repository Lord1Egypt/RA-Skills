import os from 'node:os';
import crypto from 'node:crypto';
import { Resource } from '@opentelemetry/resources';
import { INSTRUMENTATION_LIBRARY } from './types.js';

/**
 * Compute a short hash of the plugin config for change detection.
 * Returns first 8 hex chars of SHA-256.
 */
export function configHash(config: Record<string, unknown>): string {
  const stable = JSON.stringify(config, Object.keys(config).sort());
  return crypto.createHash('sha256').update(stable).digest('hex').slice(0, 8);
}

export function buildResource(
  serviceVersion?: string,
  processOwner?: string,
  deploymentEnv?: string,
  workspaceId?: string,
  applicationId?: string,
  pluginConfig?: Record<string, unknown>,
): Resource {
  const attrs: Record<string, string> = {
    'service.name': 'openclaw',
    'host.name': os.type(),
    'host.arch': os.arch(),
    'process.owner': processOwner ?? os.userInfo().username,
  };

  // Use OpenClaw version if available, fall back to plugin version
  attrs['service.version'] = serviceVersion || INSTRUMENTATION_LIBRARY.version;

  // Plugin identification — allows tracing which plugin version and config is active
  attrs['telemetry.sdk.name'] = INSTRUMENTATION_LIBRARY.name;
  attrs['telemetry.sdk.version'] = INSTRUMENTATION_LIBRARY.version;
  if (pluginConfig) {
    attrs['telemetry.config.hash'] = configHash(pluginConfig);
  }

  const runtime = typeof process !== 'undefined' && (process as NodeJS.Process).versions?.bun
    ? 'bun'
    : 'node';
  attrs['process.runtime.name'] = runtime;
  attrs['process.runtime.version'] = process.version ?? '';

  if (deploymentEnv) {
    attrs['deployment.environment'] = deploymentEnv;
  }
  if (workspaceId) {
    attrs['openclaw.workspace.id'] = workspaceId;
  }
  if (applicationId) {
    attrs['openclaw.application.id'] = applicationId;
  }

  return new Resource(attrs);
}
