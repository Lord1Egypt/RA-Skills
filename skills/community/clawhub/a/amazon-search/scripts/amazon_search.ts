import * as cheerio from 'cheerio';
import * as fs from 'fs';
import * as path from 'path';
import {cacheImage} from '@t2p/image-cache';
import { execSync } from "child_process";

// 使用 Playwright 直接搜索（通过子进程）
async function searchWithPlaywright(keyword: string, proxy?: string, pages: number = 1): Promise<ItemAmazon[]> {
    console.log(`Using Playwright to search Amazon...`);

    let cmd = `npm run psearch -- "${keyword}" --pages=${pages}`;
    if (proxy) {
        cmd += ` --proxy=${proxy}`;
    }

    const output = execSync(cmd, {
        encoding: "utf-8",
        timeout: 300000, // 5分钟超时
        cwd: __dirname
    });

    // 从输出中提取 JSON 结果部分
    const resultsStart = output.indexOf('=== Results ===');
    const totalEnd = output.lastIndexOf('Total: ');

    if (resultsStart !== -1 && totalEnd !== -1) {
        // 提取 Results 标记后的内容
        const jsonStart = output.indexOf('[', resultsStart);
        const jsonEnd = output.lastIndexOf(']', totalEnd);

        if (jsonStart !== -1 && jsonEnd !== -1 && jsonEnd > jsonStart) {
            const jsonStr = output.substring(jsonStart, jsonEnd + 1);
            try {
                return JSON.parse(jsonStr);
            } catch (e) {
                console.error('Failed to parse results:', e);
                return [];
            }
        }
    }
    return [];
}

export interface ItemAmazon {
    id_?: string;
    uuid?: string;
    original_image_url?: string;
    title?: string;
    item_page?: string;
    rating?: number;
    review_count?: number;
    price?: string;
    description?: string;
}

export function parseAmazonList(html: string): ItemAmazon[] {
    const $ = cheerio.load(html);

    const listItems = $('[role="listitem"]');
    const result: ItemAmazon[] = [];

    listItems.each((_, el) => {
        const item = parseItem($, el);
        if (item) result.push(item);
    });

    return result;
}

function parseItem($: cheerio.CheerioAPI, el: any): ItemAmazon | null {
    const e = $(el);
    const item: ItemAmazon = {};

    item.id_ = e.attr('data-asin') || undefined;

    let data_uuid = e.attr('data-uuid');
    if (!data_uuid) data_uuid = e.attr('id') || undefined;
    item.uuid = data_uuid;

    // 图片
    const imageEl = e.find('img.s-image').first();
    if (!imageEl.length) {
        return null;
    }

    const srcset = imageEl.attr('srcset');
    if (srcset) {
        const entries = srcset.split(',');
        const lastEntry = entries[entries.length - 1].trim();
        const parts = lastEntry.split(/\s+/);
        item.original_image_url = parts[0];
    }

    // 标题
    let h2 = e.find('h2').first();
    if (h2.length) {
        item.title = h2.text();
    } else {
        const span = e.find('h2 > span').first();
        if (span.length) item.title = span.text();
    }

    // 商品链接
    let linkEl =
        e.find('a.a-link-normal.s-no-outline').first() ||
        e.find('a.a-link-normal.s-line-clamp-4.s-link-style.a-text-normal').first() ||
        e.find('a.a-link-normal.s-underline-text.s-underline-link-text.null.s-link-style').first() ||
        e.find('a.a-link-normal.s-no-hover.s-underline-text.s-underline-link-text.s-link-style a-text-normal').first();

    if (linkEl && linkEl.length) {
        const href = linkEl.attr('href') || undefined;
        if (href) item.item_page = "https://www.amazon.com" + href;
    }

    // 评分
    const ratingEl = e.find("div[data-cy='reviews-block'] span.a-size-small.a-color-base").first();
    if (ratingEl.length) {
        item.rating = parseFloat(ratingEl.text().trim());
    } else {
        const popoverEl = e.find('a.a-popover-trigger.a-declarative').first();
        if (popoverEl.length) {
            const val = popoverEl.text().split(' ')[0];
            item.rating = parseFloat(val);
        }
    }

    // 评分人数
    const ratingsEl = e.find('span.a-size-mini.puis-normal-weight-text.s-underline-text').first();
    if (ratingsEl.length) {
        const text = ratingsEl.text().replace(/[^0-9.]/g, '');
        if (ratingsEl.text().includes('万')) {
            item.review_count = Math.floor(parseFloat(text) * 10000);
        } else if (ratingsEl.text().includes('K')) {
            item.review_count = Math.floor(parseFloat(text) * 1000);
        } else {
            item.review_count = parseInt(text);
        }
    } else {
        const fallbackEl = e.find('span.a-size-base.s-underline-text').first();
        if (fallbackEl.length) {
            item.review_count = parseInt(
                fallbackEl.text().replace(/[^0-9.]/g, '')
            );
        }
    }

    // 价格
    const priceEl = e.find('span.a-offscreen').first();
    if (priceEl.length) {
        item.price = priceEl.text();
    } else {
        const secondaryPriceEl = e.find('.a-row.a-size-base.a-color-secondary span.a-color-base').first();
        if (secondaryPriceEl.length) {
            item.price = secondaryPriceEl.text();
        }
    }

    // 描述
    let descEl = e.find('h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal').first();
    if (descEl.length) {
        item.description = descEl.text().trim();
    } else {
        descEl = e.find('a.s-line-clamp-2 > h2 > span').first();
        if (descEl.length) {
            item.description = descEl.text().trim();
        }
    }

    return item;
}

async function run_local_scraper(keyword: string,
                                 options?: {
                                     timeoutMs?: number;
                                     incremental?: boolean;
                                     price_min?: number,
                                     price_max?: number,
                                     pages?: number;
                                     numOfProducts?: number;
                                     proxy?: string;
                                     download?: boolean;
                                 }): Promise<{ items: ItemAmazon[]; newItems: ItemAmazon[]; totalCached: number; }> {

    const incremental = options?.incremental ?? false;
    const numOfProducts = options?.numOfProducts;
    const pages = options?.pages ?? 1;

    // 使用 Playwright 直接搜索（通过子进程）
    const allItems = await searchWithPlaywright(keyword, options?.proxy, pages);

    // 应用产品数量限制
    let limitedItems = allItems;
    if (numOfProducts && allItems.length > numOfProducts) {
        limitedItems = allItems.slice(0, numOfProducts);
        console.log(`Limited to ${numOfProducts} products`);
    }

    // Remove duplicates by ASIN
    const uniqueItems = Array.from(
        new Map(limitedItems.map(item => [item.id_, item])).values()
    );

    // 加载已缓存的 ID
    const cachedIds = loadCacheIds(keyword);
    const totalCached = cachedIds.size;
    // 找出新的结果
    const newItems = uniqueItems.filter(item => !cachedIds.has(item.id_));
    // 将所有新 ID 追加到 cache
    const newIds = newItems.map(item => item.id_).filter((id): id is string => !!id);
    appendToCache(keyword, newIds);
    return {items: incremental ? newItems : uniqueItems, newItems, totalCached};
}

// 将搜索词转换为安全的文件名
function sanitizeKeyword(keyword: string): string {
    // 1. 移除或替换危险字符，保留字母、数字、中文、常用分隔符
    // 保留: 字母、数字、中文、空格、连字符、下划线
    let sanitized = keyword
        .replace(/[\/\\:*?"<>|]/g, '')  // 移除 Windows/Unix 不允许的字符
        .replace(/[^a-zA-Z0-9\u4e00-\u9fa5\s-_]/g, '_')  // 其他特殊字符替换为下划线
        .trim();

    // 2. 将多个连续空白或下划线替换为单个下划线
    sanitized = sanitized.replace(/[\s_]+/g, '_');

    // 3. 移除首尾下划线
    sanitized = sanitized.replace(/^_+|_+$/g, '');

    // 4. 限制长度 (最大 100 字符，为时间戳和结果数留空间)
    // 文件名总长度建议不超过 255 字符
    const maxLength = 100;
    if (sanitized.length > maxLength) {
        sanitized = sanitized.substring(0, maxLength);
        // 确保截断后不以 _ 结尾
        sanitized = sanitized.replace(/_+$/g, '');
    }

    // 5. 如果处理后为空，使用默认名称
    if (!sanitized) {
        sanitized = 'search';
    }

    return sanitized;
}

// 清空指定关键词的缓存
export function clearCache(keyword: string): boolean {
    const sanitizedKeyword = sanitizeKeyword(keyword);
    const cacheDir = path.join(__dirname, '..', 'resultscache');
    const cacheFile = path.join(cacheDir, `${sanitizedKeyword}_cache.md`);

    if (fs.existsSync(cacheFile)) {
        fs.unlinkSync(cacheFile);
        return true;
    }
    return false;
}

export function setProxy(proxyUrl: string): void {
    process.env.T2P_PROXY = proxyUrl;
}

// 获取 T2P_PROXY 环境变量
export function getProxy(): string | undefined {
    return process.env.T2P_PROXY;
}

// 读取 cache 文件中的 ID 集合
function loadCacheIds(keyword: string): Set<string> {
    const sanitizedKeyword = sanitizeKeyword(keyword);
    const cacheDir = path.join(__dirname, '..', 'resultscache');
    const cacheFile = path.join(cacheDir, `${sanitizedKeyword}_cache.md`);

    const ids = new Set<string>();
    if (fs.existsSync(cacheFile)) {
        const content = fs.readFileSync(cacheFile, 'utf-8');
        content.split('\n').forEach(line => {
            const trimmed = line.trim();
            if (trimmed) {
                ids.add(trimmed);
            }
        });
    }
    return ids;
}

// 将新的 ID 追加到 cache 文件
function appendToCache(keyword: string, newIds: string[]): void {
    if (newIds.length === 0) return;

    const sanitizedKeyword = sanitizeKeyword(keyword);
    const cacheDir = path.join(__dirname, '..', 'resultscache');
    if (!fs.existsSync(cacheDir)) {
        fs.mkdirSync(cacheDir, {recursive: true});
    }
    const cacheFile = path.join(cacheDir, `${sanitizedKeyword}_cache.md`);

    const content = newIds.join('\n') + '\n';
    fs.appendFileSync(cacheFile, content, 'utf-8');
}

// 保存搜索结果到 results 目录
function saveResults(keyword: string, items: ItemAmazon[], outputDir?: string): string {
    const sanitizedKeyword = sanitizeKeyword(keyword);
    const resultsDir = outputDir ? path.resolve(outputDir) : path.join(__dirname, '..', 'results');
    if (!fs.existsSync(resultsDir)) {
        fs.mkdirSync(resultsDir, {recursive: true});
    }

    const timestamp = Date.now();
    const filename = `${sanitizedKeyword}_${timestamp}_${items.length}.json`;
    const filepath = path.join(resultsDir, filename);

    const data = {
        keyword: keyword,
        timestamp: new Date().toISOString(),
        count: items.length,
        items: items
    };

    fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf-8');
    return filepath;
}


(async () => {
    // 只在直接运行此文件时执行
    if (!import.meta.main) return;

    // 解析命令行参数
    const args = process.argv.slice(2);
    const incremental = args.includes('--incremental');
    const clearCacheFlag = args.includes('--clear-cache');
    const download = args.includes('--download');

    // 解析 --pages 参数
    let pages = 1;
    const pagesArg = args.find(arg => arg.startsWith('--pages='));
    if (pagesArg) {
        const pagesValue = parseInt(pagesArg.split('=')[1], 10);
        if (!isNaN(pagesValue) && pagesValue > 0) {
            pages = pagesValue;
        }
    }

    // 解析 --num-products 参数
    let numOfProducts: number | undefined;
    const numProductsArg = args.find(arg => arg.startsWith('--num-products='));
    if (numProductsArg) {
        const numValue = parseInt(numProductsArg.split('=')[1], 10);
        if (!isNaN(numValue) && numValue > 0) {
            numOfProducts = numValue;
        }
    }

    // 解析 --output 参数
    let outputDir: string | undefined;
    const outputArg = args.find(arg => arg.startsWith('--output='));
    if (outputArg) {
        outputDir = outputArg.split('=')[1];
    }

    // 移除标志参数，获取位置参数
    const positionalArgs = args.filter(arg =>
        !['--incremental', '--clear-cache', '--download'].includes(arg) &&
        !arg.startsWith('--pages=') &&
        !arg.startsWith('--num-products=') &&
        !arg.startsWith('--output=')
    );

    const keyword = positionalArgs[0] || "shirt";

    // 处理清空缓存
    if (clearCacheFlag) {
        const deleted = clearCache(keyword);
        if (deleted) {
            console.log(`已清空 "${keyword}" 的缓存`);
        } else {
            console.log(`"${keyword}" 没有缓存文件`);
        }
        return;
    }

    // 从环境变量获取 proxy
    const proxy = process.env.T2P_PROXY;

    if (incremental) {
        console.log("增量模式: 只输出新的结果");
    }

    if (pages > 1) {
        console.log(`多页模式: 最多抓取 ${pages} 页`);
    }

    if (numOfProducts) {
        console.log(`商品限制: 最多 ${numOfProducts} 个商品`);
    }

    if (download) {
        console.log("下载模式: 搜索后自动下载图片");
    }

    if (outputDir) {
        console.log(`输出目录: ${outputDir}`);
    }

    try {
        const {items, newItems, totalCached} = await run_local_scraper(keyword, {
            proxy: proxy || undefined,
            incremental: incremental,
            pages: pages,
            numOfProducts: numOfProducts,
            download: download
        });

        console.log(`缓存中原已有: ${totalCached} 条`);
        console.log(`抓取结果总数: ${items.length}`);
        console.log(`结果新增数量: ${newItems.length}`);

        // 保存结果到文件
        if (items.length > 0) {
            const filepath = saveResults(keyword, items, outputDir);
            console.log(`结果已保存到: ${filepath}`);

            // 如果开启下载模式，下载图片
            if (download) {
                console.log(`\n开始下载 ${items.length} 张图片...`);
                let downloaded = 0;
                let cached = 0;
                let failed = 0;
                let skipped = 0;

                for (const item of items) {
                    if (!item.original_image_url) {
                        console.log(`跳过无图片URL的商品: ${item.id_ || item.uuid}`);
                        skipped++;
                        continue;
                    }
                    try {
                        const result = await cacheImage(item.original_image_url);
                        if (result.fromCache) {
                            cached++;
                        } else {
                            downloaded++;
                        }
                        console.log(`✓ ${item.id_ || item.uuid} -> ${result.localPath}`);
                    } catch (err) {
                        console.error(`✗ ${item.id_ || item.uuid} 下载失败:`, err);
                        failed++;
                    }
                }

                console.log(`\n下载完成: ${downloaded} 张新下载, ${cached} 张来自缓存, ${failed} 张失败, ${skipped} 张跳过`);
            }
        }

    } catch (err) {
        console.error("运行失败:", err);
    }
})();
