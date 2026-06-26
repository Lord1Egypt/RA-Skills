import { NWCClient } from "@getalby/sdk";

const NWC_URL = process.env.ALBY_NWC_URL;
const bolt11 = process.argv[2];

if (!NWC_URL) {
  console.error("ERROR: ALBY_NWC_URL not set. Add it to openclaw.json env.");
  process.exitCode = 1;
  process.exit();
}

if (!bolt11) {
  console.error("Usage: node pay_bolt11.mjs <bolt11>");
  process.exitCode = 1;
  process.exit();
}

// Basic bolt11 format check
if (!/^ln[a-z0-9]+$/i.test(bolt11)) {
  console.error("Invalid bolt11 format.");
  process.exitCode = 1;
  process.exit();
}

const client = new NWCClient({ nostrWalletConnectUrl: NWC_URL });

try {
  // Timeout: abort if payment hangs longer than 30s
  const result = await Promise.race([
    client.payInvoice({ invoice: bolt11 }),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("payInvoice timed out after 30s")), 30_000)
    ),
  ]);
  // Only log essential fields — avoid leaking sensitive payment details
  console.log(JSON.stringify({ preimage: result.preimage, paid: true }));
} catch (e) {
  console.error("ERROR:", e.message);
  process.exitCode = 1;
} finally {
  client.close();
}
