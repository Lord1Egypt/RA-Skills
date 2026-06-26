"use strict";
/**
 * HTTP client for the Auction House API v1
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.listAuctions = listAuctions;
exports.searchAuctions = searchAuctions;
exports.getAuction = getAuction;
exports.getMyAuctions = getMyAuctions;
exports.getMyBids = getMyBids;
exports.getWalletInfo = getWalletInfo;
exports.createAuction = createAuction;
exports.placeBid = placeBid;
const DEFAULT_BASE_URL = 'https://www.houseproto.fun';
function getBaseUrl() {
    return process.env.AUCTION_HOUSE_URL || DEFAULT_BASE_URL;
}
function getApiKey() {
    const key = process.env.AUCTION_HOUSE_API_KEY;
    if (!key) {
        throw new Error('AUCTION_HOUSE_API_KEY environment variable is not set. ' +
            'Generate one at https://www.houseproto.fun/settings');
    }
    return key;
}
async function request(method, path, body) {
    const url = `${getBaseUrl()}/api/v1${path}`;
    const headers = {
        'x-api-key': getApiKey(),
        'Content-Type': 'application/json',
    };
    const res = await fetch(url, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
    });
    const data = await res.json();
    return {
        ok: res.ok,
        status: res.status,
        data,
    };
}
// ─── Read Operations ───
async function listAuctions(params) {
    const query = new URLSearchParams();
    if (params?.status)
        query.set('status', params.status);
    if (params?.limit)
        query.set('limit', params.limit.toString());
    if (params?.offset)
        query.set('offset', params.offset.toString());
    const qs = query.toString();
    return request('GET', `/auctions${qs ? `?${qs}` : ''}`);
}
async function searchAuctions(params) {
    const query = new URLSearchParams();
    if (params.search)
        query.set('search', params.search);
    if (params.currency)
        query.set('currency', params.currency);
    if (params.token)
        query.set('token', params.token);
    if (params.minPrice !== undefined)
        query.set('minPrice', params.minPrice.toString());
    if (params.maxPrice !== undefined)
        query.set('maxPrice', params.maxPrice.toString());
    if (params.createdAfter)
        query.set('createdAfter', params.createdAfter);
    if (params.endingWithin !== undefined)
        query.set('endingWithin', params.endingWithin.toString());
    if (params.sort)
        query.set('sort', params.sort);
    if (params.status)
        query.set('status', params.status);
    if (params.limit)
        query.set('limit', params.limit.toString());
    const qs = query.toString();
    return request('GET', `/auctions${qs ? `?${qs}` : ''}`);
}
async function getAuction(blockchainAuctionId) {
    return request('GET', `/auctions/${blockchainAuctionId}`);
}
async function getMyAuctions(params) {
    const query = new URLSearchParams();
    if (params?.status)
        query.set('status', params.status);
    if (params?.limit)
        query.set('limit', params.limit.toString());
    const qs = query.toString();
    return request('GET', `/me/auctions${qs ? `?${qs}` : ''}`);
}
async function getMyBids(params) {
    const query = new URLSearchParams();
    if (params?.limit)
        query.set('limit', params.limit.toString());
    const qs = query.toString();
    return request('GET', `/me/bids${qs ? `?${qs}` : ''}`);
}
async function getWalletInfo(tokenAddress) {
    const query = new URLSearchParams();
    if (tokenAddress)
        query.set('token', tokenAddress);
    const qs = query.toString();
    return request('GET', `/me/wallet${qs ? `?${qs}` : ''}`);
}
// ─── Write Operations ───
async function createAuction(params) {
    return request('POST', '/auctions/create', params);
}
async function placeBid(blockchainAuctionId, amount) {
    return request('POST', `/auctions/${blockchainAuctionId}/bid`, { amount });
}
//# sourceMappingURL=client.js.map