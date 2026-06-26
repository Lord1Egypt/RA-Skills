import { prisma } from '../../lib/prisma';

export const [feature]Repository = {
  create: async (data: any) => {
    return prisma.[feature].create({
      data,
    });
  },

  findAll: async (page: number, perPage: number, search?: string) => {
    const skip = (page - 1) * perPage;
    const where: any = {
      deletedAt: null, // Soft delete filter
    };

    // Add search filter if needed
    // if (search) {
    //   where.OR = [
    //     { name: { contains: search, mode: 'insensitive' } },
    //     { email: { contains: search, mode: 'insensitive' } },
    //   ];
    // }

    const [data, count] = await Promise.all([
      prisma.[feature].findMany({
        skip,
        take: perPage,
        where,
        orderBy: { createdAt: 'desc' },
      }),
      prisma.[feature].count({ where }),
    ]);

    return { data, count };
  },

  findById: async (id: string) => {
    return prisma.[feature].findUnique({
      where: { id, deletedAt: null },
    });
  },

  update: async (id: string, data: any) => {
    return prisma.[feature].update({
      where: { id },
      data: { ...data, updatedAt: new Date() },
    });
  },

  softDelete: async (id: string) => {
    return prisma.[feature].update({
      where: { id },
      data: { deletedAt: new Date() },
    });
  },

  hardDelete: async (id: string) => {
    return prisma.[feature].delete({
      where: { id },
    });
  },
};
