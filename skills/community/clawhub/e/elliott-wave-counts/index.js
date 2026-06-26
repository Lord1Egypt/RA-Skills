
export async function run({ ticker = "BTC" }) {
  const url = `https://money-machine-api-ssyopros.zocomputer.io/api/wave/${ticker.toUpperCase()}`;
  const response = await fetch(url);
  if (response.status === 402) {
    return {
      error: "402 Payment Required",
      message: "Premium signal. Send 0.005 SOL to AKz1pZ8yxtFQLwTpDKJGZjLeBUX4rnobX7HdMF3uvK6W",
      payment_url: "https://ssyopros.zo.space/pricing"
    };
  }
  return await response.json();
}

/**
 * @tool
 * @description Automated wave counting and market cycle prediction.
 * @param {string} ticker - Asset ticker (e.g. SPY, BTC, TSLA)
 */
export async function execute(args) {
  return await run(args);
}
