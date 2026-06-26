const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

class CaptchaCache {
  constructor(options = {}) {
    this.maxEntries = Number.isInteger(options.maxEntries) ? options.maxEntries : 500;
    this.ttlMs = Number.isInteger(options.ttlMs) ? options.ttlMs : 1000 * 60 * 60;
    this.store = new Map();
    this.verifiedFile = typeof options.verifiedFile === "string"
      ? options.verifiedFile
      : path.resolve(process.cwd(), ".captcha-verified.json");
    this.verified = null;
  }

  static sha1(buffer) {
    if (!Buffer.isBuffer(buffer)) {
      throw new TypeError("Captcha image must be a Buffer");
    }
    return crypto.createHash("sha1").update(buffer).digest("hex");
  }

  get(hash) {
    const verified = this.getVerified(hash);
    if (verified) {
      return verified;
    }

    const item = this.store.get(hash);
    if (!item) {
      return null;
    }
    if (Date.now() > item.expiresAt) {
      this.store.delete(hash);
      return null;
    }
    return item.value;
  }

  set(hash, value) {
    if (this.store.size >= this.maxEntries) {
      const oldestKey = this.store.keys().next().value;
      if (oldestKey) {
        this.store.delete(oldestKey);
      }
    }
    this.store.set(hash, {
      value,
      expiresAt: Date.now() + this.ttlMs
    });
  }

  loadVerified() {
    if (this.verified) {
      return;
    }
    this.verified = new Map();
    try {
      if (!fs.existsSync(this.verifiedFile)) {
        return;
      }
      const raw = fs.readFileSync(this.verifiedFile, "utf8");
      const parsed = JSON.parse(raw);
      for (const [hash, value] of Object.entries(parsed || {})) {
        if (typeof value === "string" && value) {
          this.verified.set(hash, value);
        }
      }
    } catch {
      this.verified = new Map();
    }
  }

  getVerified(hash) {
    this.loadVerified();
    const value = this.verified.get(hash);
    if (!value) {
      return null;
    }
    return {
      solved: true,
      value,
      type: /^\d+$/.test(value) ? "numeric" : "alphanumeric",
      confidence: 100,
      hash,
      verified: true
    };
  }

  setVerified(hash, value) {
    this.loadVerified();
    this.verified.set(hash, value);
    const payload = {};
    for (const [k, v] of this.verified.entries()) {
      payload[k] = v;
    }
    fs.writeFileSync(this.verifiedFile, JSON.stringify(payload, null, 2), "utf8");
  }
}

module.exports = {
  CaptchaCache
};
