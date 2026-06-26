/**
 * 领域模型基类
 */
class BaseEntity {
  constructor(data = {}) {
    this.id = data.id || this.generateId();
    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
  }

  generateId() {
    return require('crypto').randomUUID();
  }

  validate() {
    if (!this.id) {
      throw new ValidationError('Entity must have an id');
    }
  }

  toJSON() {
    return {
      id: this.id,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt
    };
  }
}

class ValidationError extends Error {
  constructor(message, field = null) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
  }
}

module.exports = { BaseEntity, ValidationError };

