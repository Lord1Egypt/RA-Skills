import { type NextFunction, type Request, type Response } from 'express';
import { AppError } from '../../middleware';
import { ResponseHandler } from '../../utils';
import { [feature]Service } from './[feature].service';

export const [FEATURE]Controller = {
  create: async (req: Request, res: Response, next: NextFunction) => {
    const { body } = req;
    const result = await [feature]Service.create(body);

    if (result instanceof AppError) {
      next(result);
      return;
    }

    ResponseHandler.created(res, result, '[FEATURE] created successfully');
  },

  findAll: async (req: Request, res: Response, next: NextFunction) => {
    const { query } = req;
    const result = await [feature]Service.findAll(query);

    if (result instanceof AppError) {
      next(result);
      return;
    }

    ResponseHandler.ok(
      res,
      result.data,
      '[FEATURES] fetched successfully',
      result.meta,
    );
  },

  findById: async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params;
    const result = await [feature]Service.findById(id);

    if (result instanceof AppError) {
      next(result);
      return;
    }

    ResponseHandler.ok(res, result, '[FEATURE] fetched successfully');
  },

  update: async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params;
    const { body } = req;
    const result = await [feature]Service.update(id, body);

    if (result instanceof AppError) {
      next(result);
      return;
    }

    ResponseHandler.ok(res, null, '[FEATURE] updated successfully');
  },

  softDelete: async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params;
    const result = await [feature]Service.softDelete(id);

    if (result instanceof AppError) {
      next(result);
      return;
    }

    ResponseHandler.ok(res, null, '[FEATURE] deleted successfully');
  },
};
