import { useCallback, useEffect, useMemo, useState } from "react";

import { Footer } from "./components/Footer";
import { Header } from "./components/Header";
import { HomePage } from "./components/HomePage";
import { IndicatorPage } from "./components/IndicatorPage";
import { SectorNav } from "./components/SectorNav";
import { SectorPage } from "./components/SectorPage";
import { TickerBar } from "./components/TickerBar";
import {
  clearAllTasks,
  fetchIndicators,
  fetchSectors
} from "./services/api";
import type { IndicatorSummary, SectorSnapshot, SectorSummary } from "./types";

const TICKER_SECTORS = ["equity_index", "fx", "rate"];

export default function App() {
  const [sectors, setSectors] = useState<SectorSummary[]>([]);
  const [indicators, setIndicators] = useState<IndicatorSummary[]>([]);
  const [currentSectorId, setCurrentSectorId] = useState<string | null>(null);
  const [currentIndicatorId, setCurrentIndicatorId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [snapshotCache, setSnapshotCache] = useState<Record<string, SectorSnapshot>>({});

  const handleSnapshotLoaded = useCallback((sectorId: string, snapshot: SectorSnapshot) => {
    setSnapshotCache((prev) => ({ ...prev, [sectorId]: snapshot }));
  }, []);

  useEffect(() => {
    const controller = new AbortController();

    clearAllTasks().catch(() => undefined);

    fetchSectors(controller.signal)
      .then(setSectors)
      .catch((err: Error) => {
        if (err.name !== "AbortError") setError(err.message);
      });

    fetchIndicators(undefined, controller.signal)
      .then(setIndicators)
      .catch((err: Error) => {
        if (err.name !== "AbortError") setError(err.message);
      });

    const cleanup = () => {
      fetch("/api/tasks", { method: "DELETE", keepalive: true }).catch(() => undefined);
    };
    window.addEventListener("beforeunload", cleanup);
    return () => {
      controller.abort();
      window.removeEventListener("beforeunload", cleanup);
    };
  }, []);

  const activeSector = useMemo(
    () => sectors.find((sector) => sector.id === currentSectorId) ?? null,
    [sectors, currentSectorId]
  );

  function handleSelectSector(sectorId: string | null) {
    setCurrentSectorId(sectorId);
    setCurrentIndicatorId(null);
  }

  function handleSelectIndicator(indicatorId: string) {
    if (!currentSectorId) {
      const indicator = indicators.find((ind) => ind.id === indicatorId);
      if (indicator) {
        const matchingSector = sectors.find((s) => s.name === indicator.level1);
        if (matchingSector) {
          setCurrentSectorId(matchingSector.id);
        }
      }
    }
    setCurrentIndicatorId(indicatorId);
  }

  function handleBackToSector() {
    setCurrentIndicatorId(null);
  }

  function handleBackHome() {
    setCurrentSectorId(null);
    setCurrentIndicatorId(null);
  }

  return (
    <div className="app-shell">
      <Header
        sectorCount={sectors.length}
        indicatorCount={indicators.length}
      />

      <SectorNav
        sectors={sectors}
        activeSectorId={currentSectorId}
        onSelect={handleSelectSector}
      />

      <TickerBar
        sectorIds={TICKER_SECTORS}
        sectors={sectors}
        snapshotCache={snapshotCache}
      />

      <main className="site-main">
        {error && <div className="error-banner global">{error}</div>}

        {!activeSector && !currentIndicatorId && (
          <HomePage sectors={sectors} onSelectSector={handleSelectSector} />
        )}

        {activeSector && !currentIndicatorId && (
          <SectorPage
            sectorSummary={activeSector}
            indicators={indicators}
            cachedSnapshot={snapshotCache[activeSector.id] ?? null}
            onSnapshotLoaded={handleSnapshotLoaded}
            onSelectIndicator={handleSelectIndicator}
          />
        )}

        {currentIndicatorId && (
          <IndicatorPage
            indicatorId={currentIndicatorId}
            sector={activeSector}
            onBack={handleBackToSector}
            onBackHome={handleBackHome}
          />
        )}
      </main>

      <Footer />
    </div>
  );
}
