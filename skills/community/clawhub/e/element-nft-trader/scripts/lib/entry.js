"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const index_1 = require("./code/index");
const ethers_1 = require("ethers");
const EXPLORER_URLS = {
    eth: "https://etherscan.io",
    bsc: "https://bscscan.com",
    polygon: "https://polygonscan.com",
    avalanche: "https://snowtrace.io",
    arbitrum: "https://arbiscan.io",
    zksync: "https://explorer.zksync.io",
    linea: "https://lineascan.build",
    base: "https://basescan.org",
    opbnb: "https://opbnbscan.com",
    scroll: "https://scrollscan.com",
    manta_pacific: "https://manta.socialscan.net",
    optimism: "https://optimistic.etherscan.io",
    mantle: "https://mantlescan.xyz",
    zkfair: "https://zkfair.io",
    blast: "https://blastscan.io",
    merlin: "https://merlinchain.io",
    mode: "https://explorer.mode.network",
    cyber: "https://cyber.socialscan.net",
    bob: "https://bobscan.com",
    lightlink: "https://explorer.lightlink.io",
    nanon: "https://nanonscan.io",
    bera: "https://berascan.com",
    zeta: "https://zetachain-node.blockscout.com",
    nibiru: "https://nibiscan.io",
    abstract: "https://abscan.org",
    monad: "https://monadscan.xyz",
    bitlayer: "https://bitlayerscan.com",
    mantra: "https://mantrascan.io",
};
// ============== Utilities ==============
function log(data) {
    console.log(JSON.stringify(data));
}
function isBlank(value) {
    return value == null || (typeof value === "string" && value.trim() === "");
}
function getExplorerUrl(network) {
    return EXPLORER_URLS[network.toLowerCase()] || "https://etherscan.io";
}
function normalizeQuantity(quantity) {
    const parsed = Number(quantity);
    return Number.isFinite(parsed) && parsed > 0 ? parsed : 1;
}
function calculateOrderCost(order, quantity) {
    const orderPrice = Number(order?.price);
    if (!Number.isFinite(orderPrice)) {
        return String(order?.price ?? "");
    }
    const requestedQuantity = normalizeQuantity(quantity);
    const availableQuantity = Number(order?.quantity);
    if (String(order?.schema).toUpperCase() === "ERC1155" &&
        Number.isFinite(availableQuantity) &&
        availableQuantity > 0) {
        return String((orderPrice * requestedQuantity) / availableQuantity);
    }
    return String(orderPrice * requestedQuantity);
}
function formatUnixTimestamp(timestamp) {
    if (timestamp == null || timestamp === "")
        return null;
    const numeric = Number(timestamp);
    if (!Number.isFinite(numeric) || numeric <= 0) {
        return String(timestamp);
    }
    return new Date(numeric * 1000).toISOString().replace(".000Z", " UTC");
}
function serializeOrder(order) {
    return {
        orderId: order.orderId,
        maker: order.maker,
        contractAddress: order.contractAddress,
        tokenId: order.tokenId,
        schema: order.schema,
        standard: order.standard,
        quantity: order.quantity,
        price: order.price,
        priceBase: order.priceBase,
        priceUSD: order.priceUSD,
        paymentToken: order.paymentToken,
        saleKind: order.saleKind,
        side: order.side,
        listingTime: formatUnixTimestamp(order.listingTime),
        expirationTime: formatUnixTimestamp(order.expirationTime),
        taker: order.taker,
        exchangeData: order.exchangeData,
    };
}
function isNativePaymentToken(paymentToken) {
    if (isBlank(paymentToken))
        return true;
    const normalized = String(paymentToken).toLowerCase();
    return normalized === index_1.NULL_ADDRESS || normalized === index_1.ETH_TOKEN_ADDRESS;
}
function extractErrorMessage(error) {
    if (error?.reason)
        return String(error.reason);
    if (error?.message)
        return String(error.message);
    if (error?.error?.message)
        return String(error.error.message);
    if (typeof error === "string")
        return error;
    return JSON.stringify(error);
}
function extractErrorCode(error) {
    if (error?.code)
        return String(error.code);
    if (error?.error?.code)
        return String(error.error.code);
    return null;
}
function logError(type, message, code = null, extra = {}) {
    log({ status: "error", type, message, code, ...extra });
    process.exit(1);
}
function validateRequiredFields(operation, values) {
    const missing = values
        .filter(({ value, rule }) => (rule ? !rule(value) : isBlank(value)))
        .map(({ field, detail }) => ({ field, detail }));
    if (missing.length === 0)
        return;
    const fields = missing.map((item) => item.field);
    const details = missing
        .filter((item) => item.detail)
        .map((item) => `${item.field}: ${item.detail}`);
    logError("validation", `Missing or invalid required parameters for ${operation}: ${fields.join(", ")}`, null, {
        operation,
        fields,
        details: details.length ? details : undefined,
    });
}
function validateOrderFields(operation, order, prefix, fields) {
    validateRequiredFields(operation, fields.map(({ field, detail }) => ({
        field: `${prefix}.${field}`,
        value: order?.[field],
        detail,
    })));
}
function validateInput(input) {
    const { operationType } = input;
    const stateChangingOperations = [
        "erc721sell",
        "erc1155sell",
        "buy",
        "offer",
        "acceptOffer",
        "cancel",
    ];
    if (isBlank(operationType)) {
        logError("validation", "operationType is required");
    }
    if (isBlank(input.network)) {
        logError("validation", `network is required for ${operationType}`, null, {
            operation: operationType,
            fields: ["network"],
        });
    }
    if (stateChangingOperations.includes(operationType) &&
        input.confirmed !== true) {
        logError("validation", `${operationType} requires confirmed=true after explicit user confirmation`, null, {
            operation: operationType,
            fields: ["confirmed"],
        });
    }
    switch (operationType) {
        case "erc721sell": {
            validateRequiredFields(operationType, [
                {
                    field: "sellOrders.items",
                    value: input.sellOrders?.items,
                    rule: (value) => Array.isArray(value) && value.length > 0,
                    detail: "Provide at least one ERC721 item to list",
                },
            ]);
            (input.sellOrders?.items ?? []).forEach((item, index) => {
                validateRequiredFields(operationType, [
                    {
                        field: `sellOrders.items[${index}].erc721TokenAddress`,
                        value: item?.erc721TokenAddress,
                    },
                    {
                        field: `sellOrders.items[${index}].erc721TokenId`,
                        value: item?.erc721TokenId,
                    },
                    {
                        field: `sellOrders.items[${index}].paymentTokenAmount`,
                        value: item?.paymentTokenAmount,
                    },
                ]);
            });
            return;
        }
        case "erc1155sell":
            validateRequiredFields(operationType, [
                {
                    field: "erc1155sellOrder.assetAddress",
                    value: input.erc1155sellOrder?.assetAddress,
                },
                {
                    field: "erc1155sellOrder.assetId",
                    value: input.erc1155sellOrder?.assetId,
                },
                {
                    field: "erc1155sellOrder.quantity",
                    value: input.erc1155sellOrder?.quantity,
                },
                {
                    field: "erc1155sellOrder.paymentTokenAmount",
                    value: input.erc1155sellOrder?.paymentTokenAmount,
                },
            ]);
            return;
        case "offer":
            validateRequiredFields(operationType, [
                {
                    field: "offerOrder.assetAddress",
                    value: input.offerOrder?.assetAddress,
                },
                {
                    field: "offerOrder.assetSchema",
                    value: input.offerOrder?.assetSchema,
                    detail: "Explicitly set ERC721 or ERC1155 for offer creation",
                },
                {
                    field: "offerOrder.paymentTokenAmount",
                    value: input.offerOrder?.paymentTokenAmount,
                },
            ]);
            return;
        case "acceptOffer": {
            validateRequiredFields(operationType, [
                {
                    field: "acceptOfferOrder.order",
                    value: input.acceptOfferOrder?.order,
                },
            ]);
            const order = input.acceptOfferOrder?.order;
            validateOrderFields(operationType, order, "acceptOfferOrder.order", [
                { field: "orderId" },
                { field: "contractAddress" },
                { field: "standard" },
                { field: "schema" },
                { field: "side", detail: "Use a buy-side order returned by query" },
                { field: "paymentToken" },
                { field: "price" },
            ]);
            const saleKind = Number(order?.saleKind);
            if ((saleKind === 7 || saleKind === 8) &&
                isBlank(input.acceptOfferOrder?.assetId)) {
                logError("validation", "acceptOfferOrder.assetId is required for collection-wide offers", null, { operation: operationType, fields: ["acceptOfferOrder.assetId"] });
            }
            return;
        }
        case "buy": {
            validateRequiredFields(operationType, [
                {
                    field: "buyOrders.orders",
                    value: input.buyOrders?.orders,
                    rule: (value) => Array.isArray(value) && value.length > 0,
                    detail: "Provide at least one order returned by query",
                },
            ]);
            const orders = input.buyOrders?.orders ?? [];
            orders.forEach((order, index) => {
                validateOrderFields(operationType, order, `buyOrders.orders[${index}]`, [
                    { field: "orderId" },
                    { field: "contractAddress" },
                    { field: "standard" },
                    { field: "schema" },
                    {
                        field: "side",
                        detail: "Use a sell-side order returned by query",
                    },
                    { field: "paymentToken" },
                    { field: "price" },
                ]);
                if (!isNativePaymentToken(order?.paymentToken)) {
                    validateRequiredFields(operationType, [
                        {
                            field: `buyOrders.orders[${index}].paymentTokenDecimals`,
                            value: order?.paymentTokenDecimals,
                            detail: "ERC20-priced buys require paymentTokenDecimals; look it up from the payment token reference instead of guessing",
                        },
                    ]);
                }
            });
            const hasERC1155 = orders.some((order) => String(order?.schema).toUpperCase() === "ERC1155");
            if (hasERC1155) {
                validateRequiredFields(operationType, [
                    {
                        field: "buyOrders.quantities",
                        value: input.buyOrders?.quantities,
                        rule: (value) => Array.isArray(value) && value.length === orders.length,
                        detail: "ERC1155 buys require a quantities array aligned with orders",
                    },
                ]);
            }
            return;
        }
        case "query":
            validateRequiredFields(operationType, [
                {
                    field: "queryOrders.asset_contract_address",
                    value: input.queryOrders?.asset_contract_address,
                },
            ]);
            return;
        case "queryAccountOrders":
            return;
        case "cancel": {
            validateRequiredFields(operationType, [
                {
                    field: "ordersToCancel.orders",
                    value: input.ordersToCancel?.orders,
                    rule: (value) => Array.isArray(value) && value.length > 0,
                    detail: "Provide at least one full order object to cancel",
                },
            ]);
            (input.ordersToCancel?.orders ?? []).forEach((order, index) => {
                validateOrderFields(operationType, order, `ordersToCancel.orders[${index}]`, [
                    { field: "maker" },
                    { field: "schema" },
                    { field: "standard" },
                    { field: "exchangeData" },
                ]);
            });
            return;
        }
        case "getAddress":
            return;
        default:
            return;
    }
}
// ============== Credentials & SDK ==============
async function getCredentials() {
    const apiKeyFromEnv = process.env.ELEMENT_API_KEY;
    const privateKeyFromEnv = process.env.ELEMENT_WALLET_PRIVATE_KEY;
    if (!apiKeyFromEnv || !privateKeyFromEnv) {
        throw new Error("Missing required environment variables: ELEMENT_API_KEY and ELEMENT_WALLET_PRIVATE_KEY");
    }
    return {
        apiKey: apiKeyFromEnv,
        wallet: { private_key: privateKeyFromEnv },
    };
}
async function createSDK(network) {
    const credentials = await getCredentials();
    const chainId = (0, index_1.getChainId)(network, false);
    const chainMId = (0, index_1.getChainMId)(chainId);
    const rpcUrl = await (0, index_1.getRpcUrlFromRemote)(chainMId);
    const provider = new ethers_1.ethers.providers.JsonRpcProvider(rpcUrl);
    const signer = new ethers_1.ethers.Wallet(credentials.wallet.private_key, provider);
    return new index_1.ElementSDK({
        networkName: network,
        isTestnet: false,
        apiKey: credentials.apiKey,
        signer: signer,
    });
}
async function getInput() {
    if (process.argv[2]) {
        try {
            return JSON.parse(process.argv[2]);
        }
        catch (e) {
            throw new Error(`Invalid JSON in command argument: ${extractErrorMessage(e)}`);
        }
    }
    return new Promise((resolve, reject) => {
        let data = "";
        process.stdin.setEncoding("utf8");
        process.stdin.on("data", (chunk) => {
            data += chunk;
        });
        process.stdin.on("end", () => {
            try {
                resolve(JSON.parse(data.trim()));
            }
            catch (e) {
                reject(new Error(`Invalid JSON in stdin: ${extractErrorMessage(e)}`));
            }
        });
        process.stdin.on("error", (e) => reject(new Error(`stdin error: ${extractErrorMessage(e)}`)));
    });
}
// ============== Operation Handlers ==============
async function handleERC721Sell(sdk, params) {
    if (!params)
        throw new Error("sellOrders is not set");
    const result = await sdk.makeERC721SellOrders(params);
    if (result.succeedList.length === 0 && result.failedList.length > 0) {
        logError("erc721sell", "All orders failed", null, {
            failedList: result.failedList.map((item) => ({
                tokenId: item.assetTokenId,
                contractAddress: item.assetContract,
                error: item.errorDetail,
            })),
        });
    }
    log({
        status: "success",
        operation: "erc721sell",
        succeedCount: result.succeedList.length,
        failedCount: result.failedList.length,
        succeedList: result.succeedList.map((o) => ({
            orderId: o.orderId,
            contractAddress: o.contractAddress,
            tokenId: o.tokenId,
            price: o.price,
            paymentToken: o.paymentToken,
            expirationTime: formatUnixTimestamp(o.expirationTime),
        })),
        failedList: result.failedList.map((item) => ({
            tokenId: item.assetTokenId,
            contractAddress: item.assetContract,
            error: item.errorDetail,
        })),
    });
}
async function handleERC1155Sell(sdk, params) {
    if (!params)
        throw new Error("erc1155sellOrder is not set");
    const result = await sdk.makeSellOrder(params);
    log({
        status: "success",
        operation: "erc1155sell",
        orderId: result.orderId,
        contractAddress: result.contractAddress,
        tokenId: result.tokenId,
        price: result.price,
        paymentToken: result.paymentToken,
        listingTime: formatUnixTimestamp(result.listingTime),
        expirationTime: formatUnixTimestamp(result.expirationTime),
    });
}
async function handleBuy(sdk, params, explorerBase) {
    if (!params)
        throw new Error("buyOrders is not set");
    const orders = params.orders ?? [];
    const hasERC20Payment = orders.some((order) => !isNativePaymentToken(order?.paymentToken));
    if (hasERC20Payment) {
        if (orders.length !== 1) {
            logError("buy", "ERC20-priced buys currently support exactly one order at a time", null, {
                orderCount: orders.length,
                paymentTokens: orders.map((order) => order?.paymentToken ?? null),
            });
        }
        const order = orders[0];
        const quantity = params.quantities?.[0];
        const tx = await sdk.fillOrder({
            order,
            quantity,
        });
        let receipt;
        try {
            receipt = await tx.wait();
        }
        catch (e) {
            logError("buy", `Transaction failed on-chain: ${extractErrorMessage(e)}`, extractErrorCode(e), {
                transactionHash: tx.hash,
                explorerUrl: `${explorerBase}/tx/${tx.hash}`,
            });
        }
        log({
            status: receipt.status === 1 ? "success" : "failed",
            operation: "buy",
            paymentMode: "erc20-single-fill",
            orders: [
                {
                    orderId: order.orderId,
                    contractAddress: order.contractAddress,
                    tokenId: order.tokenId,
                    schema: order.schema,
                    requestedQuantity: String(quantity ?? "1"),
                    paymentToken: order.paymentToken,
                    cost: calculateOrderCost(order, quantity),
                },
            ],
            transactionHash: tx.hash,
            blockNumber: receipt.blockNumber,
            gasUsed: receipt.gasUsed.toString(),
            explorerUrl: `${explorerBase}/tx/${tx.hash}`,
        });
        return;
    }
    const tx = await sdk.batchBuyWithETH(params);
    let receipt;
    try {
        receipt = await tx.wait();
    }
    catch (e) {
        logError("buy", `Transaction failed on-chain: ${extractErrorMessage(e)}`, extractErrorCode(e), {
            transactionHash: tx.hash,
            explorerUrl: `${explorerBase}/tx/${tx.hash}`,
        });
    }
    log({
        status: receipt.status === 1 ? "success" : "failed",
        operation: "buy",
        paymentMode: "native-batch-buy",
        orders: params.orders.map((order, index) => ({
            orderId: order.orderId,
            contractAddress: order.contractAddress,
            tokenId: order.tokenId,
            schema: order.schema,
            requestedQuantity: String(params.quantities?.[index] ?? "1"),
            paymentToken: order.paymentToken,
            cost: calculateOrderCost(order, params.quantities?.[index]),
        })),
        transactionHash: tx.hash,
        blockNumber: receipt.blockNumber,
        gasUsed: receipt.gasUsed.toString(),
        explorerUrl: `${explorerBase}/tx/${tx.hash}`,
    });
}
async function handleOffer(sdk, params) {
    if (!params)
        throw new Error("offerOrder is not set");
    const result = await sdk.makeBuyOrder(params);
    log({
        status: "success",
        operation: "offer",
        orderId: result.orderId,
        contractAddress: result.contractAddress,
        price: result.price,
        paymentToken: result.paymentToken,
        listingTime: formatUnixTimestamp(result.listingTime),
        expirationTime: formatUnixTimestamp(result.expirationTime),
    });
}
async function handleAcceptOffer(sdk, params, explorerBase) {
    if (!params?.order)
        throw new Error("acceptOfferOrder.order is not set");
    const tx = await sdk.fillOrder(params);
    let receipt;
    try {
        receipt = await tx.wait();
    }
    catch (e) {
        logError("acceptOffer", `Transaction failed on-chain: ${extractErrorMessage(e)}`, extractErrorCode(e), {
            transactionHash: tx.hash,
            explorerUrl: `${explorerBase}/tx/${tx.hash}`,
        });
    }
    log({
        status: receipt.status === 1 ? "success" : "failed",
        operation: "acceptOffer",
        acceptedOffer: {
            orderId: params.order.orderId,
            maker: params.order.maker,
            contractAddress: params.order.contractAddress,
            tokenId: String(params.assetId ?? params.order.tokenId ?? ""),
            schema: params.order.schema,
            quantity: String(params.quantity ?? "1"),
            paymentToken: params.order.paymentToken,
            price: params.order.price,
            proceeds: calculateOrderCost(params.order, params.quantity),
        },
        transactionHash: tx.hash,
        blockNumber: receipt.blockNumber,
        gasUsed: receipt.gasUsed.toString(),
        explorerUrl: `${explorerBase}/tx/${tx.hash}`,
    });
}
async function handleQuery(sdk, query) {
    if (!query?.asset_contract_address) {
        throw new Error("asset_contract_address is not set");
    }
    const orders = await sdk.queryOrders(query);
    log({
        status: "success",
        operation: "query",
        count: orders.length,
        orders: orders.map((o) => serializeOrder(o)),
    });
}
async function handleQueryAccountOrders(sdk, params = {}) {
    const payload = await sdk.queryAccountOrders(params);
    const assetList = payload?.assetList ?? [];
    const chain = (sdk.apiOption?.chain || "").toString();
    log({
        status: "success",
        operation: "queryAccountOrders",
        chain,
        usingDefaultAccount: isBlank(params.wallet_address),
        walletAddress: params.wallet_address ?? null,
        contractAddress: params.contract_address ?? null,
        cursor: params.cursor ?? null,
        pageInfo: payload?.pageInfo ?? null,
        count: assetList.length,
        orders: assetList.map((item) => ({
            cursor: item?.cursor ?? null,
            name: item?.asset?.name,
            slug: item?.asset?.collection?.slug,
            tokenId: item?.asset?.tokenId,
            collection: item?.asset?.collection?.name,
            contractAddress: item?.asset?.contractAddress,
            price: item?.orderData?.accountOrder?.price,
            priceUSD: item?.orderData?.accountOrder?.priceUSD,
            paymentToken: item?.orderData?.accountOrder?.paymentToken,
            quantity: item?.orderData?.accountOrder?.quantity,
            side: item?.orderData?.accountOrder?.side,
            saleKind: item?.orderData?.accountOrder?.saleKind,
            standard: item?.orderData?.accountOrder?.standard,
            schema: item?.orderData?.accountOrder?.schema,
            listingTime: formatUnixTimestamp(item?.orderData?.accountOrder?.listingTime),
            expirationTime: formatUnixTimestamp(item?.orderData?.accountOrder?.expirationTime),
        })),
    });
}
async function handleGetAddress(sdk) {
    const address = await sdk.web3Signer.getCurrentAccount();
    log({
        status: "success",
        operation: "getAddress",
        address,
    });
}
async function handleCancel(sdk, params, explorerBase) {
    if (!params?.orders?.length)
        throw new Error("ordersToCancel is not set or empty");
    const result = await sdk.cancelOrders({ orders: params.orders });
    if (result.succeedTransactions.length === 0) {
        logError("cancel", "No orders were successfully cancelled");
    }
    const transactions = [];
    for (const txInfo of result.succeedTransactions) {
        let receipt;
        try {
            receipt = await txInfo.transaction.wait();
        }
        catch (e) {
            transactions.push({
                transactionHash: txInfo.transaction.hash,
                status: "failed",
                message: extractErrorMessage(e),
                explorerUrl: `${explorerBase}/tx/${txInfo.transaction.hash}`,
            });
            continue;
        }
        transactions.push({
            transactionHash: txInfo.transaction.hash,
            blockNumber: receipt.blockNumber,
            gasUsed: receipt.gasUsed.toString(),
            status: receipt.status === 1 ? "success" : "failed",
            explorerUrl: `${explorerBase}/tx/${txInfo.transaction.hash}`,
        });
    }
    log({
        status: "success",
        operation: "cancel",
        cancelledCount: result.succeedTransactions.length,
        transactions,
    });
}
// ============== Main ==============
async function main() {
    let input;
    try {
        input = await getInput();
    }
    catch (e) {
        logError("input", extractErrorMessage(e), extractErrorCode(e));
    }
    validateInput(input);
    const { network, operationType } = input;
    let sdk;
    const needsSdk = true;
    if (needsSdk) {
        try {
            sdk = await createSDK(network);
        }
        catch (e) {
            logError("sdk_init", extractErrorMessage(e), extractErrorCode(e));
        }
    }
    const explorerBase = network
        ? getExplorerUrl(network)
        : "https://etherscan.io";
    try {
        switch (operationType) {
            case "erc721sell":
                await handleERC721Sell(sdk, input.sellOrders);
                break;
            case "erc1155sell":
                await handleERC1155Sell(sdk, input.erc1155sellOrder);
                break;
            case "buy":
                await handleBuy(sdk, input.buyOrders, explorerBase);
                break;
            case "offer":
                await handleOffer(sdk, input.offerOrder);
                break;
            case "acceptOffer":
                await handleAcceptOffer(sdk, input.acceptOfferOrder, explorerBase);
                break;
            case "query":
                await handleQuery(sdk, input.queryOrders);
                break;
            case "queryAccountOrders":
                await handleQueryAccountOrders(sdk, input.queryAccountOrders);
                break;
            case "cancel":
                await handleCancel(sdk, input.ordersToCancel, explorerBase);
                break;
            case "getAddress":
                await handleGetAddress(sdk);
                break;
            default:
                throw new Error(`Unsupported operation type: ${operationType}`);
        }
    }
    catch (e) {
        logError(operationType || "unknown", extractErrorMessage(e), extractErrorCode(e));
    }
}
main();
//# sourceMappingURL=entry.js.map