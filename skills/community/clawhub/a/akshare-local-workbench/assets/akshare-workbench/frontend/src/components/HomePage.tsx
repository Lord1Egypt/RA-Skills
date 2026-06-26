import { useEffect, useState } from "react";

import { getAIConfig } from "../services/api";
import type { SectorSummary } from "../types";

import { AIChatPanel } from "./AIChatPanel";
import { AISettingsModal } from "./AISettingsModal";

interface HomePageProps {
  sectors: SectorSummary[];
  onSelectSector: (sectorId: string) => void;
}

export function HomePage({ sectors, onSelectSector }: HomePageProps) {
  const [configured, setConfigured] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);

  useEffect(() => {
    getAIConfig()
      .then((cfg) => setConfigured(cfg.configured))
      .catch(() => undefined);
  }, []);

  return (
    <section className="home-page">
      <div className="hero">
        <h1>选择板块，提取数据</h1>
        <p className="hero-sub">
          覆盖 {sectors.length} 个数据板块，支持 AI 智能取数、在线预览与导出
        </p>
      </div>

      {settingsOpen && (
        <AISettingsModal
          onClose={() => setSettingsOpen(false)}
          onSaved={(cfg) => setConfigured(cfg.configured)}
        />
      )}

      <div className="section-header home-section-header">
        <h3 className="section-title">按板块浏览</h3>
      </div>

      <div className="sector-grid">
        {sectors.map((sector) => (
          <button
            key={sector.id}
            type="button"
            className="sector-card"
            onClick={() => onSelectSector(sector.id)}
            style={{ ["--accent" as string]: sector.accent } as Record<string, string>}
          >
            <div className="sector-card-top">
              <span className="sector-count">{sector.indicator_count} 指标</span>
            </div>
            <h3 className="sector-name">{sector.name}</h3>
            <p className="sector-desc">{sector.description}</p>
            <span className="sector-cta">进入 →</span>
          </button>
        ))}
      </div>

      <div className="section-header home-section-header home-section-gap">
        <h3 className="section-title">AI 智能取数</h3>
      </div>

      <AIChatPanel configured={configured} onOpenSettings={() => setSettingsOpen(true)} />
    </section>
  );
}
