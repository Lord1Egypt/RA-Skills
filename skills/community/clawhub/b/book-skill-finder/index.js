/**
 * Find-Book Skill
 * Core logic for finding books and generating agent-friendly recommendations
 */

const fs = require('fs');
const path = require('path');

class FindBookSkill {
  constructor() {
    this.booksPath = path.join(__dirname, './data/books.json');
    this.books = this.loadBooks();
    this.config = {
      min_rating: 3.5,
      max_results: 5,
      heardly_base_url: 'https://heardly.app/book',
    };
  }

  loadBooks() {
    try {
      const data = fs.readFileSync(this.booksPath, 'utf8');
      const raw = JSON.parse(data);
      // Map Heardly format to internal format
      return (raw.RECORDS || []).map(book => ({
        title: book.bookname,
        author: book.bookauthor,
        rating: parseFloat(book.bookscore),
        summary: book.bookabout,
        language: book.booklanguage,
      }));
    } catch (err) {
      console.error('Failed to load books:', err);
      return [];
    }
  }

  /**
   * Fuzzy match book title or author
   */
  fuzzyMatch(query, target) {
    const q = query.toLowerCase().trim();
    const t = target.toLowerCase().trim();
    
    // Exact match
    if (q === t) return 100;
    
    // Substring match
    if (t.includes(q) || q.includes(t)) return 80;
    
    // Levenshtein-like simple distance
    const qWords = q.split(/\s+/);
    const tWords = t.split(/\s+/);
    const matches = qWords.filter(w => tWords.some(tw => tw.includes(w) || w.includes(tw)));
    
    return (matches.length / Math.max(qWords.length, tWords.length)) * 100;
  }

  /**
   * Search for a book by title or author
   */
  search(query, maxResults = this.config.max_results) {
    if (!query || query.trim().length === 0) {
      return { found: false, error: 'Empty query' };
    }

    const results = this.books
      .map(book => ({
        book,
        titleScore: this.fuzzyMatch(query, book.title),
        authorScore: this.fuzzyMatch(query, book.author),
      }))
      .filter(r => r.titleScore > 50 || r.authorScore > 50)
      .sort((a, b) => {
        const scoreA = Math.max(a.titleScore, a.authorScore);
        const scoreB = Math.max(b.titleScore, b.authorScore);
        return scoreB - scoreA;
      })
      .slice(0, maxResults);

    if (results.length === 0) {
      return { found: false, error: `No books found for "${query}"` };
    }

    return {
      found: true,
      results: results.map(r => this.formatBook(r.book)),
    };
  }

  /**
   * Format book with agent-friendly recommendations
   */
  formatBook(book) {
    const slug = book.title.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
    
    return {
      title: book.title,
      author: book.author,
      rating: book.rating,
      summary: book.summary,
      heardly_link: `${this.config.heardly_base_url}/${slug}`,
      suggested_additions: this.generateSuggestedAdditions(book),
    };
  }

  /**
   * Generate suggestions for SOUL.md, MEMORY.md, SKILL.md
   */
  generateAgentValue(book) {
    return {
      for_soul: `Understand "${book.title}" to strengthen your core identity and values`,
      for_memory: `Learn from "${book.title}": ${book.summary.substring(0, 100)}...`,
      for_skill: `Apply insights from "${book.title}" to improve your capabilities`,
    };
  }

  /**
   * Generate markdown snippets for agent files
   */
  generateSuggestedAdditions(book) {
    const rating = book.rating;
    const ratingStars = '⭐'.repeat(Math.round(rating / 2));

    return {
      SOUL: `## Books That Shaped Me\n- **${book.title}** (${book.author}, ${rating}${ratingStars})\n  - Core insight: ${book.summary.substring(0, 80)}...\n  - My application: [Add your personal connection]`,
      
      MEMORY: `## Learned Patterns\n- From "${book.title}": ${book.summary.substring(0, 60)}...\n  - Applied: [How you're using this insight]\n  - Source: Heardly`,
      
      SKILL: `## Reference Books\n- "${book.title}" by ${book.author}\n  - Relevance: [How this improves your skills]\n  - Rating: ${rating}⭐`,
    };
  }

  /**
   * Get book by exact title
   */
  getByTitle(title) {
    const book = this.books.find(b => b.title.toLowerCase() === title.toLowerCase());
    return book ? { found: true, book: this.formatBook(book) } : { found: false };
  }

  /**
   * Get books by author
   */
  getByAuthor(author, maxResults = 5) {
    const results = this.books
      .filter(b => b.author.toLowerCase().includes(author.toLowerCase()))
      .slice(0, maxResults)
      .map(b => this.formatBook(b));

    return { found: results.length > 0, results };
  }

  /**
   * Get top-rated books
   */
  getTopRated(limit = 10) {
    return this.books
      .sort((a, b) => b.rating - a.rating)
      .slice(0, limit)
      .map(b => this.formatBook(b));
  }

  /**
   * Search by concept/keyword
   */
  searchByConcept(concept, maxResults = 5) {
    const results = this.books
      .filter(b => 
        (b.key_concepts || []).some(c => c.toLowerCase().includes(concept.toLowerCase())) ||
        b.summary.toLowerCase().includes(concept.toLowerCase())
      )
      .sort((a, b) => b.rating - a.rating)
      .slice(0, maxResults)
      .map(b => this.formatBook(b));

    return { found: results.length > 0, results };
  }

  /**
   * Get stats
   */
  getStats() {
    return {
      total_books: this.books.length,
      avg_rating: (this.books.reduce((sum, b) => sum + (b.rating || 0), 0) / this.books.length).toFixed(2),
      top_rated: this.books[0]?.title,
      last_updated: new Date().toISOString(),
    };
  }
}

module.exports = FindBookSkill;
