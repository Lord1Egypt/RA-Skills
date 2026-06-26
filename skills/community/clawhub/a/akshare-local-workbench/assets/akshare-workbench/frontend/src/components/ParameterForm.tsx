import type { Indicator, IndicatorParam } from "../types";
import type { ParamValue, ParamValues } from "../utils/dateLink";

interface ParameterFormProps {
  indicator: Indicator;
  values: ParamValues;
  loading: boolean;
  onChange: (name: string, value: ParamValue) => void;
  onSubmit: (refresh?: boolean) => void;
  onClear: () => void;
}

function optionLabel(value: string): string {
  if (value === "") {
    return "不复权 / 空值";
  }
  return value;
}

function renderInput(
  param: IndicatorParam,
  value: ParamValue,
  onChange: (name: string, value: ParamValue) => void
) {
  if (param.type === "select") {
    return (
      <select
        value={String(value ?? "")}
        onChange={(event) => onChange(param.name, event.target.value)}
      >
        {(param.options ?? []).map((option) => (
          <option key={`${param.name}-${option}`} value={option}>
            {optionLabel(option)}
          </option>
        ))}
      </select>
    );
  }

  if (param.type === "boolean") {
    return (
      <label className="checkbox-row">
        <input
          checked={Boolean(value)}
          type="checkbox"
          onChange={(event) => onChange(param.name, event.target.checked)}
        />
        启用
      </label>
    );
  }

  const inputType = param.type === "integer" || param.type === "number" ? "number" : param.type;
  return (
    <input
      value={String(value ?? "")}
      type={inputType}
      placeholder={param.placeholder ?? undefined}
      onChange={(event) => onChange(param.name, event.target.value)}
    />
  );
}

export function ParameterForm({
  indicator,
  values,
  loading,
  onChange,
  onSubmit,
  onClear
}: ParameterFormProps) {
  return (
    <section className="panel parameter-panel">
      <div className="panel-heading">
        <p className="eyebrow">
          {indicator.level1} / {indicator.level2} / {indicator.level3}
        </p>
        <h2>{indicator.name}</h2>
        <p className="panel-desc">{indicator.description}</p>
        <a
          className="docs-link"
          href={indicator.docs_url}
          target="_blank"
          rel="noreferrer"
        >
          查看 AKShare 文档 ↗
        </a>
      </div>

      <div className="param-grid">
        {indicator.params.length === 0 ? (
          <div className="no-params">该指标无需额外参数，可直接提取。</div>
        ) : (
          indicator.params.map((param) => (
            <label className="field" key={param.name}>
              <span>
                {param.label}
                {param.required && <b>*</b>}
              </span>
              {renderInput(param, values[param.name] ?? "", onChange)}
              {param.description && <small>{param.description}</small>}
            </label>
          ))
        )}
      </div>

      {indicator.result_notes && (
        <p className="result-note">{indicator.result_notes}</p>
      )}

      <div className="actions">
        <button
          className="primary-button"
          disabled={loading}
          onClick={() => onSubmit()}
          type="button"
        >
          {loading ? "提取中..." : "提取"}
        </button>
        <button
          className="ghost-button"
          disabled={loading}
          onClick={() => onSubmit(true)}
          type="button"
          title="绕过本地缓存，重新请求数据源"
        >
          强制刷新
        </button>
        <button
          className="ghost-button"
          disabled={loading}
          onClick={onClear}
          type="button"
        >
          清理 / 新任务
        </button>
      </div>
    </section>
  );
}
