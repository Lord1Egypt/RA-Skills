const fs = require('fs');
const https = require('https');

// 配置
const FUND_DOC_TOKEN = 'J9BndSQkHoguODx96PtcNslnnsc';
const FEISHU_APP_ID = 'cli_a9f34580c5badbd9';
const FEISHU_APP_SECRET = 'DDxM8UV6Dn5OO0Il8MxNGbGmX1PEiLuJ';

// 获取access_token
function getAccessToken() {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify({
            app_id: FEISHU_APP_ID,
            app_secret: FEISHU_APP_SECRET
        });
        
        const options = {
            hostname: 'open.feishu.cn',
            path: '/open-apis/auth/v3/tenant_access_token/internal',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        };
        
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                try {
                    const result = JSON.parse(body);
                    resolve(result.tenant_access_token);
                } catch (e) {
                    reject(e);
                }
            });
        });
        
        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

// 解析命令行参数获取基金数据
function parseFundData(args) {
    const input = args.join(' ');
    
    // 提取日期
    const dateMatch = input.match(/(\d{4}-\d{2}-\d{2})/);
    const date = dateMatch ? dateMatch[1] : new Date().toISOString().split('T')[0];
    
    // 提取今日收益
    const profitMatch = input.match(/今日收益变化:\s*([+-]?[\d,]+\.?\d*)\s*元/);
    const todayProfit = profitMatch ? profitMatch[1] : '0';
    
    // 提取持仓总收益
    const totalProfitMatch = input.match(/持仓总收益:\s*([+-]?[\d,]+\.?\d*)\s*元/);
    const totalProfit = totalProfitMatch ? totalProfitMatch[1] : '0';
    
    // 提取总本金
    const principalMatch = input.match(/总本金:\s*([\d,]+\.?\d*)\s*元/);
    const principal = principalMatch ? principalMatch[1] : '0';
    
    // 提取总市值
    const marketMatch = input.match(/总市值:\s*([\d,]+\.?\d*)\s*元/);
    const market = marketMatch ? marketMatch[1] : '0';
    
    // 提取总收益率
    const returnMatch = input.match(/总收益率[^\d]*([+-]?[\d,]+\.?\d*)%/);
    const totalReturn = returnMatch ? returnMatch[1] : '0';
    
    // 提取上涨/下跌基金数量
    const upMatch = input.match(/上涨.*?(\d+).*?只/);
    const downMatch = input.match(/下跌.*?(\d+).*?只/);
    const upCount = upMatch ? upMatch[1] : '0';
    const downCount = downMatch ? downMatch[1] : '0';
    
    // 提取最佳/最差
    const bestMatch = input.match(/今日最佳[:\s]+([^\n，,]+)/);
    const worstMatch = input.match(/今日最差[:\s]+([^\n，,]+)/);
    const best = bestMatch ? bestMatch[1].trim() : '';
    const worst = worstMatch ? worstMatch[1].trim() : '';
    
    return { date, todayProfit, totalProfit, principal, market, totalReturn, upCount, downCount, best, worst, raw: input };
}

// 更新飞书文档 - 在末尾新增
async function updateFeishuDoc(token, docToken, content) {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify({
            doc_token: docToken,
            block: {
                block_type: 17,  // markdown类型
                markdown: {
                    content: content.markdown
                }
            }
        });
        
        const options = {
            hostname: 'open.feishu.cn',
            path: `/open-apis/docx/v1/documents/${docToken}/blocks/append`,
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        };
        
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                console.log('Feishu append response:', body.substring(0, 200));
                resolve(body);
            });
        });
        
        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

async function main() {
    try {
        const fundData = parseFundData(process.argv.slice(2));
        
        console.log('Parsed Fund Data:', JSON.stringify({
            date: fundData.date,
            todayProfit: fundData.todayProfit,
            totalProfit: fundData.totalProfit,
            upCount: fundData.upCount,
            downCount: fundData.downCount
        }, null, 2));
        
        // 获取token
        const token = await getAccessToken();
        console.log('Got Feishu token');
        
        // 构建文档内容 - Markdown格式用于追加
        const content = {
            title: `基金投资记录 - ${fundData.date}`,
            markdown: `
---
## 📊 ${fundData.date} 基金汇总

| 指标 | 数值 |
|------|------|
| 总本金 | ${fundData.principal} 元 |
| 总市值 | ${fundData.market} 元 |
| 持仓总收益 | ${fundData.totalProfit} 元 |
| 今日收益 | ${fundData.todayProfit} 元 |
| 总收益率 | ${fundData.totalReturn}% |

### 📈 上涨基金 (${fundData.upCount}只)
${fundData.best ? `🏆 最佳: ${fundData.best}` : ''}

### 📉 下跌基金 (${fundData.downCount}只)
${fundData.worst ? `📉 最差: ${fundData.worst}` : ''}

---
*更新于 ${fundData.date}*
`,
            date: fundData.date,
            todayProfit: fundData.todayProfit,
            totalProfit: fundData.totalProfit,
            principal: fundData.principal,
            market: fundData.market,
            totalReturn: fundData.totalReturn,
            upCount: fundData.upCount,
            downCount: fundData.downCount,
            best: fundData.best,
            worst: fundData.worst
        };
        
        console.log('Updating Feishu doc with:', JSON.stringify(content, null, 2));
        
        // 调用飞书API追加内容
        await updateFeishuDoc(token, FUND_DOC_TOKEN, content);
        
        console.log('✅ Fund Feishu doc updated with append!');
        
    } catch (e) {
        console.error('Error:', e.message);
    }
}

main();
