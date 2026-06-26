/**
 * NL2SQL AES-256 Encryption Tool
 * Algorithm: AES-256-CBC + HMAC-SHA256 (Encrypt-then-MAC)
 * 
 * 与 Java 端Nl2SqlServiceImpl中的加解密逻辑保持一致
 * Java使用AES/CBC/PKCS5Padding + HMACSHA256
 */

const crypto = require('crypto');

// ============================================================
// 配置（必须与 Java 端保持一致）
// ============================================================

// AES-256 key: 32字节，用UTF-8编码
const AES_KEY_STRING = 'WisdomACM2026NL2SQLSecretKey32B!';
const AES_KEY = Buffer.from(AES_KEY_STRING, 'utf8'); // 32 bytes

// HMAC key: 16 bytes（与AES key相同，简化处理，生产环境应分离）
const HMAC_KEY = AES_KEY;

// AES/CBC/PKCS5Padding constants
const IV_LENGTH = 16; // 16 bytes for AES-256-CBC
const BLOCK_SIZE = 16; // AES block size

// ============================================================
// 加密函数
// ============================================================

function encrypt(plaintext) {
    // 1. Generate random IV
    const iv = crypto.randomBytes(IV_LENGTH);
    
    // 2. AES-256-CBC encryption with PKCS5/PKCS7 padding
    const cipher = crypto.createCipheriv('aes-256-cbc', AES_KEY, iv);
    const encrypted = Buffer.concat([
        cipher.update(plaintext, 'utf8'),
        cipher.final()
    ]);
    
    // 3. HMAC-SHA256 for authentication (Encrypt-then-MAC)
    // MAC = HMAC-SHA256(HMAC_KEY, iv || encrypted_data)
    const hmac = crypto.createHmac('sha256', HMAC_KEY);
    hmac.update(Buffer.concat([iv, encrypted]));
    const authTag = hmac.digest(); // 32 bytes
    
    // 4. Output: base64(iv || encrypted || authTag)
    const combined = Buffer.concat([iv, encrypted, authTag]);
    return {
        ciphertext: combined.toString('base64'),
        iv: iv.toString('base64'),
        algorithm: 'AES-256-CBC-HMAC-SHA256'
    };
}

// ============================================================
// 解密函数
// ============================================================

function decrypt(encryptedData, ivBase64) {
    // 1. Decode IV
    const iv = Buffer.from(ivBase64, 'base64');
    
    // 2. Decode combined ciphertext
    const combined = Buffer.from(encryptedData, 'base64');
    
    // 3. Extract: iv (16) + encrypted (len-48) + authTag (32)
    const authTagLen = 32;
    const encryptedLen = combined.length - IV_LENGTH - authTagLen;
    
    if (encryptedLen < 0) {
        throw new Error('Ciphertext too short: missing encrypted data or auth tag');
    }
    
    const encrypted = combined.slice(IV_LENGTH, IV_LENGTH + encryptedLen);
    const authTag = combined.slice(IV_LENGTH + encryptedLen);
    
    // 4. Verify HMAC
    const hmac = crypto.createHmac('sha256', HMAC_KEY);
    hmac.update(Buffer.concat([iv, encrypted]));
    const expectedAuthTag = hmac.digest();
    
    // Constant-time comparison to prevent timing attacks
    if (!crypto.timingSafeEqual(authTag, expectedAuthTag)) {
        throw new Error('HMAC verification failed: data has been tampered with');
    }
    
    // 5. AES-256-CBC decryption
    const decipher = crypto.createDecipheriv('aes-256-cbc', AES_KEY, iv);
    const decrypted = Buffer.concat([
        decipher.update(encrypted),
        decipher.final()
    ]);
    
    return decrypted.toString('utf8');
}

// ============================================================
// CLI 接口
// ============================================================

if (require.main === module) {
    const [,, command, ...args] = process.argv;
    
    if (command === 'encrypt') {
        const plaintext = args.join(' ');
        const result = encrypt(plaintext);
        console.log(JSON.stringify(result, null, 2));
    } else if (command === 'decrypt') {
        // decrypt <ciphertext> <iv>
        const [ciphertext, iv] = args;
        const result = decrypt(ciphertext, iv);
        console.log('Decrypted:', result);
    } else {
        // Interactive test
        const testSql = 'SELECT * FROM wsd_plan_task WHERE DEL = 0 LIMIT 10';
        console.log('Testing with:', testSql);
        
        const encrypted = encrypt(testSql);
        console.log('\nEncrypted:', JSON.stringify(encrypted, null, 2));
        
        const decrypted = decrypt(encrypted.ciphertext, encrypted.iv);
        console.log('\nDecrypted:', decrypted);
        
        if (testSql === decrypted) {
            console.log('\n✅ Encrypt/Decrypt test PASSED');
        } else {
            console.log('\n❌ Encrypt/Decrypt test FAILED');
            process.exit(1);
        }
    }
}

module.exports = { encrypt, decrypt };
