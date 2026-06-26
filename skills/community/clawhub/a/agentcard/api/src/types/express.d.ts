import type { PaymentContext, WalletContext } from "./http-context";

declare global {
  namespace Express {
    interface Request {
      paymentContext?: PaymentContext;
      walletContext?: WalletContext;
    }
  }
}

export {};
