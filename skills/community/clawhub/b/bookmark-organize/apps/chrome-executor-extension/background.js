const EXTENSION_VERSION = "0.1.1";
const LATEST_UNDO_KEY = "latestUndoRecord";
const DEFAULT_BRIDGE_WS_URL = "ws://127.0.0.1:8787/ws";
const BRIDGE_WS_URL_KEY = "bridgeWsUrl";
const BRIDGE_RETRY_MS = 3000;
const BRIDGE_HEARTBEAT_ALARM = "bridge-heartbeat";

let bridgeSocket = null;
let bridgeConnected = false;
let reconnectTimer = null;
let connectingBridge = false;

chrome.runtime.onInstalled.addListener(() => {
  console.log("Bookmark Organize Executor installed");
  ensureHeartbeatAlarm();
  ensureBridgeConnection();
});

chrome.runtime.onStartup?.addListener(() => {
  ensureHeartbeatAlarm();
  ensureBridgeConnection();
});

chrome.alarms?.onAlarm.addListener((alarm) => {
  if (alarm?.name !== BRIDGE_HEARTBEAT_ALARM) {
    return;
  }
  sendBridgeHeartbeat();
  ensureBridgeConnection();
});

ensureHeartbeatAlarm();
ensureBridgeConnection();

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  handleBridgeMessage(message)
    .then(sendResponse)
    .catch((error) => sendResponse(toErrorResponse("INTERNAL_EXECUTION_ERROR", error?.message || String(error))));
  return true;
});

chrome.runtime.onMessageExternal.addListener((message, sender, sendResponse) => {
  handleBridgeMessage(message)
    .then(sendResponse)
    .catch((error) => sendResponse(toErrorResponse("INTERNAL_EXECUTION_ERROR", error?.message || String(error))));
  return true;
});

async function handleBridgeMessage(message) {
  switch (message?.type) {
    case "bridge.health":
      return health();
    case "bridge.context":
      return context(message.scope);
    case "bridge.validate":
      return validate(message.actions || []);
    case "bridge.apply":
      return apply(message.actions || []);
    case "bridge.undo":
      return undo(message.undoToken);
    case "bridge.cleanup_test_artifacts":
      return cleanupTestArtifacts();
    default:
      return toErrorResponse("INVALID_ACTION_PLAN", `Unsupported bridge message: ${String(message?.type || "unknown")}`);
  }
}

async function health() {
  return {
    ok: true,
    extensionVersion: EXTENSION_VERSION,
    browser: "chrome",
    bridgeConnected,
    bridgeUrl: await getBridgeWsUrl(),
    capabilities: {
      readBookmarks: true,
      applyActions: true,
      undo: true
    }
  };
}

async function context(scope) {
  const tree = await getBookmarkTree();
  const normalized = flattenBookmarkTree(tree);
  return {
    bookmarks: normalized.bookmarks,
    folders: normalized.folders,
    scope: scope || { type: "all", label: "All bookmarks" }
  };
}

async function validate(actions) {
  const currentContext = await context({ type: "all", label: "All bookmarks" });
  const folderPaths = new Map(currentContext.folders.map((folder) => [folder.path.join(" / "), { id: folder.id, path: folder.path }]));
  const bookmarkIds = new Set(currentContext.bookmarks.map((bookmark) => bookmark.id));
  const folderIds = new Set(currentContext.folders.map((folder) => folder.id));
  const validatedActions = [];

  for (const action of actions) {
    if (action.type === "create_folder") {
      const parentPath = resolveFolderPath(action.parentId, action.parentPath, currentContext.folders);
      const ok = Boolean(parentPath && action.title);
      if (ok) {
        folderPaths.set([...parentPath, action.title].join(" / "), { id: null, path: [...parentPath, action.title] });
      }
      validatedActions.push({
        actionId: action.actionId,
        type: action.type,
        status: ok ? "valid" : "invalid",
        title: ok ? `Create folder "${action.title}"` : "Cannot create folder",
        description: ok ? `Create under ${parentPath.join(" / ")}` : "Missing a valid parent folder or title",
        executable: ok,
        badge: ok ? "Applicable" : "Invalid"
      });
      continue;
    }

    if (action.type === "move_bookmark") {
      const targetPath = action.targetPath || resolveFolderPath(action.targetFolderId, undefined, currentContext.folders);
      const ok = bookmarkIds.has(action.bookmarkId) && Array.isArray(targetPath) && folderPaths.has(targetPath.join(" / "));
      validatedActions.push({
        actionId: action.actionId,
        type: action.type,
        status: ok ? "valid" : "invalid",
        title: ok ? `Move bookmark ${action.bookmarkId}` : "Cannot move bookmark",
        description: ok ? `Move to ${targetPath.join(" / ")}` : "Bookmark or target folder does not exist",
        executable: ok,
        badge: ok ? "Applicable" : "Invalid"
      });
      continue;
    }

    if (action.type === "rename_bookmark") {
      const ok = bookmarkIds.has(action.bookmarkId) && Boolean(action.newTitle);
      validatedActions.push({
        actionId: action.actionId,
        type: action.type,
        status: ok ? "valid" : "invalid",
        title: ok ? `Rename bookmark ${action.bookmarkId}` : "Cannot rename bookmark",
        description: ok ? `Change to "${action.newTitle}"` : "Bookmark does not exist or the new title is empty",
        executable: ok,
        badge: ok ? "Applicable" : "Invalid"
      });
      continue;
    }

    if (action.type === "rename_folder") {
      const ok = folderIds.has(action.folderId) && Boolean(action.newTitle);
      validatedActions.push({
        actionId: action.actionId,
        type: action.type,
        status: ok ? "valid" : "invalid",
        title: ok ? `Rename folder ${action.folderId}` : "Cannot rename folder",
        description: ok ? `Change to "${action.newTitle}"` : "Folder does not exist or the new title is empty",
        executable: ok,
        badge: ok ? "Applicable" : "Invalid"
      });
      continue;
    }
  }

  return { validatedActions };
}

async function apply(actions) {
  const currentContext = await context({ type: "all", label: "All bookmarks" });
  const folderPathToId = new Map(currentContext.folders.map((folder) => [folder.path.join(" / "), folder.id]));
  const bookmarkMap = new Map(currentContext.bookmarks.map((bookmark) => [bookmark.id, bookmark]));
  const folderMap = new Map(currentContext.folders.map((folder) => [folder.id, folder]));
  const undoSteps = [];
  let appliedCount = 0;
  let skippedCount = 0;

  for (const action of actions) {
    if (action.type === "create_folder") {
      const parentPath = resolveFolderPath(action.parentId, action.parentPath, currentContext.folders);
      const parentId = parentPath ? folderPathToId.get(parentPath.join(" / ")) : null;
      if (!parentId || !action.title) {
        skippedCount += 1;
        continue;
      }

      const created = await bookmarksCreate({ parentId, title: action.title });
      folderPathToId.set([...parentPath, action.title].join(" / "), created.id);
      undoSteps.push({
        type: "delete_folder",
        folderId: created.id,
        title: action.title
      });
      appliedCount += 1;
      continue;
    }

    if (action.type === "rename_bookmark") {
      const bookmark = bookmarkMap.get(action.bookmarkId);
      if (!bookmark || !action.newTitle) {
        skippedCount += 1;
        continue;
      }
      undoSteps.push({
        type: "rename_bookmark",
        bookmarkId: bookmark.id,
        title: bookmark.title
      });
      await bookmarksUpdate(action.bookmarkId, { title: action.newTitle });
      appliedCount += 1;
      continue;
    }

    if (action.type === "rename_folder") {
      const folder = folderMap.get(action.folderId);
      if (!folder || !action.newTitle) {
        skippedCount += 1;
        continue;
      }
      undoSteps.push({
        type: "rename_folder",
        folderId: folder.id,
        title: folder.title
      });
      await bookmarksUpdate(action.folderId, { title: action.newTitle });
      appliedCount += 1;
      continue;
    }

    if (action.type === "move_bookmark") {
      const bookmark = bookmarkMap.get(action.bookmarkId);
      let targetFolderId = action.targetFolderId || null;
      if (!targetFolderId && Array.isArray(action.targetPath)) {
        targetFolderId = await ensureRuntimeFolderPath(action.targetPath, folderPathToId);
      }
      if (!bookmark || !targetFolderId) {
        skippedCount += 1;
        continue;
      }
      undoSteps.push({
        type: "move_bookmark",
        bookmarkId: bookmark.id,
        parentId: bookmark.parentId,
        index: bookmark.index
      });
      await bookmarksMove(action.bookmarkId, { parentId: targetFolderId });
      appliedCount += 1;
      continue;
    }
  }

  const undoToken = {
    kind: "latest-apply",
    id: `apply-${Date.now()}`
  };
  await storageSet({
    [LATEST_UNDO_KEY]: {
      undoToken,
      steps: undoSteps.reverse(),
      createdAt: Date.now()
    }
  });

  return {
    appliedCount,
    skippedCount,
    warnings: [],
    undoToken
  };
}

async function undo(undoToken) {
  const stored = await storageGet(LATEST_UNDO_KEY);
  const latestUndo = stored[LATEST_UNDO_KEY] || null;
  if (!latestUndo) {
    return toErrorResponse("UNDO_NOT_AVAILABLE", "No undo record is available.");
  }
  if (undoToken?.id && latestUndo.undoToken?.id !== undoToken.id) {
    return toErrorResponse("UNDO_NOT_AVAILABLE", "The requested undo token does not match the latest apply.");
  }

  const warnings = [];
  for (const step of latestUndo.steps || []) {
    try {
      await runUndoStep(step);
    } catch (error) {
      warnings.push(String(error?.message || error));
    }
  }
  await storageSet({ [LATEST_UNDO_KEY]: null });
  return {
    ok: warnings.length === 0,
    warnings
  };
}

async function runUndoStep(step) {
  if (step.type === "delete_folder") {
    return bookmarksRemove(step.folderId);
  }
  if (step.type === "rename_bookmark") {
    return bookmarksUpdate(step.bookmarkId, { title: step.title });
  }
  if (step.type === "rename_folder") {
    return bookmarksUpdate(step.folderId, { title: step.title });
  }
  if (step.type === "move_bookmark") {
    const safeIndex = await getSafeBookmarkMoveIndex(step.parentId, step.index);
    return bookmarksMove(step.bookmarkId, { parentId: step.parentId, index: safeIndex });
  }
}

async function cleanupTestArtifacts() {
  const allowedTitles = new Set([
    "OpenClaw Skill E2E Test",
    "可删除 - E2E Test",
    "Smoke Test Folder"
  ]);
  const tree = await getBookmarkTree();
  const normalized = flattenBookmarkTree(tree);
  const removed = [];
  const skipped = [];

  for (const folder of normalized.folders) {
    if (!allowedTitles.has(folder.title)) {
      continue;
    }

    const children = await bookmarksGetChildren(folder.id);
    if (children.length > 0) {
      skipped.push({
        id: folder.id,
        title: folder.title,
        reason: "folder_not_empty"
      });
      continue;
    }

    await bookmarksRemoveTree(folder.id);
    removed.push({
      id: folder.id,
      title: folder.title,
      path: folder.path
    });
  }

  return {
    ok: true,
    removed,
    skipped
  };
}

async function ensureRuntimeFolderPath(targetPath, folderPathToId) {
  const existingId = folderPathToId.get(targetPath.join(" / ")) || null;
  if (existingId) {
    return existingId;
  }

  let deepestExistingLength = 0;
  for (let length = targetPath.length; length > 0; length -= 1) {
    if (folderPathToId.has(targetPath.slice(0, length).join(" / "))) {
      deepestExistingLength = length;
      break;
    }
  }

  for (let index = deepestExistingLength + 1; index <= targetPath.length; index += 1) {
    const currentPath = targetPath.slice(0, index);
    const currentKey = currentPath.join(" / ");
    if (folderPathToId.has(currentKey)) {
      continue;
    }
    const parentPath = currentPath.slice(0, -1);
    const parentId = folderPathToId.get(parentPath.join(" / ")) || null;
    const title = currentPath[currentPath.length - 1];
    if (!parentId || !title) {
      return null;
    }
    const created = await bookmarksCreate({ parentId, title });
    folderPathToId.set(currentKey, created.id);
  }

  return folderPathToId.get(targetPath.join(" / ")) || null;
}

function flattenBookmarkTree(tree) {
  const bookmarks = [];
  const folders = [];

  function visit(node, parentPath = []) {
    const title = node.title || "";
    const path = node.id === "0" ? [] : [...parentPath, title].filter(Boolean);

    if (node.url) {
      bookmarks.push({
        id: node.id,
        title,
        url: node.url,
        path: parentPath,
        parentId: node.parentId || "0",
        index: node.index
      });
      return;
    }

    if (node.id !== "0") {
      folders.push({
        id: node.id,
        title,
        path,
        parentId: node.parentId || "0",
        index: node.index
      });
    }

    for (const child of node.children || []) {
      visit(child, path);
    }
  }

  for (const root of tree) {
    visit(root, []);
  }

  return { bookmarks, folders };
}

function resolveFolderPath(folderId, folderPath, folders) {
  if (Array.isArray(folderPath) && folderPath.length > 0) {
    return folderPath;
  }
  if (!folderId) {
    return null;
  }
  const folder = folders.find((item) => item.id === folderId);
  return folder ? folder.path : null;
}

function toErrorResponse(code, message) {
  return {
    error: {
      code,
      message
    }
  };
}

function getBookmarkTree() {
  return new Promise((resolve, reject) => {
    chrome.bookmarks.getTree((tree) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
        return;
      }
      resolve(tree);
    });
  });
}

function bookmarksCreate(payload) {
  return new Promise((resolve, reject) => {
    chrome.bookmarks.create(payload, (node) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
        return;
      }
      resolve(node);
    });
  });
}

function bookmarksUpdate(id, changes) {
  return new Promise((resolve, reject) => {
    chrome.bookmarks.update(id, changes, (node) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
        return;
      }
      resolve(node);
    });
  });
}

function bookmarksMove(id, destination) {
  return new Promise((resolve, reject) => {
    chrome.bookmarks.move(id, destination, (node) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
        return;
      }
      resolve(node);
    });
  });
}

function bookmarksRemove(id) {
  return new Promise((resolve, reject) => {
    chrome.bookmarks.remove(id, () => {
      if (chrome.runtime.lastError) {
        const message = chrome.runtime.lastError.message || "";
        if (message.includes("Can't find bookmark")) {
          resolve();
          return;
        }
        reject(chrome.runtime.lastError);
        return;
      }
      resolve();
    });
  });
}

function bookmarksRemoveTree(id) {
  return new Promise((resolve, reject) => {
    chrome.bookmarks.removeTree(id, () => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
        return;
      }
      resolve();
    });
  });
}

function bookmarksGetChildren(parentId) {
  return new Promise((resolve, reject) => {
    chrome.bookmarks.getChildren(parentId, (nodes) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
        return;
      }
      resolve(Array.isArray(nodes) ? nodes : []);
    });
  });
}

function storageGet(key) {
  return new Promise((resolve) => chrome.storage.local.get(key, resolve));
}

function storageSet(payload) {
  return new Promise((resolve) => chrome.storage.local.set(payload, resolve));
}

async function getSafeBookmarkMoveIndex(parentId, desiredIndex) {
  if (!parentId || typeof desiredIndex !== "number" || Number.isNaN(desiredIndex)) {
    return undefined;
  }
  const children = await new Promise((resolve, reject) => {
    chrome.bookmarks.getChildren(parentId, (nodes) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
        return;
      }
      resolve(Array.isArray(nodes) ? nodes : []);
    });
  });

  return Math.max(0, Math.min(desiredIndex, children.length));
}

async function getBridgeWsUrl() {
  const stored = await storageGet(BRIDGE_WS_URL_KEY);
  const configured = stored[BRIDGE_WS_URL_KEY];
  return typeof configured === "string" && configured.trim() ? configured.trim() : DEFAULT_BRIDGE_WS_URL;
}

async function ensureBridgeConnection() {
  if (bridgeSocket && (bridgeSocket.readyState === WebSocket.OPEN || bridgeSocket.readyState === WebSocket.CONNECTING)) {
    return;
  }
  if (connectingBridge) {
    return;
  }
  connectingBridge = true;
  clearReconnectTimer();

  try {
    const bridgeUrl = await getBridgeWsUrl();
    const socket = new WebSocket(bridgeUrl);
    bridgeSocket = socket;

    socket.addEventListener("open", () => {
      connectingBridge = false;
      bridgeConnected = true;
      socket.send(JSON.stringify({
        type: "hello",
        role: "chrome-executor",
        extensionVersion: EXTENSION_VERSION,
        capabilities: {
          readBookmarks: true,
          applyActions: true,
          undo: true
        }
      }));
      sendBridgeHeartbeat();
    });

    socket.addEventListener("message", async (event) => {
      let payload;
      try {
        payload = JSON.parse(event.data);
      } catch (error) {
        console.warn("Failed to parse bridge payload", error);
        return;
      }

      if (payload?.type !== "request" || !payload.requestId) {
        return;
      }

      let response;
      try {
        response = await handleBridgeMessage(payload.message);
      } catch (error) {
        response = toErrorResponse("INTERNAL_EXECUTION_ERROR", error?.message || String(error));
      }

      if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
          type: "response",
          requestId: payload.requestId,
          response
        }));
      }
    });

    socket.addEventListener("close", () => {
      connectingBridge = false;
      bridgeConnected = false;
      if (bridgeSocket === socket) {
        bridgeSocket = null;
      }
      scheduleReconnect();
    });

    socket.addEventListener("error", () => {
      connectingBridge = false;
      bridgeConnected = false;
    });
  } catch (error) {
    connectingBridge = false;
    bridgeConnected = false;
    scheduleReconnect();
  }
}

function scheduleReconnect() {
  if (reconnectTimer) {
    return;
  }
  reconnectTimer = setTimeout(() => {
    reconnectTimer = null;
    ensureBridgeConnection();
  }, BRIDGE_RETRY_MS);
}

function clearReconnectTimer() {
  if (!reconnectTimer) {
    return;
  }
  clearTimeout(reconnectTimer);
  reconnectTimer = null;
}

function ensureHeartbeatAlarm() {
  chrome.alarms?.create(BRIDGE_HEARTBEAT_ALARM, {
    periodInMinutes: 1
  });
}

function sendBridgeHeartbeat() {
  if (!bridgeSocket || bridgeSocket.readyState !== WebSocket.OPEN) {
    return;
  }

  bridgeSocket.send(JSON.stringify({
    type: "heartbeat",
    role: "chrome-executor",
    extensionVersion: EXTENSION_VERSION,
    sentAt: Date.now()
  }));
}
