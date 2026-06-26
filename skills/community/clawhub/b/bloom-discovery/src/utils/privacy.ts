import { createHash, randomBytes } from 'crypto';

// Laplace noise for ε-differential privacy (CSPRNG-backed)
export function addLaplaceNoise(value: number, epsilon = 1.0, sensitivity = 100): number {
  const scale = sensitivity / epsilon;
  const u = (randomBytes(4).readUInt32BE() / 0xffffffff) - 0.5;
  const noise = -scale * Math.sign(u) * Math.log(1 - 2 * Math.abs(u));
  return Math.max(0, Math.min(100, Math.round(value + noise)));
}

export function privatizeSpectrums<T extends Record<string, number>>(
  spectrums: T,
  epsilon = 1.0
): T {
  const result: Record<string, number> = {};
  for (const [key, value] of Object.entries(spectrums)) {
    result[key] = addLaplaceNoise(value, epsilon);
  }
  return result as T;
}

export function conversationFingerprint(text: string): string {
  return createHash('sha256').update(text).digest('hex');
}
