// =============================================================================
// User Entity — Clean Architecture Domain Layer
// =============================================================================
//
// This entity belongs to the innermost layer. It has ZERO external
// dependencies — no framework imports, no database imports, no HTTP imports.
//
// The entity encapsulates business rules and invariants. External code
// interacts with the entity through its public methods.
//
// Customize: Replace this with your own domain entity.
// =============================================================================

// Value object imports are OK — they're in the same layer
// import { Email } from '../value-objects/email.value-object';
// import { UserId } from '../value-objects/user-id.value-object';

export interface UserProps {
  id: string;
  email: string;
  name: string;
  status: "active" | "suspended" | "deactivated";
  failedLoginAttempts: number;
  createdAt: Date;
}

export class User {
  private constructor(
    public readonly id: string,
    private _email: string,
    private _name: string,
    private _status: "active" | "suspended" | "deactivated",
    private _failedLoginAttempts: number,
    public readonly createdAt: Date
  ) {}

  // ---------- Factory methods ----------

  /** Create a new user. Use this for new registrations. */
  static create(props: { email: string; name: string }): User {
    return new User(
      crypto.randomUUID(),
      props.email,
      props.name,
      "active",
      0,
      new Date()
    );
  }

  /** Reconstitute from persistence. Use this in repository mappers. */
  static reconstitute(props: UserProps): User {
    return new User(
      props.id,
      props.email,
      props.name,
      props.status,
      props.failedLoginAttempts,
      props.createdAt
    );
  }

  // ---------- Getters ----------

  get email(): string {
    return this._email;
  }
  get name(): string {
    return this._name;
  }
  get status(): string {
    return this._status;
  }

  // ---------- Business behavior ----------

  /** Check if the user is allowed to log in. */
  canLogin(): boolean {
    return this._status === "active" && this._failedLoginAttempts < 5;
  }

  /** Record a failed login attempt. Suspends after 5 failures. */
  recordFailedLogin(): void {
    this._failedLoginAttempts++;
    if (this._failedLoginAttempts >= 5) {
      this._status = "suspended";
    }
  }

  /** Record a successful login. Resets failure counter. */
  recordSuccessfulLogin(): void {
    this._failedLoginAttempts = 0;
  }

  /** Deactivate the user account. */
  deactivate(): void {
    if (this._status === "deactivated") {
      throw new Error("User is already deactivated");
    }
    this._status = "deactivated";
  }

  /** Identity-based equality. Two users with the same ID are the same user. */
  equals(other: User): boolean {
    return this.id === other.id;
  }
}
