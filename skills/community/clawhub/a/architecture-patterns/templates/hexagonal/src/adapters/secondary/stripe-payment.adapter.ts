// =============================================================================
// Stripe Payment Adapter — Hexagonal Architecture Secondary Adapter
// =============================================================================
//
// This is a SECONDARY (driven) adapter. It implements the PaymentGateway
// port using the Stripe SDK.
//
// The adapter translates between:
// - Domain vocabulary (ChargeRequest, ChargeResult) ← port types
// - Vendor vocabulary (Stripe.Charge, Stripe.ChargeCreateParams) ← SDK types
//
// Key rules:
// - Implements the port interface exactly
// - Translates vendor errors to domain errors
// - Contains NO business logic — only translation
// - Stripe SDK is imported HERE, never in domain or ports
//
// Customize: Replace with your payment provider's SDK.
// =============================================================================

import Stripe from "stripe";
import {
  PaymentGateway,
  ChargeRequest,
  ChargeResult,
  RefundRequest,
  RefundResult,
} from "../../ports/outbound/payment-gateway.port";

export class StripePaymentAdapter implements PaymentGateway {
  private readonly stripe: Stripe;

  constructor(apiKey: string) {
    this.stripe = new Stripe(apiKey);
  }

  async charge(request: ChargeRequest): Promise<ChargeResult> {
    try {
      // Translate domain request → Stripe API call
      const paymentIntent = await this.stripe.paymentIntents.create({
        amount: Math.round(request.amount * 100), // Stripe uses cents
        currency: request.currency.toLowerCase(),
        payment_method: request.paymentMethodId,
        confirm: true,
        automatic_payment_methods: {
          enabled: true,
          allow_redirects: "never",
        },
        metadata: {
          orderId: request.orderId,
        },
        description: request.description,
      });

      // Translate Stripe response → domain result
      return {
        paymentId: paymentIntent.id,
        status: paymentIntent.status === "succeeded" ? "succeeded" : "pending",
      };
    } catch (error) {
      // Translate Stripe errors → domain result (not Stripe exceptions)
      if (error instanceof Stripe.errors.StripeCardError) {
        return {
          paymentId: "",
          status: "failed",
          failureReason: error.message,
        };
      }

      // Unexpected Stripe errors become domain-level payment errors
      throw new PaymentProcessingError(
        `Payment processing failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  async refund(request: RefundRequest): Promise<RefundResult> {
    try {
      const refund = await this.stripe.refunds.create({
        payment_intent: request.paymentId,
        amount: Math.round(request.amount * 100),
        reason: request.reason as Stripe.RefundCreateParams.Reason,
      });

      return {
        refundId: refund.id,
        status: refund.status === "succeeded" ? "succeeded" : "pending",
      };
    } catch (error) {
      throw new PaymentProcessingError(
        `Refund processing failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
}

// ---------- Domain error (could live in domain/errors/) ----------

class PaymentProcessingError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "PaymentProcessingError";
  }
}
