/**
 * 模糊匹配工具模块
 * 用于第三方数据与天眼查搜索结果的匹配和核查
 */

/**
 * 标准化文本：去除空白、标点、常见后缀
 */
export function normalizeText(text) {
  if (!text) return '';
  return text
    .trim()
    .replace(/[\s\u3000]+/g, '')  // 去除所有空白（含全角空格）
    .replace(/[，。、；：""''（）\(\)【】\[\]《》<>！？!?·\-—_,.:;'"]/g, '')
    .replace(/(中标公告|成交公告|中标结果公告|中标候选人公示|招标公告|采购公告|询价公告|竞争性谈判公告|竞争性磋商公告|单一来源公告|政府采购合同公告)$/g, '')
    .toLowerCase();
}

/**
 * 最长公共子串比率
 * @returns {number} 0-1 之间的相似度
 */
export function stringSimilarity(a, b) {
  if (!a || !b) return 0;
  const na = normalizeText(a);
  const nb = normalizeText(b);
  if (na === nb) return 1;
  if (!na || !nb) return 0;

  const shorter = na.length <= nb.length ? na : nb;
  const longer = na.length > nb.length ? na : nb;

  // 最长公共子串（DP）
  let maxLen = 0;
  const dp = new Array(shorter.length + 1).fill(0);

  for (let i = 1; i <= longer.length; i++) {
    let prev = 0;
    for (let j = 1; j <= shorter.length; j++) {
      const temp = dp[j];
      if (longer[i - 1] === shorter[j - 1]) {
        dp[j] = prev + 1;
        if (dp[j] > maxLen) maxLen = dp[j];
      } else {
        dp[j] = 0;
      }
      prev = temp;
    }
  }

  // 用较短字符串长度作为分母
  return maxLen / shorter.length;
}

/**
 * 统一解析各种金额格式为"元"（数字）
 * 支持: "¥77,800,000" / "80万元" / "3608.68万元" / "18.98万元" / "189777元" / "1,234.56万元"
 * @param {string} str - 金额字符串
 * @param {Object} options - 可选配置
 * @param {string} options.sourceHint - 来源提示，如 'tianyancha' 会对无单位小数字默认按万元处理
 * @returns {number|null} 金额（元），无法解析返回 null
 */
export function parseAmountYuan(str, options = {}) {
  if (!str || str === '-') return null;

  const cleaned = String(str).replace(/[¥￥\s,，]/g, '');

  // 快速排除明显不是金额的文本（如项目编号、混杂地址等）
  // 允许：数字、小数点、金额单位、少量括号/横线
  const nonAmountChars = cleaned.replace(/[\d.万亿元万億]/g, '');
  const reallyBad = nonAmountChars.replace(/[-()（）\s]/g, '');
  if (reallyBad.length > 0) return null;

  // 匹配数字部分和单位
  const match = cleaned.match(/([\d.]+)\s*(万元|亿元|元)?/);
  if (!match) return null;

  const numStr = match[1];
  // 排除多个小数点的异常数字（如 705000.00110000.00）
  if ((numStr.match(/\./g) || []).length > 1) return null;

  let num = parseFloat(numStr);
  if (isNaN(num)) return null;

  const unit = match[2] || '';
  if (unit === '亿元') {
    num *= 100000000;
  } else if (unit === '万元') {
    num *= 10000;
  } else {
    // 无单位或"元"
    // 如果数字很大（>10000），大概率已经是元，不做转换
    // 如果来源是天眼查且无单位、数值<1000，默认视为万元（招投标金额极少以百元为单位）
    if (options.sourceHint === 'tianyancha' && num < 1000) {
      num *= 10000;
    }
  }

  return num;
}

/**
 * 比较两个金额是否接近
 * @param {number|null} amountA - 金额A（元）
 * @param {number|null} amountB - 金额B（元）
 * @param {number} tolerance - 允许偏差比例，默认 0.3 (30%)
 * @returns {{ match: boolean, ratio: number|null }}
 */
export function compareAmount(amountA, amountB, tolerance = 0.3) {
  if (amountA == null || amountB == null || amountA === 0 || amountB === 0) {
    return { match: false, ratio: null };
  }
  const ratio = Math.abs(amountA - amountB) / Math.max(amountA, amountB);
  return { match: ratio <= tolerance, ratio };
}

/**
 * 检查文本 b 是否包含文本 a（或反向），用于采购单位/中标单位匹配
 * 支持：完全匹配、子串包含、去除常见后缀后匹配
 */
export function entityMatch(a, b) {
  if (!a || !b) return false;
  const na = a.replace(/[\s\u3000]/g, '').trim();
  const nb = b.replace(/[\s\u3000]/g, '').trim();
  if (na === nb) return true;
  if (na.includes(nb) || nb.includes(na)) return true;

  // 去除常见后缀后再比较
  const suffixes = ['有限公司', '有限责任公司', '股份有限公司', '集团有限公司'];
  let sa = na, sb = nb;
  for (const s of suffixes) {
    sa = sa.replace(s, '');
    sb = sb.replace(s, '');
  }
  if (sa && sb && (sa.includes(sb) || sb.includes(sa))) return true;

  return false;
}

/**
 * 判断文本是否明显是地址/地点信息（而非企业/机构名称）
 */
export function isAddressLike(text) {
  if (!text) return false;
  const t = text.replace(/[\s\u3000]/g, '');
  // 包含明显的地址关键词
  const addressKeywords = ['地点：', '地址：', '开标室', '会议室', '楼', '层',
    '路', '街', '号', '幢', '单元'];
  // 如果包含多个地址特征词，或明确以地点/地址开头
  const hitCount = addressKeywords.filter(kw => t.includes(kw)).length;
  if (hitCount >= 2) return true;
  if (/^(地点|地址|开标地点|评审地点)[：:]/.test(text)) return true;
  return false;
}

/**
 * 按年份过滤搜索结果
 * @param {Array} searchResults - 天眼查搜索结果
 * @param {number} targetYear - 目标年份，默认2025
 * @returns {Array} 过滤后的结果
 */
export function filterResultsByYear(searchResults, targetYear = 2025) {
  if (!searchResults || searchResults.length === 0) return [];
  return searchResults.filter(r => {
    if (!r.date) return true; // 无日期保留，后续降低权重
    const year = parseInt(r.date.split('-')[0], 10);
    return year === targetYear;
  });
}

/**
 * 从天眼查搜索结果列表中找最佳匹配
 * @param {Object} excelRow - Excel 行数据 { buyer, projectName, winner, amountYuan }
 * @param {Array} searchResults - 天眼查搜索结果 [{ title, buyer, amount, date, link, fullText }]
 * @param {number} targetYear - 目标年份，默认2025（用于日期评分）
 * @returns {{ matched: Object|null, score: number, details: string[] }}
 */
export function matchSearchResult(excelRow, searchResults, targetYear = 2025) {
  if (!searchResults || searchResults.length === 0) {
    return { matched: null, score: 0, details: ['搜索结果为空'] };
  }

  let bestMatch = null;
  let bestScore = -Infinity;
  let bestDetails = [];

  for (const result of searchResults) {
    let score = 0;
    const details = [];

    // 0. 年份检查（硬过滤前置，2026年直接淘汰）
    if (result.date) {
      const resultYear = parseInt(result.date.split('-')[0], 10);
      if (resultYear !== targetYear) {
        score = -100;
        details.push(`年份不匹配: ${resultYear}年 ≠ ${targetYear}年 (直接淘汰)`);
        if (score > bestScore) {
          bestScore = score;
          bestMatch = result;
          bestDetails = details;
        }
        continue;
      }
    }

    // 1. 项目标题相似度 (权重 35)
    const titleSim = stringSimilarity(excelRow.projectName, result.title);
    const titleScore = titleSim >= 0.8 ? 35 : titleSim >= 0.4 ? Math.round(titleSim * 43.75) : 0;
    score += titleScore;
    details.push(`标题相似度: ${(titleSim * 100).toFixed(0)}% (${titleScore}/35)`);

    // 2. 采购单位匹配 (权重 25)
    const buyerMatched = entityMatch(excelRow.buyer, result.buyer);
    if (buyerMatched) {
      score += 25;
      details.push(`采购单位: 匹配 (25/25)`);
    } else {
      details.push(`采购单位: 不匹配 (0/25) [Excel: ${excelRow.buyer}, 天眼查: ${result.buyer}]`);
    }

    // 3. 金额接近度 (权重 20)
    const tycAmount = parseAmountYuan(result.amount, { sourceHint: 'tianyancha' });
    const { match: amountMatched, ratio } = compareAmount(excelRow.amountYuan, tycAmount);
    if (amountMatched) {
      const amountScore = ratio !== null ? Math.round((1 - ratio / 0.3) * 20) : 10;
      score += amountScore;
      details.push(`金额: 偏差 ${ratio !== null ? (ratio * 100).toFixed(1) + '%' : '未知'} (${amountScore}/20)`);
    } else if (ratio === null) {
      // 一方缺失金额，给部分分
      score += 5;
      details.push(`金额: 一方缺失 (5/20)`);
    } else {
      details.push(`金额: 偏差 ${(ratio * 100).toFixed(1)}% 超限 (0/20)`);
    }

    // 4. 中标单位匹配（权重15）
    let winnerMatched = false;
    if (excelRow.winner) {
      // 优先用 result.winner（如果搜索结果有提取到）
      if (result.winner && entityMatch(excelRow.winner, result.winner)) {
        winnerMatched = true;
      } else if (result.fullText && entityMatch(excelRow.winner, result.fullText)) {
        winnerMatched = true;
      }
    }
    if (winnerMatched) {
      score += 15;
      details.push(`中标单位: 匹配 (15/15)`);
    } else {
      details.push(`中标单位: 不匹配 (0/15)`);
    }

    // 5. 发布时间匹配 (权重 5)
    if (result.date) {
      const resultYear = parseInt(result.date.split('-')[0], 10);
      if (resultYear === targetYear) {
        score += 5;
        details.push(`发布年份: 匹配 (${targetYear}年) (+5)`);
      }
    } else {
      // 无日期给2分安慰分
      score += 2;
      details.push(`发布年份: 缺失 (+2)`);
    }

    if (score > bestScore) {
      bestScore = score;
      bestMatch = result;
      bestDetails = details;
    }
  }

  // 强匹配兜底：采购单位+中标单位同时命中，且金额不矛盾，保底65分
  if (bestMatch && bestScore < 65) {
    const buyerMatched = entityMatch(excelRow.buyer, bestMatch.buyer);
    let winnerMatched = false;
    if (excelRow.winner) {
      if (bestMatch.winner && entityMatch(excelRow.winner, bestMatch.winner)) {
        winnerMatched = true;
      } else if (bestMatch.fullText && entityMatch(excelRow.winner, bestMatch.fullText)) {
        winnerMatched = true;
      }
    }

    const tycAmount = parseAmountYuan(bestMatch.amount, { sourceHint: 'tianyancha' });
    const amountNotConflict =
      excelRow.amountYuan == null || tycAmount == null || compareAmount(excelRow.amountYuan, tycAmount, 0.5).match;

    if (buyerMatched && winnerMatched && amountNotConflict) {
      bestScore = 65;
      bestDetails.push('强匹配兜底: 采购单位+中标单位同时命中 (+65)');
    }
  }

  return { matched: bestMatch, score: bestScore, details: bestDetails, titleSimilarity: bestMatch ? stringSimilarity(excelRow.projectName, bestMatch.title) : 0 };
}

/**
 * 核对详情页数据与 Excel 数据
 * @param {Object} excelRow - { buyer, projectName, winner, amountYuan, city, subject }
 * @param {Object} detailData - fetchBiddingDetail 返回的详情数据
 * @param {number} targetYear - 目标年份，默认2025
 * @returns {{ passed: boolean, reasons: string[] }}
 */
export function verifyDetail(excelRow, detailData, targetYear = 2025) {
  const reasons = [];

  // 核对发布日期（年份）
  if (detailData.publishDate) {
    const yearMatch = detailData.publishDate.match(/(\d{4})/);
    if (yearMatch) {
      const year = parseInt(yearMatch[1], 10);
      if (year !== targetYear) {
        reasons.push(`发布日期不匹配 [Excel要求${targetYear}年, 天眼查: ${detailData.publishDate}]`);
      }
    }
  }

  // 核对中标单位（排除明显是地址的提取错误）
  if (detailData.winner && excelRow.winner) {
    if (isAddressLike(detailData.winner)) {
      // 详情页 winner 明显是地址，不可靠，不以此判定不匹配
      reasons.push(`中标单位详情页提取疑似地址，暂不核对 [天眼查: ${detailData.winner}]`);
    } else if (!entityMatch(excelRow.winner, detailData.winner)) {
      reasons.push(`中标单位不匹配 [Excel: ${excelRow.winner}, 天眼查: ${detailData.winner}]`);
    }
  }

  // 核对采购单位（排除明显是地址或混杂其他字段的提取错误）
  if (detailData.bidder && excelRow.buyer) {
    const cleanBidder = detailData.bidder.replace(/(预算金额|中标金额|发布时间|公告类型).*$/g, '').trim();
    if (isAddressLike(cleanBidder)) {
      reasons.push(`采购单位详情页提取疑似地址，暂不核对 [天眼查: ${detailData.bidder}]`);
    } else if (!entityMatch(excelRow.buyer, cleanBidder)) {
      reasons.push(`采购单位不匹配 [Excel: ${excelRow.buyer}, 天眼查: ${detailData.bidder}]`);
    }
  }

  // 核对金额（如果详情页有金额信息）
  if (detailData.amount && excelRow.amountYuan) {
    const detailAmount = parseAmountYuan(detailData.amount, { sourceHint: 'tianyancha' });
    // 如果解析后的金额 < 100 元，很可能是提取到了其他数字（如数量、评分等），忽略
    if (detailAmount !== null && detailAmount < 100) {
      reasons.push(`详情页提取金额过小(${detailAmount}元)，可能不是中标金额，暂不核对`);
    } else {
      const { match, ratio } = compareAmount(excelRow.amountYuan, detailAmount);
      if (!match && ratio !== null) {
        reasons.push(`金额差异过大 [Excel: ${excelRow.amountYuan}元, 天眼查: ${detailData.amount}, 偏差: ${(ratio * 100).toFixed(1)}%]`);
      }
    }
  }

  return {
    passed: reasons.length === 0,
    reasons,
  };
}
