# Clean Architecture Guide

Layer-by-layer guide to implementing Clean Architecture with TypeScript. Each layer has clear responsibilities, and dependencies always point inward.

---

## Core Concept

Clean Architecture organizes code into concentric layers. The innermost layer (Entities) has zero dependencies. Each outer layer depends only on layers inside it. This is the **Dependency Rule**: source code dependencies always point inward.

```
┌─────────────────────────────────────────────────┐
│  Infrastructure (DB, HTTP, Config)              │
│  ┌─────────────────────────────────────────┐    │
│  │  Adapters (Controllers, Repos, Mappers) │    │
│  │  ┌─────────────────────────────────┐    │    │
│  │  │  Use Cases (Application Logic)  │    │    │
│  │  │  ┌─────────────────────────┐    │    │    │
│  │  │  │  Entities (Domain)      │    │    │    │
│  │  │  └─────────────────────────┘    │    │    │
│  │  └─────────────────────────────────┘    │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

Inner layers define **interfaces**. Outer layers **implement** them.

---

## Layer 1: Entities (Domain Layer)

The innermost layer contains business objects and rules that exist independent of any application. These are the core concepts of your domain.

### Pattern 1: Rich Entity

Entities encapsulate both data and behavior. An entity with only data and no methods is an "anemic model" — an anti-pattern.

❌ **Bad: Anemic entity — just a data bag**

```typescript
// Entity has no behavior — all logic lives in external services
class User {
  id: string;
  email: string;
  name: string;
  status: "active" | "suspended" | "deactivated";
  failedLoginAttempts: number;
  lastLoginAt: Date | null;
}

// Service does all the work — entity is just a struct
class UserService {
  suspend(user: User): void {
    user.status = "suspended"; // Direct mutation from outside
  }

  canLogin(user: User): boolean {
    return user.status === "active" && user.failedLoginAttempts < 5;
  }
}
```

✅ **Good: Rich entity with encapsulated behavior**

```typescript
class User {
  private constructor(
    public readonly id: UserId,
    private _email: Email,
    private _name: string,
    private _status: "active" | "suspended" | "deactivated",
    private _failedLoginAttempts: number,
    private _lastLoginAt: Date | null
  ) {}

  static create(props: { email: Email; name: string }): User {
    return new User(
      UserId.generate(),
      props.email,
      props.name,
      "active",
      0,
      null
    );
  }

  get email(): Email { return this._email; }
  get status(): string { return this._status; }

  canLogin(): boolean {
    return this._status === "active" && this._failedLoginAttempts < 5;
  }

  recordFailedLogin(): void {
    this._failedLoginAttempts++;
    if (this._failedLoginAttempts >= 5) {
      this._status = "suspended";
    }
  }

  recordSuccessfulLogin(): void {
    this._failedLoginAttempts = 0;
    this._lastLoginAt = new Date();
  }

  deactivate(): void {
    if (this._status === "deactivated") {
      throw new Error("User already deactivated");
    }
    this._status = "deactivated";
  }
}
```

**Rule:** Push behavior into entities. If a service is just getting data from an entity, deciding something, and setting data back — that logic belongs in the entity.

---

### Pattern 2: Value Objects in Entities

Value objects replace primitive types with domain-specific types that carry validation and behavior.

❌ **Bad: Primitive obsession — email as raw string**

```typescript
class User {
  email: string;

  constructor(email: string) {
    // Validation scattered across codebase
    this.email = email;
  }
}

// Validation repeated everywhere email is used
function sendEmail(email: string): void {
  if (!email.includes("@")) throw new Error("Invalid email");
  // ...
}
```

✅ **Good: Email value object with built-in validation**

```typescript
class Email {
  private readonly value: string;

  private constructor(value: string) {
    this.value = value;
  }

  static create(value: string): Email {
    if (!value || !value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
      throw new InvalidEmailError(value);
    }
    return new Email(value.toLowerCase().trim());
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }

  get domain(): string {
    return this.value.split("@")[1];
  }

  toString(): string {
    return this.value;
  }
}

// Usage in entity — impossible to have an invalid email
class User {
  constructor(
    public readonly id: UserId,
    private _email: Email  // Always valid by construction
  ) {}
}
```

**Rule:** If a primitive has validation rules, formatting behavior, or is compared for equality — wrap it in a value object. Validation happens once at creation, not everywhere the value is used.

---

### Pattern 3: Entity Identity

Entities are compared by identity (ID), not by their attributes. Two users with the same name are different users. Value objects are the opposite — compared by their content.

❌ **Bad: No clear identity semantics**

```typescript
class Product {
  name: string;
  price: number;

  equals(other: Product): boolean {
    // Comparing by attributes — is this an entity or value object?
    return this.name === other.name && this.price === other.price;
  }
}
```

✅ **Good: Entity equality by ID, value object equality by content**

```typescript
// Entity: compared by ID
class Product {
  constructor(
    public readonly id: ProductId,
    private _name: string,
    private _price: Money
  ) {}

  equals(other: Product): boolean {
    return this.id.equals(other.id);
  }
}

// Value Object: compared by content
class Money {
  constructor(
    public readonly amount: number,
    public readonly currency: string
  ) {}

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new CurrencyMismatchError(this.currency, other.currency);
    }
    return new Money(this.amount + other.amount, this.currency);
  }
}
```

**Rule:** Entities have identity (compared by ID). Value objects have no identity (compared by attributes). This distinction drives how you implement equality and persistence.

---

## Layer 2: Use Cases (Application Layer)

Use cases contain application-specific business rules. They orchestrate entities and define the application's behavior. Each use case represents a single operation the system can perform.

### Pattern 4: Use Case Structure

Each use case is a single class with an `execute` method. It takes a request DTO and returns a response DTO.

❌ **Bad: Business logic in the controller**

```typescript
class UserController {
  async createUser(req: Request, res: Response): Promise<void> {
    // Business logic mixed with HTTP handling
    const existing = await this.userRepo.findByEmail(req.body.email);
    if (existing) {
      res.status(409).json({ error: "Email taken" });
      return;
    }

    const hashedPassword = await bcrypt.hash(req.body.password, 12);
    const user = { id: uuid(), email: req.body.email, password: hashedPassword };
    await this.userRepo.save(user);
    await this.emailService.sendWelcome(user.email);

    res.status(201).json({ id: user.id, email: user.email });
  }
}
```

✅ **Good: Dedicated use case class**

```typescript
// Request and response DTOs — plain data, no framework types
interface CreateUserRequest {
  email: string;
  name: string;
  password: string;
}

interface CreateUserResponse {
  id: string;
  email: string;
  name: string;
}

class CreateUserUseCase {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly passwordHasher: PasswordHasher,
    private readonly emailNotifier: EmailNotifier
  ) {}

  async execute(request: CreateUserRequest): Promise<CreateUserResponse> {
    const email = Email.create(request.email);

    const existing = await this.userRepository.findByEmail(email);
    if (existing) {
      throw new UserAlreadyExistsError(email);
    }

    const hashedPassword = await this.passwordHasher.hash(request.password);
    const user = User.create({ email, name: request.name, hashedPassword });

    await this.userRepository.save(user);
    await this.emailNotifier.sendWelcome(email);

    return { id: user.id.toString(), email: email.toString(), name: request.name };
  }
}
```

**Rule:** One use case = one class = one `execute` method. Use cases know nothing about HTTP, CLI, or any delivery mechanism. They take plain DTOs and return plain DTOs.

---

### Pattern 5: Use Case Composition

When one operation needs logic from another, resist the urge to call one use case from another. Instead, extract shared logic into a domain service.

❌ **Bad: Use case calling another use case**

```typescript
class CreateOrderUseCase {
  constructor(private createInvoiceUseCase: CreateInvoiceUseCase) {}

  async execute(request: CreateOrderRequest): Promise<CreateOrderResponse> {
    const order = Order.create(request);
    await this.orderRepo.save(order);

    // Tightly couples two use cases — what if invoice creation fails?
    // What if CreateInvoiceUseCase needs request data we don't have?
    await this.createInvoiceUseCase.execute({ orderId: order.id });

    return { orderId: order.id };
  }
}
```

✅ **Good: Shared domain service or domain events**

```typescript
// Option 1: Domain service for shared logic
class PricingService {
  calculateOrderTotal(items: OrderItem[], discounts: Discount[]): Money {
    // Shared pricing logic used by both orders and invoices
  }
}

// Option 2: Domain events for loose coupling
class CreateOrderUseCase {
  constructor(
    private orderRepo: OrderRepository,
    private eventBus: EventBus
  ) {}

  async execute(request: CreateOrderRequest): Promise<CreateOrderResponse> {
    const order = Order.create(request);
    await this.orderRepo.save(order);

    // Publish event — invoice creation is a separate concern
    await this.eventBus.publish(new OrderCreatedEvent(order.id));

    return { orderId: order.id.toString() };
  }
}
```

**Rule:** Use cases should not call other use cases. Extract shared logic into domain services, or decouple operations with domain events.

---

### Pattern 6: Input/Output Boundaries

Use cases must not depend on delivery-mechanism types. Express Request objects, GraphQL contexts, or CLI arguments must never reach the use case layer.

❌ **Bad: Framework types leaking into use case**

```typescript
import { Request } from "express";

class GetUserUseCase {
  async execute(req: Request): Promise<any> {
    const userId = req.params.id;           // Express dependency
    const authToken = req.headers.authorization; // HTTP concept
    // ...
  }
}
```

✅ **Good: Plain DTOs at the boundary**

```typescript
// Input DTO — no framework types
interface GetUserRequest {
  userId: string;
  requesterId: string;  // Already extracted from auth token by controller
}

// Output DTO — no entity types
interface GetUserResponse {
  id: string;
  email: string;
  name: string;
  memberSince: string;
}

class GetUserUseCase {
  constructor(private userRepo: UserRepository) {}

  async execute(request: GetUserRequest): Promise<GetUserResponse> {
    const user = await this.userRepo.findById(UserId.from(request.userId));
    if (!user) throw new UserNotFoundError(request.userId);

    return {
      id: user.id.toString(),
      email: user.email.toString(),
      name: user.name,
      memberSince: user.createdAt.toISOString(),
    };
  }
}
```

**Rule:** The use case layer defines its own input/output types. Controllers map from framework types to these DTOs. Use cases never import from framework packages.

---

## Layer 3: Interface Adapters

Adapters convert data between the use case layer and the external world. Controllers translate HTTP requests into use case inputs. Repositories translate between domain objects and database records.

### Pattern 7: Controllers

Controllers are thin — they translate HTTP requests into use case calls and use case responses into HTTP responses.

❌ **Bad: Fat controller with business logic**

```typescript
class UserController {
  async updateProfile(req: Request, res: Response): Promise<void> {
    const user = await this.userRepo.findById(req.params.id);
    if (!user) { res.status(404).json({ error: "Not found" }); return; }

    // Business rules in the controller
    if (req.body.email && req.body.email !== user.email) {
      const existing = await this.userRepo.findByEmail(req.body.email);
      if (existing) { res.status(409).json({ error: "Email taken" }); return; }
      if (!this.isValidEmail(req.body.email)) {
        res.status(400).json({ error: "Invalid email" }); return;
      }
    }

    user.name = req.body.name || user.name;
    user.email = req.body.email || user.email;
    await this.userRepo.save(user);
    res.status(200).json(user);
  }
}
```

✅ **Good: Thin controller delegating to use case**

```typescript
class UserController {
  constructor(private updateProfileUseCase: UpdateProfileUseCase) {}

  async updateProfile(req: Request, res: Response): Promise<void> {
    try {
      const result = await this.updateProfileUseCase.execute({
        userId: req.params.id,
        name: req.body.name,
        email: req.body.email,
      });
      res.status(200).json(result);
    } catch (error) {
      if (error instanceof UserNotFoundError) {
        res.status(404).json({ error: error.message });
      } else if (error instanceof EmailAlreadyTakenError) {
        res.status(409).json({ error: error.message });
      } else {
        throw error;  // Let error middleware handle unexpected errors
      }
    }
  }
}
```

**Rule:** Controllers do three things: (1) extract data from the request, (2) call the use case, (3) map the result or error to an HTTP response. No business logic.

---

### Pattern 8: Presenters / Response Mapping

Entities should never be serialized directly to API responses. A presenter (or response mapper) converts domain objects to the shape the client expects.

❌ **Bad: Entity serialized directly**

```typescript
// Leaks internal state, ORM metadata, and implementation details
app.get("/users/:id", async (req, res) => {
  const user = await userRepo.findById(req.params.id);
  res.json(user); // Exposes password hash, internal IDs, etc.
});
```

✅ **Good: Presenter maps to response shape**

```typescript
class UserPresenter {
  static toResponse(user: User): UserResponse {
    return {
      id: user.id.toString(),
      email: user.email.toString(),
      displayName: user.name,
      memberSince: user.createdAt.toISOString(),
      // Omits: passwordHash, failedLoginAttempts, internal flags
    };
  }

  static toListResponse(users: User[]): UserListResponse {
    return {
      users: users.map(UserPresenter.toResponse),
      count: users.length,
    };
  }
}
```

**Rule:** Never expose domain entities to the outside world. Use presenters or response mappers to control exactly what data leaves the system.

---

### Pattern 9: Repository Implementations

The domain layer defines repository interfaces. The adapter layer implements them using specific technologies (Prisma, TypeORM, Knex, etc.).

❌ **Bad: ORM entities used as domain entities**

```typescript
// Domain layer directly depends on Prisma — can't test without database
import { PrismaClient } from "@prisma/client";

class UserService {
  constructor(private prisma: PrismaClient) {}

  async getUser(id: string) {
    // Prisma model leaked into domain — tightly coupled to ORM
    return this.prisma.user.findUnique({ where: { id } });
  }
}
```

✅ **Good: Repository maps between ORM models and domain entities**

```typescript
// Domain layer — defines what it needs
interface UserRepository {
  findById(id: UserId): Promise<User | null>;
  findByEmail(email: Email): Promise<User | null>;
  save(user: User): Promise<void>;
}

// Adapter layer — implements using Prisma
class PrismaUserRepository implements UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: UserId): Promise<User | null> {
    const record = await this.prisma.user.findUnique({
      where: { id: id.toString() },
    });
    return record ? this.toDomain(record) : null;
  }

  async save(user: User): Promise<void> {
    const data = this.toPersistence(user);
    await this.prisma.user.upsert({
      where: { id: data.id },
      create: data,
      update: data,
    });
  }

  // Maps from DB record to domain entity
  private toDomain(record: PrismaUser): User {
    return User.reconstitute({
      id: UserId.from(record.id),
      email: Email.create(record.email),
      name: record.name,
      status: record.status,
    });
  }

  // Maps from domain entity to DB record
  private toPersistence(user: User): PrismaUserData {
    return {
      id: user.id.toString(),
      email: user.email.toString(),
      name: user.name,
      status: user.status,
    };
  }
}
```

**Rule:** Repository interfaces live in the domain layer. Repository implementations live in the adapter layer. The mapping between ORM models and domain entities happens inside the repository.

---

## Layer 4: Infrastructure

The outermost layer contains framework configuration, database connections, external service clients, and the application's composition root.

### Pattern 10: Dependency Injection via Composition Root

All wiring happens in a single place — the composition root. Use cases receive their dependencies through constructor injection.

❌ **Bad: Use case creates its own dependencies**

```typescript
class CreateOrderUseCase {
  async execute(request: CreateOrderRequest): Promise<void> {
    // Creating dependencies inside the use case
    const repo = new PrismaOrderRepository(new PrismaClient());
    const emailer = new SendGridEmailService(process.env.SENDGRID_KEY!);

    // Impossible to test without real database and SendGrid
    const order = Order.create(request);
    await repo.save(order);
    await emailer.sendConfirmation(order);
  }
}
```

✅ **Good: Dependencies injected through constructor**

```typescript
// Use case receives interfaces, not implementations
class CreateOrderUseCase {
  constructor(
    private readonly orderRepo: OrderRepository,
    private readonly emailNotifier: EmailNotifier
  ) {}

  async execute(request: CreateOrderRequest): Promise<void> {
    const order = Order.create(request);
    await this.orderRepo.save(order);
    await this.emailNotifier.sendConfirmation(order);
  }
}

// Composition root — wires everything together
function createApp(): Application {
  const prisma = new PrismaClient();
  const sendgrid = new SendGridClient(config.sendgridKey);

  // Repositories
  const userRepo = new PrismaUserRepository(prisma);
  const orderRepo = new PrismaOrderRepository(prisma);

  // External services
  const emailNotifier = new SendGridEmailNotifier(sendgrid);
  const paymentGateway = new StripePaymentGateway(config.stripeKey);

  // Use cases
  const createOrder = new CreateOrderUseCase(orderRepo, emailNotifier);
  const createUser = new CreateUserUseCase(userRepo, emailNotifier);

  // Controllers
  const userController = new UserController(createUser);
  const orderController = new OrderController(createOrder);

  return new Application(userController, orderController);
}
```

**Rule:** Dependencies flow inward at the type level (use cases depend on interfaces) and are wired outward at the composition root. The composition root is the only place that knows about all implementations.

---

## Testing Strategy by Layer

Each layer has a different testing approach. Inner layers are easier to test because they have fewer dependencies.

### Entities: Pure unit tests, no mocking needed

```typescript
describe("User", () => {
  it("should suspend after 5 failed login attempts", () => {
    const user = User.create({ email: Email.create("a@b.com"), name: "Test" });

    for (let i = 0; i < 5; i++) {
      user.recordFailedLogin();
    }

    expect(user.status).toBe("suspended");
    expect(user.canLogin()).toBe(false);
  });
});
```

### Use Cases: Mock repository interfaces

```typescript
describe("CreateUserUseCase", () => {
  it("should reject duplicate emails", async () => {
    const userRepo: UserRepository = {
      findByEmail: vi.fn().mockResolvedValue(existingUser),
      save: vi.fn(),
      findById: vi.fn(),
    };

    const useCase = new CreateUserUseCase(userRepo, mockHasher, mockNotifier);

    await expect(
      useCase.execute({ email: "taken@test.com", name: "Test", password: "pw" })
    ).rejects.toThrow(UserAlreadyExistsError);

    expect(userRepo.save).not.toHaveBeenCalled();
  });
});
```

### Adapters: Integration tests with real implementations

```typescript
describe("PrismaUserRepository", () => {
  let repo: PrismaUserRepository;

  beforeAll(async () => {
    repo = new PrismaUserRepository(testPrismaClient);
  });

  it("should save and retrieve a user", async () => {
    const user = User.create({ email: Email.create("a@b.com"), name: "Test" });
    await repo.save(user);

    const found = await repo.findById(user.id);
    expect(found).not.toBeNull();
    expect(found!.email.equals(user.email)).toBe(true);
  });
});
```

---

## Dependency Rule Violations

### Violation 1: Entity importing from framework

❌ **Bad:**

```typescript
import { Column, Entity, PrimaryColumn } from "typeorm"; // Framework import!

@Entity()
class User {
  @PrimaryColumn() id: string;
  @Column() email: string;
}
```

✅ **Good:**

```typescript
// Domain entity — no decorators, no framework imports
class User {
  constructor(
    public readonly id: UserId,
    private _email: Email
  ) {}
}

// ORM entity is a separate class in the adapter layer
```

### Violation 2: Use case returning HTTP status codes

❌ **Bad:**

```typescript
class GetUserUseCase {
  async execute(id: string): Promise<{ status: 200 | 404; body: any }> {
    const user = await this.repo.findById(id);
    if (!user) return { status: 404, body: { error: "Not found" } };
    return { status: 200, body: user };
  }
}
```

✅ **Good:**

```typescript
class GetUserUseCase {
  async execute(request: GetUserRequest): Promise<GetUserResponse> {
    const user = await this.repo.findById(UserId.from(request.userId));
    if (!user) throw new UserNotFoundError(request.userId);
    return { id: user.id.toString(), email: user.email.toString(), name: user.name };
  }
}
// Controller catches UserNotFoundError and returns 404
```

### Violation 3: Circular dependencies between layers

**Detection:** If module A imports from module B, and module B imports from module A — you have a circular dependency. This usually means a layer boundary is being crossed incorrectly.

**Fix:** Extract the shared type into an inner layer that both can depend on, or use dependency inversion (define an interface in the inner layer, implement it in the outer layer).

---

## Quick Reference

| Layer | Contains | Depends On | Tested With |
|-------|----------|------------|-------------|
| Entities | Business objects, value objects, domain errors | Nothing | Pure unit tests — no mocking |
| Use Cases | Application logic, DTOs, use case interfaces | Entities | Mocked repository/service interfaces |
| Adapters | Controllers, repositories, presenters, mappers | Use Cases, Entities | Integration tests with real implementations |
| Infrastructure | DB config, framework setup, composition root | Everything | E2E tests, smoke tests |
