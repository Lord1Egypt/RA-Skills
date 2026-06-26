"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.toString = toString;
exports.toNumber = toNumber;
exports.toHexValue = toHexValue;
const ethers_1 = require("ethers");
function toString(val) {
    if (val != null) {
        if (typeof (val) == 'number') {
            return ethers_1.BigNumber.from('0x' + val.toString(16)).toString();
        }
        return ethers_1.BigNumber.from(val).toString();
    }
    return '';
}
function toNumber(val) {
    return val != null ? Number(val.toString()) : undefined;
}
function toHexValue(value) {
    const hex = ethers_1.BigNumber.from(value).toHexString();
    if (hex.startsWith('0x0') && hex.length > 3) {
        return '0x' + hex.substring(3);
    }
    return hex;
}
//# sourceMappingURL=numberUtil.js.map