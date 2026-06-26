"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AssetSchema = exports.Market = exports.Standard = exports.SaleKind = exports.OrderSide = exports.Network = exports.ETH_TOKEN_ADDRESS = exports.NULL_ADDRESS = void 0;
exports.NULL_ADDRESS = '0x0000000000000000000000000000000000000000';
exports.ETH_TOKEN_ADDRESS = '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee';
var Network;
(function (Network) {
    Network["ETH"] = "eth";
    Network["BSC"] = "bsc";
    Network["Polygon"] = "polygon";
    Network["Avalanche"] = "avalanche";
    Network["Arbitrum"] = "arbitrum";
    Network["ZkSync"] = "zksync";
    Network["Linea"] = "linea";
    Network["Base"] = "base";
    Network["OpBNB"] = "opbnb";
    Network["Scroll"] = "scroll";
    Network["MantaPacific"] = "manta_pacific";
    Network["Optimism"] = "optimism";
    Network["Mantle"] = "mantle";
    Network["ZKFair"] = "zkfair";
    Network["Blast"] = "blast";
    Network["Merlin"] = "merlin";
    Network["Mode"] = "mode";
    Network["Cyber"] = "cyber";
    Network["BOB"] = "bob";
    Network["Lightlink"] = "lightlink";
    Network["Nanon"] = "nanon";
    Network["Bera"] = "bera";
    Network["Zeta"] = "zeta";
    Network["Nibiru"] = "nibiru";
    Network["Abstract"] = "abstract";
    Network["Monad"] = "monad";
    Network["Bitlayer"] = "bitlayer";
    Network["Mantra"] = "mantra";
})(Network || (exports.Network = Network = {}));
var OrderSide;
(function (OrderSide) {
    OrderSide[OrderSide["BuyOrder"] = 0] = "BuyOrder";
    OrderSide[OrderSide["SellOrder"] = 1] = "SellOrder";
})(OrderSide || (exports.OrderSide = OrderSide = {}));
var SaleKind;
(function (SaleKind) {
    SaleKind[SaleKind["FixedPrice"] = 0] = "FixedPrice";
    SaleKind[SaleKind["BatchSignedERC721Order"] = 3] = "BatchSignedERC721Order";
    SaleKind[SaleKind["ContractOffer"] = 7] = "ContractOffer";
    SaleKind[SaleKind["BatchOfferERC721s"] = 8] = "BatchOfferERC721s";
})(SaleKind || (exports.SaleKind = SaleKind = {}));
var Standard;
(function (Standard) {
    Standard["ElementEx"] = "element-ex-v3";
})(Standard || (exports.Standard = Standard = {}));
var Market;
(function (Market) {
    Market["ElementEx"] = "element";
})(Market || (exports.Market = Market = {}));
var AssetSchema;
(function (AssetSchema) {
    AssetSchema["ERC721"] = "ERC721";
    AssetSchema["ERC1155"] = "ERC1155";
})(AssetSchema || (exports.AssetSchema = AssetSchema = {}));
//# sourceMappingURL=types.js.map