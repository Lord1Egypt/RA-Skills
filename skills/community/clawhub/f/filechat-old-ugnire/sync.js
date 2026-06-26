const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const pdf = require('pdf-parse');
require('dotenv').config({ path: path.join(__dirname, '.env') });

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const ROOT_FOLDER_ID = process.env.FILECHAT_DRIVE_FOLDER_ID;
const DB_PATH = path.join(__dirname, 'vector_db.json');

if (!GEMINI_API_KEY || !ROOT_FOLDER_ID) {
  console.error("Missing GEMINI_API_KEY or FILECHAT_DRIVE_FOLDER_ID in .env");
  process.exit(1);
}

function getGWSFiles(folderId) {
  const query = `'${folderId}' in parents and trashed = false`;
  const escapedQuery = query.replace(/'/g, "'\\''");
  const cmd = `SSL_CERT_FILE=/workspace/cacert.pem npx @googleworkspace/cli drive files list --params '{"q": "${escapedQuery}", "fields": "files(id, name, mimeType, shortcutDetails)"}'`;
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
  const cmd = `SSL_CERT_FILE=/workspace/cacert.pem npx @googleworkspace/cli drive files get --params '{"fileId": "${fileId}", "alt": "media"}' --output "${dest}"`;
  try {
    execSync(cmd, { stdio: 'pipe' });
    return true;
  } catch(e) {
    return false;
  }
}

async function getEmbedding(text) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key=${GEMINI_API_KEY}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: "models/text-embedding-004",
      content: {
        parts: [{ text: text }]
      }
    })
  });
  if (!response.ok) {
    const err = await response.text();
    const url2 = `https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=${GEMINI_API_KEY}`;
    const response2 = await fetch(url2, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: "models/gemini-embedding-001",
          content: {
            parts: [{ text: text }]
          }
        })
    });
    if (!response2.ok) {
        const err2 = await response2.text();
        throw new Error("Both text-embedding-004 and gemini-embedding-001 failed: " + err + " / " + err2);
    }
    const data2 = await response2.json();
    return data2.embedding.values;
  }
  const data = await response.json();
  return data.embedding.values;
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

async function processFolder(folderId, currentPath, db) {
  console.log(`Scanning folder: ${currentPath || 'Root'} (${folderId})`);
  const items = getGWSFiles(folderId);
  
  for(const item of items) {
    const filePath = currentPath ? `${currentPath}/${item.name}` : item.name;
    
    let targetId = item.id;
    let mimeType = item.mimeType;
    if (mimeType === 'application/vnd.google-apps.shortcut') {
      targetId = item.shortcutDetails.targetId;
      mimeType = item.shortcutDetails.targetMimeType;
      console.log(`Resolving shortcut: ${item.name} -> ${targetId}`);
    }

    if (mimeType === 'application/vnd.google-apps.folder') {
      await processFolder(targetId, filePath, db);
    } else if (mimeType === 'application/pdf' || mimeType.includes('text') || mimeType.includes('image')) {
      console.log(`Processing file: ${filePath} (${mimeType})`);
      const tmpFile = `./filechat_${targetId}`;
      
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
            for(let i=0; i<chunks.length; i++) {
              const c = chunks[i];
              const emb = await getEmbedding(c);
              db.push({
                fileId: targetId,
                filename: filePath,
                chunkIndex: i,
                text: c,
                embedding: emb
              });
            }
            console.log(`Embedded ${chunks.length} chunks for ${item.name}`);
          }
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
  console.log("Starting FileChat Sync...");
  let db = [];
  
  await processFolder(ROOT_FOLDER_ID, "", db);
  
  fs.writeFileSync(DB_PATH, JSON.stringify(db));
  console.log(`Sync complete. Database saved to disk with ${db.length} total chunks.`);
}

main().catch(console.error);
