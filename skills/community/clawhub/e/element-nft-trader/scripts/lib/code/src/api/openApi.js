"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.postOrder = postOrder;
exports.postBatchSignedERC721SellOrder = postBatchSignedERC721SellOrder;
exports.queryTradeData = queryTradeData;
exports.queryNonce = queryNonce;
exports.queryOracleSignature = queryOracleSignature;
exports.queryFees = queryFees;
exports.queryOrders = queryOrders;
exports.queryAccountOrders = queryAccountOrders;
const axios_1 = __importDefault(require("axios"));
const openApiTypes_1 = require("./openApiTypes");
const instance = axios_1.default.create();
async function postOrder(order, option, retries = 1) {
    let r;
    try {
        console.log("Wait for postOrder.");
        r = await instance({
            method: "post",
            url: toUrl("/openapi/v1/orders/post", option),
            headers: { "x-api-key": option.apiKey },
            data: order,
            timeout: openApiTypes_1.TIME_OUT,
        });
    }
    catch (e) {
        if (shouldRetry(e, retries)) {
            console.log("postOrder failed, " + e + ", now try again.");
            await sleep(1000);
            return postOrder(order, option, retries - 1);
        }
        throw Error(`postOrder failed, ${e}, order: ${JSON.stringify(order)}`);
    }
    if (r.data?.code !== 0) {
        throw Error(`postOrder failed, ${r.data?.code}, ${r.data?.msg}, ${JSON.stringify(order)}`);
    }
    console.log("postOrder completed.");
    return r.data.data;
}
async function postBatchSignedERC721SellOrder(order, option, retries = 1) {
    let r;
    try {
        console.log("Wait for postBatchOrder.");
        r = await instance({
            method: "post",
            url: toUrl("/openapi/v1/orders/postBatch", option),
            headers: { "x-api-key": option.apiKey },
            data: order,
            timeout: openApiTypes_1.TIME_OUT,
        });
    }
    catch (e) {
        if (shouldRetry(e, retries)) {
            console.log("postBatchOrder failed, " + e + ", now try again.");
            await sleep(1000);
            return postBatchSignedERC721SellOrder(order, option, retries - 1);
        }
        throw Error(`postBatchOrder failed, ${e}, order: ${order}`);
    }
    if (r.data?.code === 0 && r.data?.data) {
        console.log("postBatchOrder completed.");
        return {
            successList: r.data.data.successList || [],
            failList: r.data.data.failList || [],
        };
    }
    throw Error(`postBatchOrder failed, ${r.data?.code}, ${r.data?.msg}, ${JSON.stringify(order)}`);
}
async function queryTradeData(account, list, option, retries = 1) {
    let r;
    try {
        r = await instance({
            method: "post",
            url: toUrl("/openapi/v1/orders/encodeTradeDataByOrderId", option),
            headers: { "x-api-key": option.apiKey },
            data: {
                chain: option.chain,
                taker: account.toLowerCase(),
                orderIdList: list,
            },
            timeout: openApiTypes_1.TIME_OUT,
        });
    }
    catch (e) {
        if (shouldRetry(e, retries)) {
            console.log("encodeTradeData failed, " + e + ", now try again.");
            await sleep(1000);
            return queryTradeData(account, list, option, retries - 1);
        }
        throw Error(`encodeTradeData failed, ${e}`);
    }
    if (r.data?.code === 0 && r.data?.data) {
        return r.data?.data;
    }
    throw Error(`encodeTradeData failed, ${r.data?.code}, ${r.data?.msg}`);
}
async function queryNonce(query, option, retries = 1) {
    let r;
    try {
        const url = toUrl(`/openapi/v1/orders/nonce?chain=${option.chain}`, option) +
            toKeyVal("maker", query) +
            toKeyVal("exchange", query) +
            toKeyVal("schema", query) +
            toKeyVal("count", query);
        r = await instance({
            method: "get",
            url: url,
            headers: { "x-api-key": option.apiKey },
            timeout: openApiTypes_1.TIME_OUT,
        });
    }
    catch (e) {
        if (shouldRetry(e, retries)) {
            console.log("queryNonce failed, " + e + ", now try again.");
            await sleep(1000);
            return queryNonce(query, option, retries - 1);
        }
        throw Error("queryNonce failed, " + e);
    }
    if (r.data?.code === 0 && r.data?.data?.nonce != null) {
        console.log("queryNonce, nonce: " + r.data.data.nonce.toString());
        return Number(r.data.data.nonce.toString());
    }
    throw Error("queryNonce failed, " + r.data?.msg);
}
async function queryOracleSignature(option, retries = 1) {
    let r;
    try {
        const url = toUrl(`/openapi/v1/orders/confData?chain=${option.chain}`, option);
        r = await instance({
            method: "get",
            url: url,
            headers: { "x-api-key": option.apiKey },
            timeout: openApiTypes_1.TIME_OUT,
        });
        if (r.data?.data?.oracleSignature != null) {
            console.log("queryOracleSignature success, oracleSignature: " +
                r.data.data.oracleSignature);
            return Number(r.data.data.oracleSignature);
        }
    }
    catch (e) {
        if (shouldRetry(e, retries)) {
            console.log("queryOracleSignature failed, " + e + ", now try again.");
            await sleep(1000);
            return queryOracleSignature(option, retries - 1);
        }
    }
    console.log("queryOracleSignature failed, use default value `0`");
    return 0;
}
async function queryFees(contractAddressList, option, retries = 1) {
    let r;
    try {
        r = await instance({
            method: "post",
            url: toUrl("/openapi/v1/collection/fee", option),
            headers: { "x-api-key": option.apiKey },
            data: {
                chain: option.chain,
                data: contractAddressList.map((value) => {
                    return {
                        contractAddress: value.toLowerCase(),
                    };
                }),
            },
            timeout: openApiTypes_1.TIME_OUT,
        });
    }
    catch (e) {
        if (shouldRetry(e, retries)) {
            console.log("queryFees failed, " + e + ", now try again.");
            await sleep(1000);
            return queryFees(contractAddressList, option, retries - 1);
        }
        throw Error("queryFees failed, " + e);
    }
    if (r.data?.code === 0) {
        return r.data?.data?.feeList || [];
    }
    throw Error("queryFees failed, " + r.data?.msg);
}
async function queryOrders(query, option) {
    const url = toUrl(`/openapi/v1/orders/list?chain=${option.chain}`, option) +
        toKeyVal("asset_contract_address", query) +
        toTokenIdsKeyVal("token_ids", query) +
        toKeyVal("sale_kind", query) +
        toKeyVal("side", query) +
        toKeyVal("maker", query) +
        toKeyVal("taker", query) +
        toKeyVal("payment_token", query) +
        toKeyVal("order_by", query) +
        toKeyVal("direction", query) +
        toKeyVal("listed_before", query) +
        toKeyVal("listed_after", query) +
        toKeyVal("limit", query) +
        toKeyVal("offset", query);
    let r;
    try {
        r = await instance({
            method: "get",
            url: url,
            headers: { "x-api-key": option.apiKey },
            timeout: openApiTypes_1.TIME_OUT,
        });
    }
    catch (e) {
        throw Error("queryOrders failed, " + e);
    }
    if (r.data?.code === 0) {
        return r.data?.data?.orders || [];
    }
    throw Error("queryOrders failed, " + r.data?.msg);
}
async function queryAccountOrders(query, option, retries = 1) {
    const chain = option.chain;
    const normalizedLimit = Number(query.limit ?? 20);
    const safeLimit = Number.isFinite(normalizedLimit) && normalizedLimit > 0
        ? Math.min(normalizedLimit, 50)
        : 20;
    const url = toUrl(`/openapi/v1/account/orderList?chain=${chain}`, option) +
        toKeyVal("wallet_address", query) +
        toKeyVal("contract_address", query) +
        toKeyVal("cursor", query) +
        `&limit=${safeLimit}`;
    let r;
    try {
        r = await instance({
            method: "get",
            url: url,
            headers: { "x-api-key": option.apiKey },
            timeout: openApiTypes_1.TIME_OUT,
        });
    }
    catch (e) {
        if (shouldRetry(e, retries)) {
            console.log("queryAccountOrders failed, " + e + ", now try again.");
            await sleep(1000);
            return queryAccountOrders(query, option, retries - 1);
        }
        throw Error("queryAccountOrders failed, " + e);
    }
    if (r.data?.code === 0) {
        return r.data?.data || {};
    }
    throw Error("queryAccountOrders failed, " + r.data?.msg);
}
function toUrl(path, option) {
    return openApiTypes_1.API_HOST + path;
}
function sleep(ms) {
    return Promise.resolve((resolve) => setTimeout(resolve, ms));
}
function toTokenIdsKeyVal(key, query) {
    let val = "";
    if (query[key]?.length) {
        for (const id of query[key]) {
            const idStr = formatVal(id);
            if (idStr != "") {
                if (val != "") {
                    val += ",";
                }
                val += idStr;
            }
        }
    }
    return val != "" ? `&${key}=${val}` : "";
}
function toKeyVal(key, query) {
    const val = formatVal(query[key]);
    return val != "" ? `&${key}=${val}` : "";
}
function formatVal(value) {
    return value != null ? value.toString().toLowerCase() : "";
}
function shouldRetry(error, retries) {
    if (retries > 0) {
        if (error?.message?.toString().startsWith("timeout of")) {
            return true;
        }
        if (error?.response) {
            const status = error?.response.status;
            return (status == 403 ||
                status == 429 ||
                status == 500 ||
                status == 502 ||
                status == 503 ||
                status == 504);
        }
    }
    return false;
}
//# sourceMappingURL=openApi.js.map