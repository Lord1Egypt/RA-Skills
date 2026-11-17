import { config } from "dotenv";
import { x402Client, wrapFetchWithPayment, x402HTTPClient } from "@x402/fetch";
import { ExactSvmScheme } from "@x402/svm/exact/client";
import { createKeyPairSignerFromBytes } from "@solana/kit";
import { base58 } from "@scure/base";

config();

const svmPrivateKey = process.env.SVM_PRIVATE_KEY as string;
const baseURL = process.env.BRIDGENODE_URL || "https://bridgenode.cc";
const url = `${baseURL}/v1/chat/completions`;

/**
 * BridgeNode buyer-side example: pay per request with Solana USDC via x402.
 */
async function main(): Promise<void> {
  const svmSigner = await createKeyPairSignerFromBytes(base58.decode(svmPrivateKey));

  const client = new x402Client();
  client.register("solana:*", new ExactSvmScheme(svmSigner));

  const fetchWithPayment = wrapFetchWithPayment(fetch, client);
  const httpClient = new x402HTTPClient(client);

  console.log(`POST ${url}\n`);
  const response = await fetchWithPayment(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "deepseek-v4-flash",
      messages: [{ role: "user", content: "Say hello in one sentence." }],
      max_tokens: 100,
    }),
  });

  const result = await httpClient.processResponse(response);
  console.dir(result, { depth: null });
}

main().catch((error) => {
  console.error(error?.response?.data?.error ?? error);
  process.exit(1);
});
