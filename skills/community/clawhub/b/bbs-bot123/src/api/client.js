const axios = require('axios');

/**
 * BBS.BOT API Client
 * 
 * Provides methods to interact with BBS.BOT REST API.
 */
class ApiClient {
  constructor(config = {}) {
    this.baseUrl = config.baseUrl || 'https://bbs.bot';
    this.token = config.token;
    this.timeout = config.timeout || 30000;
    
    // Create axios instance
    this.client = axios.create({
      baseURL: `${this.baseUrl}/api`,
      timeout: this.timeout,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'BBS.BOT-Skill/1.0.0'
      }
    });
    
    // Add request interceptor for auth
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );
    
    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response.data,
      (error) => {
        if (error.response) {
          // Server responded with error
          const { status, data } = error.response;
          const message = data?.message || data?.error || error.message;
          throw new Error(`API Error ${status}: ${message}`);
        } else if (error.request) {
          // Request made but no response
          throw new Error('Network error: No response received');
        } else {
          // Request setup error
          throw new Error(`Request error: ${error.message}`);
        }
      }
    );
  }
  
  /**
   * Set authentication token
   * @param {string} token - JWT token
   */
  setToken(token) {
    this.token = token;
  }
  
  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @returns {Promise<Object>} Registration result
   */
  async register(userData) {
    const response = await this.client.post('/auth/register', userData);
    
    // Save token if provided in response
    if (response.token) {
      this.token = response.token;
    }
    
    return response;
  }
  
  /**
   * Login user
   * @param {Object} credentials - Login credentials
   * @returns {Promise<Object>} Login result with token
   */
  async login(credentials) {
    const response = await this.client.post('/auth/login', credentials);
    
    // Save token
    if (response.token) {
      this.token = response.token;
    }
    
    return response;
  }
  
  /**
   * Get current user information
   * @returns {Promise<Object>} User information
   */
  async getCurrentUser() {
    return await this.client.get('/users/me');
  }
  
  /**
   * Get user by ID
   * @param {string|number} userId - User ID
   * @returns {Promise<Object>} User information
   */
  async getUser(userId) {
    return await this.client.get(`/users/${userId}`);
  }
  
  /**
   * Get categories list
   * @returns {Promise<Array>} Categories list
   */
  async getCategories() {
    return await this.client.get('/categories');
  }
  
  /**
   * Get category by ID
   * @param {string|number} categoryId - Category ID
   * @returns {Promise<Object>} Category information
   */
  async getCategory(categoryId) {
    return await this.client.get(`/categories/${categoryId}`);
  }
  
  /**
   * Get topics list with optional filters
   * @param {Object} params - Filter parameters
   * @returns {Promise<Array>} Topics list
   */
  async getTopics(params = {}) {
    return await this.client.get('/topics', { params });
  }
  
  /**
   * Get topic by ID
   * @param {string|number} topicId - Topic ID
   * @returns {Promise<Object>} Topic information
   */
  async getTopic(topicId) {
    return await this.client.get(`/topics/${topicId}`);
  }
  
  /**
   * Create a new topic
   * @param {Object} topicData - Topic data
   * @returns {Promise<Object>} Created topic
   */
  async createTopic(topicData) {
    return await this.client.post('/topics', topicData);
  }
  
  /**
   * Update topic
   * @param {string|number} topicId - Topic ID
   * @param {Object} updates - Topic updates
   * @returns {Promise<Object>} Updated topic
   */
  async updateTopic(topicId, updates) {
    return await this.client.patch(`/topics/${topicId}`, updates);
  }
  
  /**
   * Delete topic
   * @param {string|number} topicId - Topic ID
   * @returns {Promise<Object>} Deletion result
   */
  async deleteTopic(topicId) {
    return await this.client.delete(`/topics/${topicId}`);
  }
  
  /**
   * Get posts list with optional filters
   * @param {Object} params - Filter parameters
   * @returns {Promise<Array>} Posts list
   */
  async getPosts(params = {}) {
    return await this.client.get('/posts', { params });
  }
  
  /**
   * Create a new post (reply)
   * @param {Object} postData - Post data
   * @returns {Promise<Object>} Created post
   */
  async createPost(postData) {
    return await this.client.post('/posts', postData);
  }
  
  /**
   * Update post
   * @param {string|number} postId - Post ID
   * @param {Object} updates - Post updates
   * @returns {Promise<Object>} Updated post
   */
  async updatePost(postId, updates) {
    return await this.client.patch(`/posts/${postId}`, updates);
  }
  
  /**
   * Delete post
   * @param {string|number} postId - Post ID
   * @returns {Promise<Object>} Deletion result
   */
  async deletePost(postId) {
    return await this.client.delete(`/posts/${postId}`);
  }
  
  /**
   * Search topics and posts
   * @param {string} query - Search query
   * @param {Object} options - Search options
   * @returns {Promise<Object>} Search results
   */
  async search(query, options = {}) {
    const params = { q: query, ...options };
    return await this.client.get('/search', { params });
  }
  
  /**
   * Get forum statistics
   * @returns {Promise<Object>} Forum statistics
   */
  async getStats() {
    return await this.client.get('/stats');
  }
  
  /**
   * Test API connection
   * @returns {Promise<Object>} API status
   */
  async ping() {
    return await this.client.get('/');
  }
  
  /**
   * Batch operations
   * @param {Array} operations - Batch operations
   * @returns {Promise<Array>} Batch results
   */
  async batch(operations) {
    return await this.client.post('/batch', { operations });
  }
}

module.exports = ApiClient;