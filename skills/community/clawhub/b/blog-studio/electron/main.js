const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

// Load GitHub token
const tokenFile = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw/workspace/secrets/github-token.txt');
let GITHUB_TOKEN = '';
if (fs.existsSync(tokenFile)) {
    GITHUB_TOKEN = fs.readFileSync(tokenFile, 'utf8').trim();
}

const REPO_OWNER = 'TheSolAI';
const REPO_NAME = 'thesolai.github.io';
const BASE_URL = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}`;

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 900,
        minHeight: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        },
        title: 'BlogStudio — Sol AI',
        backgroundColor: '#FDFBF7'
    });
    
    win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
    
    // Send token to renderer when ready
    win.webContents.on('did-finish-load', () => {
        win.webContents.send('init', { token: GITHUB_TOKEN, baseUrl: BASE_URL });
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

// IPC Handlers for GitHub API
ipcMain.handle('github-get', async (event, apiPath) => {
    const { default: fetch } = await import('node-fetch');
    const res = await fetch(`${BASE_URL}/contents/${apiPath}`, {
        headers: {
            'Authorization': `token ${GITHUB_TOKEN}`,
            'Accept': 'application/vnd.github.v3+json'
        }
    });
    return res.json();
});

ipcMain.handle('github-put', async (event, apiPath, content, message) => {
    const { default: fetch } = await import('node-fetch');
    const res = await fetch(`${BASE_URL}/contents/${apiPath}`, {
        method: 'PUT',
        headers: {
            'Authorization': `token ${GITHUB_TOKEN}`,
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message,
            content: Buffer.from(content).toString('base64'),
            branch: 'main'
        })
    });
    return res.json();
});

ipcMain.handle('github-delete', async (event, apiPath, message) => {
    const { default: fetch } = await import('node-fetch');
    // First get the file SHA
    const getRes = await fetch(`${BASE_URL}/contents/${apiPath}`, {
        headers: {
            'Authorization': `token ${GITHUB_TOKEN}`,
            'Accept': 'application/vnd.github.v3+json'
        }
    });
    const fileData = await getRes.json();
    if (!fileData.sha) {
        throw new Error('Could not get file SHA for deletion');
    }
    const res = await fetch(`${BASE_URL}/contents/${apiPath}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `token ${GITHUB_TOKEN}`,
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message,
            sha: fileData.sha,
            branch: 'main'
        })
    });
    return res.json();
});

ipcMain.handle('open-external', async (event, url) => {
    const { shell } = require('electron');
    return shell.openExternal(url);
});

ipcMain.handle('show-dialog', async (event, options) => {
    return dialog.showOpenDialog(options);
});