const integerFormatter = new Intl.NumberFormat("en-US", {
  maximumFractionDigits: 0
});

const decimalFormatter = new Intl.NumberFormat("en-US", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
});

export function formatCellValue(value: unknown): string {
  if (value === null || value === undefined) {
    return "";
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) {
      return "";
    }
    if (Number.isInteger(value)) {
      return integerFormatter.format(value);
    }
    return decimalFormatter.format(value);
  }
  if (typeof value === "string") {
    const trimmed = value.trim();
    if (trimmed === "") {
      return "";
    }
    const numeric = Number(trimmed.replace(/,/g, ""));
    if (Number.isFinite(numeric) && /^-?\d[\d.,]*$/.test(trimmed)) {
      if (trimmed.includes(".")) {
        return decimalFormatter.format(numeric);
      }
      return integerFormatter.format(numeric);
    }
    return value;
  }
  if (typeof value === "boolean") {
    return value ? "是" : "否";
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  return String(value);
}

export function formatSignedPercent(value: number | null | undefined): string {
  if (value === null || value === undefined || !Number.isFinite(value)) {
    return "—";
  }
  const formatted = decimalFormatter.format(value);
  return value > 0 ? `+${formatted}%` : `${formatted}%`;
}
