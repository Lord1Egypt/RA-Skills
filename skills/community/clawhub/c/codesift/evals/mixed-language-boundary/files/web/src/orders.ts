// Client for the orders API described in docs/api.md.

export interface Order {
  id: string;
  totalCents: number;
}

/** Fetch one order and return it typed for the order page. */
export async function fetchOrder(id: string): Promise<Order> {
  const response = await fetch(`/orders/${encodeURIComponent(id)}`);
  return (await response.json()) as Order;
}

/** Format an order total for display, for example "$12.34". */
export function formatTotal(order: Order): string {
  return `$${(order.totalCents / 100).toFixed(2)}`;
}
