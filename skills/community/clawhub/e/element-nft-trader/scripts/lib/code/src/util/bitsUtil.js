"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.encodeBits = encodeBits;
const ethers_1 = require("ethers");
function encodeBits(args) {
    let data = '0x';
    for (const arg of args) {
        data += toHexBytes(ethers_1.BigNumber.from(arg[0].toString()).toHexString(), arg[1]);
    }
    return data;
}
function toHexBytes(hexStr, bitCount) {
    const count = bitCount / 4;
    const str = hexStr.toLowerCase().startsWith('0x') ? hexStr.substring(2).toLowerCase() : hexStr.toLowerCase();
    if (str.length > count) {
        return str.substring(str.length - count);
    }
    let zero = '';
    for (let i = str.length; i < count; i++) {
        zero += '0';
    }
    return zero + str;
}
//# sourceMappingURL=bitsUtil.js.map