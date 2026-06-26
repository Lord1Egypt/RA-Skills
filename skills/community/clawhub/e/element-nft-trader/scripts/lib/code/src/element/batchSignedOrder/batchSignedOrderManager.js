"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.BatchSignedOrderManager = exports.maxBasicERC20Amount = exports.maxERC20Amount = exports.maxBasicNftId = void 0;
exports.getSucceedList = getSucceedList;
const Web3Signer_1 = require("../../signer/Web3Signer");
const contracts_1 = require("../../contracts/contracts");
const ethers_1 = require("ethers");
const types_1 = require("../../types/types");
const orderTypes_1 = require("../order/orderTypes");
const chainUtil_1 = require("../../util/chainUtil");
const tokenUtil_1 = require("../../util/tokenUtil");
const batchSignedTypedData_1 = require("./batchSignedTypedData");
const openApi_1 = require("../../api/openApi");
const numberUtil_1 = require("../../util/numberUtil");
exports.maxBasicNftId = ethers_1.BigNumber.from('0xffffffffffffffffffffffffffffffffffffffff');
exports.maxERC20Amount = ethers_1.BigNumber.from('0xffffffffffffffffffffffffffffffffffffffff');
exports.maxBasicERC20Amount = ethers_1.BigNumber.from('0xffffffffffffffffffffffff');
class BatchSignedOrderManager {
    constructor(web3Signer, apiOption) {
        this.web3Signer = web3Signer;
        this.apiOption = apiOption;
    }
    async createOrders(params, counter) {
        const fees = await this.queryFees(params);
        const platformFeeRecipient = getPlatformFeeRecipient(fees);
        const chain = (0, chainUtil_1.getChain)(this.web3Signer.chainId);
        const maker = await this.web3Signer.getCurrentAccount();
        const paymentToken = (0, tokenUtil_1.toStandardERC20Token)(params.paymentToken);
        const { listingTime, expirationTime } = getOrderTime(params);
        const elementEx = await this.getElementEx();
        const hashNonce = (counter != null) ? counter : await elementEx.getHashNonce(maker);
        const list = getOrders(params.items);
        const orders = [];
        let error;
        for (const order of list) {
            try {
                const nonce = await (0, openApi_1.queryNonce)({
                    maker: maker,
                    schema: types_1.AssetSchema.ERC721,
                    count: order.itemCount
                }, this.apiOption);
                const oracleSignature = await (0, openApi_1.queryOracleSignature)(this.apiOption);
                setCollectionFees(order.basicCollections, fees);
                setCollectionFees(order.collections, fees);
                orders.push({
                    exchange: elementEx.address.toLowerCase(),
                    maker: maker.toLowerCase(),
                    listingTime: listingTime,
                    expirationTime: expirationTime,
                    startNonce: nonce,
                    paymentToken: paymentToken,
                    platformFeeRecipient: platformFeeRecipient,
                    basicCollections: order.basicCollections,
                    collections: order.collections,
                    hashNonce: hashNonce.toString(),
                    oracleSignature,
                    chain: chain
                });
            }
            catch (e) {
                error = e;
            }
        }
        if (orders.length == 0) {
            throw error;
        }
        return orders;
    }
    async approveAndGetCounter(params) {
        checkSellOrdersParams(params);
        const set = new Set;
        for (const item of params.items) {
            set.add(item.erc721TokenAddress.toLowerCase());
        }
        const elementEx = await this.getElementEx();
        const helper = await this.getHelper();
        const list = [];
        for (const value of set.values()) {
            list.push({
                tokenType: 0,
                tokenAddress: value,
                operator: elementEx.address
            });
        }
        const owner = await this.web3Signer.getCurrentAccount();
        const r = await helper.getSDKApprovalsAndCounter(owner, list);
        for (let i = 0; i < list.length; i++) {
            if (r.approvals[i].eq(0)) {
                console.log('start approveERC721, ERC721Address =', list[i].tokenAddress);
                const tx = await this.web3Signer.approveERC721Proxy(owner, list[i].tokenAddress, elementEx.address, params);
                console.log('approveERC721, tx.hash', tx.hash);
                const receipt = await tx.wait(1);
                console.log('approveERC721, completed receipt', JSON.stringify(receipt));
                console.log('approveERC721, completed gasUsed =', (0, numberUtil_1.toString)(receipt.gasUsed));
            }
        }
        return parseInt(r.elementCounter);
    }
    async signOrder(order) {
        const typedData = (0, batchSignedTypedData_1.getTypedData)(order, this.web3Signer.chainId);
        const sign = await this.web3Signer.signTypedData(order.maker, typedData);
        const o = order;
        o.v = sign.v;
        o.r = sign.r;
        o.s = sign.s;
        o.hash = Web3Signer_1.Web3Signer.getOrderHash(typedData);
        // const r = await this.helper.checkBSERC721Orders(o)
        // console.log(JSON.stringify(r))
        // console.log(JSON.stringify(o))
        return o;
    }
    async getElementEx() {
        const signer = await this.web3Signer.getSigner();
        return (0, contracts_1.getElementExContract)(this.web3Signer.chainId, signer);
    }
    async getHelper() {
        const signer = await this.web3Signer.getSigner();
        return (0, contracts_1.getHelperContract)(this.web3Signer.chainId, signer);
    }
    async queryFees(params) {
        const addressList = [];
        for (const item of params.items) {
            const address = item.erc721TokenAddress.toLowerCase();
            if (!addressList.includes(address)) {
                addressList.push(address);
            }
        }
        const fees = await (0, openApi_1.queryFees)(addressList, this.apiOption);
        const map = new Map();
        for (const fee of fees) {
            map.set(fee.contractAddress.toLowerCase(), fee);
        }
        return map;
    }
}
exports.BatchSignedOrderManager = BatchSignedOrderManager;
function getSucceedList(order, assets) {
    if (assets.length == 0) {
        return [];
    }
    const map = new Map;
    let nonce = Number(order.startNonce);
    for (const collection of order.basicCollections) {
        for (const item of collection.items) {
            const key = (collection.nftAddress + ',' + item.nftId).toLowerCase();
            const value = {
                erc20TokenAmount: item.erc20TokenAmount,
                nonce: nonce++
            };
            map.set(key, value);
        }
    }
    for (const collection of order.collections) {
        for (const item of collection.items) {
            const key = (collection.nftAddress + ',' + item.nftId).toLowerCase();
            const value = {
                erc20TokenAmount: item.erc20TokenAmount,
                nonce: nonce++
            };
            map.set(key, value);
        }
    }
    const list = [];
    for (const asset of assets) {
        const assetContract = asset.assetContract?.toString().toLowerCase() || '';
        const tokenId = (0, numberUtil_1.toString)(asset.assetTokenId);
        const key = assetContract + ',' + tokenId;
        const value = map.get(key);
        if (value) {
            list.push({
                contractAddress: assetContract,
                tokenId: tokenId,
                schema: types_1.AssetSchema.ERC721,
                standard: types_1.Standard.ElementEx,
                maker: order.maker,
                listingTime: order.listingTime,
                expirationTime: order.expirationTime,
                price: Number(ethers_1.ethers.utils.formatEther(value.erc20TokenAmount)),
                paymentToken: order.paymentToken,
                saleKind: types_1.SaleKind.BatchSignedERC721Order,
                side: types_1.OrderSide.SellOrder,
                orderId: asset.orderId
            });
        }
    }
    return list;
}
function checkSellOrdersParams(params) {
    if (!params.items?.length) {
        throw Error(`makeERC721SellOrders failed, items.length error.`);
    }
    const set = new Set();
    for (const item of params.items) {
        const key = item.erc721TokenAddress.toLowerCase() + ',' + (0, numberUtil_1.toString)(item.erc721TokenId);
        if (set.has(key)) {
            throw Error(`makeERC721SellOrders failed, the same asset is not supported, assetAddress(${item.erc721TokenAddress}, assetId(${item.erc721TokenId})).`);
        }
        set.add(key);
    }
}
function setCollectionFees(collections, fees) {
    for (const collection of collections) {
        const fee = fees.get(collection.nftAddress);
        if (fee) {
            if (fee.protocolFeeAddress && fee.protocolFeeAddress.toLowerCase() != types_1.NULL_ADDRESS) {
                collection.platformFee = fee.protocolFeePoints || 0;
            }
            if (fee.royaltyFeeAddress && fee.royaltyFeeAddress.toLowerCase() != types_1.NULL_ADDRESS) {
                collection.royaltyFee = fee.royaltyFeePoints || 0;
                collection.royaltyFeeRecipient = fee.royaltyFeeAddress.toLowerCase();
            }
        }
        if (collection.platformFee < 0 || collection.royaltyFee < 0 || (collection.platformFee + collection.royaltyFee) > 10000) {
            throw Error(`makeERC721SellOrders failed, feePoint error, platformFeePoint(${collection.platformFee}, royaltyFeePoint(${collection.royaltyFee})`);
        }
    }
}
function getPlatformFeeRecipient(fees) {
    let platformFeeRecipient;
    for (const fee of fees.values()) {
        if (fee.protocolFeePoints) {
            const protocolFeeAddress = fee.protocolFeeAddress ? fee.protocolFeeAddress.toLowerCase() : types_1.NULL_ADDRESS;
            if (platformFeeRecipient) {
                if (platformFeeRecipient != protocolFeeAddress) {
                    throw Error(`check platformFeeRecipient failed, platformFeeRecipient1(${platformFeeRecipient}), platformFeeRecipient2(${protocolFeeAddress})`);
                }
            }
            else {
                platformFeeRecipient = protocolFeeAddress;
            }
        }
    }
    return platformFeeRecipient ? platformFeeRecipient : types_1.NULL_ADDRESS;
}
function getOrders(items) {
    const map = new Map;
    for (const item of items) {
        if (!item.erc721TokenAddress || item.erc721TokenAddress.toLowerCase() == types_1.NULL_ADDRESS) {
            throw Error(`makeERC721SellOrders failed, tokenAddress(${item.erc721TokenAddress}) error.`);
        }
        if (item.erc721TokenId == null || item.erc721TokenId === '') {
            throw Error(`makeERC721SellOrders failed, tokenId(${item.erc721TokenId}) error.`);
        }
        let collection = map.get(item.erc721TokenAddress.toLowerCase());
        if (collection == null) {
            collection = {
                nftAddress: item.erc721TokenAddress.toLowerCase(),
                items: [],
                isBasic: true
            };
            map.set(collection.nftAddress, collection);
        }
        const obj = {
            erc20TokenAmount: (0, numberUtil_1.toString)(item.paymentTokenAmount),
            nftId: (0, numberUtil_1.toString)(item.erc721TokenId)
        };
        collection.items.push(obj);
        if (collection.isBasic) {
            if (exports.maxBasicERC20Amount.lt(obj.erc20TokenAmount) || exports.maxBasicNftId.lt(obj.nftId)) {
                collection.isBasic = false;
            }
        }
        if (exports.maxERC20Amount.lt(obj.erc20TokenAmount)) {
            throw Error(`makeERC721SellOrders failed, item.paymentTokenAmount(${obj.erc20TokenAmount} exceed the maxValue(${exports.maxERC20Amount.toHexString()})).`);
        }
    }
    let point = 0;
    let order = null;
    const orders = [];
    for (const value of map.values()) {
        if (isOrderFulled(point, 2, order)) {
            point = 0;
            order = null;
        }
        point += 2;
        let collection;
        const plusPoint = value.isBasic ? 1 : 2;
        for (const item of value.items) {
            if (isOrderFulled(point, plusPoint, order)) {
                point = 2;
                order = null;
                collection = null;
            }
            if (order == null) {
                order = {
                    basicCollections: [],
                    collections: [],
                    itemCount: 0
                };
                orders.push(order);
            }
            if (collection == null) {
                collection = {
                    nftAddress: value.nftAddress,
                    platformFee: 0,
                    royaltyFeeRecipient: types_1.NULL_ADDRESS,
                    royaltyFee: 0,
                    items: []
                };
                if (value.isBasic) {
                    order.basicCollections.push(collection);
                }
                else {
                    order.collections.push(collection);
                }
            }
            point += plusPoint;
            order.itemCount++;
            collection.items.push(item);
        }
    }
    return orders;
}
function isOrderFulled(point, plusPoint, order) {
    if (point + plusPoint > 102) {
        return true;
    }
    return order != null && order.itemCount >= 50;
}
function getOrderTime(params) {
    const now = Math.floor(Date.now() / 1000);
    let listingTime;
    if (params.listingTime) {
        listingTime = params.listingTime;
        if (listingTime > now + orderTypes_1.MAX_LISTING_TIME) {
            throw Error('makeERC721SellOrders failed, require listingTime <= now + 1 year.');
        }
        if (listingTime < (now - 1800)) {
            throw Error('makeERC721SellOrders failed, listingTime >= now - 30 minute.');
        }
    }
    else {
        listingTime = now - 60;
    }
    let expirationTime;
    if (params.expirationTime != null) {
        expirationTime = params.expirationTime;
        if (expirationTime < Math.max(listingTime, now)) {
            throw Error('makeERC721SellOrders failed, require expirationTime >= Math.max(listingTime, now).');
        }
        if (expirationTime > Math.max(listingTime, now) + orderTypes_1.MAX_EXPIRATION_TIME) {
            throw Error('makeERC721SellOrders failed, require expirationTime <= Math.max(listingTime, now) + 1 year.');
        }
    }
    else {
        expirationTime = Math.max(listingTime, now) + orderTypes_1.DEFAULT_EXPIRATION_TIME;
    }
    return { listingTime, expirationTime };
}
//# sourceMappingURL=batchSignedOrderManager.js.map