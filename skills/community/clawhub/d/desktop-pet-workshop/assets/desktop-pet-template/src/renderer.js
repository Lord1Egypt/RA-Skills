const { ipcRenderer } = require('electron');

const CONFIG = require('./config.json');

const petImg = document.getElementById('pet-img');

let currentAction = 'idle_breathing';
let idleTimer = null;
let actionTimeout = null;

const IDLE_THRESHOLD = 30000; // 30 seconds

function getActionFile(actionId) {
  const action = CONFIG.actions.find(a => a.id === actionId);
  return action ? action.file : CONFIG.actions[0].file;
}

function switchAction(actionId, autoRevert = false) {
  const action = CONFIG.actions.find(a => a.id === actionId);
  if (!action) return;

  currentAction = actionId;
  petImg.src = '../pet-assets/' + action.file;

  clearTimeout(actionTimeout);
  resetIdleTimer();

  // Actions that play once and revert to idle
  if (autoRevert || action.loop === 'once') {
    const duration = (action.duration || 3) * 1000;
    actionTimeout = setTimeout(() => {
      switchAction('idle_breathing', false);
    }, duration);
  }
}

function resetIdleTimer() {
  clearTimeout(idleTimer);
  idleTimer = setTimeout(() => {
    if (currentAction !== 'sleepy_dozing') {
      switchAction('sleepy_dozing', false);
    }
  }, IDLE_THRESHOLD);
}

// Click interaction
petImg.addEventListener('click', () => {
  switchAction('happy_jumping', true);
});

// Hover interaction
petImg.addEventListener('mouseenter', () => {
  if (currentAction === 'idle_breathing' || currentAction === 'sleepy_dozing') {
    switchAction('cute_cuddling', false);
  }
});

petImg.addEventListener('mouseleave', () => {
  if (currentAction === 'cute_cuddling') {
    switchAction('idle_breathing', false);
  }
});

// Listen for action switches from tray menu
ipcRenderer.on('switch-action', (event, actionId) => {
  const action = CONFIG.actions.find(a => a.id === actionId);
  switchAction(actionId, action && action.loop === 'once');
});

// Start with idle
switchAction('idle_breathing', false);
