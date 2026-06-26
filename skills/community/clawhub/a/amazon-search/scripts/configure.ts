#!/usr/bin/env bun
/**
 * Amazon Search 配置工具
 * 用于输出环境变量设置命令、清理 Cache 等
 */

import { clearCache } from './amazon_search';
import * as fs from 'fs';
import * as path from 'path';


function showProxy(): void {
    const proxy = process.env.T2P_PROXY;
    if (proxy) {
        console.log(`当前 Proxy: ${proxy}`);
    } else {
        console.log('未设置 T2P_PROXY 环境变量');
    }
}

function printProxyCommand(proxyUrl: string): void {
    console.log('\n请复制以下命令设置 Proxy:');
    console.log('\x1b[32m%s\x1b[0m', `export T2P_PROXY="${proxyUrl}"`);
}

// Cache 管理
function clearKeywordCache(keyword: string): void {
    const deleted = clearCache(keyword);
    if (deleted) {
        console.log(`已清空 "${keyword}" 的缓存`);
    } else {
        console.log(`"${keyword}" 没有缓存文件`);
    }
}

function clearAllCache(): void {
    const cacheDir = path.join(__dirname, '..', 'resultscache');
    if (!fs.existsSync(cacheDir)) {
        console.log('缓存目录不存在');
        return;
    }

    const files = fs.readdirSync(cacheDir).filter(f => f.endsWith('_cache.md'));
    let count = 0;

    files.forEach(file => {
        fs.unlinkSync(path.join(cacheDir, file));
        count++;
    });

    console.log(`已清除 ${count} 个缓存文件`);
}

function listCache(): void {
    const cacheDir = path.join(__dirname, '..', 'resultscache');
    if (!fs.existsSync(cacheDir)) {
        console.log('缓存目录不存在');
        return;
    }

    const files = fs.readdirSync(cacheDir).filter(f => f.endsWith('_cache.md'));
    if (files.length === 0) {
        console.log('没有缓存文件');
        return;
    }

    console.log('缓存文件列表:');
    files.forEach(file => {
        const filepath = path.join(cacheDir, file);
        const stats = fs.statSync(filepath);
        const lines = fs.readFileSync(filepath, 'utf-8').split('\n').filter(l => l.trim()).length;
        console.log(`  - ${file} (${lines} 条记录, ${(stats.size / 1024).toFixed(2)} KB)`);
    });
}

// 显示帮助
function showHelp(): void {
    console.log(`
Amazon Search 配置工具

用法:
  bun run configure.ts [命令] [参数]

命令:
  proxy [value]           输出设置 Proxy 的环境变量命令
  proxy --show            查看当前环境变量中的 Proxy

  listcache               列出所有缓存文件
  clearcache [keyword]    清空指定关键词的缓存
  clearcache --all        清空所有缓存

  help                    显示此帮助信息

示例:
  bun run configure.ts proxy http://127.0.0.1:7890
  bun run configure.ts clearcache "shirt"
  bun run configure.ts clearcache --all
  bun run configure.ts listcache

注意:
  Proxy 只从环境变量读取，不会保存到文件。
  请使用本工具生成的 export 命令设置环境变量。
`);
}

// 主函数
function main(): void {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        showHelp();
        return;
    }

    const command = args[0];

    switch (command) {
        case 'proxy':
            if (args[1] === '--show') {
                showProxy();
            } else if (args[1]) {
                printProxyCommand(args[1]);
            } else {
                console.log('请提供 Proxy 地址或使用 --show 选项');
            }
            break;

        case 'listcache':
            listCache();
            break;

        case 'clearcache':
            if (args[1] === '--all') {
                clearAllCache();
            } else if (args[1]) {
                clearKeywordCache(args[1]);
            } else {
                console.log('请提供关键词或使用 --all 选项');
            }
            break;

        case 'help':
        default:
            showHelp();
            break;
    }
}

main();
