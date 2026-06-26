const BASE_HEADERS = {
  "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  Referer: "https://fund.eastmoney.com/",
};

async function fetchJSON(url) {
  const resp = await fetch(url, { headers: BASE_HEADERS });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
  return resp.json();
}

async function fetchText(url) {
  const resp = await fetch(url, { headers: BASE_HEADERS });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
  return resp.text();
}

function ts() {
  return Date.now();
}

// ======================== 基金相关 ========================

export async function searchFund(keyword) {
  const url = `https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?m=9&key=${encodeURIComponent(keyword)}&_=${ts()}`;
  const data = await fetchJSON(url);
  if (!data.Datas) return [];
  return data.Datas.map((item) => ({
    code: item.CODE,
    name: item.NAME,
    type: item.FundBaseInfo?.FTYPE || "",
    pinyin: item.JPCODE || "",
  }));
}

export async function getFundEstimate(fundCode) {
  const url = `https://fundgz.1234567.com.cn/js/${fundCode}.js`;
  const text = await fetchText(url);
  const match = text.match(/\{(.+?)\}/);
  if (!match) throw new Error(`无法解析基金 ${fundCode} 的估值数据`);
  const d = JSON.parse(match[0]);
  return {
    fundCode: d.fundcode,
    name: d.name,
    netValue: d.dwjz,
    estimateValue: d.gsz,
    estimateGrowthRate: d.gszzl,
    estimateTime: d.gztime,
    netValueDate: d.jzrq,
  };
}

export async function getFundBatchInfo(fundCodes) {
  const codes = Array.isArray(fundCodes) ? fundCodes.join(",") : fundCodes;
  const url = `https://fundmobapi.eastmoney.com/FundMNewApi/FundMNFInfo?pageIndex=1&pageSize=200&plat=Android&appType=ttjj&product=EFund&Version=1&deviceid=Wap&Fcodes=${codes}`;
  const data = await fetchJSON(url);
  if (!data.Datas) return [];
  return data.Datas.map((d) => ({
    fundCode: d.FCODE,
    name: d.SHORTNAME,
    date: d.PDATE,
    netValue: d.NAV,
    changeRate: d.NAVCHGRT,
    type: d.FTYPE,
  }));
}

export async function getFundInfo(fundCode) {
  const url = `https://fundmobapi.eastmoney.com/FundMApi/FundBaseTypeInformation.ashx?FCODE=${fundCode}&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&Uid=&_=${ts()}`;
  const data = await fetchJSON(url);
  const d = data.Datas;
  if (!d || !d.FCODE) return null;
  return {
    fundCode: d.FCODE,
    name: d.SHORTNAME,
    type: d.FTYPE,
    company: d.JJGS,
    manager: d.JJJL,
    netValue: d.DWJZ,
    totalNetValue: d.LJJZ,
    netValueDate: d.FSRQ,
    scale: d.ENDNAV,
    buyStatus: d.SGZT,
    sellStatus: d.SHZT,
    yield1Month: d.SYL_Y,
    yield3Month: d.SYL_3Y,
    yield6Month: d.SYL_6Y,
    yield1Year: d.SYL_1N,
    rank1Month: d.RANKM,
    rank3Month: d.RANKQ,
    rank6Month: d.RANKHY,
    rank1Year: d.RANKY,
    bonus: d.FUNDBONUS
      ? {
          date: d.FUNDBONUS.PDATE,
          ratio: d.FUNDBONUS.CHGRATIO,
        }
      : null,
  };
}

export async function getFundValuationDetail(fundCode) {
  const url = `https://fundmobapi.eastmoney.com/FundMApi/FundVarietieValuationDetail.ashx?FCODE=${fundCode}&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&_=${ts()}`;
  const data = await fetchJSON(url);
  const expansion = data.Expansion || {};
  const items = (data.Datas || []).map((raw) => {
    const parts = raw.split(",");
    return { time: parts[0], netValue: parts[1], growthRate: parts[2] };
  });
  return {
    netValue: expansion.DWJZ,
    items,
  };
}

export async function getFundNetValueHistory(fundCode, range = "y") {
  const url = `https://fundmobapi.eastmoney.com/FundMApi/FundNetDiagram.ashx?FCODE=${fundCode}&RANGE=${range}&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&_=${ts()}`;
  const data = await fetchJSON(url);
  if (!data.Datas) return [];
  return data.Datas.map((d) => ({
    date: d.FSRQ,
    netValue: d.DWJZ,
    totalNetValue: d.LJJZ,
    changeRate: d.JZZZL,
  }));
}

export async function getFundAccumulatedPerformance(fundCode, range = "y") {
  const url = `https://dataapi.1234567.com.cn/dataapi/fund/FundVPageAcc?INDEXCODE=000300&CODE=${fundCode}&FCODE=${fundCode}&RANGE=${range}&deviceid=Wap&product=EFund`;
  const data = await fetchJSON(url);
  if (!data.data) return [];
  return data.data.map((d) => ({
    date: d.pdate,
    yield: d.yield,
    indexYield: d.indexYield,
    categoryYield: d.fundTypeYield,
  }));
}

export async function getFundPosition(fundCode) {
  const url = `https://fundmobapi.eastmoney.com/FundMNewApi/FundMNInverstPosition?FCODE=${fundCode}&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&Uid=&_=${ts()}`;
  const data = await fetchJSON(url);
  const stocks = data.Datas?.fundStocks;
  if (!stocks) return { date: null, stocks: [] };
  return {
    date: data.Expansion,
    stocks: stocks.map((s) => ({
      code: s.GPDM,
      name: s.GPJC,
      exchange: s.NEWTEXCH,
      holdRatio: s.JZBL,
      changeType: s.PCTNVCHGTYPE,
      changeRatio: s.PCTNVCHG,
    })),
  };
}

export async function getFundManagerList(fundCode) {
  const url = `https://fundmobapi.eastmoney.com/FundMApi/FundManagerList.ashx?FCODE=${fundCode}&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&Uid=&_=${ts()}`;
  const data = await fetchJSON(url);
  if (!data.Datas) return [];
  return data.Datas.map((d) => ({
    id: d.MGRID,
    name: d.MGRNAME,
    startDate: d.FEMPDATE,
    endDate: d.LEMPDATE || "至今",
    days: d.DAYS,
    growthRate: d.PENAVGROWTH,
  }));
}

export async function getFundManagerDetail(fundCode) {
  const url = `https://fundmobapi.eastmoney.com/FundMApi/FundMangerDetail.ashx?FCODE=${fundCode}&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&Uid=&_=${ts()}`;
  const data = await fetchJSON(url);
  if (!data.Datas) return [];
  return data.Datas.map((d) => ({
    id: d.MGRID,
    name: d.MGRNAME,
    startDate: d.FEMPDATE,
    days: d.DAYS,
    photo: d.PHOTOURL,
    resume: d.RESUME,
  }));
}

// ======================== 股票/指数相关 ========================

export async function getStockTrend(secid) {
  const url = `https://push2.eastmoney.com/api/qt/stock/trends2/get?secid=${secid}&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f53,f56,f58&iscr=0&iscca=0&ndays=1&forcect=1`;
  const data = await fetchJSON(url);
  if (!data.data) return null;
  const trends = (data.data.trends || []).map((t) => {
    const parts = t.split(",");
    return { time: parts[0], price: parts[1], volume: parts[2], avgPrice: parts[3] };
  });
  return {
    prePrice: data.data.prePrice,
    code: data.data.code,
    name: data.data.name,
    trends,
  };
}

export async function getStockQuote(secids) {
  const ids = Array.isArray(secids) ? secids.join(",") : secids;
  const url = `https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f1,f2,f3,f4,f6,f12,f13,f14&secids=${ids}&_=${ts()}`;
  const data = await fetchJSON(url);
  if (!data.data?.diff) return [];
  return data.data.diff.map((d) => ({
    code: d.f12,
    market: d.f13,
    name: d.f14,
    price: d.f2,
    changeRate: d.f3,
    changeAmount: d.f4,
    volume: d.f6,
  }));
}

// ======================== 大盘/资金流向 ========================

export async function getMarketOverview() {
  const url = `https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=1.000001,0.399001&fields=f1,f2,f3,f4,f6,f12,f13,f104,f105,f106&_=${ts()}`;
  const data = await fetchJSON(url);
  if (!data.data?.diff) return [];
  return data.data.diff.map((d) => ({
    code: d.f12,
    market: d.f13,
    name: d.f14 || (d.f12 === "000001" ? "上证指数" : "深证成指"),
    price: d.f2,
    changeRate: d.f3,
    changeAmount: d.f4,
    turnover: d.f6,
    upCount: d.f104,
    downCount: d.f105,
    flatCount: d.f106,
  }));
}

export async function getMarketCapitalFlow() {
  const url = `https://push2.eastmoney.com/api/qt/stock/fflow/kline/get?lmt=0&klt=1&secid=1.000001&secid2=0.399001&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&_=${ts()}`;
  const data = await fetchJSON(url);
  if (!data.data?.klines) return [];
  return data.data.klines.map((line) => {
    const p = line.split(",");
    return {
      time: p[0],
      mainNet: (p[1] / 1e8).toFixed(4),
      smallNet: (p[2] / 1e8).toFixed(4),
      mediumNet: (p[3] / 1e8).toFixed(4),
      largeNet: (p[4] / 1e8).toFixed(4),
      superLargeNet: (p[5] / 1e8).toFixed(4),
    };
  });
}

export async function getSectorCapitalFlow(timeType = "f62", code = "m:90+s:4") {
  const url = `https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=${timeType}&code=${encodeURIComponent(code)}`;
  const data = await fetchJSON(url);
  if (!data.data?.diff) return [];
  return data.data.diff.map((d) => ({
    name: d.f14,
    capitalFlow: d[timeType],
  }));
}

export async function getNorthboundCapital() {
  const url = `https://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55,f56&ut=&?v=${ts()}`;
  const data = await fetchJSON(url);
  if (!data.data) return null;

  function parseFlow(arr) {
    if (!arr) return [];
    return arr.map((item) => {
      const p = item.split(",");
      return {
        time: p[0],
        netBuy: p[1] === "-" ? null : (p[1] / 1e4).toFixed(4),
        balance: p[2] === "-" ? null : (p[2] / 1e4).toFixed(4),
        netBuy2: p[3] === "-" ? null : (p[3] / 1e4).toFixed(4),
        balance2: p[4] === "-" ? null : (p[4] / 1e4).toFixed(4),
        total: p[5] === "-" ? null : (p[5] / 1e4).toFixed(4),
      };
    });
  }

  return {
    s2n: parseFlow(data.data.s2n),
    n2s: parseFlow(data.data.n2s),
  };
}
