/**
 * HTTP client for the Auction House API v1
 */
interface ApiResponse<T = any> {
    ok: boolean;
    status: number;
    data: T;
}
export declare function listAuctions(params?: {
    status?: string;
    limit?: number;
    offset?: number;
}): Promise<ApiResponse>;
export declare function searchAuctions(params: {
    search?: string;
    currency?: string;
    token?: string;
    minPrice?: number;
    maxPrice?: number;
    createdAfter?: string;
    endingWithin?: number;
    sort?: string;
    status?: string;
    limit?: number;
}): Promise<ApiResponse>;
export declare function getAuction(blockchainAuctionId: string): Promise<ApiResponse>;
export declare function getMyAuctions(params?: {
    status?: string;
    limit?: number;
}): Promise<ApiResponse>;
export declare function getMyBids(params?: {
    limit?: number;
}): Promise<ApiResponse>;
export declare function getWalletInfo(tokenAddress?: string): Promise<ApiResponse>;
export declare function createAuction(params: {
    auctionName: string;
    tokenAddress: string;
    minimumBid: number;
    durationHours: number;
    description?: string;
}): Promise<ApiResponse>;
export declare function placeBid(blockchainAuctionId: string, amount: number): Promise<ApiResponse>;
export {};
//# sourceMappingURL=client.d.ts.map