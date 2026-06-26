// =============================================================================
// Order Service — Hexagonal Architecture Domain Layer
// =============================================================================
//
// This domain service implements the inbound (primary) port.
// It contains business logic and depends on outbound (secondary) ports
// for persistence and external services.
//
// The service knows WHAT to do. Adapters know HOW.
//
// Key rules:
// - Implements a primary port interface
// - Depends on secondary port interfaces (not implementations)
// - Contains business logic — no framework or infrastructure code
// - Dependencies injected through constructor
//
// Customize: Replace with your own domain service.
// =============================================================================

// Import port interfaces — the service depends on abstractions
// import { CreateOrderPort } from '../ports/inbound/create-order.port';
// import { OrderRepository } from '../ports/outbound/order-repository.port';
// import { PaymentGateway } from '../ports/outbound/payment-gateway.port';

// ---------- Port interfaces (inline for this example) ----------

interface OrderRepository {
  findById(id: string): Promise<Order | null>;
  save(order: Order): Promise<void>;
}

interface PaymentGateway {
  charge(request: ChargeRequest): Promise<ChargeResult>;
}

interface ChargeRequest {
  orderId: string;
  amount: number;
  currency: string;
  paymentMethodId: string;
}

interface ChargeResult {
  paymentId: string;
  status: "succeeded" | "failed";
}

// ---------- Domain entity (simplified) ----------

interface OrderItem {
  productId: string;
  quantity: number;
  unitPrice: number;
}

class Order {
  constructor(
    public readonly id: string,
    public readonly customerId: string,
    private _items: OrderItem[],
    private _status: "draft" | "submitted" | "paid" | "cancelled"
  ) {}

  static create(customerId: string, items: OrderItem[]): Order {
    if (items.length === 0) {
      throw new Error("Order must have at least one item");
    }
    return new Order(crypto.randomUUID(), customerId, items, "draft");
  }

  get total(): number {
    return this._items.reduce((sum, item) => sum + item.unitPrice * item.quantity, 0);
  }

  get status(): string {
    return this._status;
  }

  get items(): ReadonlyArray<OrderItem> {
    return [...this._items];
  }

  submit(): void {
    if (this._status !== "draft") {
      throw new Error(`Cannot submit order in status: ${this._status}`);
    }
    this._status = "submitted";
  }

  markPaid(): void {
    if (this._status !== "submitted") {
      throw new Error(`Cannot mark as paid in status: ${this._status}`);
    }
    this._status = "paid";
  }
}

// ---------- Domain service ----------

export class OrderService {
  constructor(
    private readonly orderRepository: OrderRepository,
    private readonly paymentGateway: PaymentGateway
  ) {}

  /**
   * Create and submit an order, then process payment.
   *
   * This method orchestrates domain logic:
   * 1. Creates the order entity (entity validates itself)
   * 2. Submits the order (entity enforces valid transition)
   * 3. Charges payment through the gateway port
   * 4. Persists the result through the repository port
   */
  async createAndPayOrder(
    customerId: string,
    items: OrderItem[],
    paymentMethodId: string
  ): Promise<{ orderId: string; paymentId: string }> {
    // Domain entity handles its own validation
    const order = Order.create(customerId, items);
    order.submit();

    // Charge through the payment gateway port
    // The actual payment processor (Stripe, PayPal) is an adapter concern
    const chargeResult = await this.paymentGateway.charge({
      orderId: order.id,
      amount: order.total,
      currency: "USD",
      paymentMethodId,
    });

    if (chargeResult.status === "failed") {
      throw new Error(`Payment failed for order ${order.id}`);
    }

    order.markPaid();

    // Persist through the repository port
    // The actual database (Postgres, MongoDB) is an adapter concern
    await this.orderRepository.save(order);

    return {
      orderId: order.id,
      paymentId: chargeResult.paymentId,
    };
  }
}
