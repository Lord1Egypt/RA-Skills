/**
 * passwordEncrypt.js — 登录密码加密
 *
 * 职责：对登录密码做 AES-128-CBC 加密（与后端登录接口兼容）
 */
const CryptoJS = require('crypto-js');

/**
 * ACM 前端 AES-128-CBC 加密（与后端登录接口兼容）
 * @param {string} password - 明文密码
 * @returns {string} 加密后的密码
 */
function aesEncrypt(password) {
    const key = CryptoJS.enc.Utf8.parse("ABCDEFGHIJKL_KEY");
    const iv = CryptoJS.enc.Utf8.parse("ABCDEFGHUJKLM_IV");
    const encrypted = CryptoJS.AES.encrypt(
        CryptoJS.enc.Utf8.parse(password),
        key,
        { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 }
    );
    return String(encrypted).trim();
}

module.exports = {
    aesEncrypt
};
