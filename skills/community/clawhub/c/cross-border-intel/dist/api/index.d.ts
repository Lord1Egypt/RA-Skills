/**
 * API client for backend capability endpoints
 */
import type { ApiResponse, AmazonProduct, TikTokVideo } from '../core/types.js';
/**
 * Make a GET request
 */
export declare function apiGet<T>(path: string): Promise<ApiResponse<T>>;
/**
 * Make a POST request
 */
export declare function apiPost<T>(path: string, body?: unknown): Promise<ApiResponse<T>>;
/**
 * Make a PUT request
 */
export declare function apiPut<T>(path: string, body?: unknown): Promise<ApiResponse<T>>;
/**
 * Make a DELETE request
 */
export declare function apiDelete<T>(path: string): Promise<ApiResponse<T>>;
/**
 * Fetch Amazon product data from backend
 */
export declare function fetchAmazonProduct(asin: string, domain?: string): Promise<AmazonProduct>;
/**
 * Search TikTok videos from backend
 */
export declare function searchTiktokVideos(keyword: string, count?: number, sortType?: number): Promise<TikTokVideo[]>;
