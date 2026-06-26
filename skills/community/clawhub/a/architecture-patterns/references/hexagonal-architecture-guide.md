# Hexagonal Architecture Guide

Ports and adapters pattern for building technology-agnostic business logic. The domain core defines interfaces (ports) that the outside world implements (adapters).

---

## Core Concept

The hexagonal architecture (Ports & Adapters) places the domain at the center. The domain communicates with the outside world exclusively through ports — interfaces defined by the domain. Adapters connect external technologies to these ports.

```
              ┌─────────────────────────┐
   REST ──────┤  Primary    ┌────────┐  ├────── PostgreSQL
   API        │  Adapter    │        │  │       Adapter
              │     ↓       │ Domain │  │         ↑
   CLI ───────┤  Primary    │  Core  │  ├────── Redis
              │  Port       │        │  │       Adapter
              │     ↓       └────────┘  │         ↑
   GraphQL ───┤  Primary      ↑    ↓    ├────── Stripe
              │  Adapter    Port  Port  │       Adapter
              └─────────────────────────┘
                  DRIVING          DRIVEN
                  (inbound)        (outbound)
```

**Key distinction:**
- **Primary (Driving) Ports**: How the outside world drives the application (HTTP, CLI, events)
- **Secondary (Driven) Ports**: What the application drives (database, email, payment)

---

## Primary Ports (Driving Side)

Primary ports define the operations that the application offers. They are implemented by the domain/application layer and called by primary adapters.

### Pattern 1: Use Case as Primary Port

The primary port is the use case interface. Primary adapters (controllers, CLI handlers) call the port to trigger application behavior.

❌ **Bad: Controller calling domain directly, bypassing the port**

```typescript
class UserController {
  constructor(
    private userRepo: PrismaUserRepository,  // Concrete class, not interface
    private hasher: BcryptHasher             // Implementation detail exposed
  ) {}

  async createUser(req: Request, res: Response): Promise<void> {
    // Controller orchestrates domain logic — it IS the use case
    const email = Email.create(req.body.email);
    const existing = await this.userRepo.findByEmail(email);
    if (existing) throw new Error("Email taken");

    const hash = await this.hasher.hash(req.body.password);
    const user = User.create({ email, name: req.body.name, passwordHash: hash });
    await this.userRepo.save(user);
    res.json({ id: user.id.toString() });
  }
}
```

✅ **Good: Controller calls primary port (use case interface)**

```typescript
// Primary port — defines what the application can do
interface CreateUserPort {
  execute(request: CreateUserRequest): Promise<CreateUserResponse>;
}

// Use case implements the port
class CreateUserUseCase implements CreateUserPort {
  constructor(
    private userRepo: UserRepository,     // Secondary port (interface)
    private hasher: PasswordHasher         // Secondary port (interface)
  ) {}

  async execute(request: CreateUserRequest): Promise<CreateUserResponse> {
    const email = Email.create(request.email);
    const existing = await this.userRepo.findByEmail(email);
    if (existing) throw new UserAlreadyExistsError(email);

    const hash = await this.hasher.hash(request.password);
    const user = User.create({ email, name: request.name, passwordHash: hash });
    await this.userRepo.save(user);

    return { id: user.id.toString(), email: email.toString() };
  }
}

// Primary adapter — calls the port
class UserController {
  constructor(private createUser: CreateUserPort) {}

  async handleCreateUser(req: Request, res: Response): Promise<void> {
    const result = await this.createUser.execute({
      email: req.body.email,
      name: req.body.name,
      password: req.body.password,
    });
    res.status(201).json(result);
  }
}
```

**Rule:** Primary ports are use case interfaces. Primary adapters call them. The domain implements them.

---

### Pattern 2: Multiple Primary Adapters

The same business logic is accessible through multiple entry points — REST API, GraphQL, CLI, message queue — without any duplication.

❌ **Bad: Business logic duplicated across entry points**

```typescript
// REST controller
class RestOrderController {
  async createOrder(req: Request, res: Response) {
    // Business logic here...
    const order = new Order(req.body.items);
    order.calculateTotal();
    await this.db.save(order);
    res.json(order);
  }
}

// CLI handler — same logic duplicated
class CliOrderCommand {
  async run(args: string[]) {
    // Same business logic copied...
    const order = new Order(parseItems(args));
    order.calculateTotal();
    await this.db.save(order);
    console.log(order);
  }
}
```

✅ **Good: Single port, multiple adapters**

```typescript
// One primary port
interface CreateOrderPort {
  execute(request: CreateOrderRequest): Promise<CreateOrderResponse>;
}

// One implementation
class CreateOrderUseCase implements CreateOrderPort {
  async execute(request: CreateOrderRequest): Promise<CreateOrderResponse> {
    const order = Order.create(request.items);
    await this.orderRepo.save(order);
    return { orderId: order.id.toString(), total: order.total.toString() };
  }
}

// Multiple primary adapters — all call the same port
class RestOrderAdapter {
  constructor(private createOrder: CreateOrderPort) {}
  async handle(req: Request, res: Response) {
    const result = await this.createOrder.execute({ items: req.body.items });
    res.status(201).json(result);
  }
}

class CliOrderAdapter {
  constructor(private createOrder: CreateOrderPort) {}
  async handle(args: string[]) {
    const result = await this.createOrder.execute({ items: parseItems(args) });
    console.log(`Order ${result.orderId} created. Total: ${result.total}`);
  }
}

class QueueOrderAdapter {
  constructor(private createOrder: CreateOrderPort) {}
  async handleMessage(message: QueueMessage) {
    await this.createOrder.execute(JSON.parse(message.body));
    await message.ack();
  }
}
```

**Rule:** Business logic lives once in the use case. Each delivery mechanism is just an adapter that translates its format into the port's format.

---

## Secondary Ports (Driven Side)

Secondary ports define what the application needs from the outside world. The domain declares these interfaces; infrastructure implements them.

### Pattern 3: Repository as Secondary Port

The most common secondary port — abstracting persistence.

❌ **Bad: Domain service importing database client directly**

```typescript
import { PrismaClient } from "@prisma/client";

class OrderService {
  private prisma = new PrismaClient();  // Infrastructure dependency

  async getOrder(id: string): Promise<Order> {
    // Domain service knows about Prisma — tightly coupled
    const record = await this.prisma.order.findUnique({
      where: { id },
      include: { items: true },
    });
    return record as Order;  // ORM model masquerading as domain entity
  }
}
```

✅ **Good: Domain defines the interface, infrastructure implements it**

```typescript
// Secondary port — defined in domain layer
interface OrderRepository {
  findById(id: OrderId): Promise<Order | null>;
  findByCustomer(customerId: CustomerId): Promise<Order[]>;
  save(order: Order): Promise<void>;
  delete(id: OrderId): Promise<void>;
}

// Secondary adapter — defined in infrastructure layer
class PrismaOrderRepository implements OrderRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: OrderId): Promise<Order | null> {
    const record = await this.prisma.order.findUnique({
      where: { id: id.toString() },
      include: { items: true },
    });
    return record ? OrderMapper.toDomain(record) : null;
  }

  async save(order: Order): Promise<void> {
    const data = OrderMapper.toPersistence(order);
    await this.prisma.order.upsert({
      where: { id: data.id },
      create: data,
      update: data,
    });
  }
}
```

**Rule:** The domain defines what persistence operations it needs. The infrastructure decides how to implement them. The domain never imports database packages.

---

### Pattern 4: External Service Ports

Abstracting external services (payment processors, notification services, etc.) behind domain-defined interfaces.

❌ **Bad: Business logic calling Stripe SDK directly**

```typescript
import Stripe from "stripe";

class PaymentService {
  private stripe = new Stripe(process.env.STRIPE_KEY!);

  async chargeCustomer(order: Order): Promise<void> {
    // Domain logic entangled with Stripe API details
    await this.stripe.charges.create({
      amount: order.total * 100,
      currency: "usd",
      source: order.paymentMethodId,
      metadata: { orderId: order.id },
    });
  }
}
```

✅ **Good: Port defines what the domain needs, adapter wraps Stripe**

```typescript
// Secondary port — domain vocabulary, not Stripe vocabulary
interface PaymentGateway {
  charge(payment: PaymentRequest): Promise<PaymentResult>;
  refund(paymentId: PaymentId, amount: Money): Promise<RefundResult>;
}

interface PaymentRequest {
  orderId: OrderId;
  amount: Money;
  paymentMethodId: string;
}

interface PaymentResult {
  paymentId: PaymentId;
  status: "succeeded" | "failed" | "pending";
}

// Secondary adapter — wraps Stripe specifics
class StripePaymentAdapter implements PaymentGateway {
  constructor(private stripe: Stripe) {}

  async charge(payment: PaymentRequest): Promise<PaymentResult> {
    const charge = await this.stripe.charges.create({
      amount: payment.amount.toCents(),
      currency: payment.amount.currency.toLowerCase(),
      source: payment.paymentMethodId,
      metadata: { orderId: payment.orderId.toString() },
    });

    return {
      paymentId: PaymentId.from(charge.id),
      status: charge.status === "succeeded" ? "succeeded" : "failed",
    };
  }

  async refund(paymentId: PaymentId, amount: Money): Promise<RefundResult> {
    const refund = await this.stripe.refunds.create({
      charge: paymentId.toString(),
      amount: amount.toCents(),
    });
    return { refundId: RefundId.from(refund.id), status: refund.status };
  }
}
```

**Rule:** Port interfaces use domain vocabulary (PaymentRequest, Money), not vendor vocabulary (Stripe.ChargeCreateParams). When you switch from Stripe to Braintree, only the adapter changes.

---

### Pattern 5: Notification Ports

Notification services (email, SMS, push) follow the same pattern — the domain defines what to notify, adapters decide how.

❌ **Bad: Use case importing nodemailer directly**

```typescript
import nodemailer from "nodemailer";

class CreateOrderUseCase {
  async execute(request: CreateOrderRequest) {
    const order = Order.create(request);
    await this.orderRepo.save(order);

    // Infrastructure concern embedded in use case
    const transporter = nodemailer.createTransport({ /* ... */ });
    await transporter.sendMail({
      to: order.customerEmail,
      subject: "Order Confirmation",
      html: `<h1>Order ${order.id}</h1>`,
    });
  }
}
```

✅ **Good: Notification port with multiple adapter options**

```typescript
// Secondary port
interface OrderNotifier {
  sendConfirmation(order: Order): Promise<void>;
  sendShippingUpdate(order: Order, trackingNumber: string): Promise<void>;
}

// Email adapter
class EmailOrderNotifier implements OrderNotifier {
  constructor(private mailer: MailService) {}

  async sendConfirmation(order: Order): Promise<void> {
    await this.mailer.send({
      to: order.customerEmail.toString(),
      template: "order-confirmation",
      data: { orderId: order.id.toString(), total: order.total.toString() },
    });
  }
}

// SMS adapter — same port, different delivery
class SmsOrderNotifier implements OrderNotifier {
  constructor(private smsClient: SmsService) {}

  async sendConfirmation(order: Order): Promise<void> {
    await this.smsClient.send({
      to: order.customerPhone.toString(),
      message: `Order ${order.id} confirmed. Total: ${order.total}`,
    });
  }
}

// Use case depends only on the port
class CreateOrderUseCase {
  constructor(
    private orderRepo: OrderRepository,
    private notifier: OrderNotifier  // Could be email, SMS, or both
  ) {}
}
```

**Rule:** The domain says "notify the customer." The adapter decides whether that means email, SMS, push notification, or all three.

---

## Adapter Implementation Patterns

### Pattern 6: Adapter with Error Translation

Infrastructure errors should not leak into the domain. Adapters catch infrastructure-specific errors and throw domain errors.

❌ **Bad: Prisma errors leaking into use cases**

```typescript
class PrismaUserRepository implements UserRepository {
  async save(user: User): Promise<void> {
    // PrismaClientKnownRequestError leaks into domain
    await this.prisma.user.create({ data: this.toPersistence(user) });
  }
}

// Use case has to catch Prisma-specific errors
class CreateUserUseCase {
  async execute(request: CreateUserRequest) {
    try {
      await this.userRepo.save(user);
    } catch (error) {
      if (error.code === "P2002") {  // Prisma unique constraint error
        throw new UserAlreadyExistsError(email);
      }
      throw error;
    }
  }
}
```

✅ **Good: Adapter translates errors to domain exceptions**

```typescript
class PrismaUserRepository implements UserRepository {
  async save(user: User): Promise<void> {
    try {
      await this.prisma.user.create({ data: this.toPersistence(user) });
    } catch (error) {
      if (error instanceof Prisma.PrismaClientKnownRequestError) {
        if (error.code === "P2002") {
          throw new DuplicateEntityError("User", user.email.toString());
        }
      }
      throw new PersistenceError("Failed to save user", { cause: error });
    }
  }
}

// Use case only handles domain errors
class CreateUserUseCase {
  async execute(request: CreateUserRequest) {
    await this.userRepo.save(user);  // Clean — no Prisma knowledge needed
  }
}
```

**Rule:** Adapters are the translation layer. Infrastructure errors go in, domain errors come out. The domain never catches infrastructure-specific exceptions.

---

### Pattern 7: Adapter Composition

Combine multiple adapters to add cross-cutting concerns like caching, logging, or retry logic using the decorator pattern.

```typescript
// Base repository adapter
class PrismaProductRepository implements ProductRepository {
  async findById(id: ProductId): Promise<Product | null> {
    const record = await this.prisma.product.findUnique({ where: { id: id.toString() } });
    return record ? ProductMapper.toDomain(record) : null;
  }
}

// Caching decorator — same interface, adds caching behavior
class CachedProductRepository implements ProductRepository {
  constructor(
    private inner: ProductRepository,
    private cache: CacheService
  ) {}

  async findById(id: ProductId): Promise<Product | null> {
    const cached = await this.cache.get<Product>(`product:${id}`);
    if (cached) return cached;

    const product = await this.inner.findById(id);
    if (product) {
      await this.cache.set(`product:${id}`, product, { ttl: 300 });
    }
    return product;
  }
}

// Composition root wires the decorators
const productRepo = new CachedProductRepository(
  new PrismaProductRepository(prisma),
  new RedisCacheService(redis)
);
```

**Rule:** Decorators add behavior (caching, logging, metrics) without modifying the adapter or the domain. Stack them at the composition root.

---

### Pattern 8: Test Adapters (Mock/Fake)

In-memory implementations of secondary ports allow unit testing use cases without real infrastructure.

```typescript
// In-memory fake — full implementation for testing
class InMemoryUserRepository implements UserRepository {
  private users = new Map<string, User>();

  async findById(id: UserId): Promise<User | null> {
    return this.users.get(id.toString()) ?? null;
  }

  async findByEmail(email: Email): Promise<User | null> {
    for (const user of this.users.values()) {
      if (user.email.equals(email)) return user;
    }
    return null;
  }

  async save(user: User): Promise<void> {
    this.users.set(user.id.toString(), user);
  }

  async delete(id: UserId): Promise<void> {
    this.users.delete(id.toString());
  }

  // Test helper
  clear(): void {
    this.users.clear();
  }
}

// Usage in tests
describe("CreateUserUseCase", () => {
  const userRepo = new InMemoryUserRepository();
  const hasher = new FakePasswordHasher();
  const notifier = new FakeEmailNotifier();

  beforeEach(() => userRepo.clear());

  it("should create a user", async () => {
    const useCase = new CreateUserUseCase(userRepo, hasher, notifier);
    const result = await useCase.execute({
      email: "test@example.com",
      name: "Test User",
      password: "password123",
    });

    const saved = await userRepo.findById(UserId.from(result.id));
    expect(saved).not.toBeNull();
    expect(saved!.email.toString()).toBe("test@example.com");
  });
});
```

**Rule:** In-memory fakes are better than mocks for repository testing. They maintain state across operations and catch bugs that mocks miss (e.g., saving then finding).

---

## Dependency Injection

### Pattern 9: Composition Root

The composition root is the single place where all adapters are wired to ports. It lives in the infrastructure layer.

❌ **Bad: Dependencies scattered across the codebase**

```typescript
// user.controller.ts
import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();
const repo = new PrismaUserRepository(prisma);
const useCase = new CreateUserUseCase(repo);

// order.controller.ts
import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();  // Second instance!
const repo = new PrismaOrderRepository(prisma);
```

✅ **Good: Single composition root**

```typescript
// src/infrastructure/composition-root.ts
export function createApplicationContext(config: AppConfig) {
  // Infrastructure
  const prisma = new PrismaClient({ datasources: { db: { url: config.dbUrl } } });
  const redis = new Redis(config.redisUrl);
  const stripe = new Stripe(config.stripeKey);

  // Secondary adapters
  const userRepo = new PrismaUserRepository(prisma);
  const orderRepo = new PrismaOrderRepository(prisma);
  const cache = new RedisCacheService(redis);
  const paymentGateway = new StripePaymentAdapter(stripe);
  const emailNotifier = new SendGridNotifier(config.sendgridKey);

  // Use cases (with dependencies injected)
  const createUser = new CreateUserUseCase(userRepo, emailNotifier);
  const createOrder = new CreateOrderUseCase(orderRepo, paymentGateway, emailNotifier);
  const getOrder = new GetOrderUseCase(new CachedOrderRepository(orderRepo, cache));

  // Primary adapters
  const userController = new UserController(createUser);
  const orderController = new OrderController(createOrder, getOrder);

  return { userController, orderController, prisma };
}

// src/main.ts
const app = express();
const ctx = createApplicationContext(loadConfig());
app.post("/users", (req, res) => ctx.userController.handleCreate(req, res));
app.post("/orders", (req, res) => ctx.orderController.handleCreate(req, res));
```

**Rule:** One file wires everything. Every class receives its dependencies through its constructor. No class creates its own dependencies.

---

### Pattern 10: Factory Functions vs DI Container

For most TypeScript projects, manual factory functions are simpler and provide better type safety than DI containers.

```typescript
// Factory function approach — simple, type-safe, explicit
function createOrderModule(deps: {
  prisma: PrismaClient;
  stripe: Stripe;
  mailer: MailService;
}) {
  const orderRepo = new PrismaOrderRepository(deps.prisma);
  const paymentGateway = new StripePaymentAdapter(deps.stripe);
  const notifier = new EmailOrderNotifier(deps.mailer);

  return {
    createOrder: new CreateOrderUseCase(orderRepo, paymentGateway, notifier),
    getOrder: new GetOrderUseCase(orderRepo),
    cancelOrder: new CancelOrderUseCase(orderRepo, paymentGateway, notifier),
  };
}
```

**Rule:** Prefer manual wiring with factory functions for projects under ~50 use cases. DI containers (tsyringe, inversify) add complexity that is only justified in very large codebases.

---

## Common Mistakes

### Mistake 1: Too Many Ports

Creating a separate interface for every single method fragments the design and adds unnecessary indirection.

❌ **Bad: One port per operation**

```typescript
interface FindUserByIdPort { findById(id: UserId): Promise<User | null>; }
interface FindUserByEmailPort { findByEmail(email: Email): Promise<User | null>; }
interface SaveUserPort { save(user: User): Promise<void>; }
interface DeleteUserPort { delete(id: UserId): Promise<void>; }
```

✅ **Good: Cohesive port interface**

```typescript
interface UserRepository {
  findById(id: UserId): Promise<User | null>;
  findByEmail(email: Email): Promise<User | null>;
  save(user: User): Promise<void>;
  delete(id: UserId): Promise<void>;
}
```

**Rule:** Group related operations into cohesive port interfaces. A repository port typically has find, save, and delete operations together.

---

### Mistake 2: Leaking Adapter Details Through Port Design

Port interfaces shaped by a specific adapter's capabilities rather than domain needs.

❌ **Bad: Port shaped by SQL capabilities**

```typescript
interface UserRepository {
  findByQuery(sql: string, params: any[]): Promise<User[]>;  // SQL leaked
  findWithJoin(table: string, on: string): Promise<User[]>;  // Join concept leaked
  executeTransaction(fn: () => Promise<void>): Promise<void>; // DB transaction leaked
}
```

✅ **Good: Port shaped by domain needs**

```typescript
interface UserRepository {
  findById(id: UserId): Promise<User | null>;
  findByEmail(email: Email): Promise<User | null>;
  findActiveUsers(): Promise<User[]>;
  save(user: User): Promise<void>;
}
```

**Rule:** Port interfaces should use domain language, not technology language. If the interface mentions SQL, HTTP, or any specific technology, it's leaking adapter details.

---

### Mistake 3: Business Logic in Adapters

Adapters translate between the outside world and the domain. They should not contain business decisions.

❌ **Bad: Adapter making business decisions**

```typescript
class PrismaOrderRepository implements OrderRepository {
  async save(order: Order): Promise<void> {
    // Business rule in the adapter!
    if (order.total.amount > 10000) {
      order.requiresApproval = true;
    }

    await this.prisma.order.create({ data: this.toPersistence(order) });
  }
}
```

✅ **Good: Adapter only translates data**

```typescript
class PrismaOrderRepository implements OrderRepository {
  async save(order: Order): Promise<void> {
    // Only translation — no business logic
    const data = OrderMapper.toPersistence(order);
    await this.prisma.order.upsert({
      where: { id: data.id },
      create: data,
      update: data,
    });
  }
}

// Business rule lives in the entity
class Order {
  get requiresApproval(): boolean {
    return this.total.isGreaterThan(Money.of(10000, "USD"));
  }
}
```

**Rule:** If you see an `if` statement in an adapter that checks a business condition, that logic belongs in the entity or use case.

---

## Quick Reference

| Concept | Description | Example |
|---------|-------------|---------|
| Primary Port | Interface for driving the application | `CreateOrderPort`, `GetUserPort` |
| Primary Adapter | Connects external trigger to port | REST Controller, CLI Handler, Queue Consumer |
| Secondary Port | Interface for driven dependencies | `OrderRepository`, `PaymentGateway` |
| Secondary Adapter | Implements driven dependency | `PrismaOrderRepo`, `StripePaymentAdapter` |
| Domain Core | Business logic and entities | `Order`, `User`, `Money` |
| Composition Root | Single place wiring adapters to ports | `createApplicationContext()` |
| Error Translation | Adapter converts infra errors to domain errors | Prisma error → `DuplicateEntityError` |
| Test Adapter | In-memory implementation for testing | `InMemoryUserRepository` |
