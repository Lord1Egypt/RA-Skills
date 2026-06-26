import { useMemo, useState } from "react";

import type { IndicatorParam } from "../types";

type FieldValue = string | number | boolean | null;

interface CollectFormProps {
  indicatorName: string;
  form: IndicatorParam[];
  baseParams: Record<string, FieldValue>;
  onSubmit?: (values: Record<string, FieldValue>) => void;
  // When true the form is shown as a read-only record of an earlier choice:
  // all controls stay visible (selected pills highlighted) but become inactive.
  disabled?: boolean;
}

function pad(value: number): string {
  return String(value).padStart(2, "0");
}

function toISO(date: Date): string {
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

function shiftDays(days: number): string {
  const date = new Date();
  date.setDate(date.getDate() + days);
  return toISO(date);
}

function shiftMonths(months: number): string {
  const date = new Date();
  date.setMonth(date.getMonth() + months);
  return toISO(date);
}

const DATE_PRESETS: { label: string; value: () => string }[] = [
  { label: "今天", value: () => toISO(new Date()) },
  { label: "一周前", value: () => shiftDays(-7) },
  { label: "一月前", value: () => shiftMonths(-1) },
  { label: "三月前", value: () => shiftMonths(-3) },
  { label: "今年初", value: () => `${new Date().getFullYear()}-01-01` },
  { label: "一年前", value: () => shiftMonths(-12) }
];

function base_has(base: Record<string, FieldValue>, name: string): boolean {
  const value = base[name];
  return value != null && value !== "";
}

function initialValue(param: IndicatorParam, base: Record<string, FieldValue>): FieldValue {
  if (param.name in base && base[param.name] != null && base[param.name] !== "") {
    return base[param.name];
  }
  if (param.type === "boolean") return Boolean(param.default ?? false);
  if (param.default != null) return param.default;
  return "";
}

export function CollectForm({
  indicatorName,
  form,
  baseParams,
  onSubmit,
  disabled = false
}: CollectFormProps) {
  const [values, setValues] = useState<Record<string, FieldValue>>(() => {
    const initial: Record<string, FieldValue> = {};
    for (const param of form) initial[param.name] = initialValue(param, baseParams);
    return initial;
  });

  const incomplete = useMemo(
    () =>
      form.some((param) => {
        if (!param.required) return false;
        const value = values[param.name];
        return value === "" || value === null || value === undefined;
      }),
    [form, values]
  );

  // If the AI pre-filled a text/date field with a suggested value, the primary
  // action reads as "采纳" (accept the suggestion); otherwise "开始提取".
  const hasSuggestion = useMemo(
    () =>
      form.some(
        (param) =>
          (param.type === "string" || param.type === "date") &&
          base_has(baseParams, param.name)
      ),
    [form, baseParams]
  );

  function setValue(name: string, value: FieldValue) {
    setValues((prev) => ({ ...prev, [name]: value }));
  }

  return (
    <div className={`ai-bubble ai-assistant collect-bubble ${disabled ? "is-disabled" : ""}`}>
      <div className="collect-head">
        <span className="collect-chip">{disabled ? "已选择参数" : "需补充参数"}</span>
        <span className="collect-name">{indicatorName}</span>
      </div>

      <div className="collect-fields">
        {form.map((param) => {
          const current = values[param.name];
          return (
            <div className="collect-field" key={param.name}>
              <span className="collect-label">
                {param.label || param.name}
                {param.required && <b> *</b>}
              </span>

              {param.type === "select" && param.options ? (
                <div className="collect-chips">
                  {param.options.map((option) => (
                    <button
                      type="button"
                      key={option || "__default__"}
                      className={`collect-pick ${String(current) === option ? "is-active" : ""}`}
                      disabled={disabled}
                      onClick={() => setValue(param.name, option)}
                    >
                      {option === "" ? "默认" : option}
                    </button>
                  ))}
                </div>
              ) : param.type === "boolean" ? (
                <label className="collect-checkbox">
                  <input
                    type="checkbox"
                    checked={Boolean(current)}
                    disabled={disabled}
                    onChange={(e) => setValue(param.name, e.target.checked)}
                  />
                  <span>{param.description ?? "启用"}</span>
                </label>
              ) : param.type === "date" ? (
                <>
                  <div className="collect-chips">
                    {DATE_PRESETS.map((preset) => {
                      const presetValue = preset.value();
                      return (
                        <button
                          type="button"
                          key={preset.label}
                          className={`collect-pick ${current === presetValue ? "is-active" : ""}`}
                          disabled={disabled}
                          onClick={() => setValue(param.name, presetValue)}
                        >
                          {preset.label}
                        </button>
                      );
                    })}
                  </div>
                  <input
                    className="collect-input"
                    type="date"
                    value={String(current ?? "")}
                    disabled={disabled}
                    onChange={(e) => setValue(param.name, e.target.value)}
                  />
                </>
              ) : (
                <input
                  className="collect-input"
                  type="text"
                  value={String(current ?? "")}
                  placeholder={param.placeholder ?? param.description ?? ""}
                  disabled={disabled}
                  onChange={(e) => setValue(param.name, e.target.value)}
                />
              )}

              {param.description && param.type !== "boolean" && param.type !== "select" && (
                <span className="collect-hint">{param.description}</span>
              )}
            </div>
          );
        })}
      </div>

      <div className="collect-actions">
        <button
          type="button"
          className="primary-button"
          disabled={disabled || incomplete}
          onClick={() => onSubmit?.(values)}
        >
          {disabled ? "已提交" : hasSuggestion ? "采纳并提取" : "开始提取"}
        </button>
        {!disabled && (
          <span className="collect-tip">不对的话，可直接修改上方内容或在下方对话框描述</span>
        )}
      </div>
    </div>
  );
}
