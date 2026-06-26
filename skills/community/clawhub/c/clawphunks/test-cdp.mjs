import { Coinbase, Wallet } from "@coinbase/coinbase-sdk";

const apiKeyId = "b2b9e2b9-6594-4cd7-8e7f-ccb8625a6ffe";
const apiKeySecret = "Opdhd9axeAxLOEKIIcoRobdROuQ6wkaAEAq0Zq8MGAd3TfhFAG95t5HK90Q/xpO1oaYXIARpgp62CePxIM+9HA==";

Coinbase.configure({
  apiKeyName: apiKeyId,
  privateKey: apiKeySecret,
});

// List wallets
try {
  const wallets = await Wallet.listWallets();
  console.log("Wallets found:", wallets.data.length);
  
  for (const wallet of wallets.data) {
    console.log("Wallet:", wallet.id, "Network:", wallet.network_id);
    console.log("  Default Address:", wallet.default_address?.address_id);
  }
} catch (e) {
  console.error("Error:", e.message);
  console.error(e);
}
