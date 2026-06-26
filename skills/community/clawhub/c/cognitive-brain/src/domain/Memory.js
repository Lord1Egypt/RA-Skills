/**
 * 记忆实体
 */
const { BaseEntity, ValidationError } = require('./BaseEntity');
const { CONSTANTS } = require('../utils/constants.cjs');

class Memory extends BaseEntity {
  constructor(data = {}) {
    super(data);
    this.content = data.content || '';
    this.summary = data.summary || this.generateSummary();
    this.type = data.type || 'episodic';
    this.importance = data.importance ?? 0.5;
    this.sourceChannel = data.sourceChannel || 'unknown';
    this.role = data.role || 'user';
    this.entities = data.entities || [];
    this.emotion = data.emotion || { valence: 0, arousal: 0 };
    this.intent = data.intent || null;
    this.embedding = data.embedding || null;
    this.layers = data.layers || [];
    this.accessCount = data.accessCount || 0;
    this.lastAccessed = data.lastAccessed || null;
    
    this.validate();
  }

  generateSummary() {
    if (this.content.length <= CONSTANTS.CONTENT.SUMMARY_LENGTH) return this.content;
    return this.content.substring(0, CONSTANTS.CONTENT.SUMMARY_LENGTH - 3) + '...';
  }

  validate() {
    super.validate();
    
    if (!this.content || this.content.length < CONSTANTS.CONTENT.MIN_LENGTH) {
      throw new ValidationError(`Content must be at least ${CONSTANTS.CONTENT.MIN_LENGTH} characters`, 'content');
    }

    if (this.content.length > CONSTANTS.CONTENT.MAX_LENGTH) {
      throw new ValidationError(`Content too long (max ${CONSTANTS.CONTENT.MAX_LENGTH})`, 'content');
    }
    
    const validTypes = ['episodic', 'semantic', 'working', 'sensory', 'reflection', 'lesson', 'milestone', 'test'];
    if (!validTypes.includes(this.type)) {
      throw new ValidationError(`Invalid type: ${this.type}`, 'type');
    }
    
    if (this.importance < 0 || this.importance > 1) {
      throw new ValidationError('Importance must be between 0 and 1', 'importance');
    }
  }

  updateImportance(delta) {
    this.importance = Math.max(0, Math.min(1, this.importance + delta));
    this.updatedAt = new Date();
  }

  markAccessed() {
    this.accessCount++;
    this.lastAccessed = new Date();
    this.updatedAt = new Date();
  }

  toJSON() {
    return {
      ...super.toJSON(),
      content: this.content,
      summary: this.summary,
      type: this.type,
      importance: this.importance,
      sourceChannel: this.sourceChannel,
      role: this.role,
      entities: this.entities,
      emotion: this.emotion,
      intent: this.intent,
      embedding: this.embedding,
      layers: this.layers,
      accessCount: this.accessCount,
      lastAccessed: this.lastAccessed
    };
  }

  static fromRow(row) {
    return new Memory({
      id: row.id,
      content: row.content,
      summary: row.summary,
      type: row.type,
      importance: parseFloat(row.importance),
      sourceChannel: row.source_channel,
      role: row.role,
      entities: row.entities || [],
      emotion: row.emotion || { valence: 0, arousal: 0 },
      intent: row.intent,
      embedding: row.embedding,
      layers: row.layers || [],
      accessCount: row.access_count || 0,
      lastAccessed: row.last_accessed,
      createdAt: row.created_at,
      updatedAt: row.timestamp
    });
  }
}

module.exports = { Memory };

