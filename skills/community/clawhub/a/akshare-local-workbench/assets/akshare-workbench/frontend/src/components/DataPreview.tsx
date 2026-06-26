import { useEffect, useMemo, useState } from "react";

import type { ExportFormat, RunResponse } from "../types";
import { formatCellValue } from "../utils/format";

export type PreviewStatus = "idle" | "fetching";

interface DataPreviewProps {
  result: RunResponse | null;
  status?: PreviewStatus;
  onExport: (format: ExportFormat) => void;
  onClear?: () => void;
}

const EXPORT_FORMATS: ExportFormat[] = ["xlsx", "csv", "json"];

export function DataPreview({ result, status = "idle", onExport, onClear }: DataPreviewProps) {
  const allColumns = result?.columns ?? [];
  const [activeColumns, setActiveColumns] = useState<Set<string>>(new Set());

  useEffect(() => {
    setActiveColumns(new Set(allColumns));
  }, [result?.task_id, allColumns.join("|")]);

  const visibleColumns = useMemo(
    () => allColumns.filter((column) => activeColumns.has(column)),
    [allColumns, activeColumns]
  );

  function toggleColumn(column: string) {
    setActiveColumns((current) => {
      const next = new Set(current);
      if (next.has(column)) {
        if (next.size === 1) return next;
        next.delete(column);
      } else {
        next.add(column);
      }
      return next;
    });
  }

  function setAll(active: boolean) {
    setActiveColumns(active ? new Set(allColumns) : new Set(allColumns.slice(0, 1)));
  }

  const hasResult = Boolean(result);

  return (
    <section className="panel preview-panel">
      <div className="panel-heading split-heading">
        <div>
          <p className="eyebrow">Result Preview</p>
          <h2>{hasResult ? result!.indicator_name : "结果预览"}</h2>
          <p className="panel-desc">
            {hasResult
              ? `共 ${result!.row_count.toLocaleString("en-US")} 行 · ${result!.column_count} 列 · 预览前 ${result!.preview.length} 行`
              : "提取完成后，这里会显示前 500 行预览（按日期数据自动倒序），并支持按字段点亮 / 隐藏列。"}
          </p>
        </div>
        <div className="preview-toolbar">
          <button
            type="button"
            className="ghost-button preview-clear"
            disabled={!hasResult}
            onClick={() => onClear?.()}
          >
            清除
          </button>
          <div className="export-buttons">
            {EXPORT_FORMATS.map((format) => (
              <button
                key={format}
                type="button"
                className="export-button"
                disabled={!hasResult}
                onClick={() => onExport(format)}
              >
                {format.toUpperCase()}
              </button>
            ))}
          </div>
        </div>
      </div>

      {hasResult ? (
        <>
          <div className="column-toggles">
            <div className="column-toggle-head">
              <span className="column-toggle-label">字段</span>
              <div className="column-toggle-actions">
                <button type="button" className="link-button" onClick={() => setAll(true)}>
                  全部点亮
                </button>
                <button type="button" className="link-button" onClick={() => setAll(false)}>
                  仅留首列
                </button>
              </div>
            </div>
            <div className="column-toggle-pills">
              {allColumns.map((column) => {
                const active = activeColumns.has(column);
                return (
                  <button
                    key={column}
                    type="button"
                    className={`column-pill ${active ? "is-active" : ""}`}
                    onClick={() => toggleColumn(column)}
                  >
                    <span className="column-pill-dot" />
                    {column}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  {visibleColumns.map((column) => (
                    <th key={column}>{column}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {result!.preview.map((row, rowIndex) => (
                  <tr key={`row-${rowIndex}`}>
                    {visibleColumns.map((column) => (
                      <td key={`${rowIndex}-${column}`}>{formatCellValue(row[column])}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : status === "fetching" ? (
        <FetchingState />
      ) : (
        <IdleState />
      )}
    </section>
  );
}

function FetchingState() {
  return (
    <div className="preview-body preview-fetching">
      <div className="preview-state-head">
        <h3 className="preview-state-title">
          等待提取结果
          <span className="typing-dots">
            <i />
            <i />
            <i />
          </span>
        </h3>
        <p className="panel-desc">已匹配接口，正在从数据源拉取，结果将在此呈现</p>
      </div>
      <div className="skeleton-toolbar">
        <span className="skeleton-chip" />
        <span className="skeleton-chip" />
        <span className="skeleton-chip" />
      </div>
      <div className="skeleton-table" aria-hidden="true">
        {Array.from({ length: 7 }).map((_, rowIndex) => (
          <div className="skeleton-row" key={`sk-row-${rowIndex}`}>
            {Array.from({ length: 5 }).map((__, cellIndex) => (
              <span
                className="skeleton-cell"
                key={`sk-cell-${rowIndex}-${cellIndex}`}
                style={{ animationDelay: `${(rowIndex * 5 + cellIndex) * 55}ms` }}
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

function IdleState() {
  return (
    <div className="preview-body preview-idle" aria-hidden="true">
      <div className="idle-orb">
        <span className="idle-bar" />
        <span className="idle-bar" />
        <span className="idle-bar" />
        <span className="idle-bar" />
      </div>
      <p className="idle-text">暂无数据</p>
      <p className="idle-sub">在左侧用一句话描述你想要的数据，结果会在这里实时呈现</p>
    </div>
  );
}
