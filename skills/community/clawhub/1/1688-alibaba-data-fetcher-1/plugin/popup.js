// ============================================================
// 1688 Data Claw - Popup Script
// 弹出界面交互逻辑
// ============================================================

const CLAW_VERSION = '1.0.0';

// DOM 元素
const els = {
  statusDot: document.getElementById('statusDot'),
  statusText: document.getElementById('statusText'),
  pageType: document.getElementById('pageType'),
  sycmCount: document.getElementById('sycmCount'),
  workCount: document.getElementById('workCount'),
  btnClaw: document.getElementById('btnClaw'),
  clawSpinner: document.getElementById('clawSpinner'),
  clawText: document.getElementById('clawText'),
  btnClear: document.getElementById('btnClear'),
  pageInfo: document.getElementById('pageInfo'),
  currentPageType: document.getElementById('currentPageType'),
  currentPageCount: document.getElementById('currentPageCount'),
  rowCompanyName: document.getElementById('rowCompanyName'),
  currentCompanyName: document.getElementById('currentCompanyName'),
  rowRank: document.getElementById('rowRank'),
  currentRank: document.getElementById('currentRank'),
  rowPayAmt: document.getElementById('rowPayAmt'),
  currentPayAmt: document.getElementById('currentPayAmt'),
  rowItemCnt: document.getElementById('rowItemCnt'),
  currentItemCnt: document.getElementById('currentItemCnt'),
  rowPullSales: document.getElementById('rowPullSales'),
  currentPullSales: document.getElementById('currentPullSales'),
  rowRevealCnt: document.getElementById('rowRevealCnt'),
  currentRevealCnt: document.getElementById('currentRevealCnt'),
  rowFlowPv: document.getElementById('rowFlowPv'),
  currentFlowPv: document.getElementById('currentFlowPv'),
  rowClickRate: document.getElementById('rowClickRate'),
  currentClickRate: document.getElementById('currentClickRate'),
  rowBounceRate: document.getElementById('rowBounceRate'),
  currentBounceRate: document.getElementById('currentBounceRate'),
  rowMobileShare: document.getElementById('rowMobileShare'),
  currentMobileShare: document.getElementById('currentMobileShare'),
  rowInquiry: document.getElementById('rowInquiry'),
  currentInquiry: document.getElementById('currentInquiry'),
  rowFlowSourceRecent7: document.getElementById('rowFlowSourceRecent7'),
  currentFlowSourceRecent7: document.getElementById('currentFlowSourceRecent7'),
  rowKeywordsRecent7: document.getElementById('rowKeywordsRecent7'),
  currentKeywordsRecent7: document.getElementById('currentKeywordsRecent7'),
  rowTradePay: document.getElementById('rowTradePay'),
  currentTradePay: document.getElementById('currentTradePay'),
  rowTradePayByr: document.getElementById('rowTradePayByr'),
  currentTradePayByr: document.getElementById('currentTradePayByr'),
  rowTradePayQty: document.getElementById('rowTradePayQty'),
  currentTradePayQty: document.getElementById('currentTradePayQty'),
  rowTradePayRate: document.getElementById('rowTradePayRate'),
  currentTradePayRate: document.getElementById('currentTradePayRate'),
  rowTradePerAmt: document.getElementById('rowTradePerAmt'),
  currentTradePerAmt: document.getElementById('currentTradePerAmt'),
  rowTradeRefund: document.getElementById('rowTradeRefund'),
  currentTradeRefund: document.getElementById('currentTradeRefund'),
  rowTradeRefundRate: document.getElementById('rowTradeRefundRate'),
  currentTradeRefundRate: document.getElementById('currentTradeRefundRate'),
  rowTradeMord: document.getElementById('rowTradeMord'),
  currentTradeMord: document.getElementById('currentTradeMord'),
  rowTradeNewBuyer: document.getElementById('rowTradeNewBuyer'),
  currentTradeNewBuyer: document.getElementById('currentTradeNewBuyer'),
  rowWwResponse: document.getElementById('rowWwResponse'),
  currentWwResponse: document.getElementById('currentWwResponse'),
  rowWwSatisfaction: document.getElementById('rowWwSatisfaction'),
  currentWwSatisfaction: document.getElementById('currentWwSatisfaction'),
  rowLgt48hGotRate: document.getElementById('rowLgt48hGotRate'),
  currentLgt48hGotRate: document.getElementById('currentLgt48hGotRate'),
  rowLgtFulfillRate: document.getElementById('rowLgtFulfillRate'),
  currentLgtFulfillRate: document.getElementById('currentLgtFulfillRate'),
  rowLgtPlanAccRate: document.getElementById('rowLgtPlanAccRate'),
  currentLgtPlanAccRate: document.getElementById('currentLgtPlanAccRate'),
  rowLgtRfdFhRate: document.getElementById('rowLgtRfdFhRate'),
  currentLgtRfdFhRate: document.getElementById('currentLgtRfdFhRate'),
  rowQualityRfdRate: document.getElementById('rowQualityRfdRate'),
  currentQualityRfdRate: document.getElementById('currentQualityRfdRate'),
  rowQualityBadRate: document.getElementById('rowQualityBadRate'),
  currentQualityBadRate: document.getElementById('currentQualityBadRate'),
  rowNlhScore: document.getElementById('rowNlhScore'),
  currentNlhScore: document.getElementById('currentNlhScore'),
  rowQualityScore: document.getElementById('rowQualityScore'),
  currentQualityScore: document.getElementById('currentQualityScore'),
  rowRefundScore: document.getElementById('rowRefundScore'),
  currentRefundScore: document.getElementById('currentRefundScore'),
  extensionId: document.getElementById('extensionId'),
  apiCode: document.getElementById('apiCode'),
  toast: document.getElementById('toast')
};

// 工具函数
function showToast(message, duration = 2000) {
  if (!els.toast) return;
  els.toast.textContent = message;
  els.toast.classList.add('show');
  setTimeout(() => els.toast?.classList.remove('show'), duration);
}

function setStatus(status, text) {
  if (!els.statusDot || !els.statusText) return;
  els.statusDot.className = 'status-dot';
  if (status) els.statusDot.classList.add(status);
  els.statusText.textContent = text;
}

function setLoading(loading) {
  if (!els.btnClaw || !els.clawSpinner || !els.clawText) return;
  els.btnClaw.disabled = loading;
  els.clawSpinner.style.display = loading ? 'inline-block' : 'none';
  els.clawText.textContent = loading ? '采集中...' : '立即采集当前页';
}

// 获取当前标签页信息
async function getCurrentTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

// 检测1688页面类型
function detect1688PageType(url) {
  if (!url || !url.includes('1688.com')) return 'not_1688';
  if (url.includes('work.1688.com')) return 'work';
  if (url.includes('sycm.1688.com')) return 'sycm';
  if (url.includes('/offer/') && /offer\/\d+\.html/.test(url)) return 'detail';
  if (url.includes('s.1688.com') || url.includes('search')) return 'search_list';
  if (url.includes('shop')) return 'shop_list';
  return 'other';
}

// 更新统计信息
async function updateStats() {
  try {
    const response = await chrome.runtime.sendMessage({ action: 'GET_SUMMARY' });
    if (response.success) {
      els.sycmCount.textContent = response.summary.sycmCount || 0;
      els.workCount.textContent = response.summary.workCount || 0;
    }
  } catch (e) {
    console.error('获取统计失败:', e);
  }
}

// 更新页面信息
async function updatePageInfo() {
  const tab = await getCurrentTab();
  if (!tab) return;

  const pageType = detect1688PageType(tab.url);
  els.pageType.textContent = {
    'detail': '详情页',
    'search_list': '搜索列表',
    'shop_list': '店铺列表',
    'sycm': '生意参谋',
    'work': '工作台',
    'other': '其他',
    'not_1688': '非1688'
  }[pageType] || '未知';

  if (pageType !== 'not_1688') {
    els.pageInfo.style.display = 'block';
    els.currentPageType.textContent = els.pageType.textContent;

    // 获取当前页面数据
    try {
      const response = await chrome.tabs.sendMessage(tab.id, { action: 'GET_CLAW_DATA' });
      if (response && response.success && response.data) {
        const data = response.data;
        if (data._pageType === 'work') {
          // 工作台页面：显示旺旺响应率和满意度
          els.rowPageCount.style.display = 'none';

          if (data.wwResponse) {
            els.rowWwResponse.style.display = 'flex';
            els.currentWwResponse.textContent = data.wwResponse.display ? `${data.wwResponse.display}%` : '-';
          } else {
            els.rowWwResponse.style.display = 'none';
          }

          if (data.wwSatisfaction) {
            els.rowWwSatisfaction.style.display = 'flex';
            els.currentWwSatisfaction.textContent = data.wwSatisfaction.display ? `${data.wwSatisfaction.display}%` : '-';
          } else {
            els.rowWwSatisfaction.style.display = 'none';
          }

          // 物流体验指标
          if (data.lgt48hGotRate) {
            els.rowLgt48hGotRate.style.display = 'flex';
            els.currentLgt48hGotRate.textContent = data.lgt48hGotRate.display ? `${data.lgt48hGotRate.display}%` : '-';
          } else {
            els.rowLgt48hGotRate.style.display = 'none';
          }

          if (data.lgtFulfillRate) {
            els.rowLgtFulfillRate.style.display = 'flex';
            els.currentLgtFulfillRate.textContent = data.lgtFulfillRate.display ? `${data.lgtFulfillRate.display}%` : '-';
          } else {
            els.rowLgtFulfillRate.style.display = 'none';
          }

          if (data.lgtPlanAccRate) {
            els.rowLgtPlanAccRate.style.display = 'flex';
            els.currentLgtPlanAccRate.textContent = data.lgtPlanAccRate.display ? `${data.lgtPlanAccRate.display}%` : '-';
          } else {
            els.rowLgtPlanAccRate.style.display = 'none';
          }

          if (data.lgtRfdFhRate) {
            els.rowLgtRfdFhRate.style.display = 'flex';
            els.currentLgtRfdFhRate.textContent = data.lgtRfdFhRate.display ? `${data.lgtRfdFhRate.display}%` : '-';
          } else {
            els.rowLgtRfdFhRate.style.display = 'none';
          }

          // 品质体验指标
          if (data.qualityRfdRate) {
            els.rowQualityRfdRate.style.display = 'flex';
            els.currentQualityRfdRate.textContent = data.qualityRfdRate.display ? `${data.qualityRfdRate.display}%` : '-';
          } else {
            els.rowQualityRfdRate.style.display = 'none';
          }

          if (data.qualityBadRate) {
            els.rowQualityBadRate.style.display = 'flex';
            els.currentQualityBadRate.textContent = data.qualityBadRate.display ? `${data.qualityBadRate.display}%` : '-';
          } else {
            els.rowQualityBadRate.style.display = 'none';
          }

          // 新灯塔综合评分
          if (data.nlhScore) {
            els.rowNlhScore.style.display = 'flex';
            els.currentNlhScore.textContent = `${data.nlhScore.score}${data.nlhScore.title ? ' · ' + data.nlhScore.title : ''}`;
          } else {
            els.rowNlhScore.style.display = 'none';
          }

          if (data.qualityScore) {
            els.rowQualityScore.style.display = 'flex';
            els.currentQualityScore.textContent = `${data.qualityScore.score}${data.qualityScore.title ? ' · ' + data.qualityScore.title : ''}`;
          } else {
            els.rowQualityScore.style.display = 'none';
          }

          if (data.refundScore) {
            els.rowRefundScore.style.display = 'flex';
            els.currentRefundScore.textContent = `${data.refundScore.score}${data.refundScore.title ? ' · ' + data.refundScore.title : ''}`;
          } else {
            els.rowRefundScore.style.display = 'none';
          }

          // 隐藏其他页面类型数据
          els.rowCompanyName.style.display = 'none';
          els.rowRank.style.display = 'none';
          els.rowPayAmt.style.display = 'none';
          els.rowItemCnt.style.display = 'none';
          els.rowPullSales.style.display = 'none';
          els.rowRevealCnt.style.display = 'none';
          els.rowFlowPv.style.display = 'none';
          els.rowClickRate.style.display = 'none';
          els.rowBounceRate.style.display = 'none';
          els.rowMobileShare.style.display = 'none';
          els.rowInquiry.style.display = 'none';
          els.rowFlowSourceRecent7.style.display = 'none';
          els.rowKeywordsRecent7.style.display = 'none';
          els.rowTradePay.style.display = 'none';
          els.rowTradePayByr.style.display = 'none';
          els.rowTradePayQty.style.display = 'none';
          els.rowTradePayRate.style.display = 'none';
          els.rowTradePerAmt.style.display = 'none';
          els.rowTradeRefund.style.display = 'none';
          els.rowTradeRefundRate.style.display = 'none';
          els.rowTradeMord.style.display = 'none';
          els.rowTradeNewBuyer.style.display = 'none';
        } else if (data._pageType === 'sycm') {
          // 生意参谋页面：显示公司名、排名、支付金额、商品概况
          els.rowPageCount.style.display = 'none';
          els.rowWwResponse.style.display = 'none';
          els.rowWwSatisfaction.style.display = 'none';
          els.rowLgt48hGotRate.style.display = 'none';
          els.rowLgtFulfillRate.style.display = 'none';
          els.rowLgtPlanAccRate.style.display = 'none';
          els.rowLgtRfdFhRate.style.display = 'none';
          els.rowQualityRfdRate.style.display = 'none';
          els.rowQualityBadRate.style.display = 'none';
          els.rowNlhScore.style.display = 'none';
          els.rowQualityScore.style.display = 'none';
          els.rowRefundScore.style.display = 'none';
          els.rowQualityRfdRate.style.display = 'none';
          els.rowQualityBadRate.style.display = 'none';
          els.rowNlhScore.style.display = 'none';
          els.rowQualityScore.style.display = 'none';
          els.rowRefundScore.style.display = 'none';
          els.rowCompanyName.style.display = 'flex';
          els.currentCompanyName.textContent = data.companyName || '未获取';

          if (data.rankTrend) {
            els.rowRank.style.display = 'flex';
            els.rowPayAmt.style.display = 'flex';
            const cate2 = data.rankTrend.cateLevel2 || '';
            const layer = data.rankTrend.layer ?? '';
            const layerText = layer ? `第${layer}层级` : '';
            els.currentRank.textContent = layerText
              ? `${layerText} · 第${data.rankTrend.rank}名${cate2 ? ' · ' + cate2 : ''}`
              : `${cate2 || '主营类目'} 第${data.rankTrend.rank}名`;
            els.currentPayAmt.textContent = `¥${data.rankTrend.payAmt}`;
          } else {
            els.rowRank.style.display = 'none';
            els.rowPayAmt.style.display = 'none';
          }

          if (data.itemOverview) {
            els.rowItemCnt.style.display = 'flex';
            els.rowPullSales.style.display = 'flex';
            els.currentItemCnt.textContent = data.itemOverview.itemCnt ?? '-';
            els.currentPullSales.textContent = data.itemOverview.pullSalesItemCnt ?? '-';
          } else {
            els.rowItemCnt.style.display = 'none';
            els.rowPullSales.style.display = 'none';
          }

          if (data.flowStats) {
            els.rowRevealCnt.style.display = 'flex';
            els.rowFlowPv.style.display = 'flex';
            els.rowClickRate.style.display = 'flex';
            els.rowBounceRate.style.display = 'flex';
            els.rowMobileShare.style.display = 'flex';
            els.currentRevealCnt.textContent = data.flowStats.revealCnt ?? '-';
            els.currentFlowPv.textContent = `${data.flowStats.pv ?? '-'}/${data.flowStats.uv ?? '-'}`;
            els.currentClickRate.textContent = data.flowStats.clickRate ? `${(data.flowStats.clickRate * 100).toFixed(2)}%` : '-';
            els.currentBounceRate.textContent = data.flowStats.bounceRate ? `${(data.flowStats.bounceRate * 100).toFixed(2)}%` : '-';
            els.currentMobileShare.textContent = data.flowStats.mobileShare ? `${(data.flowStats.mobileShare * 100).toFixed(2)}%` : '-';
          } else {
            els.rowRevealCnt.style.display = 'none';
            els.rowFlowPv.style.display = 'none';
            els.rowClickRate.style.display = 'none';
            els.rowBounceRate.style.display = 'none';
            els.rowMobileShare.style.display = 'none';
          }

          if (data.inquiry) {
            els.rowInquiry.style.display = 'flex';
            els.currentInquiry.textContent = data.inquiry.effectiveInQUsers ?? '-';
          } else {
            els.rowInquiry.style.display = 'none';
          }

          // 近7天流量来源
          if (data.flowSourceRecent7 && data.flowSourceRecent7.sources && data.flowSourceRecent7.sources.length > 0) {
            els.rowFlowSourceRecent7.style.display = 'flex';
            // 只取一级来源（outerLevel=1）用于摘要展示
            const level1 = data.flowSourceRecent7.sources.filter(s => s.outerLevel === 1);
            const top3 = level1.slice(0, 3);
            const totalUv = data.flowSourceRecent7.totalMyUv || 1;
            els.currentFlowSourceRecent7.textContent = top3.map(s => {
              const share = totalUv > 0 && s.uv ? ((s.uv / totalUv) * 100).toFixed(1) + '%' : '-';
              const payInfo = s.fleadPayAmt !== null ? ` 支付¥${s.fleadPayAmt.toFixed(0)}` : '';
              return `${s.name || '未知'}:${s.uv ?? '-'}(${share})${payInfo}`;
            }).join(' · ');
          } else {
            els.rowFlowSourceRecent7.style.display = 'none';
          }

          // 近7天入店关键词
          if (data.keywordsRecent7 && data.keywordsRecent7.keywords && data.keywordsRecent7.keywords.length > 0) {
            els.rowKeywordsRecent7.style.display = 'flex';
            const top3 = data.keywordsRecent7.keywords.slice(0, 3);
            const totalPay7 = data.tradeRecent7?.payAmt || 1;
            els.currentKeywordsRecent7.textContent = top3.map(k => {
              const payShare = totalPay7 > 0 && k.leadPayAmt ? ((k.leadPayAmt / totalPay7) * 100).toFixed(1) + '%' : '-';
              return `${k.keyword || '未知'}:${k.keywordRevealCnt ?? '-'}/${k.uv ?? '-'}(${payShare})`;
            }).join(' · ');
          } else {
            els.rowKeywordsRecent7.style.display = 'none';
          }

          if (data.trade) {
            els.rowTradePay.style.display = 'flex';
            els.rowTradePayByr.style.display = 'flex';
            els.rowTradePayQty.style.display = 'flex';
            els.rowTradePayRate.style.display = 'flex';
            els.rowTradePerAmt.style.display = 'flex';
            els.rowTradeRefund.style.display = 'flex';
            els.rowTradeRefundRate.style.display = 'flex';
            els.rowTradeMord.style.display = 'flex';
            els.rowTradeNewBuyer.style.display = 'flex';
            els.currentTradePay.textContent = `¥${data.trade.payAmt ?? '-'}`;
            els.currentTradePayByr.textContent = data.trade.payByrCnt ?? '-';
            els.currentTradePayQty.textContent = data.trade.payItemQty ?? '-';
            els.currentTradePayRate.textContent = data.trade.payRate !== null ? `${(data.trade.payRate * 100).toFixed(2)}%` : '-';
            els.currentTradePerAmt.textContent = data.trade.perByrAmt ? `¥${data.trade.perByrAmt}` : '-';
            els.currentTradeRefund.textContent = `¥${data.trade.rfdSucAmt ?? 0}`;
            els.currentTradeRefundRate.textContent = data.trade.refundRate !== null ? `${(data.trade.refundRate * 100).toFixed(2)}%` : '-';
            els.currentTradeMord.textContent = data.trade.payMordCnt ?? '-';
            els.currentTradeNewBuyer.textContent = data.trade.payNewByrCnt ?? '-';
          } else {
            els.rowTradePay.style.display = 'none';
            els.rowTradePayByr.style.display = 'none';
            els.rowTradePayQty.style.display = 'none';
            els.rowTradePayRate.style.display = 'none';
            els.rowTradePerAmt.style.display = 'none';
            els.rowTradeRefund.style.display = 'none';
            els.rowTradeRefundRate.style.display = 'none';
          }
        } else {
          // 非生意参谋页面：隐藏 sycm 行，显示采集数量
          els.rowPageCount.style.display = 'flex';
          els.rowCompanyName.style.display = 'none';
          els.rowRank.style.display = 'none';
          els.rowPayAmt.style.display = 'none';
          els.rowItemCnt.style.display = 'none';
          els.rowPullSales.style.display = 'none';
          els.rowRevealCnt.style.display = 'none';
          els.rowFlowPv.style.display = 'none';
          els.rowClickRate.style.display = 'none';
          els.rowBounceRate.style.display = 'none';
          els.rowMobileShare.style.display = 'none';
          els.rowInquiry.style.display = 'none';
          els.rowFlowSourceRecent7.style.display = 'none';
          els.rowKeywordsRecent7.style.display = 'none';
          els.rowTradePay.style.display = 'none';
          els.rowTradePayByr.style.display = 'none';
          els.rowTradePayQty.style.display = 'none';
          els.rowTradePayRate.style.display = 'none';
          els.rowTradePerAmt.style.display = 'none';
          els.rowTradeRefund.style.display = 'none';
          els.rowTradeRefundRate.style.display = 'none';
          els.rowTradeMord.style.display = 'none';
          els.rowTradeNewBuyer.style.display = 'none';
          els.rowWwResponse.style.display = 'none';
          els.rowWwSatisfaction.style.display = 'none';
          els.rowLgt48hGotRate.style.display = 'none';
          els.rowLgtFulfillRate.style.display = 'none';
          els.rowLgtPlanAccRate.style.display = 'none';
          els.rowLgtRfdFhRate.style.display = 'none';
          els.rowQualityRfdRate.style.display = 'none';
          els.rowQualityBadRate.style.display = 'none';
          els.rowNlhScore.style.display = 'none';
          els.rowQualityScore.style.display = 'none';
          els.rowRefundScore.style.display = 'none';
          els.rowQualityRfdRate.style.display = 'none';
          els.rowQualityBadRate.style.display = 'none';
          els.rowNlhScore.style.display = 'none';
          els.rowQualityScore.style.display = 'none';
          els.rowRefundScore.style.display = 'none';

          if (data._pageType === 'detail') {
            els.currentPageCount.textContent = '1条详情';
          } else if (data._pageType === 'list') {
            els.currentPageCount.textContent = `${data.items?.length || 0}条列表`;
          }
        }
      } else {
        els.rowPageCount.style.display = 'flex';
        els.rowCompanyName.style.display = 'none';
        els.rowRank.style.display = 'none';
        els.rowPayAmt.style.display = 'none';
        els.rowItemCnt.style.display = 'none';
        els.rowPullSales.style.display = 'none';
        els.rowRevealCnt.style.display = 'none';
        els.rowFlowPv.style.display = 'none';
        els.rowClickRate.style.display = 'none';
        els.rowBounceRate.style.display = 'none';
        els.rowMobileShare.style.display = 'none';
        els.rowInquiry.style.display = 'none';
        els.rowFlowSourceRecent7.style.display = 'none';
        els.rowKeywordsRecent7.style.display = 'none';
        els.rowTradePay.style.display = 'none';
        els.rowTradePayByr.style.display = 'none';
        els.rowTradePayQty.style.display = 'none';
        els.rowTradePayRate.style.display = 'none';
        els.rowTradePerAmt.style.display = 'none';
        els.rowTradeRefund.style.display = 'none';
        els.rowTradeRefundRate.style.display = 'none';
        els.rowTradeMord.style.display = 'none';
        els.rowTradeNewBuyer.style.display = 'none';
        els.rowWwResponse.style.display = 'none';
        els.rowWwSatisfaction.style.display = 'none';
        els.rowLgt48hGotRate.style.display = 'none';
        els.rowLgtFulfillRate.style.display = 'none';
        els.rowLgtPlanAccRate.style.display = 'none';
        els.rowLgtRfdFhRate.style.display = 'none';
        els.rowQualityRfdRate.style.display = 'none';
        els.rowQualityBadRate.style.display = 'none';
        els.rowNlhScore.style.display = 'none';
        els.rowQualityScore.style.display = 'none';
        els.rowRefundScore.style.display = 'none';
        els.currentPageCount.textContent = '未采集';
      }
    } catch (e) {
      els.rowPageCount.style.display = 'flex';
      els.rowCompanyName.style.display = 'none';
      els.rowRank.style.display = 'none';
      els.rowPayAmt.style.display = 'none';
      els.rowItemCnt.style.display = 'none';
      els.rowPullSales.style.display = 'none';
      els.rowRevealCnt.style.display = 'none';
      els.rowFlowPv.style.display = 'none';
      els.rowClickRate.style.display = 'none';
      els.rowBounceRate.style.display = 'none';
      els.rowMobileShare.style.display = 'none';
      els.rowInquiry.style.display = 'none';
      els.rowFlowSourceRecent7.style.display = 'none';
      els.rowTradePay.style.display = 'none';
      els.rowTradePayByr.style.display = 'none';
      els.rowTradePayQty.style.display = 'none';
      els.rowTradePayRate.style.display = 'none';
      els.rowTradePerAmt.style.display = 'none';
      els.rowTradeRefund.style.display = 'none';
      els.rowTradeRefundRate.style.display = 'none';
      els.rowTradeMord.style.display = 'none';
      els.rowTradeNewBuyer.style.display = 'none';
      els.rowWwResponse.style.display = 'none';
      els.rowWwSatisfaction.style.display = 'none';
      els.rowLgt48hGotRate.style.display = 'none';
      els.rowLgtFulfillRate.style.display = 'none';
      els.rowLgtPlanAccRate.style.display = 'none';
      els.rowLgtRfdFhRate.style.display = 'none';
      els.rowQualityRfdRate.style.display = 'none';
      els.rowQualityBadRate.style.display = 'none';
      els.rowNlhScore.style.display = 'none';
      els.rowQualityScore.style.display = 'none';
      els.rowRefundScore.style.display = 'none';
      els.currentPageCount.textContent = '需刷新页面';
    }
  } else {
    els.pageInfo.style.display = 'none';
  }
}

// 立即采集
async function triggerClaw() {
  const tab = await getCurrentTab();
  if (!tab) {
    showToast('无法获取当前标签页');
    return;
  }

  const pageType = detect1688PageType(tab.url);
  if (pageType === 'not_1688') {
    showToast('请在1688页面使用');
    return;
  }

  setLoading(true);
  setStatus('warning', '采集中...');

  try {
    // 先通知content script采集
    const contentResponse = await chrome.tabs.sendMessage(tab.id, { action: 'TRIGGER_CLAW' });
    console.log('Content script响应:', contentResponse);

    // 等待数据同步到storage（sycm页面需要更多时间，因为有两个API调用）
    await new Promise(r => setTimeout(r, 3000));

    // 更新统计显示
    await updateStats();
    await updatePageInfo();

    setStatus('active', '采集完成');
    showToast('数据采集成功！');
  } catch (e) {
    console.error('采集失败:', e);
    setStatus('error', '采集失败');
    showToast('采集失败: ' + e.message);
  } finally {
    setLoading(false);
  }
}

// 清空数据
async function clearData() {
  if (!confirm('确定要清空所有采集数据吗？此操作不可恢复。')) return;

  try {
    await chrome.runtime.sendMessage({ action: 'CLEAR_DATA' });
    await updateStats();
    showToast('数据已清空');
  } catch (e) {
    showToast('清空失败: ' + e.message);
  }
}

// 初始化
async function init() {
  // 获取扩展ID
  const extId = chrome.runtime.id;
  els.extensionId.textContent = extId;
  els.apiCode.textContent = `// OpenClaw 调用示例
chrome.runtime.sendMessage('ekmgnempbbamlmaolijdfjakeopniion', {
  action: 'OPEN_CLAW_API',
  mode: 'full'   // 'full' | 'sycm' | 'work' | 'summary'
}, (response) => {
  console.log(response.data);
});`;

  // 检查状态
  setStatus('active', '就绪');

  // 更新数据
  await updateStats();
  await updatePageInfo();

  // 绑定事件
  els.btnClaw.addEventListener('click', triggerClaw);
  els.btnClear.addEventListener('click', clearData);
}

// 启动
document.addEventListener('DOMContentLoaded', init);
