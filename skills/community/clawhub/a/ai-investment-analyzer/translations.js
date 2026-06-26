// 国际化翻译模块
const translations = {
  en: {
    // 基本术语
    stock: "Stock",
    crypto: "Cryptocurrency",
    forex: "Foreign Exchange",
    commodities: "Commodities",
    realEstate: "Real Estate",
    bonds: "Bonds",
    funds: "Funds",
    indices: "Indices",
    
    // 分析结果
    trend: "Trend",
    riskLevel: "Risk Level",
    recommendation: "Recommendation",
    roi: "ROI",
    confidence: "Confidence",
    
    // 风险等级
    lowRisk: "Low Risk",
    moderateRisk: "Moderate Risk",
    highRisk: "High Risk",
    
    // 投资建议
    buy: "BUY",
    hold: "HOLD",
    sell: "SELL",
    cautious: "CAUTIOUS",
    
    // 趋势描述
    upwardTrend: "Upward Trend",
    downwardTrend: "Downward Trend",
    stableTrend: "Stable",
    volatileTrend: "Volatile",
    
    // 命令说明
    analyze: "Analyze investment opportunity",
    portfolio: "Optimize portfolio configuration",
    risk: "Assess investment risk",
    forecast: "Market trend forecast",
    
    // 成功消息
    analysisComplete: "Investment analysis completed successfully",
    portfolioOptimized: "Portfolio optimized successfully",
    riskAssessmentDone: "Risk assessment completed",
    marketPredictionDone: "Market prediction generated",
    
    // 错误消息
    error: "Error in analysis",
    notSupported: "Asset type not supported",
    invalidPeriod: "Invalid analysis period",
    missingData: "Missing data for analysis"
  },
  
  zh: {
    // 基本术语
    stock: "股票",
    crypto: "加密货币",
    forex: "外汇",
    commodities: "大宗商品",
    realEstate: "房地产",
    bonds: "债券",
    funds: "基金",
    indices: "指数",
    
    // 分析结果
    trend: "趋势",
    riskLevel: "风险等级",
    recommendation: "投资建议",
    roi: "回报率",
    confidence: "置信度",
    
    // 风险等级
    lowRisk: "低风险",
    moderateRisk: "中等风险",
    highRisk: "高风险",
    
    // 投资建议
    buy: "买入",
    hold: "持有",
    sell: "卖出",
    cautious: "谨慎观望",
    
    // 趋势描述
    upwardTrend: "上涨趋势",
    downwardTrend: "下跌趋势",
    stableTrend: "稳定",
    volatileTrend: "震荡",
    
    // 命令说明
    analyze: "分析投资机会",
    portfolio: "优化投资组合",
    risk: "评估投资风险",
    forecast: "市场趋势预测",
    
    // 成功消息
    analysisComplete: "投资分析完成成功",
    portfolioOptimized: "投资组合优化成功",
    riskAssessmentDone: "风险评估完成",
    marketPredictionDone: "市场预测生成",
    
    // 错误消息
    error: "分析过程中出错",
    notSupported: "资产类型不支持",
    invalidPeriod: "分析周期无效",
    missingData: "缺少分析数据"
  },
  
  ja: {
    // 基本术语
    stock: "株式",
    crypto: "暗号資産",
    forex: "外国為替",
    commodities: "商品",
    realEstate: "不動産",
    bonds: "債券",
    funds: "ファンド",
    indices: "指数",
    
    // 分析结果
    trend: "トレンド",
    riskLevel: "リスクレベル",
    recommendation: "投資提案",
    roi: "利益率",
    confidence: "信頼度",
    
    // 风险等级
    lowRisk: "低リスク",
    moderateRisk: "中リスク",
    highRisk: "高リスク",
    
    // 投资建议
    buy: "購入",
    hold: "保有",
    sell: "売却",
    cautious: "慎重に",
    
    // 趋势描述
    upwardTrend: "上昇トレンド",
    downwardTrend: "下落トレンド",
    stableTrend: "安定",
    volatileTrend: "変動",
    
    // 命令说明
    analyze: "投資機会の分析",
    portfolio: "ポートフォリオ最適化",
    risk: "投資リスク評価",
    forecast: "市場トレンド予測",
    
    // 成功消息
    analysisComplete: "投資分析が完了しました",
    portfolioOptimized: "ポートフォリオが最適化されました",
    riskAssessmentDone: "リスク評価が完了しました",
    marketPredictionDone: "市場予測が生成されました",
    
    // 错误消息
    error: "分析エラー",
    notSupported: "資産タイプがサポートされていません",
    invalidPeriod: "分析期間が無効です",
    missingData: "分析データが不足しています"
  },
  
  de: {
    // 基本术语
    stock: "Aktie",
    crypto: "Kryptowährung",
    forex: "Währungen",
    commodities: "Rohstoffe",
    realEstate: "Immobilien",
    bonds: "Anleihen",
    funds: "Fonds",
    indices: "Indices",
    
    // 分析结果
    trend: "Trend",
    riskLevel: "Risikostufe",
    recommendation: "Empfehlung",
    roi: "ROI",
    confidence: "Konfidenz",
    
    // 风险等级
    lowRisk: "Niedriges Risiko",
    moderateRisk: "Moderates Risiko",
    highRisk: "Hohes Risiko",
    
    // 投资建议
    buy: "KAUFEN",
    hold: "HALTEN",
    sell: "VERKAUFEN",
    cautious: "VORSICHTIG",
    
    // 趋势描述
    upwardTrend: "Aufwärtstrend",
    downwardTrend: "Abwärtstrend",
    stableTrend: "Stabil",
    volatileTrend: "Volatil",
    
    // 命令说明
    analyze: "Analyse der Investitionsmöglichkeit",
    portfolio: "Portfolio-Optimierung",
    risk: "Investitionsrisiko-Evaluierung",
    forecast: "Markttrend-Prognose",
    
    // 成功消息
    analysisComplete: "Investitionsanalyse erfolgreich abgeschlossen",
    portfolioOptimized: "Portfolio erfolgreich optimiert",
    riskAssessmentDone: "Risiko-Evaluierung abgeschlossen",
    marketPredictionDone: "Marktprognose generiert",
    
    // 错误消息
    error: "Analysefehler",
    notSupported: "Asset-Typ nicht unterstützt",
    invalidPeriod: "Analyseperiode ungültig",
    missingData: "Fehlende Analyse-Daten"
  }
};

// 根据语言获取翻译
function translate(key, language = "en") {
  return translations[language][key] || key;
}

// 获取支持的语言列表
function getSupportedLanguages() {
  return Object.keys(translations);
}

// 根据语言输出
function localizedOutput(data, language = "en") {
  const result = {};
  
  for (const key in data) {
    const translation = translate(key, language);
    result[translation] = data[key];
  }
  
  return result;
}

module.exports = {
  translate,
  getSupportedLanguages,
  localizedOutput
};