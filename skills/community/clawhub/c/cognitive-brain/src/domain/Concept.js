/**
 * 概念实体
 */
const { BaseEntity, ValidationError } = require('./BaseEntity');

class Concept extends BaseEntity {
  constructor(data = {}) {
    super(data);
    this.name = data.name || '';
    this.type = data.type || 'general';
    this.attributes = data.attributes || {};
    this.importance = data.importance ?? 0.5;
    this.activation = data.activation ?? 0.0;
    this.accessCount = data.accessCount || 0;
    this.lastAccessed = data.lastAccessed || null;
    this.embedding = data.embedding || null;
    
    this.validate();
  }

  validate() {
    super.validate();
    
    if (!this.name || this.name.length < 1) {
      throw new ValidationError('Concept name is required', 'name');
    }
    
    if (this.name.length > 100) {
      throw new ValidationError('Concept name too long', 'name');
    }
    
    if (this.importance < 0 || this.importance > 1) {
      throw new ValidationError('Importance must be between 0 and 1', 'importance');
    }
  }

  markAccessed() {
    this.accessCount++;
    this.lastAccessed = new Date();
    this.updatedAt = new Date();
  }

  updateActivation(value) {
    this.activation = Math.max(0, Math.min(1, value));
    this.updatedAt = new Date();
  }

  toJSON() {
    return {
      id: this.id,
      name: this.name,
      type: this.type,
      attributes: this.attributes,
      importance: this.importance,
      activation: this.activation,
      accessCount: this.accessCount,
      lastAccessed: this.lastAccessed,
      embedding: this.embedding,
      createdAt: this.createdAt,
      lastUpdated: this.updatedAt
    };
  }

  static fromRow(row) {
    return new Concept({
      id: row.id,
      name: row.name,
      type: row.type,
      attributes: row.attributes || {},
      importance: parseFloat(row.importance),
      activation: parseFloat(row.activation),
      accessCount: row.access_count || 0,
      lastAccessed: row.last_accessed,
      embedding: row.embedding,
      createdAt: row.created_at,
      updatedAt: row.last_updated
    });
  }
}

module.exports = { Concept };

