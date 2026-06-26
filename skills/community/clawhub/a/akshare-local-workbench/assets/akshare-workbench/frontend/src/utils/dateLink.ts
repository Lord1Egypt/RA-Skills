import type { Indicator } from "../types";

export type ParamValue = string | number | boolean | null;
export type ParamValues = Record<string, ParamValue>;

const START_FIELDS = new Set(["start_date", "begin_date", "from_date"]);
const END_FIELDS = new Set(["end_date", "stop_date", "to_date"]);

function findField(indicator: Indicator | null, names: Set<string>): string | null {
  if (!indicator) {
    return null;
  }
  const match = indicator.params.find(
    (param) => param.type === "date" && names.has(param.name)
  );
  return match ? match.name : null;
}

export function applyDateLink(
  indicator: Indicator | null,
  values: ParamValues,
  changedName: string,
  changedValue: ParamValue
): ParamValues {
  const startField = findField(indicator, START_FIELDS);
  const endField = findField(indicator, END_FIELDS);

  const next: ParamValues = { ...values, [changedName]: changedValue };

  if (!startField || !endField) {
    return next;
  }

  if (changedName !== startField) {
    return next;
  }

  const startValue = typeof changedValue === "string" ? changedValue : "";
  const currentEnd = next[endField];
  const endValue = typeof currentEnd === "string" ? currentEnd : "";

  if (!startValue) {
    return next;
  }

  if (!endValue || endValue < startValue) {
    next[endField] = startValue;
  }

  return next;
}
