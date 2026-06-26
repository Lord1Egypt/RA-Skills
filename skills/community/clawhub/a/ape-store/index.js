const { createApeToken } = require("./skill");
const config = require("./skill.json");

const args = process.argv.slice(2).join(" ");

function parseCommand(input) {
  const nameMatch = input.match(/name\s+(\S+)/i);
  const symbolMatch = input.match(/symbol\s+(\S+)/i);
  const descMatch = input.match(/description\s+(.+?)(?:\s+and\s+image|$)/i);
  const imageMatch = input.match(/image\s+(\S+)/i);

  if (!nameMatch || !symbolMatch || !descMatch) {
    throw new Error("Invalid command format.");
  }

  return {
    name: nameMatch[1].replace(/"/g, "").trim(),
    symbol: symbolMatch[1].replace(/"/g, "").trim(),
    description: descMatch[1].replace(/"/g, "").trim(),
    imagePath: imageMatch ? imageMatch[1].replace(/"/g, "").trim() : null,
  };
}

(async () => {
  try {
    const { name, symbol, description, imagePath } = parseCommand(args);

    console.log("Creating token: " + name + " (" + symbol + ")");
    console.log("Description: " + description);
    if (imagePath) console.log("Image: " + imagePath);

    const result = await createApeToken({
      name,
      symbol,
      description,
      imagePath,
      privateKey: config.config.privateKey,
      rpcUrl: config.config.rpcUrl,
    });

    console.log("\nSuccess!");
    console.log("TX Hash: " + result.txHash);
    console.log("Block: " + result.blockNumber);
  } catch (err) {
    console.error("\nError: " + err.message);
    process.exit(1);
  }
})();
