"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.toOrderInformation = toOrderInformation;
exports.toOrderRequest = toOrderRequest;
const ethers_1 = require("ethers");
const chainUtil_1 = require("../../util/chainUtil");
const config_1 = require("../../contracts/config");
const types_1 = require("../../types/types");
const bitsUtil_1 = require("../../util/bitsUtil");
const tokenUtil_1 = require("../../util/tokenUtil");
function toOrderInformation(order, orderId) {
    let price = order.basePrice;
    if (order.quantity) {
        price = ethers_1.BigNumber.from(order.basePrice).div(order.quantity).toString();
    }
    return {
        contractAddress: order.metadata.asset.address,
        tokenId: order.metadata.asset.id,
        schema: order.metadata.schema,
        standard: types_1.Standard.ElementEx,
        maker: order.maker,
        listingTime: Number(order.listingTime),
        expirationTime: Number(order.expirationTime),
        price: Number(ethers_1.ethers.utils.formatEther(price)),
        paymentToken: order.paymentToken,
        saleKind: order.saleKind,
        side: order.side,
        orderId
    };
}
function toOrderRequest(signedOrder) {
    const { order, signature, chainId } = signedOrder;
    const chain = (0, chainUtil_1.getChain)(chainId);
    const exchange = config_1.CONTRACTS_ADDRESSES[chainId].ElementEx;
    const info = parseOrder(order);
    const expiry = decodeExpiry(order.expiry);
    const totalERC20Amount = calcTotalERC20Amount(order);
    const paymentToken = (0, tokenUtil_1.toStandardERC20Token)(order.erc20Token);
    const request = {
        exchange: exchange.toLowerCase(),
        maker: order.maker.toLowerCase(),
        taker: order.taker.toLowerCase(),
        side: info.side,
        saleKind: expiry.saleKind,
        oracleSignature: expiry.oracleSignature,
        paymentToken: paymentToken,
        quantity: info.quantity,
        basePrice: totalERC20Amount,
        extra: expiry.extra,
        listingTime: expiry.listingTime,
        expirationTime: expiry.expirationTime,
        metadata: info.metadata,
        fees: toLowerCaseFees(order.fees),
        nonce: order.nonce,
        hashNonce: order.hashNonce,
        hash: signedOrder.orderHash,
        signatureType: signature.signatureType,
        v: signature.v,
        r: signature.r,
        s: signature.s,
        chain: chain
    };
    if (info.properties != null) {
        request.properties = toLowerCaseProperties(info.properties);
        if (request.properties.length > 0) {
            request.saleKind = types_1.SaleKind.ContractOffer;
        }
    }
    return request;
}
function toLowerCaseFees(fees) {
    return fees.map(fee => ({
        recipient: fee.recipient.toLowerCase(),
        amount: ethers_1.BigNumber.from(fee.amount).toString(),
        feeData: fee.feeData
    }));
}
function toLowerCaseProperties(properties) {
    return properties.map(property => ({
        propertyValidator: property.propertyValidator.toLowerCase(),
        propertyData: property.propertyData
    }));
}
function calcTotalERC20Amount(order) {
    let total = ethers_1.BigNumber.from(order.erc20TokenAmount);
    for (let i = 0; i < order.fees.length; i++) {
        total = total.add(order.fees[i].amount);
    }
    return total.toString();
}
function parseOrder(order) {
    let side;
    let quantity;
    let metadata;
    let properties;
    if (order['nft'] != undefined) {
        quantity = '1';
        metadata = {
            asset: {
                id: order['nftId'],
                address: order['nft'].toString().toLowerCase()
            },
            schema: types_1.AssetSchema.ERC721
        };
        if (order['nftProperties'] != undefined) {
            side = types_1.OrderSide.BuyOrder;
            properties = toLowerCaseProperties(order['nftProperties']);
        }
        else {
            side = types_1.OrderSide.SellOrder;
            properties = undefined;
        }
    }
    else if (order['erc1155Token'] != undefined) {
        quantity = order['erc1155TokenAmount'];
        metadata = {
            asset: {
                id: order['erc1155TokenId'],
                address: order['erc1155Token'].toString().toLowerCase()
            },
            schema: types_1.AssetSchema.ERC1155
        };
        if (order['erc1155TokenProperties'] != undefined) {
            side = types_1.OrderSide.BuyOrder;
            properties = toLowerCaseProperties(order['erc1155TokenProperties']);
        }
        else {
            side = types_1.OrderSide.SellOrder;
            properties = undefined;
        }
    }
    else {
        throw Error('toOrderStr error');
    }
    return { side, quantity, metadata, properties };
}
function decodeExpiry(expiry) {
    // saleKind (4bit) + reserved(156bit) + extra(32bit) + listingTime(32bit) + expiryTime(32bit) = 256bit
    const hex = (0, bitsUtil_1.encodeBits)([[expiry, 256]]).substring(2);
    const orderSaleKindHex = '0x' + hex.substring(0, 1);
    const oracleSignatureHex = '0x' + hex.substring(1, 2);
    const extraHex = '0x' + hex.substring(40, 48);
    const listingTimeHex = '0x' + hex.substring(48, 56);
    const expiryTimeHex = '0x' + hex.substring(56, 64);
    return {
        saleKind: parseInt(orderSaleKindHex),
        oracleSignature: parseInt(oracleSignatureHex),
        extra: parseInt(extraHex).toString(),
        listingTime: parseInt(listingTimeHex),
        expirationTime: parseInt(expiryTimeHex)
    };
}
//# sourceMappingURL=orderConverter.js.map