const { app, BrowserWindow, screen, ipcMain, Tray, Menu } = require('electron');
const path = require('path');

let mainWindow = null;
let tray = null;
let isIgnoreMouse = false;

function createWindow() {
  const { width: screenWidth, height: screenHeight } = screen.getPrimaryDisplay().workAreaSize;

  mainWindow = new BrowserWindow({
    width: 256,
    height: 256,
    x: screenWidth - 300,
    y: screenHeight - 350,
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    resizable: false,
    maximizable: false,
    minimizable: false,
    fullscreenable: false,
    skipTaskbar: true,
    hasShadow: false,
    webPreferences: {
      preload: path.join(__dirname, 'src', 'renderer.js'),
      contextIsolation: false,
      nodeIntegration: true
    }
  });

  mainWindow.loadFile(path.join(__dirname, 'src', 'index.html'));
  mainWindow.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true });

  // Forward mouse events from renderer for click/hover detection
  ipcMain.on('pet-click', () => {
    mainWindow.webContents.send('switch-action', 'happy_jumping');
  });

  ipcMain.on('pet-hover', () => {
    mainWindow.webContents.send('switch-action', 'cute_cuddling');
  });

  ipcMain.on('pet-leave', () => {
    mainWindow.webContents.send('switch-action', 'idle_breathing');
  });

  ipcMain.on('idle-timeout', () => {
    mainWindow.webContents.send('switch-action', 'sleepy_dozing');
  });

  // Tray menu for manual action switching
  tray = new Tray(null);
  const contextMenu = Menu.buildFromTemplate([
    { label: '待机呼吸', click: () => mainWindow.webContents.send('switch-action', 'idle_breathing') },
    { label: '开心蹦跳', click: () => mainWindow.webContents.send('switch-action', 'happy_jumping') },
    { label: '软萌撒娇', click: () => mainWindow.webContents.send('switch-action', 'cute_cuddling') },
    { label: '犯困打盹', click: () => mainWindow.webContents.send('switch-action', 'sleepy_dozing') },
    { label: '挥手打招呼', click: () => mainWindow.webContents.send('switch-action', 'waving_greeting') },
    { type: 'separator' },
    { label: '退出', click: () => app.quit() }
  ]);
  tray.setContextMenu(contextMenu);
  tray.setToolTip('Desktop Pet');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
