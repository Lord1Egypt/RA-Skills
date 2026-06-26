#!/usr/bin/env node

import fs from 'fs';
import path from 'path';

// 读取环境变量或.env文件
function getApiKey() {
    // 首先尝试环境变量
    if (process.env.ALI_IQS_API_KEY) {
        return process.env.ALI_IQS_API_KEY;
    }
    
    // 然后尝试读取.env文件
    const envPath = path.join(process.cwd(), '.env');
    if (fs.existsSync(envPath)) {
        const envContent = fs.readFileSync(envPath, 'utf8');
        const match = envContent.match(/ALI_IQS_API_KEY\s*=\s*(.+)/);
        if (match) {
            return match[1].trim();
        }
    }
    
    throw new Error('ALI_IQS_API_KEY not found in environment or .env file');
}

async function search(query) {
    const apiKey = getApiKey();
    const url = 'https://cloud-iqs.aliyuncs.com/search/unified';
    
    const requestBody = {
        query: query,
        engineType: "Generic",
        contents: {
            mainText: true,
            markdownText: false,
            summary: false,
            rerankScore: true
        }
    };
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${await response.text()}`);
        }
        
        const data = await response.json();
        console.log('=== 完整原始响应 ===');
        console.log(JSON.stringify(data, null, 2));
        console.log('=== 响应结束 ===');
        
        const pageItems = data.pageItems || [];
        console.log(`API返回的总结果数: ${pageItems.length}`);
        
        const results = [];
        let position = 1;
        for (const item of pageItems) {
            const score = item.rerankScore || 0;
            console.log(`结果 ${position}: 分数=${score}, 链接=${item.link || '无'}`);
            // 只保留非空链接且分数超过0.5的结果
            if (item.link && score > 0.5) {
                results.push({
                    title: item.title || '',
                    url: item.link,
                    description: item.mainText || '',
                    score: score,
                    position: position++
                });
            }
        }
        
        console.log(`过滤后符合条件的结果数: ${results.length}`);
        
    } catch (error) {
        console.error('Search error:', error.message);
        process.exit(1);
    }
}

// 获取查询参数
const query = process.argv[2];
if (!query) {
    console.error('Usage: node debug-search.mjs "search query"');
    process.exit(1);
}

search(query);