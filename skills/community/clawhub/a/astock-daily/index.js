#!/usr/bin/env node
/**
 * A 股每日精选股票技能
 * 获取新股发行信息和 20 元以下精选股票，发送邮件
 */

const https = require('https');
const http = require('http');

// 配置
const CONFIG = {
  email: '8@batype.com',
  priceLimit: 20, // 价格上限（元）
  maxStocks: 50,  // 最多返回的股票数量
};

/**
 * HTTP GET 请求
 */
function httpGet(url, timeout = 15000) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    const req = client.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    });
    req.on('error', reject);
    req.setTimeout(timeout, () => {
      req.destroy();
      reject(new Error(`Request timeout after ${timeout}ms`));
    });
  });
}

/**
 * 获取新股发行数据（东方财富 API）
 */
async function getNewStocks() {
  try {
    // 东方财富新股申购数据
    const url = 'http://data.eastmoney.com/xg/xg/default.aspx';
    const apiData = await httpGet(
      'http://datacenter-web.eastmoney.com/api/data/v1/get?' + 
      'sortColumns=APPLY_DATE,SECURITY_CODE&sortTypes=-1,-1&' +
      'pageSize=20&pageNumber=1&reportName=RPTA_APP_IPOAPPLY&' +
      'columns=SECURITY_CODE,SECURITY_NAME,APPLY_DATE,ISSUE_PRICE,LISTING_DATE&' +
      'source=WEB&client=WEB'
    );
    
    if (apiData && apiData.result && apiData.result.data) {
      return apiData.result.data.map(item => ({
        code: item.SECURITY_CODE,
        name: item.SECURITY_NAME,
        applyDate: item.APPLY_DATE,
        issuePrice: item.ISSUE_PRICE,
        listingDate: item.LISTING_DATE,
      }));
    }
    return [];
  } catch (error) {
    console.error('获取新股数据失败:', error.message);
    return [];
  }
}

/**
 * 获取 A 股股票列表（新浪财经 API）
 * 筛选 20 元以下的股票
 */
async function getLowPriceStocks() {
  try {
    // 使用新浪财经 API 获取 A 股数据（返回 GBK 编码的 JSON）
    const apiUrl = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?' +
      'page=1&num=500&sort=symbol&asc=1&node=hs_a&symbol=&_s_r_a=page';
    
    const data = await httpGet(apiUrl);
    
    if (!data || !Array.isArray(data)) {
      console.log('股票 API 返回数据格式异常');
      return [];
    }
    
    console.log(`API 返回 ${data.length} 只股票`);
    
    // 筛选 20 元以下的股票
    const lowPriceStocks = data.filter(stock => {
      const price = parseFloat(stock.trade);
      return price !== null && price !== undefined && price > 0 && price <= CONFIG.priceLimit;
    });
    
    console.log(`筛选后 ${lowPriceStocks.length} 只股票（<=¥${CONFIG.priceLimit}）`);
    
    // 按成交量排序，取前 N 只
    lowPriceStocks.sort((a, b) => (parseInt(b.volume) || 0) - (parseInt(a.volume) || 0)); // 按成交量降序
    
    return lowPriceStocks.slice(0, CONFIG.maxStocks).map(stock => ({
      code: stock.code,
      name: stock.name,
      price: parseFloat(stock.trade),
      changePercent: parseFloat(stock.changepercent),
      volume: parseInt(stock.volume),
      turnover: parseFloat(stock.amount) / 10000, // 转为万
      marketCap: parseFloat(stock.mktcap) / 10000, // 转为亿
    }));
  } catch (error) {
    console.error('获取股票数据失败:', error.message);
    return [];
  }
}

/**
 * 格式化数字（添加千分位）
 */
function formatNumber(num) {
  if (num === null || num === undefined) return '-';
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * 生成邮件内容
 */
function generateEmailContent(newStocks, lowPriceStocks) {
  const date = new Date().toLocaleDateString('zh-CN');
  
  let html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 800px; margin: 0 auto; padding: 20px; }
    h1 { color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; }
    h2 { color: #333; margin-top: 30px; }
    table { width: 100%; border-collapse: collapse; margin: 15px 0; }
    th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background-color: #f5f5f5; font-weight: bold; }
    tr:hover { background-color: #f9f9f9; }
    .price { color: #e74c3c; font-weight: bold; }
    .positive { color: #e74c3c; }
    .negative { color: #27ae60; }
    .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>📈 A 股每日精选</h1>
    <p>日期：${date}</p>
    
    <h2>🆕 新股发行</h2>
  `;
  
  if (newStocks.length > 0) {
    html += `
    <table>
      <thead>
        <tr>
          <th>代码</th>
          <th>名称</th>
          <th>申购日期</th>
          <th>发行价</th>
          <th>上市日期</th>
        </tr>
      </thead>
      <tbody>
    `;
    
    newStocks.forEach(stock => {
      html += `
        <tr>
          <td>${stock.code}</td>
          <td>${stock.name}</td>
          <td>${stock.applyDate || '-'}</td>
          <td class="price">¥${stock.issuePrice || '-'}</td>
          <td>${stock.listingDate || '-'}</td>
        </tr>
      `;
    });
    
    html += `</tbody></table>`;
  } else {
    html += `<p>近期无新股发行数据</p>`;
  }
  
  html += `
    <h2>💰 ${CONFIG.priceLimit}元以下精选股票</h2>
    <p>按成交量排序，共 ${lowPriceStocks.length} 只</p>
  `;
  
  if (lowPriceStocks.length > 0) {
    html += `
    <table>
      <thead>
        <tr>
          <th>代码</th>
          <th>名称</th>
          <th>现价</th>
          <th>涨跌幅</th>
          <th>成交量 (手)</th>
          <th>成交额 (万)</th>
          <th>总市值 (亿)</th>
        </tr>
      </thead>
      <tbody>
    `;
    
    lowPriceStocks.forEach(stock => {
      const changeClass = stock.changePercent >= 0 ? 'positive' : 'negative';
      const changeSign = stock.changePercent >= 0 ? '+' : '';
      html += `
        <tr>
          <td>${stock.code}</td>
          <td>${stock.name}</td>
          <td class="price">¥${stock.price.toFixed(2)}</td>
          <td class="${changeClass}">${changeSign}${stock.changePercent.toFixed(2)}%</td>
          <td>${formatNumber(stock.volume)}</td>
          <td>${formatNumber((stock.turnover / 10000).toFixed(2))}</td>
          <td>${formatNumber((stock.marketCap / 100000000).toFixed(2))}</td>
        </tr>
      `;
    });
    
    html += `</tbody></table>`;
  } else {
    html += `<p>暂无符合条件的股票数据</p>`;
  }
  
  html += `
    <div class="footer">
      <p>⚠️ 免责声明：以上数据仅供参考，不构成投资建议。股市有风险，投资需谨慎。</p>
      <p>数据来源：东方财富网、新浪财经</p>
    </div>
  </div>
</body>
</html>
  `;
  
  return html;
}

/**
 * 发送邮件（支持多种方式）
 */
async function sendEmail(htmlContent) {
  const { exec } = require('child_process');
  const fs = require('fs');
  const path = require('path');
  const nodemailer = require('nodemailer');
  
  const subject = `📈 A 股每日精选 - ${new Date().toLocaleDateString('zh-CN')}`;
  
  // 方法 1: 使用 nodemailer（需要配置 SMTP）- 推荐
  try {
    const smtpConfig = process.env.SMTP_CONFIG;
    if (smtpConfig) {
      console.log('正在尝试 SMTP 发送...');
      const config = JSON.parse(smtpConfig);
      console.log({
        host: config.host,
        port: parseInt(config.port) || 587,
        secure: config.secure || false,
        auth: {
          user: config.user,
          pass: config.pass,
        },
      });
      // 添加 TLS 配置避免证书问题
      const tlsConfig = config.tls || (config.secure ? { rejectUnauthorized: false } : undefined);
      
      const transporter = nodemailer.createTransport({
        host: config.host,
        port: parseInt(config.port) || 587,
        secure: config.secure || false,
        tls: tlsConfig,
        auth: {
          user: config.user,
          pass: config.pass,
        },
        connectionTimeout: 10000, // 连接超时 10 秒
        socketTimeout: 10000,     //  socket 超时 10 秒
      });
      
      // 测试连接（带超时）
      await Promise.race([
        transporter.verify(),
        new Promise((_, reject) => setTimeout(() => reject(new Error('SMTP verify timeout')), 15000))
      ]);
      console.log('SMTP 连接成功！');
      
      // 发送邮件（带超时）
      await Promise.race([
        transporter.sendMail({
          from: config.from || config.user,
          to: CONFIG.email,
          subject: subject,
          html: htmlContent,
        }),
        new Promise((_, reject) => setTimeout(() => reject(new Error('SMTP sendMail timeout')), 30000))
      ]);
      
      console.log('✅ 邮件已发送（SMTP）');
      return true;
    }
  } catch (error) {
    console.error('❌ SMTP 错误:', error.message);
    console.log('尝试其他方式...');
  }
  
  // 方法 2: 使用 sendmail（macOS 默认支持）
  try {
    const tempFile = path.join(__dirname, 'email.tmp');
    const emailContent = `To: ${CONFIG.email}
Subject: ${subject}
MIME-Version: 1.0
Content-Type: text/html; charset=UTF-8

${htmlContent}
`;
    
    fs.writeFileSync(tempFile, emailContent);
    
    return new Promise((resolve) => {
      exec(`/usr/sbin/sendmail -t < "${tempFile}"`, (error) => {
        fs.unlinkSync(tempFile);
        if (error) {
          console.error('❌ sendmail 发送失败:', error.message);
          resolve(false);
        } else {
          console.log('✅ 邮件已发送（sendmail）');
          resolve(true);
        }
      });
    });
  } catch (error) {
    console.error('❌ sendmail 发送失败:', error.message);
  }
  
  // 方法 3: 保存到文件，手动发送
  const outputFile = path.join(__dirname, `email-${new Date().toISOString().split('T')[0]}.html`);
  fs.writeFileSync(outputFile, htmlContent);
  console.log(`💾 邮件内容已保存到：${outputFile}`);
  console.log('💡 请配置 SMTP 或手动发送该 HTML 文件');
  
  return false;
}

/**
 * 保存数据到文件（备用）
 */
function saveToFile(data) {
  const fs = require('fs');
  const path = require('path');
  const date = new Date().toISOString().split('T')[0];
  const filePath = path.join(__dirname, `data-${date}.json`);
  
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
  console.log(`💾 数据已保存到：${filePath}`);
}

/**
 * 主函数
 */
async function main() {
  console.log('🚀 开始获取 A 股数据...');
  console.log(`📧 目标邮箱：${CONFIG.email}`);
  console.log(`💰 价格上限：¥${CONFIG.priceLimit}`);
  
  // 获取数据
  const [newStocks, lowPriceStocks] = await Promise.all([
    getNewStocks(),
    getLowPriceStocks(),
  ]);
  
  console.log(`📊 获取到新股：${newStocks.length} 只`);
  console.log(`📊 获取到低价股：${lowPriceStocks.length} 只`);
  
  // 生成邮件内容
  const emailContent = generateEmailContent(newStocks, lowPriceStocks);
  
  // 保存数据到文件
  saveToFile({
    date: new Date().toISOString(),
    newStocks,
    lowPriceStocks,
  });
  
  // 发送邮件
  await sendEmail(emailContent);
  
  console.log('✅ 完成！');
}

// 运行
main().catch(console.error);
