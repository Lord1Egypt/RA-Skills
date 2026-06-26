import 'dotenv/config'; 
import express from 'express';
import cors from 'cors';
import { GoogleGenAI } from '@google/genai';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

const DOWNLOADS_DIR = path.join(__dirname, 'downloads');
await fs.mkdir(DOWNLOADS_DIR, { recursive: true }).catch(console.error);

app.use(cors());
app.use(express.json({ limit: '50mb' })); // Allows for large image/PDF uploads
app.use(express.static(path.join(__dirname, 'public')));
app.use('/downloads', express.static(DOWNLOADS_DIR));

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const SYSTEM_PROMPT = `You are an expert system architect and data visualizer. Your function is to generate valid Mermaid.js diagrams AND Draw.io (mxGraph) diagrams.

## Supported Diagram Types & Strict Rules
1. **Mermaid Diagrams**: Default to this. Use standard Mermaid syntax. Wrap in \`\`\`mermaid
2. **Draw.io Diagrams**: If the user explicitly asks for "draw.io", output raw Draw.io mxGraphModel XML. Wrap it in \`\`\`xml. Use the standard <mxGraphModel><root><mxCell/></root></mxGraphModel> structure.

## Contextual Generation
- The user may provide images, PDFs, or text documents. Extract the relationships, architecture, or timeline from these files to build the diagram.
- If the user provides an existing diagram code, update it based on the request.
- Output ONLY the raw code block. NEVER include explanations or introductory text.`;

app.get('/api/health', (req, res) => res.json({ status: 'ok' }));

app.post('/api/generate', async (req, res) => {
    const { prompt, currentCode, type, files } = req.body;
    if (!prompt && (!files || files.length === 0)) {
        return res.status(400).json({ error: "Prompt or files are required" });
    }
    
    let promptText = currentCode
        ? `Here is the current diagram:\n\`\`\`${type === 'drawio' ? 'xml' : 'mermaid'}\n${currentCode}\n\`\`\`\nUpdate it based on this request: ${prompt}`
        : `Generate a diagram for this request: ${prompt}`;

    let contents = [];

    // Process Extracted Text (.txt, .docx, code files)
    if (files && files.length > 0) {
        const textFiles = files.filter(f => f.text);
        if (textFiles.length > 0) {
            const combinedText = textFiles.map(f => `--- Content from ${f.name} ---\n${f.text}\n---`).join('\n\n');
            promptText += `\n\nContext documents provided by user:\n${combinedText}`;
        }
    }

    contents.push(promptText);

    // Process Binary Files (.pdf, .png, .jpg)
    if (files && files.length > 0) {
        files.forEach(file => {
            if (file.data && !file.text) {
                const base64Data = file.data.includes(',') ? file.data.split(',')[1] : file.data;
                contents.push({
                    inlineData: {
                        data: base64Data,
                        mimeType: file.mimeType
                    }
                });
            }
        });
    }

    try {
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: contents,
            config: { systemInstruction: SYSTEM_PROMPT, temperature: 0.2 }
        });

        let text = response.text; 
        let code = "";
        let outType = "mermaid";
        
        if (text.includes('```xml')) {
            const match = text.match(/```xml\n([\s\S]*?)\n```/);
            code = match ? match[1] : text.replace(/```xml/g, '').replace(/```/g, '');
            outType = "drawio";
        } else {
            const match = text.match(/```mermaid\n([\s\S]*?)\n```/);
            code = match ? match[1] : text.replace(/```mermaid/g, '').replace(/```/g, '');
        }

        res.json({ code: code.trim(), type: outType });
    } catch (error) {
        console.error("Error generating diagram:", error);
        res.status(500).json({ error: "Failed to generate diagram" });
    }
});

// --- SECURE FILE SAVING ---
app.post('/api/save', async (req, res) => {
    const { projectName, filename, content, isImage } = req.body;
    
    // Strict Regex Validation
    if (!projectName || !filename || !/^[a-zA-Z0-9_-]+$/.test(projectName) || !/^[a-zA-Z0-9_.-]+$/.test(filename)) {
        return res.status(400).json({ error: "Invalid project or filename format." });
    }
    
    try {
        const projectDir = path.join(DOWNLOADS_DIR, projectName);
        const filePath = path.join(projectDir, filename);

        // Failsafe: Ensure the resolved path strictly stays within the Downloads directory
        if (!filePath.startsWith(DOWNLOADS_DIR)) {
            return res.status(403).json({ error: "Access denied: Path traversal detected." });
        }

        await fs.mkdir(projectDir, { recursive: true });

        if (isImage) {
            const base64Data = content.replace(/^data:image\/\w+;base64,/, "");
            await fs.writeFile(filePath, base64Data, 'base64');
        } else {
            await fs.writeFile(filePath, content, 'utf8');
        }
        res.json({ success: true, url: `/downloads/${projectName}/${filename}` });
    } catch (error) {
        console.error("Save error:", error);
        res.status(500).json({ error: "Failed to save file" });
    }
});

app.get('/api/files', async (req, res) => {
    try {
        const filesData = {};
        const projects = await fs.readdir(DOWNLOADS_DIR);
        for (const proj of projects) {
            const projPath = path.join(DOWNLOADS_DIR, proj);
            const stat = await fs.stat(projPath);
            if (stat.isDirectory()) {
                const files = await fs.readdir(projPath);
                filesData[proj] = files.filter(f => !f.startsWith('.'));
            }
        }
        res.json(filesData);
    } catch (error) {
        res.status(500).json({ error: "Failed to read directories" });
    }
});

// --- SECURE FILE DELETION ---
app.delete('/api/files/:project/:filename', async (req, res) => {
    const { project, filename } = req.params;

    // Strict Regex Validation (Deny slashes and path traversal characters)
    if (!/^[a-zA-Z0-9_-]+$/.test(project) || !/^[a-zA-Z0-9_.-]+$/.test(filename)) {
        return res.status(400).json({ error: "Invalid project or filename format." });
    }

    try {
        const filePath = path.join(DOWNLOADS_DIR, project, filename);
        
        // Failsafe: Ensure the resolved path strictly stays within the Downloads directory
        if (!filePath.startsWith(DOWNLOADS_DIR)) {
            return res.status(403).json({ error: "Access denied: Path traversal detected." });
        }

        await fs.unlink(filePath);

        // Safely check and clean up empty directories
        const projectDir = path.join(DOWNLOADS_DIR, project);
        if (projectDir.startsWith(DOWNLOADS_DIR)) {
            const remainingFiles = await fs.readdir(projectDir);
            if (remainingFiles.filter(f => !f.startsWith('.')).length === 0) {
                await fs.rm(projectDir, { recursive: true, force: true });
            }
        }

        res.json({ success: true, message: "File deleted successfully" });
    } catch (error) {
        console.error("Delete file error:", error);
        res.status(500).json({ error: "Failed to delete file" });
    }
});

// --- SECURE PROJECT DELETION ---
app.delete('/api/projects/:project', async (req, res) => {
    const { project } = req.params;

    // Strict Regex Validation
    if (!/^[a-zA-Z0-9_-]+$/.test(project)) {
        return res.status(400).json({ error: "Invalid project name format." });
    }

    try {
        const projectDir = path.join(DOWNLOADS_DIR, project);
        
        // Failsafe: Path traversal check
        if (!projectDir.startsWith(DOWNLOADS_DIR)) {
             return res.status(403).json({ error: "Access denied: Path traversal detected." });
        }

        await fs.rm(projectDir, { recursive: true, force: true });
        res.json({ success: true, message: "Project deleted successfully" });
    } catch (error) {
        console.error("Delete project error:", error);
        res.status(500).json({ error: "Failed to delete project" });
    }
});

app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));