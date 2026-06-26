/**
 * 关联实体
 */
const { BaseEntity, ValidationError } = require('./BaseEntity');

class Association extends BaseEntity {
  constructor(data = {}) {
    super(data);
    this.fromId = data.fromId || null;
    this.toId = data.toId || null;
    this.type = data.type || 'related';
    this.weight = data.weight ?? 0.5;
    this.bidirectional = data.bidirectional ?? true;
    
    this.validate();
  }

  validate() {
    super.validate();
    
    if (!this.fromId) {
      throw new ValidationError('From concept id is required', 'fromId');
    }
    
    if (!this.toId) {
      throw new ValidationError('To concept id is required', 'toId');
    }
    
    if (this.fromId === this.toId) {
      throw new ValidationError('Cannot associate concept with itself', 'toId');
    }
    
    const validTypes = ['related', 'causes', 'part-of', 'instance-of', 'similar', 'opposite', 'temporal'];
    if (!validTypes.includes(this.type)) {
      throw new ValidationError(`Invalid association type: ${this.type}`, 'type');
    }
    
    if (this.weight < 0 || this.weight > 1) {
      throw new ValidationError('Weight must be between 0 and 1', 'weight');
    }
  }

  strengthen(factor = 0.1) {
    this.weight = Math.min(1, this.weight + factor);
    this.updatedAt = new Date();
  }

  weaken(factor = 0.1) {
    this.weight = Math.max(0, this.weight - factor);
    this.updatedAt = new Date();
  }

  toJSON() {
    return {
      ...super.toJSON(),
      fromId: this.fromId,
      toId: this.toId,
      type: this.type,
      weight: this.weight,
      bidirectional: this.bidirectional
    };
  }

  static fromRow(row) {
    return new Association({
      id: row.id,
      fromId: row.from_id,
      toId: row.to_id,
      type: row.type,
      weight: parseFloat(row.weight),
      bidirectional: row.bidirectional,
      createdAt: row.created_at,
      updatedAt: row.updated_at
    });
  }
}

module.exports = { Association };

