import { createHash } from "crypto";

export function generateToken(apiKey: string): { token: string; timestamp: string } {
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const token = createHash("md5")
    .update(`1panel${apiKey}${timestamp}`)
    .digest("hex");
  return { token, timestamp };
}
