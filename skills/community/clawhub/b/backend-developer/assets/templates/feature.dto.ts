export interface [FEATURE]Dto {
  id: string;
  // Add fields from your Prisma model, excluding sensitive fields
  // Example:
  // name: string;
  // email: string;
  // isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}
