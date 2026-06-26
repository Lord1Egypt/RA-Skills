// =============================================================================
// User Controller — Clean Architecture Adapter Layer
// =============================================================================
//
// Controllers are primary adapters. They translate HTTP requests into
// use case calls, and use case responses into HTTP responses.
//
// This layer imports from use-cases/ and domain/ — it's allowed to know
// about Express, but business logic stays in the use case.
//
// Key rules:
// - Controllers are THIN — no business logic
// - Extract data from request, call use case, format response
// - Map domain errors to HTTP status codes
// - Never call repositories directly — always go through use cases
//
// Customize: Replace with your own controller. Follow the same pattern.
// =============================================================================

import { Request, Response } from "express";
import {
  CreateUserUseCase,
  UserAlreadyExistsError,
} from "../../use-cases/create-user.use-case";

export class UserController {
  constructor(
    // Controller depends on the use case, not on repositories or entities
    private readonly createUserUseCase: CreateUserUseCase
  ) {}

  /**
   * POST /users
   *
   * The controller does three things:
   * 1. Extracts data from the HTTP request
   * 2. Calls the use case with a plain DTO
   * 3. Maps the result (or error) to an HTTP response
   */
  async create(req: Request, res: Response): Promise<void> {
    try {
      // 1. Extract — translate HTTP request to use case input
      const result = await this.createUserUseCase.execute({
        email: req.body.email,
        name: req.body.name,
      });

      // 2. Respond — translate use case output to HTTP response
      res.status(201).json(result);
    } catch (error) {
      // 3. Error mapping — translate domain errors to HTTP status codes
      if (error instanceof UserAlreadyExistsError) {
        res.status(409).json({ error: error.message });
        return;
      }

      // Unexpected errors — let Express error middleware handle them
      throw error;
    }
  }
}
