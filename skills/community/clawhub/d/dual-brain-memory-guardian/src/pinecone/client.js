import { Pinecone } from "@pinecone-database/pinecone";
import { loadConfig } from "./config.js";

async function indexExists(pc, indexName) {
  const list = await pc.listIndexes();
  const indexes = list.indexes ?? [];
  return indexes.some((item) => item.name === indexName);
}

function isConflictError(error) {
  if (!error) {
    return false;
  }

  const name = String(error.name || "");
  const message = String(error.message || "").toLowerCase();
  return name.includes("Conflict") || message.includes("already exists");
}

export async function bootstrapPinecone(overrides = {}) {
  const config = loadConfig(overrides);
  const pc = new Pinecone({ apiKey: config.apiKey });

  if (!(await indexExists(pc, config.indexName))) {
    try {
      await pc.createIndexForModel({
        name: config.indexName,
        cloud: config.cloud,
        region: config.region,
        embed: {
          model: config.model,
          fieldMap: { text: config.textField }
        },
        waitUntilReady: true
      });
    } catch (error) {
      if (!isConflictError(error)) {
        throw error;
      }
    }
  }

  const indexModel = await pc.describeIndex(config.indexName);
  if (!indexModel.host) {
    throw new Error(`Index ${config.indexName} did not return a host.`);
  }

  const index = pc.index({ host: indexModel.host });
  return { pc, index, indexModel, config };
}
