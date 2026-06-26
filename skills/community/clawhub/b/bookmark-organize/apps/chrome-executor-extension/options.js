const DEFAULT_BRIDGE_WS_URL = "ws://127.0.0.1:8787/ws";
const BRIDGE_WS_URL_KEY = "bridgeWsUrl";

const bridgeUrlInput = document.getElementById("bridgeUrlInput");
const saveBridgeUrlButton = document.getElementById("saveBridgeUrlButton");

chrome.storage.local.get(BRIDGE_WS_URL_KEY, (stored) => {
  if (bridgeUrlInput) {
    bridgeUrlInput.value = stored[BRIDGE_WS_URL_KEY] || DEFAULT_BRIDGE_WS_URL;
  }
});

saveBridgeUrlButton?.addEventListener("click", () => {
  const nextUrl = bridgeUrlInput?.value?.trim() || DEFAULT_BRIDGE_WS_URL;
  chrome.storage.local.set({ [BRIDGE_WS_URL_KEY]: nextUrl }, () => {
    setStatusText(`Bridge URL saved. Reload the extension or wait for reconnect. URL: ${nextUrl}`);
  });
});

chrome.runtime.sendMessage({ type: "bridge.health" }, (response) => {
  const statusText = document.getElementById("statusText");
  if (!statusText) {
    return;
  }

  if (chrome.runtime.lastError) {
    statusText.textContent = `Health check failed: ${chrome.runtime.lastError.message}`;
    return;
  }

  if (!response?.ok) {
    statusText.textContent = "Extension is installed, but the bridge is not ready.";
    return;
  }

  const bridgeState = response.bridgeConnected ? "Bridge connected" : "Waiting for local bridge server";
  statusText.textContent = `${bridgeState}. Version ${response.extensionVersion || "0.1.0"} using ${response.bridgeUrl || DEFAULT_BRIDGE_WS_URL}.`;
});

function setStatusText(message) {
  const statusText = document.getElementById("statusText");
  if (statusText) {
    statusText.textContent = message;
  }
}
