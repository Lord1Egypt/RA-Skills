# Input Validation Pattern

## Joi Schema + TypeScript Type

Define both together in `[feature].request.ts`:

```typescript
import Joi from 'joi';

// Joi schema for runtime validation
export const createUserSchema = Joi.object({
  name: Joi.string().required().min(2).max(100),
  email: Joi.string().email().required(),
  phone: Joi.string().optional(),
  role: Joi.string().valid('USER', 'ADMIN').default('USER'),
  isActive: Joi.boolean().default(true),
});

// TypeScript type for compile-time safety
export type CreateUserRequest = {
  name: string;
  email: string;
  phone?: string;
  role: 'USER' | 'ADMIN';
  isActive: boolean;
};
```

## Using Schemas in Routes

```typescript
import express from 'express';
import { validate } from '../middleware/validate-request';
import { createUserSchema } from './user.request';
import { userController } from './user.controller';

export const userRoutes = express.Router();

// Validate body
userRoutes.post(
  '/',
  validate(createUserSchema, 'body'),
  catchAsync(userController.create),
);

// Validate params
userRoutes.get(
  '/:id',
  validate(Joi.object({ id: Joi.string().required() }), 'params'),
  catchAsync(userController.findById),
);

// Validate query
userRoutes.get(
  '/',
  validate(
    Joi.object({
      page: Joi.number().optional().default(1),
      perPage: Joi.number().optional().default(10),
      search: Joi.string().optional(),
    }),
    'query',
  ),
  catchAsync(userController.findAll),
);
```

## Validation Middleware Implementation

```typescript
// middleware/validate-request.ts
import Joi, { ObjectSchema } from 'joi';
import { NextFunction, Request, Response } from 'express';
import { AppError } from './error-handler';

export const validate =
  (schema: ObjectSchema, field: 'body' | 'query' | 'params') =>
  (req: Request, res: Response, next: NextFunction) => {
    const data = req[field];
    const { error, value } = schema.validate(data, {
      abortEarly: false,
      stripUnknown: true, // Remove extra fields
    });

    if (error) {
      const message = cleanJoiErrorMessage(error);
      return next(new AppError('BAD_REQUEST', message));
    }

    // Replace original with validated + cleaned data
    req[field] = value;
    next();
  };

// Clean up Joi error messages
const cleanJoiErrorMessage = (error: Joi.ValidationError): string => {
  const messages = error.details.map(detail => {
    const field = detail.path.join('.');
    return `${field}: ${detail.message}`;
  });
  return messages.join('; ');
};
```

## Common Joi Patterns

```typescript
// Strings
email: Joi.string().email().required(),
password: Joi.string().min(8).required(),
url: Joi.string().uri().required(),
phone: Joi.string().pattern(/^[0-9]{10,15}$/).optional(),

// Numbers
age: Joi.number().integer().min(0).max(150),
price: Joi.number().positive(),

// Dates
birthDate: Joi.date().max('now').required(),
eventDate: Joi.date().greater('now'),

// Arrays
tags: Joi.array().items(Joi.string()).min(1),
emails: Joi.array().items(Joi.string().email()),

// Objects
metadata: Joi.object().pattern(Joi.string(), Joi.any()),

// Enums
status: Joi.string().valid('ACTIVE', 'INACTIVE', 'PENDING'),
role: Joi.string().valid('ADMIN', 'USER'),

// Conditionals
Joi.object({
  paymentMethod: Joi.string().valid('CARD', 'BANK_TRANSFER'),
  cardNumber: Joi.when('paymentMethod', {
    is: 'CARD',
    then: Joi.string().required(),
    otherwise: Joi.forbidden(),
  }),
})

// Custom validation
username: Joi.string()
  .alphanum()
  .min(3)
  .max(30)
  .required()
  .external(async (value) => {
    const exists = await User.findByUsername(value);
    if (exists) throw new Error('Username already taken');
  }),
```

## Alternative: Zod

Some projects use Zod instead of Joi:

```typescript
import { z } from 'zod';

export const createUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  phone: z.string().optional(),
  role: z.enum(['USER', 'ADMIN']).default('USER'),
});

export type CreateUserRequest = z.infer<typeof createUserSchema>;
```

**Middleware adapted:**

```typescript
const validate = (schema: ZodSchema, field: 'body' | 'query' | 'params') =>
  (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req[field]);
    if (!result.success) {
      const message = result.error.errors
        .map(e => `${e.path.join('.')}: ${e.message}`)
        .join('; ');
      return next(new AppError('BAD_REQUEST', message));
    }
    req[field] = result.data;
    next();
  };
```

## Best Practices

1. **Define both schema AND type** — Runtime validation + compile-time safety
2. **Strip unknown fields** — Prevent injection of unexpected data
3. **Use defaults** — Joi `.default()` for optional fields
4. **Consistent error messages** — Clean Joi errors before sending to client
5. **Validate early** — In middleware, before controller layer
6. **Business validation later** — Service layer validates business rules (e.g., "email not registered"), request layer validates format
7. **Document patterns** — Comment schema intent for future maintainers
