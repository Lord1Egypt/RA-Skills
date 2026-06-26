import { AppError } from '../../middleware';
import { handlePrismaError } from '../../utils';
import { [FEATURE]Dto } from './[feature].dto';
import { [feature]Mapper } from './[feature].mapper';
import { [feature]Repository } from './[feature].repository';
import { Create[FEATURE]Request, Update[FEATURE]Request } from './[feature].request';

export const [feature]Service = {
  create: async (input: Create[FEATURE]Request): Promise<AppError | [FEATURE]Dto> => {
    try {
      // Add business logic validation here
      // Example: const existing = await [feature]Repository.findBy(input.field);
      // if (existing) return new AppError('CONFLICT', 'Already exists');

      const entity = await [feature]Repository.create(input);
      return [feature]Mapper.toDto(entity);
    } catch (error) {
      return handlePrismaError(error);
    }
  },

  findAll: async (query: any) => {
    try {
      const { page = 1, perPage = 10, search } = query;
      const result = await [feature]Repository.findAll(page, perPage, search);

      return {
        data: [feature]Mapper.toDtoArray(result.data),
        meta: {
          currentPage: page,
          totalPages: Math.ceil(result.count / perPage),
          perPage,
          totalEntries: result.count,
        },
      };
    } catch (error) {
      return handlePrismaError(error);
    }
  },

  findById: async (id: string): Promise<AppError | [FEATURE]Dto> => {
    try {
      const entity = await [feature]Repository.findById(id);
      if (!entity) {
        return new AppError('NOT_FOUND', '[FEATURE] not found');
      }
      return [feature]Mapper.toDto(entity);
    } catch (error) {
      return handlePrismaError(error);
    }
  },

  update: async (
    id: string,
    input: Update[FEATURE]Request,
  ): Promise<AppError | [FEATURE]Dto> => {
    try {
      const entity = await [feature]Repository.findById(id);
      if (!entity) {
        return new AppError('NOT_FOUND', '[FEATURE] not found');
      }

      // Add business logic validation here

      const updated = await [feature]Repository.update(id, input);
      return [feature]Mapper.toDto(updated);
    } catch (error) {
      return handlePrismaError(error);
    }
  },

  softDelete: async (id: string): Promise<AppError | null> => {
    try {
      const entity = await [feature]Repository.findById(id);
      if (!entity) {
        return new AppError('NOT_FOUND', '[FEATURE] not found');
      }

      await [feature]Repository.softDelete(id);
      return null;
    } catch (error) {
      return handlePrismaError(error);
    }
  },
};
