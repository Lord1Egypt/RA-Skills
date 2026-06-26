const fs = require('fs');
const path = require('path');
const { QdrantClient } = require('@qdrant/js-client-rest');
require('dotenv').config({ path: path.join(__dirname, '.env') });

const folderArg = process.argv[2];
const query = process.argv[3];
if (!folderArg || !query) {
  console.error("Usage: node query.js <DRIVE_FOLDER_ID> \"<SEARCH_QUERY>\"");
  process.exit(1);
}

const ROOT_FOLDER_ID = folderArg;
const DB_PATH = path.join(__dirname, `vector_db_${ROOT_FOLDER_ID}.json`);

const QDRANT_URL = process.env.QDRANT_URL;
const QDRANT_API_KEY = process.env.QDRANT_API_KEY;
const USE_QDRANT = !!QDRANT_URL;

const EMBEDDING_PROVIDER = process.env.EMBEDDING_PROVIDER || "gemini";
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

if (!USE_QDRANT && !fs.existsSync(DB_PATH)) {
  console.error(`Database not found for folder ${ROOT_FOLDER_ID}. Please run sync.js first.`);
  process.exit(1);
}

let db = [];
if (!USE_QDRANT) {
  db = JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));
}

function cosineSimilarity(A, B) {
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  for (let i = 0; i < A.length; i++) {
    dotProduct += A[i] * B[i];
    normA += A[i] * A[i];
    normB += B[i] * B[i];
  }
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

async function getEmbedding(text) {
  if (EMBEDDING_PROVIDER === "openai") {
    const response = await fetch("https://api.openai.com/v1/embeddings", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: "text-embedding-3-small",
        input: text
      })
    });
    if (!response.ok) throw new Error(await response.text());
    const data = await response.json();
    return data.data[0].embedding;
  } else {
    // Gemini
    const url1 = `https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2-preview:embedContent?key=${GEMINI_API_KEY}`;
    const res1 = await fetch(url1, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: "models/gemini-embedding-2-preview",
        content: { parts: [{ text: text }] }
      })
    });
    
    if (res1.ok) {
      const data = await res1.json();
      return data.embedding.values;
    }
    
    const url2 = `https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=${GEMINI_API_KEY}`;
    const res2 = await fetch(url2, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: "models/gemini-embedding-001",
          content: { parts: [{ text: text }] }
        })
    });
    if (!res2.ok) {
        throw new Error("Both Gemini models failed: " + await res2.text());
    }
    const data2 = await res2.json();
    return data2.embedding.values;
  }
}

async function main() {
  const queryEmbedding = await getEmbedding(query);

  const topK = [];
  
  if (USE_QDRANT) {
    const qdrant = new QdrantClient({ url: QDRANT_URL, apiKey: QDRANT_API_KEY });
    const collectionName = `filechat_${ROOT_FOLDER_ID}`;
    const searchResult = await qdrant.search(collectionName, {
        vector: queryEmbedding,
        limit: 3,
        with_payload: true
    });
    searchResult.forEach(res => {
      topK.push({
        filename: res.payload.filename,
        fileId: res.payload.fileId,
        similarity: res.score,
        text: res.payload.text
      });
    });
  } else {
    const results = [];
    for (const doc of db) {
      const sim = cosineSimilarity(queryEmbedding, doc.embedding);
      results.push({ ...doc, similarity: sim });
    }
    results.sort((a, b) => b.similarity - a.similarity);
    const top3 = results.slice(0, 3);
    top3.forEach(res => {
      topK.push({
        filename: res.filename,
        fileId: res.fileId,
        similarity: res.similarity,
        text: res.text
      });
    });
  }

  console.log("Top matches for:", query);
  for (let i = 0; i < topK.length; i++) {
    console.log(`\nMatch ${i+1}:`);
    console.log(`Filename: ${topK[i].filename}`);
    console.log(`File ID: ${topK[i].fileId}`);
    console.log(`Similarity: ${topK[i].similarity.toFixed(4)}`);
    console.log(`Snippet: ${topK[i].text.substring(0, 200)}...`);
  }
}

main().catch(console.error);
