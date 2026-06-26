// =============================================================================
// OrderSubmitted Domain Event — DDD Tactical Pattern
// =============================================================================
//
// Domain events represent something that happened in the domain.
// They are named in past tense and carry enough data for handlers
// to react without querying back to the source aggregate.
//
// Key rules:
// - Past tense name: OrderSubmitted, not SubmitOrder
// - Immutable — created once, never modified
// - Self-describing — handlers shouldn't need to query the DB
// - Collected by the aggregate during mutation
// - Published after the aggregate is persisted (not during mutation)
//
// Customize: Create events for significant state changes in your domain.
// =============================================================================

/**
 * Base class for all domain events.
 * Provides a timestamp and requires an event type identifier.
 */
export abstract class DomainEvent {
  /** When the event occurred. Set automatically at creation. */
  public readonly occurredAt: Date = new Date();

  /** Unique event type string for dispatching. */
  abstract readonly eventType: string;
}

/**
 * Raised when an order is submitted by a customer.
 *
 * Handlers might:
 * - Send a confirmation email (SendConfirmationHandler)
 * - Reserve inventory (UpdateInventoryHandler)
 * - Create an invoice (CreateInvoiceHandler)
 * - Notify the warehouse (NotifyWarehouseHandler)
 *
 * Each handler is independent — one handler's failure
 * should not prevent others from running.
 */
export class OrderSubmittedEvent extends DomainEvent {
  readonly eventType = "order.submitted";

  constructor(
    /** The order that was submitted. */
    public readonly orderId: string,
    /** The customer who submitted the order. */
    public readonly customerId: string,
    /** Total amount — handlers don't need to query the order. */
    public readonly totalAmount: number,
    /** Currency of the total amount. */
    public readonly currency: string,
    /** Number of items — useful for warehouse notification. */
    public readonly itemCount: number
  ) {
    super();
  }
}
