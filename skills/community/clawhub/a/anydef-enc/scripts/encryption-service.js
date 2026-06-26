/**
 * Encryption Service (Manual Local Mode)
 * 
 * Implements MK -> KEK -> DEK hierarchy using PBKDF2 for Master Key derivation.
 * Supports reboot persistence by ensuring the same passphrase always yields the same MK.
 */

export class EncryptionService {
  private static masterKey: CryptoKey | null = null;
  private static kek: CryptoKey | null = null;
  private static deks: Map<string, CryptoKey> = new Map();

  /**
   * Unlocks the vault using a user-provided passphrase.
   * Derives a deterministic Master Key (MK) using PBKDF2 + a persistent Salt.
   */
  static async unlock(passphrase: string) {
    const encoder = new TextEncoder();
    
    // 1. Get or Initialize a persistent salt to ensure deterministic MK across reboots
    let saltBase64 = await window.storage.get("enc-vault-salt");
    let salt: Uint8Array;
    if (!saltBase64) {
      salt = window.crypto.getRandomValues(new Uint8Array(16));
      await window.storage.set("enc-vault-salt", this.bufferToBase64(salt));
    } else {
      salt = this.base64ToBuffer(saltBase64);
    }
    
    // 2. Import raw passphrase as a base key
    const baseKey = await window.crypto.subtle.importKey(
      "raw",
      encoder.encode(passphrase),
      "PBKDF2",
      false,
      ["deriveKey"]
    );
    
    // 3. Derive high-entropy Master Key (MK)
    this.masterKey = await window.crypto.subtle.deriveKey(
      { 
        name: "PBKDF2", 
        salt: salt, 
        iterations: 100000, 
        hash: "SHA-256" 
      },
      baseKey,
      { name: "AES-GCM", length: 256 },
      false,
      ["encrypt", "decrypt"]
    );

    console.log("Vault Master Key established.");
    await this.initKek();
  }

  /**
   * Initializes or retrieves the KEK (wrapped by MK).
   */
  private static async initKek() {
    if (!this.masterKey) throw new Error("Vault locked: Master Key missing.");
    
    const wrappedKek = await window.storage.get("enc-kek-wrapped");
    
    if (wrappedKek) {
      // Recovery: Unwrap existing KEK with the newly derived MK
      this.kek = await this.unwrapKey(wrappedKek, this.masterKey, "KEK");
    } else {
      // First run: Generate KEK and wrap it with MK
      this.kek = await window.crypto.subtle.generateKey(
        { name: "AES-GCM", length: 256 },
        true,
        ["encrypt", "decrypt", "wrapKey", "unwrapKey"]
      );
      const wrapped = await this.wrapKey(this.kek, this.masterKey);
      await window.storage.set("enc-kek-wrapped", wrapped);
    }
  }

  /**
   * Encrypts data for a specific scope (memory, history, assets, etc.).
   */
  static async encrypt(scope: string, data: string): Promise<string> {
    const dek = await this.getOrCreateDek(scope);
    const iv = window.crypto.getRandomValues(new Uint8Array(12));
    const encoded = new TextEncoder().encode(data);
    
    const ciphertext = await window.crypto.subtle.encrypt(
      { name: "AES-GCM", iv },
      dek,
      encoded
    );

    return `${this.bufferToBase64(iv)}:${this.bufferToBase64(new Uint8Array(ciphertext))}`;
  }

  /**
   * Decrypts scoped data.
   */
  static async decrypt(scope: string, encryptedData: string): Promise<string> {
    const dek = await this.getOrCreateDek(scope);
    const [ivBase64, cipherBase64] = encryptedData.split(':');
    const iv = this.base64ToBuffer(ivBase64);
    const ciphertext = this.base64ToBuffer(cipherBase64);
    
    const decrypted = await window.crypto.subtle.decrypt(
      { name: "AES-GCM", iv },
      dek,
      ciphertext
    );

    return new TextDecoder().decode(decrypted);
  }

  private static async getOrCreateDek(scope: string): Promise<CryptoKey> {
    if (!this.kek) throw new Error("KEK not initialized. Did you unlock the vault?");
    if (this.deks.has(scope)) return this.deks.get(scope)!;

    const storageKey = `enc-dek-${scope}`;
    const wrappedDek = await window.storage.get(storageKey);
    
    let dek: CryptoKey;
    if (wrappedDek) {
      dek = await this.unwrapKey(wrappedDek, this.kek, `DEK_${scope}`);
    } else {
      dek = await window.crypto.subtle.generateKey(
        { name: "AES-GCM", length: 256 },
        true,
        ["encrypt", "decrypt"]
      );
      const wrapped = await this.wrapKey(dek, this.kek);
      await window.storage.set(storageKey, wrapped);
    }
    
    this.deks.set(scope, dek);
    return dek;
  }

  // --- Helper Methods ---

  private static async wrapKey(keyToWrap: CryptoKey, wrappingKey: CryptoKey): Promise<string> {
    const iv = window.crypto.getRandomValues(new Uint8Array(12));
    const rawExport = await window.crypto.subtle.exportKey("raw", keyToWrap);
    const wrapped = await window.crypto.subtle.encrypt(
      { name: "AES-GCM", iv },
      wrappingKey,
      rawExport
    );
    return `${this.bufferToBase64(iv)}:${this.bufferToBase64(new Uint8Array(wrapped))}`;
  }

  private static async unwrapKey(wrappedStr: string, wrappingKey: CryptoKey, purpose: string): Promise<CryptoKey> {
    const [ivBase64, cipherBase64] = wrappedStr.split(':');
    const iv = this.base64ToBuffer(ivBase64);
    const ciphertext = this.base64ToBuffer(cipherBase64);

    const rawKey = await window.crypto.subtle.decrypt(
      { name: "AES-GCM", iv },
      wrappingKey,
      ciphertext
    );

    return window.crypto.subtle.importKey(
      "raw",
      rawKey,
      { name: "AES-GCM" },
      true,
      purpose.startsWith("KEK") ? ["encrypt", "decrypt", "wrapKey", "unwrapKey"] : ["encrypt", "decrypt"]
    );
  }

  private static bufferToBase64(buf: Uint8Array): string {
    return btoa(String.fromCharCode(...buf));
  }

  private static base64ToBuffer(base64: string): Uint8Array {
    return new Uint8Array(atob(base64).split("").map(c => c.charCodeAt(0)));
  }
}
