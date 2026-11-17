(function () {
  'use strict';

  // ============================================================
  // 1688 Data Claw - Content Script
  // 负责在1688页面中自动提取商品数据
  // ============================================================

  const CLAW_VERSION = '1.0.0';
  const DEBUG = true;

  function log(...args) {
    if (DEBUG) console.log('[1688-Claw]', ...args);
  }

  // --- 工具函数 ---
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const text = (el) => el ? el.textContent.trim() : '';
  const attr = (el, name) => el ? el.getAttribute(name) : '';

  // 提取价格数字
  function extractPrice(str) {
    if (!str) return null;
    const match = str.match(/(\d+(?:\.\d+)?)/);
    return match ? parseFloat(match[1]) : null;
  }

  // 提取商品ID from URL
  function extractOfferId(url) {
    if (!url) return null;
    const match = url.match(/offer\/(\d+)\.html/);
    return match ? match[1] : null;
  }

  // 安全JSON序列化
  function safeStringify(obj) {
    try {
      return JSON.stringify(obj);
    } catch (e) {
      return '{}';
    }
  }

  // --- 页面类型检测 ---
  function detectPageType() {
    const url = location.href;
    if (url.includes('work.1688.com')) {
      return 'work';
    }
    if (url.includes('sycm.1688.com')) {
      return 'sycm';
    }
    if (url.includes('/offer/') && /offer\/\d+\.html/.test(url)) {
      return 'detail';
    }
    if (url.includes('s.1688.com') || url.includes('search')) {
      return 'search_list';
    }
    if (url.includes('shop')) {
      return 'shop_list';
    }
    if (url.includes('detail.1688.com')) {
      return 'detail';
    }
    return 'unknown';
  }

  // 辅助函数：从灯塔 indexSet 中提取指定指标的最新数据
  function extractIndexFromSet(indexSet, indexCode) {
    const idx = indexSet.find(i => i.indexCode === indexCode);
    if (!idx || !idx.indexList || idx.indexList.length === 0) return null;
    const last = idx.indexList[idx.indexList.length - 1];
    return {
      score: last.score ?? null,
      display: last.display ?? '',
      time: last.time ?? '',
      averageScore: idx.averageScore ?? '',
      excellentScore: idx.excellentScore ?? '',
      name: idx.name ?? '',
      define: idx.define ?? '',
      unit: idx.unit ?? ''
    };
  }

  // 辅助函数：提取1688账号唯一标识（从cookie或回退到URL）
  function extractAccountId() {
    const getCookie = (name) => {
      const match = document.cookie.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
      return match ? match[1] : '';
    };
    // 尝试按优先级提取稳定账号标识
    const loginId = getCookie('loginId');
    if (loginId) return 'login_' + loginId;
    const unb = getCookie('unb');
    if (unb) return 'unb_' + unb;
    const memberId = getCookie('memberId');
    if (memberId) return 'member_' + memberId;
    const m_h5_tk = getCookie('_m_h5_tk');
    if (m_h5_tk) {
      const token = m_h5_tk.split('_')[0];
      if (token) return 'token_' + token;
    }
    // 回退到URL（域名级别，避免不同路径产生新条目）
    return location.host;
  }

  // 通用请求：获取工作台灯塔模块数据（带 moduleCode）
  async function fetchWorkModule(token, moduleCode) {
    const appKey = '12574478';
    const timestamp = Date.now();
    const dataObj = {
      terminalType: 'work',
      accountType: '1688',
      ref: '{}',
      bizParams: '{}',
      routingDataType: 'POSTMAN',
      dataPlans: JSON.stringify({
        CDT_7nkFnu: {
          items: ['queryServiceExperienceModuleData'],
          params: {
            queryServiceExperienceModuleData: { moduleCode: moduleCode }
          }
        }
      })
    };
    const dataStr = JSON.stringify(dataObj);
    const sign = window.__CLAW_MD5__.getAliSign(token, timestamp, appKey, dataStr);

    const apiUrl = `https://h5api.m.1688.com/h5/mtop.alibaba.cbu.workdiordatareaderservice.getvaluesfromgateway/1.0/?jsv=2.7.2&appKey=${appKey}&t=${timestamp}&sign=${sign}&api=mtop.alibaba.cbu.WorkDiorDataReaderService.getValuesFromGateway&v=1.0&type=originaljson&dataType=json&jsonpIncPrefix=dior_fetch_data_${timestamp}`;

    const resp = await fetch(apiUrl, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `data=${encodeURIComponent(dataStr)}`
    });
    const json = await resp.json();
    return json;
  }

  // 通用请求：获取工作台新灯塔综合分/评分概况
  async function fetchWorkScore(token) {
    const appKey = '12574478';
    const timestamp = Date.now();
    const dataObj = {
      terminalType: 'work',
      accountType: '1688',
      ref: '{}',
      bizParams: '{}',
      routingDataType: 'POSTMAN',
      dataPlans: JSON.stringify({
        CDT_7nkFnu: {
          items: ['queryNlhScoreAndBenefitsData'],
          params: {
            queryNlhScoreAndBenefitsData: {}
          }
        }
      })
    };
    const dataStr = JSON.stringify(dataObj);
    const sign = window.__CLAW_MD5__.getAliSign(token, timestamp, appKey, dataStr);

    const apiUrl = `https://h5api.m.1688.com/h5/mtop.alibaba.cbu.workdiordatareaderservice.getvaluesfromgateway/1.0/?jsv=2.7.2&appKey=${appKey}&t=${timestamp}&sign=${sign}&api=mtop.alibaba.cbu.WorkDiorDataReaderService.getValuesFromGateway&v=1.0&type=originaljson&dataType=json&jsonpIncPrefix=dior_fetch_data_${timestamp}`;

    const resp = await fetch(apiUrl, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `data=${encodeURIComponent(dataStr)}`
    });
    const json = await resp.json();
    return json;
  }

  // --- 1688 工作台 (work.1688.com) 数据采集 ---
  async function extractWorkPage() {
    const url = location.href;
    const result = {
      _clawVersion: CLAW_VERSION,
      _crawledAt: new Date().toISOString(),
      _pageType: 'work',
      url,
      accountId: extractAccountId(),
      // 旺旺服务
      wwResponse: null,
      wwSatisfaction: null,
      // 物流体验
      lgt48hGotRate: null,      // 48H揽收率
      lgtFulfillRate: null,     // 履约率
      lgtPlanAccRate: null,     // 物流时效达成率
      lgt72hReceiveRate: null,  // 72H支签率
      lgtFulfillDzRate: null,   // 定制品履约率
      lgtRfdFhRate: null,       // 物流发货退款率
      // 品质体验
      qualityRfdRate: null,     // 品质退款率
      qualityBadRate: null,     // 商品品质差评率
      // 新灯塔综合评分
      nlhScore: null,           // 新灯塔综合分
      qualityScore: null,       // 商品体验
      refundScore: null,        // 售后体验
      lgtScore: null,           // 物流体验
      wwScore: null,            // 咨询体验
      starScore: null,          // 星级
      cateLvl1Name: '',         // 主营一级类目
      benefitsUnlocked: [],     // 已解锁权益
      benefitsUnlockedPending: [], // 未解锁权益
      source: '1688-work'
    };

    try {
      // 1. 获取 _m_h5_tk cookie
      const getCookie = (name) => {
        const match = document.cookie.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
        return match ? match[1] : '';
      };
      const m_h5_tk = getCookie('_m_h5_tk');
      if (!m_h5_tk) {
        log('工作台采集: 未找到 _m_h5_tk cookie');
        return result;
      }
      const token = m_h5_tk.split('_')[0];
      log('工作台 token:', token);

      // 2. 并行请求四个接口：旺旺模块 + 物流模块 + 品质模块 + 新灯塔综合评分
      const [wwJson, lgtJson, qualityJson, scoreJson] = await Promise.all([
        fetchWorkModule(token, 'shop_ww_response').catch(e => {
          log('旺旺模块请求失败:', e);
          return null;
        }),
        fetchWorkModule(token, 'shop_lgt').catch(e => {
          log('物流模块请求失败:', e);
          return null;
        }),
        fetchWorkModule(token, 'shop_quality').catch(e => {
          log('品质模块请求失败:', e);
          return null;
        }),
        fetchWorkScore(token).catch(e => {
          log('评分概况请求失败:', e);
          return null;
        })
      ]);

      // 3. 提取旺旺服务数据
      if (wwJson && wwJson.ret && wwJson.ret[0] && wwJson.ret[0].includes('SUCCESS')) {
        const cdt = wwJson.data?.CDT_7nkFnu;
        const value = cdt?.values?.queryServiceExperienceModuleData?.value?.returnValue;
        if (value && value.indexSet) {
          const indexSet = value.indexSet;
          result.wwResponse = extractIndexFromSet(indexSet, 'shop_sns_ww_response_rate_30d');
          result.wwSatisfaction = extractIndexFromSet(indexSet, 'shop_sns_good_ax_rate_30d_v2');
          log('工作台[旺旺]采集成功:', '响应率', result.wwResponse?.score, '满意度', result.wwSatisfaction?.score);
        }
      } else {
        log('工作台[旺旺] API 返回失败:', wwJson?.ret);
      }

      // 4. 提取物流体验数据
      if (lgtJson && lgtJson.ret && lgtJson.ret[0] && lgtJson.ret[0].includes('SUCCESS')) {
        const cdt = lgtJson.data?.CDT_7nkFnu;
        const value = cdt?.values?.queryServiceExperienceModuleData?.value?.returnValue;
        if (value && value.indexSet) {
          const indexSet = value.indexSet;
          result.lgt48hGotRate = extractIndexFromSet(indexSet, 'shop_nps_lgt_48h_got_rate_30d');
          result.lgtFulfillRate = extractIndexFromSet(indexSet, 'shop_lgt_fulfill_got_rate_30d');
          result.lgtPlanAccRate = extractIndexFromSet(indexSet, 'shop_shop_lgt_plan_acc_rate_30d');
          result.lgt72hReceiveRate = extractIndexFromSet(indexSet, 'shop_nps_lgt_72h_receive_rate_30d');
          result.lgtFulfillDzRate = extractIndexFromSet(indexSet, 'shop_nps_lgt_fulfill_got_dz_rate_30d');
          result.lgtRfdFhRate = extractIndexFromSet(indexSet, 'shop_rfd_lgt_fh_ord_rate_30d_v1');
          log('工作台[物流]采集成功:', '48H揽收', result.lgt48hGotRate?.score, '履约率', result.lgtFulfillRate?.score);
        }
      } else {
        log('工作台[物流] API 返回失败:', lgtJson?.ret);
      }

      // 5. 提取品质体验数据
      if (qualityJson && qualityJson.ret && qualityJson.ret[0] && qualityJson.ret[0].includes('SUCCESS')) {
        const cdt = qualityJson.data?.CDT_7nkFnu;
        const value = cdt?.values?.queryServiceExperienceModuleData?.value?.returnValue;
        if (value && value.indexSet) {
          const indexSet = value.indexSet;
          result.qualityRfdRate = extractIndexFromSet(indexSet, 'shop_rfd_quality_ord_rate_30d');
          result.qualityBadRate = extractIndexFromSet(indexSet, 'shop_itm_quality_mord_cnt_30d_rate_v1');
          log('工作台[品质]采集成功:', '品质退款率', result.qualityRfdRate?.score, '商品品质差评率', result.qualityBadRate?.score);
        }
      } else {
        log('工作台[品质] API 返回失败:', qualityJson?.ret);
      }

      // 6. 提取新灯塔综合评分
      if (scoreJson && scoreJson.ret && scoreJson.ret[0] && scoreJson.ret[0].includes('SUCCESS')) {
        const cdt = scoreJson.data?.CDT_7nkFnu;
        const value = cdt?.values?.queryNlhScoreAndBenefitsData?.value?.returnValue;
        if (value) {
          result.cateLvl1Name = value.cateLvl1Name || '';
          const scoreList = value.moduleServiceScoreModelList || [];
          scoreList.forEach(item => {
            if (item.code === 'shop_nps_service_score_total') {
              result.nlhScore = { score: item.score, name: item.name, title: item.title, copyWriting: item.copyWriting };
            } else if (item.code === 'shop_quality') {
              result.qualityScore = { score: item.score, name: item.name, title: item.title, proportionSuffix: item.proportionSuffix, copyWriting: item.copyWriting };
            } else if (item.code === 'shop_refund') {
              result.refundScore = { score: item.score, name: item.name, title: item.title, proportionSuffix: item.proportionSuffix, copyWriting: item.copyWriting };
            } else if (item.code === 'shop_lgt') {
              result.lgtScore = { score: item.score, name: item.name, title: item.title, proportionSuffix: item.proportionSuffix, copyWriting: item.copyWriting };
            } else if (item.code === 'shop_ww_response') {
              result.wwScore = { score: item.score, name: item.name, title: item.title, proportionSuffix: item.proportionSuffix, copyWriting: item.copyWriting };
            } else if (item.code === 'shop_star') {
              result.starScore = { score: item.score, name: item.name, title: item.title, copyWriting: item.copyWriting };
            }
          });
          result.benefitsUnlocked = (value.unlockedBenefits || []).map(b => b.display || '');
          result.benefitsUnlockedPending = (value.unUnLockedBenefits || []).map(b => b.display || '');
          log('工作台[评分]采集成功:', '新灯塔分', result.nlhScore?.score, '商品', result.qualityScore?.score, '售后', result.refundScore?.score);
        }
      } else {
        log('工作台[评分] API 返回失败:', scoreJson?.ret);
      }
    } catch (e) {
      log('工作台采集失败:', e);
    }

    return result;
  }

  // --- 生意参谋 (sycm) 数据采集 ---
  async function extractSycmPage() {
    const url = location.href;
    const timestamp = Date.now();
    const infoUrl = `https://sycm.1688.com/ms/common/information.json?_=${timestamp}`;

    const result = {
      _clawVersion: CLAW_VERSION,
      _crawledAt: new Date().toISOString(),
      _pageType: 'sycm',
      url,
      companyName: '',
      companyUrl: '',
      category: '',
      subCategory: '',
      identity: '',
      competeVersion: '',
      isSvip: false,
      hasSigned: false,
      isSudo: false,
      rawUser: null,
      rawDiamond: null,
      pageData: {},
      source: '1688-sycm'
    };

    // 1. 从 API 获取用户信息
    try {
      const resp = await fetch(infoUrl, {
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      const json = await resp.json();

      if (json.code === 0 && json.data) {
        const userData = json.data.user;
        const runAs = userData && userData.runAs ? userData.runAs : null;

        if (runAs) {
          result.companyName = runAs.companyName || '';
          result.companyUrl = runAs.homepageUrl || '';
          result.identity = runAs.identity || '';
          result.competeVersion = runAs.competeVersion || '';
          result.isSvip = runAs.identity === 'svip';

          if (runAs.cate) {
            result.category = runAs.cate.name || '';
            if (runAs.cate.subCate) {
              result.subCategory = runAs.cate.subCate.name || '';
            }
          }
        }

        result.hasSigned = userData && userData.hasSigned === true;
        result.isSudo = json.data.site && json.data.site.isSudo === true;
        result.rawUser = json.data.user;
        result.rawDiamond = json.data.diamond;
      }
    } catch (e) {
      log('生意参谋 API 获取失败:', e);
    }

    // 2. 从 shopRankTrend 获取店铺排名趋势（先尝试今天，失败则兜底昨天）
    try {
      const pad = (n) => String(n).padStart(2, '0');
      const makeDate = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
      const today = new Date();
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const dateCandidates = [makeDate(today), makeDate(yesterday)];

      let trendJson = null;
      for (const dateStr of dateCandidates) {
        const trendUrl = `https://sycm.1688.com/ms/portal/shopRankTrend.json?dateType=day&dateRange=${dateStr}|${dateStr}&_=${timestamp}`;
        const trendResp = await fetch(trendUrl, {
          credentials: 'include',
          headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          }
        });
        trendJson = await trendResp.json();
        if (trendJson.code === 0 && trendJson.data) {
          log('排名趋势 API 成功:', dateStr);
          break;
        }
        log('排名趋势 API 失败:', dateStr, trendJson.message || trendJson.code);
      }

      if (trendJson.code === 0 && trendJson.data) {
        const d = trendJson.data;
        const len = d.statDate?.length || 0;
        if (len > 0) {
          const lastIdx = len - 1;
          // 转换时间戳为日期
          const ts = d.statDate[lastIdx];
          const lastDate = new Date(ts);
          const lastDateStr = `${lastDate.getFullYear()}-${pad(lastDate.getMonth() + 1)}-${pad(lastDate.getDate())}`;

          result.rankTrend = {
            lastDate: lastDateStr,
            rank: d.rank?.[lastIdx] ?? null,
            payAmt: d.payAmt?.[lastIdx] ?? null,
            cateLevel1: d.cateLevel1Name?.[lastIdx] ?? '',
            cateLevel2: d.cateLevel2Name?.[lastIdx] ?? '',
            cateLevel1Id: d.cateLevel1Id?.[lastIdx] ?? null,
            cateLevel2Id: d.cateLevel2Id?.[lastIdx] ?? null,
            layer: d.mainCate1Layer?.[lastIdx] ?? null,
            // 原始30天数据保留，供外部分析
            rawDates: d.statDate,
            rawRanks: d.rank,
            rawPayAmt: d.payAmt,
            rawCateLevel2: d.cateLevel2Name
          };

          log('排名趋势提取成功:', lastDateStr, '排名', result.rankTrend.rank, '金额', result.rankTrend.payAmt);
        }
      }
    } catch (e) {
      log('排名趋势 API 获取失败:', e);
    }

    // 3. 从 itemCoreIndexOverview 获取昨日商品概况
    try {
      const pad = (n) => String(n).padStart(2, '0');
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayStr = `${yesterday.getFullYear()}-${pad(yesterday.getMonth() + 1)}-${pad(yesterday.getDate())}`;
      const overviewUrl = `https://sycm.1688.com/ms/item/itemCoreIndexOverview.json?device=0&dateType=day&dateRange=${yesterdayStr}|${yesterdayStr}&_=${timestamp}`;

      const overviewResp = await fetch(overviewUrl, {
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      const overviewJson = await overviewResp.json();

      if (overviewJson.code === 0 && overviewJson.data) {
        const d = overviewJson.data;
        result.itemOverview = {
          statDate: d.statDate?.value ? new Date(d.statDate.value).toISOString().slice(0, 10) : yesterdayStr,
          itemCnt: d.itemCnt?.value ?? null,
          pullSalesItemCnt: d.pullSalesItemCnt?.value ?? null,
          uv: d.uv?.value ?? null,
          payItemQty: d.payItemQty?.value ?? null,
          hasVisitorItemCnt: d.hasVisitorItemCnt?.value ?? null,
          itemPv: d.itemPv?.value ?? null,
          raw: d
        };
        log('商品概况提取成功:', 'itemCnt', result.itemOverview.itemCnt, '动销', result.itemOverview.pullSalesItemCnt);
      }
    } catch (e) {
      log('商品概况 API 获取失败:', e);
    }

    // 4. 从 ovralShopFlowSource/overview 获取昨日流量统计
    try {
      const pad = (n) => String(n).padStart(2, '0');
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayStr = `${yesterday.getFullYear()}-${pad(yesterday.getMonth() + 1)}-${pad(yesterday.getDate())}`;
      const indexCode = 'revealCnt,adRevealCnt,uv,zgcUv,pv,zgcPv,bounceRate,bUv,bPv,avgPvs,adGuidPv,payByrCnt,payAmt';

      // 全平台
      const allDeviceUrl = `https://sycm.1688.com/ms/flow/ovralShopFlowSource/overview.json?dateType=day&dateRange=${yesterdayStr}|${yesterdayStr}&device=0&indexCode=${indexCode}&_=${timestamp}`;
      const allResp = await fetch(allDeviceUrl, {
        credentials: 'include',
        headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }
      });
      const allJson = await allResp.json();

      // 无线端
      const mobileUrl = `https://sycm.1688.com/ms/flow/ovralShopFlowSource/overview.json?dateType=day&dateRange=${yesterdayStr}|${yesterdayStr}&device=2&indexCode=${indexCode}&_=${timestamp}`;
      const mobileResp = await fetch(mobileUrl, {
        credentials: 'include',
        headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }
      });
      const mobileJson = await mobileResp.json();

      let allData = null;
      let mobileData = null;

      if (allJson.code === 0 && allJson.data) {
        const d = allJson.data;
        allData = {
          statDate: d.statDate?.value ? new Date(d.statDate.value).toISOString().slice(0, 10) : yesterdayStr,
          revealCnt: d.revealCnt?.value ?? null,
          pv: d.pv?.value ?? null,
          uv: d.uv?.value ?? null,
          bounceRate: d.bounceRate?.value ?? null,
          payByrCnt: d.payByrCnt?.value ?? null,
          payAmt: d.payAmt?.value ?? null,
          raw: d
        };
      }

      if (mobileJson.code === 0 && mobileJson.data) {
        const d = mobileJson.data;
        mobileData = {
          uv: d.uv?.value ?? null,
          pv: d.pv?.value ?? null,
          raw: d
        };
      }

      if (allData) {
        const revealCnt = allData.revealCnt || 0;
        const pv = allData.pv || 0;
        const uv = allData.uv || 0;
        const mobileUv = mobileData?.uv || 0;

        result.flowStats = {
          statDate: allData.statDate,
          revealCnt: allData.revealCnt,
          pv: allData.pv,
          uv: allData.uv,
          bounceRate: allData.bounceRate,
          payByrCnt: allData.payByrCnt,
          payAmt: allData.payAmt,
          clickRate: revealCnt > 0 ? (pv / revealCnt).toFixed(4) : null,
          avgPvs: uv > 0 ? (pv / uv | 0) : null,
          mobileUv: mobileData?.uv ?? null,
          mobilePv: mobileData?.pv ?? null,
          mobileShare: uv > 0 && mobileData?.uv !== null ? (mobileData.uv / uv).toFixed(4) : null,
          allRaw: allData.raw,
          mobileRaw: mobileData?.raw ?? null
        };
        log('流量统计提取成功:', 'revealCnt', revealCnt, 'pv', pv, 'uv', uv, 'mobileUv', mobileUv);
      }
    } catch (e) {
      log('流量统计 API 获取失败:', e);
    }

    // 5. 从 inquiry/coreIndex 获取昨日询盘概况
    try {
      const pad = (n) => String(n).padStart(2, '0');
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayStr = `${yesterday.getFullYear()}-${pad(yesterday.getMonth() + 1)}-${pad(yesterday.getDate())}`;
      const indexCode = 'effectiveInQUsers,wangInQUsers,bEffectiveInQUsers,bWangInQUsers,effectInQCnt,wangInQCnt,factoryInQUsers,factoryWangInQUsers,factorySheetInQUsers,factoryPhoneInQUsers,factoryPerfectInQUsers,factoryWangPerfectInQUsers,factorySheetPerfectInQUsers,factoryPhonePerfectInQUsers';
      const inquiryUrl = `https://sycm.1688.com/ms/customer/inquiry/coreIndex.json?dateType=day&dateRange=${yesterdayStr}|${yesterdayStr}&indexCode=${indexCode}&_=${timestamp}`;

      const inquiryResp = await fetch(inquiryUrl, {
        credentials: 'include',
        headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }
      });
      const inquiryJson = await inquiryResp.json();

      if (inquiryJson.code === 0 && inquiryJson.data) {
        const d = inquiryJson.data;
        result.inquiry = {
          statDate: d.statDate?.value ? new Date(d.statDate.value).toISOString().slice(0, 10) : yesterdayStr,
          effectiveInQUsers: d.effectiveInQUsers?.value ?? null,
          wangInQUsers: d.wangInQUsers?.value ?? null,
          bEffectiveInQUsers: d.bEffectiveInQUsers?.value ?? null,
          bWangInQUsers: d.bWangInQUsers?.value ?? null,
          effectInQCnt: d.effectInQCnt?.value ?? null,
          wangInQCnt: d.wangInQCnt?.value ?? null,
          factoryInQUsers: d.factoryInQUsers?.value ?? null,
          factoryWangInQUsers: d.factoryWangInQUsers?.value ?? null,
          factorySheetInQUsers: d.factorySheetInQUsers?.value ?? null,
          factoryPhoneInQUsers: d.factoryPhoneInQUsers?.value ?? null,
          factoryPerfectInQUsers: d.factoryPerfectInQUsers?.value ?? null,
          factoryWangPerfectInQUsers: d.factoryWangPerfectInQUsers?.value ?? null,
          factorySheetPerfectInQUsers: d.factorySheetPerfectInQUsers?.value ?? null,
          factoryPhonePerfectInQUsers: d.factoryPhonePerfectInQUsers?.value ?? null,
          repeatRate: d.repeatRate ?? null,
          cateScoreFh: d.cateScoreFh ?? null,
          cateScoreHm: d.cateScoreHm ?? null,
          cateScoreXy: d.cateScoreXy ?? null,
          scorefh: d.scorefh ?? null,
          scorehm: d.scorehm ?? null,
          scorexy: d.scorexy ?? null,
          raw: d
        };
        log('询盘概况提取成功:', 'effectiveInQUsers', result.inquiry.effectiveInQUsers);
      }
    } catch (e) {
      log('询盘概况 API 获取失败:', e);
    }

    // 6. 从 transaction/getTradeCoreIndex 获取昨日交易概况
    try {
      const pad = (n) => String(n).padStart(2, '0');
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayStr = `${yesterday.getFullYear()}-${pad(yesterday.getMonth() + 1)}-${pad(yesterday.getDate())}`;
      const tradeUrl = `https://sycm.1688.com/ms/transaction/getTradeCoreIndex.json?dateType=day&dateRange=${yesterdayStr}|${yesterdayStr}&device=0&_=${timestamp}`;

      const tradeResp = await fetch(tradeUrl, {
        credentials: 'include',
        headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }
      });
      const tradeJson = await tradeResp.json();

      if (tradeJson.code === 0 && tradeJson.data) {
        const d = tradeJson.data;
        const payAmt = d.payAmt?.value ?? 0;
        const oldPayByrAmt = d.oldPayByrAmt?.value ?? 0;
        const payByrCnt = d.payByrCnt?.value ?? 0;
        const payOldByrCnt = d.payOldByrCnt?.value ?? 0;
        const payNewByrCnt = d.payNewByrCnt?.value ?? 0;

        result.trade = {
          statDate: d.statDate?.value ? new Date(d.statDate.value).toISOString().slice(0, 10) : yesterdayStr,
          payAmt: payAmt,
          payByrCnt: payByrCnt,
          payNewByrCnt: payNewByrCnt,
          payOldByrCnt: payOldByrCnt,
          payItemQty: d.payItemQty?.value ?? null,
          payMordCnt: d.payMordCnt?.value ?? null,
          payRate: d.payRate?.value ?? null,
          payToOnRate: d.payToOnRate?.value ?? null,
          perByrAmt: d.perByrAmt?.value ?? null,
          rfdSucAmt: d.rfdSucAmt?.value ?? null,
          crtOrdItmQty: d.crtOrdItmQty?.value ?? null,
          crtByrCnt: d.crtByrCnt?.value ?? null,
          crtOrdAmt: d.crtOrdAmt?.value ?? null,
          // 衍生指标
          newBuyerAmt: oldPayByrAmt > 0 ? payAmt - oldPayByrAmt : payAmt,
          newBuyerShare: payAmt > 0 && oldPayByrAmt > 0 ? ((payAmt - oldPayByrAmt) / payAmt).toFixed(4) : null,
          oldBuyerShare: payByrCnt > 0 && payOldByrCnt > 0 ? (payOldByrCnt / payByrCnt).toFixed(4) : null,
          oldBuyerPerAmt: payOldByrCnt > 0 && oldPayByrAmt > 0 ? (oldPayByrAmt / payOldByrCnt).toFixed(2) : null,
          refundRate: payAmt > 0 && d.rfdSucAmt?.value ? (d.rfdSucAmt.value / payAmt).toFixed(4) : null,
          raw: d
        };
        log('交易概况提取成功:', 'payAmt', payAmt, 'payByrCnt', payByrCnt, 'newBuyer', payNewByrCnt);
      }
    } catch (e) {
      log('交易概况 API 获取失败:', e);
    }

    // 7. 近7天交易概况
    try {
      const pad = (n) => String(n).padStart(2, '0');
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const start = new Date(yesterday);
      start.setDate(start.getDate() - 6);
      const startStr = `${start.getFullYear()}-${pad(start.getMonth() + 1)}-${pad(start.getDate())}`;
      const endStr = `${yesterday.getFullYear()}-${pad(yesterday.getMonth() + 1)}-${pad(yesterday.getDate())}`;
      const trade7Url = `https://sycm.1688.com/ms/transaction/getTradeCoreIndex.json?dateType=recent7&dateRange=${startStr}|${endStr}&device=0&_=${timestamp}`;

      const trade7Resp = await fetch(trade7Url, {
        credentials: 'include',
        headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }
      });
      const trade7Json = await trade7Resp.json();

      if (trade7Json.code === 0 && trade7Json.data) {
        const d = trade7Json.data;
        const payAmt = d.payAmt?.value ?? 0;
        result.tradeRecent7 = {
          dateRange: `${startStr}|${endStr}`,
          payAmt: payAmt,
          payByrCnt: d.payByrCnt?.value ?? null,
          payNewByrCnt: d.payNewByrCnt?.value ?? null,
          payOldByrCnt: d.payOldByrCnt?.value ?? null,
          payItemQty: d.payItemQty?.value ?? null,
          payMordCnt: d.payMordCnt?.value ?? null,
          payRate: d.payRate?.value ?? null,
          perByrAmt: d.perByrAmt?.value ?? null,
          rfdSucAmt: d.rfdSucAmt?.value ?? null,
          refundRate: payAmt > 0 && d.rfdSucAmt?.value ? (d.rfdSucAmt.value / payAmt).toFixed(4) : null,
          raw: d
        };
        log('近7天交易概况提取成功:', 'payAmt', payAmt);
      }
    } catch (e) {
      log('近7天交易概况 API 获取失败:', e);
    }

    // 8. 近7天流量来源（含支付转化数据）
    try {
      const pad = (n) => String(n).padStart(2, '0');
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const start = new Date(yesterday);
      start.setDate(start.getDate() - 6);
      const startStr = `${start.getFullYear()}-${pad(start.getMonth() + 1)}-${pad(start.getDate())}`;
      const endStr = `${yesterday.getFullYear()}-${pad(yesterday.getMonth() + 1)}-${pad(yesterday.getDate())}`;
      const flowSourceUrl = `https://sycm.1688.com/ms/flow/strategy/shopInFlowTreeWithGoodV2.json?dateRange=${startStr}|${endStr}&dateType=recent7&order=desc&orderBy=fleadPayByrCnt&device=2&_=${timestamp}`;

      const fsResp = await fetch(flowSourceUrl, {
        credentials: 'include',
        headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }
      });
      const fsJson = await fsResp.json();

      if (fsJson.code === 0 && fsJson.data) {
        // 扁平化提取树形结构中的所有节点（一级+二级）
        const allSources = [];
        const extractNode = (node) => {
          if (!node) return;
          allSources.push({
            name: node.outerName?.value ?? '',
            outerId: node.outerId?.value ?? '',
            parentOuterId: node.parentOuterId?.value ?? '',
            outerLevel: node.outerLevel?.value ?? 1,
            uv: node.uv?.value ?? null,
            bUv: node.bUv?.value ?? null,
            newUv: node.newUv?.value ?? null,
            oldUv: node.oldUv?.value ?? null,
            adUv: node.adUv?.value ?? null,
            fleadPayByrCnt: node.fleadPayByrCnt?.value ?? null,
            fleadPayAmt: node.fleadPayAmt?.value ?? null,
            fleadCrtByrCnt: node.fleadCrtByrCnt?.value ?? null,
            fleadCrtOrdAmt: node.fleadCrtOrdAmt?.value ?? null,
            goodUv: node.goodUv?.value ?? null,
            goodBUv: node.goodBUv?.value ?? null,
            goodBPayAmt: node.goodBPayAmt?.value ?? null,
            goodBCrtAmt: node.goodBCrtAmt?.value ?? null,
            leadPayAmtDisPercent: node.leadPayAmtDisPercent?.value ?? null,
            leadPayAmtDiscount: node.leadPayAmtDiscount?.value ?? null
          });
          if (node.children && Array.isArray(node.children)) {
            node.children.forEach(extractNode);
          }
        };
        fsJson.data.forEach(extractNode);

        const totalMyUv = allSources.reduce((sum, s) => sum + (s.uv || 0), 0);
        const totalFleadPayAmt = allSources.reduce((sum, s) => sum + (s.fleadPayAmt || 0), 0);

        result.flowSourceRecent7 = {
          dateRange: `${startStr}|${endStr}`,
          sources: allSources,
          totalMyUv,
          totalFleadPayAmt
        };
        log('近7天流量来源提取成功:', allSources.length, '条', '总UV', totalMyUv, '总引导支付', totalFleadPayAmt.toFixed(2));
      }
    } catch (e) {
      log('近7天流量来源 API 获取失败:', e);
    }

    // 9. 近7天入店关键词
    try {
      const pad = (n) => String(n).padStart(2, '0');
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const start = new Date(yesterday);
      start.setDate(start.getDate() - 6);
      const startStr = `${start.getFullYear()}-${pad(start.getMonth() + 1)}-${pad(start.getDate())}`;
      const endStr = `${yesterday.getFullYear()}-${pad(yesterday.getMonth() + 1)}-${pad(yesterday.getDate())}`;
      const keywordUrl = `https://sycm.1688.com/ms/flow/getShopKeyWordWithWeb.json?dateRange=${startStr}|${endStr}&dateType=recent7&pageSize=10&page=1&order=desc&orderBy=keywordRevealCnt&device=0&_=${timestamp}`;

      const kwResp = await fetch(keywordUrl, {
        credentials: 'include',
        headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }
      });
      const kwJson = await kwResp.json();

      if (kwJson.code === 0 && kwJson.data && kwJson.data.data) {
        const keywords = kwJson.data.data.map(item => ({
          keyword: item.exposeKeyword?.value ?? '',
          keywordRevealCnt: item.keywordRevealCnt?.value ?? null,
          uv: item.uv?.value ?? null,
          pv: item.pv?.value ?? null,
          leadPayAmt: item.leadPayAmt?.value ?? null,
          leadPayByrCnt: item.leadPayByrCnt?.value ?? null,
          leadCrtByrCnt: item.leadCrtByrCnt?.value ?? null,
          clickRate: item.clickRate?.value ?? null,
          webClickRate: item.webClickRate?.value ?? null,
          webPayRate: item.webPayRate?.value ?? null,
          revealItem: item.revealItem?.value ?? null,
          bestOrder: item.bestOrder?.value ?? null,
          avgOrder: item.avgOrder?.value ?? null,
          webSearchIndex: item.webSearchIndex?.value ?? null,
          webSupplyAndDemandIndex: item.webSupplyAndDemandIndex?.value ?? null,
          referencePrice: item.referencePrice?.value ?? null
        }));
        const totalKeywordReveal = keywords.reduce((sum, k) => sum + (k.keywordRevealCnt || 0), 0);
        const totalLeadPayAmt = keywords.reduce((sum, k) => sum + (k.leadPayAmt || 0), 0);

        result.keywordsRecent7 = {
          dateRange: `${startStr}|${endStr}`,
          keywords,
          totalKeywordReveal,
          totalLeadPayAmt,
          recordCount: kwJson.data.recordCount || 0
        };
        log('近7天入店关键词提取成功:', keywords.length, '条', '总展现', totalKeywordReveal, '总引导支付', totalLeadPayAmt);
      } else {
        log('近7天入店关键词 API 返回异常:', 'code=', kwJson.code, 'hasData=', !!kwJson.data, 'hasDataData=', !!(kwJson.data && kwJson.data.data));
      }
    } catch (e) {
      log('近7天入店关键词 API 获取失败:', e);
    }

    // 10. 从页面中提取更多数据（备用）
    try {
      // 尝试从页面元素获取公司名
      if (!result.companyName) {
        const nameSelectors = [
          '.company-name',
          '[data-spm="company-name"]',
          '.shop-name',
          '.sycm-company-name'
        ];
        for (const sel of nameSelectors) {
          const el = $(sel);
          if (el) {
            result.companyName = text(el);
            break;
          }
        }
      }

      // 提取页面标题中的数据指标
      result.pageData.title = document.title;
      result.pageData.urlPath = location.pathname;
    } catch (e) {
      log('页面备用提取失败:', e);
    }

    log('生意参谋采集完成:', result.companyName || '(未获取到公司名)');
    return result;
  }

  // --- 数据发送 ---
  function sendData(data) {
    try {
      // 通过Chrome Runtime发送给background.js
      if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.sendMessage) {
        chrome.runtime.sendMessage({
          action: 'CLAW_DATA',
          source: '1688-content-script',
          data: data
        }, (response) => {
          if (chrome.runtime.lastError) {
            log('发送消息失败:', chrome.runtime.lastError.message);
          } else {
            log('数据已发送, 响应:', response);
          }
        });
      }
    } catch (e) {
      log('发送数据异常:', e);
    }
  }

  // --- 主入口 ---
  async function main() {
    const pageType = detectPageType();
    log('页面类型:', pageType, 'URL:', location.href);

  // 全局去重检查：同一页面类型 5 分钟内不重复采集（避免 SPA 路由切换导致重复请求）
  const DEDUP_INTERVAL = 5 * 60 * 1000; // 5分钟
  const dedupKey = `__claw_1688_dedup_${pageType}`;
  const lastCrawl = sessionStorage.getItem(dedupKey);
  if (lastCrawl) {
    const elapsed = Date.now() - parseInt(lastCrawl);
    if (elapsed < DEDUP_INTERVAL) {
      log(`[${pageType}] 该页面类型已在近期采集(${(elapsed / 1000).toFixed(0)}秒前)，跳过`);
      return;
    }
  }
  sessionStorage.setItem(dedupKey, Date.now().toString());

    let data = null;
    if (pageType === 'work') {
      data = await extractWorkPage();
    } else if (pageType === 'sycm') {
      data = await extractSycmPage();
    } else {
      log('未知页面类型，跳过采集');
      return;
    }

    if (data) {
      if (pageType === 'work') {
        log('采集完成，工作台:', data.wwResponse ?? '未获取');
      } else if (pageType === 'sycm') {
        log('采集完成，生意参谋:', data.companyName || '未获取');
      }
      sendData(data);

      // 同时挂载到window，方便外部调试
      window.__CLAW_1688_DATA__ = data;
    }
  }

  // 页面加载完成后执行
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(main, 1000);
  } else {
    window.addEventListener('DOMContentLoaded', () => setTimeout(main, 1000));
  }

  // 监听URL变化（SPA路由）
  let lastUrl = location.href;
  setInterval(() => {
    if (location.href !== lastUrl) {
      lastUrl = location.href;
      log('URL变化，重新采集');
      setTimeout(main, 1500);
    }
  }, 2000);

  // 监听来自popup/background的消息
  if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.onMessage) {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'GET_CLAW_DATA') {
        const data = window.__CLAW_1688_DATA__ || null;
        sendResponse({
          success: !!data,
          data: data,
          pageType: detectPageType()
        });
      }
      if (request.action === 'TRIGGER_CLAW') {
        main();
        sendResponse({ success: true });
      }
      return true;
    });
  }

})();
