"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ElementSDK = void 0;
const chainUtil_1 = require("./util/chainUtil");
const openApi_1 = require("./api/openApi");
const types_1 = require("./types/types");
const Web3Signer_1 = require("./signer/Web3Signer");
const batchSignedOrderManager_1 = require("./element/batchSignedOrder/batchSignedOrderManager");
const orderManager_1 = require("./element/order/orderManager");
const orderConverter_1 = require("./element/order/orderConverter");
const numberUtil_1 = require("./util/numberUtil");
const receiptUtil_1 = require("./util/receiptUtil");
const assetUtil_1 = require("./util/assetUtil");
const ethers_1 = require("ethers");
const tokenUtil_1 = require("./util/tokenUtil");
class ElementSDK {
    constructor(config) {
        this.isTestnet = false;
        if (config.isTestnet != null) {
            this.isTestnet = config.isTestnet;
        }
        this.chainId = (0, chainUtil_1.getChainId)(config.networkName, this.isTestnet);
        this.apiOption = {
            chain: config.networkName,
            isTestnet: this.isTestnet,
            apiKey: config.apiKey,
        };
        this.web3Signer = new Web3Signer_1.Web3Signer(config.signer, this.chainId);
        this.batchOrderManager = new batchSignedOrderManager_1.BatchSignedOrderManager(this.web3Signer, this.apiOption);
        this.orderManager = new orderManager_1.OrderManager(this.web3Signer);
    }
    async makeERC721SellOrders(params) {
        let error;
        const succeedList = [];
        const failedList = [];
        // 1. setApproveForAll
        const counter = await this.batchOrderManager.approveAndGetCounter(params);
        // 2. create orders
        const orders = await this.batchOrderManager.createOrders(params, counter);
        for (const order of orders) {
            try {
                // 3. sign order
                const signedOrder = await this.batchOrderManager.signOrder(order);
                // 4. post order
                const r = await (0, openApi_1.postBatchSignedERC721SellOrder)(signedOrder, this.apiOption);
                succeedList.push(...(0, batchSignedOrderManager_1.getSucceedList)(signedOrder, r.successList));
                failedList.push(...r.failList);
            }
            catch (e) {
                error = e;
            }
        }
        if (succeedList.length == 0 && failedList.length == 0) {
            throw error;
        }
        return {
            succeedList: succeedList,
            failedList: failedList,
        };
    }
    async makeSellOrder(params) {
        if (params.assetId == null) {
            throw Error("createSellOrder failed, asset.id is undefined.");
        }
        if ((!params.assetSchema || params.assetSchema.toLowerCase() == "erc721") &&
            (!params.takerAddress ||
                params.takerAddress.toLowerCase() == types_1.NULL_ADDRESS)) {
            const r = await this.makeERC721SellOrders({
                listingTime: params.listingTime,
                expirationTime: params.expirationTime,
                paymentToken: params.paymentToken,
                items: [
                    {
                        erc721TokenId: (0, numberUtil_1.toString)(params.assetId),
                        erc721TokenAddress: params.assetAddress,
                        paymentTokenAmount: (0, numberUtil_1.toString)(params.paymentTokenAmount),
                    },
                ],
                gasPrice: params.gasPrice,
                maxFeePerGas: params.maxFeePerGas,
                maxPriorityFeePerGas: params.maxPriorityFeePerGas,
            });
            if (!r.succeedList?.length) {
                const e = r.failedList?.length ? r.failedList[0].errorDetail : "";
                throw Error("createSellOrder failed, " + e);
            }
            return r.succeedList[0];
        }
        return await this.makeOrder(params, false);
    }
    async makeBuyOrder(params) {
        return await this.makeOrder(params, true);
    }
    async fillOrder(params) {
        if (params.order.standard?.toString().toLowerCase() != types_1.Standard.ElementEx) {
            throw Error(`fillOrder failed, standard(${params.order.standard}) is not supported`);
        }
        const account = await this.web3Signer.getCurrentAccount();
        const takeCount = params.quantity ? Number(params.quantity) || 1 : 1;
        if (params.order.side === types_1.OrderSide.SellOrder ||
            params.order.side == "sell") {
            if ((0, tokenUtil_1.toStandardERC20Token)(params.order.paymentToken) !== types_1.NULL_ADDRESS) {
                const providedDecimals = Number(params.order.paymentTokenDecimals);
                if (!Number.isFinite(providedDecimals)) {
                    throw Error("fillOrder failed, ERC20-priced orders require `paymentTokenDecimals`. Look it up from the payment token reference and pass it explicitly.");
                }
                const decimals = providedDecimals;
                const payValue = takeCount * Number(params.order.price);
                const value = ethers_1.ethers.utils.parseUnits(payValue.toString(), decimals);
                console.log("approve: " + JSON.stringify(params), JSON.stringify(value));
                await (0, assetUtil_1.approveERC20)(this.web3Signer, params.order.paymentToken, value, params);
            }
        }
        else {
            await (0, assetUtil_1.setApproveForAll)(this.web3Signer, params.order.contractAddress, params);
        }
        if (params.order.saleKind === types_1.SaleKind.ContractOffer ||
            params.order.saleKind === types_1.SaleKind.BatchOfferERC721s) {
            if (!params.assetId?.toString()) {
                throw Error(`fillOrder failed, Collection-Based Offer requires the \`assetId\`.`);
            }
        }
        const tradeData = await (0, openApi_1.queryTradeData)(account, [
            {
                orderId: params.order.orderId,
                takeCount,
                tokenId: params.assetId?.toString(),
            },
        ], this.apiOption);
        const call = {
            from: account,
            to: tradeData.to,
            value: tradeData.value,
            data: tradeData.data,
            gasPrice: params.gasPrice,
            maxPriorityFeePerGas: params.maxPriorityFeePerGas,
            maxFeePerGas: params.maxFeePerGas,
        };
        return this.web3Signer.ethSend(call);
    }
    async batchBuyWithETH(params) {
        const taker = await this.web3Signer.getCurrentAccount();
        const list = this.toOrderIdList(params.orders, params.quantities);
        const tradeData = await (0, openApi_1.queryTradeData)(taker, list, this.apiOption);
        const call = {
            from: taker,
            to: tradeData.to,
            value: tradeData.value,
            data: tradeData.data,
            gasPrice: params.gasPrice,
            maxPriorityFeePerGas: params.maxPriorityFeePerGas,
            maxFeePerGas: params.maxFeePerGas,
        };
        return this.web3Signer.ethSend(call);
    }
    async encodeTradeData(params) {
        let taker = params.taker;
        if (taker == null || taker == "" || taker.toLowerCase() == types_1.NULL_ADDRESS) {
            taker = await this.web3Signer.getCurrentAccount();
        }
        const list = this.toOrderIdList(params.orders, params.quantities, params.tokenIds);
        const tradeData = await (0, openApi_1.queryTradeData)(taker, list, this.apiOption);
        return {
            toContract: tradeData.to,
            payableValue: tradeData.value,
            data: tradeData.data,
            flags: tradeData.flags,
        };
    }
    getBoughtAssets(receipt) {
        return (0, receiptUtil_1.getBoughtAssets)(receipt);
    }
    async cancelOrder(params) {
        const account = await this.web3Signer.getCurrentAccount();
        if (params.order?.maker?.toLowerCase() != account.toLowerCase()) {
            throw Error(`cancelOrder failed, account mismatch, order.maker(${params.order?.maker}), account(${account}).`);
        }
        const signedOrder = JSON.parse(params.order.exchangeData);
        if (params.order.standard?.toString().toLowerCase() == types_1.Standard.ElementEx) {
            if (params.order.schema.toLowerCase() == types_1.AssetSchema.ERC721.toLowerCase()) {
                return this.orderManager.cancelERC721Orders([signedOrder], params);
            }
            else if (params.order.schema.toLowerCase() == types_1.AssetSchema.ERC1155.toLowerCase()) {
                return this.orderManager.cancelERC1155Orders([signedOrder], params);
            }
            else {
                throw Error("cancelOrder failed, unsupported schema : " + params.order.schema);
            }
        }
        else {
            throw Error("cancelOrder failed, unsupported standard : " + params.order.standard);
        }
    }
    async cancelOrders(params) {
        if (!params.orders?.length) {
            throw Error(`cancelOrders failed, orders?.length error.`);
        }
        const account = await this.web3Signer.getCurrentAccount();
        params.orders.forEach((value, index, array) => {
            if (account.toLowerCase() != value.maker?.toLowerCase()) {
                throw Error(`cancelOrders failed, account mismatch, index=(${index}), order.maker(${value.maker}), account(${account}).`);
            }
        });
        const elementERC721Orders = [];
        const elementERC1155Orders = [];
        const elementERC721SignedOrders = [];
        const elementERC1155SignedOrders = [];
        for (const order of params.orders) {
            if (order.exchangeData && order.standard) {
                const signedOrder = JSON.parse(order.exchangeData);
                if (order.standard.toLowerCase() == types_1.Standard.ElementEx) {
                    if (order.schema?.toLowerCase() == types_1.AssetSchema.ERC721.toLowerCase()) {
                        elementERC721Orders.push(order);
                        elementERC721SignedOrders.push(signedOrder);
                    }
                    else if (order.schema?.toLowerCase() == types_1.AssetSchema.ERC1155.toLowerCase()) {
                        elementERC1155Orders.push(order);
                        elementERC1155SignedOrders.push(signedOrder);
                    }
                }
            }
        }
        const succeedTransactions = [];
        if (elementERC721Orders.length > 0) {
            const tx = await this.orderManager.cancelERC721Orders(elementERC721SignedOrders, params);
            succeedTransactions.push({
                orders: elementERC721Orders,
                transaction: tx,
            });
        }
        if (elementERC1155Orders.length > 0) {
            try {
                const tx = await this.orderManager.cancelERC1155Orders(elementERC1155SignedOrders, params);
                succeedTransactions.push({
                    orders: elementERC1155Orders,
                    transaction: tx,
                });
            }
            catch (e) {
                if (succeedTransactions.length == 0) {
                    throw e;
                }
            }
        }
        if (succeedTransactions.length == 0) {
            throw Error("cancelOrders failed.");
        }
        return { succeedTransactions: succeedTransactions };
    }
    async cancelAllOrdersForSigner(params) {
        if (params?.standard?.toLowerCase() == types_1.Standard.ElementEx ||
            !params?.standard) {
            return this.orderManager.cancelAllOrders(params);
        }
        else {
            throw Error(`cancelAllOrders failed`);
        }
    }
    async queryOrders(query) {
        return await (0, openApi_1.queryOrders)(query, this.apiOption);
    }
    async queryAccountOrders(query) {
        return await (0, openApi_1.queryAccountOrders)(query, this.apiOption);
    }
    toOrderIdList(orders, quantities, tokenIds) {
        const list = [];
        for (let i = 0; i < orders.length; i++) {
            let takeCount = 1;
            if (quantities?.length && i < quantities?.length) {
                takeCount = Number(quantities[i]) || 1;
            }
            let tokenId;
            if (tokenIds?.length && i < tokenIds.length) {
                tokenId = tokenIds[i]?.toString();
            }
            else {
                if (orders[i].saleKind === types_1.SaleKind.ContractOffer ||
                    orders[i].saleKind === types_1.SaleKind.BatchOfferERC721s) {
                    throw Error(`orders[${i}] error, the collection-based offer requires the \`assetId\``);
                }
            }
            list.push({
                orderId: orders[i].orderId,
                takeCount,
                tokenId,
            });
        }
        return list;
    }
    async makeOrder(params, isBuyOrder) {
        const schema = params.assetSchema || types_1.AssetSchema.ERC721;
        if (schema.toLowerCase() != "erc721" && schema.toLowerCase() != "erc1155") {
            throw Error("makeOrder failed, unsupported schema : " + schema);
        }
        const assetId = (0, numberUtil_1.toString)(params.assetId) || undefined;
        const accountAddress = await this.web3Signer.getCurrentAccount();
        const takerAddress = params.takerAddress
            ? params.takerAddress.toLowerCase()
            : types_1.NULL_ADDRESS;
        // 1. query nonce
        const nonce = await (0, openApi_1.queryNonce)({
            maker: accountAddress,
            schema: schema,
            count: 1,
        }, this.apiOption);
        // 2. query oracleSignature flag
        const oracleSignature = await (0, openApi_1.queryOracleSignature)(this.apiOption);
        // 3. queryFees
        let platformFeePoint, platformFeeAddress, royaltyFeePoint, royaltyFeeAddress;
        if (takerAddress === types_1.NULL_ADDRESS) {
            const fees = await (0, openApi_1.queryFees)([params.assetAddress], this.apiOption);
            if (fees.length > 0) {
                platformFeePoint = fees[0].protocolFeePoints;
                platformFeeAddress = fees[0].protocolFeeAddress;
                royaltyFeePoint = fees[0].royaltyFeePoints;
                royaltyFeeAddress = fees[0].royaltyFeeAddress;
            }
        }
        // 4. create order
        const quantity = params.quantity != null ? (0, numberUtil_1.toString)(params.quantity) : undefined;
        const orderParams = {
            makerAddress: accountAddress,
            takerAddress,
            asset: {
                id: assetId,
                address: params.assetAddress,
                schema: schema.toString().toUpperCase(),
            },
            quantity: quantity,
            paymentToken: params.paymentToken,
            startTokenAmount: (0, numberUtil_1.toString)(params.paymentTokenAmount),
            platformFeePoint: platformFeePoint ?? 0,
            platformFeeAddress: platformFeeAddress,
            royaltyFeePoint: royaltyFeePoint ?? 0,
            royaltyFeeAddress: royaltyFeeAddress,
            listingTime: (0, numberUtil_1.toNumber)(params.listingTime),
            expirationTime: (0, numberUtil_1.toNumber)(params.expirationTime),
            nonce: nonce.toString(),
            saleKind: types_1.SaleKind.FixedPrice,
            oracleSignature,
        };
        const order = isBuyOrder
            ? await this.orderManager.createBuyOrder(orderParams, params)
            : await this.orderManager.createSellOrder(orderParams, params);
        console.log(order);
        // 4. sign order
        const signedOrder = await this.orderManager.signOrder(order);
        // 5. post order
        const request = (0, orderConverter_1.toOrderRequest)(signedOrder);
        const response = await (0, openApi_1.postOrder)(request, this.apiOption);
        return (0, orderConverter_1.toOrderInformation)(request, response.orderId);
    }
    async transferERC721(tokenAddress, tokenId, toAddress) {
        return (0, assetUtil_1.transferERC721)(this.web3Signer, tokenAddress, tokenId, toAddress);
    }
    async transferERC1155(tokenAddress, tokenId, toAddress, quantity) {
        return (0, assetUtil_1.transferERC1155)(this.web3Signer, tokenAddress, tokenId, toAddress, quantity);
    }
}
exports.ElementSDK = ElementSDK;
//# sourceMappingURL=index.js.map