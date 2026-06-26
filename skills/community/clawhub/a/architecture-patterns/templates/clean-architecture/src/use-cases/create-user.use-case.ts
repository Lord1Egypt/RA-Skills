// =============================================================================
// Create User Use Case — Clean Architecture Application Layer
// =============================================================================
//
// Use cases contain application-specific business logic. They orchestrate
// entities and repository interfaces to accomplish a specific task.
//
// This layer imports from domain/ only — never from adapters/ or infrastructure/.
//
// Key rules:
// - One class per use case with a single execute() method
// - Takes a plain DTO as input, returns a plain DTO as output
// - No framework types (no Express Request, no Prisma types)
// - Dependencies injected through constructor (interfaces, not implementations)
//
// Customize: Replace with your own use case. Follow the same structure.
// =============================================================================

import { User } from "../domain/entities/user.entity";
import { UserRepository } from "../domain/interfaces/repository.interface";

// ---------- Request / Response DTOs ----------
// Plain objects — no framework dependencies, no entity references

export interface CreateUserRequest {
  email: string;
  name: string;
}

export interface CreateUserResponse {
  id: string;
  email: string;
  name: string;
}

// ---------- Use Case ----------

export class CreateUserUseCase {
  constructor(
    // Depends on the interface, not the implementation.
    // PrismaUserRepository or InMemoryUserRepository — doesn't matter here.
    private readonly userRepository: UserRepository
  ) {}

  async execute(request: CreateUserRequest): Promise<CreateUserResponse> {
    // 1. Validate business rules
    const existingUser = await this.userRepository.findByEmail(request.email);
    if (existingUser) {
      throw new UserAlreadyExistsError(request.email);
    }

    // 2. Create domain entity (entity handles its own validation)
    const user = User.create({
      email: request.email,
      name: request.name,
    });

    // 3. Persist through repository interface
    await this.userRepository.save(user);

    // 4. Return response DTO (not the entity itself)
    return {
      id: user.id,
      email: user.email,
      name: user.name,
    };
  }
}

// ---------- Domain Error ----------
// Errors are domain concepts — they describe what went wrong in business terms.

export class UserAlreadyExistsError extends Error {
  constructor(email: string) {
    super(`A user with email "${email}" already exists`);
    this.name = "UserAlreadyExistsError";
  }
}
