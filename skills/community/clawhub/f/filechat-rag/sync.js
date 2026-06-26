const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const pdf = require('pdf-parse');
const { QdrantClient } = require('@qdrant/js-client-rest');
require('dotenv').config({ path: path.join(__dirname, '.env') });

const folderArg = process.argv[2];
if (!folderArg) {
  console.error("Usage: node sync.js <DRIVE_FOLDER_ID>");
  process.exit(1);
}

const ROOT_FOLDER_ID = folderArg;

// Vector DB Configuration
const QDRANT_URL = process.env.QDRANT_URL;
const QDRANT_API_KEY = process.env.QDRANT_API_KEY;

// Keep Local DB as fallback if no Qdrant configured
const USE_QDRANT = !!QDRANT_URL;
const DB_PATH = path.join(__dirname, `vector_db_${ROOT_FOLDER_ID}.json`);

const META_PATH = path.join(__dirname, `meta_${ROOT_FOLDER_ID}.json`);

const EMBEDDING_PROVIDER = process.env.EMBEDDING_PROVIDER || "gemini";
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

if (EMBEDDING_PROVIDER === "gemini" && !GEMINI_API_KEY) {
  console.error("Missing GEMINI_API_KEY for embedding provider 'gemini'.");
  process.exit(1);
} else if (EMBEDDING_PROVIDER === "openai" && !OPENAI_API_KEY) {
  console.error("Missing OPENAI_API_KEY for embedding provider 'openai'.");
  process.exit(1);
}

let qdrant;
if (USE_QDRANT) {
  qdrant = new QdrantClient({ url: QDRANT_URL, apiKey: QDRANT_API_KEY });
}

const CERT_PREFIX = require('fs').existsSync('/workspace/cacert.pem') ? 'SSL_CERT_FILE=/workspace/cacert.pem ' : '';

function getGWSFiles(folderId) {
  const query = `'${folderId}' in parents and trashed = false`;
  const escapedQuery = query.replace(/'/g, "'\\''");
  const cmd = `${CERT_PREFIX}npx @googleworkspace/cli drive files list --params '{"q": "${escapedQuery}", "fields": "files(id, name, mimeType, modifiedTime, shortcutDetails)"}'`;
  try {
    const res = execSync(cmd, { encoding: 'utf-8', stdio: 'pipe' });
    const jsonStart = res.indexOf('{');
    const cleanRes = res.substring(jsonStart);
    return JSON.parse(cleanRes).files || [];
  } catch(e) {
    console.error("Error fetching files from GWS:", e.message);
    return [];
  }
}

function downloadFile(fileId, dest) {
  const cmd = `${CERT_PREFIX}npx @googleworkspace/cli drive files get --params '{"fileId": "${fileId}", "alt": "media"}' --output "${dest}"`;
  try {
    execSync(cmd, { stdio: 'pipe' });
    return true;
  } catch(e) {
    return false;
  }
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

function chunkText(text, maxWords = 200) {
  const words = text.split(/\s+/);
  const chunks = [];
  for(let i=0; i < words.length; i += maxWords) {
    chunks.push(words.slice(i, i + maxWords).join(" "));
  }
  return chunks;
}

async function extractTextFromImage(filePath, mimeType) {
  if (EMBEDDING_PROVIDER === "openai") {
    console.log("OCR for OpenAI not implemented. Skipping image text extraction.");
    return "";
  } else {
    const { GoogleGenerativeAI } = require("@google/generative-ai");
    const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
    const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });
    const prompt = "Please transcribe all the text visible in this image accurately. Do not add any extra commentary, just the text.";
    const imagePart = {
      inlineData: {
        data: Buffer.from(fs.readFileSync(filePath)).toString("base64"),
        mimeType
      },
    };
    const result = await model.generateContent([prompt, imagePart]);
    const response = await result.response;
    return response.text();
  }
}

async function processFolder(folderId, currentPath, db, meta) {
  console.log(`Scanning folder: ${currentPath || 'Root'} (${folderId})`);
  const items = getGWSFiles(folderId);
  const collectionName = `filechat_${ROOT_FOLDER_ID}`;
  
  for(const item of items) {
    const filePath = currentPath ? `${currentPath}/${item.name}` : item.name;
    
    let targetId = item.id;
    let mimeType = item.mimeType;
    let modifiedTime = item.modifiedTime;

    if (mimeType === 'application/vnd.google-apps.shortcut') {
      targetId = item.shortcutDetails.targetId;
      mimeType = item.shortcutDetails.targetMimeType;
      console.log(`Resolving shortcut: ${item.name} -> ${targetId}`);
    }

    if (mimeType === 'application/vnd.google-apps.folder') {
      await processFolder(targetId, filePath, db, meta);
    } else if (mimeType === 'application/pdf' || mimeType.includes('text') || mimeType.includes('image')) {
      
      if (meta[targetId] && meta[targetId] === modifiedTime) {
        console.log(`Skipping file (unchanged): ${filePath}`);
        continue;
      }

      console.log(`Processing file: ${filePath} (${mimeType})`);
      const tmpFile = `./filechat_${targetId}`;
      
      if (!USE_QDRANT) {
        // Remove old chunks from local db
        for (let i = db.length - 1; i >= 0; i--) {
          if (db[i].fileId === targetId) db.splice(i, 1);
        }
      } else {
        // Remove old chunks from Qdrant
        await qdrant.delete(collectionName, { filter: { must: [{ key: "fileId", match: { value: targetId } }] } });
      }
      
      if(downloadFile(targetId, tmpFile)) {
        let text = "";
        try {
          if (mimeType === 'application/pdf') {
            const dataBuffer = fs.readFileSync(tmpFile);
            const data = await pdf(dataBuffer);
            text = data.text;
          } else if (mimeType.includes('image')) {
            text = await extractTextFromImage(tmpFile, mimeType);
          } else {
            text = fs.readFileSync(tmpFile, 'utf8');
          }
          
          if(text.trim()) {
            const chunks = chunkText(text);
            const points = [];
            for(let i=0; i<chunks.length; i++) {
              const c = chunks[i];
              const emb = await getEmbedding(c);
              
              if (USE_QDRANT) {
                // UUID v5 based on TargetID+Index or just random
                const crypto = require('crypto');
                const pointId = crypto.randomUUID();
                points.push({
                  id: pointId,
                  vector: emb,
                  payload: { fileId: targetId, filename: filePath, chunkIndex: i, text: c }
                });
              } else {
                db.push({ fileId: targetId, filename: filePath, chunkIndex: i, text: c, embedding: emb });
              }
            }
            if (USE_QDRANT && points.length > 0) {
              await qdrant.upsert(collectionName, { wait: true, points });
            }
            console.log(`Embedded ${chunks.length} chunks for ${item.name}`);
          }
          meta[targetId] = modifiedTime; // update meta on success
        } catch(e) {
          console.error(`Failed to parse/embed ${item.name}: ${e.message}`);
        }
        if(fs.existsSync(tmpFile)) fs.unlinkSync(tmpFile);
      } else {
        console.error(`Failed to download ${item.name}`);
      }
    } else {
      console.log(`Skipping unsupported file type: ${filePath} (${mimeType})`);
    }
  }
}

async function main() {
  console.log(`Starting FileChat Sync for Folder ID: ${ROOT_FOLDER_ID}...`);
  let db = [];
  if (!USE_QDRANT && fs.existsSync(DB_PATH)) {
    try { db = JSON.parse(fs.readFileSync(DB_PATH, 'utf8')); } catch(e) {}
  }
  let meta = {};
  if (fs.existsSync(META_PATH)) {
    try { meta = JSON.parse(fs.readFileSync(META_PATH, 'utf8')); } catch(e) {}
  }

  if (USE_QDRANT) {
    const collectionName = `filechat_${ROOT_FOLDER_ID}`;
    const res = await qdrant.getCollections();
    const exists = res.collections.find(c => c.name === collectionName);
    if (!exists) {
       console.log(`Creating Qdrant collection ${collectionName}...`);
       const vectorSize = EMBEDDING_PROVIDER === "openai" ? 1536 : 768; // 768 for gemini-embedding models
       await qdrant.createCollection(collectionName, { vectors: { size: vectorSize, distance: "Cosine" } });
    }
  }
  
  await processFolder(ROOT_FOLDER_ID, "", db, meta);
  
  if (!USE_QDRANT) {
    fs.writeFileSync(DB_PATH, JSON.stringify(db));
    console.log(`Sync complete. Local database saved to disk with ${db.length} total chunks.`);
  } else {
    console.log(`Sync complete. Updated Qdrant database.`);
  }
  fs.writeFileSync(META_PATH, JSON.stringify(meta, null, 2));
}

main().catch(console.error);
