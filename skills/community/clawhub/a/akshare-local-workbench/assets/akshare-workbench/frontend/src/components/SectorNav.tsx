import type { SectorSummary } from "../types";

interface SectorNavProps {
  sectors: SectorSummary[];
  activeSectorId: string | null;
  onSelect: (sectorId: string | null) => void;
}

export function SectorNav({ sectors, activeSectorId, onSelect }: SectorNavProps) {
  return (
    <nav className="sector-nav">
      <div className="sector-nav-inner">
        <button
          type="button"
          className={`sector-tab home-tab ${activeSectorId === null ? "is-active" : ""}`}
          onClick={() => onSelect(null)}
        >
          <span className="sector-tab-name">首页</span>
        </button>
        {sectors.map((sector) => {
          const active = activeSectorId === sector.id;
          return (
            <button
              key={sector.id}
              type="button"
              className={`sector-tab ${active ? "is-active" : ""}`}
              onClick={() => onSelect(sector.id)}
              style={{ ["--accent" as string]: sector.accent } as Record<string, string>}
            >
              <span className="sector-tab-name">{sector.name}</span>
              <span className="sector-tab-count">{sector.indicator_count}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}
