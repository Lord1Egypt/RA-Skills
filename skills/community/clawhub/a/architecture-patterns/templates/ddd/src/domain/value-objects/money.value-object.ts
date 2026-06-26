// =============================================================================
// Money Value Object — DDD Tactical Pattern
// =============================================================================
//
// Value objects are immutable, identity-less, and validated on creation.
// Two Money instances with the same amount and currency are equal.
//
// Key rules:
// - Private constructor — creation only through static factory
// - Validation at creation — a Money instance is always valid
// - Immutable — all operations return NEW instances
// - Equality by value — compared by amount and currency, not by reference
//
// Customize: Adjust currencies, precision, and operations for your domain.
// =============================================================================

export class Money {
  // Private constructor forces creation through factory method
  private constructor(
    public readonly amount: number,
    public readonly currency: string
  ) {}

  // ---------- Factory ----------

  /** Create a Money value. Validates amount and currency. */
  static of(amount: number, currency: string): Money {
    if (!Number.isFinite(amount)) {
      throw new Error(`Money amount must be finite, got: ${amount}`);
    }
    if (amount < 0) {
      throw new Error(`Money amount must be non-negative, got: ${amount}`);
    }
    const allowed = ["USD", "EUR", "GBP"];
    if (!allowed.includes(currency)) {
      throw new Error(`Unsupported currency: ${currency}`);
    }
    // Round to 2 decimal places to avoid floating point issues
    return new Money(Math.round(amount * 100) / 100, currency);
  }

  /** Zero amount for a given currency. */
  static zero(currency: string): Money {
    return Money.of(0, currency);
  }

  // ---------- Arithmetic (returns new instances — immutable) ----------

  add(other: Money): Money {
    this.assertSameCurrency(other);
    return Money.of(this.amount + other.amount, this.currency);
  }

  subtract(other: Money): Money {
    this.assertSameCurrency(other);
    return Money.of(this.amount - other.amount, this.currency);
  }

  multiply(factor: number): Money {
    return Money.of(this.amount * factor, this.currency);
  }

  // ---------- Comparison ----------

  isGreaterThan(other: Money): boolean {
    this.assertSameCurrency(other);
    return this.amount > other.amount;
  }

  isZero(): boolean {
    return this.amount === 0;
  }

  // ---------- Equality (by value, not identity) ----------

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }

  // ---------- Conversion ----------

  /** Convert to cents/pence for payment APIs (e.g., Stripe). */
  toCents(): number {
    return Math.round(this.amount * 100);
  }

  toString(): string {
    return `${this.currency} ${this.amount.toFixed(2)}`;
  }

  // ---------- Internal ----------

  private assertSameCurrency(other: Money): void {
    if (this.currency !== other.currency) {
      throw new Error(
        `Cannot operate on different currencies: ${this.currency} vs ${other.currency}`
      );
    }
  }
}
