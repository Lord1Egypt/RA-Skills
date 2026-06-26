"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.estimateGas = estimateGas;
const axios_1 = __importDefault(require("axios"));
async function estimateGas(chainId) {
    if (chainId == 137) {
        return estimateGasPolygon();
    }
}
async function estimateGasPolygon() {
    try {
        const response = await (0, axios_1.default)({
            method: "get",
            url: "https://gasstation.polygon.technology/v2",
            timeout: 5000,
        });
        const obj = await response.data;
        const fastMaxPriorityFee = Number.parseFloat(obj.fast.maxPriorityFee);
        const baseFee = Number.parseFloat(obj.estimatedBaseFee);
        let maxPriorityFee = Math.floor(fastMaxPriorityFee * 1e9);
        let estimatedBaseFee;
        if (baseFee >= 10) {
            estimatedBaseFee = Math.floor(baseFee * 1.125 * 1e9);
        }
        else if (baseFee >= 5) {
            estimatedBaseFee = Math.floor(baseFee * 1.5 * 1e9);
        }
        else {
            estimatedBaseFee = Math.floor(baseFee * 2 * 1e9);
        }
        return {
            maxFeePerGas: maxPriorityFee + estimatedBaseFee,
            maxPriorityFeePerGas: maxPriorityFee,
        };
    }
    catch (e) { }
}
//# sourceMappingURL=gasUtil.js.map