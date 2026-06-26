/**
 * Crypto Short Signal Generator - 公开层
 * 
 * 这部分代码运行在 ClawHub 上
 * 只包含收费接口和基础验证
 * 核心逻辑在 api.js (付费层)
 */

const axios = require('axios');

// SkillPay 配置
const BILLING_URL = 'https://skillpay.me/api/v1/billing';
const API_KEY = process.env.SKILLPAY_API_KEY || 'sk_0e14dceabeea3a6371770165736b89add613f7ab8f729c57aef555525b0f1a00';
const SKILL_ID = process.env.SKILL_ID || 'crypto-short-signal';

// 付费层 API 地址 (可以部署在 SkillPay Cloud 或你的服务器)
const PAID_API_URL = process.env.PAID_API_URL || 'https://api.skillpay.me/skills/crypto-short-signal/analyze';

const headers = { 
    'X-API-Key': API_KEY, 
    'Content-Type': 'application/json' 
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
 * 调用付费层 API
 */
async function callPaidAPI(userId, tokenSymbol) {
    try {
        const { data } = await axios.post(PAID_API_URL, {
            user_id: userId,
            token: tokenSymbol
        }, {
            headers: {
                'X-API-Key': API_KEY,
                'Content-Type': 'application/json'
            }
        });
        
        return data;
    } catch (error) {
        // 如果付费层 API 不可用，返回错误
        return {
            status: "error",
            message: `分析服务暂时不可用：${error.message}`
        };
    }
}

/**
 * 主函数
 */
async function main(event) {
    const userId = event.user_id || event.userId || 'anonymous';
    const inputData = event.input || event.data || {};
    const tokenSymbol = (inputData.token || '').toUpperCase();
    
    // 第一步：扣费
    const chargeResult = await chargeUser(userId);
    
    if (!chargeResult.ok) {
        // 余额不足，返回支付链接
        return {
            status: "payment_required",
            payment_url: chargeResult.payment_url,
            message: chargeResult.message,
            skill_info: {
                name: "加密货币做空信号生成器",
                price: "0.001 USDT",
                description: "提前 7 天知道哪些币要暴跌 30%+",
                min_deposit: "8 USDT"
            }
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
    
    // 第三步：调用付费层 API (核心逻辑)
    const result = await callPaidAPI(userId, tokenSymbol);
    
    return result;
}

// 导出模块
module.exports = {
    main,
    chargeUser,
    callPaidAPI
};

// 测试函数
if (require.main === module) {
    console.log("测试公开层...");
    // 这里可以添加测试代码
}
