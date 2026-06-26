# DDD Tactical Patterns

Value objects, entities, aggregates, repositories, domain events, and domain services implemented in TypeScript. These are the building blocks of a domain-driven design.

---

## Value Objects

Value objects represent descriptive, immutable concepts with no identity. Two value objects with the same attributes are considered equal.

### Pattern 1: Immutable Value Object

Value objects are created with validation and cannot be modified. Operations return new instances.

❌ **Bad: Mutable plain object used as currency amount**

```typescript
// No validation, mutable, no behavior
interface Money {
  amount: number;
  currency: string;
}

function createPayment(money: Money) {
  money.amount = money.amount * 1.1; // Mutated — caller affected
  // No guarantee amount is positive or currency is valid
}
```

✅ **Good: Immutable value object with validation**

```typescript
class Money {
  private constructor(
    public readonly amount: number,
    public readonly currency: string
  ) {}

  static of(amount: number, currency: string): Money {
    if (!Number.isFinite(amount)) {
      throw new InvalidMoneyError(`Amount must be finite: ${amount}`);
    }
    if (amount < 0) {
      throw new InvalidMoneyError(`Amount must be non-negative: ${amount}`);
    }
    const validCurrencies = ["USD", "EUR", "GBP", "JPY"];
    if (!validCurrencies.includes(currency)) {
      throw new InvalidMoneyError(`Invalid currency: ${currency}`);
    }
    return new Money(amount, currency);
  }

  add(other: Money): Money {
    this.assertSameCurrency(other);
    return Money.of(this.amount + other.amount, this.currency);
  }

  subtract(other: Money): Money {
    this.assertSameCurrency(other);
    if (this.amount < other.amount) {
      throw new InsufficientFundsError(this, other);
    }
    return Money.of(this.amount - other.amount, this.currency);
  }

  multiply(factor: number): Money {
    return Money.of(Math.round(this.amount * factor * 100) / 100, this.currency);
  }

  isGreaterThan(other: Money): boolean {
    this.assertSameCurrency(other);
    return this.amount > other.amount;
  }

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }

  toCents(): number {
    return Math.round(this.amount * 100);
  }

  toString(): string {
    return `${this.currency} ${this.amount.toFixed(2)}`;
  }

  private assertSameCurrency(other: Money): void {
    if (this.currency !== other.currency) {
      throw new CurrencyMismatchError(this.currency, other.currency);
    }
  }
}
```

**Rule:** Value objects are immutable. All operations return new instances. Validation happens at creation — a value object is always valid by construction.

---

### Pattern 2: Value Object with Behavior

Value objects encapsulate domain logic related to the concept they represent.

```typescript
class DateRange {
  private constructor(
    public readonly start: Date,
    public readonly end: Date
  ) {}

  static create(start: Date, end: Date): DateRange {
    if (end <= start) {
      throw new InvalidDateRangeError("End must be after start");
    }
    return new DateRange(start, end);
  }

  contains(date: Date): boolean {
    return date >= this.start && date <= this.end;
  }

  overlaps(other: DateRange): boolean {
    return this.start < other.end && this.end > other.start;
  }

  get durationInDays(): number {
    const ms = this.end.getTime() - this.start.getTime();
    return Math.ceil(ms / (1000 * 60 * 60 * 24));
  }

  extend(days: number): DateRange {
    const newEnd = new Date(this.end);
    newEnd.setDate(newEnd.getDate() + days);
    return DateRange.create(this.start, newEnd);
  }

  equals(other: DateRange): boolean {
    return (
      this.start.getTime() === other.start.getTime() &&
      this.end.getTime() === other.end.getTime()
    );
  }
}
```

**Rule:** Value objects are not just data containers. They encapsulate logic that belongs to the concept — date ranges know about overlap, money knows about arithmetic, addresses know about formatting.

---

### Pattern 3: Replacing Primitives

Replace primitive types with value objects when the primitive has validation rules, formatting, or risk of being confused with other values of the same type.

❌ **Bad: Primitive types everywhere — easy to mix up**

```typescript
class OrderService {
  async createOrder(
    userId: string,      // Which string is which?
    productId: string,   // Easy to swap arguments
    quantity: number,     // Could be negative
    price: number         // Could be NaN
  ): Promise<string> {   // What does the return string represent?
    // ...
  }
}

// Bug: arguments swapped — compiles fine, fails at runtime
orderService.createOrder(productId, userId, price, quantity);
```

✅ **Good: Value objects prevent mix-ups at compile time**

```typescript
class UserId {
  private constructor(private readonly value: string) {}
  static from(value: string): UserId {
    if (!value || value.trim().length === 0) throw new Error("Invalid user ID");
    return new UserId(value);
  }
  equals(other: UserId): boolean { return this.value === other.value; }
  toString(): string { return this.value; }
}

class ProductId {
  private constructor(private readonly value: string) {}
  static from(value: string): ProductId {
    if (!value) throw new Error("Invalid product ID");
    return new ProductId(value);
  }
  equals(other: ProductId): boolean { return this.value === other.value; }
  toString(): string { return this.value; }
}

class Quantity {
  private constructor(public readonly value: number) {}
  static of(value: number): Quantity {
    if (!Number.isInteger(value) || value < 1) {
      throw new Error("Quantity must be a positive integer");
    }
    return new Quantity(value);
  }
}

class OrderService {
  async createOrder(
    userId: UserId,
    productId: ProductId,
    quantity: Quantity,
    price: Money
  ): Promise<OrderId> {
    // Arguments can't be swapped — types prevent it
  }
}
```

**Rule:** Replace primitives with value objects when: (1) the value has validation rules, (2) values of the same type could be confused, or (3) the value has operations or formatting.

---

## Entities

Entities are objects defined by their identity, not their attributes. An entity can change over time but remains the same entity.

### Pattern 4: Entity with Identity

Entities are compared by ID. Two entities with the same ID are the same entity, regardless of their other attributes.

❌ **Bad: No clear identity, compared by attributes**

```typescript
class Customer {
  name: string;
  email: string;

  isSameAs(other: Customer): boolean {
    // Attribute comparison — what if name changes?
    return this.name === other.name && this.email === other.email;
  }
}
```

✅ **Good: Identity-based equality**

```typescript
class Customer {
  constructor(
    public readonly id: CustomerId,
    private _name: string,
    private _email: Email
  ) {}

  // Entities are equal when their IDs match
  equals(other: Customer): boolean {
    return this.id.equals(other.id);
  }

  // Name can change — entity identity is unchanged
  changeName(newName: string): void {
    if (!newName || newName.trim().length === 0) {
      throw new InvalidNameError("Name cannot be empty");
    }
    this._name = newName.trim();
  }

  get name(): string { return this._name; }
  get email(): Email { return this._email; }
}
```

**Rule:** Entity equality is always by ID. Attributes are mutable but identity is permanent. If two objects could have identical attributes but represent different things, they're entities.

---

### Pattern 5: Rich Entity (Anti-Anemic)

Entities encapsulate their behavior. Business rules that govern an entity's state live inside the entity, not in external services.

❌ **Bad: Anemic entity — all logic in services**

```typescript
class Order {
  id: string;
  items: OrderItem[];
  status: string;
  total: number;
}

class OrderService {
  addItem(order: Order, item: OrderItem): void {
    if (order.status !== "draft") throw new Error("Cannot modify");
    order.items.push(item);
    order.total = order.items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  }

  submit(order: Order): void {
    if (order.items.length === 0) throw new Error("Empty order");
    if (order.status !== "draft") throw new Error("Already submitted");
    order.status = "submitted";
  }

  cancel(order: Order): void {
    if (order.status === "shipped") throw new Error("Already shipped");
    order.status = "cancelled";
  }
}
```

✅ **Good: Entity with encapsulated behavior**

```typescript
class Order {
  private constructor(
    public readonly id: OrderId,
    private _items: OrderItem[],
    private _status: OrderStatus,
    private _submittedAt: Date | null
  ) {}

  static create(): Order {
    return new Order(OrderId.generate(), [], OrderStatus.Draft, null);
  }

  addItem(product: Product, quantity: Quantity): void {
    if (!this._status.isDraft()) {
      throw new OrderAlreadySubmittedError(this.id);
    }
    const existingItem = this._items.find((i) => i.productId.equals(product.id));
    if (existingItem) {
      existingItem.increaseQuantity(quantity);
    } else {
      this._items.push(OrderItem.create(product, quantity));
    }
  }

  removeItem(productId: ProductId): void {
    if (!this._status.isDraft()) {
      throw new OrderAlreadySubmittedError(this.id);
    }
    this._items = this._items.filter((i) => !i.productId.equals(productId));
  }

  submit(): void {
    if (this._items.length === 0) {
      throw new EmptyOrderError(this.id);
    }
    if (!this._status.isDraft()) {
      throw new OrderAlreadySubmittedError(this.id);
    }
    this._status = OrderStatus.Submitted;
    this._submittedAt = new Date();
  }

  cancel(): void {
    if (this._status.isShipped()) {
      throw new CannotCancelShippedOrderError(this.id);
    }
    this._status = OrderStatus.Cancelled;
  }

  get total(): Money {
    return this._items.reduce(
      (sum, item) => sum.add(item.lineTotal),
      Money.of(0, "USD")
    );
  }

  get status(): OrderStatus { return this._status; }
  get items(): ReadonlyArray<OrderItem> { return [...this._items]; }
}
```

**Rule:** Ask "who should know this rule?" If the rule is about an entity's own state, it belongs in the entity. Services that just get data, make decisions, and set data back are a sign of an anemic model.

---

### Pattern 6: Entity State Transitions

Model valid state transitions explicitly. The entity enforces which transitions are allowed.

❌ **Bad: Status set directly from outside**

```typescript
class Task {
  status: "todo" | "in_progress" | "done" | "archived";

  setStatus(status: string): void {
    this.status = status; // Any transition allowed — todo → archived? done → todo?
  }
}
```

✅ **Good: Explicit state machine**

```typescript
class TaskStatus {
  private constructor(private readonly value: string) {}

  static readonly Todo = new TaskStatus("todo");
  static readonly InProgress = new TaskStatus("in_progress");
  static readonly Done = new TaskStatus("done");
  static readonly Archived = new TaskStatus("archived");

  private static readonly validTransitions: Record<string, string[]> = {
    todo: ["in_progress"],
    in_progress: ["done", "todo"],
    done: ["archived"],
    archived: [],
  };

  canTransitionTo(target: TaskStatus): boolean {
    return TaskStatus.validTransitions[this.value]?.includes(target.value) ?? false;
  }

  toString(): string { return this.value; }
}

class Task {
  constructor(
    public readonly id: TaskId,
    private _title: string,
    private _status: TaskStatus
  ) {}

  start(): void {
    this.transitionTo(TaskStatus.InProgress);
  }

  complete(): void {
    this.transitionTo(TaskStatus.Done);
  }

  archive(): void {
    this.transitionTo(TaskStatus.Archived);
  }

  private transitionTo(newStatus: TaskStatus): void {
    if (!this._status.canTransitionTo(newStatus)) {
      throw new InvalidTransitionError(this._status, newStatus);
    }
    this._status = newStatus;
  }

  get status(): TaskStatus { return this._status; }
}
```

**Rule:** Don't expose a generic `setStatus()`. Provide named methods for each transition (`start()`, `complete()`, `archive()`). The entity enforces which transitions are valid.

---

## Aggregates

Aggregates are clusters of entities and value objects treated as a single unit for data changes. The aggregate root is the entry point — all external access goes through it.

### Pattern 7: Aggregate Root

All modifications to an aggregate's internals go through the aggregate root. External code never reaches into child entities directly.

❌ **Bad: External code reaching into aggregate internals**

```typescript
// External code modifying an order's item directly
const order = await orderRepo.findById(orderId);
const item = order.items[0];
item.quantity = 5;         // Direct mutation of internal state
item.price = newPrice;     // Bypasses aggregate invariant checks
await orderRepo.save(order);
```

✅ **Good: All changes through the aggregate root**

```typescript
class Order {
  private _items: OrderItem[];

  // External code uses this method — never touches items directly
  updateItemQuantity(productId: ProductId, newQuantity: Quantity): void {
    if (!this._status.isDraft()) {
      throw new OrderAlreadySubmittedError(this.id);
    }

    const item = this._items.find((i) => i.productId.equals(productId));
    if (!item) {
      throw new ItemNotInOrderError(this.id, productId);
    }

    item.updateQuantity(newQuantity); // Internal mutation is OK within aggregate
    this.recalculateTotal();          // Aggregate maintains its invariants
  }

  // Items exposed as readonly to prevent external mutation
  get items(): ReadonlyArray<OrderItem> {
    return [...this._items];
  }
}
```

**Rule:** External code calls methods on the aggregate root. The root coordinates changes to its internals and maintains invariants. Never expose mutable references to child entities.

---

### Pattern 8: Aggregate Boundaries

Aggregates reference other aggregates by ID, not by direct object reference. Keep aggregates small and focused.

❌ **Bad: Giant aggregate containing everything**

```typescript
class Customer {
  id: CustomerId;
  name: string;
  orders: Order[];           // All orders loaded every time
  addresses: Address[];      // All addresses loaded too
  paymentMethods: PaymentMethod[];

  // Loading a customer loads all their orders, addresses, payments...
  // Can't load one order without loading the entire customer
}
```

✅ **Good: Small aggregates with ID references**

```typescript
class Customer {
  constructor(
    public readonly id: CustomerId,
    private _name: string,
    private _email: Email,
    private _defaultAddressId: AddressId | null
  ) {}
  // Customer is small — just identity and contact info
}

class Order {
  constructor(
    public readonly id: OrderId,
    private _customerId: CustomerId,    // ID reference, not object
    private _shippingAddressId: AddressId, // ID reference
    private _items: OrderItem[],
    private _status: OrderStatus
  ) {}
  // Order is its own aggregate — loaded independently
}

class Address {
  constructor(
    public readonly id: AddressId,
    private _customerId: CustomerId,   // ID reference back
    private _street: string,
    private _city: string,
    private _country: Country
  ) {}
}
```

**Rule:** Reference other aggregates by ID, not by object. Each aggregate is loaded independently. If you need data from another aggregate, query its repository.

---

### Pattern 9: Aggregate Invariants

Aggregates enforce business rules (invariants) that span multiple objects within the aggregate boundary.

```typescript
class ShoppingCart {
  private readonly MAX_ITEMS = 50;
  private readonly MAX_QUANTITY_PER_ITEM = 10;

  constructor(
    public readonly id: CartId,
    private _customerId: CustomerId,
    private _items: CartItem[]
  ) {}

  addItem(productId: ProductId, quantity: Quantity, price: Money): void {
    // Invariant: max items in cart
    if (this._items.length >= this.MAX_ITEMS) {
      throw new CartFullError(this.id, this.MAX_ITEMS);
    }

    const existing = this._items.find((i) => i.productId.equals(productId));

    if (existing) {
      const newQuantity = existing.quantity.value + quantity.value;
      // Invariant: max quantity per item
      if (newQuantity > this.MAX_QUANTITY_PER_ITEM) {
        throw new MaxQuantityExceededError(productId, this.MAX_QUANTITY_PER_ITEM);
      }
      existing.updateQuantity(Quantity.of(newQuantity));
    } else {
      this._items.push(CartItem.create(productId, quantity, price));
    }
  }

  // Invariant: cart total (cross-item rule)
  get total(): Money {
    return this._items.reduce(
      (sum, item) => sum.add(item.lineTotal),
      Money.of(0, "USD")
    );
  }
}
```

**Rule:** Invariants that span multiple entities belong in the aggregate root. If a rule only involves one entity, put it in that entity. If it spans entities in different aggregates, use a domain service.

---

### Pattern 10: Aggregate Sizing

Start with small aggregates. Split when you see performance issues, concurrency conflicts, or unrelated concerns bundled together.

❌ **Bad: One aggregate for everything product-related**

```typescript
class Product {
  id: ProductId;
  name: string;
  description: string;
  price: Money;
  inventory: InventoryItem[];  // Stock levels — changes very frequently
  reviews: Review[];           // User reviews — grows unbounded
  images: ProductImage[];      // Rarely changes
  categories: Category[];      // Rarely changes

  // Loading a product loads ALL reviews and inventory
  // Updating inventory locks the entire product aggregate
}
```

✅ **Good: Separate aggregates for separate concerns**

```typescript
// Product aggregate — catalog information
class Product {
  constructor(
    public readonly id: ProductId,
    private _name: string,
    private _description: string,
    private _price: Money,
    private _categoryIds: CategoryId[]
  ) {}
}

// Inventory aggregate — stock levels (changes frequently)
class Inventory {
  constructor(
    public readonly id: InventoryId,
    private _productId: ProductId,   // ID reference
    private _quantity: number,
    private _reservedQuantity: number
  ) {}

  reserve(quantity: number): void {
    if (this.availableQuantity < quantity) {
      throw new InsufficientStockError(this._productId, quantity);
    }
    this._reservedQuantity += quantity;
  }

  get availableQuantity(): number {
    return this._quantity - this._reservedQuantity;
  }
}

// Review aggregate — user content (grows unbounded)
class ProductReview {
  constructor(
    public readonly id: ReviewId,
    private _productId: ProductId,   // ID reference
    private _customerId: CustomerId,
    private _rating: Rating,
    private _content: string
  ) {}
}
```

**Rule:** Split aggregates when: (1) different parts change at different rates, (2) loading the whole aggregate is expensive, (3) concurrent updates cause conflicts, or (4) parts have unrelated business rules.

---

## Repositories

Repositories provide an interface for loading and saving aggregates. They abstract the persistence mechanism from the domain.

### Pattern 11: Repository Contract

Repository interfaces live in the domain layer. They define operations using domain types.

```typescript
// Domain layer — defines the contract
interface OrderRepository {
  findById(id: OrderId): Promise<Order | null>;
  findByCustomer(customerId: CustomerId): Promise<Order[]>;
  findPendingOrders(): Promise<Order[]>;
  save(order: Order): Promise<void>;
  delete(id: OrderId): Promise<void>;
  nextId(): OrderId;
}
```

**Rule:** Repository interfaces use domain types (OrderId, not string). They return domain aggregates (Order, not a database row). The interface knows nothing about SQL, MongoDB, or any persistence technology.

---

### Pattern 12: Repository for Aggregates Only

Repositories exist for aggregate roots only. Child entities and value objects are saved through their parent aggregate.

❌ **Bad: Repository for every entity**

```typescript
// Separate repositories for aggregate root and its children
interface OrderRepository { save(order: Order): Promise<void>; }
interface OrderItemRepository { save(item: OrderItem): Promise<void>; }
interface ShippingInfoRepository { save(info: ShippingInfo): Promise<void>; }

// External code saves parts independently — aggregate invariants bypassed
await orderItemRepo.save(newItem);  // No aggregate validation
```

✅ **Good: Repository for aggregate root only**

```typescript
interface OrderRepository {
  findById(id: OrderId): Promise<Order | null>;
  save(order: Order): Promise<void>;
  // Saves the entire aggregate: order + items + shipping info
}

// The repository implementation handles child entities internally
class PrismaOrderRepository implements OrderRepository {
  async save(order: Order): Promise<void> {
    await this.prisma.$transaction(async (tx) => {
      // Save the aggregate root
      await tx.order.upsert({ where: { id: order.id.toString() }, /* ... */ });

      // Save child entities as part of the same transaction
      await tx.orderItem.deleteMany({ where: { orderId: order.id.toString() } });
      await tx.orderItem.createMany({
        data: order.items.map((item) => this.toItemPersistence(item, order.id)),
      });
    });
  }
}
```

**Rule:** One repository per aggregate root. Child entities are persisted through the aggregate's repository. This ensures the aggregate is always saved as a consistent whole.

---

### Pattern 13: Specification Pattern

Encapsulate complex query criteria as domain objects. This keeps query logic testable and composable.

```typescript
// Specification interface
interface Specification<T> {
  isSatisfiedBy(entity: T): boolean;
}

// Concrete specifications
class OverdueOrderSpec implements Specification<Order> {
  constructor(private readonly asOf: Date) {}

  isSatisfiedBy(order: Order): boolean {
    return (
      order.status.isPending() &&
      order.createdAt < new Date(this.asOf.getTime() - 7 * 24 * 60 * 60 * 1000)
    );
  }
}

class HighValueOrderSpec implements Specification<Order> {
  constructor(private readonly threshold: Money) {}

  isSatisfiedBy(order: Order): boolean {
    return order.total.isGreaterThan(this.threshold);
  }
}

// Repository supports specifications
interface OrderRepository {
  findMatching(spec: Specification<Order>): Promise<Order[]>;
}

// Usage
const overdueHighValue = new AndSpecification(
  new OverdueOrderSpec(new Date()),
  new HighValueOrderSpec(Money.of(1000, "USD"))
);
const orders = await orderRepo.findMatching(overdueHighValue);
```

**Rule:** Use specifications when query criteria are complex, reusable, or need to be testable in isolation. For simple queries, named repository methods (`findPendingOrders()`) are sufficient.

---

## Domain Events

Domain events capture something that happened in the domain. They enable loose coupling between aggregates and bounded contexts.

### Pattern 14: Raising Events

Aggregates collect events during their operations. Events are published after the aggregate is persisted, not during mutation.

❌ **Bad: Publishing events during entity mutation**

```typescript
class Order {
  constructor(private eventBus: EventBus) {}  // Domain depends on infrastructure

  submit(): void {
    this._status = OrderStatus.Submitted;
    // What if save fails? Event already published!
    this.eventBus.publish(new OrderSubmittedEvent(this.id));
  }
}
```

✅ **Good: Collecting events, publishing after persistence**

```typescript
class Order {
  private _domainEvents: DomainEvent[] = [];

  submit(): void {
    if (this._items.length === 0) throw new EmptyOrderError(this.id);
    this._status = OrderStatus.Submitted;
    this._submittedAt = new Date();

    // Event collected — not yet published
    this._domainEvents.push(
      new OrderSubmittedEvent(this.id, this._customerId, this.total)
    );
  }

  get domainEvents(): ReadonlyArray<DomainEvent> {
    return [...this._domainEvents];
  }

  clearEvents(): void {
    this._domainEvents = [];
  }
}

// Repository publishes events after successful save
class OrderRepositoryImpl implements OrderRepository {
  constructor(
    private prisma: PrismaClient,
    private eventBus: EventBus
  ) {}

  async save(order: Order): Promise<void> {
    await this.prisma.order.upsert(/* ... */);

    // Events published only after successful persistence
    for (const event of order.domainEvents) {
      await this.eventBus.publish(event);
    }
    order.clearEvents();
  }
}
```

**Rule:** Aggregates collect events. Events are published after the aggregate is persisted. This guarantees no events for failed operations.

---

### Pattern 15: Event Structure

Domain events are named in past tense — they describe something that already happened. They carry enough data for handlers to react without querying back.

❌ **Bad: Vague event with minimal data**

```typescript
class OrderEvent {
  type: string;       // "order_change" — what changed?
  orderId: string;
  timestamp: Date;
  // Handler must query the database to understand what happened
}
```

✅ **Good: Specific, self-describing event**

```typescript
abstract class DomainEvent {
  public readonly occurredAt: Date = new Date();
  abstract readonly eventType: string;
}

class OrderSubmittedEvent extends DomainEvent {
  readonly eventType = "order.submitted";

  constructor(
    public readonly orderId: OrderId,
    public readonly customerId: CustomerId,
    public readonly totalAmount: Money,
    public readonly itemCount: number
  ) {
    super();
  }
}

class OrderCancelledEvent extends DomainEvent {
  readonly eventType = "order.cancelled";

  constructor(
    public readonly orderId: OrderId,
    public readonly customerId: CustomerId,
    public readonly reason: string
  ) {
    super();
  }
}

class PaymentReceivedEvent extends DomainEvent {
  readonly eventType = "payment.received";

  constructor(
    public readonly paymentId: PaymentId,
    public readonly orderId: OrderId,
    public readonly amount: Money,
    public readonly method: string
  ) {
    super();
  }
}
```

**Rule:** Event names are past tense (`OrderSubmitted`, not `SubmitOrder`). Events carry relevant IDs and key data. Handlers should not need to query the database to understand the event.

---

### Pattern 16: Event Handlers

Event handlers react to domain events. They run after the originating transaction completes, enabling eventual consistency between aggregates.

❌ **Bad: Synchronous handler doing writes in same transaction**

```typescript
class OrderSubmittedHandler {
  handle(event: OrderSubmittedEvent): void {
    // Runs synchronously in the same transaction as order save
    // If this fails, the order save is rolled back — tight coupling
    const invoice = Invoice.createFrom(event.orderId, event.totalAmount);
    this.invoiceRepo.save(invoice);  // Same transaction
    this.emailService.send(event.customerId, "Order confirmed");  // Blocking
  }
}
```

✅ **Good: Asynchronous handlers with eventual consistency**

```typescript
class SendOrderConfirmationHandler {
  constructor(private emailNotifier: EmailNotifier) {}

  async handle(event: OrderSubmittedEvent): Promise<void> {
    await this.emailNotifier.sendOrderConfirmation(
      event.customerId,
      event.orderId,
      event.totalAmount
    );
  }
}

class CreateInvoiceHandler {
  constructor(private invoiceRepo: InvoiceRepository) {}

  async handle(event: OrderSubmittedEvent): Promise<void> {
    const invoice = Invoice.createFor(event.orderId, event.totalAmount);
    await this.invoiceRepo.save(invoice);
  }
}

class UpdateInventoryHandler {
  constructor(private inventoryService: InventoryService) {}

  async handle(event: OrderSubmittedEvent): Promise<void> {
    await this.inventoryService.reserveStock(event.orderId);
  }
}

// Event dispatcher — wires events to handlers
class EventDispatcher {
  private handlers = new Map<string, DomainEventHandler[]>();

  register(eventType: string, handler: DomainEventHandler): void {
    const existing = this.handlers.get(eventType) ?? [];
    existing.push(handler);
    this.handlers.set(eventType, existing);
  }

  async dispatch(event: DomainEvent): Promise<void> {
    const handlers = this.handlers.get(event.eventType) ?? [];
    await Promise.allSettled(
      handlers.map((h) => h.handle(event))
    );
  }
}
```

**Rule:** Event handlers run after the originating aggregate is persisted. Each handler is independent — one handler's failure should not prevent others from running. Use `Promise.allSettled` for parallel handler execution.

---

## Domain Services

Domain services contain business logic that doesn't belong to a single entity or value object. They coordinate operations across multiple aggregates.

### Pattern 17: When to Use Domain Services

Use a domain service when business logic spans multiple aggregates and cannot be placed in either one.

❌ **Bad: Forcing cross-aggregate logic into one entity**

```typescript
class Order {
  // Order shouldn't know about inventory or pricing rules
  submit(inventory: Inventory, pricingRules: PricingRules): void {
    for (const item of this._items) {
      if (!inventory.hasStock(item.productId, item.quantity)) {
        throw new OutOfStockError(item.productId);
      }
      const price = pricingRules.calculatePrice(item.productId, item.quantity);
      item.setPrice(price);
    }
    inventory.reserveAll(this._items);  // Order modifying inventory!
    this._status = OrderStatus.Submitted;
  }
}
```

✅ **Good: Domain service coordinating multiple aggregates**

```typescript
class OrderSubmissionService {
  constructor(
    private inventoryService: InventoryAvailabilityService,
    private pricingService: PricingService
  ) {}

  async submit(order: Order): Promise<void> {
    // Check inventory (reads from Inventory aggregate)
    for (const item of order.items) {
      const available = await this.inventoryService.checkAvailability(
        item.productId,
        item.quantity
      );
      if (!available) {
        throw new InsufficientStockError(item.productId);
      }
    }

    // Calculate final prices (might involve discount rules across items)
    const finalTotal = await this.pricingService.calculateTotal(order.items);

    // Submit the order (entity handles its own state transition)
    order.submit(finalTotal);
  }
}
```

**Rule:** Domain services coordinate. They don't contain state. If logic involves a single aggregate, put it in the aggregate. If it spans aggregates, put it in a domain service.

---

### Pattern 18: Domain Service vs Application Service

Domain services contain business rules. Application services orchestrate use cases — they handle transactions, authorization, and coordination.

❌ **Bad: Mixing orchestration with business rules**

```typescript
class OrderApplicationService {
  async submitOrder(userId: string, orderId: string): Promise<void> {
    // Authorization (application concern)
    const user = await this.userRepo.findById(userId);
    if (!user) throw new UnauthorizedError();

    // Business rule (domain concern — should not be here)
    const order = await this.orderRepo.findById(orderId);
    if (order.total.isGreaterThan(Money.of(10000, "USD"))) {
      order.requireApproval();
    }

    // More business logic mixed with orchestration
    const inventory = await this.inventoryRepo.findByProducts(order.productIds);
    for (const item of order.items) {
      if (inventory.getStock(item.productId) < item.quantity) {
        throw new Error("Out of stock");
      }
    }

    // Transaction (application concern)
    await this.db.transaction(async () => {
      await this.orderRepo.save(order);
      await this.inventoryRepo.reserveAll(order.items);
    });
  }
}
```

✅ **Good: Clear separation**

```typescript
// Domain service — pure business logic
class OrderSubmissionService {
  async validateAndSubmit(order: Order, inventory: Inventory): void {
    // Business rules only — no database, no auth, no transactions
    inventory.ensureAvailability(order.items);
    order.submit();
  }
}

// Application service — orchestration
class SubmitOrderUseCase {
  constructor(
    private orderRepo: OrderRepository,
    private inventoryRepo: InventoryRepository,
    private submissionService: OrderSubmissionService,
    private unitOfWork: UnitOfWork
  ) {}

  async execute(request: SubmitOrderRequest): Promise<void> {
    // Load aggregates
    const order = await this.orderRepo.findById(OrderId.from(request.orderId));
    if (!order) throw new OrderNotFoundError(request.orderId);

    const inventory = await this.inventoryRepo.findByProducts(order.productIds);

    // Delegate business logic to domain service
    this.submissionService.validateAndSubmit(order, inventory);

    // Persist changes in a transaction
    await this.unitOfWork.execute(async () => {
      await this.orderRepo.save(order);
      await this.inventoryRepo.save(inventory);
    });
  }
}
```

**Rule:** Domain services have business logic, no infrastructure concerns. Application services (use cases) orchestrate: load aggregates, call domain services, persist results, handle transactions.

---

## Anti-Patterns

### Anemic Domain Model

❌ **Bad: Entities are just data bags, all logic in services**

```typescript
class Account {
  balance: number;
  status: string;
  overdraftLimit: number;
}

class AccountService {
  withdraw(account: Account, amount: number): void {
    if (account.status !== "active") throw new Error("Inactive");
    if (account.balance - amount < -account.overdraftLimit) throw new Error("Limit");
    account.balance -= amount;
  }
}
```

✅ **Good: Entity encapsulates its own rules**

```typescript
class Account {
  withdraw(amount: Money): void {
    if (!this._status.isActive()) throw new InactiveAccountError(this.id);
    if (this.wouldExceedOverdraftLimit(amount)) throw new OverdraftLimitError(this.id);
    this._balance = this._balance.subtract(amount);
  }

  private wouldExceedOverdraftLimit(amount: Money): boolean {
    const resultingBalance = this._balance.subtract(amount);
    return resultingBalance.amount < -this._overdraftLimit.amount;
  }
}
```

### Aggregate of Everything

Keep aggregates small. If loading an aggregate requires loading hundreds of related objects, the boundary is too wide. Split into smaller aggregates connected by ID references.

### Repository Overuse

Don't create repositories for value objects or child entities. Only aggregate roots get repositories. OrderItem is saved through OrderRepository, not through its own repository.

---

## Quick Reference

| Pattern | What | Key Rule |
|---------|------|----------|
| Value Object | Immutable, no identity, validated on creation | Equality by value; operations return new instances |
| Entity | Has identity, mutable state | Equality by ID; encapsulates behavior and invariants |
| Aggregate | Consistency boundary around root + children | All changes through root; reference other aggregates by ID |
| Aggregate Root | Entry point to the aggregate | External code only calls root methods |
| Repository | Persistence interface for aggregates | One per aggregate root; returns domain objects, not DB rows |
| Specification | Encapsulated query criteria | Use for complex, reusable, testable query logic |
| Domain Event | Past-tense record of something that happened | Collected during mutation, published after persistence |
| Event Handler | Reacts to domain events | Runs after originating transaction; handlers are independent |
| Domain Service | Cross-aggregate business logic | No state; coordinates entities; no infrastructure concerns |
| Application Service | Use case orchestration | Loads aggregates, calls domain services, manages transactions |
