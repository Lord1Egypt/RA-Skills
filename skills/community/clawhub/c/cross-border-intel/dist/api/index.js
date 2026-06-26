/**
 * API client for backend capability endpoints
 */
import { getIntelApiUrl, getIntelApiToken } from '../core/config.js';
/**
 * Make an API request
 */
async function apiRequest(method, path, body) {
    const url = `${getIntelApiUrl()}${path}`;
    const token = getIntelApiToken();
    const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
    };
    const options = {
        method,
        headers,
    };
    if (body) {
        options.body = JSON.stringify(body);
    }
    try {
        const response = await fetch(url, options);
        const data = await response.json();
        if (!data.success) {
            throw new Error(data.message || 'Request failed');
        }
        return data;
    }
    catch (error) {
        if (error.message === 'Request failed') {
            throw error;
        }
        throw new Error(`API request failed: ${error.message}`);
    }
}
/**
 * Make a GET request
 */
export async function apiGet(path) {
    return apiRequest('GET', path);
}
/**
 * Make a POST request
 */
export async function apiPost(path, body) {
    return apiRequest('POST', path, body);
}
/**
 * Make a PUT request
 */
export async function apiPut(path, body) {
    return apiRequest('PUT', path, body);
}
/**
 * Make a DELETE request
 */
export async function apiDelete(path) {
    return apiRequest('DELETE', path);
}
/**
 * Fetch Amazon product data from backend
 */
export async function fetchAmazonProduct(asin, domain = 'com') {
    const response = await apiPost('/intel/capabilities/amazon/product', { asin, domain });
    if (!response.data?.product) {
        throw new Error('No product data in response');
    }
    return response.data.product;
}
/**
 * Search TikTok videos from backend
 */
export async function searchTiktokVideos(keyword, count = 20, sortType = 0) {
    const response = await apiPost('/intel/capabilities/tiktok/search', { keyword, count, sortType });
    return response.data?.videos || [];
}
