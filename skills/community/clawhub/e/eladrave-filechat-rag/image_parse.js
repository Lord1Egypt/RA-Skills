const fs = require('fs');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

function fileToGenerativePart(path, mimeType) {
  return {
    inlineData: {
      data: Buffer.from(fs.readFileSync(path)).toString("base64"),
      mimeType
    },
  };
}

async function extractTextFromImage(filePath, mimeType) {
  const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });
  const prompt = "Please transcribe all the text visible in this image accurately. Do not add any extra commentary, just the text.";
  const imagePart = fileToGenerativePart(filePath, mimeType);
  const result = await model.generateContent([prompt, imagePart]);
  const response = await result.response;
  return response.text();
}

module.exports = { extractTextFromImage };
