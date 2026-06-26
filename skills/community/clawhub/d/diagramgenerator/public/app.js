console.log("🚀 Initializing AI Diagram Generator...");

// Global state variables
let currentCode = "";
let currentType = "mermaid";
let previewCode = "";
let previewType = "mermaid";
let attachedPromptFiles = [];
let mermaid; // Will be loaded dynamically

// --- 1. Safe Initialization ---
async function initApp() {
    try {
        console.log("📦 Loading Mermaid.js from CDN...");
        const mermaidModule = await import('https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs');
        mermaid = mermaidModule.default;
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        console.log("✅ Mermaid loaded successfully.");
    } catch (error) {
        console.error("❌ Failed to load Mermaid:", error);
        updateStatus("Warning: Could not load Mermaid engine. Check your internet connection or ad-blocker.", true);
    }

    bindEventListeners();
    fetchSavedFiles();
}

// --- 2. Event Listeners ---
function bindEventListeners() {
    document.getElementById('generateBtn').addEventListener('click', generateDiagram);
    document.getElementById('saveServerTextBtn').addEventListener('click', () => saveTextToServer('mmd'));
    document.getElementById('saveServerDrawioBtn').addEventListener('click', () => saveTextToServer('drawio'));
    document.getElementById('saveServerPngBtn').addEventListener('click', () => saveImageToServer('png'));
    document.getElementById('saveServerJpgBtn').addEventListener('click', () => saveImageToServer('jpeg'));
    document.getElementById('refreshFilesBtn').addEventListener('click', fetchSavedFiles);

    // Editor Code Loader
    document.getElementById('loadFileBtn').addEventListener('click', (e) => {
        e.preventDefault();
        document.getElementById('fileInput').click();
    });
    document.getElementById('fileInput').addEventListener('change', loadLocalTextFile);

    // Prompt Context Attacher
    document.getElementById('attachContextBtn').addEventListener('click', (e) => {
        e.preventDefault();
        document.getElementById('promptFileInput').click();
    });
    document.getElementById('promptFileInput').addEventListener('change', handlePromptFileUpload);

    // Modal Listeners
    document.getElementById('closeModalBtn').addEventListener('click', closeModal);
    document.getElementById('loadIntoEditorBtn').addEventListener('click', loadPreviewIntoEditor);
    document.getElementById('rerenderPreviewBtn').addEventListener('click', updatePreviewFromEditor);

    window.onclick = function(event) {
        if (event.target === document.getElementById('previewModal')) closeModal();
    }

    document.querySelectorAll('.example-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const promptText = e.currentTarget.getAttribute('data-prompt');
            if (promptText) {
                document.getElementById('promptInput').value = promptText;
            }
        });
    });
}

// --- 3. UI Helpers ---
function updateStatus(message, isError = false, isVisible = true) {
    const statusDiv = document.getElementById('statusMessage');
    statusDiv.style.display = isVisible ? 'block' : 'none';
    statusDiv.innerHTML = message;
    statusDiv.style.background = isError ? '#ffebee' : '#e8f5e9';
    statusDiv.style.borderLeftColor = isError ? '#f44336' : '#4caf50';
    statusDiv.style.color = isError ? '#c62828' : '#2e7d32';
}

// --- 4. Context File Handling ---
async function handlePromptFileUpload(event) {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    const textBasedExtensions = ['txt', 'js', 'py', 'json', 'html', 'css', 'ts', 'java', 'md'];

    for (let file of files) {
        const ext = file.name.split('.').pop().toLowerCase();

        if (textBasedExtensions.includes(ext)) {
            const text = await file.text();
            attachedPromptFiles.push({ name: file.name, text: text, type: 'text' });
            renderAttachedFilesUI();
        } else if (ext === 'docx') {
            const arrayBuffer = await file.arrayBuffer();
            try {
                const result = await mammoth.extractRawText({ arrayBuffer: arrayBuffer });
                attachedPromptFiles.push({ name: file.name, text: result.value, type: 'text' });
                renderAttachedFilesUI();
            } catch (e) {
                updateStatus(`❌ Failed to parse DOCX: ${e.message}`, true);
            }
        } else if (['pdf', 'png', 'jpg', 'jpeg'].includes(ext)) {
            const reader = new FileReader();
            reader.onload = (e) => {
                attachedPromptFiles.push({
                    name: file.name,
                    data: e.target.result,
                    mimeType: file.type || (ext === 'pdf' ? 'application/pdf' : `image/${ext}`)
                });
                renderAttachedFilesUI();
            };
            reader.readAsDataURL(file);
        } else {
            updateStatus(`❌ Unsupported file type: ${ext}`, true);
        }
    }
    event.target.value = ''; 
}

function renderAttachedFilesUI() {
    const container = document.getElementById('attachedFilesContainer');
    container.innerHTML = '';
    
    attachedPromptFiles.forEach((file, index) => {
        const pill = document.createElement('div');
        pill.className = 'file-pill';
        
        let icon = '📄';
        if (file.name.match(/\.(png|jpe?g)$/i)) icon = '🖼️';
        if (file.name.endsWith('.pdf')) icon = '📕';
        
        pill.innerHTML = `
            <span>${icon} ${file.name}</span>
            <span class="remove-file" data-index="${index}">&times;</span>
        `;
        container.appendChild(pill);
    });

    document.querySelectorAll('.remove-file').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const index = e.target.getAttribute('data-index');
            attachedPromptFiles.splice(index, 1);
            renderAttachedFilesUI();
        });
    });
}

// --- 5. Main Generation Logic ---
async function generateDiagram() {
    const promptInput = document.getElementById('promptInput');
    const prompt = promptInput.value.trim();
    
    if (!prompt && attachedPromptFiles.length === 0) {
        return updateStatus("Please enter a description or attach a context file first!", true);
    }

    updateStatus("🚀 Sending prompt and context to AI backend...");
    document.getElementById('generateBtn').disabled = true;

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                prompt: prompt || "Generate a diagram based on the attached files.", 
                currentCode, 
                type: currentType,
                files: attachedPromptFiles 
            })
        });
        
        updateStatus("🧠 Rendering output...");
        const data = await response.json();
        if (data.error) throw new Error(data.error);

        currentCode = data.code;
        currentType = data.type;
        
        await renderMainOutput(currentCode, currentType);
        promptInput.value = ""; 
        updateStatus(`✅ ${currentType.toUpperCase()} generated successfully!`);
        setTimeout(() => updateStatus("", false, false), 4000);
    } catch (error) {
        updateStatus(`❌ Error: ${error.message}`, true);
    } finally {
        document.getElementById('generateBtn').disabled = false;
    }
}

async function renderMainOutput(code, type) {
    document.getElementById('placeholderText').style.display = 'none';
    const mermaidDiv = document.getElementById('mermaidOutput');
    const drawioIframe = document.getElementById('drawioOutput');

    if (type === 'mermaid') {
        if (!mermaid) return updateStatus("Mermaid library did not load. Cannot render.", true);
        mermaidDiv.style.display = 'block';
        drawioIframe.style.display = 'none';
        try {
            const { svg } = await mermaid.render(`main-mermaid-${Date.now()}`, code);
            mermaidDiv.innerHTML = svg;
        } catch (error) {
            mermaidDiv.innerHTML = `<span style="color:red">Mermaid Error: ${error.message}</span>`;
        }
    } else {
        mermaidDiv.style.display = 'none';
        drawioIframe.style.display = 'block';
        drawioIframe.src = `https://viewer.diagrams.net/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Diagram#R${encodeURIComponent(code)}`;
    }
}

// --- 6. Server Save Logic ---
function getProjectName() {
    return document.getElementById('projectNameInput').value.trim() || 'default_project';
}

async function saveTextToServer(ext) {
    if (!currentCode) return updateStatus("No diagram to save!", true);
    const finalExt = ext === 'drawio' ? 'drawio' : (currentType === 'drawio' ? 'drawio' : 'mmd');
    
    try {
        updateStatus(`💾 Saving as .${finalExt}...`);
        await fetch('/api/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                projectName: getProjectName(), 
                filename: `diagram_${Date.now()}.${finalExt}`, 
                content: currentCode, 
                isImage: false 
            })
        });
        updateStatus(`✅ Diagram saved as .${finalExt}`);
        fetchSavedFiles(); 
        setTimeout(() => updateStatus("", false, false), 3000);
    } catch (error) {
        updateStatus(`❌ Save failed: ${error.message}`, true);
    }
}

async function saveImageToServer(format = 'png') {
    if (currentType !== 'mermaid') {
        return updateStatus(`Image saving currently only supports Mermaid. Save as .drawio instead.`, true);
    }
    
    const svgElement = document.querySelector('#mermaidOutput svg');
    if (!svgElement) return updateStatus("No diagram to save!", true);

    updateStatus(`🖼️ Processing ${format.toUpperCase()}...`);

    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    const img = new Image();
    const rect = svgElement.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;

    img.onload = async () => {
        if (format === 'jpeg') {
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }
        ctx.drawImage(img, 0, 0);
        
        const ext = format === 'jpeg' ? 'jpg' : 'png';
        
        try {
            await fetch('/api/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    projectName: getProjectName(), 
                    filename: `diagram_${Date.now()}.${ext}`, 
                    content: canvas.toDataURL(`image/${format}`), 
                    isImage: true 
                })
            });
            updateStatus(`✅ ${format.toUpperCase()} saved to server!`);
            fetchSavedFiles(); 
            setTimeout(() => updateStatus("", false, false), 3000);
        } catch (error) {
            updateStatus(`❌ Save failed: ${error.message}`, true);
        }
    };
    
    const svgData = new XMLSerializer().serializeToString(svgElement);
    img.src = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svgData)));
}

// --- 7. Sidebar File Browser Logic ---
async function fetchSavedFiles() {
    const treeDiv = document.getElementById('fileBrowserTree');
    treeDiv.innerHTML = "<em>Loading...</em>";
    
    try {
        const response = await fetch('/api/files');
        const projects = await response.json();
        
        if (Object.keys(projects).length === 0) {
            treeDiv.innerHTML = "<p>No saved projects yet.</p>";
            return;
        }
        treeDiv.innerHTML = '';

        for (const [projectName, files] of Object.entries(projects)) {
            const projectBox = document.createElement('div');
            projectBox.className = 'project-box';
            
            const titleContainer = document.createElement('div');
            titleContainer.className = 'project-title-container';
            titleContainer.innerHTML = `<h4>📁 ${projectName}</h4>`;
            
            const deleteProjBtn = document.createElement('button');
            deleteProjBtn.innerHTML = '🗑️';
            deleteProjBtn.className = 'delete-proj-btn';
            deleteProjBtn.title = "Delete entire project";
            deleteProjBtn.onclick = () => deleteProject(projectName);
            
            titleContainer.appendChild(deleteProjBtn);
            projectBox.appendChild(titleContainer);

            const fileList = document.createElement('ul');
            files.forEach(file => {
                const li = document.createElement('li');
                li.className = 'file-item';
                
                let icon = '📄';
                if (file.endsWith('.drawio') || file.endsWith('.xml')) icon = '📐';
                else if (file.match(/\.(png|jpe?g)$/i)) icon = '🖼️';

                const fileSpan = document.createElement('span');
                fileSpan.textContent = `${icon} ${file}`;
                fileSpan.className = 'file-name';
                fileSpan.onclick = () => openPreviewModal(projectName, file);

                const deleteBtn = document.createElement('button');
                deleteBtn.innerHTML = '🗑️';
                deleteBtn.className = 'delete-file-btn';
                deleteBtn.title = "Delete file";
                deleteBtn.onclick = (e) => { 
                    e.stopPropagation(); 
                    deleteFile(projectName, file); 
                };

                li.appendChild(fileSpan);
                li.appendChild(deleteBtn);
                fileList.appendChild(li);
            });
            projectBox.appendChild(fileList);
            treeDiv.appendChild(projectBox);
        }
    } catch (error) {
        treeDiv.innerHTML = `<span style="color:red">Failed to load files. Are you running on localhost:3000?</span>`;
    }
}

async function deleteFile(project, filename) {
    if (!confirm(`Delete "${filename}"?`)) return;
    try {
        await fetch(`/api/files/${encodeURIComponent(project)}/${encodeURIComponent(filename)}`, { method: 'DELETE' });
        fetchSavedFiles();
    } catch (e) {
        updateStatus("❌ Delete failed", true);
    }
}

async function deleteProject(project) {
    if (!confirm(`🚨 Are you sure you want to delete the ENTIRE project "${project}"?`)) return;
    try {
        await fetch(`/api/projects/${encodeURIComponent(project)}`, { method: 'DELETE' });
        fetchSavedFiles();
    } catch (e) {
        updateStatus("❌ Delete failed", true);
    }
}

// --- 8. Modal Live Editor Logic ---
async function openPreviewModal(project, filename) {
    const modal = document.getElementById('previewModal');
    document.getElementById('previewTitle').textContent = `Preview: ${project} / ${filename}`;
    
    document.getElementById('previewImage').style.display = 'none';
    document.getElementById('previewCodeContainer').style.display = 'none';
    document.getElementById('loadIntoEditorBtn').style.display = 'none';

    if (filename.match(/\.(mmd|drawio|xml)$/i)) {
        document.getElementById('previewCodeContainer').style.display = 'flex';
        document.getElementById('loadIntoEditorBtn').style.display = 'inline-block';
        previewType = filename.endsWith('.mmd') ? 'mermaid' : 'drawio';
        
        try {
            const response = await fetch(`/downloads/${project}/${filename}`);
            const code = await response.text();
            document.getElementById('previewCodeEditor').value = code;
            previewCode = code;
            await renderPreviewContent(previewCode, previewType);
        } catch (e) {
            document.getElementById('previewCodeEditor').value = "Failed to load file content.";
        }
    } else {
        const imgEl = document.getElementById('previewImage');
        imgEl.src = `/downloads/${project}/${filename}`;
        imgEl.style.display = 'block';
    }
    modal.style.display = 'block';
}

function updatePreviewFromEditor() {
    previewCode = document.getElementById('previewCodeEditor').value;
    renderPreviewContent(previewCode, previewType);
}

async function renderPreviewContent(code, type) {
    const mermaidEl = document.getElementById('previewMermaid');
    const drawioEl = document.getElementById('previewDrawio');

    if (type === 'mermaid') {
        if (!mermaid) return;
        mermaidEl.style.display = 'block';
        drawioEl.style.display = 'none';
        try {
            const { svg } = await mermaid.render(`preview-render-${Date.now()}`, code);
            mermaidEl.innerHTML = svg;
        } catch (error) {
            mermaidEl.innerHTML = `<span style="color:red; display:inline-block; margin-top:20px;">Render Error: ${error.message}</span>`;
        }
    } else {
        mermaidEl.style.display = 'none';
        drawioEl.style.display = 'block';
        drawioEl.src = `https://viewer.diagrams.net/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Preview#R${encodeURIComponent(code)}`;
    }
}

function loadPreviewIntoEditor() {
    if (previewCode) {
        currentCode = previewCode;
        currentType = previewType;
        renderMainOutput(currentCode, currentType);
        updateStatus("✅ Diagram loaded into main editor.");
        closeModal();
    }
}

function closeModal() {
    document.getElementById('previewModal').style.display = 'none';
    document.getElementById('previewCodeEditor').value = '';
    document.getElementById('previewImage').src = '';
    document.getElementById('previewMermaid').innerHTML = '';
}

// --- 9. Local File Import Logic ---
function loadLocalTextFile(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = async (e) => {
        currentCode = e.target.result; 
        currentType = file.name.endsWith('.drawio') || file.name.endsWith('.xml') ? 'drawio' : 'mermaid';
        
        try {
            await renderMainOutput(currentCode, currentType);
            document.getElementById('promptInput').value = ""; 
            updateStatus(`✅ Loaded local file as ${currentType.toUpperCase()}`);
        } catch (err) {
            updateStatus("❌ Error rendering loaded file", true);
        }
        event.target.value = ''; 
    };
    reader.readAsText(file);
}

// Boot up the app
initApp();