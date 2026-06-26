// =============================================================================
// Repository Interface — Clean Architecture Domain Layer
// =============================================================================
//
// This interface (port) defines what the domain needs from persistence.
// It lives in the domain layer but is IMPLEMENTED in the adapter layer.
//
// The domain says WHAT it needs. The adapter decides HOW to provide it.
//
// Key rules:
// - Uses domain types (User, not PrismaUser)
// - No mention of SQL, Prisma, MongoDB, or any specific technology
// - One repository per aggregate root
//
// Customize: Replace User with your aggregate root entity.
// =============================================================================

import { User } from "../entities/user.entity";

/**
 * Repository interface for the User aggregate.
 *
 * Implemented by:
 * - PrismaUserRepository (production — in adapters/repositories/)
 * - InMemoryUserRepository (testing)
 */
export interface UserRepository {
  /** Find a user by their unique ID. Returns null if not found. */
  findById(id: string): Promise<User | null>;

  /** Find a user by email address. Returns null if not found. */
  findByEmail(email: string): Promise<User | null>;

  /** Persist a user (create or update). */
  save(user: User): Promise<void>;

  /** Remove a user by ID. */
  delete(id: string): Promise<void>;
}
