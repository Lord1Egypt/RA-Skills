import { Indexer } from "@0gfoundation/0g-ts-sdk";
import path from "path";
import fs from "fs"; // Added native File System module
import "dotenv/config";

// Initialize 0G SDK with your network configuration
const INDEXER_RPC = process.env.INDEXER_RPC;
const indexer = new Indexer(INDEXER_RPC);

async function downloadFromIndexer(rootHash, outputPath, encryptionKeyHex) {
  // Resolve absolute path so the agent framework saves it in the exact right workspace folder
  const absoluteOutputPath = path.resolve(outputPath);

  // Set up standard download options with Merkle proof verification enabled
  const downloadOptions = {
    proof: true
  };

  // If a hex key was passed by the agent, decode it and inject it into the decryption configuration
  if (encryptionKeyHex) {
    console.log("Secure key provided. Preparing decryption layer...");
    const symmetricKey = Buffer.from(encryptionKeyHex, 'hex');
    downloadOptions.decryption = { symmetricKey };
  }

  // Use downloadToBlob instead of download when dealing with inline SDK decryption options
  const [blob, dlErr] = await indexer.downloadToBlob(rootHash, downloadOptions);
  
  if (dlErr !== null) {
    throw new Error(`Download/Decryption error: ${dlErr}`);
  }

  // FIX: Extract the ArrayBuffer from the web Blob, then convert it safely into a Node Buffer
  const arrayBuffer = await blob.arrayBuffer();
  const bufferData = Buffer.from(arrayBuffer);
  
  // Write the clean buffer to your local machine disk
  fs.writeFileSync(absoluteOutputPath, bufferData);

  return absoluteOutputPath;
}

async function main() {
  const rootHash = process.argv[2];
  const outputPath = process.argv[3];
  const encryptionKeyHex = process.argv[4];

  if (!rootHash || !outputPath) {
    console.error("Error: Missing parameters.");
    console.log("Usage: node clawback-download.js <rootHash> <outputPath> [encryptionKeyHex]");
    process.exit(1);
  }

  try {
    console.log(`Initiating ClawBack recovery for hash: ${rootHash}...`);
    const finalPath = await downloadFromIndexer(rootHash, outputPath, encryptionKeyHex);
    
    const outputResult = {
      status: "success",
      recoveredFile: finalPath,
      decrypted: !!encryptionKeyHex
    };

    console.log("ClawBack Recovery Completed!");
    console.log(JSON.stringify(outputResult, null, 2));
  } catch (error) {
    console.error("ClawBack Recovery Failed:", error.message);
    process.exit(1);
  }
}

main();