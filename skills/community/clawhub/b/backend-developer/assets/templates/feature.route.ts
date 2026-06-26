import express from 'express';
import { auth } from '../../middleware/auth-middleware';
import { validate } from '../../middleware/validate-request';
import { catchAsync } from '../../utils/catch-async';
import { [FEATURE]Controller } from './[feature].controller';
import { create[FEATURE]Schema, update[FEATURE]Schema } from './[feature].request';

export const [feature]Routes = express.Router();

// Create [feature]
[feature]Routes.post(
  '/',
  auth('ACCESS', ['ADMIN']),
  validate(create[FEATURE]Schema, 'body'),
  catchAsync([FEATURE]Controller.create),
);

// Get all [features]
[feature]Routes.get(
  '/',
  auth('ACCESS', ['ADMIN', 'USER']),
  validate(
    // Add query validation schema if needed
    // validate(query[FEATURE]Schema, 'query'),
  ),
  catchAsync([FEATURE]Controller.findAll),
);

// Get [feature] by ID
[feature]Routes.get(
  '/:id',
  auth('ACCESS', ['ADMIN', 'USER']),
  catchAsync([FEATURE]Controller.findById),
);

// Update [feature]
[feature]Routes.put(
  '/:id',
  auth('ACCESS', ['ADMIN']),
  validate(update[FEATURE]Schema, 'body'),
  catchAsync([FEATURE]Controller.update),
);

// Delete [feature]
[feature]Routes.delete(
  '/:id',
  auth('ACCESS', ['ADMIN']),
  catchAsync([FEATURE]Controller.softDelete),
);
