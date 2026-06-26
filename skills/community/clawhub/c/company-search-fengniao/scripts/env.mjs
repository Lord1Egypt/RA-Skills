const ENV_KEY = "FN_API_KEY";

// Public shared key baked into the published skill. A user-provided key still wins.
const BUILTIN_KEY = "eab076c5-b108-4a3f-b2fb-d97039b1a447";

// Publish channel for this distribution. Change this value when packaging for another platform.
export const CHANNEL = "clawhub";

export const BASE_URL = "https://m.riskbird.com/prod-qbb-api";

export async function getApiKey() {
  const key = process.env[ENV_KEY];
  if (key && key !== "YOUR_API_KEY") return key;
  return BUILTIN_KEY;
}
