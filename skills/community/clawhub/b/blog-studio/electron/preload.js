const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('blogstudio', {
    // GitHub operations
    githubGet: (path) => ipcRenderer.invoke('github-get', path),
    githubPut: (path, content, message) => ipcRenderer.invoke('github-put', path, content, message),
    githubDelete: (path, message) => ipcRenderer.invoke('github-delete', path, message),
    
    // Utility
    openExternal: (url) => ipcRenderer.invoke('open-external', url),
    showDialog: (options) => ipcRenderer.invoke('show-dialog', options),
    
    // Events
    onInit: (callback) => ipcRenderer.on('init', (event, data) => callback(data))
});