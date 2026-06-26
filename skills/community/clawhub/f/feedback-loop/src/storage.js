/**
 * Storage Manager - Handles persistence of feedback data
 */
const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'data');
const FEEDBACK_FILE = path.join(DATA_DIR, 'feedback.json');
const ANALYSIS_FILE = path.join(DATA_DIR, 'analysis.json');
const SUGGESTIONS_FILE = path.join(DATA_DIR, 'suggestions.json');
const TRACKING_FILE = path.join(DATA_DIR, 'tracking.json');

class Storage {
  constructor() {
    this.ensureDataDir();
  }

  ensureDataDir() {
    if (!fs.existsSync(DATA_DIR)) {
      fs.mkdirSync(DATA_DIR, { recursive: true });
    }
  }

  readJson(filePath, defaultValue = []) {
    try {
      if (fs.existsSync(filePath)) {
        const data = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(data);
      }
    } catch (error) {
      console.error(`Error reading ${filePath}:`, error.message);
    }
    return defaultValue;
  }

  writeJson(filePath, data) {
    try {
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
      return true;
    } catch (error) {
      console.error(`Error writing ${filePath}:`, error.message);
      return false;
    }
  }

  // Feedback operations
  getAllFeedback() {
    return this.readJson(FEEDBACK_FILE, []);
  }

  addFeedback(feedback) {
    const feedbacks = this.getAllFeedback();
    feedbacks.push({
      id: this.generateId(),
      timestamp: new Date().toISOString(),
      ...feedback
    });
    return this.writeJson(FEEDBACK_FILE, feedbacks);
  }

  getFeedbackById(id) {
    const feedbacks = this.getAllFeedback();
    return feedbacks.find(f => f.id === id);
  }

  getFeedbackBySession(sessionId) {
    const feedbacks = this.getAllFeedback();
    return feedbacks.filter(f => f.sessionId === sessionId);
  }

  // Analysis operations
  getAllAnalyses() {
    return this.readJson(ANALYSIS_FILE, []);
  }

  saveAnalysis(analysis) {
    const analyses = this.getAllAnalyses();
    analyses.push({
      id: this.generateId(),
      timestamp: new Date().toISOString(),
      ...analysis
    });
    return this.writeJson(ANALYSIS_FILE, analyses);
  }

  // Suggestions operations
  getAllSuggestions() {
    return this.readJson(SUGGESTIONS_FILE, []);
  }

  saveSuggestion(suggestion) {
    const suggestions = this.getAllSuggestions();
    suggestions.push({
      id: this.generateId(),
      timestamp: new Date().toISOString(),
      status: 'pending',
      ...suggestion
    });
    return this.writeJson(SUGGESTIONS_FILE, suggestions);
  }

  updateSuggestionStatus(id, status, note = '') {
    const suggestions = this.getAllSuggestions();
    const index = suggestions.findIndex(s => s.id === id);
    if (index !== -1) {
      suggestions[index].status = status;
      suggestions[index].updatedAt = new Date().toISOString();
      if (note) {
        suggestions[index].note = note;
      }
      return this.writeJson(SUGGESTIONS_FILE, suggestions);
    }
    return false;
  }

  // Tracking operations
  getAllTracking() {
    return this.readJson(TRACKING_FILE, []);
  }

  addTrackingEntry(entry) {
    const tracking = this.getAllTracking();
    tracking.push({
      id: this.generateId(),
      timestamp: new Date().toISOString(),
      ...entry
    });
    return this.writeJson(TRACKING_FILE, tracking);
  }

  getTrackingBySuggestion(suggestionId) {
    const tracking = this.getAllTracking();
    return tracking.filter(t => t.suggestionId === suggestionId);
  }

  generateId() {
    return `fb_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // Statistics
  getStats() {
    const feedbacks = this.getAllFeedback();
    const suggestions = this.getAllSuggestions();
    const analyses = this.getAllAnalyses();

    const explicitCount = feedbacks.filter(f => f.type === 'explicit').length;
    const implicitCount = feedbacks.filter(f => f.type === 'implicit').length;

    const suggestionStatus = {
      pending: suggestions.filter(s => s.status === 'pending').length,
      implemented: suggestions.filter(s => s.status === 'implemented').length,
      rejected: suggestions.filter(s => s.status === 'rejected').length,
      in_progress: suggestions.filter(s => s.status === 'in_progress').length
    };

    return {
      totalFeedback: feedbacks.length,
      explicitFeedback: explicitCount,
      implicitFeedback: implicitCount,
      totalSuggestions: suggestions.length,
      suggestionStatus,
      totalAnalyses: analyses.length,
      lastFeedback: feedbacks.length > 0 ? feedbacks[feedbacks.length - 1].timestamp : null,
      lastAnalysis: analyses.length > 0 ? analyses[analyses.length - 1].timestamp : null
    };
  }
}

module.exports = Storage;
