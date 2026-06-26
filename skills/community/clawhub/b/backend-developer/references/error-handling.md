# Error Handling Pattern

## AppError Class

```typescript
export class AppError extends Error {
  public readonly code: ErrorCode;
  public readonly httpStatus: number;

  constructor(errorCode: ErrorCode, message?: string) {
    super(ERROR_CODE[errorCode].message);
    this.message = message ?? ERROR_CODE[errorCode].message;
    this.code = ERROR_CODE[errorCode].code;
    this.httpStatus = ERROR_CODE[errorCode].httpStatus;
  }
}
```

## Service Returns Union Type

Services return either data or AppError:

```typescript
export const userService = {
  create: async (input: CreateUserDto): Promise<AppError | UserDto> => {
    const existing = await userRepository.findByEmail(input.email);
    if (existing) {
      return new AppError('CONFLICT', 'Email already registered');
    }
    
    const user = await userRepository.create(input);
    return userMapper.toDto(user);
  },
};
```

## Controller Handles AppError

```typescript
export const userController = {
  create: async (req: Request, res: Response, next: NextFunction) => {
    const result = await userService.create(req.body);
    
    // Check if service returned error
    if (result instanceof AppError) {
      next(result); // Pass to error handler middleware
      return;
    }
    
    // Otherwise respond with data
    ResponseHandler.created(res, result, 'User created');
  },
};
```

## Error Handler Middleware

```typescript
export const errorHandler: ErrorRequestHandler = (
  err: AppError | Error,
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  // Handle known AppError
  if (err instanceof AppError) {
    const response: ApiResponse<null> = {
      status: 'error',
      error: {
        code: err.code,
        message: err.message,
      },
    };
    return res.status(err.httpStatus).json(response);
  }

  // Handle JSON parse errors
  if (
    err instanceof SyntaxError &&
    'status' in err &&
    err.status === 400 &&
    'body' in err
  ) {
    const response = {
      status: 'error',
      error: {
        code: ERROR_CODE.BAD_REQUEST.code,
        message: 'Invalid JSON payload',
      },
    };
    return res.status(400).json(response);
  }

  // Unhandled error — don't expose details in production
  console.error(err.stack);
  const response: ApiResponse<null> = {
    status: 'error',
    error: {
      code: ERROR_CODE.INTERNAL_SERVER_ERROR.code,
      message: 'Internal Server Error',
    },
  };
  res.status(500).json(response);
};
```

## Prisma Error Handling

Convert Prisma errors to AppError:

```typescript
// utils/handle-prisma-error.ts
export const handlePrismaError = (error: any): AppError => {
  if (error.code === 'P2002') {
    // Unique constraint violation
    const field = error.meta?.target?.[0] || 'field';
    return new AppError('CONFLICT', `${field} already exists`);
  }
  
  if (error.code === 'P2025') {
    // Record not found
    return new AppError('NOT_FOUND', 'Record not found');
  }
  
  if (error.code === 'P2003') {
    // Foreign key constraint violation
    return new AppError('BAD_REQUEST', 'Invalid reference');
  }
  
  // Default to internal error
  return new AppError('INTERNAL_SERVER_ERROR');
};
```

**Usage in repository:**

```typescript
export const userRepository = {
  create: async (input: CreateUserDto) => {
    try {
      return await prisma.user.create({ data: input });
    } catch (error) {
      throw handlePrismaError(error);
    }
  },
};
```

**But service catches it:**

```typescript
export const userService = {
  create: async (input: CreateUserDto): Promise<AppError | UserDto> => {
    try {
      const user = await userRepository.create(input);
      return userMapper.toDto(user);
    } catch (error) {
      // Repository throws AppError; just re-throw or return
      return error as AppError;
    }
  },
};
```

## Error Codes Reference

```typescript
export const ERROR_CODE = {
  BAD_REQUEST: {
    code: 'BAD_REQUEST',
    message: 'Bad Request',
    httpStatus: 400,
  },
  UNAUTHORIZED: {
    code: 'UNAUTHORIZED',
    message: 'Unauthorized',
    httpStatus: 401,
  },
  FORBIDDEN: {
    code: 'FORBIDDEN',
    message: 'Forbidden',
    httpStatus: 403,
  },
  NOT_FOUND: {
    code: 'NOT_FOUND',
    message: 'Not Found',
    httpStatus: 404,
  },
  CONFLICT: {
    code: 'CONFLICT',
    message: 'Resource already exists',
    httpStatus: 409,
  },
  UNPROCESSABLE_ENTITY: {
    code: 'UNPROCESSABLE_ENTITY',
    message: 'Unprocessable Entity',
    httpStatus: 422,
  },
  INTERNAL_SERVER_ERROR: {
    code: 'INTERNAL_SERVER_ERROR',
    message: 'Internal Server Error',
    httpStatus: 500,
  },
  EXTERNAL_API_ERROR: {
    code: 'EXTERNAL_API_ERROR',
    message: 'External service error',
    httpStatus: 503,
  },
  TOO_MANY_REQUESTS: {
    code: 'TOO_MANY_REQUESTS',
    message: 'Too Many Requests',
    httpStatus: 429,
  },
};
```

**Add custom codes as needed** — keep them aligned with HTTP status semantics.
