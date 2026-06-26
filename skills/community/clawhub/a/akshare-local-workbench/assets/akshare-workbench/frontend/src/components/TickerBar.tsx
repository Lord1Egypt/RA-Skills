import { useMemo } from "react";

import type { SectorSnapshot, SectorSummary } from "../types";

interface TickerBarProps {
  sectorIds: string[];
  sectors: SectorSummary[];
  snapshotCache: Record<string, SectorSnapshot>;
}

interface TickerItem {
  key: string;
  label: string;
  value: string;
  unit: string;
  change: string | null;
  direction: "up" | "down" | "flat";
  accent: string;
  pending: boolean;
}

interface PlaceholderCard {
  label: string;
  decimals: number;
  unit: string;
}

// Card metadata mirrors backend/app/catalog/sectors.yaml so the ticker can keep
// scrolling with zero-valued placeholders before the first snapshot arrives.
const PLACEHOLDERS: Record<string, PlaceholderCard[]> = {
  equity_index: [
    { label: "上证指数", decimals: 2, unit: "" },
    { label: "沪深300", decimals: 2, unit: "" },
    { label: "创业板指", decimals: 2, unit: "" },
    { label: "上证50", decimals: 2, unit: "" },
    { label: "中证500", decimals: 2, unit: "" },
    { label: "北向资金净买额", decimals: 2, unit: "亿元" }
  ],
  fx: [
    { label: "美元兑人民币", decimals: 4, unit: "" },
    { label: "欧元兑人民币", decimals: 4, unit: "" },
    { label: "100 日元兑人民币", decimals: 4, unit: "" },
    { label: "英镑兑人民币", decimals: 4, unit: "" },
    { label: "港币兑人民币", decimals: 4, unit: "" },
    { label: "澳元兑人民币", decimals: 4, unit: "" }
  ],
  rate: [
    { label: "1 年期 LPR", decimals: 2, unit: "%" },
    { label: "5 年期 LPR", decimals: 2, unit: "%" },
    { label: "Shibor 隔夜", decimals: 2, unit: "%" },
    { label: "Shibor 3 月", decimals: 2, unit: "%" },
    { label: "Shibor 1 年", decimals: 2, unit: "%" },
    { label: "美联储基准利率", decimals: 2, unit: "%" }
  ]
};

function formatZero(decimals: number): string {
  return (0).toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  });
}

export function TickerBar({ sectorIds, sectors, snapshotCache }: TickerBarProps) {
  const items = useMemo<TickerItem[]>(() => {
    const accentOf = (sectorId: string) =>
      sectors.find((s) => s.id === sectorId)?.accent ?? "#1e6ee8";

    const collected: TickerItem[] = [];
    sectorIds.forEach((sectorId) => {
      const accent = accentOf(sectorId);
      const snapshot = snapshotCache[sectorId];

      if (snapshot && snapshot.cards.length > 0) {
        snapshot.cards.forEach((card) => {
          const hasValue = card.value !== null;
          collected.push({
            key: `${sectorId}-${card.title}`,
            label: card.title,
            // Cards that haven't resolved yet (or failed) show a formatted 0
            // instead of being dropped, so the bar stays populated.
            value: hasValue ? card.value_display : formatZero(card.decimals),
            unit: card.unit,
            change: hasValue ? card.change_display : null,
            direction:
              !hasValue || card.change === null || card.change === 0
                ? "flat"
                : card.change > 0
                  ? "up"
                  : "down",
            accent,
            pending: !hasValue
          });
        });
        return;
      }

      // No snapshot fetched yet: emit zero-valued placeholders so the marquee
      // keeps scrolling the moment the user lands on the page.
      (PLACEHOLDERS[sectorId] ?? []).forEach((card) => {
        collected.push({
          key: `${sectorId}-${card.label}`,
          label: card.label,
          value: formatZero(card.decimals),
          unit: card.unit,
          change: null,
          direction: "flat",
          accent,
          pending: true
        });
      });
    });
    return collected;
  }, [sectorIds, sectors, snapshotCache]);

  if (items.length === 0) return null;

  // Duplicate the track so the marquee loops seamlessly.
  const track = [...items, ...items];

  return (
    <div className="ticker-bar" role="marquee" aria-label="实时核心报价">
      <span className="ticker-live">
        <span className="ticker-live-dot" />
        LIVE
      </span>
      <div className="ticker-viewport">
        <div className="ticker-track">
          {track.map((item, index) => (
            <span
              className={`ticker-item ${item.pending ? "is-pending" : ""}`}
              key={`${item.key}-${index}`}
              aria-hidden={index >= items.length}
            >
              <span className="ticker-dot" style={{ background: item.accent }} />
              <span className="ticker-label">{item.label}</span>
              <span className="ticker-value">
                {item.value}
                {item.unit && <span className="ticker-unit">{item.unit}</span>}
              </span>
              {item.change && (
                <span className={`ticker-change is-${item.direction}`}>
                  {item.direction === "up" ? "▲" : item.direction === "down" ? "▼" : "•"}{" "}
                  {item.change}
                </span>
              )}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
