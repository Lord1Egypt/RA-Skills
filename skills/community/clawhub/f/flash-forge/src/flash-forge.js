/**
 * FlashForge — AI Flashcard Generator with Spaced Repetition
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');

class FlashForge {
  constructor(options = {}) {
    this.deckFile = options.deckFile || './flashcards.json';
    this.deck = this._load();
  }

  addCard(front, back, tags = []) {
    const card = {
      id: Date.now().toString(36) + Math.random().toString(36).slice(2, 5),
      front, back, tags,
      created: new Date().toISOString(),
      interval: 1, easeFactor: 2.5, repetitions: 0,
      nextReview: new Date().toISOString().split('T')[0]
    };
    this.deck.push(card);
    this._save();
    return card;
  }

  getDue(date) {
    const d = date || new Date().toISOString().split('T')[0];
    return this.deck.filter(c => c.nextReview <= d);
  }

  review(cardId, quality) {
    // SM-2 algorithm: quality 0-5 (0=forgot, 5=perfect)
    const card = this.deck.find(c => c.id === cardId);
    if (!card) return null;
    quality = Math.max(0, Math.min(5, Math.round(quality)));
    
    if (quality < 3) {
      card.repetitions = 0;
      card.interval = 1;
    } else {
      if (card.repetitions === 0) card.interval = 1;
      else if (card.repetitions === 1) card.interval = 6;
      else card.interval = Math.round(card.interval * card.easeFactor);
      card.repetitions++;
    }
    
    card.easeFactor = Math.max(1.3, card.easeFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)));
    const next = new Date();
    next.setDate(next.getDate() + card.interval);
    card.nextReview = next.toISOString().split('T')[0];
    this._save();
    return { nextReview: card.nextReview, interval: card.interval, easeFactor: card.easeFactor.toFixed(2) };
  }

  stats() {
    const today = new Date().toISOString().split('T')[0];
    return {
      total: this.deck.length,
      due: this.deck.filter(c => c.nextReview <= today).length,
      mastered: this.deck.filter(c => c.interval > 21).length,
      learning: this.deck.filter(c => c.interval <= 21 && c.repetitions > 0).length,
      new: this.deck.filter(c => c.repetitions === 0).length
    };
  }

  exportAnki() {
    return this.deck.map(c => `${c.front}\t${c.back}\t${c.tags.join(' ')}`).join('\n');
  }

  _load() { try { return JSON.parse(fs.readFileSync(this.deckFile, 'utf8')); } catch { return []; } }
  _save() { try { fs.writeFileSync(this.deckFile, JSON.stringify(this.deck, null, 2)); } catch {} }
}

module.exports = { FlashForge };
