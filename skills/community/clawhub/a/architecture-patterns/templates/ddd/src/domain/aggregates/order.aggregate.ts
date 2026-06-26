// =============================================================================
// Order Aggregate — DDD Tactical Pattern
// =============================================================================
//
// The aggregate root is the entry point for all modifications. External code
// NEVER reaches into child entities (OrderItem) directly.
//
// Key rules:
// - All changes go through the aggregate root's public methods
// - The root enforces invariants across its children
// - Child entities are exposed as readonly (no external mutation)
// - Domain events are collected during operations, published after persistence
// - Other aggregates are referenced by ID, not by object
//
// Customize: Replace with your own aggregate. Follow the same structure.
// =============================================================================

import { Money } from "../value-objects/money.value-object";

// ---------- Domain event base ----------

abstract class DomainEvent {
  public readonly occurredAt: Date = new Date();
  abstract readonly eventType: string;
}

// ---------- Child entity (managed by the aggregate) ----------

class OrderItem {
  constructor(
    public readonly productId: string,
    private _quantity: number,
    private _unitPrice: Money
  ) {
    if (_quantity < 1) {
      throw new Error("Quantity must be at least 1");
    }
  }

  get quantity(): number {
    return this._quantity;
  }

  get lineTotal(): Money {
    return this._unitPrice.multiply(this._quantity);
  }

  /** Only callable within the aggregate — not exposed externally. */
  updateQuantity(newQuantity: number): void {
    if (newQuantity < 1) {
      throw new Error("Quantity must be at least 1");
    }
    this._quantity = newQuantity;
  }
}

// ---------- Aggregate root ----------

type OrderStatus = "draft" | "submitted" | "cancelled";

export class Order {
  private _domainEvents: DomainEvent[] = [];

  private constructor(
    public readonly id: string,
    private readonly _customerId: string,  // ID reference to Customer aggregate
    private _items: OrderItem[],
    private _status: OrderStatus,
    private _submittedAt: Date | null
  ) {}

  // ---------- Factory methods ----------

  /** Create a new draft order. */
  static create(customerId: string): Order {
    return new Order(crypto.randomUUID(), customerId, [], "draft", null);
  }

  /** Reconstitute from persistence (used by repository mapper). */
  static reconstitute(props: {
    id: string;
    customerId: string;
    items: Array<{ productId: string; quantity: number; unitPrice: Money }>;
    status: OrderStatus;
    submittedAt: Date | null;
  }): Order {
    const items = props.items.map(
      (i) => new OrderItem(i.productId, i.quantity, i.unitPrice)
    );
    return new Order(props.id, props.customerId, items, props.status, props.submittedAt);
  }

  // ---------- Getters (readonly access to internals) ----------

  get customerId(): string {
    return this._customerId;
  }

  get status(): OrderStatus {
    return this._status;
  }

  get submittedAt(): Date | null {
    return this._submittedAt;
  }

  /** Items exposed as readonly — external code cannot mutate them. */
  get items(): ReadonlyArray<{ productId: string; quantity: number; lineTotal: Money }> {
    return this._items.map((item) => ({
      productId: item.productId,
      quantity: item.quantity,
      lineTotal: item.lineTotal,
    }));
  }

  /** Calculate total across all items — aggregate-level invariant. */
  get total(): Money {
    if (this._items.length === 0) {
      return Money.zero("USD");
    }
    return this._items.reduce(
      (sum, item) => sum.add(item.lineTotal),
      Money.zero("USD")
    );
  }

  // ---------- Domain events ----------

  get domainEvents(): ReadonlyArray<DomainEvent> {
    return [...this._domainEvents];
  }

  clearEvents(): void {
    this._domainEvents = [];
  }

  // ---------- Business behavior (all changes through the root) ----------

  /** Add an item to the order. Only allowed in draft status. */
  addItem(productId: string, quantity: number, unitPrice: Money): void {
    this.assertDraft("add items");

    // Check if product already in order — aggregate enforces uniqueness
    const existing = this._items.find((i) => i.productId === productId);
    if (existing) {
      existing.updateQuantity(existing.quantity + quantity);
    } else {
      this._items.push(new OrderItem(productId, quantity, unitPrice));
    }
  }

  /** Remove an item from the order. Only allowed in draft status. */
  removeItem(productId: string): void {
    this.assertDraft("remove items");

    const index = this._items.findIndex((i) => i.productId === productId);
    if (index === -1) {
      throw new Error(`Product ${productId} not found in order ${this.id}`);
    }
    this._items.splice(index, 1);
  }

  /** Submit the order. Enforces non-empty invariant. Raises domain event. */
  submit(): void {
    this.assertDraft("submit");

    if (this._items.length === 0) {
      throw new Error(`Cannot submit empty order ${this.id}`);
    }

    // State transition
    this._status = "submitted";
    this._submittedAt = new Date();

    // Collect domain event — published after persistence
    this._domainEvents.push(
      new OrderSubmittedEvent(this.id, this._customerId, this.total)
    );
  }

  /** Cancel the order. Only draft and submitted orders can be cancelled. */
  cancel(reason: string): void {
    if (this._status === "cancelled") {
      throw new Error(`Order ${this.id} is already cancelled`);
    }

    this._status = "cancelled";

    this._domainEvents.push(
      new OrderCancelledEvent(this.id, this._customerId, reason)
    );
  }

  // ---------- Internal invariant enforcement ----------

  private assertDraft(action: string): void {
    if (this._status !== "draft") {
      throw new Error(`Cannot ${action} on order ${this.id} in status: ${this._status}`);
    }
  }
}

// ---------- Domain events (past tense — something that happened) ----------

class OrderSubmittedEvent extends DomainEvent {
  readonly eventType = "order.submitted";

  constructor(
    public readonly orderId: string,
    public readonly customerId: string,
    public readonly totalAmount: Money
  ) {
    super();
  }
}

class OrderCancelledEvent extends DomainEvent {
  readonly eventType = "order.cancelled";

  constructor(
    public readonly orderId: string,
    public readonly customerId: string,
    public readonly reason: string
  ) {
    super();
  }
}
