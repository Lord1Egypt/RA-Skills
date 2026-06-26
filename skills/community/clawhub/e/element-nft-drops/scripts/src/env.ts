export function getRequiredEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

export function normalizeWalletPrivateKey(value: string): string {
  const trimmed = value.trim();
  if (!/^0x[0-9a-fA-F]{64}$/.test(trimmed)) {
    throw new Error("ELEMENT_WALLET_PRIVATE_KEY must be a 0x-prefixed 32-byte hex private key");
  }
  return trimmed;
}

export function getRequiredWalletPrivateKey(): string {
  return normalizeWalletPrivateKey(getRequiredEnv("ELEMENT_WALLET_PRIVATE_KEY"));
}

export function redactKnownSecrets(text: string): string {
  const walletPrivateKey = process.env.ELEMENT_WALLET_PRIVATE_KEY?.trim();
  if (!walletPrivateKey) {
    return text;
  }
  return text.split(walletPrivateKey).join("[REDACTED:ELEMENT_WALLET_PRIVATE_KEY]");
}
