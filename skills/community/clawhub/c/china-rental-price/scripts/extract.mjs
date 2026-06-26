function toPriceNumber(raw) {
  const value = Number(String(raw).replace(/,/g, ""));
  if (!Number.isFinite(value) || value < 20 || value > 50000) {
    return null;
  }

  return Math.round(value * 100) / 100;
}

export function extractPriceSignalsFromText(text) {
  const source = String(text || "").replace(/\u00a0/g, " ");
  const results = [];
  const patterns = [
    { regex: /(?:¥|￥|RMB|CNY)\s*([0-9]{2,5}(?:\.[0-9]{1,2})?)/gi, unit: "unknown" },
    { regex: /([0-9]{2,5}(?:\.[0-9]{1,2})?)\s*元\s*(起|\/天|每天|\/日)?/gi, unit: "unknown" }
  ];

  for (const pattern of patterns) {
    let match;
    while ((match = pattern.regex.exec(source)) !== null) {
      const price = toPriceNumber(match[1]);
      if (!price) {
        continue;
      }

      const snippet = source.slice(Math.max(0, match.index - 40), Math.min(source.length, match.index + 80));
      results.push({
        price,
        snippet: snippet.trim(),
        pricingUnit: /\/天|每天|\/日/.test(match[0]) ? "day" : "unknown"
      });
    }
  }

  return dedupePriceSignals(results);
}

export function dedupePriceSignals(items) {
  const seen = new Set();
  const deduped = [];
  for (const item of items) {
    const key = `${item.price}:${item.pricingUnit}:${item.snippet}`;
    if (seen.has(key)) {
      continue;
    }
    seen.add(key);
    deduped.push(item);
  }
  return deduped.sort((a, b) => a.price - b.price);
}

export function summarizeSignals(signals) {
  if (!signals.length) {
    return {
      priceMin: null,
      priceTotalIfAvailable: null,
      availableCars: 0,
      vehicleClass: null,
      pricingUnit: null
    };
  }

  const sortedSignals = [...signals].sort((a, b) => a.price - b.price);

  return {
    priceMin: sortedSignals[0].price,
    priceTotalIfAvailable: sortedSignals.find((item) => item.pricingUnit === "unknown")?.price ?? sortedSignals[0].price,
    availableCars: sortedSignals.length,
    vehicleClass: guessVehicleClass(sortedSignals),
    pricingUnit: sortedSignals[0].pricingUnit
  };
}

function guessVehicleClass(signals) {
  const snippet = signals.map((item) => item.snippet).join(" ");
  const labels = [
    "经济型",
    "舒适型",
    "紧凑型",
    "SUV",
    "商务",
    "MPV",
    "豪华型",
    "中大型"
  ];

  return labels.find((label) => snippet.includes(label)) || null;
}
