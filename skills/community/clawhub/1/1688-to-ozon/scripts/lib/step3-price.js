#!/usr/bin/env node
/**
 * Step 3: 定价计算（内置实现）
 * 
 * 功能：
 * - 读取商品重量和采购价
 * - 计算物流费用
 * - 计算售价（含佣金、利润）
 * - 输出定价结果
 * 
 * 输出：
 * - pricing.md - 定价详情
 * - result.json - 结构化定价数据
 */

const fs = require('fs');
const path = require('path');
const { log, writeProgress } = require('./logger');
const { getOutputDir } = require('./workspace');
const { loadConfig } = require('./config');

const OUTPUT_DIR = path.join(getOutputDir(), 'ozon-pricer');

/**
 * 执行定价计算
 */
function runPricing(weight, purchasePrice, shippingCost, profitMargin = 0.2) {
  log('Step 3: 开始计算定价...', 'info');
  
  try {
    // 加载配置
    const config = loadConfig();
    
    // 确保输出目录存在
    if (!fs.existsSync(OUTPUT_DIR)) {
      fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }
    
    // 解析参数
    const weightKg = parseWeight(weight);
    const purchasePriceCNY = parseFloat(purchasePrice);
    const domesticShippingCNY = parseFloat(shippingCost) || 0;
    
    if (!weightKg || !purchasePriceCNY) {
      throw new Error('缺少必需参数：重量或采购价');
    }
    
    // 计算定价
    const pricingResult = calculatePricing({
      weightKg,
      purchasePriceCNY,
      domesticShippingCNY,
      profitMargin,
      config
    });
    
    // 保存结果
    const pricingMdFile = path.join(OUTPUT_DIR, 'pricing.md');
    const resultJsonFile = path.join(OUTPUT_DIR, 'result.json');
    
    fs.writeFileSync(pricingMdFile, formatPricingMd(pricingResult));
    fs.writeFileSync(resultJsonFile, JSON.stringify(pricingResult, null, 2));
    
    log('Step 3 完成：定价计算成功', 'success');
    log(`最终售价：₽${pricingResult.finalPriceRUB.toFixed(2)} (¥${pricingResult.finalPriceCNY.toFixed(2)})`, 'info');
    writeProgress(getOutputDir(), 'step3_pricing', 'completed', {
      outputDir: OUTPUT_DIR,
      pricingMd: pricingMdFile,
      resultJson: resultJsonFile,
      pricingData: pricingResult
    });
    
    return {
      success: true,
      outputDir: OUTPUT_DIR,
      pricingData: pricingResult
    };
    
  } catch (error) {
    log(`Step 3 失败：${error.message}`, 'error');
    writeProgress(getOutputDir(), 'step3_pricing', 'failed', {
      error: error.message
    });
    throw error;
  }
}

/**
 * 解析重量
 */
function parseWeight(weight) {
  if (!weight) return null;
  
  const match = weight.match(/(\d+(?:\.\d+)?)\s*(g|kg)/i);
  if (!match) return parseFloat(weight) || null;
  
  const value = parseFloat(match[1]);
  const unit = match[2].toLowerCase();
  
  return unit === 'kg' ? value : value / 1000;
}

/**
 * 计算定价
 */
function calculatePricing(params) {
  const { weightKg, purchasePriceCNY, domesticShippingCNY, profitMargin, config } = params;
  
  // 1. 物流费用（CEL Standard，简化计算）
  const shippingCostCNY = calculateShipping(weightKg, config.pricing);
  
  // 2. 总成本（CNY）
  const totalCostCNY = purchasePriceCNY + domesticShippingCNY + shippingCostCNY;
  
  // 3. 汇率转换（CNY → RUB）
  const exchangeRate = config.pricing?.exchangeRate || 13.5;
  const totalCostRUB = totalCostCNY * exchangeRate;
  
  // 4. OZON 佣金（约 15%）
  const commissionRate = 0.15;
  
  // 5. 计算售价（含利润）
  // 公式：售价 = 成本 / (1 - 佣金率 - 利润率)
  const finalPriceCNY = totalCostCNY / (1 - commissionRate - profitMargin);
  const finalPriceRUB = finalPriceCNY * exchangeRate;
  
  // 6. 详细拆分
  const commissionCNY = finalPriceCNY * commissionRate;
  const profitCNY = finalPriceCNY * profitMargin;
  
  return {
    weightKg,
    purchasePriceCNY,
    domesticShippingCNY,
    shippingCostCNY,
    totalCostCNY,
    totalCostRUB,
    exchangeRate,
    commissionRate,
    commissionCNY,
    profitMargin,
    profitCNY,
    finalPriceCNY: finalPriceCNY,
    finalPriceRUB: finalPriceRUB,
    priceBreakdown: {
      cost: totalCostCNY.toFixed(2),
      commission: commissionCNY.toFixed(2),
      profit: profitCNY.toFixed(2),
      final: finalPriceCNY.toFixed(2)
    }
  };
}

/**
 * 计算物流费用（简化版）
 */
function calculateShipping(weightKg, config) {
  // CEL Standard 简化计算：首重 0.5kg ¥40，续重每 kg ¥40
  const baseWeight = 0.5;
  const basePrice = 40;
  const extraPricePerKg = 40;
  
  if (weightKg <= baseWeight) {
    return basePrice;
  }
  
  const extraWeight = weightKg - baseWeight;
  return basePrice + Math.ceil(extraWeight) * extraPricePerKg;
}

/**
 * 格式化 Markdown 输出
 */
function formatPricingMd(result) {
  return `# 定价详情

## 基本信息
- **重量**: ${result.weightKg * 1000}g (${result.weightKg}kg)
- **采购价**: ¥${result.purchasePriceCNY.toFixed(2)}
- **国内运费**: ¥${result.domesticShippingCNY.toFixed(2)}

## 成本计算
- **国际物流**: ¥${result.shippingCostCNY.toFixed(2)}
- **总成本**: ¥${result.totalCostCNY.toFixed(2)} (₽${result.totalCostRUB.toFixed(2)})

## 售价计算
- **OZON 佣金**: ${(result.commissionRate * 100).toFixed(0)}% = ¥${result.commissionCNY.toFixed(2)}
- **利润率**: ${(result.profitMargin * 100).toFixed(0)}% = ¥${result.profitCNY.toFixed(2)}
- **汇率**: 1 CNY = ${result.exchangeRate} RUB

## 最终售价
- **人民币**: ¥${result.finalPriceCNY.toFixed(2)}
- **卢布**: ₽${result.finalPriceRUB.toFixed(2)}

## 价格拆分
\`\`\`
成本：¥${result.priceBreakdown.cost}
佣金：¥${result.priceBreakdown.commission}
利润：¥${result.priceBreakdown.profit}
─────────────
售价：¥${result.priceBreakdown.final}
\`\`\`
`;
}

module.exports = {
  runPricing,
  OUTPUT_DIR,
  parseWeight,
  calculatePricing,
  calculateShipping,
  formatPricingMd
};
