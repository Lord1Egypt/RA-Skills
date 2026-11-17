// Exact signed decimal accounting. Arithmetic amounts serialize as strings.
const SCALE = 10n ** 18n;
export function decimal(value, label = "decimal") {
  if (typeof value !== "string" || !/^-?\d{1,24}(?:\.\d{1,18})?$/.test(value.trim())) {
    throw new Error(`${label} must be a signed decimal string with at most 18 decimal places`);
  }
  const text = value.trim();
  const [whole, fraction = ""] = text.replace(/^-/, "").split(".");
  return (text.startsWith("-") ? -1n : 1n) * (BigInt(whole) * SCALE + BigInt(fraction.padEnd(18, "0")));
}
export function amount(value) {
  const sign = value < 0n ? "-" : "";
  const absolute = value < 0n ? -value : value;
  const fraction = (absolute % SCALE).toString().padStart(18, "0").replace(/0+$/, "");
  return `${sign}${absolute / SCALE}${fraction ? `.${fraction}` : ""}`;
}
export function multiply(a, b) { return a * b / SCALE; }
export function absolute(value) { return value < 0n ? -value : value; }
export function percent(a, b) { return b === 0n ? null : Number(a * 1000000n / b) / 10000; }
