/**
 * Self-test stub.
 * The original selftest module was missing, which broke the entire CLI on import.
 * This minimal stub restores the import so all commands load. Background
 * scheduler self-tests are a no-op until a real implementation is added.
 */

export interface SelfTestResult {
  name: string;
  status: 'OK' | 'ERROR';
  detail?: string;
}

export async function runSelfTests(): Promise<SelfTestResult[]> {
  return [];
}
