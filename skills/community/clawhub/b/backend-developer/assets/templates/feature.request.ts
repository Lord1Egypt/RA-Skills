import Joi from 'joi';

export const create[FEATURE]Schema = Joi.object({
  // Define your create request fields
  // Example:
  // name: Joi.string().required().min(2).max(100),
  // email: Joi.string().email().required(),
  // isActive: Joi.boolean().default(true),
});

export type Create[FEATURE]Request = {
  // Match your schema structure
  // Example:
  // name: string;
  // email: string;
  // isActive: boolean;
};

export const update[FEATURE]Schema = Joi.object({
  // Define your update request fields (usually optional)
  // Example:
  // name: Joi.string().optional().min(2).max(100),
  // email: Joi.string().email().optional(),
  // isActive: Joi.boolean().optional(),
});

export type Update[FEATURE]Request = Partial<Create[FEATURE]Request>;
