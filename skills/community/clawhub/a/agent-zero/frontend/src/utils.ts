/** Compact price: $1.8M / $850K / $500. Returns null for null input. */
export function formatPriceCompact(price: number | null): string | null {
  if (price == null) return null
  if (price >= 1_000_000) return `$${(price / 1_000_000).toFixed(1).replace(/\.0$/, '')}M`
  if (price >= 1_000) return `$${Math.round(price / 1_000)}K`
  return `$${price}`
}

/** Full price with currency via Intl (e.g. CA$1,250,000). Returns null for null input. */
export function formatPriceFull(price: number | null, currency: string | null): string | null {
  if (price == null) return null
  return new Intl.NumberFormat('en-CA', {
    style: 'currency',
    currency: currency ?? 'CAD',
    maximumFractionDigits: 0,
  }).format(price)
}
