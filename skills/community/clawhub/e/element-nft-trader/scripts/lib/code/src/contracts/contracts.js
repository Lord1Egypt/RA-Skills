"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ContractABI = void 0;
exports.getElementExContract = getElementExContract;
exports.getHelperContract = getHelperContract;
const config_1 = require("./config");
const ethers_1 = require("ethers");
var index_1 = require("./abi/index");
Object.defineProperty(exports, "ContractABI", { enumerable: true, get: function () { return index_1.ContractABI; } });
function getElementExContract(chainId, signer) {
    const address = config_1.CONTRACTS_ADDRESSES[chainId].ElementEx;
    return new ethers_1.Contract(address, config_1.ContractABI.elementEx.abi, signer);
}
// export function getElementExSwapContract(chainId: number, signer: Signer): Contract {
//   const address = CONTRACTS_ADDRESSES[chainId as keyof typeof CONTRACTS_ADDRESSES].ElementExSwapV2
//   return new Contract(address, ContractABI.elementExSwap.abi, signer)
// }
function getHelperContract(chainId, signer) {
    const address = config_1.CONTRACTS_ADDRESSES[chainId].Helper;
    return new ethers_1.Contract(address, config_1.ContractABI.helper.abi, signer);
}
//# sourceMappingURL=contracts.js.map