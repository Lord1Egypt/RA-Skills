/**
 * Price Trend Embeddable Component
 *
 * 用于在 AI 对话中嵌入价格趋势图表的独立组件
 * 支持 React 环境直接引用
 *
 * @usage
 * import { PriceTrendEmbed, convertPriceInsights } from './PriceTrendEmbed';
 *
 * const chartProps = convertPriceInsights(priceInsights, searchParams);
 * <PriceTrendEmbed {...chartProps} />
 */

import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';

// ===== 样式定义 (CSS-in-JS for portability) =====
const styles = {
  chart: {
    marginTop: '12px',
    background: 'var(--white, #FFFFFF)',
    border: '1px solid var(--border, #EEEEEE)',
    borderRadius: '12px',
    padding: '16px',
  },
  titleRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '4px',
  },
  title: {
    fontSize: '16px',
    fontWeight: '600',
    color: 'var(--text-1, #1A1A1A)',
  },
  curWrap: {
    textAlign: 'right',
  },
  curPrice: {
    fontFamily: "var(--font-num, 'DM Sans', sans-serif)",
    fontSize: '28px',
    fontWeight: '500',
    lineHeight: '1',
    letterSpacing: '-0.5px',
  },
  curCurrency: {
    fontSize: '16px',
    fontWeight: '400',
    marginRight: '2px',
    opacity: '0.7',
  },
  curChange: {
    fontSize: '13px',
    fontWeight: '500',
    marginTop: '3px',
  },
  badges: {
    display: 'flex',
    gap: '8px',
    margin: '10px 0 16px',
    flexWrap: 'wrap',
  },
  badge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '4px',
    padding: '4px 10px',
    borderRadius: '999px',
    fontSize: '13px',
    fontWeight: '500',
  },
  badgeLow: { background: '#F0FAF6', color: '#16A571' },
  badgeMid: { background: '#F7F7F8', color: '#666666' },
  badgeHigh: { background: '#FFF5F5', color: '#E54D4D' },
  badgeNeutral: { background: '#F5F5F5', color: '#999999' },
  canvas: {
    position: 'relative',
    width: '100%',
    height: '160px',
    marginBottom: '8px',
    touchAction: 'none',
    cursor: 'crosshair',
  },
  tooltip: {
    position: 'absolute',
    top: '-6px',
    transform: 'translateX(-50%)',
    background: '#1A1A1A',
    color: '#FFFFFF',
    padding: '6px 12px',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '600',
    fontFamily: "var(--font-num, 'DM Sans', sans-serif)",
    whiteSpace: 'nowrap',
    pointerEvents: 'none',
    zIndex: 10,
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
  },
  tooltipArrow: {
    content: "''",
    position: 'absolute',
    bottom: '-5px',
    left: '50%',
    transform: 'translateX(-50%)',
    borderLeft: '6px solid transparent',
    borderRight: '6px solid transparent',
    borderTop: '6px solid #1A1A1A',
  },
  crosshair: {
    position: 'absolute',
    top: 0,
    width: '1px',
    height: '100%',
    background: '#CCCCCC',
    pointerEvents: 'none',
    zIndex: 5,
  },
  dot: {
    position: 'absolute',
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    background: '#6666FF',
    border: '2.5px solid #FFFFFF',
    boxShadow: '0 1px 4px rgba(0,0,0,0.15)',
    transform: 'translate(-50%, -50%)',
    pointerEvents: 'none',
    zIndex: 6,
  },
  yLabels: {
    position: 'absolute',
    top: 0,
    left: 0,
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    padding: '8px 0',
    pointerEvents: 'none',
  },
  yLabel: {
    fontFamily: "var(--font-num, 'DM Sans', sans-serif)",
    fontSize: '10px',
    color: '#CCCCCC',
    lineHeight: '1',
  },
  footer: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '13px',
    color: '#999999',
    paddingTop: '4px',
  },
  stats: {
    display: 'flex',
    gap: 0,
    marginTop: '14px',
    borderTop: '0.5px solid #EEEEEE',
  },
  stat: {
    flex: 1,
    textAlign: 'center',
    padding: '12px 0 4px',
  },
  statLabel: {
    fontSize: '12px',
    color: '#999999',
    marginBottom: '4px',
  },
  statVal: {
    fontFamily: "var(--font-num, 'DM Sans', sans-serif)",
    fontSize: '18px',
    fontWeight: '700',
    color: '#1A1A1A',
  },
  hint: {
    textAlign: 'center',
    fontSize: '13px',
    color: '#999999',
    marginTop: '10px',
  },
  avgLabel: {
    position: 'absolute',
    right: '4px',
    transform: 'translateY(-50%)',
    background: '#F0EFFF',
    color: '#6666FF',
    fontSize: '11px',
    fontWeight: '600',
    fontFamily: "var(--font-num, 'DM Sans', sans-serif)",
    padding: '2px 6px',
    borderRadius: '4px',
    pointerEvents: 'none',
    zIndex: 4,
    whiteSpace: 'nowrap',
  },
};

// ===== 工具函数 =====

/**
 * 格式化日期为"月/日"
 */
function fmtDateShort(dateStr) {
  const d = new Date(dateStr);
  return `${d.getMonth() + 1}/${d.getDate()}`;
}

/**
 * 格式化日期为"X 月 X 日"
 */
function fmtDate(dateStr) {
  const d = new Date(dateStr);
  return `${d.getMonth() + 1}月${d.getDate()}日`;
}

/**
 * 将后端 priceInsights 转换为组件需要的格式
 *
 * @param {Object} priceInsights - 后端返回的价格洞察数据
 * @param {Array} priceInsights.priceHistory - [[timestamp, price], ...]
 * @param {number} priceInsights.lowestPrice - 最低价格
 * @param {string} priceInsights.priceLevel - "low" | "typical" | "high"
 * @param {Object} searchParams - 搜索参数
 * @param {string} searchParams.destination - 目的地代码
 * @returns {Object|null} 转换后的数据，如果输入无效则返回 null
 */
export function convertPriceInsights(priceInsights, searchParams) {
  if (!priceInsights || !Array.isArray(priceInsights.priceHistory) || priceInsights.priceHistory.length === 0) {
    return null;
  }

  const data = priceInsights.priceHistory.map(([timestamp, price]) => ({
    date: new Date(timestamp * 1000).toISOString().split('T')[0],
    price,
  }));

  const prices = data.map(d => d.price);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const average = Math.round(prices.reduce((a, b) => a + b, 0) / prices.length);
  const currentPrice = priceInsights.lowestPrice || prices[prices.length - 1];
  const pctDiff = Math.round(((currentPrice - average) / average) * 100);

  const levelMap = { low: 'low', typical: 'mid', high: 'high' };
  const level = levelMap[priceInsights.priceLevel] || 'mid';

  let trend = 'stable';
  if (data.length >= 14) {
    const recent = data.slice(-7).map(d => d.price);
    const earlier = data.slice(-14, -7).map(d => d.price);
    const recentAvg = recent.reduce((a, b) => a + b, 0) / recent.length;
    const earlierAvg = earlier.reduce((a, b) => a + b, 0) / earlier.length;
    if (recentAvg < earlierAvg * 0.95) trend = 'falling';
    else if (recentAvg > earlierAvg * 1.05) trend = 'rising';
  }

  return {
    data,
    currentPrice,
    analysis: { min, max, average, pctDiff, level, trend },
    destination: { code: searchParams?.destination || 'DST' },
  };
}

// ===== PriceChart 组件 =====

const levelText = { low: '低于均价', mid: '价格适中', high: '高于均价' };
const trendText = { falling: '📉 近期下降', rising: '📈 近期上涨', stable: '➡️ 走势平稳' };

/**
 * 价格趋势图表组件
 */
export function PriceChart({ data, currentPrice, analysis, destination }) {
  const canvasRef = useRef(null);
  const [hover, setHover] = useState(null);
  const [dims, setDims] = useState({ w: 300, h: 160 });

  useEffect(() => {
    const el = canvasRef.current;
    if (!el) return;
    const ro = new ResizeObserver(entries => {
      const { width } = entries[0].contentRect;
      if (width > 0) setDims({ w: width, h: 160 });
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const padL = 0, padR = 0, padT = 12, padB = 12;

  const points = useMemo(() => {
    if (!Array.isArray(data) || data.length === 0) return [];
    const prices = data.map(d => d.price);
    const minP = Math.min(...prices), maxP = Math.max(...prices);
    const range = maxP - minP || 1;
    const cW = dims.w - padL - padR, cH = dims.h - padT - padB;
    return data.map((d, i) => ({
      x: padL + (i / (data.length - 1)) * cW,
      y: padT + cH - ((d.price - minP) / range) * cH,
      price: d.price,
      date: d.date,
      index: i,
    }));
  }, [data, dims]);

  const linePath = useMemo(() => {
    if (!points.length) return '';
    let d = `M ${points[0].x} ${points[0].y}`;
    for (let i = 1; i < points.length; i++) {
      const p0 = points[i - 1], p1 = points[i];
      const cpx = (p0.x + p1.x) / 2;
      d += ` C ${cpx} ${p0.y}, ${cpx} ${p1.y}, ${p1.x} ${p1.y}`;
    }
    return d;
  }, [points]);

  const areaPath = useMemo(() => {
    if (!points.length) return '';
    return linePath + ` L ${points[points.length - 1].x} ${dims.h} L ${points[0].x} ${dims.h} Z`;
  }, [linePath, points, dims]);

  const avgY = useMemo(() => {
    const prices = data.map(d => d.price);
    const minP = Math.min(...prices), maxP = Math.max(...prices);
    const range = maxP - minP || 1;
    const cH = dims.h - padT - padB;
    return padT + cH - ((analysis.average - minP) / range) * cH;
  }, [data, dims, analysis]);

  const interact = useCallback((cx) => {
    const el = canvasRef.current;
    if (!el || !points.length) return;
    const rect = el.getBoundingClientRect();
    const x = cx - rect.left;
    let near = points[0], md = Infinity;
    for (const p of points) {
      const d = Math.abs(p.x - x);
      if (d < md) { md = d; near = p; }
    }
    setHover(near);
  }, [points]);

  const lineColor = 'var(--brand, #6666FF)';
  const gid = 'g-' + (destination?.code || 'DST') + '-' + Math.random().toString(36).slice(2, 6);

  const footerStartLabel = data.length > 0 ? fmtDateShort(data[0].date) : '';
  const footerEndLabel = data.length > 0 ? fmtDateShort(data[data.length - 1].date) : '';

  // 空数据防护
  if (!data || data.length === 0) {
    return (
      <div style={{ ...styles.chart, textAlign: 'center', padding: '40px 16px' }}>
        <p style={{ color: '#999', fontSize: '14px' }}>暂无价格数据</p>
      </div>
    );
  }

  return (
    <div style={styles.chart}>
      {/* Title Row */}
      <div style={styles.titleRow}>
        <div>
          <div style={styles.title}>近 60 天价格走势</div>
        </div>
        <div style={styles.curWrap}>
          <div style={{ ...styles.curPrice, color: lineColor }}>
            <span style={styles.curCurrency}>¥</span>{(hover ? hover.price : currentPrice).toLocaleString()}
          </div>
          {hover ? (
            <div style={{ ...styles.curChange, color: '#999999' }}>{fmtDate(hover.date)}</div>
          ) : (
            <div style={{ ...styles.curChange, color: lineColor }}>
              {analysis.pctDiff > 0 ? '+' : ''}{analysis.pctDiff}% vs 均价
            </div>
          )}
        </div>
      </div>

      {/* Badges */}
      <div style={styles.badges}>
        <span style={{
          ...styles.badge,
          ...(analysis.level === 'low' ? styles.badgeLow :
              analysis.level === 'high' ? styles.badgeHigh : styles.badgeMid)
        }}>
          {analysis.level === 'low' ? '↓' : analysis.level === 'high' ? '↑' : '→'} {levelText[analysis.level]}
        </span>
        <span style={{ ...styles.badge, ...styles.badgeNeutral }}>
          {trendText[analysis.trend]}
        </span>
      </div>

      {/* Chart Canvas */}
      <div
        style={styles.canvas}
        ref={canvasRef}
        onMouseMove={(e) => interact(e.clientX)}
        onMouseLeave={() => setHover(null)}
        onTouchStart={(e) => interact(e.touches[0].clientX)}
        onTouchMove={(e) => { e.preventDefault(); interact(e.touches[0].clientX); }}
        onTouchEnd={() => setHover(null)}
      >
        <svg viewBox={`0 0 ${dims.w} ${dims.h}`} preserveAspectRatio="none">
          <defs>
            <linearGradient id={gid} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#6666FF" stop-opacity="0.12" />
              <stop offset="100%" stop-color="#6666FF" stop-opacity="0.01" />
            </linearGradient>
          </defs>
          <path d={areaPath} fill={`url(#${gid})`} />
          <line
            x1={points[0]?.x || 0}
            y1={avgY}
            x2={points[points.length - 1]?.x || dims.w}
            y2={avgY}
            stroke="#6666FF"
            stroke-width="1"
            stroke-dasharray="4 3"
            opacity="0.5"
          />
          <path d={linePath} fill="none" stroke="#6666FF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
          {points.length > 0 && !hover && (
            <circle
              cx={points[points.length - 1].x}
              cy={points[points.length - 1].y}
              r="4.5"
              fill="#6666FF"
              stroke="white"
              stroke-width="2.5"
            />
          )}
        </svg>

        {/* Average Label */}
        <div style={{ ...styles.avgLabel, top: avgY + 'px' }}>
          均价 ¥{analysis.average.toLocaleString()}
        </div>

        {/* Hover Elements */}
        {hover && (
          <>
            <div style={{ ...styles.crosshair, left: hover.x + 'px' }} />
            <div style={{ ...styles.dot, left: hover.x + 'px', top: hover.y + 'px' }} />
            <div style={{ ...styles.tooltip, left: Math.max(50, Math.min(dims.w - 50, hover.x)) + 'px' }}>
              {fmtDateShort(hover.date)} · ¥{hover.price.toLocaleString()}
            </div>
          </>
        )}
      </div>

      {/* Footer Date Labels */}
      <div style={styles.footer}>
        <span>{footerStartLabel}</span>
        <span>{footerEndLabel}</span>
      </div>

      {/* Stats */}
      <div style={styles.stats}>
        <div style={styles.stat}>
          <div style={styles.statLabel}>最低价</div>
          <div style={styles.statVal}>¥{analysis.min.toLocaleString()}</div>
        </div>
        <div style={{ ...styles.stat, borderLeft: '0.5px solid #EEEEEE' }}>
          <div style={styles.statLabel}>平均价</div>
          <div style={styles.statVal}>¥{analysis.average.toLocaleString()}</div>
        </div>
        <div style={{ ...styles.stat, borderLeft: '0.5px solid #EEEEEE' }}>
          <div style={styles.statLabel}>最高价</div>
          <div style={styles.statVal}>¥{analysis.max.toLocaleString()}</div>
        </div>
      </div>

      {/* Hint */}
      <div style={styles.hint}>👆 滑动查看每日价格</div>
    </div>
  );
}

// ===== 默认导出 =====
export default PriceChart;
