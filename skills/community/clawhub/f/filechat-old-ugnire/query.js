const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '.env') });

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const DB_PATH = path.join(__dirname, 'vector_db.json');

if (!GEMINI_API_KEY) {
  console.error("Missing GEMINI_API_KEY in .env");
  process.exit(1);
}

if (!fs.existsSync(DB_PATH)) {
  console.error("Database not found. Please run sync.js first.");
  process.exit(1);
}

const db = JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));

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
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=${GEMINI_API_KEY}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: "models/gemini-embedding-001",
      content: { parts: [{ text: text }] }
    })
  });
  if (!response.ok) throw new Error(await response.text());
  const data = await response.json();
  return data.embedding.values;
}

async function main() {
  const query = process.argv[2];
  if (!query) {
    console.error("Please provide a search query.");
    process.exit(1);
  }

  const queryEmbedding = await getEmbedding(query);

  const results = [];
  for (const doc of db) {
    const sim = cosineSimilarity(queryEmbedding, doc.embedding);
    results.push({ ...doc, similarity: sim });
  }

  results.sort((a, b) => b.similarity - a.similarity);
  const topK = results.slice(0, 3);

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
