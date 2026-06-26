/**
 * Auto Video Generator Web UI - Frontend Application
 * Handles user interactions, API calls, and real-time updates
 */

// ============================================================
// Global State
// ============================================================

const state = {
    currentMode: 'file',
    selectedFile: null,
    currentTaskId: null,
    socket: null,
    startTime: null,
    timerInterval: null,
};

// ============================================================
// Initialization
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeSocket();
    loadTemplates();
    loadRecentTasks();
    
    console.log('Auto Video Generator Web UI initialized');
});

function initializeSocket() {
    state.socket = io();
    
    state.socket.on('connect', () => {
        console.log('Connected to server');
        showToast('Connected to server', 'success');
    });
    
    state.socket.on('task_progress', (data) => {
        updateProgress(data.progress, data.stage);
    });
    
    state.socket.on('task_completed', (data) => {
        handleTaskCompleted(data);
    });
    
    state.socket.on('task_failed', (data) => {
        handleTaskFailed(data.error);
    });
    
    state.socket.on('disconnect', () => {
        console.log('Disconnected from server');
        showToast('Connection lost. Reconnecting...', 'warning');
    });
}

// ============================================================
// Input Mode Switching
// ============================================================

function switchMode(mode) {
    state.currentMode = mode;
    
    // Update button states
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });
    
    // Show/hide input areas
    document.querySelectorAll('.input-area').forEach(area => {
        area.classList.remove('active');
    });
    
    document.getElementById(`${mode}-input-area`).classList.add('active');
}

// ============================================================
// File Upload Handling
// ============================================================

function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    
    const dropZone = document.getElementById('drop-zone');
    dropZone.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('drop-zone').classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('drop-zone').classList.remove('dragover');
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

async function processFile(file) {
    // Validate file type
    const allowedExtensions = ['html', 'vue', 'tsx', 'jsx', 'json', 'yaml', 'yml', 'md'];
    const extension = file.name.split('.').pop().toLowerCase();
    
    if (!allowedExtensions.includes(extension)) {
        showToast(`Unsupported file type: .${extension}`, 'error');
        return;
    }
    
    // Validate file size (50MB max)
    if (file.size > 50 * 1024 * 1024) {
        showToast('File too large. Maximum size is 50MB.', 'error');
        return;
    }
    
    // Upload file
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        showLoading(true);
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData,
        });
        
        const result = await response.json();
        
        if (result.success) {
            state.selectedFile = result.data;
            
            // Update UI
            document.getElementById('file-info').classList.remove('hidden');
            document.getElementById('selected-filename').textContent = result.data.original_name;
            document.getElementById('selected-filesize').textContent = formatFileSize(result.data.size);
            
            showToast(`File uploaded: ${result.data.original_name}`, 'success');
        } else {
            throw new Error(result.error || 'Upload failed');
        }
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function clearFile() {
    state.selectedFile = null;
    document.getElementById('file-info').classList.add('hidden');
    document.getElementById('file-input').value = '';
}

// ============================================================
// Video Generation
// ============================================================

async function startGeneration() {
    // Validate input
    let inputData = {};
    
    if (state.currentMode === 'file') {
        if (!state.selectedFile) {
            showToast('Please upload a file first', 'warning');
            return;
        }
        inputData = {
            type: 'file',
            input_data: state.selectedFile.path,
        };
    } else if (state.currentMode === 'url') {
        const url = document.getElementById('page-url').value.trim();
        if (!url) {
            showToast('Please enter a URL', 'warning');
            return;
        }
        if (!url.startsWith('http') && !url.startsWith('file://')) {
            showToast('Please enter a valid URL (http/https/file)', 'warning');
            return;
        }
        inputData = {
            type: 'url',
            input_data: url,
        };
    } else if (state.currentMode === 'template') {
        const selectedTemplate = document.querySelector('.template-card.selected');
        if (!selectedTemplate) {
            showToast('Please select a template', 'warning');
            return;
        }
        inputData = {
            type: 'template',
            input_data: selectedTemplate.dataset.id,
        };
    }
    
    // Gather configuration
    const config = {
        browser: {
            headless: document.getElementById('cfg-headless').checked,
            viewport_width: parseInt(document.getElementById('cfg-width').value),
            viewport_height: parseInt(document.getElementById('cfg-height').value),
        },
        video: {
            fps: parseInt(document.getElementById('cfg-fps').value),
            quality: document.getElementById('cfg-quality').value,
        },
        audio: {
            voice: document.getElementById('cfg-voice').value,
            rate: document.getElementById('cfg-rate').value,
            volume: document.getElementById('cfg-volume').value,
        },
    };
    
    inputData.config = config;
    
    try {
        // Disable generate button
        const generateBtn = document.getElementById('generate-btn');
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="spinner"></span> Generating...';
        
        // Start generation
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(inputData),
        });
        
        const result = await response.json();
        
        if (result.success) {
            state.currentTaskId = result.data.task_id;
            state.startTime = Date.now();
            
            // Update UI for processing
            updateStatusUI('processing');
            document.getElementById('task-id-display').textContent = `Task: ${result.data.task_id}`;
            
            // Subscribe to task updates
            if (state.socket) {
                state.socket.emit('subscribe_task', { task_id: result.data.task_id });
            }
            
            // Start elapsed time timer
            startTimer();
            
            showToast('Video generation started!', 'info');
        } else {
            throw new Error(result.error || 'Failed to start generation');
        }
    } catch (error) {
        showToast(error.message, 'error');
        resetGenerateButton();
    }
}

function updateProgress(progress, stage) {
    // Update progress bar
    const progressBar = document.getElementById('progress-bar');
    const progressPercent = document.getElementById('progress-percent');
    const stageText = document.getElementById('stage-text');
    
    progressBar.style.width = `${progress}%`;
    progressPercent.textContent = `${Math.round(progress)}%`;
    stageText.textContent = stage || 'Processing...';
    
    // Update status badge
    const statusBadge = document.getElementById('status-badge');
    statusBadge.className = 'status-badge status-processing';
    statusBadge.textContent = 'Processing';
    
    // Estimate remaining time
    if (progress > 0 && progress < 100) {
        const elapsed = (Date.now() - state.startTime) / 1000;
        const totalEstimated = (elapsed / progress) * 100;
        const remaining = totalEstimated - elapsed;
        
        document.getElementById('remaining-time').textContent = formatTime(remaining);
    }
}

function handleTaskCompleted(data) {
    stopTimer();
    
    updateStatusUI('completed');
    document.getElementById('stage-text').textContent = 'Generation complete!';
    
    // Show output info
    document.getElementById('output-info').classList.remove('hidden');
    document.getElementById('preview-empty').classList.add('hidden');
    
    // Set video source
    const videoPlayer = document.getElementById('video-player');
    videoPlayer.src = `/api/preview/${data.output_file}`;
    videoPlayer.classList.remove('hidden');
    
    // Update download button
    document.getElementById('download-btn').onclick = () => downloadVideo(data.output_file);
    
    // Load task details
    loadTaskDetails(state.currentTaskId);
    
    showToast('Video generated successfully!', 'success');
    resetGenerateButton();
    
    // Refresh recent tasks
    loadRecentTasks();
}

function handleTaskFailed(error) {
    stopTimer();
    
    updateStatusUI('failed');
    document.getElementById('stage-text').textContent = `Error: ${error}`;
    
    showToast(`Generation failed: ${error}`, 'error');
    resetGenerateButton();
}

function resetGenerateButton() {
    const generateBtn = document.getElementById('generate-btn');
    generateBtn.disabled = false;
    generateBtn.innerHTML = '▶️ Generate Video Now';
}

// ============================================================
// Timer Functions
// ============================================================

function startTimer() {
    document.getElementById('started-time').textContent = formatTime(0);
    
    state.timerInterval = setInterval(() => {
        const elapsed = (Date.now() - state.startTime) / 1000;
        document.getElementById('elapsed-time').textContent = formatTime(elapsed);
    }, 1000);
}

function stopTimer() {
    if (state.timerInterval) {
        clearInterval(state.timerInterval);
        state.timerInterval = null;
    }
}

// ============================================================
// Status UI Updates
// ============================================================

function updateStatusUI(status) {
    const statusBadge = document.getElementById('status-badge');
    
    switch (status) {
        case 'processing':
            statusBadge.className = 'status-badge status-processing';
            statusBadge.textContent = 'Processing';
            break;
        case 'completed':
            statusBadge.className = 'status-badge status-completed';
            statusBadge.textContent = 'Completed';
            break;
        case 'failed':
            statusBadge.className = 'status-badge status-failed';
            statusBadge.textContent = 'Failed';
            break;
        default:
            statusBadge.className = 'status-badge status-pending';
            statusBadge.textContent = 'Ready';
    }
}

// ============================================================
// Download & Actions
// ============================================================

function downloadVideo(filename = null) {
    const file = filename || state.currentOutputFile;
    if (!file) {
        showToast('No video available for download', 'warning');
        return;
    }
    
    window.open(`/api/download/${file}`, '_blank');
}

function shareVideo() {
    const url = window.location.href;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(() => {
            showToast('Link copied to clipboard!', 'success');
        });
    } else {
        showToast('Share link: ' + url, 'info');
    }
}

function generateNew() {
    // Reset UI
    state.currentTaskId = null;
    state.selectedFile = null;
    
    document.getElementById('progress-bar').style.width = '0%';
    document.getElementById('progress-percent').textContent = '0%';
    document.getElementById('stage-text').textContent = 'Waiting to start...';
    document.getElementById('output-info').classList.add('hidden');
    document.getElementById('preview-empty').classList.remove('hidden');
    document.getElementById('video-player').classList.add('hidden');
    document.getElementById('video-player').src = '';
    document.getElementById('task-id-display').textContent = 'No task running';
    
    updateStatusUI('pending');
    clearFile();
    
    showToast('Ready for new video generation', 'info');
}

// ============================================================
// Templates & History
// ============================================================

async function loadTemplates() {
    try {
        const response = await fetch('/api/templates');
        const result = await response.json();
        
        if (result.success) {
            renderTemplates(result.data);
        }
    } catch (error) {
        console.error('Failed to load templates:', error);
    }
}

function renderTemplates(templates) {
    const grid = document.getElementById('templates-grid');
    const modalBody = document.getElementById('templates-modal-body');
    
    const html = templates.map(template => `
        <div class="template-card" data-id="${template.id}" onclick="selectTemplate(this)">
            <div class="template-icon">${template.icon}</div>
            <div class="template-name">${template.name}</div>
            <div class="template-desc">${template.description}</div>
        </div>
    `).join('');
    
    grid.innerHTML = html;
    modalBody.innerHTML = `
        <div class="templates-grid">
            ${html}
        </div>
    `;
}

function selectTemplate(element) {
    document.querySelectorAll('.template-card').forEach(card => {
        card.classList.remove('selected');
    });
    element.classList.add('selected');
    
    showToast(`Selected: ${element.querySelector('.template-name').textContent}`, 'info');
}

function showTemplates() {
    document.getElementById('templates-modal').classList.remove('hidden');
}

async function loadRecentTasks() {
    try {
        const response = await fetch('/api/tasks?limit=5');
        const result = await response.json();
        
        if (result.success && result.data.length > 0) {
            renderRecentTasks(result.data);
        }
    } catch (error) {
        console.error('Failed to load tasks:', error);
    }
}

function renderRecentTasks(tasks) {
    const container = document.getElementById('recent-tasks');
    
    container.innerHTML = tasks.map(task => `
        <div class="task-item" onclick="loadTaskDetails('${task.id}')">
            <div class="task-info">
                <div style="display:flex;align-items:center;">
                    <span class="task-status-dot ${getStatusDotClass(task.status)}"></span>
                    <span class="task-type">Task ${task.id}</span>
                </div>
                <div class="task-time">${formatDateTime(task.created_at)}</div>
            </div>
        </div>
    `).join('');
}

async function showHistory() {
    try {
        const response = await fetch('/api/tasks?limit=50');
        const result = await response.json();
        
        if (result.success) {
            const tbody = document.getElementById('history-table-body');
            
            tbody.innerHTML = result.data.map(task => `
                <tr>
                    <td><code>${task.id}</code></td>
                    <td>${task.type}</td>
                    <td>
                        <span class="status-badge status-${task.status}">
                            ${task.status.charAt(0).toUpperCase() + task.status.slice(1)}
                        </span>
                    </td>
                    <td>${task.progress}%</td>
                    <td>${formatDateTime(task.created_at)}</td>
                    <td>
                        ${task.output_file 
                            ? `<button class="btn btn-primary btn-sm" onclick="downloadVideo('${task.output_file}')">Download</button>`
                            : '-'
                        }
                    </td>
                </tr>
            `).join('');
            
            document.getElementById('history-modal').classList.remove('hidden');
        }
    } catch (error) {
        showToast('Failed to load history', 'error');
    }
}

async function loadTaskDetails(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`);
        const result = await response.json();
        
        if (result.success && result.data.result) {
            const data = result.data;
            
            document.getElementById('output-filename').textContent = data.output_file || '--';
            document.getElementById('output-duration').textContent = data.result?.duration || '--';
            document.getElementById('output-size').textContent = data.result?.file_size || '--';
            document.getElementById('output-resolution').textContent = data.result?.resolution || '--';
            
            if (data.output_file) {
                state.currentOutputFile = data.output_file;
                
                const videoPlayer = document.getElementById('video-player');
                videoPlayer.src = `/api/preview/${data.output_file}`;
                videoPlayer.classList.remove('hidden');
                document.getElementById('preview-empty').classList.add('hidden');
                document.getElementById('output-info').classList.remove('hidden');
            }
        }
    } catch (error) {
        console.error('Failed to load task details:', error);
    }
}

// ============================================================
// Configuration Sections Toggle
// ============================================================

function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    const icon = section.previousElementSibling.querySelector('.toggle-icon');
    
    section.classList.toggle('open');
    icon.classList.toggle('collapsed');
}

// ============================================================
// Modal Functions
// ============================================================

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

// Close modal on outside click
document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });
});

// ============================================================
// Toast Notifications
// ============================================================

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ',
    };
    
    toast.innerHTML = `<span>${icons[type] || ''}</span> ${message}`;
    container.appendChild(toast);
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ============================================================
// Utility Functions
// ============================================================

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function formatDateTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('zh-CN', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getStatusDotClass(status) {
    const classes = {
        completed: 'status-dot-success',
        processing: 'status-dot-processing',
        failed: 'status-dot-failed',
        pending: '',
    };
    return classes[status] || '';
}

function showLoading(show) {
    const generateBtn = document.getElementById('generate-btn');
    if (show) {
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="spinner"></span> Processing...';
    } else {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '▶️ Generate Video Now';
    }
}

// Add spinner CSS dynamically
const style = document.createElement('style');
style.textContent = `
    .spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

console.log('Web UI application loaded successfully');
