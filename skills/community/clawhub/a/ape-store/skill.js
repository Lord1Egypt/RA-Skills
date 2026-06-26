const ethers = require("ethers");
const FormData = require("form-data");
const fetch = require("node-fetch");
const fs = require("fs");
const path = require("path");

const CONTRACT_ADDRESS = "0xB1900F41d78D330A2a35C6771b3A6088a1b51309";

const ABI = [
  {
    inputs: [
      { internalType: "uint256", name: "id", type: "uint256" },
      {
        components: [
          { internalType: "string", name: "name", type: "string" },
          { internalType: "string", name: "symbol", type: "string" },
          { internalType: "int24", name: "initialTick", type: "int24" },
          { internalType: "uint24", name: "fee", type: "uint24" },
        ],
        internalType: "struct ApeStoreRouterV3.DeployParams",
        name: "_token",
        type: "tuple",
      },
      { internalType: "bytes", name: "signature", type: "bytes" },
    ],
    name: "deployToken",
    outputs: [{ internalType: "contract Token", name: "token", type: "address" }],
    stateMutability: "payable",
    type: "function",
  },
];

async function createApeToken({ name, symbol, description, imagePath, privateKey, rpcUrl }) {
  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const wallet = new ethers.Wallet(privateKey, provider);
  const creatorAddress = wallet.address;

  console.log("[1/3] Sending POST request to Ape.Store API...");

  const form = new FormData();
  form.append("chain", "8453");
  form.append("creator", creatorAddress);
  form.append("name", name);
  form.append("symbol", symbol);
  form.append("description", description);
  form.append("telegram", "");
  form.append("twitter", "");
  form.append("website", "");
  form.append("protocol", "30");
  form.append("signature", "");
  form.append("hidden", "false");
  form.append("botTrap", "false");

  if (imagePath) {
    const resolvedPath = path.resolve(imagePath);
    form.append("image", fs.createReadStream(resolvedPath));
    console.log("   Image attached: " + resolvedPath);
  }

  const apiResponse = await fetch("https://ape.store/api/token", {
    method: "POST",
    body: form,
    headers: form.getHeaders(),
  });

  if (!apiResponse.ok) {
    const errText = await apiResponse.text();
    throw new Error("API Error " + apiResponse.status + ": " + errText);
  }

  const { id, signature } = await apiResponse.json();
  console.log("[2/3] Got id=" + id + ", signature=" + signature);

  console.log("[3/3] Calling deployToken on BASE network...");
  const contract = new ethers.Contract(CONTRACT_ADDRESS, ABI, wallet);

  const tx = await contract.deployToken(
    id,
    { name, symbol, initialTick: -207200, fee: 10000 },
    signature
  );

  console.log("   TX sent: " + tx.hash);
  const receipt = await tx.wait();
  console.log("   TX confirmed in block " + receipt.blockNumber);
  console.log("Token " + name + " (" + symbol + ") successfully deployed on BASE!");

  return { txHash: tx.hash, blockNumber: receipt.blockNumber };
}

module.exports = { createApeToken };