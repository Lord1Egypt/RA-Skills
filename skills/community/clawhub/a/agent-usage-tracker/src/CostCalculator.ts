import { ModelPricing } from "./types.js";

export class CostCalculator {
  private readonly pricing = new Map<string, ModelPricing>();

  constructor(initialPricing: Record<string, ModelPricing> = {}) {
    for (const [model, price] of Object.entries(initialPricing)) {
      this.setPricing(model, price);
    }
  }

  setPricing(model: string, pricing: ModelPricing): void {
    if (pricing.inputCostPerMillion < 0 || pricing.outputCostPerMillion < 0) {
      throw new Error("Pricing values must be non-negative.");
    }

    this.pricing.set(model, pricing);
  }

  getPricing(model: string): ModelPricing | undefined {
    return this.pricing.get(model);
  }

  calculateCost(model: string, promptTokens: number, completionTokens: number) {
    const pricing = this.pricing.get(model);

    if (!pricing) {
      return {
        inputCostUsd: 0,
        outputCostUsd: 0,
        totalCostUsd: 0
      };
    }

    const inputCostUsd = (promptTokens / 1_000_000) * pricing.inputCostPerMillion;
    const outputCostUsd = (completionTokens / 1_000_000) * pricing.outputCostPerMillion;

    return {
      inputCostUsd,
      outputCostUsd,
      totalCostUsd: inputCostUsd + outputCostUsd
    };
  }
}
