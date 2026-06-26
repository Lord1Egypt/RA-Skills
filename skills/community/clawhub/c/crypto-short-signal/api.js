/**
 * Crypto Short Signal API - 付费层
 * 
 * 这部分代码运行在 SkillPay Cloud 或你的私有服务器上
 * 包含核心逻辑和敏感数据，不公开
 */

const axios = require('axios');

// SkillPay 配置 (保密)
const BILLING_URL = 'https://skillpay.me/api/v1/billing';
const API_KEY = process.env.SKILLPAY_API_KEY || 'sk_0e14dceabeea3a6371770165736b89add613f7ab8f729c57aef555525b0f1a00';
const SKILL_ID = process.env.SKILL_ID || 'crypto-short-signal';

const headers = { 
    'X-API-Key': API_KEY, 
    'Content-Type': 'application/json' 
};

// 代币数据库 (保密)
const TOKEN_DATABASE = {
    "ZRO": {
        "name": "LayerZero",
        "unlock_date": "2026-03-20",
        "unlock_amount": "32.6M",
        "unlock_percent": 3.26,
        "circulating_ratio": 20.26,
        "fdv_mcap": 4.94,
        "historical_drop": -5.97,
        "win_rate": 78
    },
    "BARD": {
        "name": "Lombard",
        "unlock_date": "2026-03-18",
        "unlock_amount": "11.35M",
        "unlock_percent": 1.14,
        "circulating_ratio": 22.5,
        "fdv_mcap": 4.44,
        "historical_drop": -4.0,
        "win_rate": 100
    },
    "STABLE": {
        "name": "Stable",
        "unlock_date": "2027-01-01",
        "unlock_amount": "待确认",
        "unlock_percent": "待确认",
        "circulating_ratio": 20.56,
        "fdv_mcap": 4.86,
        "historical_drop": "待验证",
        "win_rate": "待验证"
    }
};

/**
 * 扣费函数
 */
async function chargeUser(userId, amount = 0) {
    try {
        const { data } = await axios.post(BILLING_URL + '/charge', {
            user_id: userId,
            skill_id: SKILL_ID,
            amount: amount,
        }, { headers });
        
        if (data.success) {
            return { 
                ok: true, 
                balance: data.balance,
                message: "扣费成功"
            };
        } else {
            return { 
                ok: false, 
                balance: data.balance, 
                payment_url: data.payment_url,
                message: "余额不足，请充值"
            };
        }
    } catch (error) {
        return {
            ok: false,
            balance: 0,
            payment_url: "",
            message: `扣费接口错误：${error.message}`
        };
    }
}

/**
 * 核心分析逻辑 (保密)
 */
function analyzeToken(tokenSymbol) {
    if (!TOKEN_DATABASE[tokenSymbol]) {
        return {
            status: "error",
            message: `未找到代币：${tokenSymbol}`
        };
    }
    
    const token = TOKEN_DATABASE[tokenSymbol];
    
    // 计算做空信号
    const unlockDate = new Date(token.unlock_date);
    const shortStart = new Date(unlockDate);
    shortStart.setDate(shortStart.getDate() - 7);
    const shortEnd = new Date(unlockDate);
    shortEnd.setDate(shortEnd.getDate() - 1);
    
    // 生成目标价格和止损
    const currentPrice = 1.0;
    const targetPrice = currentPrice * (1 + token.historical_drop / 100);
    const stopLoss = currentPrice * 1.10;
    
    return {
        status: "success",
        data: {
            token: tokenSymbol,
            name: token.name,
            unlock_date: token.unlock_date,
            unlock_amount: token.unlock_amount,
            unlock_percent: `${token.unlock_percent}%`,
            circulating_ratio: `${token.circulating_ratio}%`,
            fdv_mcap: `${token.fdv_mcap}x`,
            risk_level: token.fdv_mcap > 4 ? "高" : "中",
            short_signal: {
                short_start: shortStart.toISOString().split('T')[0],
                short_end: shortEnd.toISOString().split('T')[0],
                target_drop: `${token.historical_drop}%`,
                target_price: `$${targetPrice.toFixed(2)}`,
                stop_loss: `$${stopLoss.toFixed(2)}`,
                win_rate: `${token.win_rate}%`
            }
        }
    };
}

/**
 * API 入口函数
 */
async function handleRequest(event) {
    const userId = event.user_id || event.userId || 'anonymous';
    const inputData = event.input || event.data || {};
    const tokenSymbol = (inputData.token || '').toUpperCase();
    
    // 第一步：扣费
    const chargeResult = await chargeUser(userId);
    
    if (!chargeResult.ok) {
        return {
            status: "payment_required",
            payment_url: chargeResult.payment_url,
            message: chargeResult.message
        };
    }
    
    // 第二步：验证输入
    if (!tokenSymbol) {
        return {
            status: "error",
            message: "请提供代币符号，如：ZRO, BARD, STABLE",
            examples: ["ZRO", "BARD", "STABLE"]
        };
    }
    
    // 第三步：执行分析 (核心逻辑)
    const result = analyzeToken(tokenSymbol);
    
    return result;
}

// 导出模块
module.exports = {
    handleRequest,
    chargeUser,
    analyzeToken
};
