import { GoogleGenAI, createUserContent, createPartFromUri } from "@google/genai";
import { fileURLToPath } from 'url';
import path from 'path';

// Note: Ensure your environment has GEMINI_API_KEY set
const ai = new GoogleGenAI({});

async function transcribeDirect(audioFilePath) {
    try {
        const filePath = path.resolve(audioFilePath);
        
        // Upload file to Gemini File API
        // SDK handles the streaming/upload, clearer than manual file read
        const myFile = await ai.files.upload({
            file: filePath,
            config: { mimeType: "audio/ogg" }, // Can be adapted for others
        });

        // Generate content
        const response = await ai.models.generateContent({
            model: "gemini-3.1-flash-preview",
            contents: createUserContent([
                createPartFromUri(myFile.uri, myFile.mimeType),
                "Transcribe this Burmese audio accurately. Return only the Burmese transcription without any markdown or formatting.",
            ]),
        });

        // Output result
        console.log(response.text.trim());

        // Cleanup
        await ai.files.delete(myFile.name);
        
    } catch (error) {
        console.error("Transcription failed:", error.message);
        process.exit(1);
    }
}

const args = process.argv.slice(2);
if (args.length === 0) {
    console.log("Usage: node transcribe-direct.js <audio-file>");
    process.exit(1);
}

await transcribeDirect(args[0]);