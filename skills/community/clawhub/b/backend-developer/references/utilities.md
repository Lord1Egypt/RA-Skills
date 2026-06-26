# Utilities & Helper Functions

## ResponseHandler

Format consistent JSON responses:

```typescript
// utils/response-handler.ts
import { Response, NextFunction } from 'express';
import { AppError } from '../middleware';
import { ERROR_CODE, ApiResponse } from '../interface';

export const ResponseHandler = {
  // Success response with 200 status
  ok<T, M = null>(res: Response, data: T, message = 'Success', meta?: M) {
    const response: ApiResponse<T> = {
      status: 'success',
      message,
      data,
      ...(meta && { meta }),
    };
    return res.status(200).json(response);
  },

  // Created response with 201 status
  created<T>(res: Response, data: T, message = 'Created') {
    const response: ApiResponse<T> = {
      status: 'success',
      message,
      data,
    };
    return res.status(201).json(response);
  },

  // Error helpers — create AppError and pass to next()
  badRequest(next: NextFunction, message = ERROR_CODE.BAD_REQUEST.message) {
    next(new AppError('BAD_REQUEST', message));
  },

  unauthorized(next: NextFunction, message = ERROR_CODE.UNAUTHORIZED.message) {
    next(new AppError('UNAUTHORIZED', message));
  },

  forbidden(next: NextFunction, message = ERROR_CODE.FORBIDDEN.message) {
    next(new AppError('FORBIDDEN', message));
  },

  notFound(next: NextFunction, message = ERROR_CODE.NOT_FOUND.message) {
    next(new AppError('NOT_FOUND', message));
  },

  conflict(next: NextFunction, message = 'Resource already exists') {
    next(new AppError('CONFLICT', message));
  },

  internalServerError(
    next: NextFunction,
    message = ERROR_CODE.INTERNAL_SERVER_ERROR.message,
  ) {
    next(new AppError('INTERNAL_SERVER_ERROR', message));
  },
};
```

## catchAsync — Promise Error Wrapper

Wrap async route handlers to catch unhandled promise rejections:

```typescript
// utils/catch-async.ts
import { NextFunction, Request, RequestHandler, Response } from 'express';

export const catchAsync =
  (fn: RequestHandler) =>
  (req: Request, res: Response, next: NextFunction) =>
    Promise.resolve(fn(req, res, next)).catch(next);
```

**Usage in routes:**

```typescript
// Before: manual try-catch
routes.post('/', (req, res, next) => {
  try {
    const result = await service.create(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
});

// After: catchAsync wrapper
routes.post('/', catchAsync(async (req, res) => {
  const result = await service.create(req.body);
  res.json(result);
}));
```

## Prisma Error Handler

Convert Prisma-specific errors to AppError:

```typescript
// utils/handle-prisma-error.ts
import { PrismaClientKnownRequestError } from '@prisma/client/runtime/library';
import { AppError } from '../middleware';

export const handlePrismaError = (error: any): AppError => {
  if (!(error instanceof PrismaClientKnownRequestError)) {
    return new AppError('INTERNAL_SERVER_ERROR');
  }

  switch (error.code) {
    case 'P2002':
      // Unique constraint violation
      const field = error.meta?.target?.[0] || 'field';
      return new AppError('CONFLICT', `${field} already exists`);

    case 'P2025':
      // Record not found (e.g., deleteMany with non-existent id)
      return new AppError('NOT_FOUND', 'Record not found');

    case 'P2003':
      // Foreign key constraint violation
      return new AppError('BAD_REQUEST', 'Invalid reference to related record');

    case 'P2014':
      // Required relation violation
      return new AppError('BAD_REQUEST', 'Cannot perform operation on related records');

    case 'P2016':
      // Query interpretation error
      return new AppError('BAD_REQUEST', 'Invalid query');

    case 'P2028':
      // Transaction API error
      return new AppError('INTERNAL_SERVER_ERROR', 'Transaction failed');

    default:
      console.error('Unhandled Prisma error:', error.code, error.message);
      return new AppError('INTERNAL_SERVER_ERROR');
  }
};
```

**Common Prisma Error Codes:**

| Code | Meaning | HTTP Status |
|------|---------|------------|
| P2002 | Unique constraint violation | 409 Conflict |
| P2025 | Record not found | 404 Not Found |
| P2003 | Foreign key violation | 400 Bad Request |
| P2014 | Required relation violation | 400 Bad Request |
| P2016 | Query interpretation error | 400 Bad Request |
| P2028 | Transaction error | 500 Internal Error |

## Clean Joi Error Messages

Sanitize Joi validation errors for client response:

```typescript
// utils/clean-joi-error-message.ts
import Joi from 'joi';

export const cleanJoiErrorMessage = (error: Joi.ValidationError): string => {
  const messages = error.details.map(detail => {
    const field = detail.path.join('.');
    const label = detail.context?.label || field;
    return `${label}: ${detail.message.replace(/"/g, '')}`;
  });
  return messages.join('; ');
};

// Example:
// Input: "name" is required
// Output: name: is required
```

## Query Builder Helper

Type-safe Prisma query with optional filters:

```typescript
// utils/prisma-query.ts
import { Prisma } from '@prisma/client';

export const buildQuery = <T extends Record<string, any>>(
  filters: T,
): { where: Prisma.UserWhereInput } => {
  const where: Prisma.UserWhereInput = {};

  if (filters.search) {
    where.OR = [
      { name: { contains: filters.search, mode: 'insensitive' } },
      { email: { contains: filters.search, mode: 'insensitive' } },
    ];
  }

  if (filters.status) {
    where.status = filters.status;
  }

  if (filters.isActive !== undefined) {
    where.isActive = filters.isActive;
  }

  return { where };
};
```

## Pagination Helper

Reusable pagination logic:

```typescript
// utils/paginate.ts
export interface PaginationParams {
  page: number;
  perPage: number;
}

export interface PaginationMeta {
  currentPage: number;
  totalPages: number;
  perPage: number;
  totalEntries: number;
}

export const calculatePagination = (
  totalCount: number,
  page: number,
  perPage: number,
): PaginationMeta => {
  return {
    currentPage: page,
    totalPages: Math.ceil(totalCount / perPage),
    perPage,
    totalEntries: totalCount,
  };
};

export const getPaginationSkip = (page: number, perPage: number) =>
  (page - 1) * perPage;
```

**Usage in repository:**

```typescript
export const userRepository = {
  findAll: async (page: number, perPage: number) => {
    const skip = getPaginationSkip(page, perPage);
    const [data, count] = await Promise.all([
      prisma.user.findMany({ skip, take: perPage }),
      prisma.user.count(),
    ]);
    return {
      data,
      meta: calculatePagination(count, page, perPage),
    };
  },
};
```

## Logger Helper

Simple request/response logging:

```typescript
// utils/logger.ts
import { Request, Response, NextFunction } from 'express';

export const requestLogger = (req: Request, res: Response, next: NextFunction) => {
  const start = Date.now();
  const path = `${req.method} ${req.path}`;

  res.on('finish', () => {
    const duration = Date.now() - start;
    const status = res.statusCode;
    const level = status >= 400 ? 'error' : 'info';
    console.log(
      `[${level.toUpperCase()}] ${path} ${status} ${duration}ms`,
    );
  });

  next();
};
```

## Environment Config

Centralized env loading with type safety:

```typescript
// config/config.ts
import dotenv from 'dotenv';

dotenv.config();

export const config = {
  NODE_ENV: process.env.NODE_ENV || 'development',
  PORT: parseInt(process.env.PORT || '3000'),
  DB_URL: process.env.DATABASE_URL || '',
  JWT_SECRET: process.env.JWT_SECRET || '',
  JWT_EXPIRE: process.env.JWT_EXPIRE || '24h',
  LOG_LEVEL: process.env.LOG_LEVEL || 'info',
} as const;

// Validate required vars on startup
const required = ['DATABASE_URL', 'JWT_SECRET'];
const missing = required.filter(key => !process.env[key]);
if (missing.length) {
  throw new Error(`Missing env vars: ${missing.join(', ')}`);
}
```
