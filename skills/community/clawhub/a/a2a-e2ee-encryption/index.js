/**
 * A2A End-to-End Encryption (E2EE)
 * 
 * Provides encryption utilities for secure agent-to-agent communication
 * using RSA asymmetric encryption with AES symmetric hybrid for large messages.
 */

const crypto = require('crypto');

// Configuration
const RSA_KEY_SIZE = 2048;
const AES_KEY_SIZE = 256;
const AES_IV_SIZE = 16;
const HASH_ALGORITHM = 'sha256';

/**
 * Generate an RSA key pair for asymmetric encryption
 * @param {number} keySize - RSA key size in bits (default: 2048)
 * @returns {Object} Key pair with publicKey and privateKey
 */
function generateKeyPair(keySize = RSA_KEY_SIZE) {
  const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: keySize,
    publicKeyEncoding: {
      type: 'spki',
      format: 'pem'
    },
    privateKeyEncoding: {
      type: 'pkcs8',
      format: 'pem'
    }
  });
  
  return { publicKey, privateKey };
}

/**
 * Export a key to a portable format (base64)
 * @param {string} key - PEM formatted key
 * @returns {string} Base64 encoded key
 */
function exportKey(key) {
  return Buffer.from(key).toString('base64');
}

/**
 * Import a key from portable format
 * @param {string} exportedKey - Base64 encoded key
 * @returns {string} PEM formatted key
 */
function importKey(exportedKey) {
  return Buffer.from(exportedKey, 'base64').toString('utf-8');
}

/**
 * Get key fingerprint for verification
 * @param {string} key - PEM formatted public key
 * @returns {string} SHA-256 fingerprint
 */
function getKeyFingerprint(key) {
  return crypto.createHash(HASH_ALGORITHM).update(key).digest('hex');
}

/**
 * Encrypt a message using recipient's public key
 * For small messages: RSA direct encryption
 * For large messages: Hybrid RSA+AES encryption
 * 
 * @param {string|Buffer} message - Message to encrypt
 * @param {string} recipientPublicKey - Recipient's public key (PEM)
 * @returns {Object} Encrypted message with metadata
 */
function encrypt(message, recipientPublicKey) {
  const messageBuffer = Buffer.isBuffer(message) ? message : Buffer.from(message, 'utf-8');
  
  // Check message size - RSA can only encrypt messages smaller than key size
  const maxDirectSize = (RSA_KEY_SIZE / 8) - 42; // PKCS#1 v1.5 padding overhead
  
  if (messageBuffer.length <= maxDirectSize) {
    // Direct RSA encryption for small messages
    const encrypted = crypto.publicEncrypt(
      {
        key: recipientPublicKey,
        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
        oaepHash: HASH_ALGORITHM
      },
      messageBuffer
    );
    
    return {
      type: 'direct',
      encrypted: encrypted.toString('base64'),
      algorithm: 'RSA-OAEP'
    };
  } else {
    // Hybrid encryption for large messages
    // Generate random AES key and IV
    const aesKey = crypto.randomBytes(AES_KEY_SIZE / 8);
    const iv = crypto.randomBytes(AES_IV_SIZE);
    
    // Encrypt message with AES
    const cipher = crypto.createCipheriv(`aes-${AES_KEY_SIZE}-gcm`, aesKey, iv);
    const encryptedMessage = Buffer.concat([
      cipher.update(messageBuffer),
      cipher.final()
    ]);
    const authTag = cipher.getAuthTag();
    
    // Encrypt AES key with RSA
    const encryptedKey = crypto.publicEncrypt(
      {
        key: recipientPublicKey,
        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
        oaepHash: HASH_ALGORITHM
      },
      aesKey
    );
    
    return {
      type: 'hybrid',
      encryptedKey: encryptedKey.toString('base64'),
      iv: iv.toString('base64'),
      encrypted: encryptedMessage.toString('base64'),
      authTag: authTag.toString('base64'),
      algorithm: 'RSA-OAEP+AES-256-GCM'
    };
  }
}

/**
 * Decrypt a message using own private key
 * @param {Object} encryptedData - Encrypted message object from encrypt()
 * @param {string} privateKey - Own private key (PEM)
 * @returns {string} Decrypted message
 */
function decrypt(encryptedData, privateKey) {
  if (encryptedData.type === 'direct') {
    // Direct RSA decryption
    const decrypted = crypto.privateDecrypt(
      {
        key: privateKey,
        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
        oaepHash: HASH_ALGORITHM
      },
      Buffer.from(encryptedData.encrypted, 'base64')
    );
    
    return decrypted.toString('utf-8');
  } else if (encryptedData.type === 'hybrid') {
    // Hybrid RSA+AES decryption
    
    // Decrypt AES key with RSA
    const aesKey = crypto.privateDecrypt(
      {
        key: privateKey,
        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
        oaepHash: HASH_ALGORITHM
      },
      Buffer.from(encryptedData.encryptedKey, 'base64')
    );
    
    // Decrypt message with AES
    const decipher = crypto.createDecipheriv(
      `aes-${AES_KEY_SIZE}-gcm`,
      aesKey,
      Buffer.from(encryptedData.iv, 'base64')
    );
    decipher.setAuthTag(Buffer.from(encryptedData.authTag, 'base64'));
    
    const decrypted = Buffer.concat([
      decipher.update(Buffer.from(encryptedData.encrypted, 'base64')),
      decipher.final()
    ]);
    
    return decrypted.toString('utf-8');
  } else {
    throw new Error(`Unknown encryption type: ${encryptedData.type}`);
  }
}

/**
 * Sign a message with private key
 * @param {string} message - Message to sign
 * @param {string} privateKey - Private key (PEM)
 * @returns {string} Signature in base64
 */
function sign(message, privateKey) {
  const sign = crypto.createSign(HASH_ALGORITHM);
  sign.update(message);
  sign.end();
  return sign.sign(privateKey, 'base64');
}

/**
 * Verify a signature with public key
 * @param {string} message - Original message
 * @param {string} signature - Signature in base64
 * @param {string} publicKey - Public key (PEM)
 * @returns {boolean} Whether signature is valid
 */
function verify(message, signature, publicKey) {
  const verifier = crypto.createVerify(HASH_ALGORITHM);
  verifier.update(message);
  verifier.end();
  return verifier.verify(publicKey, signature, 'base64');
}

/**
 * Compute HMAC for message integrity
 * @param {string} message - Message to authenticate
 * @param {string} key - Shared secret key
 * @returns {string} HMAC in hex
 */
function computeHMAC(message, key) {
  return crypto.createHmac(HASH_ALGORITHM, key).update(message).digest('hex');
}

/**
 * Verify HMAC
 * @param {string} message - Message to verify
 * @param {string} hmac - Expected HMAC
 * @param {string} key - Shared secret key
 * @returns {boolean} Whether HMAC is valid
 */
function verifyHMAC(message, hmac, key) {
  const computed = computeHMAC(message, key);
  return crypto.timingSafeEqual(Buffer.from(hmac), Buffer.from(computed));
}

/**
 * Generate a shared secret for symmetric encryption
 * @param {number} length - Secret length in bytes (default: 32)
 * @returns {string} Secret in base64
 */
function generateSharedSecret(length = 32) {
  return crypto.randomBytes(length).toString('base64');
}

/**
 * Encrypt with shared secret (symmetric)
 * @param {string} message - Message to encrypt
 * @param {string} secret - Shared secret (base64)
 * @returns {Object} Encrypted data with IV
 */
function encryptSymmetric(message, secret) {
  const key = crypto.createHash(HASH_ALGORITHM).update(secret).digest();
  const iv = crypto.randomBytes(AES_IV_SIZE);
  
  const cipher = crypto.createCipheriv(`aes-${AES_KEY_SIZE}-gcm`, key, iv);
  const encrypted = Buffer.concat([
    cipher.update(message, 'utf-8'),
    cipher.final()
  ]);
  const authTag = cipher.getAuthTag();
  
  return {
    iv: iv.toString('base64'),
    encrypted: encrypted.toString('base64'),
    authTag: authTag.toString('base64')
  };
}

/**
 * Decrypt with shared secret (symmetric)
 * @param {Object} data - Encrypted data from encryptSymmetric()
 * @param {string} secret - Shared secret (base64)
 * @returns {string} Decrypted message
 */
function decryptSymmetric(data, secret) {
  const key = crypto.createHash(HASH_ALGORITHM).update(secret).digest();
  
  const decipher = crypto.createDecipheriv(
    `aes-${AES_KEY_SIZE}-gcm`,
    key,
    Buffer.from(data.iv, 'base64')
  );
  decipher.setAuthTag(Buffer.from(data.authTag, 'base64'));
  
  const decrypted = Buffer.concat([
    decipher.update(Buffer.from(data.encrypted, 'base64')),
    decipher.final()
  ]);
  
  return decrypted.toString('utf-8');
}

/**
 * Create a secure message envelope for A2A communication
 * @param {string} message - Message content
 * @param {string} recipientPublicKey - Recipient's public key
 * @param {string} senderPrivateKey - Sender's private key (for signing)
 * @returns {Object} Secure envelope
 */
function createSecureEnvelope(message, recipientPublicKey, senderPrivateKey) {
  const encrypted = encrypt(message, recipientPublicKey);
  const signature = sign(JSON.stringify(encrypted), senderPrivateKey);
  
  return {
    version: '1.0',
    encrypted,
    signature,
    timestamp: Date.now()
  };
}

/**
 * Open a secure message envelope
 * @param {Object} envelope - Secure envelope
 * @param {string} recipientPrivateKey - Recipient's private key
 * @param {string} senderPublicKey - Sender's public key (for verification)
 * @returns {Object} Decrypted message and verification status
 */
function openSecureEnvelope(envelope, recipientPrivateKey, senderPublicKey) {
  // Verify signature
  const signatureValid = verify(
    JSON.stringify(envelope.encrypted),
    envelope.signature,
    senderPublicKey
  );
  
  if (!signatureValid) {
    throw new Error('Invalid signature - message may have been tampered');
  }
  
  // Decrypt message
  const message = decrypt(envelope.encrypted, recipientPrivateKey);
  
  return {
    message,
    signatureValid,
    timestamp: envelope.timestamp
  };
}

module.exports = {
  // Key management
  generateKeyPair,
  exportKey,
  importKey,
  getKeyFingerprint,
  generateSharedSecret,
  
  // Asymmetric encryption
  encrypt,
  decrypt,
  
  // Signing
  sign,
  verify,
  
  // Symmetric encryption
  encryptSymmetric,
  decryptSymmetric,
  
  // Message integrity
  computeHMAC,
  verifyHMAC,
  
  // A2A envelope
  createSecureEnvelope,
  openSecureEnvelope
};
