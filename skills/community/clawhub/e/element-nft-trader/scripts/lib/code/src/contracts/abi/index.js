"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ContractABI = void 0;
const ERC20_json_1 = __importDefault(require("./common/ERC20.json"));
const ERC721_json_1 = __importDefault(require("./common/ERC721.json"));
const ERC1155_json_1 = __importDefault(require("./common/ERC1155.json"));
const WETH_json_1 = __importDefault(require("./common/WETH.json"));
const IElementEx_json_1 = __importDefault(require("./elementEx/IElementEx.json"));
const IElementExSwapV2_json_1 = __importDefault(require("./elementEx/IElementExSwapV2.json"));
const IAggTraderHelper_json_1 = __importDefault(require("./elementEx/IAggTraderHelper.json"));
exports.ContractABI = {
    weth: WETH_json_1.default,
    erc20: ERC20_json_1.default,
    erc721: ERC721_json_1.default,
    erc1155: ERC1155_json_1.default,
    elementEx: IElementEx_json_1.default,
    elementExSwap: IElementExSwapV2_json_1.default,
    helper: IAggTraderHelper_json_1.default,
};
//# sourceMappingURL=index.js.map