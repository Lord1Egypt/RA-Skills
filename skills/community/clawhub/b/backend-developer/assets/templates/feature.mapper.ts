import { [FEATURE]Dto } from './[feature].dto';

export const [feature]Mapper = {
  toDto(entity: any): [FEATURE]Dto {
    return {
      id: entity.id,
      // Map fields from entity to DTO
      // Example:
      // name: entity.name,
      // email: entity.email,
      // isActive: entity.isActive,
      createdAt: entity.createdAt,
      updatedAt: entity.updatedAt,
    };
  },

  toDtoArray(entities: any[]): [FEATURE]Dto[] {
    return entities.map(e => this.toDto(e));
  },
};
