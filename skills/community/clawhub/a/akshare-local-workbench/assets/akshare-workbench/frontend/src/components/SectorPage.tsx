import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { fetchSector, fetchSectorSnapshot } from "../services/api";
import type {
  IndicatorSummary,
  Sector,
  SectorSnapshot,
  SectorSummary
} from "../types";

interface SectorPageProps {
  sectorSummary: SectorSummary;
  indicators: IndicatorSummary[];
  cachedSnapshot: SectorSnapshot | null;
  onSnapshotLoaded: (sectorId: string, snapshot: SectorSnapshot) => void;
  onSelectIndicator: (indicatorId: string) => void;
}

const ALL_TAB = "__all__";

const SOURCE_COLORS: Record<string, string> = {
  eastmoney: "#e74c3c",
  sina: "#e67e22",
  ths: "#f39c12",
  jin10: "#3498db",
  nbs: "#2ecc71",
  pbc: "#1abc9c",
  cfdc: "#9b59b6",
  jsl: "#e91e63",
  cmec: "#00bcd4",
  sse: "#607d8b",
  shfe: "#795548",
  dce: "#ff9800",
  csindex: "#009688",
  swindex: "#673ab7",
  safe: "#4caf50",
  amac: "#8bc34a",
  legulegu: "#ff5722",
  "99futures": "#ffc107",
  akshare: "#2196f3",
};

export function SectorPage({
  sectorSummary,
  indicators,
  cachedSnapshot,
  onSnapshotLoaded,
  onSelectIndicator
}: SectorPageProps) {
  const [sector, setSector] = useState<Sector | null>(null);
  const [snapshot, setSnapshot] = useState<SectorSnapshot | null>(null);
  const [snapshotLoading, setSnapshotLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeLevel2, setActiveLevel2] = useState<string>(ALL_TAB);

  const showSnapshot = sectorSummary.id !== "company_financials";
  const snapshotController = useRef<AbortController | null>(null);

  // Keep the latest cache / callback in refs so the auto-load effect can read
  // them without re-running when the App-level cache updates after a load.
  const cachedSnapshotRef = useRef(cachedSnapshot);
  cachedSnapshotRef.current = cachedSnapshot;
  const onSnapshotLoadedRef = useRef(onSnapshotLoaded);
  onSnapshotLoadedRef.current = onSnapshotLoaded;

  const loadSnapshot = useCallback(
    (refresh: boolean) => {
      snapshotController.current?.abort();
      const controller = new AbortController();
      snapshotController.current = controller;

      setSnapshotLoading(true);
      fetchSectorSnapshot(sectorSummary.id, refresh, controller.signal)
        .then((result) => {
          if (!controller.signal.aborted) {
            setSnapshot(result);
            onSnapshotLoadedRef.current(sectorSummary.id, result);
          }
        })
        .catch((err: Error) => {
          if (err.name !== "AbortError") setError(err.message);
        })
        .finally(() => {
          if (!controller.signal.aborted) setSnapshotLoading(false);
        });
    },
    [sectorSummary.id]
  );

  useEffect(() => {
    const controller = new AbortController();
    setError(null);
    setSector(null);
    setActiveLevel2(ALL_TAB);

    fetchSector(sectorSummary.id, controller.signal)
      .then((detail) => setSector(detail))
      .catch((err: Error) => {
        if (err.name !== "AbortError") setError(err.message);
      });

    if (showSnapshot) {
      const cached = cachedSnapshotRef.current;
      if (cached) {
        setSnapshot(cached);
      } else {
        setSnapshot(null);
      }
    } else {
      setSnapshot(null);
    }
    setSnapshotLoading(false);

    return () => {
      controller.abort();
      snapshotController.current?.abort();
    };
  }, [sectorSummary.id, showSnapshot]);

  const sectorIndicators = useMemo<IndicatorSummary[]>(() => {
    if (!sector) return [];
    return sector.indicator_ids
      .map((indicatorId) => indicators.find((item) => item.id === indicatorId))
      .filter((item): item is IndicatorSummary => Boolean(item));
  }, [sector, indicators]);

  const level2Groups = useMemo(() => {
    const counts = new Map<string, number>();
    sectorIndicators.forEach((indicator) => {
      counts.set(indicator.level2, (counts.get(indicator.level2) ?? 0) + 1);
    });
    return Array.from(counts.entries()).map(([level2, count]) => ({ level2, count }));
  }, [sectorIndicators]);

  const filteredIndicators = useMemo(() => {
    return sectorIndicators.filter((indicator) => {
      if (activeLevel2 !== ALL_TAB && indicator.level2 !== activeLevel2) return false;
      return true;
    });
  }, [sectorIndicators, activeLevel2]);

  const accentStyle = {
    ["--accent" as string]: sectorSummary.accent
  } as Record<string, string>;

  return (
    <section className="sector-page" style={accentStyle}>
      <header className="sector-header">
        <div>
          <h2>{sectorSummary.name}</h2>
          <p className="sector-desc">{sectorSummary.description}</p>
        </div>
        <div className="sector-header-meta">
          <span className="meta-pill">{sectorSummary.indicator_count} 个指标</span>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      {showSnapshot && (
        <section className="snapshot-section">
          <div className="section-header">
            <h3 className="section-title">核心报价</h3>
            <button
              type="button"
              className="refresh-button"
              disabled={snapshotLoading}
              onClick={() => loadSnapshot(true)}
            >
              <span className={`refresh-icon ${snapshotLoading ? "is-spinning" : ""}`}>↻</span>
              刷新
            </button>
          </div>
          <div className="snapshot-grid">
            {snapshotLoading
              ? Array.from({ length: 6 }).map((_, index) => (
                  <div className="snapshot-card snapshot-loading" key={`skeleton-${index}`}>
                    <div className="snapshot-card-head">
                      <span className="snapshot-title">加载中…</span>
                    </div>
                    <div className="snapshot-value">—</div>
                  </div>
                ))
              : (snapshot?.cards ?? []).map((card) => {
                  const isUp = card.change !== null && card.change >= 0;
                  return (
                    <div className="snapshot-card" key={card.title}>
                      <div className="snapshot-card-head">
                        <span className="snapshot-title">{card.title}</span>
                        {card.change_display && (
                          <span
                            className={`snapshot-change ${isUp ? "is-up" : "is-down"}`}
                          >
                            {isUp ? "▲" : "▼"} {card.change_display}
                          </span>
                        )}
                      </div>
                      <div className="snapshot-value">
                        {card.value_display}
                        {card.unit && card.value !== null && (
                          <span className="snapshot-unit">{card.unit}</span>
                        )}
                      </div>
                      {card.error ? (
                        <div className="snapshot-error">{card.error}</div>
                      ) : (
                        card.description && (
                          <div className="snapshot-desc">{card.description}</div>
                        )
                      )}
                    </div>
                  );
                })}
          </div>
          {!snapshotLoading && snapshot === null && (
            <div className="snapshot-placeholder">
              <span className="snapshot-placeholder-icon">📊</span>
              <span>点击右上方「刷新」按钮加载实时核心报价数据。</span>
            </div>
          )}
          {!snapshotLoading && snapshot !== null && (snapshot.cards.length ?? 0) === 0 && (
            <div className="empty-hint">该板块暂未配置核心报价。</div>
          )}
        </section>
      )}

      <section className="indicator-section">
        <div className="section-header">
          <h3 className="section-title">
            可提取指标
            <span className="section-count">
              {filteredIndicators.length}/{sectorIndicators.length}
            </span>
          </h3>
        </div>

        {level2Groups.length > 1 && (
          <div className="subcat-bar">
            <button
              type="button"
              className={`subcat-pill ${activeLevel2 === ALL_TAB ? "is-active" : ""}`}
              onClick={() => setActiveLevel2(ALL_TAB)}
            >
              全部 <span className="subcat-count">{sectorIndicators.length}</span>
            </button>
            {level2Groups.map(({ level2, count }) => (
              <button
                key={level2}
                type="button"
                className={`subcat-pill ${activeLevel2 === level2 ? "is-active" : ""}`}
                onClick={() => setActiveLevel2(level2)}
              >
                {level2} <span className="subcat-count">{count}</span>
              </button>
            ))}
          </div>
        )}

        {activeLevel2 === "实时行情" && (
          <div className="rate-limit-warning">
            <span className="warning-icon">⚠️</span>
            <div>
              <strong>限流风险提示</strong>
              <p>
                实时行情指标会触发大量数据请求，容易被数据供应商限流或拒绝连接。建议按需提取，避免短时间内频繁操作。
              </p>
            </div>
          </div>
        )}

        <div className="indicator-grid">
          {filteredIndicators.length === 0 && (
            <div className="empty-hint">
              {sectorIndicators.length === 0
                ? "该板块暂未注册指标。"
                : "没有符合条件的指标。"}
            </div>
          )}
          {filteredIndicators.map((indicator) => (
            <button
              key={indicator.id}
              type="button"
              className="indicator-card"
              onClick={() => onSelectIndicator(indicator.id)}
            >
              <div className="indicator-card-top">
                <span className="indicator-tag">{indicator.level3}</span>
                <span className="indicator-sub-badge">{indicator.level2}</span>
              </div>
              <h4>{indicator.name}</h4>
              {indicator.source_name && (
                <span
                  className="source-badge"
                  style={{ backgroundColor: SOURCE_COLORS[indicator.source] || "#666" }}
                >
                  {indicator.source_name}
                  {indicator.update_frequency && ` · ${indicator.update_frequency}`}
                </span>
              )}
              <p>{indicator.description}</p>
              <span className="indicator-cta">进入提取页面 →</span>
            </button>
          ))}
        </div>
      </section>
    </section>
  );
}
