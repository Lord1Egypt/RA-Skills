import { useEffect, useState } from "react";

import {
  buildExportUrl,
  clearTask,
  fetchIndicator,
  runExtraction
} from "../services/api";
import type { ExportFormat, Indicator, RunResponse, SectorSummary } from "../types";
import { applyDateLink, type ParamValue, type ParamValues } from "../utils/dateLink";

import { DataPreview } from "./DataPreview";
import { ParameterForm } from "./ParameterForm";

interface IndicatorPageProps {
  indicatorId: string;
  sector: SectorSummary | null;
  onBack: () => void;
  onBackHome: () => void;
}

function defaultParams(indicator: Indicator): ParamValues {
  return indicator.params.reduce<ParamValues>((acc, param) => {
    acc[param.name] = (param.default as ParamValue | undefined) ?? "";
    return acc;
  }, {});
}

export function IndicatorPage({
  indicatorId,
  sector,
  onBack,
  onBackHome
}: IndicatorPageProps) {
  const [indicator, setIndicator] = useState<Indicator | null>(null);
  const [params, setParams] = useState<ParamValues>({});
  const [result, setResult] = useState<RunResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setError(null);
    setResult(null);

    fetchIndicator(indicatorId)
      .then((detail) => {
        if (!active) return;
        setIndicator(detail);
        setParams(defaultParams(detail));
      })
      .catch((err: Error) => active && setError(err.message));

    return () => {
      active = false;
    };
  }, [indicatorId]);

  function handleParamChange(name: string, value: ParamValue) {
    setParams((current) => applyDateLink(indicator, current, name, value));
  }

  async function handleSubmit(refresh = false) {
    if (!indicator) {
      return;
    }
    setLoading(true);
    setError(null);
    try {
      if (result) {
        await clearTask(result.task_id).catch(() => undefined);
      }
      const nextResult = await runExtraction(indicator.id, params, refresh);
      setResult(nextResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : "提取失败");
    } finally {
      setLoading(false);
    }
  }

  async function handleClear() {
    if (result) {
      await clearTask(result.task_id).catch(() => undefined);
    }
    setResult(null);
    if (indicator) {
      setParams(defaultParams(indicator));
    }
    setError(null);
  }

  function handleExport(format: ExportFormat) {
    if (!result) {
      return;
    }
    window.open(buildExportUrl(result.task_id, format), "_blank", "noopener,noreferrer");
  }

  const accentStyle = sector
    ? ({ ["--accent" as string]: sector.accent } as Record<string, string>)
    : undefined;

  return (
    <section className="indicator-page" style={accentStyle}>
      <nav className="breadcrumb">
        <button type="button" className="link-button" onClick={onBackHome}>
          首页
        </button>
        {sector && (
          <>
            <span className="breadcrumb-sep">/</span>
            <button type="button" className="link-button" onClick={onBack}>
              {sector.name}
            </button>
          </>
        )}
        <span className="breadcrumb-sep">/</span>
        <span className="breadcrumb-current">
          {indicator?.name ?? "加载中…"}
        </span>
        {sector && (
          <button
            type="button"
            className="ghost-button breadcrumb-back"
            onClick={onBack}
          >
            ← 返回板块
          </button>
        )}
      </nav>

      {indicator?.source_name && (
        <div className="indicator-source-bar">
          <span
            className="source-badge"
            style={{
              backgroundColor:
                {
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
                }[indicator.source] || "#666",
            }}
          >
            {indicator.source_name}
            {indicator.update_frequency && ` · ${indicator.update_frequency}`}
          </span>
        </div>
      )}

      {indicator?.level2 === "实时行情" && (
        <div className="rate-limit-warning">
          <span className="warning-icon">⚠️</span>
          <div>
            <strong>限流风险提示</strong>
            <p>
              实时行情数据量大，容易被数据供应商限流或拒绝连接。如遇失败，请等待数分钟后重试，避免短时间内频繁提取。
            </p>
          </div>
        </div>
      )}

      {error && <div className="error-banner">{error}</div>}

      <div className="workspace-grid">
        {indicator ? (
          <ParameterForm
            indicator={indicator}
            values={params}
            loading={loading}
            onChange={handleParamChange}
            onSubmit={handleSubmit}
            onClear={handleClear}
          />
        ) : (
          <section className="panel parameter-panel">
            <p>加载指标中...</p>
          </section>
        )}
        <DataPreview result={result} onExport={handleExport} />
      </div>
    </section>
  );
}
