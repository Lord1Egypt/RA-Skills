"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.toContractERC20Token = toContractERC20Token;
exports.toStandardERC20Token = toStandardERC20Token;
const types_1 = require("../types/types");
function toContractERC20Token(erc20Token) {
    if (erc20Token && erc20Token.toLowerCase() != types_1.NULL_ADDRESS) {
        return erc20Token.toLowerCase();
    }
    return types_1.ETH_TOKEN_ADDRESS;
}
function toStandardERC20Token(erc20Token) {
    if (erc20Token && erc20Token.toLowerCase() != types_1.ETH_TOKEN_ADDRESS) {
        return erc20Token.toLowerCase();
    }
    return types_1.NULL_ADDRESS;
}
//# sourceMappingURL=tokenUtil.js.map