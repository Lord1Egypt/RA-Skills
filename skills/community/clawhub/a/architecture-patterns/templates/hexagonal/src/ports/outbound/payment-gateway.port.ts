// =============================================================================
// Payment Gateway Port — Hexagonal Architecture Outbound Port
// =============================================================================
//
// This is a SECONDARY (outbound/driven) port. It defines what the domain
// needs from a payment processor, using domain vocabulary.
//
// The interface knows nothing about Stripe, PayPal, or any specific vendor.
// Adapters in adapters/secondary/ implement this interface with vendor SDKs.
//
// Key rules:
// - Uses domain types (Money, OrderId), not vendor types
// - Defines operations the domain needs, not what the vendor offers
// - Error handling uses domain errors, not vendor exceptions
//
// Customize: Adapt the interface to your payment requirements.
// =============================================================================

export interface ChargeRequest {
  orderId: string;
  amount: number;
  currency: string;
  paymentMethodId: string;
  description?: string;
}

export interface ChargeResult {
  paymentId: string;
  status: "succeeded" | "failed" | "pending";
  failureReason?: string;
}

export interface RefundRequest {
  paymentId: string;
  amount: number;
  reason?: string;
}

export interface RefundResult {
  refundId: string;
  status: "succeeded" | "failed" | "pending";
}

/**
 * Payment gateway port — defines what the domain needs from payment processing.
 *
 * Implementations:
 * - StripePaymentAdapter (production)
 * - FakePaymentGateway (testing — always succeeds)
 * - FailingPaymentGateway (testing — always fails)
 */
export interface PaymentGateway {
  /** Charge a payment method for an order. */
  charge(request: ChargeRequest): Promise<ChargeResult>;

  /** Refund a previous charge (partial or full). */
  refund(request: RefundRequest): Promise<RefundResult>;
}
