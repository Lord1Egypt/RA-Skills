import { NWCClient, LN, SATS } from "@getalby/sdk";

const client = new NWCClient({ 
    nostrWalletConnectUrl: process.env.ALBY_NWC_URL 
});

// Check balance
const { balance } = await client.getBalance();
console.log(`Balance: ${Math.floor(balance / 1000)} sats`);

// Pay a BOLT11 invoice
await client.payInvoice({ 
    invoice: "lnbc...", 
    amount: 1000 * 1000 // msats explicitly 
});

// Pay a Lightning address
const ln = new LN(process.env.ALBY_NWC_URL);
await ln.pay("user@getalby.com", SATS(100));

// Create an invoice to receive
const result = await client.makeInvoice({ 
    amount: 2000 * 1000, 
    description: "Payment" 
});
console.log(result.invoice);

client.close();
