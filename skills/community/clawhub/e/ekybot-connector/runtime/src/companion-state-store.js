const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');

class EkybotCompanionStateStore {
  constructor(filePath = null) {
    this.filePath =
      filePath ||
      process.env.EKYBOT_COMPANION_STATE_PATH ||
      path.join(os.homedir(), '.config', 'ekybot-companion', 'state.json');
    this.identityFilePath =
      process.env.EKYBOT_COMPANION_IDENTITY_PATH ||
      path.join(os.homedir(), '.config', 'ekybot-companion', 'machine.json');
  }

  ensureParentDir() {
    fs.mkdirSync(path.dirname(this.filePath), { recursive: true });
  }

  ensureIdentityParentDir() {
    fs.mkdirSync(path.dirname(this.identityFilePath), { recursive: true });
  }

  load() {
    if (!fs.existsSync(this.filePath)) {
      return null;
    }

    return JSON.parse(fs.readFileSync(this.filePath, 'utf8'));
  }

  loadIdentity() {
    if (!fs.existsSync(this.identityFilePath)) {
      return null;
    }

    return JSON.parse(fs.readFileSync(this.identityFilePath, 'utf8'));
  }

  saveIdentity(identity) {
    this.ensureIdentityParentDir();
    fs.writeFileSync(
      this.identityFilePath,
      JSON.stringify(
        {
          ...identity,
          updatedAt: new Date().toISOString(),
        },
        null,
        2
      ),
      'utf8'
    );
  }

  ensureDeviceIdentity() {
    const current = this.loadIdentity();

    if (current?.deviceId) {
      return current;
    }

    const next = {
      deviceId: crypto.randomUUID(),
      createdAt: new Date().toISOString(),
    };

    this.saveIdentity(next);
    return next;
  }

  computeMachineFingerprint(rootConfigPath) {
    const identity = this.ensureDeviceIdentity();
    const normalizedRootConfigPath = rootConfigPath || 'unknown-openclaw-root';
    return crypto
      .createHash('sha256')
      .update(`${identity.deviceId}:${normalizedRootConfigPath}`)
      .digest('hex');
  }

  save(state) {
    this.ensureParentDir();
    fs.writeFileSync(
      this.filePath,
      JSON.stringify(
        {
          ...state,
          updatedAt: new Date().toISOString(),
        },
        null,
        2
      ),
      'utf8'
    );
  }

  merge(patch) {
    const current = this.load() || {};
    const nextPatch = typeof patch === 'function' ? patch(current) : patch;
    this.save({
      ...current,
      ...nextPatch,
    });
  }

  upsertActiveRequest(request) {
    if (!request?.requestId) {
      return;
    }

    this.merge((current) => {
      const activeRequests = Array.isArray(current.activeRequests) ? current.activeRequests : [];
      const nextEntry = {
        ...activeRequests.find((entry) => entry.requestId === request.requestId),
        ...request,
        lastHeartbeatAt: request.lastHeartbeatAt || new Date().toISOString(),
      };

      return {
        activeRequests: [
          ...activeRequests.filter((entry) => entry.requestId !== request.requestId),
          nextEntry,
        ],
      };
    });
  }

  clearActiveRequest(requestId) {
    if (!requestId) {
      return;
    }

    this.merge((current) => ({
      activeRequests: (Array.isArray(current.activeRequests) ? current.activeRequests : []).filter(
        (entry) => entry.requestId !== requestId
      ),
    }));
  }

  clear() {
    if (fs.existsSync(this.filePath)) {
      fs.unlinkSync(this.filePath);
    }
  }
}

module.exports = EkybotCompanionStateStore;
