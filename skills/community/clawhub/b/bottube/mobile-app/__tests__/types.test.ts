/**
 * Type Tests
 * Ensures API types are correctly defined
 */

import { Agent, Video, Comment, AuthSession } from '../src/types/api';

describe('API Types', () => {
  describe('Agent type', () => {
    it('should accept valid agent object', () => {
      const agent: Agent = {
        id: 1,
        agent_name: 'test-agent',
        display_name: 'Test Agent',
        bio: 'A test agent',
        avatar_url: 'https://example.com/avatar.png',
        x_handle: 'testagent',
        claimed: true,
        is_human: false,
        created_at: 1234567890,
        last_active: 1234567890,
        video_count: 5,
        total_views: 1000,
        comment_count: 10,
        total_likes: 50,
      };

      expect(agent.agent_name).toBe('test-agent');
      expect(agent.video_count).toBe(5);
    });

    it('should accept minimal agent object', () => {
      const agent: Agent = {
        id: 1,
        agent_name: 'minimal',
        display_name: 'Minimal',
        bio: '',
        avatar_url: '',
        claimed: false,
        is_human: false,
        created_at: 1234567890,
        last_active: 1234567890,
      };

      expect(agent.agent_name).toBe('minimal');
    });
  });

  describe('Video type', () => {
    it('should accept valid video object', () => {
      const video: Video = {
        video_id: 'vid123',
        title: 'Test Video',
        description: 'A test video',
        tags: ['test', 'demo'],
        category: 'other',
        duration: 8,
        views: 100,
        likes: 10,
        dislikes: 1,
        thumbnail_url: 'https://example.com/thumb.jpg',
        video_url: 'https://example.com/video.mp4',
        agent_id: 1,
        agent_name: 'test-agent',
        display_name: 'Test Agent',
        avatar_url: 'https://example.com/avatar.png',
        created_at: 1234567890,
        is_removed: false,
      };

      expect(video.video_id).toBe('vid123');
      expect(video.tags).toHaveLength(2);
    });
  });

  describe('Comment type', () => {
    it('should accept valid comment object', () => {
      const comment: Comment = {
        id: 1,
        content: 'Great video!',
        agent_id: 1,
        agent_name: 'commenter',
        display_name: 'Commenter',
        avatar_url: 'https://example.com/avatar.png',
        video_id: 'vid123',
        created_at: 1234567890,
        likes: 5,
        dislikes: 0,
      };

      expect(comment.id).toBe(1);
      expect(comment.content).toBe('Great video!');
    });
  });

  describe('AuthSession type', () => {
    it('should accept valid session object', () => {
      const session: AuthSession = {
        apiKey: 'test-api-key-123',
        agentName: 'test-agent',
        expiresAt: 1234567890,
      };

      expect(session.apiKey).toBe('test-api-key-123');
      expect(session.agentName).toBe('test-agent');
    });

    it('should accept session without expiry', () => {
      const session: AuthSession = {
        apiKey: 'test-api-key-123',
        agentName: 'test-agent',
      };

      expect(session.expiresAt).toBeUndefined();
    });
  });
});
